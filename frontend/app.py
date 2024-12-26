import os
import requests as rq
import streamlit as st
import folium


from map import Map


# Внутрення сеть докер композа
# st.write(rq.get(f"http://backend:{os.getenv('BACKEND_PORT')}/").text)

class Place:
    def __init__(self, index, name, latitude, longitude):
        self.index = index
        self.name = name
        self.latitude = latitude
        self.longitude = longitude

def swap_places(lst, idx, nwidx):
    lst[idx], lst[nwidx] = lst[nwidx], lst[idx]

# def clear_text_input(text_input_key):
#     st.session_state[text_input_key] = ""

if "map" not in st.session_state:
    st.session_state["map"] = Map()

if "places" not in st.session_state:
    st.session_state["places"] = []

m = st.session_state["map"]
places = st.session_state["places"]

for place in places:
    with st.container(border=True):
        index = places.index(place)

        name_column, upButton_column, downButton_column, deleteButton_column = st.columns([0.79, 0.07, 0.07, 0.07])

        with name_column:
            st.write(place.name)

        with upButton_column:
            if st.button("⬆", key=str(index) + "upButton"):
                new_index = len(places) - 1 if index == 0 else index - 1
                swap_places(places, index, new_index)
                st.rerun()

        with downButton_column:
            if st.button("⬇", key=str(index) + "downButton"):
                new_index = 0 if index == len(st.session_state["places"]) - 1 else index + 1
                swap_places(places, index, new_index)
                st.rerun()

        with deleteButton_column:
            if st.button("❌", key=str(index) + "deleteButton"):
                st.session_state["places"].pop(index)
                st.rerun()

with st.form("Name"):
    name_column, latitude_column, longitude_column, addButton_column = st.columns([0.53, 0.2, 0.2, 0.07])

    with name_column:
        name = st.text_input("Name", label_visibility="collapsed", placeholder="Name of place")

    with latitude_column:
        latitude = st.text_input("latitude", label_visibility="collapsed", placeholder="Latitude")

    with longitude_column:
        longitude = st.text_input("longitude", label_visibility="collapsed", placeholder="Longitude")

    with addButton_column:
        if st.form_submit_button("➕") and name not in [item.name for item in places]:
            index = len(places) - 1
            place = Place(index=index,
                          name=name,
                          latitude=float(latitude),
                          longitude=float(longitude))
            places.append(place)
            st.rerun()


drawed_map = m.draw_map(places)

comp = st.components.v1.html(drawed_map.render(), height=500)

# 37.78497
# -122.43327

# 37.78071
# -122.41445