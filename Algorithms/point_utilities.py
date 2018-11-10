from math import sin, cos, asin, sqrt, radians

#calculates the haversine distance between two points
def haversine_distance(point_a, point_b):
    lon1, lat1, lon2, lat2 = map(radians, [point_a.get_longitude(), point_a.get_latitude(), point_b.get_longitude(),
                                           point_b.get_latitude()])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = 6371000  # Radius of earth in meters. Use 3956 for miles
    return c * r

#counts the number of staypoints for a specific user
def get_number_of_sp_per_user(stp):
    #the total number of users is unknown
    #but we can use the number of user_id in the staypoints as an approximation
    num_sp=[0]
    id_user = 0
    for p in stp:
        if int(p.get_user_identifier()) is id_user:
            num_sp[id_user] += 1
        elif int(p.get_user_identifier()) > id_user:
            while int(p.get_user_identifier()) > id_user:
                num_sp += [0]
                id_user += 1
            num_sp[id_user] += 1
    return num_sp
