import numpy as np 
import pandas as pd 
import seaborn as sns 
import matplotlib.pyplot as plt 
train_data = pd.read_csv("archive/Training Data.csv")
train_data.drop("Id",axis=1)
train_data.head()
train_data["Profession"]=pd.factorize(train_data.Profession)[0]
train_data["CITY"]=pd.factorize(train_data.CITY)[0]
train_data["STATE"]=pd.factorize(train_data.STATE)[0]
train_data["Married/Single"]=pd.factorize(train_data['Married/Single'])[0]
train_data["House_Ownership"]=pd.factorize(train_data.House_Ownership)[0]
train_data["Car_Ownership"]=pd.factorize(train_data.Car_Ownership)[0]
xtrain=train_data.drop("Risk_Flag",axis=1)
ytrain=train_data["Risk_Flag"]
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(xtrain, ytrain, test_size=0.3)
from sklearn.ensemble import RandomForestClassifier
RFC = RandomForestClassifier(max_features=0.6,n_estimators=100)
RFC.fit(X_train,y_train)
X_test.head()
y_pred = RFC.predict(X_test)
y_pred
from sklearn.metrics import accuracy_score,precision_score,recall_score,f1_score,confusion_matrix

accu = accuracy_score(y_test,y_pred)
presi = precision_score(y_test,y_pred)

f1 = f1_score(y_test,y_pred)
print(accu)
print("--------")
print(presi)
print("--------")
print(f1)
import seaborn as sns 

sns.heatmap(confusion_matrix(y_test,y_pred),annot=True, fmt='g', cmap="BuGn", cbar=True)