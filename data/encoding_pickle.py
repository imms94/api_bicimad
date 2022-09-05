from sklearn import preprocessing
import pandas as pd
import numpy as np
from math import pi, sin, cos

from sklearn.preprocessing import StandardScaler, OneHotEncoder
import pickle


def fit_Standard(df):
    #Transform the data
    temp = df
    f_transformer = StandardScaler()
    fitter = f_transformer.fit(temp[['activate', 'reservations_count', 'light', 'total_bases', 'free_bases', 'longitude', 'no_available', 'latitude', 'time','feels_like', 'weekday', 'year', 'month', 'hour_sin', 'hour_cos','weekday_sin', 'weekday_cos', 'month_sin', 'month_cos']])
    temp.holidays = temp.holidays.astype('int')
    with open("fit_standard.pkl", "wb") as file:
        pickle.dump(fitter, file)



def fit_OHE(df):
    temp = df
    temp.holidays = temp.holidays.astype('int')
    ohe = OneHotEncoder(sparse=False, handle_unknown='ignore')
    categorical_features = ['year','weather_main']
    transformed_data = ohe.fit(temp[categorical_features])
    with open("fit_OHE.pkl", "wb") as file:
        pickle.dump(transformed_data, file)






def transform_standard(df):
    #Encode the data
    temp_model = df
    f_transformer = pickle.load(open("fit_standard.pkl","rb"))

    temp_model[['activate', 'reservations_count', 'light', 'total_bases', 'free_bases', 'longitude', 'no_available', 'latitude', 'time',
       'feels_like', 'weekday', 'year', 'month', 'hour_sin', 'hour_cos',
        'weekday_sin', 'weekday_cos', 'month_sin', 'month_cos']] = f_transformer.transform(temp_model[['activate', 'reservations_count', 'light', 'total_bases', 'free_bases', 'longitude', 'no_available', 'latitude', 'time',
       'feels_like', 'weekday', 'year', 'month', 'hour_sin', 'hour_cos',
        'weekday_sin', 'weekday_cos', 'month_sin', 'month_cos']])



    return temp_model



def transform_OHE(df):
    temp_model = df
    ohe = pickle.load(open("fit_OHE.pkl","rb"))
    categorical_features = ['year', 'weather_main']

    transformed_data = pd.DataFrame(ohe.transform(df[categorical_features]))
    transformed_data.columns = ohe.get_feature_names(categorical_features)


   # transformed_data.columns = ohe.get_feature_names(categorical_features)
    return transformed_data

def concatenate(df1,df2):
    concatenated_data = pd.concat([df1, df2], axis=1)
    temp_model = concatenated_data.drop(columns=['year', 'month', 'weekday', 'weather_main','date'])
    temp_model['datetime'] = temp_model['datetime'].apply(lambda x: x[0:10]+' '+x[10:]+':00')
    temp_model['datetime']=pd.to_datetime(temp_model['datetime'], format='%Y-%m-%d %H:%M:%S')
    temp_model = temp_model.set_index('datetime')
    temp_model.sort_values(by='datetime')
    temp_model = temp_model.drop(columns=['name', 'number', 'address', 'id'])

    return temp_model
