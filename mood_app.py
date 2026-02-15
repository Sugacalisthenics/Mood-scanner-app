import sys
import os
from types import ModuleType
import fer  # Pehle import karein taaki rasta pata chale

# --- STEP 1: SMART PATH HACK ---
try:
    import pkg_resources
except ImportError:
    # Creating a mock that actually finds the library's folder
    mock_pkg = ModuleType("pkg_resources")
    
    def resource_filename(package_or_requirement, resource_name):
        # Yeh line fer library ke asli folder ka rasta nikaalti hai
        base_path = os.path.dirname(fer.__file__)
        return os.path.join(base_path, resource_name)
    
    mock_pkg.resource_filename = resource_filename
    sys.modules["pkg_resources"] = mock_pkg

# --- STEP 2: REST OF THE IMPORTS ---
import streamlit as st
from fer.fer import FER
from PIL import Image
import numpy as np

# --- STEP 3: APP LOGIC ---
st.set_page_config(page_title="Suga's Mood Scanner", page_icon="📸")
st.title("📸 Suga's Mood Scanner")

@st.cache_resource
def load_detector():
    # mtcnn=False memory bachata hai
    return FER(mtcnn=False) 

try:
    detector = load_detector()
except Exception as e:
    st.error(f"AI Brain Error: {e}")
    st.info("Check: Settings mein Python version 3.11 select karein.")
    st.stop()

# Camera input and analysis logic
img_file_buffer = st.camera_input("Smile for Suga!")
if img_file_buffer is not None:
    image = Image.open(img_file_buffer)
    img_array = np.array(image)
    result = detector.detect_emotions(img_array)

    if result:
        emotions = result[0]['emotions']
        dominant = max(emotions, key=emotions.get)
        st.header(f"You look: {dominant.upper()}!")
        st.json(emotions)
    else:
        st.warning("Face detect nahi hua!")
