from Libraries import st, utils
from streamlit_main import athletes_df


def CountryWiseAnalysis(athletes_df):
    st.title('Country-wise Analysis')
    st.sidebar.title('Country-wise Analysis')

    country_list = athletes_df['region'].dropna().unique().tolist()
    country_list.sort()

    selected_country = st.sidebar.selectbox('Select a Country', country_list)

    st.markdown(f"### {selected_country} Participation Over the Years")

    country_df = utils.yearwise_medal_data(athletes_df, selected_country)
    fig = st.line_chart(country_df, x="Year", y="Medal")


CountryWiseAnalysis(athletes_df)
