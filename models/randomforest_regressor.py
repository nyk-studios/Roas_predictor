import pandas as pd
from models.base_model import BaseModel
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score


score_mapper = {
        'mean_squared_error': mean_squared_error ,
        'r2_score':r2_score,
       
    }



class RandomForestRegressormodel(BaseModel):
    def __init__(self, config):
        self.config = config
        self.metric = self.config['model_metric']
        self.n_estimators = self.config['model_params']['n_estimators']
        self.max_depth = self.config['model_params']['max_depth']
        self.min_samples_leaf = self.config['model_params']['min_samples_leaf']
        self.model = RandomForestRegressor(n_estimators=self.n_estimators,
                                                  max_depth=self.max_depth,
                                                  min_samples_leaf=self.min_samples_leaf,
                                                  )

    def train(self, X_train, X_val, y_train, y_val):
        

        self.model.fit(X_train.values,
                       y=y_train.values)

    def predict(self, X_test: pd.DataFrame):
        if not self.model:
            raise RuntimeError("Model has not been trained.")
       
        return self.model.predict(X_test.values)

    def evaluate(self, X_test, y_test):
        if self.model is None:
            raise RuntimeError("Model has not been trained.")
       
       
        predictions = self.predict(X_test)
        score = score_mapper[self.metric](y_test, predictions)

        return score

    def fit(self, X, y):
        self.model.fit(X=X, y=y)


    def get_params(self, deep=True):
        return { "n_estimators": self.n_estimators, "max_depth": self.max_depth, "min_samples_leaf": self.min_samples_leaf,}

    def set_params(self, **parameters):
       self.model.set_params(**parameters)
       
        # for parameter, value in parameters.items():
        #     setattr(self, parameter, value)
        # self.model =  RandomForestRegressor(n_estimators=self.n_estimators,
        #                                           max_depth=self.max_depth,
        #                                           min_samples_leaf=self.min_samples_leaf,
        #                                           )
        



   