import os
import requests as rq
import streamlit as st
import folium
import json


from map import Map


# Внутрення сеть докер композа
# st.write(rq.get(f"http://backend:{os.getenv('BACKEND_PORT')}/").text)

class Place:
    def __init__(self, index, name, latitude, longitude):
        self.index = index
        self.name = name
        self.latitude = latitude
        self.longitude = longitude

    def to_dict(self):
        return {
            "index": self.index,
            "name": self.name,
            "latitude": self.latitude,
            "longitude": self.longitude
        }

def swap_places(lst, idx, nwidx):
    lst[idx], lst[nwidx] = lst[nwidx], lst[idx]

# def clear_text_input(text_input_key):
#     st.session_state[text_input_key] = ""

st.set_page_config(page_title="Get N Cities", layout="wide")

if "map" not in st.session_state:
    st.session_state["map"] = Map()

if "places" not in st.session_state:
    st.session_state["places"] = [
        Place(0, "Start", 37.78497, -122.43327),
        Place(1, "Curr", 37.78336, -122.42518),
        Place(2, "End", 37.78071, -122.41445)
    ]

map = st.session_state["map"]
places = st.session_state["places"]

st.header("Соберите маршрут")

map_column, places_column = st.columns([0.7, 0.3])

with map_column:
    js = json.dumps([place.to_dict() for place in places])

    map.parse_places(js)
    map.make_routes()
    map.make_markers()
    st.components.v1.html(folium.Figure().add_child(map.draw()).render(), height=650)

with places_column:

    for place in places:
        with st.container(border=True):
            index = places.index(place)

            name_column, upButton_column, downButton_column, deleteButton_column = st.columns([0.7, 0.1, 0.1, 0.1])

            with name_column:
                st.write(place.name)

            with upButton_column:
                if st.button("⬆", key=str(index) + "upButton"):
                    new_index = len(places) - 1 if index == 0 else index - 1
                    swap_places(places, index, new_index)
                    st.rerun()

            with downButton_column:
                if st.button("⬇", key=str(index) + "downButton"):
                    new_index = 0 if index == len(places) - 1 else index + 1
                    swap_places(places, index, new_index)
                    st.rerun()

            with deleteButton_column:
                if st.button("❌", key=str(index) + "deleteButton"):
                    places.pop(index)
                    st.rerun()

    with st.form("Name"):
        name_column, latitude_column, longitude_column, addButton_column = st.columns([0.5, 0.2, 0.2, 0.1])

        with name_column:
            name = st.text_input("Name", label_visibility="collapsed", placeholder="Name of place")

        with latitude_column:
            latitude = st.text_input("latitude", label_visibility="collapsed", placeholder="Latitude")

        with longitude_column:
            longitude = st.text_input("longitude", label_visibility="collapsed", placeholder="Longitude")

        with addButton_column:
            if st.form_submit_button("➕") and name not in [item.name for item in places]:
                try:
                    index = len(places) - 1
                    place = Place(index=index,
                                  name=name,
                                  latitude=float(latitude),
                                  longitude=float(longitude))
                    places.append(place)
                    st.rerun()
                except:
                    pass