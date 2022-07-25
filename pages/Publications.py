import html
import streamlit as st
from annotated_text import annotated_text
import yaml
from htbuilder import H, HtmlElement, styles
from htbuilder.units import unit

# Only works in 3.7+: from htbuilder import div, span
div = H.div
span = H.span

px = unit.px
rem = unit.rem
em = unit.em

TAG_COLORS = {
    "data science": "#ff4b4b",
    "medical physics": "#ffa421",
    "ml ops": "#ffe312",
    "insurance": "#21c354",
    "digital breast tomosynthesis": "#00d4b1", 
    "mammography": "#00c0f2",
    "deep learning": "#1c83e1",
    "convolutional neural networks": "#803df5",
    "computer-aided diagnosis": "#808495",
}

# Colors from the Streamlit palette.
# These are red-70, orange-70, ..., violet-70, gray-70.

OPACITIES = [
    "33", "66",
]

with open("data/publications.yaml", 'r') as stream:
    data = (yaml.safe_load(stream))
    
def render_tag(tag: str, color: str):
    color_style = {}

    if color:
        color_style['color'] = color

    # background = None
    # if not background:
    # label_sum = sum(ord(c) for c in tag)
    background_color = TAG_COLORS[tag]
    background_opacity = "33"
    background = background_color + background_opacity
        
    return (
        span(
            style=styles(
                background=background,
                border_radius=rem(0.33),
                padding=(rem(0.125), rem(0.5)),
                overflow="hidden",
                **color_style,
            )
        )
        (
            html.escape(tag),(
                span(
                    style=styles(
                        font_size=em(0.67),
                        opacity=0.5,
                    )),
            ),
        )
    )
    
    
def render_tags(tags: list) -> str:
    
    out = div()

    for tag in tags:
        color = "black"
        tag_html = render_tag(tag, color)
        out(tag_html)
        out(html.escape(" "))

    tag_string = str(out)
    st.markdown(
        tag_string,
        unsafe_allow_html=True,
    )

    
def publication_element(pub_data: dict):
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f'**[{pub_data["title"]}]({pub_data["link"]})**')
        st.markdown(pub_data["authors"])
        st.markdown(pub_data["journal"])
        st.markdown(pub_data["date"])
        # st.markdown(pub_data["type"])
        render_tags(pub_data["tags"])
        with st.expander("Abstract"):
            st.write(pub_data["abstract"])
    with col2:
        st.image(pub_data["image"])
    
publication_element(data[0])