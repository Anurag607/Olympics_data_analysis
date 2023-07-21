from Libraries import st, pd, preprocess

# Page Imports
from pages.Dummy_Page import DummyPage
from pages.Sex_Based_Analysis_Page import SexBasedAnalysis
from pages.Athlete_Wise_Analysis_Page import AthleteWiseAnalysis
from pages.Country_Wise_Analysis_Page import CountryWiseAnalysis
from pages.Performance_Wise_Analysis_Page import PerformanceWiseAnalysis
from pages.Male_Female_Participation_Analysis_Page import MaleFemaileParticipationAnalysis


st.title('Olympics Data Analysis')

st.sidebar.title('Olympics Data Analysis')
st.sidebar.markdown(
    'Data source: https://www.kaggle.com/heesoo37/120-years-of-olympic-history-athletes-and-results'
)


@st.cache_data(persist=True)
# Loading the data form the CSV files...
def load_data():
    athletes_df = pd.read_csv("./assets/athlete_events.csv")
    regions = pd.read_csv('./assets/noc_regions.csv')
    athletes_df = preprocess.preprocess(athletes_df, regions)
    return athletes_df


athletes_df = load_data()

# Defining the user menu in the sidebar...
user_menu = st.sidebar.radio(
    'Select an Option',
    (
        'Dummy Page',
        'Country-wise Analysis',
        'Athlete wise Analysis',
        'Sex Based Analysis',
        'Male-Female Participation Analysis',
        'Performance wise Analysis'
    )
)

if user_menu == 'Dummy Page':
    DummyPage(athletes_df)

elif user_menu == 'Country-wise Analysis':
    CountryWiseAnalysis(athletes_df)

elif user_menu == 'Athlete-wise Analysis':
    AthleteWiseAnalysis(athletes_df)

elif user_menu == 'Sex Based Analysis':
    SexBasedAnalysis(athletes_df)

elif user_menu == 'Male-Female Participation Analysis':
    MaleFemaileParticipationAnalysis(athletes_df)

elif user_menu == 'Performance wise Analysis':
    PerformanceWiseAnalysis(athletes_df)
