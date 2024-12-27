import osmnx as ox
import networkx as nx
import folium
import json
import numpy as np

class Map:
    def __init__(self):
        self.location = "San Francisco, California, United States"
        self.mode = "walk"
        self.optimizer = "time"
        self.graph = ox.graph_from_place(self.location, network_type=self.mode)

        self.m = None
        self.places = None
        self.routes = None
        self.markers = None

    def reset(self):
        self.m = folium.Map(location=(np.mean([value for value, _ in self.places]),
                                      np.mean([value for _, value in self.places])),
                            tiles="Cartodb Positron",
                            zoom_start=15,
                            attr="Shkolin Alexandr",
                            attributionControl=0)  # location=ox.geocode(self.location)

    def parse_places(self, places):
        self.places = [(item["latitude"], item["longitude"]) for item in json.loads(places)]
        self.reset()

        return self.places

    def create_route(self, start_coords, end_coords):

        start_node = ox.nearest_nodes(self.graph, X=start_coords[1], Y=start_coords[0])
        end_node = ox.nearest_nodes(self.graph, X=end_coords[1], Y=end_coords[0])

        shortest_route = ox.routing.shortest_path(self.graph, start_node, end_node, weight=self.optimizer)

        return ox.routing.route_to_gdf(self.graph, shortest_route)

    def make_routes(self):
        self.routes = []

        for index, place in enumerate(self.places):
            if index < len(self.places) - 1:
                current_place, next_place = place, self.places[index + 1]
                route = self.create_route(current_place, next_place)
                self.routes.append(route)

        return self.routes

    def make_markers(self):
        self.markers = []

        for index, place in enumerate(self.places):
            if index == 0:
                marker = {"location": place,
                          "icon": "person",
                          "color": "green",
                          }
            elif index == len(self.places) - 1:
                marker = {"location": place,
                          "icon": "flag-checkered",
                          "color": "red",
                          }
            else:
                marker = {"location": place,
                          "icon": "star",
                          "color": "orange",
                          }

            self.markers.append(marker)

        return self.markers

    def draw(self):
        for route in self.routes:
            folium.GeoJson(route).add_to(self.m)

        for marker in self.markers:
            folium.Marker(
                location = marker["location"],
                # popup = start_latlng,
                icon=folium.Icon(prefix="fa", icon=marker["icon"], color=marker["color"])
            ).add_to(self.m)

        return self.m
