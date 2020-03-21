from gensim.utils import simple_preprocess
from unidecode import unidecode
import pandas as pd

# Drop rows with na content
news_df = pd.read_csv("getcoronanews/news.csv")
news_df = news_df[~news_df["content"].isna()]

# Get the content
news = news_df["content"].apply(unidecode).apply(simple_preprocess)



