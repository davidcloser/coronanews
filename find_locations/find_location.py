import pandas as pd
import numpy as np
import re
from unidecode import unidecode

# Drop rows with na content
news_df = pd.read_csv("getcoronanews/news.csv")
news_df = news_df[~news_df["content"].isna()]

# List of districts
pt_df = pd.read_csv("getcoronanews/data/pt.csv")
madeira_df = pd.read_csv("getcoronanews/data/madeira.csv")
acores_df = pd.read_csv("getcoronanews/data/acores.csv")

concatenated_df = pd.concat((pt_df, madeira_df, acores_df))


# Convert the names of the council into lower case and ascii versions
def convert_names_url_format(row: str) -> str:
    """ Converts the names of locations and districts to lowercase and connected by -"""
    return unidecode(row.lower())


# Process the news df
processed_news = news_df.applymap(convert_names_url_format)
processed_news["total_content"] = processed_news["url"] + processed_news["title"] + processed_news["content"]

# Remove all non characters from the contents
processed_news["total_content"] = processed_news["total_content"].apply(lambda x: re.sub("[^a-zA-Z]", " ", x ))


# Find location from the URL
url_match_strings = concatenated_df.applymap(convert_names_url_format)
# Drop duplicated concelho names
url_match_strings = url_match_strings.loc[~url_match_strings["Concelhos"].duplicated()]

district_regex = r"\b" +"(" + "|".join(url_match_strings["Distrito"].unique().tolist()) + ")"
location_regex = r"\b" +"(" + "|".join(url_match_strings["Concelhos"].unique().tolist()) + ")"

# Try to match district and council from the URL
processed_news["district"] = processed_news["total_content"].apply(lambda x: re.findall(district_regex, x))
processed_news["location"] = processed_news["total_content"].apply(lambda x: re.findall(location_regex, x))

# # Get the names out of the list
processed_news["location"] = processed_news["location"].apply(lambda x: x[0] if x else np.nan)
processed_news["district_with_council"] = processed_news["location"].map(url_match_strings.set_index("Concelhos")["Distrito"])
processed_news.loc[processed_news["district_with_council"].isna(), "district"] = processed_news["district"]

# Append the processed df to the old news df
news_df["district"] = processed_news["district"]
news_df["location"] = processed_news["location"]
news_df["total_content"] = processed_news["total_content"]

# Only preserve news that have location (At least the district)
news_df = news_df[news_df["district"]]


