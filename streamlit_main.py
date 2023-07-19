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
import altair as alt


st.title('Olympics Data Analysis')
st.markdown('Data source: https://www.kaggle.com/heesoo37/120-years-of-olympic-history-athletes-and-results')

st.sidebar.title('Olympics Data Analysis')
st.sidebar.markdown('Data source: https://www.kaggle.com/heesoo37/120-years-of-olympic-history-athletes-and-results')

user_menu = st.sidebar.radio(
    'Select an Option',
    ('Dummy Page','Country-wise Analysis','Athlete wise Analysis', 'Sex Based Analysis','Performance wise Analysis')
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

    total_athletes=medal_tally[medal_tally['region']==selected_country].groupby('Sex')
    total_male_athlete=total_athletes.count()['ID']['M']
    total_female_athlete=total_athletes.count()['ID']['F']
    
    color_scheme=['aquamarine','turquoise'] 

    fig=plt.figure(figsize=(10,6))
    
    source=pd.DataFrame({
        "Gender":['Male','Female'],
        "Count":[total_male_athlete,total_female_athlete]
    })
    fig=alt.Chart(source).mark_arc(innerRadius=70).encode(
    theta="Count:Q",
    color=alt.Color("Gender:N",scale=alt.Scale(range=['aquamarine','turquoise'])),
    ).properties(
        height=450,
    ).configure_legend(
        orient="bottom"
    )
    st.altair_chart(fig, use_container_width=True)
    st.dataframe(source, use_container_width=True)
    # Plotting Bar chart for Sex Based Medal Distribution According To Each Country
    heading=f"Medal Count by Medal Type and Gender For {selected_country}"
    gk = bc.mf_medal_tally(medal_tally,selected_country)

    
    fig=alt.Chart(gk).mark_bar().encode(
    x=alt.X("Gender:N").axis(labelAngle=0),
    y='count:Q',
    color=alt.Color('Gender:N',scale=alt.Scale(range=['aquamarine','turquoise'])),
    column='Medal:N'
    ).properties(
        width=140,
        height=400,
        # title=heading
    ).configure_title(
        align='center',
        fontSize=25,
    ).configure_header(
        titleColor='#9ca0ad',
        titleFontSize=14,
        labelColor='#9ca0ad',
        labelFontSize=14
    )
    
    st.altair_chart(fig)
    pivot_data=bc.mf_medal_pivot_data(medal_tally,selected_country)
    st.dataframe(pivot_data, use_container_width=True)
    
elif user_menu == 'Performance wise Analysis':

    st.sidebar.title("Performance wise Analysis")
    feature_list = ['Countries','Athletes']
    feature_list.sort()

    selected_feature = st.sidebar.selectbox('Plot by',feature_list)
    st.markdown(f"### Top 10 {selected_feature} ")
   
    if selected_feature == 'Countries':
        athletes_df.groupby('region').sum()[['Gold','Silver','Bronze']].sort_values('Gold',ascending=False).reset_index()

        # Dropped Duplicate Rows 

        medal_tally=athletes_df.drop_duplicates(subset={'Team','NOC','Games','Year','City','Sport','Event','Medal'})

        medal_tally=medal_tally.groupby('region').sum()[['Gold','Silver','Bronze']].reset_index()

        medal_tally['Total']=medal_tally['Gold']+medal_tally['Silver']+medal_tally['Bronze']
        medal_tally=medal_tally.sort_values('Gold',ascending=False)
        top10countries=medal_tally.head(10)
        top10countries

        
        fig = alt.Chart(top10countries).mark_bar().encode(
            x=alt.X('region',sort='-y',axis=alt.Axis(labelAngle=-25)),
            y='Total',
            color=alt.Color('region', legend=None)
        ).properties(
            width=600,
            height=400,
            title='Top 10 Countries'
        )

        st.altair_chart(fig)

        fig = alt.Chart(top10countries).mark_bar().encode(
            x=alt.X('region',sort='-y',axis=alt.Axis(labelAngle=-25)),
            y='Gold',
            color=alt.Color('region', legend=None)
        ).properties(
            width=600,
            height=400,
            title='Gold Medal Count by Country (Top 10)'
        )

        st.altair_chart(fig)
        fig = alt.Chart(top10countries).mark_bar().encode(
            x=alt.X('region',sort='-y',axis=alt.Axis(labelAngle=-25)),
            y='Silver',
            color=alt.Color('region', legend=None)
        ).properties(
            width=600,
            height=400,
            title='Silver Medal Count by Country (Top 10)'
        )

        st.altair_chart(fig)
        fig = alt.Chart(top10countries).mark_bar().encode(
            x=alt.X('region',sort='-y',axis=alt.Axis(labelAngle=-25)),
            y='Bronze',
            color=alt.Color('region', legend=None)
        ).properties(
            width=600,
            height=400,
            title='Bronze Medal Count by Country (Top 10)'
        )

        st.altair_chart(fig)
        
    else :
        athlete=athletes_df.groupby('Name').sum()[['Gold','Silver','Bronze']].sort_values('Gold',ascending=False).reset_index()
        
        athlete['Total']=athlete['Gold']+athlete['Silver']+athlete['Bronze']
        athlete=athlete.sort_values('Total',ascending=False)
        top10athlete=athlete.head(10)
        top10athlete

        
        fig = alt.Chart(top10athlete).mark_bar().encode(
            x=alt.X('Name', sort='-y',axis=alt.Axis(labelAngle=-80)),
            y='Total',
            color='Name'
        ).properties(
            width=800,
            height=400,
            title='Top 10 Athletes'
        )
        st.altair_chart(fig)
        fig = alt.Chart(top10athlete).mark_bar().encode(
            x=alt.X('Name', sort='-y',axis=alt.Axis(labelAngle=-80)),
            y='Gold',
            color='Name'
        ).properties(
            width=800,
            height=400,
            title='Top 10 Gold Medalists'
        )
        st.altair_chart(fig)
        fig = alt.Chart(top10athlete).mark_bar().encode(
            x=alt.X('Name', sort='-y',axis=alt.Axis(labelAngle=-85)),
            y='Silver',
            color='Name'
        ).properties(
            width=800,
            height=400,
            title='Top 10 Silver Medalists'
        )
        st.altair_chart(fig)
        fig = alt.Chart(top10athlete).mark_bar().encode(
            x=alt.X('Name', sort='-y',axis=alt.Axis(labelAngle=-80)),
            y='Bronze',
            color='Name'
        ).properties(
            width=800,
            height=400,
            title='Top 10 Bronze Medalists'
        )
        st.altair_chart(fig)

    



    