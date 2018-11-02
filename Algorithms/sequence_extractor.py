from Classes.entities import Sequence, Node


def extract_sequencies(staypoints, clusters):
    sequencies = []
    for i in range(len(staypoints)):
        pos = get_user_seq_pos(sequencies, staypoints[i].get_user_identifier())
        if pos is None:
            new_user_seq = Sequence(staypoints[i].get_user_identifier())
            if clusters[i] is not -1:
                node = Node(clusters[i], 0, 1, staypoints[i].get_leav_time())
                new_user_seq.add_node(node)
            sequencies.append(new_user_seq)
        else:
            if sequencies[pos].has_nodes():
                if clusters[i] is sequencies[pos].get_latest_node().get_clust_id():
                    sequencies[pos].get_latest_node().add_staypoint()
                    sequencies[pos].get_latest_node().set_leav_time(staypoints[i].get_leav_time())
                else:
                    if clusters[i] is not -1:
                        time_diff = staypoints[i].get_arv_time() - sequencies[pos].get_latest_node().get_leav_time()
                        time_diff_in_hours = time_diff.total_seconds() / 3600
                        node = Node(clusters[i], time_diff_in_hours, 1, staypoints[i].get_leav_time())
                        sequencies[pos].add_node(node)
            else:
                if clusters[i] is not -1:
                    node = Node(clusters[i], 0, 1, staypoints[i].get_leav_time())
                    sequencies[pos].add_node(node)
    return sequencies


def get_user_seq_pos(sequencies, user_id):
    i = 0
    while i < len(sequencies):
        if sequencies[i].get_user_id() is user_id:
            return i
        i += 1

    return None
