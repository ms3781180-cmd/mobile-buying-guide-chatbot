import os
import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

# Load environment variables
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

# Page configuration
st.set_page_config(
    page_title="MobileMatch AI",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Custom UI styling
st.markdown("""
<style>
    .stApp {
        background:
            radial-gradient(circle at 10% 10%, #34228a 0%, transparent 35%),
            radial-gradient(circle at 90% 90%, #005e70 0%, transparent 35%),
            linear-gradient(135deg, #0a1023, #131c38);
        color: #f8fafc;
    }

    .block-container {
        max-width: 980px;
        padding-top: 2.5rem;
        padding-bottom: 3rem;
    }

    .hero-card {
        padding: 2.2rem;
        text-align: center;
        border-radius: 24px;
        background: rgba(255, 255, 255, 0.10);
        border: 1px solid rgba(255, 255, 255, 0.18);
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.28);
        backdrop-filter: blur(12px);
        margin-bottom: 1.5rem;
    }

    .hero-title {
        font-size: 2.6rem;
        font-weight: 800;
        margin-bottom: 0.4rem;
        background: linear-gradient(90deg, #ffffff, #8ce7ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .hero-subtitle {
        color: #d3ddf3;
        font-size: 1.05rem;
        margin-bottom: 0;
    }

    .feature-card {
        background: rgba(255, 255, 255, 0.09);
        border: 1px solid rgba(255, 255, 255, 0.14);
        border-radius: 18px;
        padding: 1.1rem;
        text-align: center;
        min-height: 120px;
    }

    .feature-card h4 {
        margin: 0.25rem 0;
        color: #ffffff;
    }

    .feature-card p {
        color: #cbd5e1;
        font-size: 0.88rem;
        margin: 0;
    }

    div[data-testid="stTextArea"] textarea {
        background: rgba(255, 255, 255, 0.95);
        color: #111827;
        border-radius: 14px;
        border: 2px solid transparent;
        padding: 0.9rem;
        font-size: 1rem;
    }

    div[data-testid="stTextArea"] textarea:focus {
        border-color: #58d9ff;
        box-shadow: 0 0 0 3px rgba(88, 217, 255, 0.2);
    }

    .stButton > button {
        width: 100%;
        border: none;
        border-radius: 14px;
        padding: 0.8rem;
        font-size: 1.05rem;
        font-weight: 700;
        color: #07111f;
        background: linear-gradient(90deg, #5ee7ff, #7d9cff);
        transition: all 0.2s ease;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(94, 231, 255, 0.28);
    }

    .answer-card {
        background: rgba(255, 255, 255, 0.96);
        color: #172033;
        padding: 1.6rem;
        border-radius: 18px;
        margin-top: 1.4rem;
        box-shadow: 0 12px 32px rgba(0, 0, 0, 0.22);
    }

    .footer-text {
        text-align: center;
        color: #aab8d3;
        font-size: 0.85rem;
        padding-top: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# Hero section
st.markdown("""
<div class="hero-card">
    <div class="hero-title">📱 MobileMatch AI</div>
    <p class="hero-subtitle">
        Your smart companion for finding the right phone for your budget and lifestyle ✨
    </p>
</div>
""", unsafe_allow_html=True)

# Feature cards
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-card">
        <div style="font-size: 2rem;">📸</div>
        <h4>Camera</h4>
        <p>Find phones for photos, videos, and social media.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <div style="font-size: 2rem;">🎮</div>
        <h4>Gaming</h4>
        <p>Compare performance, cooling, display, and battery.</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
        <div style="font-size: 2rem;">💰</div>
        <h4>Budget</h4>
        <p>Get recommendations that fit your price range.</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# API key validation
if not groq_api_key:
    st.error("❌ GROQ_API_KEY not found. Please add it to your `.env` file.")
    st.stop()

# User question
question = st.text_area(
    "🔍 What phone are you looking for?",
    placeholder="Example: Recommend a phone under ₹30,000 with a great camera and good gaming performance.",
    height=150,
)

if st.button("✨ Find My Perfect Phone"):

    if not question.strip():
        st.warning("⚠️ Please enter a mobile-related question first.")
        st.stop()

    llm = ChatGroq(
        groq_api_key=groq_api_key,
        model="llama-3.1-8b-instant",
        temperature=0.3,
    )

    prompt = ChatPromptTemplate.from_template("""
You are an expert mobile phone buying guide assistant. 📱

Answer ONLY questions related to smartphones, mobile accessories, phone comparisons,
camera quality, gaming, battery life, display, storage, processors, 5G, Android,
iPhones, and phone-buying advice.

If the question is NOT related to mobile phones, reply exactly:

Sorry, I only answer mobile phone buying guide questions. 📱

Question:
{question}

Use this format:

### 📱 Best Recommendation
Give a direct recommendation.

### ✨ Why It Fits Your Needs
- Point 1
- Point 2
- Point 3

### 🔍 Important Specifications
- Processor:
- Camera:
- Battery:
- Display:
- Storage/RAM:

### 💡 Buying Tips
- Point 1
- Point 2

### ⚠️ Note
Mention that prices, availability, and specifications can vary if relevant.
""")

    chain = prompt | llm

    with st.spinner("Searching for the best match... 📱✨"):
        try:
            response = chain.invoke({"question": question})

            st.markdown("""
            <div class="answer-card">
                <h2 style="margin-top: 0;">🤖 Your Mobile Guide</h2>
            """, unsafe_allow_html=True)

            st.markdown(response.content)
            st.markdown("</div>", unsafe_allow_html=True)

        except Exception as e:
            st.error(f"❌ Something went wrong: {e}")

st.markdown("""
<p class="footer-text">
    📱 MobileMatch AI • Compare smarter, buy better ✨
</p>
""", unsafe_allow_html=True)