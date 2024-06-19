class RoasModel:

    @classmethod 
    def run_model(cls,data,params,Id_col,cost_col,rev_col):
        
        
        y_predict_low = params['y_predict_low']
        y_predict_high = params['y_predict_high']
        accum_cost = params['accum_cost']
        accum_roas = params['accum_roas']
        days_since_start = params['days_since_start']





        df_ads_to_stop = data[(data['y_predict'] > y_predict_low) &
                                  (data['y_predict'] < y_predict_high) &
                                  (data['accum_cost'] > accum_cost) &
                                  (data['accum_Roas'] < accum_roas) &
                                  (data['days_since_start'] > days_since_start) 
                                   ].drop_duplicates(Id_col,keep='first')
        
        
        
        
        return df_ads_to_stop

    @classmethod 
    def cal_results(cls,data,ads_stop,cost_col,rev_col):
        
        # find ads which did not meet the stop conditions                            
        df_rest_ads = data[~data['ad_id'].isin(ads_stop['ad_id'].unique().tolist())]
        cost_before_algo = data[cost_col].sum()
        rev_before_algo = data[rev_col].sum()
        tot_roas_before_algo = round(rev_before_algo/cost_before_algo,2)
        cost_after_algo = ads_stop[cost_col].sum() + df_rest_ads[cost_col].sum()
        rev_after_algo = ads_stop[rev_col].sum() + df_rest_ads[rev_col].sum()
        tot_roas_after_algo = round(rev_after_algo/cost_after_algo,2)
        percent_of_budget = round(cost_after_algo/cost_before_algo,2)

        return cost_before_algo,tot_roas_before_algo,tot_roas_after_algo,percent_of_budget

        