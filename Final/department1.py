import pickle
import joblib
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import sklearn
print(sklearn.__version__)
# st.set_page_config(
#     page_title="Attrition Analysis",
#     page_icon="📈",
# )
# Function to generate plots
def main():
    def generate_plots(df, cat):
        for i, col in enumerate(cat):
            fig, axes = plt.subplots(1, 2, figsize=(10, 5))

            # count of col (countplot)
            ax = sns.countplot(data=df, x=col, ax=axes[0])
            activities = [var for var in df[col].value_counts().sort_index().index]
            ax.set_xticks(np.arange(len(activities)))  # Set ticks explicitly
            ax.set_xticklabels(activities, rotation=90)
            for container in ax.containers:
                ax.bar_label(container)

            # count of col (pie chart)
            index = df[col].value_counts().index
            size = df[col].value_counts().values
            explode = (0.05, 0.05)

            axes[1].pie(size, labels=index, autopct='%1.1f%%', pctdistance=0.85)

            # Inner circle
            centre_circle = plt.Circle((0, 0), 0.70, fc='white')
            fig.gca().add_artist(centre_circle)
            plt.suptitle(col, backgroundcolor='black', color='white', fontsize=15)

            # Show the plot
            st.pyplot(fig)

    attrition_analysis_model = joblib.load(open("attrition_model_with_scaler.sav", 'rb'))
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox("Go to", ["Prediction", "Plot Analysis","Attrition Count Plot","Report"])

    # Main content
    if page == "Prediction":
        st.title("Attrition Analysis System for HR")
        col1,col2,col3=st.columns(3)
        with col1:
            Age=st.number_input('Age')
        with col2:
            BusinessTravel=st.selectbox("Business Travels",["Travel rarely","Travel frequently","Non-Travel"])
            if BusinessTravel=="Travel Rarely":
                BusinessTravel=2
            elif BusinessTravel=="Travel frequently":
                BusinessTravel=3
            else:
                BusinessTravel=4
        with col3:
            DailyRate=st.number_input("Daily rate")

        with col1:
            Department=st.selectbox("Department",["Sales","Human Resources","Research & Development"])
            if Department=="Sales":
                Department=2
            elif Department=="Human Resources":
                Department=3
            else:
                Department=4
        with col2:
            DistanceFromHome=st.number_input("Distance from home(km)")
        with col3: 
            EducationField=st.selectbox("Education Field",["Life Sciences","Medical","Marketing","Techincal Degree","Human Resources","Other"])
            if EducationField=="Life Sciences":
                EducationField=2
            elif EducationField=="Medical":
                EducationField=3
            elif EducationField=="Marketing":
                EducationField=4
            elif EducationField=="Techincal Degree":
                EducationField=5
            elif EducationField=="Human Resources":
                EducationField=6
            else:
                EducationField=7

        with col1:
            Education=st.selectbox("Education",["Below college","College","Bachelor","Master","Doctor"])
            if Education=="Below college":
                Education=1
            if Education=="College":
                Education=2
            if Education=="Bachelor":
                Education=3
            if Education=="Master":
                Education=4
            if Education=="Doctor":
                Education=5

        with col2:
            EnvironmentSatisfaction=st.selectbox("Environment Satisfaction",["Low","Medium","High","Very High"])
            if EnvironmentSatisfaction=="Low":
                EnvironmentSatisfaction=1
            if EnvironmentSatisfaction=="Medium":
                EnvironmentSatisfaction=2
            if EnvironmentSatisfaction=="High":
                EnvironmentSatisfaction=3
            if EnvironmentSatisfaction=="Very High":
                EnvironmentSatisfaction=4

        with col3:
            Gender=st.selectbox("Gender",["Male","Female"])
            if Gender=="Male":
                Gender=2
            else:
                Gender=3

        with col1:
            HourlyRate=st.number_input("Hourly Rate")

        with col2:
            JobInvolvement=st.selectbox("Job Involvment",["Low","Medium","High","Very High"])
            if JobInvolvement=="Low":
                JobInvolvement=1
            elif JobInvolvement=="Medium":
                JobInvolvement=2
            elif JobInvolvement=="High":
                JobInvolvement=3    
            else:
                JobInvolvement=4
                
        with col3:
            JobLevel=st.number_input("Job Level",min_value=1,max_value=5)

        with col1:
            JobRole=st.selectbox("Job Role",["Sales Executive","Manufacturing Director","Healthcare Representative","Manager","Research Director","Laboratory Technician","Sales Representative","Research Scientist","Human Resources"])
            if JobRole=="Sales Executive":
                JobRole=2
            if JobRole=="Manufacturing Director":
                JobRole=3
            if JobRole=="Healthcare Representative":
                JobRole=4
            if JobRole=="Manager":
                JobRole=5
            if JobRole=="Reasearch Director":
                JobRole=6
            if JobRole=="Laboratory Technician":
                JobRole=7
            if JobRole=="Sales Representative":
                JobRole=8
            if JobRole=="Research Scientist":
                JobRole=9
            if JobRole=="Human Resources":
                JobRole=10

        with col2:
            JobSatisfaction=st.selectbox("Job Satisfaction",["Low","Medium","High","Very High"])
            if JobSatisfaction=="Low":
                JobSatisfaction=1
            elif JobSatisfaction=="Medium":
                JobSatisfaction=2
            elif JobSatisfaction=="High":
                JobSatisfaction=3    
            else:
                JobSatisfaction=4

        with col3:
            MaritalStatus=st.selectbox("Marital Status",["Single","Married","Divorced"])
            if MaritalStatus=="Single":
                MaritalStatus=2
            elif MaritalStatus=="Married":
                MaritalStatus=3
            else:
                MaritalStatus=4

        with col1:
            MonthlyRate=st.number_input("Monthly Rate")
            
        with col2:
            NumCompaniesWorked=st.number_input("Number of companies worked")

        with col3:
            OverTime=st.selectbox("Over Time",["Yes","No"])
            if OverTime=="Yes":
                OverTime=2
            else:
                OverTime=3

        with col1:
            PercentSalaryHike=st.number_input("Percentage of Salary Hike")

        with col2:
            PerformanceRating=st.selectbox("Performance Rating",["Low","Good","Excellent","Outstanding"])
            if PerformanceRating=="Low":
                PerformanceRating=1
            elif PerformanceRating=="Good":
                PerformanceRating=2
            elif PerformanceRating=="Excellent":
                PerformanceRating=3
            else:
                PerformanceRating=4


        with col3:
            RelationshipSatisfaction=st.selectbox("Relationship Satisfaction",["Low","Medium","High","Very High"])
            if RelationshipSatisfaction=="Low":
                RelationshipSatisfaction=1
            elif RelationshipSatisfaction=="Medium":
                RelationshipSatisfaction=2
            elif RelationshipSatisfaction=="High":
                RelationshipSatisfaction=3    
            else:
                RelationshipSatisfaction=4
                
        with col1:
            StockOptionLevel=st.number_input("Stock Option Level",min_value=0)

        with col2:
            TotalWorkingYears=st.number_input("Total Working Years")
        
        with col3:
            TrainingTimesLastYear=st.number_input("Number of times employees were trained in the last year")

        with col1:
            WorkLifeBalance=st.selectbox("Work Life Balance",["Bad","Good","Better","Best"])
            if WorkLifeBalance=="Bad":
                WorkLifeBalance=1
            elif WorkLifeBalance=="Good":
                WorkLifeBalance=2
            elif WorkLifeBalance=="Better":
                WorkLifeBalance=3
            else:
                WorkLifeBalance=4

        with col2:
            YearsSinceLastPromotion=st.number_input("Number of years since last promotion")
            
        user_inputs = pd.DataFrame({
            'Age': [Age],
            'Attrition': [0],
            'BusinessTravel': [BusinessTravel],
            'DailyRate': [DailyRate],
            'Department': [Department],
            'DistanceFromHome': [DistanceFromHome],
            'Education': [Education],
            'EducationField': [EducationField],
            'EnvironmentSatisfaction': [EnvironmentSatisfaction],
            'Gender': [Gender],
            'HourlyRate': [HourlyRate],
            'JobInvolvement': [JobInvolvement],
            'JobLevel': [JobLevel],
            'JobRole': [JobRole],
            'JobSatisfaction': [JobSatisfaction],
            'MaritalStatus': [MaritalStatus],
            'MonthlyRate': [MonthlyRate],
            'NumCompaniesWorked': [NumCompaniesWorked],
            'OverTime': [OverTime],
            'PercentSalaryHike': [PercentSalaryHike],
            'PerformanceRating': [PerformanceRating],
            'RelationshipSatisfaction': [RelationshipSatisfaction],
            'StockOptionLevel': [StockOptionLevel],
            'TotalWorkingYears': [TotalWorkingYears],
            'TrainingTimesLastYear': [TrainingTimesLastYear],
            'WorkLifeBalance': [WorkLifeBalance],
            'YearsSinceLastPromotion': [YearsSinceLastPromotion]
        })

        scaler = attrition_analysis_model[1]

        normalized_inputs = scaler.transform(user_inputs)
        print(normalized_inputs)
        # Convert the normalized inputs to a DataFrame with consistent feature names
        normalized_df = pd.DataFrame(normalized_inputs, columns=user_inputs.columns)

        # Add a placeholder 'Attrition' column for prediction
        normalized_df['Attrition'] = 0
        # code for Prediction
        attrition_analysis = ''
        
            # creating a button for Prediction
            
        if st.button('Attrition Analysis Result'):
                        attrition_prediction = attrition_analysis_model[0].predict(normalized_df.drop('Attrition', axis=1))
                        if (attrition_prediction[0]==1):
                                attrition_analysis = 'The employee will most likely not resign'
                        else:
                                attrition_analysis = 'The employee will most likely resign'
                
                        st.success(attrition_analysis)




    elif page == "Plot Analysis":
        st.title("Attrition Analysis System for HR - Plot Analysis")
        # Load the dataset (replace 'your_dataset.csv' with the actual file name)
        df = pd.read_csv('WA_Fn-UseC_-HR-Employee-Attrition.csv')
        cat = df.select_dtypes(['object']).columns

        # Placeholder for plots
        plot_placeholder = st.empty()

        # Your existing code for generating plots
        # ...

        # Generate and display plots
        generate_plots(df, cat)
        
    elif page == "Attrition Count Plot":
        st.title("Attrition Analysis System for HR - Attrition Count Plots")
        # Load the dataset (replace 'your_dataset.csv' with the actual file name)
        df = pd.read_csv('WA_Fn-UseC_-HR-Employee-Attrition.csv')
        cat = df.select_dtypes(['object']).columns

        # Additional section for count plots with respect to "Attrition"
        for column in cat:
            plt.figure(figsize=(10, 5))
            ax = sns.countplot(x=df[column], data=df, hue="Attrition")
            for container in ax.containers:
                ax.bar_label(container)
            plt.title(column, backgroundcolor='black', color='white', fontsize=20)
            plt.xticks(rotation=90)
            plt.xlabel(column, fontsize=20)
            plt.grid()
            st.pyplot(plt)
            plt.close()
            
            
    elif page=="Report":
        st.title("Attrition Analysis System for HR - Attrition Report")
        st.subheader("📈Attrition Report")
        st.info(
            """
            - Attrition is the highest for both men and women from 18 to 35 years of age and gradually decreases.
            - As income increases, attrition decreases.
            - Attrition is much less in divorced women.
            - Attrition is higher for employees who usually travel than others, and this rate is higher for women than for men.
            - Attrition is the highest for those in level 1 jobs.
            - Women with the job position of manager, research director, and laboratory technician have almost no attrition.
            - Men with the position of sales expert have a lot of attrition.
            """
        )

if __name__=="__main__":
    main()
