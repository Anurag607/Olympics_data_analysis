from Libraries import st, pd, preprocess

# Page Imports
from pages.Sex_Based_Analysis_Page import SexBasedAnalysis
from pages.Athlete_Wise_Analysis_Page import AthleteWiseAnalysis
from pages.Country_Wise_Analysis_Page import CountryWiseAnalysis
from pages.Performance_Wise_Analysis_Page import PerformanceWiseAnalysis
from pages.Male_Female_Participation_Analysis_Page import MaleFemaileParticipationAnalysis

st.sidebar.title('Olympics Data Analysis')
st.sidebar.markdown(
    'Data source: https://www.kaggle.com/heesoo37/120-years-of-olympic-history-athletes-and-results'
)

athletes = pd.read_csv("./assets/athlete_events.csv")
regions = pd.read_csv('./assets/noc_regions.csv')


@st.cache_data(persist=True)
# Loading the data form the CSV files...
def load_data():
    athletes_df = preprocess.preprocess(athletes, regions)
    return athletes_df


athletes_df = load_data()

# Page Navigation

st.markdown("## Olympics Data Analysis")
st.markdown("#### Select a page from the sidebar to start analyzing")
st.markdown(
    "Data source: https://www.kaggle.com/heesoo37/120-years-of-olympic-history-athletes-and-results")

st.markdown("### Contributors")
st.markdown("- [Bhavik Agarwal](https://github.com/Bhavik-ag)")
st.markdown("- [Anurag Goswami](https://github.com/Anurag607)")
st.markdown("- [Ayushi Mourya](https://github.com/AyushiMourya22)")
st.markdown("- [Arjit Patel](https://github.com/Arjit1136)")
