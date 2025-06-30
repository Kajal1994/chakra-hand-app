import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase, WebRtcMode
import mediapipe as mp, cv2, av, time

# ---------- page layout ----------
st.set_page_config(page_title="Calibrate", layout="centered")
st.title("🔧 Camera Calibration")

st.write(
    "1️⃣ **Allow webcam**  2️⃣ **Raise an open palm** until you see ✅  3️⃣ Click **Continue**"
)

# ---------- shared flags ----------
st.session_state.setdefault("calibrated", False)

mp_hands = mp.solutions.hands
mp_draw  = mp.solutions.drawing_utils


class CalibProcessor(VideoProcessorBase):
    def __init__(self):
        self.hands   = mp_hands.Hands(max_num_hands=1)
        self.hand_ok = False

    def recv(self, frame: av.VideoFrame) -> av.VideoFrame:
        img = frame.to_ndarray(format="bgr24")
        res = self.hands.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

        if res.multi_hand_landmarks:
            self.hand_ok = True
            for lm in res.multi_hand_landmarks:
                mp_draw.draw_landmarks(
                    img, lm, mp_hands.HAND_CONNECTIONS,
                    mp_draw.DrawingSpec(color=(0, 255, 0), thickness=2)
                )
            cv2.putText(img, "Hand detected", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        else:
            self.hand_ok = False
            cv2.putText(img, "Show open palm", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        return av.VideoFrame.from_ndarray(img, format="bgr24")


ctx = webrtc_streamer(
    key="calib_stream",                    # unique per page
    mode=WebRtcMode.SENDRECV,
    video_processor_factory=CalibProcessor,
    media_stream_constraints={"video": True, "audio": False},
    async_processing=True,
    desired_playing_state=True,
)

# ---------- sync flag ----------
if ctx.video_processor:
    st.session_state["calibrated"] = ctx.video_processor.hand_ok

status_msg = "✅ Hand detected" if st.session_state["calibrated"] else "Waiting for hand…"
st.markdown(f"### Status: {status_msg}")

# ---------- single Continue button ----------
if st.button(
    "Continue to Live Session",
    disabled=not st.session_state["calibrated"],
    key="continue_btn",
):
    st.switch_page("pages/2_Live_Session.py")

# ---------- refresh loop ----------
# Only refresh while webcam is active and user hasn't calibrated yet
if ctx.state.playing and not st.session_state["calibrated"]:
    time.sleep(0.5)
    st.rerun()
