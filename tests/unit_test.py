import src.helper as hlp
import pandas as pd

def test_preprocess_data():
    data = [
        (38,1,2,138,175,0,1,173,0,0,2,4,2,1),
        (38,1,2,138,175,0,1,173,0,0,2,4,2,1),
        (67,1,0,160,286,0,0,108,1,1.5,1,3,2,0),
        (67,1,0,120,229,0,0,129,1,2.6,1,2,3,0),     
    ]
    columns = ['age', 'sex', 'cp', 'trtbps', 'chol', 'fbs',
                'restecg', 'thalachh', 'exng', 'oldpeak',
                'slp', 'caa', 'thall', 'output']
    df = pd.DataFrame(data, columns=columns)

    df_prepared = hlp.preprocess_data(df)

    expected_data = [
        (38,1,2,138,175,0,1,173,0,0,2,4,2,1),
        (67,1,0,160,286,0,0,108,1,1.5,1,3,2,0),
        (67,1,0,120,229,0,0,129,1,2.6,1,2,3,0), 
    ]
    expected_df = pd.DataFrame(expected_data, columns=columns)

    assert df_prepared.to_dict(orient='records') == expected_df.to_dict(orient='records')