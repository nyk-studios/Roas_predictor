from get_data import get_data_from_table
from yaml import *
from Utilis.yaml_parser import read_and_create_objects_from_yaml 

if __name__ == "__main__":
    # get components from config file 
    yaml_components = read_and_create_objects_from_yaml('config.yaml')
    # parse the start and end dates for the data fetching
    start_date = yaml_components['dates']['start_date']
    end_date = yaml_components['dates']['end_date']
    
    # get the Data 
    df = get_data_from_table(start_date,end_date)
    print(df)
    