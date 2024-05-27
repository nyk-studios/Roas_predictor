from preprocessing_files.preprocessing_utils import preprocessing_funcs
import pandas as pd

mapper = {
        'fillna': preprocessing_funcs.fillna ,
        'get_relative_date': preprocessing_funcs.get_relative_date,
        'get_accum_cols': preprocessing_funcs.get_accum_cols,
        'get_dif_from_previous_days': preprocessing_funcs.get_dif_from_previous_days
    }
        

class PROC:
    @classmethod
    def process(cls,functions_params, df):
        for func in functions_params:
            mapper[list(func.keys())[0]](
                params=list(func.values())[0], data=df
            )

# if __name__ == "__main__":
#     a = pd.DataFrame()
#     PROC.process({'awsda':'asd'},a)

# def processing_run(dataframe,config_data):
#     for func in config_data:
#         params = list(func.values())[0]
#         params.append({'data':dataframe})
#         mapper[list(func.keys())[0]](params)
    
    
 #   print(config_data) 
    
    
