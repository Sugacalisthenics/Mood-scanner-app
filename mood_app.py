import sys
import os
from types import ModuleType

# --- STEP 1: PYTHON 3.13 COMPATIBILITY HACK ---
try:
    import pkg_resources
except ImportError:
    mock_pkg = ModuleType("pkg_resources")
    def resource_filename(package_or_requirement, resource_name):
        return os.path.abspath(resource_name)
    mock_pkg.resource_filename = resource_filename
    sys.modules["pkg_resources"] = mock_pkg

# --- STEP 2: IMPORTS ---
import streamlit as st
from fer.fer import FER
from PIL import Image
import numpy as np

# --- STEP 3: APP UI ---
st.set_page_config(page_title="Suga's Mood Scanner", page_icon="📸")

st.title("📸 Suga's Mood Scanner")
st.write("Take a photo, and I'll tell you how you're feeling!")

@st.cache_resource
def load_detector():
    return FER(mtcnn=False) 

try:
    detector = load_detector()
except Exception as e:
    st.error(f"AI Loading Error: {e}")
    st.stop()

# --- STEP 4: CAMERA ---
img_file_buffer = st.camera_input("Smile for the camera!")

if img_file_buffer is not None:
    image = Image.open(img_file_buffer)
    img_array = np.array(image)

    with st.spinner('Analyzing your mood...'):
        result = detector.detect_emotions(img_array)

    if result:
        emotions = result[0]['emotions']
        dominant_emotion = max(emotions, key=emotions.get)
        score = emotions[dominant_emotion]

        st.divider()
        st.header(f"You look: **{dominant_emotion.upper()}** 😲")
        st.progress(float(score))
        st.write(f"Confidence: {int(score * 100)}%")
        
        with st.expander("Detailed breakdown"):
            st.json(emotions)
            
        if dominant_emotion == "happy":
            st.balloons()
    else:
        st.warning("Face detect nahi hua! Thoda paas aaiye.")

st.markdown("---")
st.caption("Built with ❤️ by Suga | Powered by FER & Streamlit")
