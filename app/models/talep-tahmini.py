# model.py
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.linear_model import LinearRegression
import joblib

# Veri setini oku
data = pd.read_csv('datasets/retail_store_inventory.csv')

# String verileri sayısal yap
le = LabelEncoder()
data['Store ID'] = le.fit_transform(data['Store ID'])
data['Product ID'] = le.fit_transform(data['Product ID'])
data['Category'] = le.fit_transform(data['Category'])
data['Region'] = le.fit_transform(data['Region'])
data['Weather Condition'] = le.fit_transform(data['Weather Condition'])
data['Seasonality'] = le.fit_transform(data['Seasonality'])

# Kullanılmayacak kolonları kaldır
data.drop(columns=['Date'], axis=1, inplace=True)

# Bağımsız ve bağımlı değişkenler
X = data.drop('Demand Forecast', axis=1)
y = data['Demand Forecast']

# Eğitim-test ayır
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Ölçeklendir
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)

# Modeli eğit
model = LinearRegression()
model.fit(X_train, y_train)

# Modeli ve scaler'ı kaydet
joblib.dump(model, 'retail_store_inventory_model.pkl')
joblib.dump(scaler, 'retail_store_inventory_scaler.pkl')
