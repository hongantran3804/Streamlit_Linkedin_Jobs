import streamlit as st
import pandas as pd
import plotly.express as px
st.set_page_config("Home Page",layout="wide")
st.header("Linkedin Scraping Jobs")
tab1, tab2, tab3, tab4, tab5 = st.tabs(['General Information','Import Data','Data Exploration','Visualization','Data Cleaning & Feature Engineering'])
with tab1:
    st.markdown(f"""
                <div>
             <h3><strong>Define Project: </strong></h3>
    
In this dynamic project, I harnessed the power of machine learning to revolutionize the way we understand and predict salaries based on LinkedIn job titles. Leveraging advanced algorithms, I developed a robust model capable of analyzing various factors that influence salary outcomes, providing valuable insights for both job seekers and employers.
<br><br>
<h3><strong>Key Features: </strong></h3>
- Data-driven Insights: I curated a comprehensive dataset from LinkedIn, incorporating diverse job titles and corresponding salary information. This data served as the foundation for training the machine learning model.
<br>
- Predictive Modeling: Through the implementation of cutting-edge machine learning techniques, I created a predictive model capable of forecasting salary ranges for specific job titles. This enables users to make informed decisions regarding salary expectations.
<br>
- User-Friendly Interface: The project includes an intuitive interface that allows users to input a job title and receive an accurate salary prediction. This user-friendly design enhances accessibility and encourages widespread utilization.
<br>
- Continuous Learning: To ensure the model's accuracy and relevance, I implemented a feedback loop for continuous learning. This enables the model to adapt to changing job market dynamics and evolving salary trends.              
</div>""",unsafe_allow_html=True)


with tab2:
    st.subheader("Import dataset")
    df = pd.read_csv("C:\AProgramming\Python\Linkedin\Fixed_Linkedin.csv")
    st.info(f"Rows, Columns: {df.shape}")
    st.dataframe(df)
with tab3:
    col1,col2 = st.columns([2,1])
    with col1:
        df = pd.read_csv("C:\AProgramming\Python\Linkedin\Fixed_Linkedin.csv")
        error_values = pd.DataFrame({'No unique values': df.nunique(),
                            'Missing Value': df.isna().sum(),
                            'Duplicated': df.duplicated().sum(),
                            'Dtype': df.dtypes})
        st.dataframe(error_values, width=1500)
    with col2:
        st.markdown(f"""
                    <div>
                  <h5> Analysis:</h5>

- The dataset appears to have information related to job postings or employment opportunities.

- Salary column has a significant number of unique values, indicating diversity in salary information.

- Columns like Job_Title, Company_Name, Skills, Industry, and Location have a considerable number of unique values, suggesting diversity in job titles, companies, required skills, industries, and job locations.

- Employee column has 16 unique values, possibly indicating different employee types or categories.

- Some columns have missing values, such as Job_Title, Employee, and Industry. The handling of missing data may be necessary depending on the analysis goals.
</div>""",unsafe_allow_html=True)
        
with tab4:
    tmp_df = pd.read_csv("C:\AProgramming\Python\Linkedin\Streamlit_Linkedin\Streamlit_Linkedin_Jobs.csv")
    fil_Location = tmp_df['Location'].value_counts().reset_index()
    get_location = fil_Location[fil_Location['count'] >= 10]['Location']
    job_title_df = tmp_df['Job_Title'].value_counts().reset_index()
    get_title = job_title_df[job_title_df['count'] >= 10]['Job_Title']
    choice = st.multiselect(label="Select options",options=["Illustrating the relationships among location, job title, working type, number of employees, and salary.",
                                                "Illustrating the relationships among location, job title, working type, number of employees, and mean salary.",
                                                "Displaying the frequency of companies requiring a top skill.",
                                                "Illustrating the distribution of job postings based on the time of scraping job information."],
        default="Illustrating the relationships among location, job title, working type, number of employees, and salary.")
    
    if "Illustrating the relationships among location, job title, working type, number of employees, and salary." in choice:
        st.subheader("Illustrating the relationships among location, job title, working type, number of employees, and salary.")
        column1, column2 = st.columns([2.5,1])
        with column1:
            col1,col2 = st.columns([1,1])
            with col1:
                location_df = tmp_df[tmp_df['Location'].isin(get_location)][['Location','Salary']]
                location_df = location_df.drop_duplicates(subset="Location",keep='first')
                location = st.multiselect(label="Select location",options=location_df['Location'].unique(),default=[" New York"," San Francisco"," Los Angeles"])
                location_df = tmp_df[tmp_df['Location'].isin(location)][['Location','Salary']]
                location_plotly = px.box(location_df,x = 'Location',y = 'Salary',color = 'Location')
                st.plotly_chart(location_plotly,use_container_width=True)
            with col2:
                selection = st.selectbox(label="Select option",options=['Job_Title','Working_Type','Number_of_Employees'])
                if selection == 'Job_Title':
                    get_title_df = tmp_df[tmp_df['Job_Title'].isin(get_title)][["Job_Title","Salary"]]
                    title = st.multiselect(label="Select Job Title",options=get_title_df['Job_Title'].unique(),default=["Data Scientist","Software Engineer","Data Engineer"])
                    get_title_df = get_title_df[get_title_df['Job_Title'].isin(title)]
                    title_plot = px.box(get_title_df,x = "Job_Title",y="Salary",color="Job_Title")
                    st.plotly_chart(title_plot,use_container_width=True)
                elif selection == 'Working_Type':
                    type_df = tmp_df[["Working_Type","Salary"]]
                    type = st.multiselect(label="Select Working Type",options = type_df["Working_Type"].unique(),default=["Remote","Hybrid","On-site"])
                    type_df = type_df[type_df['Working_Type'].isin(type)]
                    type_plot = px.box(type_df,x = "Working_Type"
                                        ,y = "Salary",color = "Working_Type")
                    st.plotly_chart(type_plot,use_container_width=True)
                elif selection == 'Number_of_Employees':
                    employee = st.multiselect(label="Select Number of Employees",options=tmp_df[["Employee","Salary"]]["Employee"].unique(),default=list(tmp_df[["Employee","Salary"]].loc[0:2,"Employee"]))
                    employee_df = tmp_df[["Employee","Salary"]]
                    employee_df = employee_df[employee_df['Employee'].isin(employee)][["Employee","Salary"]]
                    employee_plot = px.box(employee_df,x = "Employee",y = "Salary",color="Employee")
                    st.plotly_chart(employee_plot,use_container_width=True)
        with column2:
            st.markdown(f"""
                        <br><br>
                        <div>
                       <h5> Analysis for relation between salary and job title, location, working type, working status </h5>
- The salary range and average salaries vary for each role, with Software Engineers generally having a higher average salary compared to Data Scientists and Data Engineers.

- Remote work options are prevalent across all roles, indicating a growing trend in the tech industry toward flexible work arrangements.

- The location of job opportunities spans major tech hubs such as San Francisco, New York, and Seattle, as well as other cities.

- Company size doesn't seem to be a limiting factor, as positions are available in startups as well as large enterprises.
                        </div>
                        """,unsafe_allow_html=True)
        
        st.markdown("#")
    if "Illustrating the relationships among location, job title, working type, number of employees, and mean salary." in choice:
        st.subheader("Illustrating the relationships among location, job title, working type, number of employees, and mean salary.")
        location_df = tmp_df.groupby('Location').agg({'Salary':'mean'}).reset_index()
        location_df = location_df.rename(columns = {'Salary':'Mean_Salary'})
        location_df = location_df[location_df['Location'].isin(get_location)]
        salary_range = st.slider("Select a range",min(location_df['Mean_Salary']),max(location_df['Mean_Salary']),(min(location_df['Mean_Salary']),max(location_df['Mean_Salary'])))
        location_df = location_df[location_df['Mean_Salary'].between(left=salary_range[0],right=salary_range[1])][["Location","Mean_Salary"]]
        location_plot = px.bar( location_df,x = "Location",y = 'Mean_Salary',color='Mean_Salary')
        st.plotly_chart(location_plot,use_container_width=True)
        col4,col5,col6 = st.columns(3)
        with col4:
            title_df = tmp_df.groupby('Job_Title').agg({"Salary":'mean'}).reset_index()
            title_df = title_df.rename(columns = {"Salary":"Mean_Salary"})
            select = st.multiselect(label="Select options",options = title_df["Job_Title"].unique(),default=["Data Scientist","Software Engineer","Data Engineer"])
            title_df = title_df[title_df['Job_Title'].isin(select)]
            title_plot = px.bar(title_df,x = "Job_Title",y = 'Mean_Salary',color='Mean_Salary')
            st.plotly_chart(title_plot,use_container_width=True)
        with col5:
            type_df = tmp_df.groupby("Working_Type").agg({"Salary":"mean"}).reset_index()
            type_df = type_df.rename(columns = {"Salary":"Mean_Salary"})
            select =st.multiselect(label="Select options",options = type_df['Working_Type'].unique(),default=['Hybrid'])
            type_df = type_df[type_df['Working_Type'].isin(select)]
            type_plot = px.bar(type_df,x = 'Working_Type',y="Mean_Salary",color = "Mean_Salary")
            st.plotly_chart(type_plot,use_container_width=True)
        with col6:
            
            employee_df = tmp_df.groupby('Employee').agg({"Salary":"mean"}).reset_index()
            employee_df = employee_df.rename(columns = {"Salary":"Mean_Salary"})
            salary_range = st.slider("Select a range",min(employee_df['Mean_Salary']),max(employee_df['Mean_Salary']),(min(employee_df['Mean_Salary']),max(employee_df['Mean_Salary'])))
            employee_df = employee_df[employee_df['Mean_Salary'].between(left = salary_range[0],right = salary_range[1])]
            employee_plot = px.bar(employee_df,x = "Employee",y = "Mean_Salary",color="Mean_Salary")
            st.plotly_chart(employee_plot,use_container_width=True)
        st.markdown("#")
    if "Displaying the frequency of companies requiring a top skill." in choice:
        st.subheader("Displaying the frequency of companies requiring a top skill.")
        col1,col2 = st.columns([2,1])
        with col1:
            
            skills_df = tmp_df.loc[:,'Python(ProgrammingLanguage)':]
            skills_df = skills_df.drop('P',axis=1)
            for col in skills_df.columns:
                if "Unname" in col:
                    skills_df.drop(columns=col,axis=1,inplace = True)
            counts = []
            skills = []
            for skill in skills_df.columns:
                if skills_df[skill].sum() > 200 and skill != "":
                    counts.append(skills_df[skill].sum())
                    skills.append(skill)
            new_skills_df = pd.DataFrame({
                'Skills' : skills,
                'Number_of_Companies':counts,
            }
            )
            skill_range = st.slider("Select a range",min(counts),max(counts),(min(counts),max(counts)))
            new_skills_df = new_skills_df[new_skills_df['Number_of_Companies'].between(left=skill_range[0],right=skill_range[1])]
            skill_plot = px.bar(new_skills_df,x = 'Skills',y = 'Number_of_Companies',color="Skills")
            st.plotly_chart(skill_plot,user_container_width=True)
        with col2:
            st.markdown(f"""
                        <br><br><br>
                        <div>
                       <h5>Analysis for Skills requirements: </h5>

- Programming Skills are Essential: Programming (568 mentions) and specific languages like Python and Java are highly sought after.

- Data Science and Analytics: Skills related to data, such as Data Science, Data Analytics, and Data Analysis, are crucial in many positions.

- Analytical and Problem-Solving Skills: Analytical Skills and Problem Solving are highlighted, indicating the importance of critical thinking.

- Communication Skills: Communication is emphasized, suggesting that effective communication is valued in these roles.

- Computer Science and Software Development: These skills are mentioned in a significant number of job postings, highlighting the demand for technical expertise.
                        </div>""",unsafe_allow_html=True)
        st.markdown("#")
    if "Illustrating the distribution of job postings based on the time of scraping job information." in choice:
        st.subheader("Illustrating the distribution of job postings based on the time of scraping job information.")
        col1, col2 = st.columns(2)
        with col1:
            date_and_job = tmp_df.groupby('Date').size().to_frame('Number_of_Jobs').reset_index()
            plot = px.line(date_and_job,x='Date',y='Number_of_Jobs')
            st.plotly_chart(plot,use_container_width=True)
        with col2:
            st.markdown(f"""
                        <br><br>
                        <div>
                        <h5>Analysis for Job postings: </h5>

- Fluctuations in Job Postings: The data shows fluctuations in the number of job postings over the given period. Some days see only a few job postings, while others show higher activity.

- Increasing Trend Over Time: There appears to be a general increasing trend in the number of job postings as time progresses. This suggests a potential growth in job opportunities during the observed period.

- Periods of Stability: Despite fluctuations, there are periods where the number of job postings remains relatively stable for some time. Identifying these stable periods could be useful for understanding consistent hiring trends.
</div>
                        """,unsafe_allow_html=True)
            
with tab5:
    df = pd.read_csv("C:\AProgramming\Python\Linkedin\Streamlit_Linkedin\Streamlit_Prediction.csv")
    st.info(f"Columns, Rows: {df.shape}")
    st.dataframe(df)
    