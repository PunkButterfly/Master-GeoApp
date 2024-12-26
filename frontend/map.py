import osmnx as ox
import networkx as nx
import folium

start_latlng = (37.78497,-122.43327)
end_latlng = (37.78071,-122.41445)


class Map:
    def __init__(self):
        self.location = "San Francisco, California, United States"
        self.mode = "walk"
        self.optimizer = "time"
        self.graph = ox.graph_from_place(self.location, network_type=self.mode)

    def create_route(self, start_place, end_place):
        # start_node = ox.nearest_nodes(self.graph, X=start_place.latitude, Y=start_place.longitude)
        # end_node = ox.nearest_nodes(self.graph, X=end_place.latitude, Y=end_place.longitude)

        start_node = ox.nearest_nodes(self.graph, X=37.78497, Y=-122.43327)
        end_node = ox.nearest_nodes(self.graph, X=37.78071, Y=-122.41445)

        shortest_route = ox.routing.shortest_path(self.graph, start_node, end_node, weight=self.optimizer)

        return ox.routing.route_to_gdf(self.graph, shortest_route)


    def draw_map(self, places):
        m = folium.Map(location=ox.geocode(self.location), tiles="Cartodb Positron")  # , zoom_start=zoom_start

        for index, place in enumerate(places):
            if index < len(places) - 1:
                current_place, next_place = place, places[index + 1]
                route = self.create_route(current_place, next_place)

                folium.GeoJson(route).add_to(m)

                start_marker = folium.Marker(
                            location = (current_place.latitude, current_place.longitude),
                            # popup = start_latlng,
                            icon = folium.Icon(color='green')).add_to(m)

                end_marker = folium.Marker(
                            location = (next_place.latitude, next_place.longitude),
                            # popup = end_latlng,
                            icon = folium.Icon(color='red')).add_to(m)

        print(m)
        return m

