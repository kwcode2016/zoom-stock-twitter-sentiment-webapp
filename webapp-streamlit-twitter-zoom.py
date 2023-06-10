import streamlit as st
import pandas as pd
import altair as alt
import datetime





st.set_page_config(page_title='Zoom Stock Twitter Analysis')




default_start_date = datetime.date(2019, 4, 1)
default_end_date = datetime.date(2022, 12, 30)

start_date = st.sidebar.date_input("Start Date", default_start_date)
end_date = st.sidebar.date_input("End Date", default_end_date)


st.title("Zoom Stock Prices with Twitter Sentiment Analysis")


st.write("Stock Price Chart")



@st.cache_data
def get_data():
    source = pd.read_csv('zoom-stock-prices-2019-04-01-2022-12-11.csv')
    return source


zm_stock_df = get_data()


zm_date_close = zm_stock_df[['Date', 'Close']]


zm_date_close['Date'] = pd.to_datetime(zm_date_close['Date'])
print(zm_date_close.info())


zm_date_close = zm_date_close[(zm_date_close['Date'] >= pd.to_datetime(start_date)) & (zm_date_close['Date'] <= pd.to_datetime(end_date))]



zm_price_chart = alt.Chart(zm_date_close).mark_line().encode(
    x='Date',
    y='Close'
).properties( 
    height=400,
    width=800
    )


# zm_price_chart



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

import altair as alt
import pandas as pd


# Create an Altair Chart from the DataFrame
zm_positive_chart = alt.Chart(daily_sum).mark_line(color='green').encode(
    # x='yearmonth(date):O',
    x='date',
    # y='sum(positive)',
    y='positive',
).properties(
    width=800,
    height=400
)


zm_negative_chart = alt.Chart(daily_sum).mark_line(color='red').encode(
    x='date',
    # x='yearmonth(date):O',
    # y='negative',
    # y='sum(negative)',
    y='negative',
).properties(
    width=800,
    height=400
)

zm_neutral_chart = alt.Chart(daily_sum).mark_line(color='grey').encode(
    x='date',
    # x='yearmonth(date):O',
    # y='neutral',
    # y='sum(neutral)',
    y='neutral',
).properties(
    width=800,
    height=400
)


# zm_positive_chart + zm_negative_chart + zm_neutral_chart




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
plt.title("Sentiment Scores over Time")
plt.xlabel("Date")
plt.ylabel("Num of Tweets")

st.pyplot(plt)






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
ax1.set_title("Sentiment Scores and Price over Time")
ax1.set_xlabel("Date")
ax1.set_ylabel("Score")
ax2.set_ylabel("Price")


st.pyplot(plt)



