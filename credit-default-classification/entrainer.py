"""Classification pédagogique : séparation par profils, sélection et seuil sur validation."""
from pathlib import Path
import json,hashlib,urllib.request,zipfile,importlib.metadata,warnings
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.special import expit
from sklearn.model_selection import StratifiedGroupKFold
from sklearn.preprocessing import StandardScaler,OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.dummy import DummyClassifier
from sklearn.metrics import accuracy_score,precision_score,recall_score,f1_score,roc_auc_score,average_precision_score,brier_score_loss,log_loss,confusion_matrix,roc_curve,precision_recall_curve
from sklearn.calibration import calibration_curve
from sklearn.exceptions import ConvergenceWarning
ROOT=Path(__file__).resolve().parent
URL='https://archive.ics.uci.edu/static/public/350/default+of+credit+card+clients.zip'
SHA='56c885f84457f6680f8438f02bfcdac9579323d8a94465ee5f26e32baa727602'
CAT=['PAY_0','PAY_2','PAY_3','PAY_4','PAY_5','PAY_6']
NUM=['LIMIT_BAL']+[f'BILL_AMT{i}' for i in range(1,7)]+[f'PAY_AMT{i}' for i in range(1,7)]
FEATURES=NUM+CAT
TARGET='default payment next month'
def save(path,obj):path.write_text(json.dumps(obj,ensure_ascii=False,indent=2))
def score(y,p,threshold):
    predicted=(p>=threshold).astype(int);tn,fp,fn,tp=confusion_matrix(y,predicted,labels=[0,1]).ravel()
    return {'threshold':float(threshold),'accuracy':float(accuracy_score(y,predicted)),
     'precision':float(precision_score(y,predicted,zero_division=0)),'recall':float(recall_score(y,predicted,zero_division=0)),
     'f1':float(f1_score(y,predicted,zero_division=0)),'roc_auc':float(roc_auc_score(y,p)),
     'average_precision':float(average_precision_score(y,p)),'brier':float(brier_score_loss(y,p)),
     'log_loss':float(log_loss(y,p)),'TN':int(tn),'FP':int(fp),'FN':int(fn),'TP':int(tp)}
def main():
    for d in ['raw','collected','analysis','models','reports']:(ROOT/d).mkdir(exist_ok=True)
    archive=ROOT/'raw/source.zip'
    if not archive.exists():urllib.request.urlretrieve(URL,archive)
    assert hashlib.sha256(archive.read_bytes()).hexdigest()==SHA
    with zipfile.ZipFile(archive) as z:(ROOT/'raw/clients.xls').write_bytes(z.read('default of credit card clients.xls'))
    df=pd.read_excel(ROOT/'raw/clients.xls',header=1);assert len(df)==30000 and df.ID.is_unique
    assert df.isna().sum().sum()==0 and np.isfinite(df[FEATURES].to_numpy()).all()
    assert set(df[TARGET])=={0,1}
    X=df[FEATURES];y=df[TARGET].to_numpy()
    groups=pd.util.hash_pandas_object(X,index=False).to_numpy()
    duplicate_profiles=int(pd.DataFrame(X).duplicated().sum())
    development,test=next(StratifiedGroupKFold(n_splits=5,shuffle=True,random_state=42).split(X,y,groups))
    fit_local,val_local=next(StratifiedGroupKFold(n_splits=4,shuffle=True,random_state=43).split(X.iloc[development],y[development],groups[development]))
    train=development[fit_local];val=development[val_local]
    for a,b in [(train,val),(train,test),(val,test)]:assert not set(groups[a])&set(groups[b])
    parts={'train':train,'validation':val,'test':test}
    assert sum(map(len,parts.values()))==30000
    pd.DataFrame({'row':range(30000),'partition':np.select([np.isin(np.arange(30000),train),np.isin(np.arange(30000),val)],['train','validation'],default='test')}).to_csv(ROOT/'collected/decoupage.csv',index=False)
    # Statistiques apprises seulement sur train ; codes de statut conservés comme catégories.
    X.iloc[train].describe().to_csv(ROOT/'analysis/statistiques_train.csv')
    codes={name:sorted(df[name].unique().tolist()) for name in CAT}
    validation=[];models={}
    for C in [.1,1,10]:
        preparation=ColumnTransformer([('numeric',StandardScaler(),NUM),('history',OneHotEncoder(handle_unknown='ignore',sparse_output=False),CAT)])
        pipeline=Pipeline([('prepare',preparation),('logistic',LogisticRegression(C=C,max_iter=2000,solver='lbfgs'))])
        with warnings.catch_warnings():
            warnings.simplefilter('error',ConvergenceWarning);pipeline.fit(X.iloc[train],y[train])
        p=pipeline.predict_proba(X.iloc[val])[:,1]
        validation.append({'C':C,**score(y[val],p,.5)});models[C]=pipeline
    pd.DataFrame(validation).to_csv(ROOT/'analysis/comparaison_validation.csv',index=False)
    chosen=max(validation,key=lambda m:(m['average_precision'],-m['brier']));C=chosen['C'];model=models[C]
    val_probability=model.predict_proba(X.iloc[val])[:,1]
    grid=[score(y[val],val_probability,t) for t in np.round(np.arange(.05,.951,.01),2)]
    threshold=max(grid,key=lambda m:(m['f1'],m['threshold']))['threshold']
    pd.DataFrame(grid).to_csv(ROOT/'analysis/seuils_validation.csv',index=False)
    prior=DummyClassifier(strategy='prior').fit(X.iloc[train],y[train])
    # Test final : modèle et seuil sont fixés ; aucun réglage après ces résultats.
    probability=model.predict_proba(X.iloc[test])[:,1]
    final=[{'model':'Reference_classe_majoritaire','partition':'test',**score(y[test],prior.predict_proba(X.iloc[test])[:,1],.5)},
           {'model':'Logistique_seuil_0.5','partition':'test',**score(y[test],probability,.5)},
           {'model':'Logistique_seuil_validation','partition':'test',**score(y[test],probability,threshold)}]
    pd.DataFrame(final).to_csv(ROOT/'analysis/scores_test.csv',index=False)
    train_metric=score(y[train],model.predict_proba(X.iloc[train])[:,1],threshold)
    # Évaluation descriptive par sexe uniquement, sans utiliser ce champ dans le modèle.
    audit=[]
    for value in sorted(df.SEX.unique()):
        mask=df.SEX.iloc[test].to_numpy()==value
        audit.append({'SEX_source_code':int(value),'count':int(mask.sum()),'observed_default_rate':float(y[test][mask].mean()),**score(y[test][mask],probability[mask],threshold)})
    pd.DataFrame(audit).to_csv(ROOT/'analysis/audit_groupes_agrege.csv',index=False)
    bins=pd.qcut(probability,10,duplicates='drop')
    calibration=pd.DataFrame({'bin':bins,'probability':probability,'observed':y[test]}).groupby('bin',observed=True).agg(count=('observed','size'),probability_mean=('probability','mean'),observed_rate=('observed','mean'))
    calibration.to_csv(ROOT/'analysis/calibration_test.csv')
    encoder=model.named_steps['prepare'].named_transformers_['history'];scaler=model.named_steps['prepare'].named_transformers_['numeric'];lr=model.named_steps['logistic']
    exported={'model':'logistic','C':C,'numeric_features':NUM,'categorical_features':CAT,
              'mean':scaler.mean_.tolist(),'scale':scaler.scale_.tolist(),'categories':[category.tolist() for category in encoder.categories_],
              'coefficients':lr.coef_[0].tolist(),'intercept':float(lr.intercept_[0]),'threshold_validation_f1':threshold,
              'target':'Défaut de paiement au mois suivant, source historique Taïwan 2005','unknown_category':'Vecteur nul, comme handle_unknown=ignore ; usage à revoir en cas de catégorie inconnue.'}
    save(ROOT/'models/logistique.json',exported)
    loaded=json.loads((ROOT/'models/logistique.json').read_text());numeric=(X.iloc[test][NUM].to_numpy()-np.array(loaded['mean']))/np.array(loaded['scale'])
    encoded=np.column_stack([(X.iloc[test][name].to_numpy()==value).astype(float) for name,values in zip(CAT,loaded['categories']) for value in values])
    recovered=expit(np.column_stack([numeric,encoded])@np.array(loaded['coefficients'])+loaded['intercept'])
    assert np.allclose(recovered,probability,atol=1e-12)
    assert all(row['TN']+row['FP']+row['FN']+row['TP']==len(test) for row in final)
    # Exemple fictif d'API locale : valeurs inventées, pas dossier d'une personne.
    example={name:0 for name in FEATURES};example['LIMIT_BAL']=100000
    for name in CAT:example[name]=0
    save(ROOT/'reports/exemple_synthetique.json',{'features':example,'probability':float(model.predict_proba(pd.DataFrame([example]))[0,1]),'synthetic':True})
    feature_names=model.named_steps['prepare'].get_feature_names_out()
    pd.DataFrame({'encoded_feature':feature_names,'coefficient_log_odds':lr.coef_[0]}).to_csv(ROOT/'analysis/coefficients.csv',index=False)
    plt.rcParams.update({'font.family':'DejaVu Sans','axes.spines.top':False,'axes.spines.right':False})
    fig,axes=plt.subplots(1,2,figsize=(12,5));fpr,tpr,_=roc_curve(y[test],probability);axes[0].plot(fpr,tpr,color='#137e8d',label=f"ROC-AUC={final[2]['roc_auc']:.3f}");axes[0].plot([0,1],[0,1],'--',color='gray');axes[0].set(xlabel='Taux de faux positifs',ylabel='Rappel (vrais positifs)',title='ROC · Test');axes[0].legend()
    precision,recall,_=precision_recall_curve(y[test],probability);axes[1].plot(recall,precision,color='#b86951',label=f"AP={final[2]['average_precision']:.3f}");axes[1].axhline(y[test].mean(),color='gray',ls='--',label='Prévalence test');axes[1].set(xlabel='Rappel',ylabel='Précision',title='Précision–rappel · Test');axes[1].legend();fig.tight_layout();fig.savefig(ROOT/'reports/courbes.png',dpi=150);plt.close(fig)
    fig,axes=plt.subplots(1,2,figsize=(10,4.5))
    for ax,row in zip(axes,final[1:]):
        matrix=np.array([[row['TN'],row['FP']],[row['FN'],row['TP']]]);ax.imshow(matrix,cmap='Blues')
        for i in range(2):
            for j in range(2):ax.text(j,i,str(matrix[i,j]),ha='center',va='center',color='white' if matrix[i,j]>matrix.max()/2 else '#18364c',fontsize=14)
        ax.set(xticks=[0,1],xticklabels=['Sans défaut','Défaut'],yticks=[0,1],yticklabels=['Sans défaut','Défaut'],xlabel='Classe estimée',ylabel='Classe observée',title=f"Test · seuil {row['threshold']:.2f}")
    fig.tight_layout();fig.savefig(ROOT/'reports/confusions.png',dpi=150);plt.close(fig)
    fig,axes=plt.subplots(1,2,figsize=(11,4.5));axes[0].plot(calibration.probability_mean,calibration.observed_rate,'o-',color='#137e8d');axes[0].plot([0,1],[0,1],'--',color='gray');axes[0].set(xlabel='Probabilité moyenne estimée',ylabel='Fréquence observée',title='Calibration descriptive test · 10 bins quantiles',xlim=(0,1),ylim=(0,1));axes[1].plot([r['threshold'] for r in grid],[r['precision'] for r in grid],label='Précision');axes[1].plot([r['threshold'] for r in grid],[r['recall'] for r in grid],label='Rappel');axes[1].plot([r['threshold'] for r in grid],[r['f1'] for r in grid],label='F1');axes[1].axvline(threshold,color='gray',ls='--');axes[1].set(xlabel='Seuil',ylabel='Score',title='Choix du seuil · Validation uniquement',ylim=(0,1));axes[1].legend();fig.tight_layout();fig.savefig(ROOT/'reports/calibration_seuil.png',dpi=150);plt.close(fig)
    summary={'rows':30000,'positive_total':int(y.sum()),'default_rate':float(y.mean()),'missing_cells':0,'duplicate_financial_profiles':duplicate_profiles,'financial_features':19,
      'partitions':{name:{'rows':len(ix),'positives':int(y[ix].sum()),'rate':float(y[ix].mean()),'groups':len(set(groups[ix]))} for name,ix in parts.items()},
      'selected_C':C,'selected_threshold':threshold,'threshold_rule':'Maximum F1 sur validation, grille .05 à .95, pas choix économique validé.',
      'validation_selected':chosen,'test':final,'train':train_metric,'audit_aggregate':audit,'status_codes':codes,
      'calibration_ece_descriptive':float((np.abs(calibration.probability_mean-calibration.observed_rate)*calibration['count']).sum()/len(test))}
    save(ROOT/'reports/resultats.json',summary)
    versions={name:importlib.metadata.version(name) for name in ['numpy','pandas','scikit-learn','scipy','matplotlib','xlrd']};(ROOT/'requirements.txt').write_text('\n'.join(f'{k}=={v}' for k,v in versions.items())+'\n')
    manifest={'objective':'Projet 11 : régression logistique et évaluation du défaut de paiement au mois suivant.','source':URL,'source_sha256':SHA,'doi':'10.24432/C55S3H','license':'CC BY 4.0','stages':{'DataCollect':'completed','DataAnalyse':'completed','DataML':'completed'},'target':TARGET,'horizon':'Mois suivant les historiques avril–septembre 2005','excluded_features':['ID','SEX','EDUCATION','MARRIAGE','AGE'],'group_rule':'Profils identiques sur les 19 variables financières gardés ensemble, même si leurs cibles diffèrent.','split':'StratifiedGroupKFold, 1/5 test puis 1/4 du développement validation ; proportions de lignes approximatives.','preprocessing':'Standardisation montants et encodage one-hot des statuts, ajustés sur train seulement.','selection':'C par Average Precision validation puis Brier ; seuil par F1 validation','test_usage':'Évaluations après choix, aucune retouche de paramètres, seuil ou calibration.','versions':versions,'checks':['30000 IDs uniques, aucune cellule absente','Profils financiers disjoints entre train/validation/test','Convergence LogisticRegression','Matrices totalisant le nombre de tests','Export JSON reproduisant toutes les probabilités test'],'limits':['Historique Taïwan 2005','Pas validation temporelle ou externe','Codes -2 et 0 non explicités dans la description UCI : conservés distincts','Probabilités non recalibrées, fiabilité examinée descriptivement','Exclusion des variables démographiques ne prouve pas absence de biais','Aucune décision individuelle ou financière automatisée'],'next_action':'Pour usage réel, validation indépendante, gouvernance, calibration et coût des erreurs adaptés.'}
    save(ROOT/'manifest.json',manifest);print(json.dumps(summary,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
