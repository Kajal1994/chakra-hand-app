import streamlit as st
from PIL import Image
import time

st.set_page_config(page_title="Chakra Visualiser", layout="centered")

# ----- TITLE & INTRO -----
st.title("🌀 Chakra Visualiser")
st.subheader("Real-time gesture-activated chakra feedback")

st.write("""
Welcome!  
This app lets you raise different hand gestures to activate and visualise your chakras
— complete with colours, sounds, and live feedback.
""")

# ----- BANNER IMAGE (optional) -----
try:
    banner = Image.open("assets/banner.jpg")  # replace filename
    st.image(banner, use_container_width=True)
except FileNotFoundError:
    pass  # no image yet

st.markdown("---")

# ----- BEGIN BUTTON -----
if st.button("👉 Begin Calibration"):
    # tiny delay for smoother UX
    time.sleep(0.3)
    # Use Streamlit's built-in page navigation
    st.switch_page("pages/1_Calibrate.py")
