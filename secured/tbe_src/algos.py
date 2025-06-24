# -*- coding: utf-8 -*-
"""
Created on Mon Nov 14 13:46:30 2016

@author: Suresh
"""

from abc import ABCMeta, abstractproperty


class Algorithm(metaclass=ABCMeta):
    X_train = None
    y_train = None
    X_test = None
    y_test = None

    def __init__(self):
        self.xcoord = None
        self.ycoord = None
        self.uid = None
        self.inputList = []
        self.image = 'algorithm'
        self.df = None

    def run_model(self):
        fitted_model = self.model.fit(X_train, y_train)
        print('fit model',fitted_model)
        return fitted_model

    def import_algorithm(self, module, name):
            module = __import__(module, fromlist=[name])
            return getattr(module, name)

    def get_parameters(self,**kwargs):
        param_dict = {}
        for key,value in kwargs.items():
            if value != '':
                param_dict[key] = value
        return param_dict

    @abstractproperty
    def algorithm_type(self):
        pass

class SVM(Algorithm):
    def __init__(self, uid):
        self.uid = uid
        self.type = None
        
    def set_parameters(self, **kwargs):
        self.type = kwargs.pop('alg_type')
        param_dict = self.get_parameters(**kwargs)
        print('filtered param_dict')
        for k in param_dict:
            print(k,'=',param_dict[k])
        atype = 'SVR'
        if self.type == 'Classifier':
            atype = 'SVC'
        svm = self.import_algorithm('sklearn.svm',atype)
        self.model = svm(**param_dict)
        print('self.model created\n =',self.model)
        
    def algorithm_type(self):
        return self.type

        
class KNearestNeighbors(Algorithm):
    def __init__(self, uid):
        self.uid = uid
        self.type = None
        
    def set_parameters(self, **kwargs):
        self.type = kwargs.pop('alg_type')
        param_dict = self.get_parameters(**kwargs)
        if self.type == 'Classifier':
            from sklearn.neighbors import KNeighborsClassifier as knn
        else:
            from sklearn.neighbors import KNeighborsRegressor as knn
#        basedir = (getattr('from sklearn','neighbors')),__import__('KNeighbors{}'.format(self.type))
        self.model = knn(**param_dict)
        
    def algorithm_type(self):
        return self.type
        
        
class LogisticRegression(Algorithm):
    def __init__(self, uid):
        self.uid = uid

    def set_parameters(self, **kwargs):
        param_dict = self.get_parameters(**kwargs)
        print(param_dict)
        try:
            param_dict['fit_intercept'] = bool(param_dict['fit_intercept'])
            param_dict['C'] = float(param_dict['C'])
            logit = self.import_algorithm('sklearn.linear_model','LogisticRegression')
            self.model = logit(**param_dict)
        except:
            return 'Fill in appropriate values'

    def algorithm_type(self):
        return 'classifier'
        
    
class LinearRegression(Algorithm):
    def __init__(self,uid):
        self.uid = uid
        
    def set_parameters(self,**kwargs):
        param_dict = self.get_parameters(**kwargs)
        from sklearn.linear_model import LinearRegression
        self.model = LinearRegression(**param_dict)
        
    def algorithm_type(self):
        return 'Regressor'
       
       
class Ridge(Algorithm):
    def __init__(self,uid):
        self.uid = uid
        
    def set_parameters(self, **kwargs):
        param_dict = self.get_parameters(**kwargs)
        try:
            param_dict['alpha'] = float(param_dict['alpha'])
            from sklearn.linear_model import Ridge
            self.model = Ridge(**param_dict)
        except:
            return 'Float is only Supported'
                
        
    def algorithm_type(self):
        return 'Regressor'


class Lasso(Algorithm):
    def __init__(self,uid):
        self.uid = uid
        
    def set_parameters(self, **kwargs):
        param_dict = self.get_parameters(**kwargs)
        try:
            param_dict['alpha'] = float(param_dict['alpha'])
            from sklearn.linear_model import Lasso
            self.model = Lasso(**param_dict)
        except:
            return 'Float is only supported'
        
        
    def algorithm_type(self):
        return 'Regressor'
        
class LeastAngleRegression(Algorithm):
    def __init__(self, uid):
        self.uid = uid
    
    def set_parameters(self, **kwargs):
        param_dict = self.get_parameters(**kwargs)
        from sklearn.linear_model import Lars
        self.model = Lars(**param_dict)
    
    def algorithm_type(self):
        return 'Regressor'


class ElasticNet(Algorithm):
    def __init__(self, uid):
        self.uid = uid
    
    def set_parameters(self, **kwargs):
        param_dict = self.get_parameters(**kwargs)
        try:
            if 'alpha' in param_dict:
                param_dict['alpha'] = float(param_dict['alpha'])
            if 'l1_ratio' in param_dict:
                param_dict['l1_ratio'] = float(param_dict['l1_ratio'])
            from sklearn.linear_model import ElasticNet
            self.model = ElasticNet(**param_dict)
            print(self.model)
        except:
            return 'Float is only supported'
        
    def algorithm_type(self):
        return 'Regressor'

class MultinomialNaiveBayes(Algorithm):
    def __init__(self,uid):
        self.uid = uid
        
    def set_parameters(self, **kwargs):
        param_dict = self.get_parameters(**kwargs)
        try:
            if 'alhpa' in param_dict: 
                param_dict['alpha'] = float(param_dict['alpha'])
            from sklearn.naive_bayes import MultinomialNB
            self.model = MultinomialNB(**param_dict)
            print(self.model)
        except:
            return 'Float is only Supported'
    
    def algorithm_type(self):
        return 'Regressor'
    
class GaussianNaiveBayes(Algorithm):
    def __init__(self,uid):
        self.uid = uid
        
        
    def set_parameters(self, **kwargs):
        from sklearn.naive_bayes import GaussianNB
        self.model = GaussianNB()
        print(self.model)
        
    
    def algorithm_type(self):
        return 'Regressor'

class BernoulliNaiveBayes(Algorithm):
    def __init__(self,uid):
        self.uid = uid
        
    def set_parameters(self, **kwargs):
        param_dict = self.get_parameters(**kwargs)
        for k,v in param_dict.items():
            print('{0}==>{1}'.format(k,type(v)))
        try:
            if 'alpha' in param_dict: 
                param_dict['alpha'] = float(param_dict['alpha'])
        except:
            return 'alpha should be a float'
        from sklearn.naive_bayes import BernoulliNB
        self.model = BernoulliNB(**param_dict)
        print(self.model)
    
    def algorithm_type(self):
        return 'Classifier'

class TheilSen(Algorithm):
    def __init__(self,uid):
        self.uid = uid
        
    def set_parameters(self, **kwargs):
        param_dict = self.get_parameters(**kwargs)
        try:
            param_dict['max_subpopulation'] = float(param_dict['max_subpopulation'])
            param_dict['tol'] = float(param_dict['tol'])
            param_dict['max_iter'] = int(param_dict['max_iter'])
            param_dict['fit_intercept'] = bool(param_dict['fit_intercept'])
            theil = self.import_algorithm('sklearn.linear_model','TheilSenRegressor')
            self.model = theil(**param_dict)
        except:
            return 'Fill in appropriate values'
        
        
    def algorithm_type(self):
        return 'Regressor'

class PassiveAggresive(Algorithm):
    def __init__(self, uid):
        self.uid = uid
        self.type = None
        
    def set_parameters(self, **kwargs):
        self.type = kwargs.pop('alg_type')
        param_dict = self.get_parameters(**kwargs)
        print(param_dict)
        try:
            param_dict['C'] = float(param_dict['C'])
            param_dict['n_iter'] = int(param_dict['n_iter'])
            if self.type == 'Classifier':
                param_dict['fit_intercept'] = bool(param_dict['fit_intercept'])
                pagg = self.import_algorithm('sklearn.linear_model','PassiveAggressive{}'.format(self.type))
                self.model = pagg(**param_dict)
            elif self.type == 'Regressor':
                param_dict['epsilon'] = float(param_dict['epsilon'])
                pagg = self.import_algorithm('sklearn.linear_model','PassiveAggressive{}'.format(self.type))
                self.model = pagg(**param_dict)
        except:
            return 'Fill in appropriate values'

    def algorithm_type(self):
        return self.type

class GradientBoost(Algorithm):
    def __init__(self, uid):
        self.uid = uid
        self.type = None
        
    def set_parameters(self, **kwargs):
        self.type = kwargs.pop('alg_type')
        param_dict = self.get_parameters(**kwargs)
        print(param_dict)
        try:
            param_dict['learning_rate'] = float(param_dict['learning_rate'])
            param_dict['n_estimators'] = int(param_dict['n_estimators'])
            param_dict['max_depth'] = int(param_dict['max_depth'])
            param_dict['min_samples_split'] = int(param_dict['min_samples_split'])
            param_dict['min_samples_leaf'] = int(param_dict['min_samples_leaf'])
            if self.type == 'Classifier':
                gbm = self.import_algorithm('sklearn.ensemble','GradientBoosting{}'.format(self.type))
                self.model = gbm(**param_dict)
            elif self.type == 'Regressor':
                gbm = self.import_algorithm('sklearn.ensemble','GradientBoosting{}'.format(self.type))
                self.model = gbm(**param_dict)
        except:
            return 'Fill in appropriate values'

    def algorithm_type(self):
        return self.type


class Adaboost(Algorithm):
    def __init__(self, uid):
        self.uid = uid
        self.type = None
        
    def set_parameters(self, **kwargs):
        self.type = kwargs.pop('alg_type')
        param_dict = self.get_parameters(**kwargs)
        print(param_dict)
        try:
            param_dict['learning_rate'] = float(param_dict['learning_rate'])
            param_dict['n_estimators'] = int(param_dict['n_estimators'])
            if self.type == 'Classifier':
                ada = self.import_algorithm('sklearn.ensemble','AdaBoost{}'.format(self.type))
                self.model = ada(**param_dict)
            elif self.type == 'Regressor':
                ada = self.import_algorithm('sklearn.ensemble','AdaBoost{}'.format(self.type))
                self.model = ada(**param_dict)
        except:
            return 'Fill in appropriate values'

    def algorithm_type(self):
        return self.type


class Extratrees(Algorithm):
    def __init__(self, uid):
        self.uid = uid
        self.type = None
        
    def set_parameters(self, **kwargs):
        self.type = kwargs.pop('alg_type')
        param_dict = self.get_parameters(**kwargs)
        print(param_dict)
        try:
            param_dict['n_estimators'] = int(param_dict['n_estimators'])
            param_dict['max_depth'] = int(param_dict['max_depth'])
            param_dict['min_samples_split'] = int(param_dict['min_samples_split'])
            param_dict['min_samples_leaf'] = int(param_dict['min_samples_leaf'])
            if self.type == 'Classifier':
                ext = self.import_algorithm('sklearn.ensemble','ExtraTrees{}'.format(self.type))
                self.model = ext(**param_dict)
            elif self.type == 'Regressor':
                ext = self.import_algorithm('sklearn.ensemble','ExtraTrees{}'.format(self.type))
                self.model = ext(**param_dict)
        except:
            return 'Fill in appropriate values'

    def algorithm_type(self):
        return self.type


class Decisiontree(Algorithm):
    def __init__(self, uid):
        self.uid = uid
        self.type = None
        
    def set_parameters(self, **kwargs):
        self.type = kwargs.pop('alg_type')
        param_dict = self.get_parameters(**kwargs)
        print(param_dict)
        try:
#            param_dict['n_estimators'] = int(param_dict['n_estimators'])
            param_dict['max_depth'] = int(param_dict['max_depth'])
            param_dict['min_samples_split'] = int(param_dict['min_samples_split'])
            param_dict['min_samples_leaf'] = int(param_dict['min_samples_leaf'])
            if self.type == 'Classifier':
                dec = self.import_algorithm('sklearn.tree','DecisionTree{}'.format(self.type))
                self.model = dec(**param_dict)
            elif self.type == 'Regressor':
                dec = self.import_algorithm('sklearn.tree','DecisionTree{}'.format(self.type))
                self.model = dec(**param_dict)
        except Exception as e:
            print(str(e))
            return 'Fill in appropriate values'

    def algorithm_type(self):
        return self.type

class RandomForest(Algorithm):
    def __init__(self, uid):
        self.uid = uid
        self.type = None
        
    def set_parameters(self, **kwargs):
        self.type = kwargs.pop('alg_type')
        param_dict = self.get_parameters(**kwargs)
        for k in param_dict:
            try:
                param_dict[k] = int(param_dict[k])
            except:
                return '{} should be an integer'.format(k)
        rf = self.import_algorithm('sklearn.ensemble','RandomForest{}'.format(self.type))
        self.model = rf(**param_dict)
        
    def algorithm_type(self):
        return self.type

class SGD(Algorithm):
    def __init__(self, uid):
        self.uid = uid
        self.type = None
        
    def set_parameters(self, **kwargs):
        self.type = kwargs.pop('alg_type')
        param_dict = self.get_parameters(**kwargs)
        if 'alpha' in param_dict:
            try:
                param_dict['alpha'] = float(param_dict['alpha'])
            except:
                return 'alpha should be a float'
        if 'n_iter' in param_dict:
            try:
                param_dict['n_iter'] = int(param_dict['n_iter'])
            except:
                return 'N iterations should be an integer'
        sgd = self.import_algorithm('sklearn.linear_model','SGD{}'.format(self.type))
        self.model = sgd(**param_dict)
        
    def algorithm_type(self):
        return self.type


class Perceptron(Algorithm):
    def __init__(self, uid):
        self.uid = uid
        self.type = None
        
    def set_parameters(self, **kwargs):
        param_dict = self.get_parameters(**kwargs)
        if 'alpha' in param_dict:
            try:
                param_dict['alpha'] = float(param_dict['alpha'])
            except:
                return 'alpha should be a float'
        if 'n_iter' in param_dict:
            try:
                param_dict['n_iter'] = int(param_dict['n_iter'])
            except:
                return 'N iterations should be an integer'
        percep = self.import_algorithm('sklearn.linear_model','Perceptron')
        self.model = percep(**param_dict)
        
    def algorithm_type(self):
        return self.type

       
class Bayesianridge(Algorithm):
    def __init__(self, uid):
        self.uid = uid
        self.type = None
        
    def set_parameters(self, **kwargs):
        param_dict = self.get_parameters(**kwargs)
        if 'tol' in param_dict:
            try:
                param_dict['tol'] = float(param_dict['tol'])
            except:
                return 'tol should be a float'
        if 'n_iter' in param_dict:
            try:
                param_dict['n_iter'] = int(param_dict['n_iter'])
            except:
                return 'N iterations should be an integer'
        bayrid = self.import_algorithm('sklearn.linear_model','BayesianRidge')
        self.model = bayrid(**param_dict)
        
    def algorithm_type(self):
        return self.type

class Omp(Algorithm):
    def __init__(self, uid):
        self.uid = uid
        self.type = None
        
    def set_parameters(self, **kwargs):
        param_dict = self.get_parameters(**kwargs)
        if 'tol' in param_dict:
            try:
                param_dict['tol'] = float(param_dict['tol'])
            except:
                return 'tol should be a float'
        if 'n_nonzero_coeffs' in param_dict:
            try:
                param_dict['n_nonzero_coefs'] = int(param_dict['n_iter'])
            except:
                return 'n_nonzero should be an integer'
        omp = self.import_algorithm('sklearn.linear_model','OrthogonalMatchingPursuit')
        self.model = omp(**param_dict)
        
    def algorithm_type(self):
        return self.type
