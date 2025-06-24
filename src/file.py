     
        
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 13 15:52:54 2016

@author: Suresh
"""
import os
import pandas as pd
import numpy as np
import sqlalchemy 
import sqlite3

import yotta_x as yt

class ReadCsv(object):
    def __init__(self,uid):
        self.xcoord = None
        self.ycoord = None
        self.uid = uid
        self.filepath = None
        self.sep = ','
        self.inputList = []
        self.df = None
        self.image = 'Read CSV'
        
    def get_dataframe(self,nrows=None):
        if self.filepath is not None:
            self.df =  pd.read_csv(self.filepath,nrows=nrows,sep=self.sep,encoding="ISO-8859-1")
            return self.df
        
    def get_columns(self):
        df = self.get_dataframe(nrows=10)
        return df.columns.tolist()
        
    def is_list_empty(self):
        return True

class Lstm(object):
    def __init__(self,uid):
        self.xcoord = None
        self.ycoord = None
        self.uid = uid
        self.filepath = None
        self.sep = ','
        self.inputList = []
        self.df = None
        self.image = 'LSTM'
        
    def is_list_empty(self):
        return True
        
        
class LoadRepo(object):
    def __init__(self,uid):
        self.xcoord = None
        self.ycoord = None
        self.uid = uid
        self.filepath = None
        self.inputList = []
        self.df = None
        self.image = 'loadrepo'
        
    def get_dataframe(self,nrows=None):
        self.df =  pd.read_pickle(self.filepath)
        return self.df
        
    def get_columns(self):
        df = self.get_dataframe(nrows=10)
        return df.columns.tolist()

    def is_list_empty(self):
        return True
        
class ReadJson(object):
    def __init__(self,uid):
        self.xcoord = None
        self.ycoord = None
        self.uid = uid
        self.filepath = None
        self.inputList = []
        self.df = None
        self.image = 'Read Json'
        
    def get_dataframe(self,nrows=None):
        if self.filepath is not None:
            self.df =  pd.read_json(self.filepath,nrows=nrows)
            return self.df
        
    def get_columns(self):
        df = self.get_dataframe(nrows=10)
        return df.columns.tolist()
        
    def is_list_empty(self):
        return True

class ReadExcel(object):
    def __init__(self,uid):
        self.xcoord = None
        self.ycoord = None
        self.uid = uid
        self.filepath = None
        self.inputList = []
        self.df = None
        self.image = 'Read Excel'
        self.sheetname = 0
        
    def get_dataframe(self,skiprows=None):
        if self.filepath is not None:
            self.df =  pd.read_excel(self.filepath,sheetname=self.sheetname,skiprows=skiprows)
            return self.df
        
    def get_columns(self):
        df = self.get_dataframe(skiprows='10:')
        return columns

    def is_list_empty(self):
        return True
 
class ManualReplace(object):
    def __init__(self,uid):
        self.xcoord = None
        self.ycoord = None
        self.uid = uid
        self.inputList = []
        self.dfs = dict()
        self.df=None
        self.replace_value=None
        self.image = 'Manual Replace'
        
    def get_dataframe(self):
        
        input_df = self.dfs[self.inputList[0]]
        print('inside manual replace')
        self.df = input_df.fillna(self.replace_value)
        return self.df
        
    def is_list_empty(self):
        return False
        
class AutoReplace(object):
    def __init__(self,uid):
        self.xcoord = None
        self.ycoord = None
        self.uid = uid
        self.inputList = []
        self.dfs = dict()
        self.df=None
        self.autoreplace_value=None
        self.image = 'Auto Replace'
        
        
    def get_dataframe(self):
        input_df = self.dfs[self.inputList[0]]
        print('inside autoreplace')
        fill = pd.Series([input_df[c].value_counts().index[0]
            if input_df[c].dtype == np.dtype('O') else input_df[c].mean() for c in input_df],
            index=input_df.columns)
        self.df = input_df.fillna(fill)
        return self.df
        
    def is_list_empty(self):
        return False
        
class Normalize(object):
    def __init__(self,uid):
        self.xcoord = None
        self.ycoord = None
        self.uid = uid
        self.inputList = []
        self.dfs = dict()
        self.df=None
        self.unique_column_id=None
        self.image = 'Normalize'
        
        
    def get_dataframe(self):
        input_df = self.dfs[self.inputList[0]]
        print('inside normalize')
        self.decol=input_df.select_dtypes(exclude=[object]).columns
        for i in self.decol:
            if self.unique_column_id not in i:
                input_df[i] = (input_df[i]-input_df[i].min())/(input_df[i].max()-input_df[i].min()) 
        self.df = input_df   
        return self.df
        
    def is_list_empty(self):
        return False

class Standardize(object):
    def __init__(self,uid):
        self.xcoord = None
        self.ycoord = None
        self.uid = uid
        self.inputList = []
        self.dfs = dict()
        self.df=None
        self.unique_column_id=None
        self.target = None
        self.image = 'Normalize'
        
        
    def get_dataframe(self):
        from sklearn.preprocessing import StandardScaler
        sc = StandardScaler()
        
        input_df = self.dfs[self.inputList[0]]
        
        self.decol=[e for e in input_df.select_dtypes(exclude=[object]).columns
                    if e not in (self.unique_column_id,self.target)]
       
#        self.decol=[e for e in input_df.select_dtypes(exclude=[object]).columns
#                    ]
        
        input_df[self.decol] =sc.fit_transform(input_df[self.decol])
        self.df = input_df   
        return self.df
        
    def is_list_empty(self):
        return False
        
class ExtendColumns(object):
    def __init__(self,uid):
        self.xcoord = None
        self.ycoord = None
        self.uid = uid
        self.inputList = []
        self.dfs = dict()
        self.df = None
        self.f_col = None
        self.ops_val = None
        self.s_col = None
        self.col_name = None
        self.image = 'Extend Columns'
        
    def get_dataframe(self):
        self.input_df = self.dfs[self.inputList[0]]
        if self.ops_val == 'Concatenate':
            #print('inside if')
            self.input_df[self.col_name] = self.input_df[self.f_col].dropna().astype(str) + self.input_df[self.s_col].dropna().astype(str)
            self.df = self.input_df.copy()
            return self.df
        else:
            return self.input_df
    
    
    def is_list_empty(self):
        return False
        

        
class Join(object):
    def __init__(self,uid):
        self.xcoord = None
        self.ycoord = None
        self.uid = uid
        self.inputList = []
        self.dfs = dict()
        self.df=None
        self.keys= []
        self.join_type=None
        self.image = 'Join'
        self.columns = []
        
    def get_dataframe(self):
        left_df = self.dfs[self.inputList[0]]
        right_df = self.dfs[self.inputList[1]]
        self.df = pd.merge(left_df,right_df,how=self.join_type,on=self.keys).reset_index()
        return self.df
        
    def is_list_empty(self):
        return False

class UidGenerator(object):
    def __init__(self,uid):
        self.xcoord = None
        self.ycoord = None
        self.uid = uid
        self.inputList = []
        self.dfs = dict()
        self.df=None
        self.seperator = None
        self.uid_cols = list()
        self.image = 'Uid-generator'
        
    def get_dataframe(self):
        input_df = self.dfs[self.inputList[0]]
        self.df = input_df
#        combined_list = self.seperator.join(str(elem) for elem in self.uid_cols)
#        self.df['UID'] = self.df[list(self.uid_cols)]
#        self.df = self.df.assign(UID=combined_list)
        self.df['UID'] = self.df[self.uid_cols].apply(lambda x: self.seperator.join(map(str,x.values)), axis=1)
        return self.df
            
    def is_list_empty(self):
        return False
        
class RawScript(object):
    def __init__(self,uid):
        self.xcoord = None
        self.ycoord = None
        self.uid = uid
        self.inputList = []
        self.dfs = dict()
        self.df=None
        self.seperator = None
        self.code = []
        self.image = 'Raw-script'
        
    def get_dataframe(self,input_df=None):
        if input_df.empty:
            input_df = self.dfs[self.inputList[0]]
        for chunk in self.code:
            try:
                exec(chunk)
#                locals()[chunk]
            except:
                return 'incorrect code'
        self.df = input_df
        return self.df

    def is_list_empty(self):
        return False
        
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
class Filter(object):
    def __init__(self,uid):
        self.xcoord = None
        self.ycoord = None
        self.inputList = []
        self.uid = uid
        self.dfs=dict()
        self.df=None
        self.column=None
        self.type=None
        self.value=None
        self.image='Filter Data'
        
    def get_dataframe(self):
        input_df = self.dfs[self.inputList[0]]
        if input_df['{}'.format(self.column)].dtype == 'object':
            print('inside')
            self.value=self.value.strip()
            self.df = input_df.query('{0}{1}"{2}"'.format(self.column,self.type,self.value))
        else :
            self.df = input_df.query('{0}{1}{2}'.format(self.column,self.type,self.value))
        return self.df
    
    def is_list_empty(self):
        return False
##################################

class Aggregate(object):
    def __init__(self,uid):
        self.xcoord = None
        self.ycoord = None
        self.inputList = []
        self.uid = uid
        self.dfs=dict()
        self.df=None
        self.column=None
        self.aggregator=None
        self.image='Aggregate'

    def get_dataframe(self):
        input_df = self.dfs[self.inputList[0]]
        print('inside group')
        self.df = input_df.groupby(self.column).agg(self.aggregator).reset_index()
        return self.df

    def is_list_empty(self):
        return False
#########################


class Sort(object):
    def __init__(self,uid):
        self.xcoord = None
        self.ycoord = None
        self.inputList = []
        self.uid = uid
        self.dfs=dict()
        self.df=None
        self.column=None
        self.sort_type=None
        self.image='Sort Data'

    def get_dataframe(self):
        input_df = self.dfs[self.inputList[0]]
        print('inside sort')
        if not self.sort_type == 'ascending':
            self.df = input_df.sort_values(self.column,ascending=False).reset_index().drop('index',1)
        else:
            self.df = input_df.sort_values(self.column,ascending=True).reset_index().drop('index',1)
        return self.df

    def is_list_empty(self):
        return False

############################

class Transpose(object):
    def __init__(self,uid):
        self.xcoord = None
        self.ycoord = None
        self.inputList = []
        self.uid = uid
        self.dfs=dict()
        self.df=None
        self.image='Transpose Data'

    def get_dataframe(self):
        input_df = self.dfs[self.inputList[0]]
        print('inside transpose')
        self.df = input_df.T
        return self.df

    def is_list_empty(self):
        return False
##############################
class Pivot(object):
    def __init__(self,uid):
        self.xcoord = None
        self.ycoord = None
        self.inputList = []
        self.uid = uid
        self.dfs=dict()
        self.df=None
        self.column = None
        self.index_column = None
        self.pivot_agg = None
        self.image='Pivot Data'

    def get_dataframe(self):
        input_df = self.dfs[self.inputList[0]]
        print('inside pivot')
        self.df = input_df.pivot_table(columns=self.column,index=self.index_column,aggfunc=self.pivot_agg)
        return self.df

    def is_list_empty(self):
        return False
        
class SplitData(object):
    def __init__(self,uid):
        self.xcoord = None
        self.ycoord = None
        self.uid = uid
        self.inputList = []
        self.dfs = dict()
        self.df=None
        self.image = 'Split Data'
        
################## Start of Append ################

class Append(object):
    def __init__(self, uid):
        self.xcoord = None
        self.ycoord = None
        self.uid = uid
        self.inputList = []
        self.dfs = dict()
        self.image = 'Append'
        self.df = None
        
    def get_dataframe(self):
        print('Inside Append')
        left_df = self.dfs[self.inputList[0]]
        right_df = self.dfs[self.inputList[1]]
        self.df = left_df.append(right_df, ignore_index = True)
        return self.df	
 
    def is_list_empty(self):
        return False
			
						
################### End of Append ###################		

############### Start of Drop Duplicates ################

class DropDuplicates(object):
    def __init__(self, uid):
        self.xcoord = None
        self.ycoord = None
        self.uid = uid
        self.inputList = []
        self.dfs = dict()
        self.image = 'Duplicate'
        self.df = None
        
    def get_dataframe(self):
        print('Inside Drop Duplicates')
        df_drop = self.dfs[self.inputList[0]]
        self.df = df_drop.drop_duplicates()
        return self.df
    
    def is_list_empty(self):
        return False
        
							
############# End of Drop Duplicates ####################	

################# Start of Remove Null #################

class RemoveNull(object):
    def __init__(self, uid):
        self.xcoord = None
        self.ycoord = None
        self.uid = uid
        self.inputList = []
        self.dfs = dict()
        self.image = 'Duplicate'
        self.df = None
        
    def get_dataframe(self):
        print('Inside Remove Nulls')
        df = self.dfs[self.inputList[0]]
        n_samples = df.shape[0]
        for col in df.columns:
            n_zeros = sum(pd.isnull(df[col]))
            if (n_zeros*100)/n_samples >=80:
                df.drop(col,axis=1,inplace=True)
                
#        self.df = df.dropna(how='all',axis=1)
        self.df = df
        return self.df
    
    def is_list_empty(self):
        return False

################# End of Remove null ##################							
        
class LinearDiscriminantAnalysis(object):
    def __init__(self,uid):
        self.xcoord = None
        self.ycoord = None
        self.uid = uid
        self.inputList = []
        self.dfs = dict()
        self.df=None
        self.dimension = None
        self.image = 'LDA'
        
    def get_dataframe(self,X,y,u_id):
        print('lda',self.dimension)
        from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
        clf = LinearDiscriminantAnalysis(n_components=int(self.dimension))
        narray = clf.fit_transform(X,y)
        self.df = pd.concat([u_id,pd.DataFrame(narray,columns=['Lda']),y],axis=1)
        return self.df            
            
    def is_list_empty(self):
        return False
        
class PrincipalComponentAnalysis(object):
    def __init__(self,uid):
        self.xcoord = None
        self.ycoord = None
        self.uid = uid
        self.inputList = []
        self.dfs = dict()
        self.df=None
        self.dimension = None
        self.image = 'LDA'
        
    def get_dataframe(self,X,y,u_id):
        print('pca',self.dimension)
        from sklearn.decomposition import PCA
        clf = PCA(n_components=int(self.dimension))
        narray = clf.fit_transform(X)
        self.df = pd.concat([u_id,pd.DataFrame(narray,columns=['Pca-{}'.format(i) for i in range(int(self.dimension))]),y],axis=1)
        return self.df            
            
    def is_list_empty(self):
        return False

class Predict(object):
    def __init__(self,uid):
        self.xcoord = None
        self.ycoord = None
        self.uid = uid
        self.inputList = []
        self.filepath = None
        self.dfs = dict()
        self.df=None
        self.image = 'Predictive'        
    
    def get_dataframe(self,nrows=None):
        if self.filepath is not None:
            self.df =  pd.read_csv(self.filepath,nrows=nrows)
            return self.df
            
    def merge_dataframe(self,x,y):
        df = pd.concat([x,y],axis=1)
        return df
        
    def get_columns(self):
        df = self.get_dataframe(nrows=10)
        columns = [col for col in df.columns]
        return columns
        
class Recommend(object):
    def __init__(self,uid):
        self.xcoord = None
        self.ycoord = None
        self.uid = uid
        self.inputList = []
        self.dfs = dict()
        self.df=None
        self.image = 'Recommend'
        self.uid = None
        self.response = None


class Manual(object):
    def __init__(self,uid):
        self.xcoord = None
        self.ycoord = None
        self.uid = uid
        self.inputList = []
        self.dfs = dict()
        self.df=None
        self.image = 'Manual'
        self.feats = None
        self.uid = None
        self.response = None
    
    def categorize(self):
        self.data = self.dfs[self.inputList[0]]
        
        tcat = [self.data.select_dtypes(include=[object]).columns]
        cat=[]
        for i in tcat:
            self.data[i] = self.data[i].astype('category')
            cat.append(i)
        self.data[cat] = self.data[cat].apply(lambda x:x.cat.codes)
        return self.data    
    
    def get_dataframe(self,feats,uid,response):
        from sklearn.model_selection import train_test_split
        self.c_data = self.categorize()
#        print(self.c_data[feats].head(5))
        self.X = self.c_data[feats]
        self.y = self.c_data[response]
        self.z = self.c_data[uid]
        self.X = self.X.fillna(0)
        self.y = self.y.fillna(0)
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.X, self.y, random_state=1)
        self.z_train,self.z_test = train_test_split(self.z,random_state=1)
        return self.X_train,self.y_train,self.X_test,self.z_test

class RunModel(object):
    def __init__(self,uid):
        self.xcoord = None
        self.ycoord = None
        self.uid = uid
        self.inputList = []
        self.dfs = dict()
        self.df=None
        self.image = 'Run Model'
        
class CrossValidation(object):
    def __init__(self,uid):
        self.xcoord = None
        self.ycoord = None
        self.uid = uid
        self.inputList = []
        self.dfs = dict()
        self.df=None
        self.image = 'Cross-validation'        
        
class MeanSquaredError(object):
    def __init__(self,uid):
        self.xcoord = None
        self.ycoord = None
        self.uid = uid
        self.inputList = []
        self.dfs = dict()
        self.df=None
        self.image = 'MSE' 
        
class TextPreprocess(object):
    def __init__(self,uid):
        self.xcoord = None
        self.ycoord = None
        self.uid = uid
        self.inputList = []
        self.dfs = dict()
        self.df=None
        self.feature = None
        self.image = 'Text Preprocess' 
        self.stop_words = None
        self.analyzer = None
        self.norm = None
        
    def preprocessor(self,text):
        from sklearn.feature_extraction.text import TfidfVectorizer
        tfidf = TfidfVectorizer(stop_words='english',ngram_range=(1, 1),
                                analyzer=self.analyzer,norm=None)
        tf_val = tfidf.fit_transform(text)
        tf_df = pd.SparseDataFrame(tf_val,columns=tfidf.get_feature_names(),default_fill_value=0)
        return tf_df
        
    def get_dataframe(self):
        input_df = self.dfs[self.inputList[0]]
        transformed_df = self.preprocessor(input_df[self.feature])        
        self.df = pd.concat([input_df,transformed_df],axis=1)
        return self.df
        
    def is_list_empty(self):
        return False

class ImportModel(object):
    def __init__(self,uid):
        self.xcoord = None
        self.ycoord = None
        self.uid = uid
        self.inputList = []
        self.dfs = dict()
        self.df=None
        self.image = 'Import Model'

    def models_list(self):
        return next(os.walk(os.path.join(os.pardir,'model')))[1]

    def retrieve_model(self,mname):
        from sklearn.externals import joblib
        loaded_mdl =  joblib.load('{0}\\{1}.mdl'.format(mname,mname))       
        return loaded_mdl
    
    
class ExportModel(object):
    def __init__(self,uid):
        self.xcoord = None
        self.ycoord = None
        self.uid = uid
        self.inputList = []
        self.dfs = dict()
        self.df=None
        self.image = 'Export Model'
        
    def save_model(self,filename,model):
        state = False
        from sklearn.externals import joblib
        try:
            model_dir = os.path.join(os.pardir,'model')
            os.chdir(model_dir)
            if not os.path.exists(filename):
                os.makedirs(filename)
                ndir = os.path.join(model_dir,filename)
                joblib.dump(model, "{0}\\{1}.mdl".format(ndir,filename))
            state = True
        except:
            state = False
        finally:
            return state
            
class ToFile(object):
    def __init__(self,uid):
        self.xcoord = None
        self.ycoord = None
        self.uid = uid
        self.inputList = []
        self.dfs = dict()
        self.df=None
        self.image = 'To File'
        
class ImgProcess(object):
    def __init__(self,uid):
        self.xcoord = None
        self.ycoord = None
        self.uid = uid
        self.inputList = []
        self.dfs = dict()
        self.df=None
        self.image = 'Image Process'
        

##################### To Database Operator ##########################	
							
class ToDatabase(object):
    
    def __init__(self,uid):
        
        self.xcoord = None
        self.ycoord = None
        self.uid = uid
        self.result = None
        self.table_name = None
        self.image = 'To Database'
        self.db_filename = '../secured/connections1.db'
        self.query = 'SELECT * FROM connections'
        self.connection_name = None
        
      
    def init_engine(self):
        conn = sqlite3.connect(self.db_filename)
        cursor = conn.cursor()
        self.query_result = cursor.execute(self.query)
        self.conn_name = [i[0] for i in self.query_result]
        return self.conn_name

    def connection_type(self,name):
        conn = sqlite3.connect(self.db_filename)
        cursor = conn.cursor()						
        self.query_result = cursor.execute(self.query)
        for i in self.query_result:
            for j in i:
                if j == name:
                    con_type = i[1]
                    c_name = i[2]
                    sch_name = i[4]
                    u_name = i[5]
                    pwd = i[6]
                    return con_type,c_name,sch_name,u_name,pwd
						
						
    def write_db(self,con_name,table_name,result):
        connection_name,c_name,sch_name,u_name,pwd = self.connection_type(con_name)    
        if connection_name == 'MySql':
            self.engine = sqlalchemy.create_engine('mysql+pymysql://{0}:{1}@localhost/{2}'.format(u_name,pwd,sch_name))
            result.to_sql(name=table_name,con=self.engine)
            return self.engine
        elif connection_name == 'SQLServer':
            self.engine = sqlalchemy.create_engine('mssql+pyodbc://{0}:{1}@localhost/database'.format(u_name,pwd,sch_name))
            return self.engine
        elif connection_name == 'DSN':
            self.engine = sqlalchemy.create_engine('mssql+pyodbc://user:password@{0}'.format(c_name))
            result.to_sql(name=table_name,con=self.engine)
            return self.engine

					 
						
################### End of Database Operator ########################
        
class Visualize(object):
    def __init__(self,uid):
        self.xcoord = None
        self.ycoord = None
        self.uid = uid
        self.inputList = []
        self.user = None
        self.passwd = None
        self.dbname = None
        self.engine = None
        self.df=None
        self.image = 'Visualize'
        
    def init_engine(self):
        self.engine = sqlalchemy.create_engine('mysql+pymysql://{0}:{1}@localhost'.format(self.user,self.passwd))
        return self.engine

    def db_list(self):
        insp = sqlalchemy.inspect(self.engine)
        databases = insp.get_schema_names()
        return databases         
        
    def activate_db(self):
        self.engine.execute('USE {}'.format(self.dbname))
        return self.engine
        
class Output(object):
    def __init__(self,uid):
        self.xcoord = None
        self.ycoord = None
        self.uid = uid
        self.inputList = []
        self.dfs = dict()
        self.image='output'
        
    def get_dataframe(self):
        return None
        
    def is_list_empty(self):
        return False


#==============================================================================
# Super hack code
#==============================================================================

class ShReport(object):
    def __init__(self,uid):
        self.xcoord = None
        self.ycoord = None
        self.inputList = []
        self.dfs = dict()
        self.df=None
        self.image = 'SH Report'

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
        
    def send_details(self):
        try:
            columns = self.df.shape[1]
            model_type = self.transformed_df.model_type
        except:
            return 'Run Superhack'
            
        return columns,model_type,self.acc.metrics
            
        
    def get_dataframe(self,input_df):
#        input_df = self.dfs[self.inputList[0]]
        self.transformed_df = yt.SplitDtypes(input_df,self.unique_column_id,self.target)        
        self.df = self.transformed_df.pre_df
        fs = yt.FeatureValidation(self.df,self.transformed_df.model_type,self.target)
        actual, pred = fs.fit_model()
        self.acc = yt.Accuracy(actual,pred,self.transformed_df.model_type)
        print('accuracy=',self.acc.metrics)        
#        self.send_details()
        return self.df

    def is_list_empty(self):
        return False
