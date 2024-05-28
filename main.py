from get_data import get_data_from_table
from yaml import *
from Utilis.yaml_parser import read_and_create_objects_from_yaml 
from preprocessing_files.processor import DataProcessor
from preprocessing_files.split_data import split_train_val_test_by_col

def run_roas_prediction():
    # get components from config file 
    yaml_components = read_and_create_objects_from_yaml('config.yaml')
    # parse the start and end dates for the data fetching
    start_date = yaml_components['dates']['start_date']
    end_date = yaml_components['dates']['end_date']
    #get the Data 
    df = get_data_from_table(start_date,end_date)
    data_processor = DataProcessor(df)
    df = data_processor.process(yaml_components['data_preprocessor'],df)
    
    # need to remove this once target function works
    
    split_data = data_processor.split_train_val_test_by_col(yaml_components['data_split'])

    model = model_run(yaml_components['model_type']) 
    
    a = 2
 
if __name__ == "__main__":
    run_roas_prediction()
