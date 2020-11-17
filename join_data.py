#!/usr/bin/env python3

import json
import pandas as pd
from tqdm import tqdm

with open("misc/SA2_with_IMD.topojson") as f:
    sa2 = json.load(f)

df = pd.read_csv("misc/New dwellings consented by 2018 statistical area 2 (Monthly).csv")
df = df[df.month >= "2020-01-01"]
eth_df = pd.read_csv("misc/2018-census-place-summaries-ethnicity-table2-2018-csv.csv")
eth_df = eth_df[eth_df.Census_usually_resident_population_count != "C"]
eth_df.Census_usually_resident_population_count = eth_df.Census_usually_resident_population_count.astype(int)

print(sa2["objects"].keys())
for geo in tqdm(sa2["objects"]["SA2_with_IMD"]["geometries"]):
    code = int(geo["properties"]["SA22018_V1_00"])
    consents = df[df.SA2_code == code]
    consents = dict(zip(consents.month, consents.total_dwelling_units))
    eth = eth_df[eth_df.Area_code == str(code)]
    eth = dict(zip(eth.Ethnic_group_total_responses_description, eth.Census_usually_resident_population_count))
    geo["properties"]["building_consents"] = consents
    geo["properties"]["ethnicity"] = eth

with open("SA2+IMD+consents+ethnicity.topojson", "w") as f:
    json.dump(sa2, f)