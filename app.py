import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Bird Strike Dashboard", layout="wide")

st.title("🦅✈️ Bird Strike Data Dashboard")
st.markdown("This app helps pilots and aviation professionals analyze bird strike incidents for better safety and planning.")

uploaded_file = st.file_uploader("Upload Bird Strike CSV File", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.success("File uploaded successfully!")
    st.write("Data Preview:")
    st.dataframe(df.head())

    # Optional filters
    with st.sidebar:
        st.header("🔍 Filters")
        if 'STATE' in df.columns:
            selected_state = st.selectbox("Select State", options=["All"] + sorted(df['STATE'].dropna().unique().tolist()))
            if selected_state != "All":
                df = df[df["STATE"] == selected_state]

        if 'AIRPORT' in df.columns:
            selected_airport = st.selectbox("Select Airport", options=["All"] + sorted(df['AIRPORT'].dropna().unique().tolist()))
            if selected_airport != "All":
                df = df[df["AIRPORT"] == selected_airport]

    # Visualization
    st.subheader("📈 Year-wise Bird Strike Reports")
    if 'INCIDENT_YEAR' in df.columns:
        year_data = df['INCIDENT_YEAR'].value_counts().sort_index()
        fig = px.bar(x=year_data.index, y=year_data.values, labels={'x': 'Year', 'y': 'Number of Strikes'})
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("📊 Strikes by Aircraft Type")
    if 'AIRCRAFT' in df.columns:
        aircraft_data = df['AIRCRAFT'].value_counts().nlargest(10)
        fig2 = px.pie(names=aircraft_data.index, values=aircraft_data.values, title="Top 10 Aircraft in Strikes")
        st.plotly_chart(fig2, use_container_width=True)

    st.subheader("⚠️ Damage Analysis")
    if 'DAMAGED' in df.columns:
        fig3 = px.histogram(df, x='DAMAGED', title="Extent of Damage")
        st.plotly_chart(fig3, use_container_width=True)

    st.info("Use the filters on the left to explore specific data!")
else:
    st.warning("Please upload a CSV file to begin.")
