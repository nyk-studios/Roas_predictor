import pandas as pd
import sys




class preprocessing_funcs:
    @classmethod
    def sort_values(cls,config_info):
        """
        get the dataframe and params of each function and checks that
        the data is there and returns them
        :config_info: the data that comes in the kwarg in each function
        :returns: dataframe and params 
        """
        
        
        try: 
            df =config_info.get('data')
        except:
            print('Cannot find dataframe in data_n_params')
        try: 
            params = config_info.get('params')
        except:
            print('Cannot find columns in data_n_params')
    
        return df,params
    
    
    
    
    
    @classmethod
    def get_data_params(cls,config_info):
        """
        get the dataframe and params of each function and checks that
        the data is there and returns them
        :config_info: the data that comes in the kwarg in each function
        :returns: dataframe and params 
        """
        
        
        try: 
            df =config_info.get('data')
        except:
            print('Cannot find dataframe in data_n_params')
        try: 
            params = config_info.get('params')
        except:
            print('Cannot find columns in data_n_params')
    
        return df,params
    
    
    @classmethod
    def fillna(cls,**kwarg):
        """ 
        function takes dataframe and cols names and fill missing
        values with 0
        :df: dataframe
        :columns: cols list to fill missing values
        :output: df with imputation  
        """        
        # get data and params
        df, params = preprocessing_funcs.get_data_params(kwarg)

        try: 
            cols = params.get('cols')
        except:
            print('Cannot find cols in params')

        missing_cols = [i for i in cols if i not in df.columns] 


        if missing_cols:
            print(f"{missing_cols} are not in the Dataframe columns")
            sys.exit()

        for i in cols:
            
            df[i].fillna(0,inplace=True)
        # soem rows might be missing
        # ad id or name, remove all rows with null 
        df.dropna(inplace=True)
        
        return df
    
    @classmethod 
    def get_relative_date(cls,**kwarg):
        """
        get the relative day since ad start
        :df: dataframe to add relative time since ad start
        :ID_col: ad id 
        :date_col: date columns
        :output: dataframe with with the new days_since_start column ordered by ID_col and days_since_start 
        """
        # get data and params
        df, params = preprocessing_funcs.get_data_params(kwarg)
        
        # get the id and date cols 
        try: 
            ID_col = params.get('cols')['ID_col']
            date_col = params.get('cols')['Date_col']
        except:
            print('Cannot find cols in params')



        # find the start date of each ad
        df = df.merge(df[[ID_col,date_col]].groupby(ID_col).min()[date_col].reset_index().rename(columns={date_col:'min_date'})
                , on =ID_col,how='left')
        # subtract the date from the start date to get the relative date of the row 
        df['days_since_start'] =  (df[date_col] - df['min_date']).dt.days
        # merge back into the original dataframe
        df = df.merge(df.groupby(ID_col).max()['days_since_start'].reset_index(name='max_days'),
                on=ID_col,how='left')
        # sort values according to ad_id and days_since_start
        df.sort_values([ID_col,'days_since_start'],inplace=True)
        # drop the min_date   
        df.drop(['min_date','max_days'],inplace=True,axis=1)

        return df

    @classmethod 
    def get_dif_from_previous_days(df,**kwarg):
        """
      get list of features and create new features which 
      are the difference of the values of the features
      and previous days values for those features. if the value of 
      days back is 5. Than for each day up to 5 days the function will 
      return a new feature with the difference of that day and the current day
      :df: dataframe
      : in kwarg: 
      :cols: list of columns to act on 
      : days back: how many days to go back   

        """
      
      
        # get data and params
        df, params = preprocessing_funcs.get_data_params(kwarg)

        # get cols and days back 
        try: 
            cols = params.get('cols')
            days_back = params.get('days_back')
        except:
            print('Cannot find cols in params')

        # create new dif columns
        for i in cols:
            for j in range(days_back):
                # new name for temp column days back and column name
                new_name = i + '_' + str(j)
                 # new name for dif columns days back _dif_ and column name
                dif_name= i + '_dif_' + str(j +1)
                # first create a columns with the dif value
                df[new_name] = df[i].shift(j + 1)
                # when there is not enough days to go back fillin 0 
                df[new_name].fillna(0,inplace=True)
                # find the dif 
                df[dif_name]  = df[i] - df[new_name]
                # remove the temp column from dataframe
                df.drop(new_name,axis=1,inplace=True)

          
        return df
    
    @classmethod 
    def get_accum_cols(df,**kwarg):
        """
        function takes dataframe and col names to create 
        new columns which are accumulation values of those cols
        :df: dataframe
        :cols: columns list to create new accumulated columns from 
        :ID_cols: the key column to order the dataframe 
        :date_col: date column to order the dataframe
        :output: new dataframe with the new accumulated cols 
        """

        # get data and params
        df, params = preprocessing_funcs.get_data_params(kwarg)
        
        # get the id and date cols 
        try: 
            ID_col = params.get('cols')['ID_col']
            date_col = params.get('cols')['Date_col']
        except:
            print('Cannot find cols in params')

        # sort the dataframe according to id and date
        df = df.sort_values([ID_col,date_col],inplace=True)

        # for each col in the list create new accumulated col  
        for i in cols:
            # new col name 
            new_name = 'accum_' + i
            # create the accum col
            df[[new_name]] = df.groupby(ID_col).cumsum()[[i]]
            
        return df
    @classmethod 
    def roas(df,cost,revenue,output_col):
        """ 
        calculate the roas rev/cost
        :df: dataframe
        :cost: cost column
        :revenue: revenue columns 
        :output_col: name of output column
        """
        
        
        df[output_col] = df[revenue]/df[cost]

        return df[output_col]

        



