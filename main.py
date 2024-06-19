from datahandle import DataHandle
from yaml import *
from Utilis.yaml_parser import read_and_create_objects_from_yaml 
from preprocessing_files.processor import DataProcessor
import models.model_utils 
from models.model_optimizer import ModelOptimizer, RoasOptimizer
import pandas as pd
from models.Roas_model import RoasModel



def run_roas_prediction():
    print('run start')
    # get components from config file 
    yaml_components = read_and_create_objects_from_yaml('config.yaml')
    # parse the start and end dates for the data fetching
    
    #get the Data 
    df = DataHandle.get_data_from_table(yaml_components['dates'])
    


    data_processor = DataProcessor(df)
    # get the historical adds data into dataframe 
    # keeps adds which are still running (have record in last 7 days)
    # in separated dataframe
    df = data_processor.process(yaml_components['data_preprocessor'])

    # split ads which are still running to check if need to be closed    
    split_data = data_processor.split_train_val_test_by_col(yaml_components['data_split'])
    print('spit data done')
    # initialze to model according to the yaml 
    model = models.model_utils.model_mapper[yaml_components['model']['model_name']]()
    # optimize the model hyperparams
    optimizer = ModelOptimizer(yaml_components['model']['optimizer_hyperparmas'],model)
    # drop columns we dont need for the model 
    cols_to_drop = yaml_components['cols_to_drop']
    # run the cross validation for the model hyperparams
    model = optimizer.hyper_param_optimization(
    split_data['X_train'].drop(cols_to_drop,axis=1),split_data['y_train'])
    # after the model try to find the best threshold for the model,budget spent,
    # num days the ad is running, and the current roas the maximize the overall roas

    #initialize and run the optimization 
    roas_optimizer = RoasOptimizer(yaml_components['model']['roas_optimizer'],model,cols_to_drop)
    results = roas_optimizer.optimize_roas(split_data['X_val'],split_data['y_val'],
                  split_data['X_test'],split_data['y_test'] )
    # drop traget column from data
    report_data = split_data['df_run'].drop('target',axis=1)
    # find the predicted y
    report_data['y_predict']  = model.predict(report_data.drop(cols_to_drop,axis=1))
    # find the ads to drop according to the model 
    report_ad_stop =  RoasModel.run_model(report_data,results['params_checked'].iloc[0],
                yaml_components['model']['roas_optimizer']['Id_col'],yaml_components['model']['roas_optimizer']['cost'],
                  yaml_components['model']['roas_optimizer']['rev']) 
    list_ads_to_remove = report_ad_stop[ yaml_components['model']['roas_optimizer']['Id_col']].unique().tolist()
    
    out_data = DataHandle.prepare_output(report_data,list_ads_to_remove,
                              yaml_components['model']['roas_optimizer']['Id_col'],
                              yaml_components['model']['roas_optimizer']['cost'],
                              yaml_components['model']['roas_optimizer']['rev'],
                              yaml_components['model']['roas_optimizer']['date'])
    
    a = 2
if __name__ == "__main__":
    run_roas_prediction()
