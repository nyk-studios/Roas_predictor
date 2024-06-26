from preprocessing_files.preprocessing_utils import preprocessing_funcs
import pandas as pd
import random  
from datetime import datetime,timedelta


mapper = {
        'fillna': preprocessing_funcs.fillna ,
        'get_relative_date': preprocessing_funcs.get_relative_date,
        'get_accum_cols': preprocessing_funcs.get_accum_cols,
        'get_dif_from_previous_days': preprocessing_funcs.get_dif_from_previous_days,
        'sort_values': preprocessing_funcs.sort_values,
        'roas': preprocessing_funcs.roas,
        'create_target_max_ratio_roas': preprocessing_funcs.create_target_max_ratio_roas,
        'remove_outliers':  preprocessing_funcs.remove_outliers
    }
        

class DataProcessor:
    
    def __init__(self, df):
        self._df = df

    def process(self,functions_params):
        for func in functions_params:
            self._df = mapper[list(func.keys())[0]](
                params=list(func.values())[0], data=self._df
            )
        return self._df
    
    def get_data(self):
        return self._df
    
   
    def split_train_val_test_by_col(self,config_data):
        """
        splits the data to train,val,test according to a 
        specific column (e.g 'ad_id'). 
        :split_col: the col 
        """
       
        try: 
            split_col = config_data.get('split_col')
            target_col = config_data.get('target_col')
            train_ratio = config_data.get('train_ratio')
            val_ratio = config_data.get('val_ratio')
            test_ratio = config_data.get('test_ratio')
            num_dyas_run_data = config_data.get('num_dyas_run_data')
        except:
            print('Cannot find cols in params')

        df_new = self._df

        # split ads which are still active to give suggestions for them later on
        temp = df_new[df_new['date'] > df_new['date'].max() - timedelta(days= num_dyas_run_data)][['ad_id', 'ad_name', 'adcampaign_name', 'adset_name']].drop_duplicates()        
        temp['still_run'] = 1
        df_new = df_new.merge(temp,on=['ad_id', 'ad_name', 'adcampaign_name', 'adset_name'],how='left' )
        df_run = df_new[df_new['still_run'] == 1].drop('still_run',axis=1)
        df_hist = df_new[df_new['still_run'].isnull()].drop('still_run',axis=1)        
    
        
        # split to train,val,test by ads to prevent data leakage
        num_ads = df_hist [split_col].nunique()
        num_train_ads = int(num_ads * train_ratio)
        num_val_ads = int(num_ads * val_ratio)
        num_test_ads = int(num_ads * test_ratio)
        all_ads = df_hist[split_col].unique().tolist()
        actuall_test_ratio =  num_test_ads/num_ads

        if  (actuall_test_ratio - 2) > test_ratio or (actuall_test_ratio + 2) < test_ratio:
            print(f'actuall_test_ratio: {actuall_test_ratio} \n Required test ratio: {test_ratio}')

        train_list = random.sample(all_ads, num_train_ads)
        list_not_in_train = [i for i in all_ads if i not in train_list]
        val_list = random.sample(list_not_in_train, num_val_ads)
        test_list = [i for i in list_not_in_train if i not in val_list]

        X_train = df_hist [df_hist [split_col].isin(train_list)].drop(target_col,axis=1)
        y_train = df_hist [df_hist [split_col].isin(train_list)][target_col].tolist()

        X_val = df_hist [df_hist [split_col].isin(val_list)].drop(target_col,axis=1)
        y_val = df_hist [df_hist [split_col].isin(val_list)][target_col].tolist()

        X_test = df_hist [df_hist [split_col].isin(test_list)].drop(target_col,axis=1)
        y_test = df_hist [df_hist [split_col].isin(test_list)][target_col].tolist()


        

        return {'X_train': X_train,
                'y_train':y_train,
                'X_val':X_val,
                'y_val':y_val,
                'X_test':X_test,
                'y_test':y_test,
                'df_run':df_run}
    
