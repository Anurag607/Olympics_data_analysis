import base64
import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import preprocessor
import utilites.utils as utils
import utilites.pie_chart_helper as sc
import utilites.mf_bar_chart_helper as bc

st.title('Olympics Data Analysis')
st.markdown('Data source: https://www.kaggle.com/heesoo37/120-years-of-olympic-history-athletes-and-results')

st.sidebar.title('Olympics Data Analysis')
st.sidebar.markdown('Data source: https://www.kaggle.com/heesoo37/120-years-of-olympic-history-athletes-and-results')

user_menu = st.sidebar.radio(
    'Select an Option',
    ('Dummy Page','Country-wise Analysis','Athlete wise Analysis', 'Sex Based Analysis')
)

@st.cache_data(persist=True)
def load_data():
    athletes_df = pd.read_csv("./assets/athlete_events.csv")
    regions = pd.read_csv('./assets/noc_regions.csv')
    athletes_df = preprocessor.preprocess(athletes_df, regions)
    return athletes_df

athletes_df = load_data()   


    

if user_menu == 'Dummy Page':
    
    # Sidebar - Team Selection
    sorted_team = sorted(athletes_df['Team'].unique())
    selected_team = st.sidebar.multiselect('Team', sorted_team)

    # Sidebar - Sport Selection
    sorted_sport = sorted(athletes_df['Sport'].unique())
    selected_sport = st.sidebar.multiselect('Sport', sorted_sport)

    # Sidebar - Event Selection
    sorted_event = sorted(athletes_df['Event'].unique())
    selected_event = st.sidebar.multiselect('Event', sorted_event)

    # Filtering Data
    df_selected_team = athletes_df[(athletes_df['Team'].isin(selected_team)) & (athletes_df['Sport'].isin(selected_sport)) & (athletes_df['Event'].isin(selected_event))]

    # Show filtered data
    st.write(df_selected_team if (not df_selected_team.empty) else athletes_df)

    # Heatmap
    if st.checkbox('Show Heatmap'):
        st.write('### Heatmap')
        st.write(df_selected_team.corr() if (not df_selected_team.empty) else athletes_df.corr())

        sns.set()
        st.set_option('deprecation.showPyplotGlobalUse', False)
        fig = plt.figure(figsize=(12,8))
        sns.heatmap(df_selected_team.corr() if (not df_selected_team.empty) else athletes_df.corr(), annot=True)
        plt.xticks(rotation=45)
        plt.yticks(rotation=45)
        plt.title('Correlation Heatmap')

        st.pyplot(fig)

    # Raw Data
    if st.checkbox('Show Raw Data', False):
        st.write(df_selected_team if (not df_selected_team.empty) else athletes_df)

    # Download CSV Data
    def filedownload(df):

        csv = df.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()
        href = f'<a href="data:file/csv;base64,{b64}" download="olympics.csv">Download CSV File</a>'
        return href

    st.markdown(filedownload(df_selected_team), unsafe_allow_html=True)

elif user_menu == 'Country-wise Analysis':
    
    st.sidebar.title('Country-wise Analysis')

    country_list = athletes_df['region'].dropna().unique().tolist()
    country_list.sort()

    selected_country = st.sidebar.selectbox('Select a Country',country_list)
    
    st.markdown(f"### {selected_country} Participation Over the Years")
    
    country_df = utils.yearwise_medal_data(athletes_df,selected_country)
    fig = st.line_chart(country_df, x="Year", y="Medal")
    
    st.markdown("### Raw Data")    
    if selected_country == 'Overall':
        st.write(athletes_df)
    else:
        data = athletes_df[athletes_df['region'] == selected_country].reset_index(drop=True)
        st.write(data)
    

elif user_menu == 'Sex Based Analysis':

    st.sidebar.title("Sex Based Analysis")
    country_list = athletes_df['region'].dropna().unique().tolist()
    country_list.sort()

    selected_country = st.sidebar.selectbox('Select a Country',country_list)

    # Dropped Duplicate Rows 
    
    medal_tally=athletes_df.drop_duplicates(subset={'Team','NOC','Games','Year','City','Sport','Event','Medal'})

    total_athletes=medal_tally['ID'].count()
    total_male_athlete=medal_tally.loc[medal_tally['Sex']=='M']['ID'].count()
    total_female_athlete=medal_tally.loc[medal_tally['Sex']=='F']['ID'].count()
    
    color_scheme=['aquamarine','turquoise']
    
    # Plotting Doughnut Chart For Total Athletes

    st.markdown("#### Total Athletes")

    fig=plt.figure(figsize=(10,6))
    fig.patch.set_facecolor('#0e1117')
    plt.rcParams['text.color'] = 'white'

    circle=plt.Circle((0,0),0.5,color='white')

    data=[total_male_athlete,total_female_athlete]
    
    plt.pie(data,labels=['Male','Female'],colors=color_scheme,autopct=lambda pct: sc.pie_pct(pct, data),counterclock=False,startangle=90,pctdistance=0.75,)
    plt.axis('equal')
    plt.legend(title='Gender',facecolor='#262730',edgecolor='#262730',labelcolor='white')
    plt.gca().add_artist(circle)
    
    st.pyplot(fig)

    # Plotting Bar chart for Sex Based Medal Distribution According To Each Country
    st.markdown(f"#### Medal Count by Medal Type and Gender For {selected_country}")
    gk = bc.mf_medal_tally(medal_tally,selected_country)
    
    # Create the figure and axes
    fig, ax = plt.subplots(figsize=(9, 5.5))
    fig.set_facecolor('#262730')
    # ax.patch.set_facecolor('#262730')

    # Plot the grouped bar chart
    gk.plot(kind='bar', width=0.7, color=['aquamarine','turquoise'], ax=ax)
    ax.set_xlabel('Medal',color='white')
    ax.set_ylabel('Count',color='white')
    ax.legend(title='Gender', bbox_to_anchor=(1, 1), facecolor='#262730',edgecolor='#262730',labelcolor='white')

    # Set the grid color to light gray
    ax.xaxis.grid(True, color='lightgray')
    ax.yaxis.grid(True, color='lightgray')

    # Make the grid appear behind the bars
    ax.set_axisbelow(True)
    plt.tight_layout()
    st.pyplot(fig)

    # Print Raw Data
    st.dataframe(gk, use_container_width=True)