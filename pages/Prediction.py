import streamlit as st
import pandas as pd
import numpy as np
from mlxtend.feature_selection import SequentialFeatureSelector
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split 
import statsmodels.api as sm
st.set_page_config("Prediction_Board",layout='wide')
st.header("Prediction DashBoard")
df = pd.read_csv("C:\AProgramming\Python\Linkedin\Streamlit_Linkedin\Streamlit_Prediction.csv")
df = df.drop(columns=['Data Analyst intern','Software Engineer intern','Data Scientist intern','Data Engineer intern'],axis=1)
x = df.iloc[:,1:]
y = df['Salary']
x_train,x_test,y_train,y_test = train_test_split(x,y,random_state=42,test_size=0.3)
model = LinearRegression()
model.fit(x_train,y_train)
y_pred = model.predict(x_test)
st.subheader("Predict your Salary")
skill_options = x_train.loc[:,'Python(ProgrammingLanguage)':'DataVisualization'].columns
job_options = x_train.loc[:,'Data Analyst':'Software Engineer'].columns
working_type_options = ['Remote','Hybrid','On-site']
location_options = x.loc[:,' Arlington':].columns
job = st.selectbox(label='Pick a Job',options=job_options)
skills = st.multiselect(label='Pick skills',options=skill_options,default=['AnalyticalSkills'])
working_type = st.selectbox(label='Pick a working type',options=working_type_options)
location = st.selectbox(label='Pick a location',options=location_options)
dummies_collection = []
for col in x.columns:
    if col in job or col in skills or col in working_type or col in location:
        dummies_collection.append(1)
    else:
        dummies_collection.append(0)
        
dummies_collection = np.array(dummies_collection).reshape(1,-1)
col1,col2,col3 = st.columns([1.25,1,1])
with col2:
    st.subheader(f"Predicted Salary: ${round(model.predict(dummies_collection)[0])}")
            
    
    