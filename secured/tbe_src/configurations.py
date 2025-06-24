# -*- coding: utf-8 -*-
"""
Created on Tue Sep 13 15:52:54 2016

@author: Suresh
"""

import os
from itertools import chain

user_dir = os.environ['USERPROFILE']
def create_dir(name):
    if not os.path.exists(name):
        os.makedirs(name)
        return name
    else:
        return name
        print('inside exception')

main_dir = create_dir(r'{}\.Dsf'.format(user_dir))
localrepository = create_dir(r'{}\LocalRepository'.format(main_dir))
processes_dir = create_dir(r'{}\processes'.format(main_dir))
output_dir = create_dir(r'{}\output'.format(main_dir))

#==============================================================================
# fonts
#==============================================================================

bigbutton = ('Cambria', 14)
smallbutton = ('Cambria', 10)
cambriamedium = ('Cambria',12)
cambriabig = ('Cambria',18)

#==============================================================================
# color codes
#==============================================================================

mainbg = '#BDC3C7'


#==============================================================================
# # folders and directories
#==============================================================================

top_images_dir = r"../images/top/"
top_images_list = ['1_open','2_save','3_play','4_download','6_vis']


frame_images = r"../images/top1/"
workflow_images = r"../images/workflow/"
bitimage = r'../images/yot.ico'
#localrepository = r"../LocalRepository"

operator_fns = {'CSV':'ReadCsv','Json':'ReadJson',
                'Excel':'ReadExcel','loadrepo':'LoadRepo',
                'Auto Replace':'AutoReplace','Manual Replace':'ManualReplace',
                'Normalize':'Normalize','Standardize':'Standardize','Join':'Join','Split':'SplitData','Append':'Append',
                'Duplicate':'DropDuplicates','Remove Nulls':'RemoveNull',
                'Recommend':'Recommend','Manual':'Manual','Extend Columns':'ExtendColumns',
                'Run Model':'RunModel','Predictive':'Predict',
                'To File':'ToFile','Visualize':'Visualize',
                'Cross Validate':'CrossValidation','MSE':'MeanSquaredError','To Database':'ToDatabase',
                'Filter':'Filter','Aggregate':'Aggregate','Sort':'Sort',
                'Transpose':'Transpose','Pivot':'Pivot','Raw Script':'RawScript',
                'Uid Generator':'UidGenerator','PCA':'PrincipalComponentAnalysis',
                'LDA':'LinearDiscriminantAnalysis','Import Model':'ImportModel','Export Model':'ExportModel',
                'Text Preprocess':'TextPreprocess','Image Process':'ImgProcess',
                'LSTM':'Lstm','Super Hack':'SuperHack'}

operator_parameters = {'CSV':'readcsv_param','Excel':'readexcel_param',
                       'Json':'readjson_param','Auto Replace':'autoreplace_param',
                       'Split':'splitdata_param',
                       'Manual Replace':'manualreplace_param','Append':'append_param',
                       'Duplicate':'drop_duplicate_param','Remove Nulls':'drop_null_param',
                       'Normalize':'normalize_param','Standardize':'standardize_param','Join':'join_param','Extend Columns':'extend_col_param',
                       'Recommend':'recommend_param','Manual':'manual_param',
                       'Run Model':'runmodel_param','Predictive':'predict_param',
                       'To File':'tofile_param','loadrepo':'loadrepo_param','To Database':'todb_param',
                       'Cross Validate':'crossvalidation_param','MSE':'mse_param','Visualize':'visualize_param',
                       'Filter':'filter_param','Aggregate':'aggregate_param','Sort':'sort_param','Transpose':'transpose_param',
                       'Pivot':'pivot_param','Uid Generator':'uidgen_param' ,'Raw Script':'rawscript_param',
                       'PCA':'pca_param','LDA':'lda_param','Import Model':'importmodel_param','Export Model':'exportmodel_param',
                       'Text Preprocess':'textpreprocess_param','Image Process':'imgprocess_param',
                       'LSTM':'lstm','Super Hack':'superhack_param'}
     
#==============================================================================
# Instance based algorithms -Suresh
#==========================================================================,====
           
instance_based = {'Knn':'KNearestNeighbors','Svm':'SVM'}

instanceb_parameters = {'Knn':'knn_param','Svm':'svm_param'}

regressors = {'Linear Regression':'LinearRegression', 'Logistic Regression':'LogisticRegression',
              'TheilSen':'TheilSen','Passive Aggressive':'PassiveAggresive','Gradient Descent':'SGD',
              'Perceptron':'Perceptron','Bayesian Ridge':'Bayesianridge','OMP':'Omp'}

regressors_parameters = {'Linear Regression':'linear_param', 'Logistic Regression':'logistic_param',
                         'TheilSen':'theilsen_param','Passive Aggressive':'passagg_param','Gradient Descent':'sgd_param',
                         'Perceptron':'perceptron_param','Bayesian Ridge':'bayesridge_param','OMP':'omp_param'}

regularizer = {'Ridge':'Ridge', 'Lasso':'Lasso','Lars':'LeastAngleRegression','Elastic Net':'ElasticNet'}

regularizer_parameters = {'Ridge':'ridge_param', 'Lasso':'lasso_param','Lars':'lars_param','Elastic Net':'elastic_param'}

bayesian = {'Multinomial Naive Bayes':'MultinomialNaiveBayes','Gaussian Naive Bayes':'GaussianNaiveBayes',
            'Bernoulli Naive Bayes':'BernoulliNaiveBayes'}

bayesian_parameters = {'Multinomial Naive Bayes':'bayes_param_mlti','Gaussian Naive Bayes':'bayes_param_gaussian',
                       'Bernoulli Naive Bayes':'bnaive_param'}

ensemble = {'GradientBoosting':'GradientBoost','AdaBoost':'Adaboost','ExtraTrees':'Extratrees','DecisionTree':'Decisiontree',
            'Random Forest':'RandomForest'}

ensemble_parameters = {'GradientBoosting':'gbm_param','AdaBoost':'ada_param','ExtraTrees':'extree_param','DecisionTree':'decision_param',
                       'Random Forest':'rforest_param'}

operator_fns.update(chain(instance_based.items(), regressors.items(), regularizer.items(), 
                          bayesian.items(),ensemble.items()))
operator_parameters.update(chain(instanceb_parameters.items(),regressors_parameters.items(),
                                 regularizer_parameters.items(), bayesian_parameters.items(),ensemble_parameters.items()))



#==============================================================================
# leftcol=['linear','randomforest','gradientboost','lars',
#          'adaboost','knn','gnaive','orthogonal','elasticnets',
#          'supportvector','multinb','preceptron']
#             
# rightcol = ['logistic','ridge','decision','bayesian',
#             'stochastic','passiveaggressive','bnaive',
#             'theilsen','extratrees','kernelridge','polynomial',
#             'ardregression']
#==============================================================================
