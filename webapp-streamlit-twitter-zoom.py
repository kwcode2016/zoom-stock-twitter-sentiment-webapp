import streamlit as st
import pandas as pd
import altair as alt


# creating the side bar
# status_text = st.sidebar.empty()

# st.sidebar.markdown("""# hello sidebar
# some things will go here

#                     """)


st.set_page_config(page_title='Zoom Stock Twitter Analysis')



# st.sidebar.write('turn on each chart check marks')
# st.sidebar.write('[ ] Zoom Stock Price')
# st.sidebar.write('[ ] Positive sentiment [blue box]')
# st.sidebar.write('[ ] Neutral Sentiment Tweets [grey box]')
# st.sidebar.write('[ ] Negative Sentiment Tweets [red box]')
# st.sidebar.write('date slider')

start_date = st.sidebar.date_input("Start Date")
end_date = st.sidebar.date_input("End Date")


st.title("Zoom Stock Prices with Twitter Sentiment Analysis")


st.write("Stock Price Chart")
st.write(start_date)
st.write(end_date)


@st.cache_data
def get_data():
    source = pd.read_csv('zoom-stock-prices-2019-04-01-2022-12-11.csv')
    return source


zm_stock_df = get_data()


zm_date_close = zm_stock_df[['Date', 'Close']]


zm_date_close['Date'] = pd.to_datetime(zm_date_close['Date'])
print(zm_date_close.info())

# zoom close price
# zm_date_close

zm_price_chart = alt.Chart(zm_date_close).mark_line().encode(
    x='Date',
    y='Close'
).properties( 
    height=700,
    width=700
    ).interactive()


zm_price_chart








# chart with finetuning
zm_tweet_sentiment_df = pd.read_csv('full300k_w_r_latest_sentiment_with_finetuning.csv')
# zm_tweet_sentiment_df[['date','sentiment_r_latest']]

zm_tweet_sentiment_df['date'] = pd.to_datetime(zm_tweet_sentiment_df['date'])

daily_sum = zm_tweet_sentiment_df.groupby([zm_tweet_sentiment_df['date'].dt.date, 'sentiment_r_latest'])['sentiment_r_latest'].count()

daily_sum = daily_sum.unstack(fill_value=0)
daily_sum.reset_index(level=0, inplace=True) # date column was not flat and cannot be accessed - this flattens all columns
# st.write(daily_sum.columns)
st.write("uncomment to see daily_sum df")
# daily_sum



import altair as alt
import pandas as pd



# Convert the 'date' column to string format for Altair
# daily_sum['date'] = daily_sum['date'].astype(str)

# Create an Altair Chart from the DataFrame
zm_positive_chart = alt.Chart(daily_sum).mark_line(color='green').encode(
    x='yearmonth(date):O',
    y='sum(positive)',
).properties(
    width=800,
    height=400
).interactive()


zm_negative_chart = alt.Chart(daily_sum).mark_line(color='red').encode(
    # x='date',
    x='yearmonth(date):O',
    # y='negative',
    y='sum(negative)',
).properties(
    width=800,
    height=400
).interactive()

zm_neutral_chart = alt.Chart(daily_sum).mark_line(color='grey').encode(
    # x='date',
    x='yearmonth(date):O',
    # y='neutral',
    y='sum(neutral)',
).properties(
    width=800,
    height=400
).interactive()


zm_positive_chart + zm_negative_chart + zm_neutral_chart




