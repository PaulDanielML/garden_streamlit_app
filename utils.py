import os
from typing import Dict, Tuple
import streamlit as st
from streamlit_folium import folium_static
import folium
import numpy as np
from PIL import Image


def save_layout_as_image(image_data: np.ndarray, file_name: str = "current_layout.png"):
    img = Image.fromarray(image_data, mode="RGBA")
    background_image = Image.open("img/background.png")
    out = background_image.resize(size=(img.width, img.height))
    mask = img.getchannel(3)
    mask = mask.point(lambda p: 230 if p > 0 else 0)
    img = img.convert("RGB")
    out.paste(img, (0, 0), mask)
    out.save(f"img/{file_name}")


def add_veggie_callback():
    st.session_state.layout_mode = "add_veggie"
    st.session_state.show_add_button = False


def back_callback():
    st.session_state.layout_mode = "legend"
    st.session_state.show_add_button = True


def show_map(coordinates: Tuple):
    my_map = folium.Map(location=coordinates, zoom_start=15)

    google_satellite_hybrid = folium.TileLayer(
        tiles="https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}",
        attr="Google",
        name="Google Satellite",
        overlay=True,
        control=True,
    )
    google_satellite_hybrid.add_to(my_map)
    folium.Marker(coordinates, popup="Our Garden").add_to(my_map)
    folium_static(my_map, width=1200, height=800)


def get_formatted_name(name: str, line_length: int = 15):
    if len(name) <= 15:
        return name
    return "\n".join(name[i : i + line_length] for i in range(0, len(name), line_length))


def get_json_files():
    return sorted([f for f in os.listdir("data") if f.endswith(".json")])


def make_centered_title(text: str, size: int = 25, obj=None):
    html = f"<h1 style='text-align: center; font-size:{size}px'>{text}</h1>"
    if obj is None:
        st.markdown(html, unsafe_allow_html=True)
    else:
        obj.markdown(html, unsafe_allow_html=True)


def drawing_mode_format_func(inp: str):
    return "Rectangle" if inp == "rect" else inp.capitalize()


def hex_to_rgb_str(hex: str):
    h = hex.lstrip("#")
    rgb = tuple(int(h[i : i + 2], 16) for i in (0, 2, 4))
    return f"rgba({rgb[0]}, {rgb[1]}, {rgb[2]}, 0.5)"


def make_colored_square(hex_color: str, size: int = 30, obj=None):
    local_obj = obj or st
    local_obj.markdown(
        f'<div style="height:{size}px;width:{size}px;background-color:{hex_color};border-radius:10px 10px 10px 10px;border-style:dotted;border-color:#19191A"></div>',
        unsafe_allow_html=True,
    )


def v_spacer(height, obj=None, sb=False) -> None:
    for _ in range(height):
        if obj is not None:
            obj.write("\n")
        else:
            if sb:
                st.sidebar.write("\n")
            else:
                st.write("\n")


if __name__ == "__main__":
    print(get_formatted_name("öasdljkfaösdlkfjaösdlfkadsfölkajsdfölaksjdfasöldfkjasödlfköj"))
