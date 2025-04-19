import pandas as pd

# df = pd.read_csv('recipes_data.csv')

# df = df.drop_duplicates(subset='title')#remove duplicates based on title
# df = df[['title', 'ingredients', 'directions','NER']]#keep only relevant columns

# print(df.head())
# print(df.describe())
# print("Shape of the data: ", df.shape)
# df.to_csv('recipes_data_cleaned.csv', index=False)#save the cleaned data




df = pd.read_csv('recipes_data_cleaned.csv')

df = df.head(100000)#dataset was too large

df.to_csv('recipes_data_cleaned.csv', index=False)