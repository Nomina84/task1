import yfinance as yf
from datetime import datetime
from GoogleNews import GoogleNews
import pandas as pd
from newsapi import NewsApiClient



end_date = datetime.now().strftime('%Y-%m-%d')
api_key=input("please enter your API key: ")

#Get information about gold, oil and dollar

gold_data = yf.download("GC=F", period='max' , start="2021-01-01" , end=end_date )
gold_dataset = pd.DataFrame(gold_data)
gold_dataset.drop('Adj Close' , axis=1 , inplace=True)
gold_dataset.columns = ["Open_gold", "High_gold", "Low_gold" , "Close_gold" ,"Volume_gold"]
print (gold_dataset)
gold_dataset.to_excel("gold_data.xlsx")

oil_data = yf.download("CL=F", period='max' , start="2021-01-01" , end=end_date )
oil_dataset = pd.DataFrame(oil_data)
oil_dataset.drop('Adj Close', axis=1 , inplace=True)
oil_dataset.columns = ["Open_oil", "High_oil", "Low_oil" , "Close_oil" ,"Volume_oil"]
print (oil_dataset)
oil_dataset.to_excel("oil_dataset.xlsx")


USD_data = yf.download("USD=X", period='max' , start="2021-01-01" , end=end_date )
USD_dataset = pd.DataFrame(USD_data)
USD_data.drop('Adj Close' , axis=1 , inplace=True)
USD_dataset.columns = ["date","Open_usd", "High_usd", "Low_usd" , "Close_usd" ,"Volume_usd"]
print (USD_dataset)
USD_dataset.to_excel('USD_dataset.xlsx')

final_dataset=gold_dataset

columns_name1={"Open_oil", "High_oil", "Low_oil" , "Close_oil" ,"Volume_oil"}
for i in columns_name1 :
    adding_column=oil_dataset[i]
    final_dataset=pd.concat([final_dataset ,adding_column.rename(i) ] , axis=1)

columns_name2={"Open_usd", "High_usd", "Low_usd" , "Close_usd" ,"Volume_usd"}
for i in columns_name2 :
    adding_column=USD_dataset[i]
    final_dataset=pd.concat([final_dataset ,adding_column.rename(i) ] , axis=1)

#Get news about gold , oil and dollar
topics = {'gold', 'OIL' , 'USD'}
from_date = "2021-01-01"
to_date = end_date

for i in topics :
    newsapi = NewsApiClient(api_key=api_key)
    news = newsapi.get_everything(q=i, from_param=from_date, to=to_date)
    news_data = {'Title': [], 'Description': [], 'URL': []}
    
    for article in news['articles']:
        title = article['title']
        description = article['description']
        url = article['url']
        
        news_data['Title'].append(title)
        news_data['Description'].append(description)
        news_data['URL'].append(url)
    news_df = pd.DataFrame(news_data)
    adding_column=news_df["title"]
    final_dataset=pd.concat([final_dataset ,adding_column.rename(f"{i} news") ] , axis=1)

#The final dataset
print (final_dataset)
final_dataset.to_excel("final_dataset.xlsx")
