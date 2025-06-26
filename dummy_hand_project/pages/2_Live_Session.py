# pages/2_Live_Session.py
import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase, WebRtcMode
import mediapipe as mp, cv2, av, time

st.set_page_config(page_title="Live Session", layout="centered")
st.title("🌀 Live Session")

st.write(
    "Raise an **open palm** to activate the Root Chakra (red glow). "
    "Next steps will add more gestures, colours, and sounds."
)

# Session default
st.session_state.setdefault("current_chakra", "None")

# ---- MediaPipe setup ----
mp_hands = mp.solutions.hands
mp_draw  = mp.solutions.drawing_utils


def is_open_palm(lm):
    # Simple heuristic: all four fingers straight & thumb pointing left
    tip_ids = [8, 12, 16, 20]
    for tid in tip_ids:
        if lm.landmark[tid].y > lm.landmark[tid - 2].y:
            return False
    return True


class LiveProcessor(VideoProcessorBase):
    def __init__(self):
        self.hands   = mp_hands.Hands(max_num_hands=1)
        self.gesture = ""

    def recv(self, frame: av.VideoFrame) -> av.VideoFrame:
        img = frame.to_ndarray(format="bgr24")
        res = self.hands.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

        self.gesture = ""
        if res.multi_hand_landmarks:
            lm = res.multi_hand_landmarks[0]
            mp_draw.draw_landmarks(img, lm, mp_hands.HAND_CONNECTIONS)
            if is_open_palm(lm):
                self.gesture = "Root"
                # add red overlay
                overlay = img.copy()
                h, w = img.shape[:2]
                cv2.circle(overlay, (w // 2, h // 2), 200, (0, 0, 255), -1)
                img = cv2.addWeighted(overlay, 0.25, img, 0.75, 0)

        return av.VideoFrame.from_ndarray(img, format="bgr24")


ctx = webrtc_streamer(
    key="live_stream",
    mode=WebRtcMode.SENDRECV,
    video_processor_factory=LiveProcessor,
    media_stream_constraints={"video": True, "audio": False},
    async_processing=True,
    desired_playing_state=True,
)

# -------- live status ----------
if ctx.video_processor:
    chakra = "Root Chakra ❤️" if ctx.video_processor.gesture == "Root" else "None"
    st.session_state["current_chakra"] = chakra

st.markdown(f"### Current Chakra → **{st.session_state['current_chakra']}**")

# -------- lightweight auto-refresh (400 ms) ------------
time.sleep(0.4)
st.rerun()
