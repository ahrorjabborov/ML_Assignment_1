# -*- coding: utf-8 -*-
"""ML-Assignment-1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1jlo9Aw88LeBEO0WbGk-UtvizMJy-oZCT

**IMPORTING LIBRARIES**
"""

import pandas as pd
import numpy as np
import sklearn as skl
import matplotlib.pyplot as plt

"""**DATASET READING**"""

df = pd.read_csv('./flight_delay.csv')

df.shape

"""**DATA EXPLORATION**"""

df

types = df.dtypes
print("Number categorical featues:", sum(types=='object'))
print(types)

"""**DATA PREPROCESSING**"""

from sklearn import preprocessing
import datetime

def count_nans(df):
    return pd.isna(df).sum().sum()

print(count_nans(df))

duration = pd.to_datetime(df['Scheduled arrival time']) - pd.to_datetime(df['Scheduled depature time'])

df['Duration'] = duration.dt.seconds / 60

df.head(5)

import seaborn as sns
sns.boxplot(x = df['Duration'])

from scipy import stats
z = np.abs(stats.zscore(df.loc[:, ['Duration']]))
threshold = 3
df.drop(df.index[np.where(z > threshold)[0]], inplace=True)

df

df_train = df[pd.to_datetime(df['Scheduled depature time']).apply(lambda x:x.date()) < datetime.date(2018, 1, 1)]
df_test  = df[pd.to_datetime(df['Scheduled depature time']).apply(lambda x:x.date()) > datetime.date(2017, 12, 31)]

x_train = df_train.drop('Delay', axis = 1)
x_test = df_test.drop('Delay', axis = 1)

y_train = df_train['Delay']
y_test = df_test['Delay']

type(x_train)

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import PolynomialFeatures 
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import cross_val_score

x = x_train['Duration'].values
y = y_train.values



plt.scatter(x,y,label="Samples")
plt.title('DELAY VS DURATION')
plt.xlabel('Duration')
plt.ylabel('Delay')
plt.legend(loc="best")
plt.show()


x = x[:, np.newaxis]
y = y[:, np.newaxis]

X = x_test['Duration'].values
X = X[:, np.newaxis]

Y = y_test.values
Y = Y[:, np.newaxis]

"""LINEAR REGRESSION"""

from sklearn.linear_model import LinearRegression
model = LinearRegression()



model.fit(x, y)

y_pred = model.predict(x)

plt.scatter(x, y, label="Samples")
plt.title('DELAY VS DURATION')
plt.xlabel('Duration')
plt.ylabel('Delay')
plt.legend(loc="best")
plt.plot(x, y_pred, color='r')
plt.show()

model.intercept_

y[:8000, 0].shape, y_pred.shape

pd.DataFrame({'Actual': y[:8000, 0], 'Predicted': y_pred}, index=[x for x in range(len(y_pred))])

r2_score(y[:8000, 0], y_pred)

"""POLYNOMIAL REGRESSION"""

from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import PolynomialFeatures
import operator



from sklearn.preprocessing import PolynomialFeatures

def create_polynomial_regression_model(degree):
  "Creates a polynomial regression model for the given degree"
  
  poly_features = PolynomialFeatures(degree=degree)
  

  X_train_poly = poly_features.fit_transform(x)
  

  poly_model = LinearRegression()
  poly_model.fit(X_train_poly, y)
  

  y_train_predicted = poly_model.predict(X_train_poly)
  

  y_test_predict = poly_model.predict(poly_features.fit_transform(X))
  

  rmse_train = np.sqrt(mean_squared_error(y, y_train_predicted))
  r2_train = r2_score(y, y_train_predicted)

  rmse_test = np.sqrt(mean_squared_error(Y, y_test_predict))
  r2_test = r2_score(Y, y_test_predict)
  
  print("The model performance for the training set")
  print("-------------------------------------------")
  print("RMSE of training set is {}".format(rmse_train))
  print("R2 score of training set is {}".format(r2_train))
  
  print("\n")
  
  print("The model performance for the test set")
  print("-------------------------------------------")
  print("RMSE of test set is {}".format(rmse_test))
  print("R2 score of test set is {}".format(r2_test))


create_polynomial_regression_model(degree=10)

x[:1000].shape

poly = PolynomialFeatures(degree=10, include_bias=True)
x_train_trans = poly.fit_transform(x[:8000])
x_test_trans = poly.transform(X)
#include bias parameter
lr = LinearRegression()
lr.fit(x_train_trans, y[:8000])

X_plotter = np.arange(0, 800, 0.1)
print(lr.intercept_, lr.coef_)
y_pred = lr.intercept_ + lr.coef_[0][1]*X_plotter + lr.coef_[0][2]*np.power(X_plotter, 2) + lr.coef_[0][3]*np.power(X_plotter, 3) + lr.coef_[0][4]*np.power(X_plotter, 4)
print(r2_score(Y[:8000], y_pred))

X_new_poly = poly.transform(x)
plt.plot(x, y, "b.",label='Training points')
plt.plot(X, Y, "g.",label='Testing points')
plt.plot(X_plotter, y_pred[:8000], '-r')
plt.xlabel("X")
plt.ylabel("y")
plt.legend()
plt.show()

from sklearn import linear_model
lasso_reg = linear_model.Lasso(alpha=50, max_iter=100, tol=0.1)
lp = lasso_reg.fit(x_train_trans, y[:8000])
lasso_reg.score(x_train_trans, y[:8000])

print(lp.intercept_, lp.coef_)
y_pred = lp.intercept_ + lp.coef_[1]*X_plotter + lp.coef_[2]*np.power(X_plotter, 2) + lp.coef_[3]*np.power(X_plotter, 3) + lp.coef_[4]*np.power(X_plotter, 4)
print(r2_score(Y[:8000], y_pred))

X_new_poly = poly.transform(x)
plt.plot(x, y, "b.",label='Training points')
plt.plot(X, Y, "g.",label='Testing points')
plt.plot(X_plotter, y_pred[:8000], '-r')
plt.xlabel("X")
plt.ylabel("y")
plt.legend()
plt.show()

