import streamlit as st
from utils.streamlit_timeline import timeline
import json

st.set_page_config(
    page_title="Timeline",
    page_icon="📅",
    layout="wide"
)

# load data
with open('data/timeline.json', "r") as f:
    data = f.read()
# data = json.loads(data)

# render timeline
timeline(data, height=800)