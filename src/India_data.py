import pandas as pd
import requests

# Fetch the data.
df = pd.read_csv("https://ourworldindata.org/grapher/total-ghg-emissions.csv?v=1&csvType=full&useColumnShortNames=true", storage_options = {'User-Agent': 'Our World In Data data fetch/1.0'})

# Fetch the metadata
metadata = requests.get("https://ourworldindata.org/grapher/total-ghg-emissions.metadata.json?v=1&csvType=full&useColumnShortNames=true").json()
df = df.sort_values("Year")
country = "India"

df = df.sort_values("Year")

df = df.rename(columns={"annual_emissions_ghg_total_co2eq": "GHG Emissions (CO2e)",
    "Entity": "Country"})

df = df[df["Country"] == country]

df["GHG Change %"] = df["GHG Emissions (CO2e)"].pct_change() * 100
df["GHG Change %"] = df["GHG Change %"].round(2)

filtered_df = df[(df["Country"] == country) & (df["Year"] >= 2005)]

clean_df = filtered_df[['Country', 'Year', 'GHG Emissions (CO2e)', 'GHG Change %']]

print(clean_df)
