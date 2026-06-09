import pandas as pd

def preprocess(df,region_df):


    df = df[df['Season'] == 'Summer']

    df = df.merge(
        region_df,
        on='NOC',
        how='left'
    )

    df.drop_duplicates(inplace=True)

    medals = pd.get_dummies(
        df['Medal'],
        dtype=int
    )

    df = pd.concat(
        [df, medals],
        axis=1
    )

    return df