import pandas as pd
from pymongo import MongoClient
from datetime import datetime


class DataHandle:
    @classmethod
    def get_data_from_table(cls,config):
        ''' 
        A function that receive the start and end dates for the data fetching
        of facebook ad campaigns table,
        and returns a data frame of the data 
        :start_date: the date the data will start 
        :end_date: the data will end
        :return: df which is a dataframe of the data 

        '''
        

        start = datetime.strptime(config['start_date'],'%Y-%m-%d')
        end = datetime.strptime(config['end_date'],'%Y-%m-%d')

        client = MongoClient('mongodb+srv://eran:MzI4f8okS2763d8Q@tmscluster.jtyul.mongodb.net/test')
        mydatabase = client.calculations
        collection_name = mydatabase.fb_roas_prediction
        cursor = collection_name.find({'date': {'$lt': end, '$gte': start}})
        list_cur = list(cursor)
        df = pd.DataFrame(list_cur)
        
        return df

    @classmethod 
    def write_meta_data(cls,df):
        
        client = MongoClient('mongodb+srv://eran:MzI4f8okS2763d8Q@tmscluster.jtyul.mongodb.net/test')
        mydatabase = client.calculations
        collection_name = mydatabase.fb_roas_prediction
        collection_name.insert_many(df.to_dict('records'))

    @classmethod 
    def write_algo_data(cls,df):
        
        client = MongoClient('mongodb+srv://eran:MzI4f8okS2763d8Q@tmscluster.jtyul.mongodb.net/test')
        mydatabase = client.calculations
        collection_name = mydatabase.fb_roas_prediction
        collection_name.insert_many(df.to_dict('records'))