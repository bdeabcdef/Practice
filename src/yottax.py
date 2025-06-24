# -*- coding: utf-8 -*-
"""
Created on Fri Feb 23 15:09:14 2018

@author: Suresh
"""
import warnings
warnings.filterwarnings("ignore")

import pandas as pd
import numpy as np

from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import RFECV

from sklearn.model_selection import train_test_split,RandomizedSearchCV,\
            GridSearchCV,StratifiedKFold,KFold,ShuffleSplit
from sklearn.metrics import r2_score,accuracy_score
import xgboost as xgb
from scipy.stats import boxcox



class YottaX(object):
    def __init__(self,df):
        self._df = df
        self.identify_dtypes()
        self.replace_nulls()
        self.normalize_df()
        
        
    def identify_dtypes(self):
        self.obj_types = {'categorical':[],'discrete':[],'continuous':[] }
        for var in self._df.columns:
            if self._df[var].dtype == 'O':
                self.obj_types['categorical'].append(var)
            elif self._df[var].nunique() < 20:
                self.obj_types['discrete'].append(var)
            else:
                self.obj_types['continuous'].append(var)
        
    def replace_nulls(self):
        for col in self.obj_types['categorical']:
            if self._df[col].isnull().mean() > 0:
                self._df[col].fillna('missing',inplace=True)
        for col in self.obj_types['discrete']:
            if self._df[col].isnull().mean() > 0:
                self._df[col].fillna(self._df[col].median(),inplace=True)
        for col in self.obj_types['continuous']:
            if self._df[col].isnull().mean() > 0:
                self._df[col].fillna(self._df[col].median(),inplace=True)
        
    def normalize_df(self):
        for var in self.obj_types['continuous']:
            if (self._df[var]<=0).any():
                self._df[var] = self._df[var] - self._df[var].min() + 1
            self._df[var] = boxcox(self._df[var]+1)[0]
            
        for var in self.obj_types['categorical']:
            temp = self._df.groupby([var])[var].count()/np.float(len(self._df))
            frequent_cat = [x for x in temp.loc[temp>0.03].index.values]
            self._df[var] = np.where(self._df[var].isin(frequent_cat), 
                                    self._df[var], 'Rare')
                                    
        for var in self.obj_types['categorical']:
            label_names = self._df[var].unique()
            label_vals = {k:i for i, k in enumerate(label_names, 0)}
            self._df[var] = self._df[var].map(label_vals)
            
        scaler = StandardScaler()
        scaler.fit(self._df)
            
    def scale_features(self):
        data_new = self._df.copy()
        df_cardinality = pd.DataFrame(columns=['cardinality'])
        for var in self.obj_types['categorical']:
            df_cardinality.loc[var] = len(self._df[var].unique())
        df_cardinality= df_cardinality.sort_values(by='cardinality') 
        df_unique_sorted_cardinality = pd.DataFrame(df_cardinality['cardinality'].unique())
        df_unique_sorted_cardinality_lowest_3 = df_unique_sorted_cardinality.iloc[:3,:]
        df_unique_sorted_cardinality_lowest_5 = df_unique_sorted_cardinality.iloc[:5,:]
        lowest_3_columns = []
        lowest_5_columns = []
        for i in df_unique_sorted_cardinality_lowest_3.values:
            lowest_3_columns.append((df_cardinality[df_cardinality['cardinality']==int(i)].index))
        for i in df_unique_sorted_cardinality_lowest_5.values:
            lowest_5_columns.append((df_cardinality[df_cardinality['cardinality']==int(i)].index))
        for j in lowest_3_columns: 
            for var in j: 
                data_dummy = pd.get_dummies(data_new[var],prefix=var)
                data_new=data_new.join(data_dummy)
        return data_new
            
    def split_data(self,X,y):
        ts=0.3
        rs=0
        X_train,X_test,y_train,y_test = train_test_split(X,y,
                                                    test_size=ts,random_state=rs)
        return X_train,X_test,y_train,y_test
                
        
class YottaRegressor(YottaX):
    def __init__(self,df,uid,target):
        self.ut = df[[uid,target]]
        self.target = target
        super().__init__(df.drop([uid,target],axis=1))
        self.feature_transformation()
        self.feature_ranking()
        
    def feature_transformation(self):
        self.ut[self.target] = np.log(self.ut[self.target])
        self.cardinal_df = pd.concat([self.ut,self.scale_features()],axis=1)
        X = self.cardinal_df.drop(self.target,1)
        y = self.cardinal_df[self.target]
        self.X_train, self.X_test, self.y_train, self.y_test = self.split_data(X,y)
        
    def feature_ranking(self):
        reg_model = xgb.XGBRegressor(
                                    objective='reg:linear', 
                                    n_estimators=100, 
                                    learning_rate=0.08, 
                                    max_depth=5, 
                                    nthread=4,
                                    subsample=0.9,
                                #    colsample_bytree=0.8,
                                    reg_lambda=6,
                                    reg_alpha=5,
                                    seed=1301,
                                    silent=True
                                )
        selector = RFECV(estimator=reg_model, step=3,cv=KFold(shuffle=True,random_state=1301),
                         scoring='r2')
        selector.fit(self.X_train, self.y_train)
        print('The optimal number of features is {}'.format(selector.n_features_))
        features = [f for f,s in zip(self.X_train.columns, selector.support_) if s]
        self.X_train_new = self.X_train[features]
        self.X_test_new  = self.X_test[features]
        
    def feature_optimization(self):
        model = xgb.XGBRegressor()
#run model 10x with 60/30 split intentionally leaving out 10%
        cv_split = ShuffleSplit(n_splits = 5, test_size = .3, train_size = .6, random_state = 0 ) 
        grid_n_estimator = [10, 50, 100, 300]
        grid_learn = [.01, .03, .05, .1, .25]
        grid_seed = [0]
        param = {  'max_depth': [1,2,4,6,8,10], #default 2,
                    'learning_rate': grid_learn, #default: .3,
                    'n_estimators': grid_n_estimator, 
                    'seed': grid_seed  
                 }
#==============================================================================
#         param = {
#         'min_child_weight': [1, 5, 10],
#         'gamma': [0.5, 1, 1.5, 2, 5],
#         'subsample': [0.6, 0.8, 1.0],
#         'colsample_bytree': [0.6, 0.8, 1.0],
#         'max_depth': [3, 4, 5]
#         }
#==============================================================================
        #start = time.perf_counter()  
        best_search = GridSearchCV(estimator = model, param_grid = param, cv = cv_split, scoring = 'r2')
        best_search.fit(self.X_train_new,self.y_train)
        #run = time.perf_counter() - start
        best_estimator = best_search.best_estimator_
        print(best_estimator)
        return best_estimator
        
    def model_build(self):
        best_model = self.feature_optimization()
        best_model.fit(self.X_train_new,self.y_train)
        y_pred = best_model.predict(self.X_test_new)
        return y_pred

    def model_accuracy(self):
        self.y_pred = self.model_build()
        return format(r2_score(self.y_test,self.y_pred)*100,'.2f')
        
        
class YottaClassifier(YottaX):
    def __init__(self,df,uid,target):
        self.ut = df[[uid,target]]
        self.target = target
        super().__init__(df.drop([uid,target],axis=1))
        self.feature_transformation()
        self.feature_ranking()
        
    def feature_transformation(self):
        self.ut[self.target] = pd.factorize(self.ut[self.target])[0]
        self.cardinal_df = pd.concat([self.ut,self.scale_features()],axis=1)
        X = self.cardinal_df.drop(self.target,1)
        y = self.cardinal_df[self.target]
        self.X_train, self.X_test, self.y_train, self.y_test = self.split_data(X,y)
        
    def feature_ranking(self):
        reg_model = xgb.XGBClassifier(
                                    objective='binary:logistic', 
                                    n_estimators=100, 
                                    learning_rate=0.08, 
                                    max_depth=5, 
                                    nthread=4,
                                    subsample=0.9,
                                #    colsample_bytree=0.8,
                                    reg_lambda=6,
                                    reg_alpha=5,
                                    seed=1301,
                                    silent=True
                                )
        selector = RFECV(estimator=reg_model, step=3,cv=StratifiedKFold(shuffle=True,random_state=1301),
                         scoring='accuracy')
        selector.fit(self.X_train, self.y_train)
        print('The optimal number of features is {}'.format(selector.n_features_))
        features = [f for f,s in zip(self.X_train.columns, selector.support_) if s]
        self.X_train_new = self.X_train[features]
        self.X_test_new  = self.X_test[features]
        
    def feature_optimization(self):
        model = xgb.XGBClassifier(
                                    objective='binary:logistic', 
                                    n_estimators=100, 
                                    learning_rate=0.02)
#run model 10x with 60/30 split intentionally leaving out 10%
        cv_split = ShuffleSplit(n_splits = 5, test_size = .3, train_size = .6, random_state = 0 ) 
        grid_n_estimator = [10, 50, 100, 300]
        grid_learn = [.01, .03, .05, .1, .25]
        grid_seed = [0]
        param = {  'max_depth': [1,2,4,6,8,10], #default 2,
                    'learning_rate': grid_learn, #default: .3,
                    'n_estimators': grid_n_estimator, 
                    'seed': grid_seed  
                 }
        #start = time.perf_counter()  
        best_search = GridSearchCV(estimator = model, param_grid= param, cv = cv_split, scoring = 'accuracy')
        best_search.fit(self.X_train_new,self.y_train)
        #run = time.perf_counter() - start
        best_estimator = best_search.best_estimator_
        print(best_estimator)
        return best_estimator
        
    def model_build(self):
        best_model = self.feature_optimization()
        best_model.fit(self.X_train_new,self.y_train)
        y_pred = best_model.predict(self.X_test_new)
        return y_pred

    def model_accuracy(self):
        self.y_pred = self.model_build()
        return format(accuracy_score(self.y_test,self.y_pred)*100,'.2f')