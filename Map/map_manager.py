import folium
import random


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


def add_users_positions(current_map, userlist):
    if userlist is not None:
        for user in userlist:
            r = lambda: random.randint(0, 255)
            color = str('#%02X%02X%02X' % (r(), r(), r()))
            for traj in user.get_trajectorylist():
                folium.PolyLine(traj.get_coord_pointlist(), color=color, weight=3, opacity=1).add_to(current_map)

        current_map.save("Map/map.html")

    return current_map
