import streamlit as st
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split 
from sklearn.linear_model import LinearRegression
st.set_page_config("Prediction_Board",layout='wide')
st.header("Prediction DashBoard")
df = pd.read_csv("Streamlit_Prediction.csv")
df = df.drop(columns=['Data Analyst intern','Software Engineer intern','Data Scientist intern','Data Engineer intern'],axis=1)
x = df.iloc[:,1:]
y = df['Salary']
x_train,x_test,y_train,y_test = train_test_split(x,y,random_state=42,test_size=0.3)
model = LinearRegression()
model.fit(x_train,y_train)
y_pred = model.predict(x_test)
st.subheader("Predict your Salary")
technical_skill_options = list(x_train.loc[:,'Python(ProgrammingLanguage)':'DataVisualization'].columns)
non_tech_skill_options = ['ProblemSolving','Communication']
technical_skill_options = [x for x in technical_skill_options if x not in non_tech_skill_options]
job_options = x_train.loc[:,'Data Analyst':'Software Engineer'].columns
working_type_options = ['Remote','Hybrid','On-site']
location_options = x.loc[:,' Arlington':].columns
job = st.selectbox(label='Pick a Job',options=job_options)
technical_skills = st.multiselect(label='Pick technical skills',options=technical_skill_options,default=['AnalyticalSkills'])
Non_tech_skills = st.multiselect(label='Pick non-tech skills',options=non_tech_skill_options,default=['ProblemSolving'])
working_type = st.selectbox(label='Pick a working type',options=working_type_options)
location = st.selectbox(label='Pick a location',options=location_options)
dummies_collection = []
for col in x.columns:
    if col in job or col in technical_skills or col in working_type or col in location or col in Non_tech_skills:
        dummies_collection.append(1)
    else:
        dummies_collection.append(0)
        
dummies_collection = np.array(dummies_collection).reshape(1,-1)
col1,col2,col3 = st.columns([1.25,1,1])
with col2:
    salary = '{:,.0f}'.format(round(model.predict(dummies_collection)[0]))
    st.subheader(f"Predicted Salary: $ {salary}")
            
    
    
