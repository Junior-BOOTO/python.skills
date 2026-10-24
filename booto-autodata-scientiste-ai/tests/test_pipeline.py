from io import BytesIO
from zipfile import ZipFile
import json
import numpy as np
import pandas as pd
import pytest
from autodata.ingestion import read_upload,validate_frame,DataError
from autodata.quality import profile
from autodata.task_router import suggest_task
from autodata.demo import make_demo
from autodata.training import run_experiment
from autodata.reports import provenance,export_zip

def test_demos():
    assert len(make_demo('classification'))==180
    assert len(make_demo('regression'))==180

def test_csv_roundtrip():
    df=make_demo('classification'); source=df.to_csv(index=False).encode()
    assert read_upload(source,'example.csv').shape==df.shape

def test_xlsx_roundtrip():
    stream=BytesIO();make_demo('regression').to_excel(stream,index=False)
    assert read_upload(stream.getvalue(),'file.xlsx').shape[0]==180

@pytest.mark.parametrize('filename', ['bad.exe','bad.csv'])
def test_invalid_data(filename):
    with pytest.raises(DataError):read_upload(b'not-a-table',filename)

def test_empty_rejected():
    with pytest.raises(DataError):validate_frame(pd.DataFrame())

def test_duplicate_columns_rejected():
    with pytest.raises(DataError):validate_frame(pd.DataFrame([[1,2]],columns=['a','a']))

def test_quality():
    df=make_demo('classification');p=profile(df)
    assert p['rows']==180 and p['missing_cells']>0 and len(p['column_details'])==5

def test_task_hint():
    assert suggest_task(pd.Series(['x','y']))=='classification'
    assert suggest_task(pd.Series(range(30)))=='regression'

def test_classification_and_regression_train():
    for task in ('classification','regression'):
        df=make_demo(task)
        result=run_experiment(df,df.columns[-1],task)
        assert len(result['comparison_cv'])==3
        assert result['train_rows']+result['test_rows']==180
        assert result['best_model'] in [d['modele'] for d in result['comparison_cv']]
        if task=='classification':
            assert 'f1_macro' in result['test_metrics'][result['best_model']]
            assert result['confusion']['matrix']
        else:
            assert 'MAE' in result['test_metrics'][result['best_model']]
        assert len(result['predictions'])==result['test_rows']

def test_same_results_same_seed():
    df=make_demo('regression');t=df.columns[-1]
    a=run_experiment(df,t,'regression')
    b=run_experiment(df,t,'regression')
    assert a['best_model']==b['best_model']
    assert a['test_metrics']==b['test_metrics']

def test_nonexistent_target():
    df=make_demo('classification')
    with pytest.raises(DataError):run_experiment(df,'invented','classification')

def test_missing_target_rejected():
    df=make_demo('regression');df.loc[0,df.columns[-1]]=np.nan
    with pytest.raises(DataError):run_experiment(df,df.columns[-1],'regression')

def test_feature_identifier_user_can_exclude():
    df=make_demo('classification');df['identifiant_unique']=np.arange(len(df))
    r=run_experiment(df,'categorie_fictive','classification',exclusions=['identifiant_unique'])
    assert 'identifiant_unique' not in r['columns_used']

def test_all_missing_feature_rejected():
    df=make_demo('classification');df['vide']=np.nan
    with pytest.raises(DataError):run_experiment(df,'categorie_fictive','classification')

def test_export_privacy_and_provenance():
    df=make_demo('classification');r=run_experiment(df,'categorie_fictive','classification')
    src=df.to_csv(index=False).encode()
    blob=export_zip(r,profile(df),provenance(src,'test.csv'))
    with ZipFile(BytesIO(blob)) as z:
        assert 'rapport.html' in z.namelist()
        assert 'manifeste.json' in z.namelist()
        assert not any('donnees/' in n for n in z.namelist())
        assert 'predictions' not in z.read('manifeste.json').decode()
        assert json.loads(z.read('manifeste.json'))['experiment']['seed']==42
