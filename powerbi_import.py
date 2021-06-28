# Authored by A Wan, 2021. All rights reserved.
# This script creates a dataframe, df, used by the PowerBI file covid_visualizations.pbix
import requests
import pandas

# Constants
on_age_groups = {"0-17": 2762885, "18-29": 2455535, "30-39": 2056059, "40-49": 1876583, "50-59": 2060934,
                 "60-69": 1795046, "70-79": 1159902, "80+": 679266, 'all_ages': 14789778, 'adults': 12026893}

age_ranges = ["0-17", "18-29", "30-39", "40-49", "50-59", "60-69", "70-79", "80+", "all_ages"]

vaccine_groups = ["full", "atleast1"]

# Get COVID-19 info and reformat data into DataFrame
data = requests.get('https://api.covid19tracker.ca/reports/province/on').json()['data']
details_df = pandas.DataFrame(data)
details_df.set_index('date', inplace=True)

# Get detailed vaccination data and reformat data
data = requests.get('https://api.covid19tracker.ca/vaccines/age-groups/province/ON').json()['data']
df = pandas.DataFrame()
df_list = []  # use a list to temporarily hold the values and improve efficiency over continuous df.appends
for e in data:
    x = pandas.Series(dtype=float)
    x.name = e['date']
    d = pandas.read_json(e['data'])
    for idx, group in enumerate(vaccine_groups):
        s = d.loc[group]
        x[group + '_adults'] = 100 * (s['all_ages'] - s['0-17']) / on_age_groups['adults']
        for k, v in s.items():
            x[group + '_' + k] = 100 * v / on_age_groups[k]
    df_list.append(x)
df = df.append(df_list)
del df_list

# Merge objects
df = df.join(details_df)

# PowerBI can't understand indices and needs it as an explicit column, also better for PowerBI to delete extra variables
df['Date'] = df.index.to_list()
del d
del details_df
