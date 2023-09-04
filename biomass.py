import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.linear_model import LinearRegression
import pandas as pd
import joblib

path = r'D:\jsonbiaozhun\LAD_LG_field_gcj02.CSV'
data = pd.read_csv(path,sep=',',header='infer',usecols=[5])

X = data.drop[['株高', 'LAI', 'swg']]
y = data['biomass']
# 划分数据集为训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


# RF分类模型
# 初始化随机森林回归模型
rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)
y_pred = rf_model.predict(X_test)
print(f"Estimated Biomass RF: {y_pred}")
joblib.dump( rf_model, 'mlr_model.pkl') 


model1 = LinearRegression()
model1.fit(X_train, y_train)
y_pred = model1.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
print(f"Mean Squared Error: {mse}")

mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
print("均方误差 (MSE):", mse)
print("R平方 (R2):", r2)

new_data = pd.DataFrame({'株高': [0], 'LAI': [1], 'swg': [2]})  
estimated_biomass = model1.predict(new_data)
print(f"Estimated Biomass MLR: {estimated_biomass}")
joblib.dump( model1, 'mlr_model.pkl') 