import pandas as pd
import numpy as np

districts_df = pd.read_csv("getcoronanews/districts.csv", index_col=0)

# Drop rows with na content
news_df = pd.read_csv("getcoronanews/news.csv")
news_df = news_df[~news_df["content"].isna()]


def find_districts(row: str) -> list:
    """ Checks if any of the districts is in the corpus of text """
    districts = [district for district in districts_df["District"].values if district in row]
    if not districts:
        return np.nan

    return districts

news_df["district"] = news_df["content"].apply(find_districts)
