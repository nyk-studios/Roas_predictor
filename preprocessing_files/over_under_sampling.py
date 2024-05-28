from imblearn.over_sampling import SMOTE

def smote(X_train_temp,y_train_temp):
    """
    takes train data and return oversmaple smote data
    :X_train_temp: train data
    :X_train_temp: target data
    :output:  X_train, y_train  which are oversmapled smote data
    """

    X_train, y_train = SMOTE().fit_resample(X_train_temp, y_train_temp)


    return  X_train, y_train