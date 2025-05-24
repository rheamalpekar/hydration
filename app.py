import streamlit as st
import time
import base64

st.set_page_config(page_title="💧 Water Reminder", layout="centered")

# Optional circular slider
try:
    from streamlit_circular_slider import circular_slider_available, circular_slider
    use_circular_slider = circular_slider_available
except ImportError:
    use_circular_slider = False

# --- Custom Styling for Water Theme ---
st.markdown("""
    <style>
    body {
        background: linear-gradient(135deg, #74ebd5 0%, #ACB6E5 100%) !important;
    }
    html, body, [class*="css"] {
        font-size: 22px !important;
        text-align: center !important;
        color: #ffffff !important;
    }
    h1 {
        font-size: 48px !important;
        margin-bottom: 20px;
        color: #ffffff !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    h2.timer {
        font-size: 72px !important;
        font-weight: 900;
        color: #00E0FF !important;
        margin-top: 10px;
    }
    .stButton>button {
        font-size: 24px !important;
        padding: 0.75em 2em !important;
        background-color: #00B4D8 !important;
        color: white !important;
        border: none;
        border-radius: 10px;
    }
    .stButton>button:hover {
        background-color: #0077b6 !important;
    }
    .stSlider>div>div {
        color: #ffffff !important;
    }
    .stCheckbox>label, .stSlider>label {
        font-size: 22px !important;
        color: #ffffff !important;
    }
    .stProgress>div>div>div {
        background-color: #00E0FF !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("💧 Water Reminder")

# Load audio safely
def get_audio_base64(file_path):
    try:
        with open(file_path, "rb") as audio_file:
            return base64.b64encode(audio_file.read()).decode()
    except FileNotFoundError:
        st.error("⚠️ Audio file 'notification.mp3' not found.")
        return None

# Time selection with optional circular sliders
st.markdown("### Set Timer Duration")

if use_circular_slider:
    minutes = circular_slider("Minutes", min_value=0, max_value=59, step=1, value=1)
    seconds = circular_slider("Seconds", min_value=0, max_value=59, step=1, value=0)
else:
    col1, col2 = st.columns(2)
    with col1:
        minutes = st.slider("Minutes", 0, 59, 1)
    with col2:
        seconds = st.slider("Seconds", 0, 59, 0)

total_seconds = minutes * 60 + seconds

# Repeating options
repeat_reminder = st.checkbox("🔁 Repeat every X minutes?")
if repeat_reminder:
    repeat_interval = st.slider("Repeat interval (minutes)", 1, 60, 15)

on_repeat = st.checkbox("🔁 On-Repeat (Auto-Restart Timer)")

# Timer Function
def run_timer(duration):
    st.markdown("### ⏱️ Time Remaining")
    time_placeholder = st.empty()
    progress_bar = st.progress(0)

    for remaining in range(duration, -1, -1):
        m, s = divmod(remaining, 60)
        time_placeholder.markdown(
            f"<h2 class='timer'>{m:02d}:{s:02d}</h2>",
            unsafe_allow_html=True,
        )
        progress_bar.progress((duration - remaining) / duration)
        time.sleep(1)

    st.balloons()
    st.success("🔔 Time to drink water!")

    audio_base64 = get_audio_base64("notification.mp3")
    if audio_base64:
        st.markdown(f"""
            <audio autoplay>
                <source src="data:audio/mpeg;base64,{audio_base64}" type="audio/mpeg">
            </audio>
        """, unsafe_allow_html=True)

# Start Reminder Button
if st.button("Start Reminder"):
    if total_seconds == 0:
        st.warning("⏱️ Set a time greater than 0.")
    else:
        if on_repeat:
            while True:
                run_timer(total_seconds)
        elif repeat_reminder:
            while True:
                run_timer(total_seconds)
                time.sleep(repeat_interval * 60)
        else:
            run_timer(total_seconds)

