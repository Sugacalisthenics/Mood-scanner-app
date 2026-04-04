import os
import sys
import importlib.util
from types import ModuleType

try:
    os.system("pip uninstall -y opencv-python opencv-contrib-python")
except:
    pass

try:
    import pkg_resources
except ImportError:
    mock_pkg = ModuleType("pkg_resources")
    def resource_filename(package_or_requirement, resource_name):
        spec = importlib.util.find_spec(package_or_requirement)
        if spec and spec.submodule_search_locations:
            return os.path.join(spec.submodule_search_locations[0], resource_name)
        return os.path.join(os.getcwd(), resource_name)
    
    mock_pkg.resource_filename = resource_filename
    sys.modules["pkg_resources"] = mock_pkg

import streamlit as st
import cv2
from fer.fer import FER
from PIL import Image, ImageOps
import numpy as np

st.set_page_config(page_title="Suga's Mirror Mood Scanner", page_icon="📸")
st.title("📸 Suga's Mood Scanner (Mirror Mode)")

@st.cache_resource
def load_detector():
    return FER(mtcnn=True) 

try:
    detector = load_detector()
except Exception as e:
    st.error(f"AI Error: {e}")
    st.stop()

img_file_buffer = st.camera_input("Smile for the camera!")

if img_file_buffer is not None:
    image = Image.open(img_file_buffer)
    image = ImageOps.mirror(image)
    img_array = np.array(image)

    with st.spinner('Analyzing your mirrored mood...'):
        result = detector.detect_emotions(img_array)

    if result:
        emotions = result[0]['emotions']
        dominant = max(emotions, key=emotions.get)
        score = emotions[dominant]

        st.divider()
        st.header(f"You look: **{dominant.upper()}** 😲")
        st.progress(float(score))
        
        with st.expander("Detailed emotional breakdown"):
            st.json(emotions)
            
        if dominant == "happy":
            st.balloons()
    else:
        st.warning("Face detect nahi hua! Thoda paas aaiye aur light sahi rakhiye.")

st.markdown("---")
st.caption("Built with ❤️ by Suga ")
