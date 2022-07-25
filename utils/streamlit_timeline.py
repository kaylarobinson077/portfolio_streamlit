from datetime import date
import json
import streamlit.components.v1 as components

"""Forked from: https://github.com/innerdoc/streamlit-timeline
Decided to fork off of the existing package to support additional customizations desired
for use in this portfolio.
"""

def assign_present_date(data):
    """Replace designated dates with the current dates.

    Parameters
    ----------
    data : dict
        json-formatted data in the timeline-js format, where any date whose
        `display_date` is set to `Present` has the date value replaced with today's date
        
    Returns
    -------
    data : dict
        Copy of the input value, with today's date passed in for designated events
    """
    today = date.today()
    today_date = {
        "year": str(today.year),
        "month": str(today.month),
        "display_date": "Present"
    }
    
    for event in data["events"]:
        for date_key in ["start_date", "end_date"]:
            if event[date_key].get("display_date") == "Present":
                event[date_key] = today_date
    
    return data

def timeline(data, height=800, start_at_end=True):
    """Create a new timeline component.

    Parameters
    ----------
    data: str or dict
        String or dict in the timeline json format: https://timeline.knightlab.com/docs/json-format.html
    height: int or None
        Height of the timeline in px

    Returns
    -------
    static_component: Boolean
        Returns a static component with a timeline
    """

    # if string then to json
    if isinstance(data, str):
        data = json.loads(data) 
    
    # update `Present` dates to today
    data = assign_present_date(data)
    
    # json to string
    json_text = json.dumps(data)

    # load json
    source_param = 'timeline_json'
    source_block = f'var {source_param} = {json_text};'

    # load css + js
    cdn_path = 'https://cdn.knightlab.com/libs/timeline3/latest'
    css_block = f'<link title="timeline-styles" rel="stylesheet" href="{cdn_path}/css/timeline.css">'
    js_block  = f'<script src="{cdn_path}/js/timeline.js"></script>'


    # write html block
    htmlcode = f''' 
    {css_block}
    {js_block}

        <div id='timeline-embed' style="width: 95%; height: {str(height)}px; margin: 1px;"></div>

        <script type="text/javascript">
            var additionalOptions = {{
                start_at_end: {json.dumps(start_at_end)}, is_embed:true,
            }}
            {source_block}
            timeline = new TL.Timeline('timeline-embed', {source_param}, additionalOptions);
        </script>'''


    # return rendered html
    static_component = components.html(htmlcode, height=height,)

    return static_component