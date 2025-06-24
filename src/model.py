# -*- coding: utf-8 -*-
"""
Created on Wed Apr 27 15:03:03 2016

@author: Suresh
"""
from configurations import *
import pandas as pd
import numpy as np
class FileHandle:
    
    def __init__(self):
        self.raw_data = None
        self.uid = None        
        self.features = []
        self.response = None
        
    def openfile(self,open_data):
#==============================================================================
#         from tkinter import filedialog as fd
#         
#         open_data = fd.askopenfilename(filetype = (("Csv Files(*.csv)", ".csv"),
#                                                    ("Json Files(*.json)",".json"),
#                                                     ("Zip Files(*.zip)",".zip"),
#                                                     ("gz Files(*.gz)",".gz")))
#==============================================================================
        from datetime import datetime
        tstart = datetime.now()
        if open_data[-3:] == 'csv':
            self.raw_data = pd.read_csv(open_data,encoding='utf-8',parse_dates=True)   
        elif open_data[-4:] == 'json':
            self.raw_data = pd.read_json(open_data)
        elif open_data[-3:] == 'zip':
            import zipfile
            ze = zipfile.ZipFile(open_data)
            self.raw_data = pd.io.parsers.read_table(ze.open(ze.namelist()[0]))
        elif open_data[-2:] == 'gz':
            self.raw_data = pd.read_csv(open_data,encoding='utf-8',compression='gzip')   

        tend = datetime.now()
        print(tend-tstart)
        #--------fill Nan values------------------#
        
#        from sklearn.preprocessing import Imputer
#        imr = Imputer(missing_values='NaN', strategy='mean', axis=0)
#
#        self.raw_data = imr.fit_transform(self.raw_data)
        self.raw_data = self.raw_data.applymap(lambda x: np.NaN if isinstance(x, str) and x.isspace() else x)
        columns = [col for col in self.raw_data.columns]
        return self.raw_data,columns
            
    def database(self):
        import pymysql
        self.dbconnection = pymysql.connect(host='localhost',
                                       user='root',
                                       password='',
                                       db='fraud',
                                       charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
        self.raw_data = pd.read_sql('select * from ccard',con=self.dbconnection)
        self.raw_data = self.raw_data.dropna(how='all',axis=1)
        self.columns = [col for col in self.raw_data.columns]
        self.dbconnection.close()
        return self.raw_data,self.columns
        
    def datatables(self,table):
        self.raw_data = pd.read_sql('select * from {}'.format(table),con=self.dbconnection)
        self.columns = [col for col in self.raw_data.columns]
        self.dbconnection.close()
        return self.raw_data,self.columns

    def data(self):
        import pymysql
        self.dbconnection = pymysql.connect(host='localhost',
                                       user='root',
                                       password='',
                                       db='fraud',
                                       charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)

        table = pd.read_sql('show tables',con=self.dbconnection)
        return table

    def replace_null(self,val):
        self.raw_data = self.raw_data.fillna(val)
        return self.raw_data
        
#==============================================================================
#     def auto_replace(self):
#         from sklearn.preprocessing import Imputer
#         imr = Imputer(missing_values='nan', strategy='mean', axis=0)
#         self.raw_data = imr.fit_transform(self.raw_data)
# #        self.raw_data = self.raw_data.fillna(self.raw_data.mean())        
#         print(self.raw_data.head())
#         return self.raw_data
#==============================================================================

    def auto_replace(self):
        from custom_imputer import DfImputer
        self.raw_data = DfImputer().fit_transform(self.raw_data)
        return self.raw_data

#==============================================================================
#     def normalize(self,val):
# #        cols=[]
#         self.decol=self.raw_data.select_dtypes(exclude=[object]).columns
#         self.n_data=self.raw_data[self.decol]
#         self.n_data.drop(val,axis=1,inplace=True)
# #        self.raw_data[self.decol] = self.n_data.apply(lambda x:(x-x.min())/(x.max()-x.min()))
#         self.n_data = self.n_data.apply(lambda x:(x-x.min())/(x.max()-x.min()))
#         self.n_data = self.n_data.combine_first(self.raw_data)
#         return self.n_data
#==============================================================================
   
    def normalize(self,val):
        self.decol=self.raw_data.select_dtypes(exclude=[object]).columns
        for i in self.decol:
            if val not in i:
                self.raw_data[i] = (self.raw_data[i]-self.raw_data[i].min())/(self.raw_data[i].max()-self.raw_data[i].min())           
        return self.raw_data

    def categorize(self,uid,data):
        try:
            idf = data[uid]
            data = data.drop(uid,axis=1)
        except:
            pass
        tcat = data.select_dtypes(include=[object]).columns.tolist()
        for cat in tcat:
            cm = {label:idx for idx,label in enumerate(np.unique(data[cat]))}
            data[cat] = data[cat].map(cm)
        
#        data[tcat] = pd.Categorical(data[tcat]).codes
        try:
            n_data = pd.concat([data,idf],axis=1)
        except:
            pass
        return n_data
        
    def train_test_split(self,size):
        from sklearn.model_selection import train_test_split
        c_data = self.raw_data.copy()
        print(c_data.head())
        print('values=',self.features,self.response,self.uid,sep='\t')
        X = c_data[self.features]
        y = c_data[self.response]
        z = c_data[self.uid]
        print('in train-test split')
        print('before train')
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(X, y, random_state=1)
        self.z_train,self.z_test = train_test_split(z,random_state=1)
        print('after train-test split')
        return self.X_train,self.y_train,self.X_test,self.y_test,self.z_test

    def predict(self,model,test):
        if self.uid in test.columns:
            test_data = self.categorize(self.uid,test)
        else:
            raise 'Unique ID not matched'
        self.output_index = test[self.uid]
#==============================================================================
#         self.predicted = model.predict(test_data[self.features])
#         res = pd.DataFrame({'Id':test[self.uid],'predicted': self.predicted})
#         return res
#==============================================================================
        res = model.predict(test_data[self.features])
        return res
        
    def to_predict(self,model):
        predicted = model.predict(self.X_test)
        return predicted

    
    def ranking(self,forest,uid,response):
        from sklearn.feature_selection import RFE
        X= self.categorize(uid,self.raw_data)
        y=X['{}'.format(response)]
        X=X.drop([uid,response],1)
        cols=X.columns.tolist()
        estimator = RFE(forest,5)
        estimator.fit(X,y)
        self.rank =estimator.ranking_
        return self.rank,cols

    def feature_ranking(self,uid,target,algorithm):
        if algorithm == 1:
            from sklearn.ensemble import RandomForestRegressor
            forest =RandomForestRegressor()
            rank,cols = self.ranking(forest,uid,target)
        elif algorithm == 2:
            from sklearn.ensemble import GradientBoostingRegressor
            forest = GradientBoostingRegressor()
            rank,cols = self.ranking(forest,uid,target)
        return rank,cols

    def _assign_pred(self):
        self.y_true = np.array(self.y_test)
        self.predicted_bin = self.predicted
        try:
            self.predicted_bin =  np.where(self.predicted >0.5,1,0)
        except:
            try:
                self.predicted_bin =  np.where(self.pred >0.5,1,0)
            except:
                pass
      
    def model_accuracy(self,predicted):
        from sklearn import metrics
#        self._assign_pred()
        self.y_true = np.array(self.y_test)
#        score = metrics.r2_score(self.y_true,self.predicted)
        
        try:
            score = metrics.accuracy_score(self.y_true,predicted)
#            score = metrics.f1_score(self.y_true,predicted)
        except:
            score = metrics.r2_score(self.y_test,predicted)
        return score*100

    def mse(self,predicted):
        from sklearn import metrics
#        self._assign_pred()
        self.y_true = np.array(self.y_test)
        try:
            score = metrics.mean_squared_error(self.y_true,predicted)
        except:
            pass
        return score

    def create_df(self):
        result = pd.DataFrame({'Id':self.output_index})
        return result
      
    def add_result(self,df,name,predicted):
        df[name] = predicted
        return df        
        
    def download_result(self,df,name):
        import os
        import subprocess
        odir = output_dir
        df.to_csv(os.path.join(odir,"{}.csv".format(name)),index=False)
        subprocess.Popen(['explorer',odir])

    def visualize(self,engine,result,name='fraud'):
#==============================================================================
#                     deprecated        
#==============================================================================
        
#==============================================================================
#         import pymysql
#         self.dbconnection = pymysql.connect(host='localhost',
#                                        user='root',
#                                        password='root',
#                                        db='fraud',
#                                        charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
#         result.to_sql(con=self.dbconnection,flavor='mysql',name='predicted',if_exists='replace',index=None)        
#==============================================================================
        table = 'predicted'
        pd.io.sql.execute('DROP TABLE IF EXISTS %s'%table, engine)
        result.to_sql(name='predicted',con=engine,index=None)        
        engine.dispose()        
        import webbrowser
        webbrowser.open('http://localhost/{}/index.html'.format(name))

