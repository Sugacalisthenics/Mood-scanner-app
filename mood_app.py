import sys
import os
from types import ModuleType
import fer 

try:
    import pkg_resources
except ImportError:
    mock_pkg = ModuleType("pkg_resources")
    def resource_filename(package_or_requirement, resource_name):
        base_path = os.path.dirname(fer.__file__)
        return os.path.join(base_path, resource_name)
    mock_pkg.resource_filename = resource_filename
    sys.modules["pkg_resources"] = mock_pkg

# --- STEP 2: IMPORTS ---
import streamlit as st
from fer.fer import FER
from PIL import Image, ImageOps  # ImageOps mirror karne ke liye
import numpy as np

# --- STEP 3: APP CONFIG ---
st.set_page_config(page_title="Suga's Mirror Mood Scanner", page_icon="📸")
st.title("📸 Suga's Mood Scanner (Mirror Mode)")

# --- STEP 4: LOAD AI (MTCNN=True for better detection) ---
@st.cache_resource
def load_detector():
    # mtcnn=True se face detection zyada accurate hogi
    return FER(mtcnn=True) 

try:
    detector = load_detector()
except Exception as e:
    st.error(f"AI Error: {e}")
    st.stop()

# --- STEP 5: CAMERA INPUT ---
img_file_buffer = st.camera_input("Smile for the camera!")

if img_file_buffer is not None:
    # 1. Image ko open karein
    image = Image.open(img_file_buffer)
    
    # 2. MIRROR FIX: Image ko horizontally flip karein
    # Isse photo bilkul waisi dikhegi jaisi aapko screen par dikh rahi thi
    image = ImageOps.mirror(image)
    
    # 3. Convert to array for AI
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
st.caption("Built with ❤️ by Suga | Fixed Mirror View")
