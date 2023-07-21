from Libraries import st, utils


def CountryWiseAnalysis(athletes_df):
    st.sidebar.title('Country-wise Analysis')

    country_list = athletes_df['region'].dropna().unique().tolist()
    country_list.sort()

    selected_country = st.sidebar.selectbox('Select a Country', country_list)

    st.markdown(f"### {selected_country} Participation Over the Years")

    country_df = utils.yearwise_medal_data(athletes_df, selected_country)
    fig = st.line_chart(country_df, x="Year", y="Medal")

    st.markdown("### Raw Data")
    if selected_country == 'Overall':
        st.write(athletes_df)
    else:
        data = athletes_df[athletes_df['region'] ==
                           selected_country].reset_index(drop=True)
        st.write(data)
