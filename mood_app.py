import sys
try:
    import pkg_resources
except ImportError:
    import pip._vendor.pkg_resources as pkg_resources
    sys.modules["pkg_resources"] = pkg_resources

import streamlit as st
from fer import FER  # Isse wapas 'from fer import FER' kar dein
from PIL import Image
import numpy as np
import streamlit as st
from fer.fer import FER
from PIL import Image


# 1. Page Configuration
st.set_page_config(page_title="Suga's Mood Scanner", page_icon="📸")

st.title("📸 Suga's Mood Scanner")
st.write("Take a photo, and I'll tell you how you're feeling!")

# 2. Load the Emotion Detector (The AI Brain)
@st.cache_resource
def load_detector():
    # 'mtcnn=True' makes it more accurate but requires the mtcnn library
    detector = FER(mtcnn=True) 
    return detector

try:
    detector = load_detector()
except Exception as e:
    st.error("Error loading the face detector. Make sure you installed mtcnn!")
    st.error(f"Details: {e}")
    st.stop()

# 3. The Webcam Input
img_file_buffer = st.camera_input("Smile for the camera!")

if img_file_buffer is not None:
    # Convert the file to an image
    image = Image.open(img_file_buffer)
    img_array = np.array(image) # Convert to a number array for the AI

    # 4. Detect Emotions
    # The detector looks at the image and finds faces + emotions
    result = detector.detect_emotions(img_array)

    if result:
        # Get the top emotion
        emotions = result[0]['emotions']
        dominant_emotion = max(emotions, key=emotions.get)
        score = emotions[dominant_emotion]

        # 5. Display the Result
        st.header(f"You look: **{dominant_emotion.upper()}** 😲")
        st.progress(score) # Show a bar for how confident the AI is
        
        # Show all probabilities
        st.write("Detailed Analysis:")
        st.json(emotions)
    else:

        st.warning("No face detected! Try moving closer to the camera or checking the lighting.")

