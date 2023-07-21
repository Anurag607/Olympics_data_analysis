from Libraries import st, pd, plt, np, alt


def MaleFemaileParticipationAnalysis(athletes_df, df_athletes, df_regions):
    st.title("Male Female Participation Analysis")
    st.sidebar.title("Male Female Participation Analysis")

    # Extracting from NOC_REGIONS.CSV

    country_code_mapping = {}
    region = df_regions['region']
    codes = df_regions['NOC']
    for index in range(len(codes)):
        country_code_mapping[codes[index]] = region[index]

    # ACCUMULATING REQUIRED DATA

    countries_code = df_athletes['NOC'].unique()
    countries = []
    for code in countries_code:
        if (code == 'SGP'):
            countries.append('SIN')
        else:
            countries.append(country_code_mapping[code])

    gender_ratio = dict(
        zip(list(codes), [[0 for x in range(2)] for x in range(len(countries))]))
    for name, group in df_athletes.groupby('NOC'):
        gender_ratio[(name, 'SIN')[name == 'SGP']][0] = list(
            group['Sex']).count('M')
        gender_ratio[(name, 'SIN')[name == 'SGP']][1] = list(
            group['Sex']).count('F')

    # Plotting the Chart

    male = [pair[0] for pair in list(gender_ratio.values())]
    female = [pair[1] for pair in list(gender_ratio.values())]
    X_axis = np.arange(len(gender_ratio.keys()))

    fig = plt.figure(figsize=(70, 35))
    plt.bar(X_axis - 0.2, female, 0.4, label='Female')
    plt.bar(X_axis + 0.2, male, 0.4, label='Male')
    plt.xticks(X_axis, list(country_code_mapping.values()),
               rotation='vertical')
    plt.legend(['Female', 'Male'], loc='upper left')
    plt.xlabel("Countries")
    plt.ylabel("Player Count")
    plt.title("Player Participation vs Host Country")

    st.pyplot(fig)
