import pandas as pd
import re

filePath = 'movies.csv'
df = pd.read_csv(filePath)

def extractYear(title):
    match = re.search(r'\((\d{4})\)', title)
    return int(match.group(1)) if match else None

def cleanTitle(title):
    titleRemoveYear = re.sub(r'\(\d{4}\)', '', title).strip()
    cleanTitle = re.sub(r'[^\w\s]', '', titleRemoveYear)
    return cleanTitle.lower()

df['year'] = df['title'].apply(extractYear)
df['title'] = df['title'].apply(cleanTitle)

genreSplit = df['genres'].str.get_dummies(sep='|')

df_encoded = df.join(genreSplit)
df_encoded.drop('genres', axis=1, inplace=True)
outputFilePath = 'movies_encoded.csv'
df_encoded.to_csv(outputFilePath, index=False)
print("One-hot encoded genres added and saved to 'movies_encoded.csv'")
