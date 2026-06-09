import pandas as pd


def medal_tally(df):
    medal_tally = df.drop_duplicates(
        subset=['NOC', 'Games', 'Team', 'Year', 'City', 'Sport', 'Event', 'Medal']
    )

    medal_tally = (
        medal_tally.groupby('region')[['Gold', 'Silver', 'Bronze']]
        .sum()
        .sort_values('Gold', ascending=False)
        .reset_index()
    )

    medal_tally['Total'] = (
            medal_tally['Gold']
            + medal_tally['Silver']
            + medal_tally['Bronze']
    )

    return medal_tally


def country_year_list(df):
    years = sorted(df['Year'].unique().tolist())
    years.insert(0, 'Overall')

    countries = sorted(df['region'].dropna().unique().tolist())
    countries.insert(0, 'Overall')

    return years, countries


def fetch_medal_tally(df, Year, Country):
    medal_df = df.drop_duplicates(
        subset=[
            'NOC', 'Games', 'Team', 'Year',
            'City', 'Sport', 'Event', 'Medal'
        ]
    )

    flag = 0

    if Year == 'Overall' and Country == 'Overall':
        temp = medal_df

    elif Year == 'Overall' and Country != 'Overall':
        flag = 1
        temp = medal_df[medal_df['region'] == Country]

    elif Year != 'Overall' and Country == 'Overall':
        temp = medal_df[medal_df['Year'] == int(Year)]

    else:
        temp = medal_df[
            (medal_df['Year'] == int(Year))
            & (medal_df['region'] == Country)
            ]

    if flag == 1:
        x = (
            temp.groupby('Year')[['Gold', 'Silver', 'Bronze']]
            .sum()
            .sort_values('Year')
            .reset_index()
        )
    else:
        x = (
            temp.groupby('NOC')[['Gold', 'Silver', 'Bronze']]
            .sum()
            .sort_values('Gold', ascending=False)
            .reset_index()
        )

    x['Total'] = x['Gold'] + x['Silver'] + x['Bronze']

    return x


def participating_nations_over_time(df, col):
    x = (
        df.groupby('Year')[col]
        .nunique()
        .reset_index(name='No of Countries')
    )

    x.rename(columns={'Year': 'Edition'}, inplace=True)

    return x


def events_over_time(df, col):
    x = (
        df.groupby('Year')[col]
        .nunique()
        .reset_index(name='No of Events')
    )

    x.rename(columns={'Year': 'Edition'}, inplace=True)

    return x


def athletes_over_time(df, col):
    x = (
        df.groupby('Year')[col]
        .nunique()
        .reset_index(name='No of Athletes')
    )

    x.rename(columns={'Year': 'Edition'}, inplace=True)

    return x


def most_successful_athlete(df, sport):
    temp_df = df.dropna(subset=['Medal'])

    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == sport]

    x = (
        temp_df['Name']
        .value_counts()
        .head(15)
        .reset_index()
    )

    x.columns = ['Name', 'Medals']

    x = (
        x.merge(df, on='Name', how='left')
        [['Name', 'Medals', 'Sport', 'region']]
        .drop_duplicates()
    )

    return x


def year_wise_medal_tally2(df, country):
    temp_df = df.dropna(subset=['Medal'])

    temp_df = temp_df.drop_duplicates(
        subset=[
            'Team', 'NOC', 'Games', 'Year',
            'City', 'Sport', 'Event', 'Medal'
        ]
    )

    if country != 'Overall':
        temp_df = temp_df[temp_df['region'] == country]

    temp_df = (
        temp_df.groupby('Year')['Medal']
        .count()
        .reset_index()
    )

    return temp_df


def country_event_heatmap(df, selected_country):
    temp_df = df.dropna(subset=['Medal'])

    temp_df = temp_df.drop_duplicates(
        subset=[
            'Team', 'NOC', 'Games', 'Year',
            'City', 'Sport', 'Event', 'Medal'
        ]
    )

    if selected_country != 'Overall':
        temp_df = temp_df[temp_df['region'] == selected_country]

    x = temp_df.pivot_table(
        index='Sport',
        columns='Year',
        values='Medal',
        aggfunc='count'
    ).fillna(0)

    return x


def most_successful_athlete_countrywise(df, country):
    temp_df = df.dropna(subset=['Medal'])

    if country != 'Overall':
        temp_df = temp_df[temp_df['region'] == country]

    x = (
        temp_df['Name']
        .value_counts()
        .head(15)
        .reset_index()
    )

    x.columns = ['Name', 'Medals']

    x = (
        x.merge(df, on='Name', how='left')
        [['Name', 'Medals', 'Sport', 'region']]
        .drop_duplicates()
    )

    return x


def weightvsheight(df, sport):
    temp_df = (
        df.drop_duplicates(
            subset=['Name', 'region']
        )
        .copy()
    )

    temp_df['Medal'] = (
        temp_df['Medal']
        .fillna('NO MEDAL')
    )

    if sport != 'Overall':
        temp_df = temp_df[
            temp_df['Sport'] == sport
            ]

    return temp_df


def men_vs_women(df):
    men = (
        df[df['Sex'] == 'M']
        .groupby('Year')
        .count()['Name']
        .reset_index()
    )

    women = (
        df[df['Sex'] == 'F']
        .groupby('Year')
        .count()['Name']
        .reset_index()
    )

    final = men.merge(
        women,
        on='Year',
        how='outer'
    )

    final.rename(
        columns={
            'Name_x': 'Male',
            'Name_y': 'Female'
        },
        inplace=True
    )

    final[['Male', 'Female']] = (
        final[['Male', 'Female']]
        .fillna(0)
        .astype(int)
    )

    return final