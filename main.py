from datahandle import DataHandle
from yaml import *
from Utilis.yaml_parser import read_and_create_objects_from_yaml 
from preprocessing_files.processor import DataProcessor
from preprocessing_files import create_fake_data 
from models.model_utils import model_mapper
from models.model_optimizer import ModelOptimizer, Roasptimizer




def run_roas_prediction():
    print('run start')
    # get components from config file 
    yaml_components = read_and_create_objects_from_yaml('config.yaml')
    # parse the start and end dates for the data fetching
    
    #get the Data 
    df = DataHandle.get_data_from_table(yaml_components['dates'])
    meta_data,df_fake = create_fake_data.FakeDate(df)

    DataHandle.write_meta_data(meta_data)
    DataHandle.write_algo_data(df_fake)


    # data_processor = DataProcessor(df)
    # df = data_processor.process(yaml_components['data_preprocessor'])
    # # if it works I nedd to make it part of the preprocessing
   
    # split_data = data_processor.split_train_val_test_by_col(yaml_components['data_split'])
    # print('spit data done')
    # model = model_mapper[yaml_components['model']['model_name']]()
    
    # optimizer = ModelOptimizer(yaml_components['model']['optimizer_hyperparmas'],model)
    
    # cols_to_drop = yaml_components['cols_to_drop']
    # model = optimizer.hyper_param_optimization(
    # split_data['X_train'].drop(cols_to_drop,axis=1),split_data['y_train'])
    
    # roas_םptimizer = Roasptimizer(yaml_components['model']['roas_optimizer'],model,cols_to_drop)
    # roas_םptimizer.optimize_roas(split_data['X_val'],split_data['y_val'],
    #               split_data['X_test'],split_data['y_test'] )

    
    
    a = 2
 
if __name__ == "__main__":
    run_roas_prediction()
