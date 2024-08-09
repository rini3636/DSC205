import pandas as pd
from datetime import datetime
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import folium
import streamlit as st

st.title('Data 205 Final')
st.subheader('Carina Andrea')

#Create dataframe, make dates index for temporal stuff later
df = pd.read_csv('https://storage.googleapis.com/scsu-data-science/bike_sharing.csv',
                 parse_dates=True,
                 index_col='dteday')


##Part 1: Line graph of riders over time
st.header('Part 1:')
#make plot
fig1 = plt.figure(figsize=(10, 6))
ax1 = fig1.add_subplot()
ax1.plot(df.index, df['cnt'], label='Share Riders Over Time', linewidth = 2)

#label plot
ax1.set_title('Share Riders Over Time')
ax1.set_xlabel('Date')
ax1.set_ylabel('Number of riders')

# Define date format
date_form = DateFormatter('%m-%y')
ax1.xaxis.set_major_formatter(date_form)

#Render to streamlit
st.pyplot(fig1)

##Part 2: Bar plot of riders by season
st.header('Part 2')
#Change numbers to actual names of seasons
df['season'].replace({1:'Winter', 2:'Spring', 3:'Summer', 4:'Fall'}, inplace=True)
#Create grouping
by_season = df['cnt'].groupby(df['season']).sum()
#Title Chart
st.subheader('Total Riders by Season')
#Render chart
st.bar_chart(by_season, x_label='Season', y_label='Total Riders', horizontal=True)

#Put things back because it caused an error later
df['season'].replace({'Winter':1, 'Spring':2, 'Summer':3, 'Fall':4}, inplace=True)

##Part 3: Interactive line graph
st.header('Part 3')
#Create radio button to get rolling average period
with st.form(key='my_form1'):
    choice = st.radio('Select a time period for the rolling average calculation:',
                      ('7 days', '14 days'))
    submitted = st.form_submit_button(label='Submit')
if submitted:
    if choice == '7 days':
        period = 7
    else:
        period = 14
    #Compute average
    rolling = df.rolling(period, center=True).mean()
    
    #make plot
    fig2 = plt.figure(figsize=(10, 6))
    ax2 = fig2.add_subplot()
    ax2.plot(rolling.index, rolling['cnt'], label='Average Share Riders', linewidth = 2)

    #label plot
    ax2.set_title('Daily Share Riders')
    ax2.set_xlabel('Date')
    ax2.set_ylabel('Number of riders')

    # Define date format
    date_form = DateFormatter('%m-%y')
    ax2.xaxis.set_major_formatter(date_form)

    #Render to streamlit
    st.pyplot(fig2)