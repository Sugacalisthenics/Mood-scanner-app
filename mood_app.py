import sys
import subprocess
try:
    import pkg_resources
except ImportError:
    try:
        import setuptools
        import pkg_resources
    except ImportError:
        # Final attempt to bypass the error in Python 3.13
        from types import ModuleType
        mock_pkg = ModuleType("pkg_resources")
        sys.modules["pkg_resources"] = mock_pkg

import streamlit as st
from fer.fer import FER
from PIL import Image
import numpy as np

# 1. Page Configuration
st.set_page_config(page_title="Suga's Mood Scanner", page_icon="📸")

st.title("📸 Suga's Mood Scanner")
st.write("Take a photo, and I'll tell you how you're feeling!")

# 2. Load the Emotion Detector
@st.cache_resource
def load_detector():
    # mtcnn=False is faster and uses less memory on free servers
    return FER(mtcnn=False) 

try:
    detector = load_detector()
except Exception as e:
    st.error(f"AI loading error: {e}")
    st.stop()

# 3. The Webcam Input
img_file_buffer = st.camera_input("Smile for the camera!")

if img_file_buffer is not None:
    image = Image.open(img_file_buffer)
    img_array = np.array(image)

    # 4. Detect Emotions
    result = detector.detect_emotions(img_array)

    if result:
        emotions = result[0]['emotions']
        dominant_emotion = max(emotions, key=emotions.get)
        score = emotions[dominant_emotion]

        st.header(f"You look: **{dominant_emotion.upper()}** 😲")
        st.progress(float(score))
        
        st.write("Detailed Analysis:")
        st.json(emotions)
    else:
        st.warning("No face detected! Try moving closer.")


