import pandas as pd
from pymongo import MongoClient
from datetime import datetime

def get_data_from_table(start_date,end_date):
 
    start = datetime.strptime(start_date,'%Y-%m-%d')
    end = datetime.strptime(end_date,'%Y-%m-%d')

    client = MongoClient('mongodb+srv://eran:MzI4f8okS2763d8Q@tmscluster.jtyul.mongodb.net/test')
    mydatabase = client.calculations
    collection_name = mydatabase.fb_roas_prediction
    cursor = collection_name.find({'date': {'$lt': end, '$gte': start}})
    list_cur = list(cursor)
    df = pd.DataFrame(list_cur)
    
    return df
