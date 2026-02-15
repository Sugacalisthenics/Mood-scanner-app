import sys
from types import ModuleType

# This mocks 'pkg_resources' which was removed in Python 3.13 
# but is still required by the 'fer' library.
try:
    import pkg_resources
except ImportError:
    mock_pkg = ModuleType("pkg_resources")
    sys.modules["pkg_resources"] = mock_pkg

# --- STEP 2: IMPORTS ---
import streamlit as st
from fer.fer import FER  # Correct import for newer 'fer' versions
from PIL import Image
import numpy as np

# --- STEP 3: PAGE CONFIGURATION ---
st.set_page_config(page_title="Suga's Mood Scanner", page_icon="📸")

# Add some custom CSS for branding
st.markdown("""
    <style>
    .main {
        background-color: #f0f2f6;
    }
    .stButton>button {
        width: 100%;
        border-radius: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("📸 Suga's Mood Scanner")
st.write("Take a photo, and I'll tell you how you're feeling!")

# --- STEP 4: LOAD THE AI BRAIN ---
@st.cache_resource
def load_detector():
    # mtcnn=False uses a faster, lighter detector suitable for free hosting
    return FER(mtcnn=False) 

try:
    detector = load_detector()
except Exception as e:
    st.error(f"AI Loading Error: {e}")
    st.info("Check if requirements.txt includes 'tensorflow-cpu' and 'fer'.")
    st.stop()

# --- STEP 5: THE CAMERA INTERFACE ---
img_file_buffer = st.camera_input("Smile for the camera!")

if img_file_buffer is not None:
    # Processing the image
    image = Image.open(img_file_buffer)
    img_array = np.array(image)

    with st.spinner('Analyzing your mood...'):
        # Detect Emotions
        result = detector.detect_emotions(img_array)

    if result:
        # result is a list; we take the first face detected
        emotions = result[0]['emotions']
        
        # Finding the emotion with the highest score
        dominant_emotion = max(emotions, key=emotions.get)
        score = emotions[dominant_emotion]

        # Display Results
        st.divider()
        st.header(f"You look: **{dominant_emotion.upper()}** 😲")
        
        # Show a progress bar for confidence
        st.write(f"Confidence: {int(score * 100)}%")
        st.progress(float(score))
        
        # Detailed Data
        with st.expander("See Detailed Probability"):
            st.json(emotions)
            
        # Fun footer message
        if dominant_emotion == "happy":
            st.balloons()
            st.success("Keep that smile going!")
        elif dominant_emotion == "sad":
            st.info("Remember, Suga thinks you're awesome! Turn that frown upside down.")
            
    else:
        st.warning("No face detected! Try moving closer to the camera or checking the lighting.")

# --- STEP 6: FOOTER ---
st.markdown("---")
st.caption("Built with ❤️ by Suga | Powered by FER & Streamlit")
