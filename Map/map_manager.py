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


def add_users_positions(current_map, id, userlist, similarities, sim_value):
    if userlist is not None and similarities is not None:
        for u in userlist:
            sim = float(similarities[int(id)][int(u.get_identifier())])
            if sim >= float(sim_value):
                r = lambda: random.randint(0, 255)
                color = str('#%02X%02X%02X' % (r(), r(), r()))
                for traj in u.get_trajectorylist():
                    folium.PolyLine(traj.get_coord_pointlist(), color=color, weight=1.5, opacity=1,
                                    popup="<b>User " + str(u.get_identifier()) + "</b><br>Similarity with User " + str(
                                        id) + ": " + str(sim)).add_to(current_map)
        for traj in userlist[int(id)].get_trajectorylist():
            folium.PolyLine(traj.get_coord_pointlist(), color="red", weight=0.5, opacity=1,
                            popup="<b>User " + str(id) + "</b>").add_to(current_map)
    current_map.save("Map/map.html")
