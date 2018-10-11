from math import sin, cos, asin, sqrt, radians
from Classes.entities import StayPoint
from Classes.side import Coordinates


def staypoint_detection(p, dist_threh, time_threh):
    sp = []
    i = 0
    while i < len(p):
        j = i + 1
        while j < len(p):
            dist = distance(p[i], p[j])
            if dist > dist_threh:
                delta_t = p[j].get_timestamp() - p[i].get_timestamp()
                delta_t = delta_t.total_seconds() / 60
                if delta_t > time_threh:
                    coord = compute_mean_coord(p, i, j)
                    s = StayPoint(coord, p[i].get_timestamp(), p[j].get_timestamp())
                    sp.append(s)
                i = j
                break
            j += 1
        i += 1
    return sp


def distance(point_a, point_b):
    lon1, lat1, lon2, lat2 = map(radians, [point_a.get_longitude(), point_a.get_latitude(), point_b.get_longitude(),
                                           point_b.get_latitude()])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = 6371000  # Radius of earth in meters. Use 3956 for miles
    return c * r


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
