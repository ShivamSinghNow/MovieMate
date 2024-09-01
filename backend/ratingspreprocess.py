import pandas as pd

df = pd.read_csv('ratings.csv')
df.drop('timestamp', axis=1, inplace=True)

UserItemMatrix = df.pivot_table(index='userId', columns='movieId', values='rating')
UserMeanRatings = UserItemMatrix.mean(axis = 1)
CenteredUserItemMatrix = UserItemMatrix.sub(UserMeanRatings, axis=0)

outputFilePath = "centereduseritem_matrix.csv"
CenteredUserItemMatrix.to_csv(outputFilePath)

print("file exported")