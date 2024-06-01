import pandas as pd
from models.base_model import BaseModel
from sklearn.ensemble import RandomForestRegressor
from models.model_utils import score_mapper

class RandomForestRegressor(BaseModel):
    def __init__(self, config):
        self.config = config
        self.treatment_col = self.config['treatment_col']
        self.metric = self.config['metric']
        self.n_estimators = 300
        self.max_depth = 5
        self.model = RandomForestRegressor(n_estimators=self.n_estimators,
                                                  max_depth=self.max_depth)

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

    def fit(self, X, treatment, y):
        self.model.fit(X=X, treatment=treatment, y=y)


    def get_params(self, deep=True):
        return {"control_name": self.control_name, "n_estimators": self.n_estimators, "max_depth": self.max_depth}

    def set_params(self, **parameters):
        for parameter, value in parameters.items():
            setattr(self, parameter, value)
        self.model = RandomForestRegressor(control_name=self.control_name,
                                                  n_estimators=self.n_estimators,
                                                  max_depth=self.max_depth)