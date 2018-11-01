from math import sin, cos, asin, sqrt, radians


def haversine_distance(point_a, point_b):
    lon1, lat1, lon2, lat2 = map(radians, [point_a.get_longitude(), point_a.get_latitude(), point_b.get_longitude(),
                                           point_b.get_latitude()])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = 6371000  # Radius of earth in meters. Use 3956 for miles
    return c * r