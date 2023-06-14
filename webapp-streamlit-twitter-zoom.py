# Summary: Webapp that displays the Zoom Stock price and the Positive and Negative daily Sentiments
# Entering the start and end date will update the Graphs to those dates allowing for better analysis

# The conva env list is listed in requirements.txt


import streamlit as st
import pandas as pd
import altair as alt
import datetime



st.set_page_config(page_title='Zoom Stock Twitter Analysis')


default_start_date = datetime.date(2019, 4, 1)
default_end_date = datetime.date(2022, 12, 30)

st.sidebar.markdown('## Instructions')
st.sidebar.markdown("Enter new dates in the Start Date and End Date fields and the chart will automatically update.")
st.sidebar.markdown("Please note that the dates must range between April 1 2019 and Dec 30 2022")
st.sidebar.markdown("---")
start_date = st.sidebar.date_input("Start Date", default_start_date)
end_date = st.sidebar.date_input("End Date", default_end_date)



st.title("Zoom Twitter Sentiment vs Stock Prices Analysis")

st.markdown('---')
st.markdown('## Seperated Stock Price and Twitter Daily Count Charts')
st.markdown('Use these charts to spot interesting date ranges to explore.')


@st.cache_data
def get_data():
    source = pd.read_csv('zoom-stock-prices-2019-04-01-2022-12-11.csv')
    return source


zm_stock_df = get_data()


zm_date_close = zm_stock_df[['Date', 'Close']]


zm_date_close['Date'] = pd.to_datetime(zm_date_close['Date'])
print(zm_date_close.info())


zm_date_close = zm_date_close[(zm_date_close['Date'] >= pd.to_datetime(start_date)) & (zm_date_close['Date'] <= pd.to_datetime(end_date))]


# using matplotlib
import matplotlib.pyplot as plt


plt.figure(figsize=(8, 5))
# Create the chart
plt.plot(zm_date_close['Date'], zm_date_close['Close'])

# Set the title
plt.title('Zoom Stock Price')

# Set the x-axis label
plt.xlabel('Date')

# Set the y-axis label
plt.ylabel('Price')
plt.xticks(rotation=45, ha='right')

# Display the chart
st.pyplot(plt)



# chart with finetuning
zm_tweet_sentiment_df = pd.read_csv('full300k_w_r_latest_sentiment_with_finetuning.csv')
zm_tweet_sentiment_df['date'] = pd.to_datetime(zm_tweet_sentiment_df['date'])
start_date = pd.to_datetime(start_date).tz_localize('UTC')
end_date = pd.to_datetime(end_date).tz_localize('UTC')
zm_tweet_sentiment_df = zm_tweet_sentiment_df[(zm_tweet_sentiment_df['date'] >= pd.to_datetime(start_date)) & (zm_tweet_sentiment_df['date'] <= pd.to_datetime(end_date))]

daily_sum = zm_tweet_sentiment_df.groupby([zm_tweet_sentiment_df['date'].dt.date, 'sentiment_r_latest'])['sentiment_r_latest'].count()
daily_sum = daily_sum.unstack(fill_value=0)
daily_sum.reset_index(level=0, inplace=True) # date column was not flat and cannot be accessed - this flattens all columns



# using matplotlib

# Convert the 'date' column to datetime format for Matplotlib
daily_sum['date'] = pd.to_datetime(daily_sum['date'])

# Create a new figure
# plt.figure(figsize=(10,6))
plt.figure(figsize=(8, 5))

# Plot the 'positive' line
plt.plot(daily_sum['date'], daily_sum['positive'], label='positive', color='green')

# Plot the 'negative' line
plt.plot(daily_sum['date'], daily_sum['negative'], label='negative', color='red')

# Plot the 'neutral' line
# plt.plot(daily_sum['date'], daily_sum['neutral'], label='neutral', color='grey')

# Add a legend
plt.legend()

# Set the title and labels
plt.title("Daily Positive and Negative Sentiment Counts over Time")
plt.xlabel("Date")
plt.xticks(rotation=45, ha='right')
plt.ylabel("Daily Sentiment Counts")

st.pyplot(plt)




st.markdown('---')
st.header('Combined Zoom Sentiment Stock Price Graph')
st.markdown('Analyze the data using the graph with the stock price overlayed with the daily Twitter sentiment counts.')

# trying to combine both charts

# Convert the 'date' and 'Date' columns to datetime format for Matplotlib
daily_sum['date'] = pd.to_datetime(daily_sum['date'])
zm_date_close['Date'] = pd.to_datetime(zm_date_close['Date'])

# Create a new figure
fig, ax1 = plt.subplots(figsize=(10,6))

# Plot the 'positive' line
ax1.plot(daily_sum['date'], daily_sum['positive'], label='positive', color='green')

# Plot the 'negative' line
ax1.plot(daily_sum['date'], daily_sum['negative'], label='negative', color='red')

# Plot the 'neutral' line
# ax1.plot(daily_sum['date'], daily_sum['neutral'], label='neutral', color='grey')

# Create a second y-axis
ax2 = ax1.twinx()

# Plot the price on the second y-axis
ax2.plot(zm_date_close['Date'], zm_date_close['Close'], label='price', color='blue')

# Add legends
ax1.legend(loc='upper left')
ax2.legend(loc='upper right')

# Set the title and labels
ax1.set_title("Daily Positive and Negative Twitter Sentiment + Price over Time")
ax1.set_xlabel("Date")

ax1.set_ylabel("Daily Sentiment Counts")
ax2.set_ylabel("Price")


plt.xticks(rotation=45, ha='right')

st.pyplot(plt)



