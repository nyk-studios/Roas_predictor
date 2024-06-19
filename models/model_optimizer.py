from models.randomforest_regressor import score_mapper
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import  r2_score
import pandas as pd
from models.Roas_model import RoasModel
import itertools 

class ModelOptimizer:
    
    def __init__(self, config, model):
        self.config = config
        self.model = model
        self.metric =  self.config['model_metric']

    def hyper_param_optimization(self, X_train, y_train):
        params = self.config['model_parmas']
        metric = self.config['model_metric']
        # Generate the parameter grid dictionary dynamically
        param_grid = {key: [value] if not isinstance(value, list) else value for key, value in params.items()}
        print(f"Running Hyper Parameter Optimization on these parameters {param_grid}")

     #  scorer = make_scorer(score_mapper[self.metric])
        scorer = self.metric
        grid_search = GridSearchCV(self.model, param_grid, scoring=scorer, cv=5)
        # run the gridsearch 
        grid_search.fit(X=X_train, y=y_train)
        # set the best params in the model 
        self.model.set_params(**grid_search.best_params_)
        # run model on best params
        self.model.fit(X=X_train, y=y_train)
        #return model
        return self.model
        
class RoasOptimizer:
    
    def __init__(self, config, model,cols_to_drop): 
        self.config = config
        self.model = model
        self.cols_drop = cols_to_drop
        


    def optimize_roas(self, X_val, y_val,X_test,y_test):
        
        cols = self.config['cols']
        cost_col = self.config['cost']
        id_col = self.config['Id_col']
        rev_col = self.config['rev']

        X_val['y_predict'] = self.model.predict(X_val.drop(self.cols_drop,axis=1))
        X_test['y_predict'] = self.model.predict(X_test.drop(self.cols_drop,axis=1))

        tot_budget = [] 
        roas_before_algo = [] 
        roas_after_algo = [] 
        percent_out_of_budget = [] 
        parmas_checked = [] 
        
        list_of_items = [cols['y_predict_low'],cols['y_predict_high'],cols['accum_cost'],cols['accum_roas'],cols['days_since_start']]
        t = 0
        for l in itertools.product(*list_of_items):
            data = X_val.copy()

            df_ads_to_stop =  RoasModel.run_model(data,
                {'y_predict_low':l[0],
                    'y_predict_high':l[1],
                    'accum_cost':l[2],
                    'accum_roas':l[3],
                    'days_since_start':l[4]},
                id_col,cost_col, rev_col) 
                            
                            
            cost_before_algo,tot_roas_before_algo,tot_roas_after_algo,percent_of_budget = RoasModel.cal_results(data,df_ads_to_stop,cost_col, rev_col)
            
            tot_budget.append(cost_before_algo)
            roas_before_algo.append(tot_roas_before_algo)
            roas_after_algo.append(tot_roas_after_algo)
            percent_out_of_budget.append(percent_of_budget)
            parmas_checked.append({'y_predict_low':l[0],'y_predict_high':l[1],'accum_cost':l[2],'accum_roas':l[3],'days_since_start':l[4] })

       
       
        optim_df = pd.DataFrame()
        optim_df['params_checked'] = parmas_checked
        optim_df['tot_budget'] = tot_budget
        optim_df['roas_before_algo'] = roas_before_algo
        optim_df['roas_after_algo'] = roas_after_algo
        optim_df['percent_out_of_budget'] = percent_out_of_budget
        optim_df_thresh =  optim_df[optim_df['percent_out_of_budget'] > self.config['budgte_threshold']]
        params_out = optim_df_thresh[optim_df_thresh['roas_after_algo'] == optim_df_thresh['roas_after_algo'].max()]
        params_out = params_out[params_out['percent_out_of_budget'] == params_out['percent_out_of_budget'].max() ].drop_duplicates('percent_out_of_budget',keep='first')
        params_out['data_type'] = 'val'
        params_out['regression_score'] = r2_score(X_val['y_predict'].tolist(),y_val)


        test_ads_stop = RoasModel.run_model(X_test,params_out['params_checked'].iloc[0],id_col,cost_col, rev_col) 
        test_cost_before_algo,test_tot_roas_before_algo,test_tot_roas_after_algo,test_percent_of_budget = RoasModel.cal_results(X_test,test_ads_stop,cost_col, rev_col)
        params_out = params_out.append({
               'params_checked': params_out['params_checked'].iloc[0],
               'tot_budget':test_cost_before_algo,
               'roas_before_algo':test_tot_roas_before_algo,
               'roas_after_algo':test_tot_roas_after_algo,
               'percent_out_of_budget':test_percent_of_budget,
               'data_type':'test',
               'regression_score':r2_score(X_test['y_predict'].tolist(),y_test)
                     },ignore_index=True)
        return params_out
        

       