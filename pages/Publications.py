import html
import streamlit as st
from annotated_text import annotated_text
import yaml
from htbuilder import H, HtmlElement, styles
from htbuilder.units import unit
from colorhash import ColorHash
import pandas as pd

# Only works in 3.7+: from htbuilder import div, span
div = H.div
span = H.span

px = unit.px
rem = unit.rem
em = unit.em


with open("data/publications.yaml", 'r') as stream:
    data = (yaml.safe_load(stream))
    
def render_tag(tag: str, color: str):
    color_style = {}

    if color:
        color_style['color'] = color
    
    # hash tag string to get a hex color
    # by using a hash, the color is deterministic
    background_color = ColorHash(tag).hex
    
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
    return tag_string
    
    # st.markdown(
    #     tag_string,
    #     unsafe_allow_html=True,
    # )
    

    
def publication_element(pub_data: dict):
    

    # table_data = {
    #     "Authors": pub_data["authors"],
    #     "Publication": pub_data["journal"],
    #     "Publication Date": pub_data["date"],
    #     "Format": pub_data["format"]
    # }
    table_markdown = f"""
    | Title            | [{pub_data["title"]}]({pub_data["link"]}) |
    |------------------|-----------|
    | Authors          | {pub_data["authors"]} |
    | Publication Date | {pub_data["date"]} |
    | Journal          | {pub_data["journal"]}|
    | Full-text Link   | {pub_data["link"]} |
    | Keywords         | {render_tags(pub_data["tags"])} |
    """
    st.markdown(table_markdown, unsafe_allow_html=True)
    
    with st.expander("Abstract"):
        st.write(pub_data["abstract"])

    
for pub in data:
    publication_element(pub)