import streamlit as st
import time
import base64

st.set_page_config(page_title="💧 Water Reminder", layout="centered")

# Custom CSS to center everything including text and inputs
st.markdown("""
    <style>
    .main {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
    }
    h1, h2, h3, h4, p, div, label {
        text-align: center !important;
        justify-content: center;
    }
    .stSlider, .stButton, .stNumberInput, .stMarkdown {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }
    </style>
""", unsafe_allow_html=True)

# Load and encode the audio file
def get_audio_base64(file_path):
    with open(file_path, "rb") as audio_file:
        return base64.b64encode(audio_file.read()).decode()

st.title("💧 Water Drinking Reminder")

# Timer inputs
col1, col2 = st.columns(2)
with col1:
    minutes = st.slider("Minutes", 0, 59, 1, key="minutes_slider")

with col2:
    seconds = st.slider("Seconds", 0, 59, 0, key="seconds_slider")

total_seconds = minutes * 60 + seconds

if st.button("Start Reminder"):
    if total_seconds == 0:
        st.warning("⏱️ Set a time greater than 0.")
    else:
        st.markdown("### ⏱️ Time Remaining")
        placeholder = st.empty()
        for remaining in range(total_seconds, -1, -1):
            m, s = divmod(remaining, 60)
            placeholder.markdown(
                f"<h2 style='text-align:center;'>{m:02d}:{s:02d}</h2>",
                unsafe_allow_html=True,
            )
            time.sleep(1)

        # Show reminder and play sound
        st.balloons()
        st.success("🔔 Time to drink water!")

        audio_base64 = get_audio_base64("notification.mp3")
        st.markdown(f"""
            <audio autoplay>
                <source src="data:audio/mpeg;base64,{audio_base64}" type="audio/mpeg">
            </audio>
        """, unsafe_allow_html=True)
