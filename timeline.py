import streamlit as st
from streamlit_timeline import timeline
import json

# use full page width
st.set_page_config(page_title="Timeline Example", layout="wide")

# load data
with open('timeline.json', "r") as f:
    data = f.read()
data = json.loads(data)

# render timeline
timeline(data, height=800)