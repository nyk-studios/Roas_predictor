# models/base_model.py

class BaseModel:
    def train(self, X_train, X_val, y_train, y_val):
        raise NotImplementedError("Method train() not implemented.")

    def predict(self, X):
        raise NotImplementedError("Method predict() not implemented.")

    def evaluate(self, X_val, y_val):
        raise NotImplementedError("Method evaluate() not implemented.")

    def fit(self, X, treatment, y):
        raise NotImplementedError("Method evaluate() not implemented.")

    def get_params(self, deep=True):
        raise NotImplementedError("Method evaluate() not implemented.")

    def set_params(self, **parameters):
        raise NotImplementedError("Method evaluate() not implemented.")