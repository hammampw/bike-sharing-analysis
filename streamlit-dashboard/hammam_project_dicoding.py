import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from babel.numbers import format_currency

# Data Wrangling
df_hari = pd.read_csv("streamlit-dashboard/day.csv")
df_hari.rename(columns={
    'dteday': 'dateday',
    'yr': 'year',
    'mnth': 'month',
    'cnt': 'count'
}, inplace=True)
df_hari['month'] = df_hari['month'].map({
    1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
    7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'
})
df_hari['year'] = df_hari['year'].map({
    0: '2011', 1: '2012'
})
df_hari['season'] = df_hari['season'].map({
    1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'
})
df_hari['weekday'] = df_hari['weekday'].map({
    0: 'Sun', 1: 'Mon', 2: 'Tue', 3: 'Wed', 4: 'Thu', 5: 'Fri', 6: 'Sat'
})
df_hari['weathersit'] = df_hari['weathersit'].map({
    1: 'Clear/Partly Cloudy',
    2: 'Misty/Cloudy',
    3: 'Light Snow/Rain',
    4: 'Severe Weather'
})

def create_daily_rent_df(df):
    daily_rent_df = df.groupby(by='dateday').agg({
        'count': 'sum'
    }).reset_index()
    return daily_rent_df

def create_daily_casual_rent_df(df):
    daily_casual_rent_df = df.groupby(by='dateday').agg({
        'casual': 'sum'
    }).reset_index()
    return daily_casual_rent_df

def create_daily_registered_rent_df(df):
    daily_registered_rent_df = df.groupby(by='dateday').agg({
        'registered': 'sum'
    }).reset_index()
    return daily_registered_rent_df

def create_season_rent_df(df):
    season_rent_df = df.groupby(by='season')[['registered', 'casual']].sum().reset_index()
    return season_rent_df

def create_monthly_rent_df(df):
    monthly_rent_df = df.groupby(by='month').agg({
        'count': 'sum'
    })
    ordered_months = [
        'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
        'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
    ]
    monthly_rent_df = monthly_rent_df.reindex(ordered_months, fill_value=0)
    return monthly_rent_df

def create_weekday_rent_df(df):
    weekday_rent_df = df.groupby(by='weekday').agg({
        'count': 'sum'
    }).reset_index()
    return weekday_rent_df

def create_workingday_rent_df(df):
    workingday_rent_df = df.groupby(by='workingday').agg({
        'count': 'sum'
    }).reset_index()
    return workingday_rent_df

def create_holiday_rent_df(df):
    holiday_rent_df = df.groupby(by='holiday').agg({
        'count': 'sum'
    }).reset_index()
    return holiday_rent_df

def create_weather_rent_df(df):
    weather_rent_df = df.groupby(by='weathersit').agg({
        'count': 'sum'
    })
    return weather_rent_df

min_date = pd.to_datetime(df_hari['dateday']).dt.date.min()
max_date = pd.to_datetime(df_hari['dateday']).dt.date.max()

with st.sidebar:
    st.image(
        'streamlit-dashboard/bike.jpeg')

    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Time Span',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = df_hari[(df_hari['dateday'] >= str(start_date)) &
                 (df_hari['dateday'] <= str(end_date))]

daily_rent_df = create_daily_rent_df(main_df)
daily_casual_rent_df = create_daily_casual_rent_df(main_df)
daily_registered_rent_df = create_daily_registered_rent_df(main_df)
season_rent_df = create_season_rent_df(main_df)
monthly_rent_df = create_monthly_rent_df(main_df)
weekday_rent_df = create_weekday_rent_df(main_df)
workingday_rent_df = create_workingday_rent_df(main_df)
holiday_rent_df = create_holiday_rent_df(main_df)
weather_rent_df = create_weather_rent_df(main_df)

# Exploratory Data Analysis
monthly_counts = df_hari.groupby(by=["month","year"]).agg({
    "count": "sum"
}).reset_index()

# Visualization
st.title('Bike Rental Analysis')

st.subheader('Daily Rentals')
col1, col2, col3 = st.columns(3)

with col1:
    daily_rent_casual = daily_casual_rent_df['casual'].sum()
    st.metric('Casual User', value=daily_rent_casual)

with col2:
    daily_rent_registered = daily_registered_rent_df['registered'].sum()
    st.metric('Registered User', value=daily_rent_registered)

with col3:
    daily_rent_total = daily_rent_df['count'].sum()
    st.metric('Total User', value=daily_rent_total)

st.subheader('Total number of bicycles rented by Month and Year')
fig = px.line(
    monthly_counts,
    x="month",
    y="count",
    color="year",
    title="Total number of bicycles rented by Month and Year"
)
st.plotly_chart(fig)

st.subheader('Monthly Rentals')
fig, ax = plt.subplots(figsize=(24, 8))
ax.plot(
    monthly_rent_df.index,
    monthly_rent_df['count'],
    marker='o',
    linewidth=2,
    color='tab:blue'
)

for index, row in enumerate(monthly_rent_df['count']):
    ax.text(index, row + 1, str(row), ha='center', va='bottom', fontsize=12)

ax.tick_params(axis='x', labelsize=25, rotation=45)
ax.tick_params(axis='y', labelsize=20)
st.pyplot(fig)

st.subheader('Scatter plot of Temperature and Humidity vs Total Bike Users')
fig, ax = plt.subplots(figsize=(10, 5))

# Scatter plot for 'temp' vs 'count'
sns.scatterplot(
    x='temp',
    y='count',
    data=df_hari,
    alpha=0.5,
    ax=ax
)
ax.set_title('Temperature vs Total Bike Users')

# Scatter plot for 'hum' vs 'count'
fig, ax = plt.subplots(figsize=(10, 5))
sns.scatterplot(
    x='hum',
    y='count',
    data=df_hari,
    alpha=0.5,
    ax=ax
)
ax.set_title('Humidity vs Total Bike Users')

st.pyplot(fig)

# Scatter plot for 'hum' vs 'count'
fig, ax = plt.subplots(figsize=(10, 5))
sns.scatterplot(
    x='temp',
    y='count',
    data=df_hari,
    alpha=0.5,
    ax=ax
)
ax.set_title('Temperature vs Total Bike Users')

st.pyplot(fig)

st.write("""
## Conclusion
- From the scatter plot, it can be concluded that temperature (temp) has a positive correlation with count, indicating that as the temperature increases, the number of bike users also tends to increase. Conversely, humidity (hum) has a negative correlation with count, although not significant, it can still decrease the number of bike users when humidity increases.
- The line chart shows differences in peak months between 2011 and 2012. The peak for 2011 occurred in June, while for 2012, it was in September. Additionally, the line plot indicates that the total number of bikes rented in 2012 is consistently higher compared to 2011.
""")

st.caption('Copyright (c) Hammam Prasetyo')
