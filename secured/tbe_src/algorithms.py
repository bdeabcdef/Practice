# -*- coding: utf-8 -*-
"""
Created on Thu Apr 28 21:46:22 2016

@author: Suresh
"""

class Algorithms():
    
    def Linreg(X,y):
        from sklearn import linear_model
        regr = linear_model.LinearRegression()
        trained = regr.fit(X,y)
        return trained
        
        
    def RandForest(X,y):
        from sklearn.ensemble import RandomForestRegressor
        forest = RandomForestRegressor()
        trained = forest.fit(X,y)
        return trained
        
     
    def GradientBoost(X,y):
        from sklearn.ensemble import GradientBoostingRegressor
        gforest = GradientBoostingRegressor()
        trained = gforest.fit(X,y)
        return trained
             
     
    def LarsLasso(X,y):
        from sklearn import linear_model 
        lars = linear_model.LassoLars(alpha=0.1, copy_X=True, fit_intercept=True,fit_path=True, max_iter=500, normalize=True,precompute='auto', verbose=False)
        trained = lars.fit(X,y)  
        return trained
        
    def AdaBoost(X,y):
        from sklearn.ensemble import AdaBoostRegressor
        adab = AdaBoostRegressor()
        trained = adab.fit(X,y)  
        return trained
        
    def knn(X,y):
        from sklearn.neighbors import KNeighborsRegressor
        k_classifier = KNeighborsRegressor(n_neighbors=5)
        trained = k_classifier.fit(X,y)
        return trained
        
    def gnaive_bayes(X,y):
        from sklearn.naive_bayes import GaussianNB
        gnaive = GaussianNB()
        trained = gnaive.fit(X,y)
        return trained
        
    def orthogonal(X,y):
        from sklearn.linear_model import OrthogonalMatchingPursuit  
        omp = OrthogonalMatchingPursuit()
        trained = omp.fit(X,y)
        return trained
        
    def elasticnet(X,y):
        from sklearn.linear_model import ElasticNet
        enet = ElasticNet(alpha=0.1)
        trained = enet.fit(X,y)
        return trained
        
    def supportvector(X,y):
        from sklearn import svm
        supvec = svm.SVR(gamma=0.0001)
        trained = supvec.fit(X,y)
        return trained
   
#additional algms   
   
    def multinaive(X,y):
        from sklearn.naive_bayes import MultinomialNB
        mnb = MultinomialNB()
        trained = mnb.fit(X,y)
        return trained

    def percept(X,y):
        from sklearn.linear_model import perceptron
        per = perceptron.Perceptron()
        trained = per.fit(X,y)
        return trained


#running right side algorithms

    def logistic(X,y):   
        from sklearn.linear_model import LogisticRegression
        logistic = LogisticRegression()
        trained = logistic.fit(X,y)
        return trained
        
    def ridge(X,y):   
        from sklearn.linear_model import Ridge
        ridg = Ridge()
        trained = ridg.fit(X,y)
        return trained
        
    def decision(X,y):   
        from sklearn.tree import DecisionTreeRegressor
        deci = DecisionTreeRegressor()
        trained = deci.fit(X,y)
        return trained
        
    def bayesian(X,y):   
        from sklearn.linear_model import BayesianRidge
        bays = BayesianRidge()
        trained = bays.fit(X,y)
        return trained
        
    def stochastic(X,y):   
        from sklearn.linear_model import SGDRegressor
        shgd = SGDRegressor(alpha=0.1)
        trained = shgd.fit(X,y)
        return trained
        
    def pasagr(X,y):   
        from sklearn.linear_model import PassiveAggressiveRegressor
        plss = PassiveAggressiveRegressor()
        trained = plss.fit(X,y)
        return trained
        
    def bnaive_bayes(X,y):
        from sklearn.naive_bayes import BernoulliNB
        bnaive = BernoulliNB()
        trained = bnaive.fit(X,y)
        return trained
        
    def theilsen(X,y):
        from sklearn.linear_model import TheilSenRegressor
        theil = TheilSenRegressor()
        trained = theil.fit(X,y)
        return trained
        
    def extratrees(X,y):   
        from sklearn.ensemble import ExtraTreesRegressor
        ext = ExtraTreesRegressor()
        trained = ext.fit(X,y)
        return trained

    def kernel(X,y):
        from sklearn.kernel_ridge import KernelRidge
        ker = KernelRidge()
        trained = ker.fit(X,y)
        return trained
   
#newly added
   
    def polyreg(X,y):
        from sklearn.preprocessing import PolynomialFeatures
        from sklearn.linear_model import LinearRegression
        from sklearn.pipeline import Pipeline
        pol = Pipeline([('poly', PolynomialFeatures(interaction_only=True)),
                  ('linear', LinearRegression(fit_intercept=False))])
        trained = pol.fit(X,y)
        return trained

    def autorel(X,y):
        from sklearn.linear_model import ARDRegression
        ard = ARDRegression()
        trained = ard.fit(X,y)
        return trained

    def bagging(X,y):
        from sklearn.ensemble import BaggingRegressor
        bagr = BaggingRegressor()
        trained = bagr.fit(X,y)
        return trained
        
    
#==============================================================================
#     def select() :
#         column=['Id','linear','randomforest','gradientboost','lars','adaboost','knn','gnaive','orthogonal','elasticnets','supportvector','multinb','preceptron','  ',
#                 'logistic','ridge','decision','bayesian','stochastic','passiveaggressive','bnaive','theilsen','extratrees','kernelridge','polynomial','ardregression','bagging']       
#         
#         plin = Linreg(X_train,y_train)
#         pred1 = plin.predict(X_test)
#         
#         prand = RandForest(X_train,y_train)
#         pred2 = prand.predict(X_test)
#         
#         pgrad = GradientBoost(X_train,y_train)
#         pred3 = pgrad.predict(X_test)
#          
#         plars = LarsLasso(X_train,y_train)
#         pred4 = plars.predict(X_test)
#           
#         pada = AdaBoost(X_train,y_train)
#         pred5 = pada.predict(X_test)
#         
#         pknn = knn(X_train,y_train)
#         pred6 = pknn.predict(X_test)
# 
#         pnaive = gnaive_bayes(X_train,y_train)
#         pred7 = pnaive.predict(X_test)
#         
#         orth = orthogonal(X_train,y_train)
#         pred8 = orth.predict(X_test)        
#         
#         pelas = elasticnet(X_train,y_train)
#         pred9 = pelas.predict(X_test)
#     
#         psvm = supportvector(X_train,y_train)
#         pred10 = psvm.predict(X_test)        
#         
#         multnb = multinaive(X_train,y_train)
#         pred23 = multnb.predict(X_test)
#         
#         perc = percept(X_train,y_train)
#         pred24 = perc.predict(X_test)
#         
#         
# #Right side algorithms
#         
#         
#         logis = logistic(X_train,y_train)
#         pred11 = logis.predict(X_test)  
#         
#         ridg = ridge(X_train,y_train)
#         pred12 = ridg.predict(X_test) 
#         
#         dec = decision(X_train,y_train)
#         pred13 = dec.predict(X_test)   
#         
#         bayesi = bayesian(X_train,y_train)
#         pred14 = bayesi.predict(X_test) 
#         
#         stocas = stochastic(X_train,y_train)
#         pred15 = stocas.predict(X_test)  
#         
#         psagr = pasagr(X_train,y_train)
#         pred16 = psagr.predict(X_test) 
#         
#         bnaiv = bnaive_bayes(X_train,y_train)
#         pred17 = bnaiv.predict(X_test) 
#         
#         thei = theilsen(X_train,y_train)
#         pred18 = thei.predict(X_test)
#         
#         extr = extratrees(X_train,y_train)
#         pred19 = extr.predict(X_test)        
#         
#         krnl = kernel(X_train,y_train)
#         pred20 = krnl.predict(X_test)   
#         
#         poly = polyreg(X_train,y_train)
#         pred33 = poly.predict(X_test)        
#         
#         ard = autorel(X_train,y_train)
#         pred34 = ard.predict(X_test)        
#         
#         bagr = bagging(X_train,y_train)
#         pred35 = bagr.predict(X_test)        
#     
#         result = pd.DataFrame({'Id':z_test,'linear':pred1,'randomforest':pred2,'gradientboost':pred3,
#                                'lars':pred4,'adaboost':pred5,'knn':pred6,'gnaive':pred7,'orthogonal':pred8,
#                                'elasticnets':pred9,'supportvector':pred10,'logistic':pred11,'ridge':pred12,
#                                'decision':pred13,'bayesian':pred14,'stochastic':pred15,'passiveaggressive':pred16,
#                                'bnaive':pred17,'theilsen':pred18,'extratrees':pred19,'kernelridge':pred20,
#                                'multinb':pred23,'preceptron':pred24,'polynomial':pred33,'ardregression':pred34,'bagging':pred35})
#         result.to_csv("predicted.csv",index=False,columns=column)
#==============================================================================
