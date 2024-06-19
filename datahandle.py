import pandas as pd
from pymongo import MongoClient
from datetime import datetime,timedelta


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
        today = datetime.now()
        if 'start_date' in config:
            start = datetime.strptime(config['start_date'],'%Y-%m-%d')
            end = datetime.strptime(config['end_date'],'%Y-%m-%d')
        else:
            end = today
            start = end - timedelta(days= 30 * config['num_months'])

        client = MongoClient('mongodb+srv://eran:MzI4f8okS2763d8Q@tmscluster.jtyul.mongodb.net/test')
        mydatabase = client.calculations
        collection_name = mydatabase.fb_roas_prediction
        cursor = collection_name.find({'date': {'$lt': end, '$gte': start}})
        list_cur = list(cursor)
        df = pd.DataFrame(list_cur)
        yesterday = today - timedelta(days=1)
        yesterday = yesterday.strftime('%Y-%m-%d')


        if len(df[df['date'] >= yesterday ]) == 0:
           raise ValueError(f'There are no ads from yesterday to analyze')




        return df

    @classmethod 
    def write_meta_data(cls,df):
        """
          writes a dataframe of the meta data
          into the meta data table in the database
          :df: meta data dataframe 
           """
        client = MongoClient('mongodb+srv://eran:MzI4f8okS2763d8Q@tmscluster.jtyul.mongodb.net/test')
        mydatabase = client.calculations
        collection_name = mydatabase.road_pred_metadata
        collection_name.insert_many(df.to_dict('records'))



    @classmethod 
    def write_algo_data(cls,df):
        """
          writes a dataframe of the algo results
          into the algo results table in the database
          :df: algo dataframe 
           """
        client = MongoClient('mongodb+srv://eran:MzI4f8okS2763d8Q@tmscluster.jtyul.mongodb.net/test')
        mydatabase = client.calculations
        collection_name = mydatabase.roas_pred_results
        collection_name.insert_many(df.to_dict('records'))

    @classmethod
    def prepare_output(cls,data,ad_listּ,id_col,cost_col,rev_col,date_col):
            """ prepare the data to fit the 
                way Marketing requested it
                :data: dataframe with the ads to remove
                :ad_list:list of the ads to be removed
                :id_col: ad id column
                :cost_col: ad cost column
                :rev_col: ad revenue column
                :output: dataframe of the ads to remove as requested
               """
            today = datetime.now()
            # keep only ads which are still running
            data_new = data[data[id_col].isin(ad_listּ)]
            # create Lifetime Roas
            data_tot = data_new.groupby(id_col).sum()[[cost_col,rev_col]].reset_index(            
            ).rename(columns = {cost_col:'tot_cost',rev_col:'tot_rev'})
            data_7_days = data_new[data_new[date_col] >= today - timedelta(days= 7) ].groupby(id_col).sum()[[cost_col,rev_col]].reset_index(            
            ).rename(columns = {cost_col:'7_days_cost',rev_col:'7_days_rev'})
            data_4_days = data_new[data_new[date_col] >= today - timedelta(days= 4) ].groupby(id_col).sum()[[cost_col,rev_col]].reset_index(            
            ).rename(columns = {cost_col:'4_days_cost',rev_col:'4_days_rev'})
            data_1_days = data_new[data_new[date_col] >= today - timedelta(days= 1) ].groupby(id_col).sum()[[cost_col,rev_col]].reset_index(            
            ).rename(columns = {cost_col:'1_days_cost',rev_col:'1_days_rev'})
            
            # get Roas of each option 
            data_tot['Lifetime'] = data_tot['tot_rev']/data_tot['tot_cost']
            data_tot.rename(columns = {'tot_cost':'Spend - Lifetime'},inplace = True)
            data_7_days['Last 7 days'] = data_7_days['7_days_rev']/data_7_days['7_days_cost']
            data_4_days['Last 4 days'] = data_4_days['4_days_rev']/data_4_days['4_days_cost']
            data_1_days['Day before'] = data_1_days['1_days_rev']/data_1_days['1_days_cost']

            # merge all data together
            data_out = data_new[['ad_id','adcampaign_name']].drop_duplicates().merge(data_tot[['ad_id','Spend - Lifetime','Lifetime']],on='ad_id',how='left')
            data_out = data_out.merge(data_7_days[['ad_id','Last 7 days']],on='ad_id',how='left')
            data_out = data_out.merge(data_4_days[['ad_id','Last 4 days']],on='ad_id',how='left')
            data_out = data_out.merge(data_1_days[['ad_id','Day before']],on='ad_id',how='left')

            return data_out






