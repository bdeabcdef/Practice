# -*- coding: utf-8 -*-
"""
Created on Thu Feb  8 11:53:26 2018
class SuperHack(object):
    def __init__(self,uid):
        self.xcoord = None
        self.ycoord = None
        self.uid = uid
        self.inputList = []
        self.dfs = dict()
        self.df=None
        self.unique_column_id=None
        self.target = None
        self.image = 'Super Hack'
        
    def get_dataframe(self):
        input_df = self.dfs[self.inputList[0]]
        yt.YottaX(input_df,self.unique_column_id,self.target) 
        sd = yt.SplitDtypes()
        self.df = sd.split_merge()
        
        fv = yt.FeatureValidation()
        fv.fit_model(self.df)
        
        ac = yt.Accuracy()
        accuracy = ac.model_accuracy()
        print('accuracy=',accuracy)        
        return self.df

    def is_list_empty(self):
        return False

@author: Suresh
"""

#==============================================================================
# Wrapper code for "SuperHack" class
#==============================================================================
import warnings
warnings.filterwarnings("ignore")


from abc import ABC, abstractmethod
import pandas as pd
import numpy as np
from scipy.stats import boxcox

#==============================================================================
# author: suresh
#==============================================================================

class YottaX(object):
    def __init__(self,data,uid,target):
#        self.df= pd.read_csv(r'E:/fraud.csv')
        self.df= data
        self.uid = uid
        self.target = target
        self.model_type = None
        self.uid_target()
        self.identify_model()
        self.get_dtypes()        
        
    def uid_target(self):
        self.df_uid_target = self.df[[self.uid,self.target]]
        self.df.drop([self.uid,self.target],axis=1,inplace=True)
        
    def identify_model(self):
        target_type = self.df_uid_target[self.target].dtype
        if ((target_type == 'float64') or (target_type == 'int64')) and \
            (self.df_uid_target[self.target].nunique() > 10):
                self.model_type = 'regression'
        else:
            self.df_uid_target[self.target] = pd.factorize(self.df_uid_target[self.target])[0]
            self.model_type = 'classification'
            
        
    def filter_dtype(self,dtype):
        return self.df.select_dtypes(include=dtype)        
        
    def identify_datetype(self):
            for col in self.df_object.columns:
                try:
                    self.df.loc[:,col] = pd.to_datetime(self.df[col])
                    self.df_object.drop(col, axis=1, inplace=True)
                except:
                    pass
                finally:
                    df = self.filter_dtype(['datetime64'])
            return df
            
    def get_dtypes(self):
        self.df_object = self.filter_dtype(['object'])
        self.df_date = self.identify_datetype()
        self.df_float = self.filter_dtype(['float'])
        self.df_int = self.filter_dtype(['integer'])
    
        
class SplitDtypes(YottaX):
    def __init__(self,p_obj):
        self.df_date = p_obj.df_date
        
    def delete_column_with_same_value(self,df):
        for col in df.columns:
            if df[col].nunique() == 1:
                df.drop(col,axis=1,inplace=True)
            elif df[col].count() == df[col].nunique():
                df.drop(col,axis=1,inplace=True)
        return df
        

#==============================================================================
# Datetime
#==============================================================================

    def date_features(self,col,name):
        self.delete_column_with_same_value(self.df_date)
        dates = pd.DataFrame({"{}_year".format(name): col.dt.year,
                              "{}_month".format(name): col.dt.month,
                              "{}_day".format(name): col.dt.day,
                              "{}_hour".format(name): col.dt.hour,
                              "{}_dayofyear".format(name): col.dt.dayofyear,
                              "{}_week".format(name): col.dt.week,
                              "{}_weekofyear".format(name): col.dt.weekofyear,
                              "{}_dayofweek".format(name): col.dt.dayofweek,
                              "{}_weekday".format(name): col.dt.weekday,
                              "{}_quarter".format(name): col.dt.quarter,
                              "{}_minutes".format(name): col.dt.minute,
                              "{}_seconds".format(name): col.dt.second,
                             })
        return dates

    def split_datetypes(self):
        for col in self.df_date.columns:
            self.df_date = pd.concat([self.df_date,
                                      self.date_features(self.df_date[col],col)],
                                    axis=1)
            try:            
                self.df_date.drop(col,axis=1,inplace=True)
            except:
                pass
            
            
#==============================================================================
#  Numeric                  
#==============================================================================
                
    def split_numerictypes(self):
        self.delete_column_with_same_value(self.df_int)
        for col in self.df_int.columns:
    # if less than 10 unique elements we put the column as object(category),
            if self.df_int[col].nunique()<10:
                self.df_object = pd.concat([self.df_object,self.df_int[col]],axis=1)
                self.df_int.drop(col,axis=1,inplace=True)
            else:
    # else in float dataframe 
                self.df_float = pd.concat([self.df_float,self.df_int[col]],axis=1)

#==============================================================================
# Float
#==============================================================================
    def handle_skewness(self):
        for col in self.df_float.columns:
            if (self.df_float[col].skew()>1.5 or self.df_float[col].skew()<-1.5):
                self.df_float[col] = boxcox(self.df[col])[0]

    def split_floattypes(self):
        for col in self.df_float.columns:
            if (self.df_float[col]==0).any():
                self.df_float[col] = self.df_float.col + 1
            if (self.df_float[col]<0).any():
                self.df_float[col] = self.df_float[col] - self.df_float[col].min()
        self.handle_skewness()
        
#==============================================================================
# Categorical     
#==============================================================================
    def split_categorytypes(self):
        for col in self.df_object.columns:
            if self.df_object[col].nunique()<10:
                self.df_object = pd.concat([self.df_object,pd.get_dummies(self.df_object[col],prefix=col)],axis=1)
                self.df_object.drop(col,axis=1,inplace=True)
            else:
                self.df_object[col] = pd.factorize(self.df_object[col])[0]

            
#==============================================================================
# Split and merge    
#==============================================================================

    def split_merge(self):
        self.split_datetypes()
        self.split_numerictypes()
        self.split_floattypes()
        self.split_categorytypes()
        pre_list = [self.df_uid_target,self.df_date,self.df_object,self.df_float]
        pre_df = pd.concat(pre_list,axis=1)
        return pre_df          



class FeatureValidation(YottaX):
    def train_test(self):
        from sklearn.model_selection import train_test_split
        self.X_train,self.X_test,self.y_train,self.y_test = \
        train_test_split(self.df.drop(self.target,1),self.df[self.target])
        
        
    def fit_model(self,df):
        self.df = df
        self.train_test()
        
        
        import xgboost as xgb
        print(self.model_type)
        if self.model_type == 'classification':
            from sklearn.ensemble import RandomForestClassifier
            model = RandomForestClassifier()
        else:
            from sklearn.ensemble import RandomForestRegressor
            model = RandomForestRegressor()
            
        model.fit(self.X_train,self.y_train)
        self.y_pred = model.predict(self.X_test)





            
#==============================================================================
# author : Anshul    
#==============================================================================

# Assume you are given the following
#self.X_train,self.y_train,self.X_test,self.y_test

class Accuracy(FeatureValidation):
        
    def model_accuracy(self):
        if self.model_type == 'classification':
            self.val = self.f_score()
        else:
            self.val = self.rmse()
            
        return self.val
#==============================================================================
#     @abstractmethod
#     def find_accuracy(self):
#         pass
#==============================================================================
# Now check accuracy for Regression and Classification models
#class RegressionAccuracy(Accuracy):
    def rmse(self):
        from sklearn.metrics import mean_squared_error
        return np.sqrt(mean_squared_error(self.y_test, self.y_pred))

    
#class ClassificationAccuracy(Accuracy):
    def f_score(self):
        from sklearn.metrics import f1_score
        return f1_score(self.y_test,self.y_pred, average='micro')

