from Libraries import pd, alt, st, plt, bc


def SexBasedAnalysis(athletes_df):
    st.title("Sex Based Analysis")
    st.sidebar.title("Sex Based Analysis")
    country_list = athletes_df['region'].dropna().unique().tolist()
    country_list.sort()

    selected_country = st.sidebar.selectbox('Select a Country', country_list)

    # Dropped Duplicate Rows
    medal_tally = athletes_df.drop_duplicates(
        subset={'Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'})

    total_athletes = medal_tally[medal_tally['region']
                                 == selected_country].groupby('Sex')
    total_male_athlete = total_athletes.count()['ID']['M']
    total_female_athlete = total_athletes.count()['ID']['F']

    color_scheme = ['aquamarine', 'turquoise']

    fig = plt.figure(figsize=(10, 6))

    source = pd.DataFrame({
        "Gender": ['Male', 'Female'],
        "Count": [total_male_athlete, total_female_athlete]
    })

    fig = alt.Chart(source).mark_arc(innerRadius=70).encode(
        theta="Count:Q",
        color=alt.Color("Gender:N", scale=alt.Scale(
            range=color_scheme)),
    ).properties(
        height=450,
    ).configure_legend(
        orient="bottom"
    )

    st.altair_chart(fig, use_container_width=True)
    st.dataframe(source, use_container_width=True)

    # Plotting Bar chart for Sex Based Medal Distribution According To Each Country

    heading = f"Medal Count by Medal Type and Gender For {selected_country}"

    gk = bc.mf_medal_tally(medal_tally, selected_country)

    fig = alt.Chart(gk).mark_bar().encode(
        x=alt.X("Gender:N").axis(labelAngle=0),
        y='count:Q',
        color=alt.Color('Gender:N', scale=alt.Scale(
            range=color_scheme)),
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

    st.altair_chart(fig, use_container_width=False)
    pivot_data = bc.mf_medal_pivot_data(medal_tally, selected_country)
    st.dataframe(pivot_data, use_container_width=True)
