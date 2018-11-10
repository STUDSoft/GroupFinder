import folium


def plot_map(theme="light", osm=False):
    folium_map = None
    if osm is True:
        folium_map = folium.Map(location=[0, 0],
                                zoom_start=2,
                                tiles="OpenStreetMap")
    else:
        if theme is "light":
            folium_map = folium.Map(location=[0, 0],
                                    zoom_start=2,
                                    tiles="CartoDB positron")
        elif theme is "dark":
            folium_map = folium.Map(location=[0, 0],
                                    zoom_start=2,
                                    tiles="CartoDB dark_matter")

    folium_map.save("Map/map.html")

    return folium_map
