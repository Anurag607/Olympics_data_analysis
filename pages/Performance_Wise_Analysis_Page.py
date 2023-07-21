from Libraries import alt, st


def PerformanceWiseAnalysis(athletes_df):
    st.sidebar.title("Performance wise Analysis")
    feature_list = ['Countries', 'Athletes']
    feature_list.sort()

    selected_feature = st.sidebar.selectbox('Plot by', feature_list)
    st.markdown(f"### Top 10 {selected_feature} ")

    if selected_feature == 'Countries':
        athletes_df.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values(
            'Gold', ascending=False).reset_index()

        # Dropped Duplicate Rows

        medal_tally = athletes_df.drop_duplicates(
            subset={'Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'})

        medal_tally = medal_tally.groupby('region').sum(
        )[['Gold', 'Silver', 'Bronze']].reset_index()

        medal_tally['Total'] = medal_tally['Gold'] + \
            medal_tally['Silver']+medal_tally['Bronze']
        medal_tally = medal_tally.sort_values('Gold', ascending=False)
        top10countries = medal_tally.head(10)
        top10countries

        fig = alt.Chart(top10countries).mark_bar().encode(
            x=alt.X('region', sort='-y', axis=alt.Axis(labelAngle=-25)),
            y='Total',
            color=alt.Color('region', legend=None)
        ).properties(
            width=600,
            height=400,
            title='Top 10 Countries'
        )

        st.altair_chart(fig)

        fig = alt.Chart(top10countries).mark_bar().encode(
            x=alt.X('region', sort='-y', axis=alt.Axis(labelAngle=-25)),
            y='Gold',
            color=alt.Color('region', legend=None)
        ).properties(
            width=600,
            height=400,
            title='Gold Medal Count by Country (Top 10)'
        )

        st.altair_chart(fig)
        fig = alt.Chart(top10countries).mark_bar().encode(
            x=alt.X('region', sort='-y', axis=alt.Axis(labelAngle=-25)),
            y='Silver',
            color=alt.Color('region', legend=None)
        ).properties(
            width=600,
            height=400,
            title='Silver Medal Count by Country (Top 10)'
        )

        st.altair_chart(fig)
        fig = alt.Chart(top10countries).mark_bar().encode(
            x=alt.X('region', sort='-y', axis=alt.Axis(labelAngle=-25)),
            y='Bronze',
            color=alt.Color('region', legend=None)
        ).properties(
            width=600,
            height=400,
            title='Bronze Medal Count by Country (Top 10)'
        )

        st.altair_chart(fig)

    else:
        athlete = athletes_df.groupby('Name').sum()[
            ['Gold', 'Silver', 'Bronze']].sort_values('Gold', ascending=False).reset_index()

        athlete['Total'] = athlete['Gold']+athlete['Silver']+athlete['Bronze']
        athlete = athlete.sort_values('Total', ascending=False)
        top10athlete = athlete.head(10)
        top10athlete

        fig = alt.Chart(top10athlete).mark_bar().encode(
            x=alt.X('Name', sort='-y', axis=alt.Axis(labelAngle=-80)),
            y='Total',
            color='Name'
        ).properties(
            width=800,
            height=400,
            title='Top 10 Athletes'
        )
        st.altair_chart(fig)
        fig = alt.Chart(top10athlete).mark_bar().encode(
            x=alt.X('Name', sort='-y', axis=alt.Axis(labelAngle=-80)),
            y='Gold',
            color='Name'
        ).properties(
            width=800,
            height=400,
            title='Top 10 Gold Medalists'
        )
        st.altair_chart(fig)
        fig = alt.Chart(top10athlete).mark_bar().encode(
            x=alt.X('Name', sort='-y', axis=alt.Axis(labelAngle=-85)),
            y='Silver',
            color='Name'
        ).properties(
            width=800,
            height=400,
            title='Top 10 Silver Medalists'
        )
        st.altair_chart(fig)
        fig = alt.Chart(top10athlete).mark_bar().encode(
            x=alt.X('Name', sort='-y', axis=alt.Axis(labelAngle=-80)),
            y='Bronze',
            color='Name'
        ).properties(
            width=800,
            height=400,
            title='Top 10 Bronze Medalists'
        )
        st.altair_chart(fig)
