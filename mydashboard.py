import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(
    page_title="LinkedIn Job Market Intelligence",
    page_icon="💼",
    layout="wide"
)
import pandas as pd
jobs = pd.read_csv("postings_small.csv", on_bad_lines="skip")
companies = pd.read_csv("companies.csv")

st.markdown("""
<style>

.stApp{
    background:#0F172A;
    color:white;
}

[data-testid="stSidebar"]{
    background:#111827;
    border-right:2px solid #0A66C2;
}

.main-title{
    text-align:center;
    color:#0A66C2;
    font-size:55px;
    font-weight:800;
}

.sub-title{
    text-align:center;
    color:#94A3B8;
    font-size:18px;
}

.kpi-card{
    background:#1E293B;
    border-radius:15px;
    padding:20px;
    text-align:center;
    border:1px solid #334155;
}

.kpi-title{
    color:#94A3B8;
}

.kpi-value{
    color:white;
    font-size:32px;
    font-weight:bold;
}

.section-title{
    color:white;
    font-size:28px;
    margin-top:25px;
}

</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="main-title">
💼 LINKEDIN JOB MARKET INTELLIGENCE
</div>

<div class="sub-title">
Real-Time Hiring Trends, Salary Intelligence & Workforce Analytics
</div>
""", unsafe_allow_html=True)

st.sidebar.title("🎛 Talent Intelligence Hub")

search_job = st.sidebar.text_input(
    "🔍 Search Job"
)

location_filter = st.sidebar.multiselect(
    "📍 Location",
    sorted(jobs["location"].dropna().unique())
)

work_type_filter = st.sidebar.multiselect(
    "💼 Work Type",
    sorted(jobs["formatted_work_type"].dropna().unique())
)

experience_filter = st.sidebar.multiselect(
    "🎓 Experience Level",
    sorted(jobs["formatted_experience_level"].dropna().unique())
)

st.sidebar.button("🔄 Reset Filters")

filtered = jobs.copy()

if location_filter:
    filtered = filtered[
        filtered["location"].isin(location_filter)
    ]

if work_type_filter:
    filtered = filtered[
        filtered["formatted_work_type"].isin(work_type_filter)
    ]

if experience_filter:
    filtered = filtered[
        filtered["formatted_experience_level"].isin(experience_filter)
    ]

if search_job:
    filtered = filtered[
        filtered["title"].str.contains(
            search_job,
            case=False,
            na=False
        )
    ]

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "📄 Total Jobs",
        len(filtered)
    )

with c2:
    st.metric(
        "🏢 Companies",
        filtered["company_name"].nunique()
    )

with c3:
    st.metric(
        "👀 Views",
        int(filtered["views"].sum())
    )

with c4:
    st.metric(
        "📝 Applications",
        int(filtered["applies"].sum())
    )
    st.markdown(
    '<div class="section-title">🏢 Top Hiring Companies</div>',
    unsafe_allow_html=True
)

top_companies = (
    filtered["company_name"]
    .value_counts()
    .head(10)
    .reset_index()
)

fig1 = px.bar(
    top_companies,
    x="company_name",
    y="count",
    color="count"
)

st.plotly_chart(
    fig1,
    use_container_width=True
)

st.markdown(
    '<div class="section-title">📍 Jobs by Location</div>',
    unsafe_allow_html=True
)

location_data = (
    filtered["location"]
    .value_counts()
    .head(10)
    .reset_index()
)

fig2 = px.bar(
    location_data,
    x="location",
    y="count",
    color="count"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

st.markdown(
    '<div class="section-title">💼 Work Type Distribution</div>',
    unsafe_allow_html=True
)

fig3 = px.pie(
    filtered,
    names="formatted_work_type"
)

st.plotly_chart(
    fig3,
    use_container_width=True
)

st.markdown(
    '<div class="section-title">🎓 Experience Levels</div>',
    unsafe_allow_html=True
)

fig4 = px.histogram(
    filtered,
    x="formatted_experience_level",
    color="formatted_experience_level"
)

st.plotly_chart(
    fig4,
    use_container_width=True
)

if "normalized_salary" in filtered.columns:

    st.markdown(
        '<div class="section-title">💰 Salary Distribution</div>',
        unsafe_allow_html=True
    )

    fig5 = px.histogram(
        filtered,
        x="normalized_salary",
        nbins=30
    )

    st.plotly_chart(
        fig5,
        use_container_width=True
    )

if (
    "views" in filtered.columns and
    "applies" in filtered.columns
):

    st.markdown(
        '<div class="section-title">📈 Applications vs Views</div>',
        unsafe_allow_html=True
    )

    fig6 = px.scatter(
        filtered,
        x="views",
        y="applies"
    )

    st.plotly_chart(
        fig6,
        use_container_width=True
    )
    st.markdown(
    '<div class="section-title">🔥 Correlation Matrix</div>',
    unsafe_allow_html=True
)

numeric_df = filtered.select_dtypes(
    include="number"
)

corr = numeric_df.corr()

fig, ax = plt.subplots(
    figsize=(10,6)
)

sns.heatmap(
    corr,
    annot=True,
    cmap="Blues"
)

st.pyplot(fig)

st.markdown(
    '<div class="section-title">📋 Executive Summary</div>',
    unsafe_allow_html=True
)

st.dataframe(
    filtered.head(20),
    use_container_width=True
)

csv = filtered.to_csv(index=False)

st.download_button(
    "📥 Download Report",
    csv,
    "linkedin_jobs_report.csv",
    "text/csv"
)

st.markdown("""
<hr>

<center>
<h3 style="color:#0A66C2;">
💼 LINKEDIN JOB MARKET INTELLIGENCE DASHBOARD
</h3>
</center>
""", unsafe_allow_html=True)

pandas
plotly
matplotlib
seaborn
numpy
