# -*- coding: utf-8 -*-
"""Rock.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1F2l_u1TM-S10Ull6rcnOzxMLSeDRlLVE
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn import datasets
from sklearn.decomposition import PCA
from sklearn import decomposition
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

df = pd.read_csv('rock.csv', delimiter = ';')
print(df.head())
print(df.describe())

df.info()

varx = df[[ 'B', 'S', 'St', 'H', 'D', 'P', 'Q']]
y = df[['Fd']] # variable target

from sklearn.linear_model import LinearRegression # import linear regression dari sklearn
regressor = LinearRegression() # inisiasi object untuk regression dengan nama regressor
regressor.fit(varx,y)

import statsmodels.api as sm
from scipy import stats


X2 = sm.add_constant(varx)
est = sm.OLS(y, X2)
est2 = est.fit()
print(est2.summary())

from statsmodels.stats.diagnostic import het_breuschpagan
bp_test = het_breuschpagan(est2.resid, est2.model.exog)
labels = ['LM Statistic', 'LM-Test p-value', 'F-Statistic', 'F-Test p-value']
print(dict(zip(labels, bp_test)))

from sklearn.model_selection import train_test_split # Import train_test_split function
from sklearn import metrics #Import scikit-learn metrics module for accuracy calculation

# Training and testing data split
x_data = df[[ 'B', 'S', 'St', 'H', 'D', 'P', 'Q']]
y_data = df[['Fd']] # variable target


X_train, X_test, y_train, y_test = train_test_split(x_data, y_data, test_size = 0.2, random_state = 0)

print("Number of test samples : ", X_test.shape[0])
print("Number of train samples : ", X_train.shape[0])

pd.DataFrame(X_train).to_csv('train.csv')
pd.DataFrame(X_test).to_csv('test.csv')

import seaborn as sns
# melihat korelasi antar kolom
plt.figure(figsize=(8, 8))
sns.heatmap(df.corr(), cmap='Reds', annot=True, fmt='.2f')

from xgboost import XGBRegressor
from sklearn.model_selection import GridSearchCV
# feature importance
#import shap
from xgboost import plot_importance
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import mean_squared_error

# Simple model
xgbreg = XGBRegressor(random_state = 0)

# Fit the model
xgbreg.fit(X_train, y_train)

# Get predictions
predictions_xgb = xgbreg.predict(X_test)

xgb_mse = mean_squared_error(y_test, predictions_xgb)
xgb_r2 = xgbreg.score(X_test, y_test)

print("R^2 : ", xgb_r2)
print("MSE : ", xgb_mse)

# Using the mean_absolute_percentage_error function
from sklearn.metrics import mean_absolute_percentage_error
print(mean_absolute_percentage_error(y_test, predictions_xgb))

from sklearn.preprocessing import StandardScaler
from sklearn.metrics import f1_score
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import cross_val_score


# Evaluating the model
from sklearn.metrics import r2_score

# Fitting Random Forest Regression to the dataset
regressor = RandomForestRegressor(n_estimators=10, random_state=0, oob_score=True)

# Fit the regressor with x and y data
regressor.fit(X_train, y_train)

# Access the OOB Score
oob_score = regressor.oob_score_
print(f'Out-of-Bag Score: {oob_score}')

# Making predictions on the same data or new data
predictionsRFR = regressor.predict(X_test)

# Evaluating the model
mse = mean_squared_error(y_test, predictionsRFR)
print(f'Mean Squared Error: {mse}')

r2 = r2_score(y_test, predictionsRFR)
print(f'R-squared: {r2}')

from sklearn.model_selection import GridSearchCV

# Hyperparameters definition
params = {
    'n_estimators' : [100,200,400,600],
    'learning_rate' : [0.01, 0.02, 0.04, 0.06, 0.08, 1],
    'max_depth' : [3,4,5,6]
}

# Get our best model
grid = GridSearchCV(estimator=XGBRegressor(), param_grid= params, cv=3)
grid.fit(x_data, y_data)

print("Best estimator : ", grid.best_estimator_)
print("Best_score : ", grid.best_score_)
print("Best parameters : ", grid.best_params_)

grid_results = pd.DataFrame(grid.cv_results_)

# Model creation
xgbreg = grid.best_estimator_.fit(X_train, y_train)

# Model evaluation
y_hat = grid.best_estimator_.predict(X_test)

xgb_mse = mean_squared_error(y_test, y_hat)
xgb_r2 = xgbreg.score(X_test, y_test)

print("R^2 : ", xgb_r2)
print("MSE for best XGBoost model : " ,xgb_mse)

print("MAPE for best XGBoost model : " ,mean_absolute_percentage_error(y_test, y_hat))

pd.DataFrame(y_hat).to_csv('prediksi.csv')