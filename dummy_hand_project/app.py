import streamlit as st
from PIL import Image
from pathlib import Path
import time

# --- PAGE CONFIG ---
st.set_page_config(page_title="Chakra Visualiser", layout="centered")

# --- TITLE & INTRO ---
st.title("🌀 Inner Universe")
st.subheader("Real-time gesture-activated chakra feedback")

st.write("""
Welcome!  
This app lets you raise different hand gestures to activate and visualise your chakras
— complete with colours, sounds, and live feedback.
""")

# --- BANNER IMAGE ---
banner_path = Path("assets/banner.jpg")
if banner_path.exists():
    st.image(str(banner_path), use_container_width=True)
else:
    st.warning("Banner image not found. Please make sure `assets/banner.jpg` is in the repo.")

st.markdown("---")

# --- BEGIN BUTTON ---
if st.button("Begin Calibration"):
    time.sleep(0.3)
    try:
        st.switch_page("pages/1_Calibrate.py")  # Streamlit >= 1.22
    except Exception:
        st.error("Could not switch page. Please use the sidebar to go to 'Calibrate'.")
