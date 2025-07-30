import kagglehub

path = kagglehub.dataset_download("shivamb/netflix-shows")

print("Path to dataset files:", path)


import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv("netflix_titles.csv")


df = df.dropna(subset=["type"])
df = df[df["type"].isin(["Movie", "TV Show"])]


df["release_year"] = pd.to_numeric(df["release_year"], errors="coerce")
df = df.dropna(subset=["release_year"])
df["release_year"] = df["release_year"].astype(int)


df["listed_in"] = df["listed_in"].fillna("Unknown")
df["country"] = df["country"].fillna("Unknown")
df["genres"] = df["listed_in"].str.split(", ")
df["countries"] = df["country"].str.split(", ")


movies = df[df["type"] == "Movie"]
tv_shows = df[df["type"] == "TV Show"]


comedies = df[df["genres"].apply(lambda x: "Comedies" in x)]


us_content = df[df["countries"].apply(lambda x: "United States" in x)]


trends = df.groupby(["release_year", "type"]).size().unstack(fill_value=0)


df_genres = df.explode("genres")
genre_popularity = df_genres["genres"].value_counts().sort_values(ascending=False)


df_countries = df.explode("countries")
country_distribution = (
    df_countries["countries"].value_counts().sort_values(ascending=False)
)


plt.figure(figsize=(12, 6))
trends.plot(kind="line")
plt.title("Content Release Trends by Type")
plt.xlabel("Release Year")
plt.ylabel("Number of Titles")
plt.grid(True)
plt.show()


plt.figure(figsize=(12, 6))
top_genres = genre_popularity.head(10)
top_genres.plot(kind="bar")
plt.title("Top 10 Genres")
plt.xlabel("Genre")
plt.ylabel("Number of Titles")
plt.xticks(rotation=45)
plt.show()


plt.figure(figsize=(12, 6))
top_countries = country_distribution.head(10)
top_countries.plot(kind="bar")
plt.title("Top 10 Countries")
plt.xlabel("Country")
plt.ylabel("Number of Titles")
plt.xticks(rotation=45)
plt.show()


df.to_csv("netflix_cleaned.csv", index=False)
print("Cleaned dataset exported as 'netflix_cleaned.csv' for Power BI.")
