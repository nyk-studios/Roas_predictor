import pandas as pd
import random
from datetime import datetime

def FakeDate(df):
    df_temp = df[df['date'] == df['date'].max()]
    zeros_count = int(len(df_temp) * 0.5) 
    ones_count = int(len(df_temp) - zeros_count)
    my_list = [0] * zeros_count + [1]*ones_count
    random.shuffle(my_list)
    df_temp['closeAd'] = my_list
    list_accum_roas = []
    for i in range(len(df_temp)):
        list_accum_roas.append(random.uniform(0,1))
    
    df_temp['accum_roas'] = list_accum_roas
    
    df_temp[['ad_id','ad_name','adcampaign_name','adset_name','date','accum_roas','closeAd']]
    
    today_date = datetime.today().strftime('%Y-%m-%d')
    meta_data = pd.DataFrame()

    meta_data = pd.DataFrame( {'date':today_date,
                               'model_hyper_params': [{ 'n_estimators': 300,'max_depth':10,'min_samples_leaf':20}],
                               'model_score_method': 'r2',
                               'model_score_train': 0.75,
                               'model_score_val': 0.71,
                               'model_score_test': 0.69,
                               'model_roas_params':[{'tot_budget': 2000000,'roas_before_algo':0.84,'roas_after_algo':0.91,'percnet_out_of_budget':0.7,
                                      'parmas_checked':{'y_predict_low': 0.7,'y_predict_high':1.1,'accum_cost':20,'accum_roas':0.9,'days_since_start':4}
                                          
                                      }],
                               'test_before_algo_roas': 0.84,
                               'test_after_algo_roas': 0.91,
                               'test_tot_budget': 800000,
                               'test_percent_of_budget_algo': 0.7


    },
    index = ['index']


    )

   
    return meta_data,df_temp