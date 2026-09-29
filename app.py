import pandas as pd
import streamlit as st
import plotly.express as px
from src.nlp_processor import clean_text, vectorizer, model
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

try:
    nltk.data.find('sentiment/vader_lexicon.zip')
except LookupError:
    nltk.download('vader_lexicon')

sia = SentimentIntensityAnalyzer()

file = pd.read_csv("data/processed_reviews.csv")

st.title("Spotify Reviews Sentiment Analysis")
st.write("This app analyzes Spotify reviews and classifies them into Positive, Neutral, or Negative sentiments based on the review text.")  

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="Total Reviews", value=len(file))
with col2:
    st.metric(label="Negative Reviews", value=f"{(len(file[file['True_Label'] == 'Negative']) / len(file) * 100):.2f}%")
with col3:
    st.metric(label="Average Rating", value=file["Rating"].mean())

rating_counts = file["Rating"].value_counts().reset_index()
rating_counts.columns = ["Rating", "Count"]

fig = px.bar(rating_counts, x="Rating", y="Count", title="Distribution of Reviews by Rating")

fig2 = px.pie(file, names = "ML_Predicted_Label", title = "Sentiment Distribution of Reviews")

st.plotly_chart(fig)
st.plotly_chart(fig2)
st.dataframe(file)

st.subheader("Try it out!")
user_input = st.text_input("Enter your review here:")

if st.button("Analyze Sentiment"):
    if user_input:

        scores = sia.polarity_scores(user_input)
        compound = scores['compound']

        if compound >= 0.05:
            final_prediction = "Positive"
        elif compound <= -0.05:
            final_prediction = "Negative"
        else:
            final_prediction = "Neutral"

        if final_prediction == "Positive":
            st.success(f"Result: {final_prediction} 😄")
        elif final_prediction == "Neutral":
            st.info(f"Result: {final_prediction} 😐")
        else:
            st.error(f"Result: {final_prediction} 😞")

        st.write(f"Compound Score: {compound:.2f}")
    else:
        st.write("Please enter a review to analyze.")

