import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
from textblob import TextBlob
import openai
import os
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Extract YouTube video ID from URL
def extract_video_id(url):
    if "v=" in url:
        return url.split("v=")[1].split("&")[0]
    elif "youtu.be/" in url:
        return url.split("youtu.be/")[1].split("?")[0]
    return None

# Fetch transcript using YouTubeTranscriptApi
def get_transcript(video_id):
    transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
    full_text = " ".join([d["text"] for d in transcript_list])
    return full_text

# Summarize text using OpenAI GPT
def summarize_text(text):
    response = openai.ChatCompletion.create(  # Fixed: ChatCompletion not chatcompletion
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Summarize the following YouTube transcript."},
            {"role": "user", "content": text}
        ],
        max_tokens=300,
        temperature=0.7
    )
    return response["choices"][0]["message"]["content"].strip()

# Sentiment analysis using TextBlob
def get_sentiment(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    if polarity > 0.1:
        return "Positive"
    elif polarity < -0.1:
        return "Negative"
    else:
        return "Neutral"

# Streamlit app UI
st.title("🎬 YouTube Video Summarizer with Sentiment Analysis")

video_url = st.text_input("Enter YouTube Video URL:")
if video_url:
    try:
        video_id = extract_video_id(video_url)
        transcript = get_transcript(video_id)

        with st.spinner("Summarizing..."):
            summary = summarize_text(transcript)

        sentiment = get_sentiment(transcript)

        st.subheader("📄 Summary")
        st.write(summary)

        st.subheader("🧠 Sentiment")
        st.write(sentiment)

    except Exception as e:
        st.error(f"Error: {e}")
else:
    st.warning("Please enter a valid URL.")
