from Classes.side import Coordinates
from Algorithms.point_utilities import haversine_distance
import numpy as np


def staypoint_detection(userlist, dist_threh, time_threh):
    sp = []
    for user in userlist:
        trajectorylist = user.get_trajectorylist()
        for trajectory in trajectorylist:
            p = trajectory.get_pointlist()
            i = 0
            while i < len(p):
                j = i + 1
                while j < len(p):
                    dist = haversine_distance(p[i], p[j])
                    if dist > dist_threh:
                        delta_t = p[j].get_timestamp() - p[i].get_timestamp()
                        delta_t = delta_t.total_seconds() / 60
                        if delta_t > time_threh:
                            coord = compute_mean_coord(p, i, j)
                            s = [coord.get_latitude(), coord.get_longitude()]
                            s = np.array(s)
                            sp.append(s)
                        i = j
                        break
                    j += 1
                i += 1
    return np.array(sp)


def compute_mean_coord(p, i, j):
    med_lat = 0
    med_long = 0
    num_points = 1
    for k in range(i, j + 1):
        med_lat += p[k].get_latitude()
        med_long += p[k].get_longitude()
        num_points += 1
    med_lat /= num_points
    med_long /= num_points
    return Coordinates(med_lat, med_long)
