import os
import streamlit as st
import streamlit.components.v1 as components


_RELEASE = False


if not _RELEASE:
# During development, point to local dev server
_component_func = components.declare_component(
"streamlit_drag",
url="http://localhost:3000",
)
else:
# For production, load built frontend from build folder
parent_dir = os.path.dirname(os.path.abspath(__file__))
build_dir = os.path.join(parent_dir, "frontend", "build")
_component_func = components.declare_component("streamlit_drag", path=build_dir)




def drag_component(items, width=3100, height=2050, key=None):
"""
items: list of {id, name, x, y, w, h}
returns updated items with new x,y
"""
if key is None:
key = "streamlit-drag-component"
result = _component_func(items=items, width=width, height=height, key=key)
return result
