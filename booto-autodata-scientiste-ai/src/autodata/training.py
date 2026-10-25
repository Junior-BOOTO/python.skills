"""Reproducible supervised tabular models, train-only fit and CV selection."""
import platform
import numpy as np
import pandas as pd
import sklearn
from sklearn.compose import ColumnTransformer
from sklearn.dummy import DummyClassifier, DummyRegressor
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor, ExtraTreesClassifier, ExtraTreesRegressor
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression, Ridge
from sklearn.metrics import accuracy_score, balanced_accuracy_score, f1_score, mean_absolute_error, mean_squared_error, r2_score, confusion_matrix
from sklearn.model_selection import StratifiedKFold, KFold, train_test_split, cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from .task_router import validate_task
from .ingestion import DataError, validate_frame

SEED = 42

def _metrics(task, y, pred):
    if task == 'classification':
        return {
            'accuracy': round(float(accuracy_score(y,pred)),4),
            'balanced_accuracy': round(float(balanced_accuracy_score(y,pred)),4),
            'f1_macro': round(float(f1_score(y,pred,average='macro',zero_division=0)),4),
        }
    return {
        'MAE': round(float(mean_absolute_error(y,pred)),4),
        'RMSE': round(float(np.sqrt(mean_squared_error(y,pred))),4),
        'R2': round(float(r2_score(y,pred)),4),
    }

def run_experiment(frame, target, task, exclusions=(), remove_duplicates=False):
    """Chooses model by CV on TRAIN; holds out test for final assessment only.

    Exclusions and deletion of identical rows are explicitly user-authorized.
    """
    frame = validate_frame(frame)
    cols = validate_task(frame,target,task,list(exclusions))
    if remove_duplicates:
        frame = frame.drop_duplicates().reset_index(drop=True)
        cols = validate_task(frame,target,task,list(exclusions))
    X,y=frame[cols],frame[target]
    numeric = X.select_dtypes(include=np.number).columns.tolist()
    categorical = [c for c in cols if c not in numeric]
    transformers=[]
    if numeric:
        transformers.append(('num',Pipeline([('imputer',SimpleImputer(strategy='median')),('scaler',StandardScaler())]),numeric))
    if categorical:
        transformers.append(('cat',Pipeline([('imputer',SimpleImputer(strategy='most_frequent')),('onehot',OneHotEncoder(handle_unknown='ignore'))]),categorical))
    preprocessor=ColumnTransformer(transformers)
    test_size = max(0.25, frame[target].nunique() / len(frame)) if task == 'classification' else 0.25
    X_train,X_test,y_train,y_test=train_test_split(
        X,y,test_size=test_size,random_state=SEED,stratify=y if task=='classification' else None)
    if task == 'classification':
        folds = min(5, int(y_train.value_counts().min()))
        if folds < 2:
            raise DataError('Trop peu de données par classe après séparation pour valider le modèle.')
        cv=StratifiedKFold(n_splits=folds,shuffle=True,random_state=SEED)
        constructors={
          'Référence (majorité)':lambda:DummyClassifier(strategy='most_frequent'),
          'Régression logistique':lambda:LogisticRegression(max_iter=600,random_state=SEED),
          'Logistique équilibrée':lambda:LogisticRegression(max_iter=1000,class_weight='balanced',random_state=SEED),
          'Extra Trees':lambda:ExtraTreesClassifier(n_estimators=80,max_depth=12,min_samples_leaf=2,random_state=SEED,n_jobs=1),
          'Forêt aléatoire':lambda:RandomForestClassifier(n_estimators=60,max_depth=8,random_state=SEED,n_jobs=1),
        }
        scoring='f1_macro'
    else:
        folds = 5
        cv=KFold(n_splits=folds,shuffle=True,random_state=SEED)
        constructors={
          'Référence (médiane)':lambda:DummyRegressor(strategy='median'),
          'Ridge':lambda:Ridge(alpha=1.0),
          'Ridge régularisée':lambda:Ridge(alpha=10.0),
          'Extra Trees':lambda:ExtraTreesRegressor(n_estimators=80,max_depth=12,min_samples_leaf=2,random_state=SEED,n_jobs=1),
          'Forêt aléatoire':lambda:RandomForestRegressor(n_estimators=60,max_depth=8,random_state=SEED,n_jobs=1),
        }
        scoring='neg_mean_absolute_error'
    leaderboard=[]
    selection_scores={}
    for name,create in constructors.items():
        pipe=Pipeline([('prepare',preprocessor),('model',create())])
        # The held-out test set is *not* used to select the winner.
        scores=cross_val_score(pipe,X_train,y_train,cv=cv,scoring=scoring,n_jobs=1,error_score='raise')
        selection_scores[name] = float(scores.mean())
        leaderboard.append({'modele':name, 'score_validation_train':round(float(scores.mean()),4),
                            'ecart_type_validation':round(float(scores.std()),4),
                            'mesure': 'F1 macro (plus élevé = meilleur)' if task == 'classification' else 'MAE (plus faible = meilleure)',
                            'valeur_validation':round(float(scores.mean() if task == 'classification' else -scores.mean()),4)})
    best=max(selection_scores, key=selection_scores.get)
    baseline=next(iter(constructors))
    evaluations={}
    prediction_frame=None
    for model_name in (baseline,best) if best != baseline else (baseline,):
        pipe=Pipeline([('prepare',preprocessor),('model',constructors[model_name]())])
        pipe.fit(X_train,y_train)
        pred=pipe.predict(X_test)
        evaluations[model_name]=_metrics(task,y_test,pred)
        if model_name==best:
            prediction_frame=pd.DataFrame({'observation':np.arange(1,len(pred)+1),
                                           'valeur_reelle':y_test.to_numpy(), 'prediction':pred})
    confusion=None
    if task=='classification':
        labels=sorted(y.unique().tolist(),key=str)
        confusion={'labels':[str(v) for v in labels],
                   'matrix':confusion_matrix(y_test,prediction_frame['prediction'],labels=labels).tolist()}
    return {
        'task':task,'target':target,'columns_used':cols,'columns_excluded':list(exclusions),
        'duplicates_removed':bool(remove_duplicates),'n_rows':len(frame),
        'train_rows':len(X_train),'test_rows':len(X_test),
        'best_model':best,'comparison_cv':leaderboard,'test_metrics':evaluations,
        'predictions':prediction_frame,'confusion':confusion,
        'cv_folds':folds,
        'method':f'Sélection par validation croisée {folds} plis sur le train ; test tenu à part ({len(X_test)} lignes).',
        'seed':SEED,'versions':{'python':platform.python_version(), 'pandas':pd.__version__, 'sklearn':sklearn.__version__},
        'warnings':([
            'Des doublons sont présents : ils peuvent gonfler les scores. Relancez avec suppression explicite des doublons.'
        ] if frame.duplicated().any() else []) + [
            'Exploration / prototype : aucune preuve de performance sur des données externes.',
            'Éviter identifiants, variables postérieures à l’événement et données sensibles.',
            'Données temporelles, déséquilibres et petits échantillons exigent une stratégie spécialisée.',
            'Le score du jeu de test ne doit pas guider une seconde sélection de modèle.',
        ],
    }
