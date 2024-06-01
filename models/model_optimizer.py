from models.model_utils import RandomForestRegressormodel
from models.randomforest_regressor import score_mapper
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import make_scorer
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import mean_squared_error, r2_score
import pandas as pd

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
        
class Roasptimizer:
    
    def __init__(self, config, model,cols_to_drop): 
        self.config = config
        self.model = model
        self.cols_drop = cols_to_drop
    
    def optimize_roas(self, X_val, y_val,X_test,y_test):
        
        cols = self.config['cols']
        X_val['y_predict'] = self.model.predict(X_val.drop(self.cols_drop,axis=1))
        X_test['y_predict'] = self.model.predict(X_test.drop(self.cols_drop,axis=1))
        val_score = r2_score(X_val['y_predict'].tolist(),y_val)
        test_score = r2_score(X_test['y_predict'].tolist(),y_test)
        tot_budget = [] 
        roas_before_algo = [] 
        roas_after_algo = [] 
        percnet_out_of_budget = [] 
        parmas_checked = [] 
        for v1 in cols['y_predict_low']:
            for v2 in cols['y_predict_high']:
                for v3 in cols['accum_cost']:
                    for v4 in cols['accum_roas']:
                        for v5 in cols['days_since_start']:
                            df_ads_to_stop = X_val[(X_val['y_predict'] > v1) &
                                  (X_val['y_predict'] < v2) &
                                  (X_val['accum_cost'] > v3) &
                                  (X_val['accum_Roas'] > v4) &
                                  (X_val['days_since_start'] > v5) 
                                   ].drop_duplicates(self.config['Id_col'],keep='first')
                            df_rest_ads = X_val[~X_val[self.config['Id_col']].isin(df_ads_to_stop[self.config['Id_col']])]
                            cost_before_algo = X_val[self.config['cost']].sum()
                            rev_before_algo = X_val[self.config['rev']].sum()
                            tot_roas_before_algo = round(rev_before_algo/cost_before_algo,2)
                            cost_after_algo = df_ads_to_stop[self.config['cost']].sum() + df_rest_ads[self.config['cost']].sum()
                            rev_after_algo = df_ads_to_stop[self.config['rev']].sum() + df_rest_ads[self.config['rev']].sum()
                            tot_roas_after_algo = round(rev_after_algo/cost_after_algo,2)
                            percent_of_budget = round(cost_after_algo/cost_before_algo,2)
                            tot_budget.append(cost_before_algo)
                            roas_before_algo.append(tot_roas_before_algo)
                            roas_after_algo.append(tot_roas_after_algo)
                            percnet_out_of_budget.append(percent_of_budget)
                            parmas_checked.append({'y_predict_low':v1,'y_predict_high':v2,'accum_cost':v3,'accum_roas':v4,'days_since_start':v5 })
        optim_df = pd.DataFrame()
        optim_df['params_checked'] = parmas_checked
        optim_df['tot_budget'] = tot_budget
        optim_df['roas_before_algo'] = roas_before_algo
        optim_df['roas_after_algo'] = roas_after_algo
        optim_df['percnet_out_of_budget'] = percnet_out_of_budget
        optim_df_thresh =  optim_df[optim_df['percnet_out_of_budget'] > self.config['budgte_threshold']]
        params_out = optim_df_thresh[optim_df_thresh['roas_after_algo'] == optim_df_thresh['roas_after_algo'].max()]['params_checked']

        return params_out
        

       