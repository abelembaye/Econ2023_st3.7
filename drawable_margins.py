# streamlit run drawable_margins.py
import streamlit as st
from streamlit_drawable_canvas import st_canvas # pip install streamlit-drawable-canvas

# Set up the layout
st.title("Drawing Canvas with Margins for Labels")

# Define canvas size and margins
canvas_width = 600
canvas_height = 400
margin_top = 50
margin_left = 50

# Create a container for the canvas and labels
canvas_container = st.container()

# Add labels to the margins
with canvas_container:
    st.write(" " * (margin_left // 10) + "Top Label")
    st.write("\n" * (margin_top // 20))
    st.write("Left Label", unsafe_allow_html=True)
    st.write(" " * ((canvas_width - margin_left) // 10) + "Right Label", unsafe_allow_html=True)

# Create the drawable canvas
canvas_result = st_canvas(
    fill_color="rgba(255, 165, 0, 0.3)",  # Fill color with some transparency
    stroke_width=2,
    stroke_color="#000000",
    background_color="#FFFFFF",
    width=canvas_width,
    height=canvas_height,
    drawing_mode="freedraw",
    key="canvas",
)

# Display the canvas result
if canvas_result.image_data is not None:
    st.image(canvas_result.image_data)