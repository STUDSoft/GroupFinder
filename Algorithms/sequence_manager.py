from Classes.entities import Sequence, Node


# eps errore di tempo per sequenze simili
def sequence_matching(seq1, seq2, max_length, eps):
    # crea le sequenze di lunghezza 1, poi rimuove quelle non presenti in seq2
    temp_set = one_length_seq_set(seq1)
    sequence_set = set()
    for s in temp_set:
        if seq1_in_seq2(s, seq2, eps):
            sequence_set.add(s)
            
    step = 1
    while step <= max_length:
        extended_set = set()
        i=0
        for s in sequence_set:
            i+=1
            if len(s.get_nodes()) - 1 is step:
                extended_set = extend_sequence(s, eps, seq1, seq2, extended_set)
        # prune_sequence effettua la potatura di sequence_set e poi unisce i due set
        sequence_set = prune_sequence(sequence_set, extended_set)
        step += 1
    return sequence_set


def extract_sequencies(staypoints, clusters):
    sequencies = []
    for i in range(len(staypoints)):
        pos = get_user_seq_pos(sequencies, staypoints[i].get_user_identifier())
        if pos is None:#if the user does not have a sequence in the array, it is created
            new_user_seq = Sequence(staypoints[i].get_user_identifier())
            if clusters[i] is not -1:#checks for noise
                node = Node(clusters[i], 0, 1, staypoints[i].get_leav_time())
                new_user_seq.add_node(node)
            sequencies.append(new_user_seq)
        else:
            if sequencies[pos].has_nodes():#a user can have a sequence with no nodes
                if clusters[i] is sequencies[pos].get_latest_node().get_clust_id():
                    sequencies[pos].get_latest_node().add_staypoint()
                    sequencies[pos].get_latest_node().set_leav_time(staypoints[i].get_leav_time())
                else:
                    if clusters[i] is not -1:#checks for noise
                        time_diff = staypoints[i].get_arv_time() - sequencies[pos].get_latest_node().get_leav_time()
                        time_diff_in_hours = time_diff.total_seconds() / 3600
                        node = Node(clusters[i], time_diff_in_hours, 1, staypoints[i].get_leav_time())
                        sequencies[pos].add_node(node)
            else:
                if clusters[i] is not -1:#checks for noise
                    node = Node(clusters[i], 0, 1, staypoints[i].get_leav_time())
                    sequencies[pos].add_node(node)
    return sequencies


def get_user_seq_pos(sequencies, user_id):
    """
    Searches wheter a user has already a sequence
    """
    i = 0
    while i < len(sequencies):
        if sequencies[i].get_user_id() is user_id:
            return i
        i += 1
    return None


def one_length_seq_set(seq):
    sequence_set = set()
    nodes = seq.get_nodes()
    for i in range(len(nodes) - 1):
        node = nodes[i]
        j = i + 1
        if(j < len(nodes)):
            tot_time = nodes[j].get_time_to()
        while j < len(nodes):
            node_j = Node(nodes[j].get_clust_id(), tot_time, nodes[j].get_num_staypoints(), nodes[j].get_leav_time())
            s = Sequence()
            s.add_node(node)
            s.add_node(node_j)
            sequence_set.add(s)
            j += 1
            if j < len(nodes):
                tot_time += nodes[j].get_time_to()
    return sequence_set


def seq1_in_seq2(seq1, seq2, eps):
    node_s1 = seq1.get_nodes()
    node_s2 = seq2.get_nodes()

    for i in range(len(node_s2)):
        if node_s1[0].get_clust_id() is node_s2[i].get_clust_id() and len(node_s1) <= (len(node_s2) - i):
            b1 = False  # segnala se non cercare la sequenza (False=cerca, True=non cercare)
            j = 1
            n = i
            minimum = []  # contiene i valori minimi di num_staypoint
            minimum += [int(min(node_s1[0].get_num_staypoints(), node_s2[n].get_num_staypoints()))]
            while j < len(node_s1) and not b1:
                k = n + 1
                if(k < len(node_s2)):
                    tot_time = node_s2[k].get_time_to()
    
                    while k < len(node_s2) and not b1:
                        if node_s2[k].get_clust_id() is node_s1[j].get_clust_id() and eps >= abs(
                                tot_time - node_s1[j].get_time_to()):
                            b1 = True
                            n = k
                        else:
                            k += 1
                            if k < len(node_s2):
                                tot_time += node_s2[k].get_time_to()

                if b1:
                    minimum += [int(min(node_s1[j].get_num_staypoints(), node_s2[n].get_num_staypoints()))]
                    j += 1
                    b1 = False
                else:
                    # se si e' usciti dal ciclo e non si e' trovata la sequnenza
                    # o una sua continuazione, e' inutile continuare a cercare
                    b1 = True

            if j is len(node_s1):
                # aggiorna la permanenza minima
                c = 0
                while c < len(node_s1):
                    if node_s1[c].get_num_staypoints() > minimum[c]:
                        node_s1[c].set_num_staypoints(minimum[c])
                    c += 1
                return True

    return False


def extend_sequence(seq, eps, seq1, seq2, extended_set):
    # eps e' usato come errore per riconoscere un passo simile
    # A partire da seq, cerca in seq1 un modo per espanderla
    #     Se lo trovi verifica che sia presente in seq2
    #     Se viene trovato, inseriscilo in extended_set
    # Restituisci extended_set
    nodes_seq = seq.get_nodes()
    nodes_seq1 = seq1.get_nodes()

    i = 0
    while i < (len(nodes_seq1) - len(nodes_seq)):
        # cerca l'inizio di seq in seq1
        if nodes_seq[0].get_clust_id() is nodes_seq1[i].get_clust_id():
            # verifica di aver trovato seq, come la funzione seq1_in_seq2()
            b1 = False  # segnala se non cercare la sequenza (False=cerca, True=non cercare)
            j = 1
            n = i  # n e' da quale punto cercare il nodo successivo
            while j < len(nodes_seq) and not b1:
                k = n + 1
                if(k < len(nodes_seq1)):
                    tot_time = nodes_seq1[k].get_time_to()
    
                    while k < len(nodes_seq1) and not b1:
                        if nodes_seq1[k].get_clust_id() is nodes_seq[j].get_clust_id() and eps >= abs(
                                tot_time - nodes_seq[j].get_time_to()):
                            b1 = True
                            n = k
                        else:
                            k += 1
                            if k < len(nodes_seq1):
                                tot_time += nodes_seq1[k].get_time_to()

                if b1:
                    j += 1
                    b1 = False
                else:
                    # se si e' usciti dal ciclo e non si e' trovata la sequnenza
                    # o una sua continuazione, e' inutile continuare a cercare
                    b1 = True

            if j is len(nodes_seq):
                # espandi la sequenza seq
                n += 1
                if(n < len(nodes_seq1)):
                    tot_time = nodes_seq1[n].get_time_to()
    
                    while n < len(nodes_seq1):
                        # copia seq
                        exp_seq = Sequence()
                        for node in nodes_seq:
                            tmp_node = Node(node.get_clust_id(), node.get_time_to(), node.get_num_staypoints(),
                                            node.get_leav_time())
                            exp_seq.add_node(tmp_node)
                        # espandi
                        new_node = Node(nodes_seq1[n].get_clust_id(), nodes_seq1[n].get_time_to(),
                                        nodes_seq1[n].get_num_staypoints(), nodes_seq1[n].get_leav_time())
                        exp_seq.add_node(new_node)
                        # controlla che sia in seq2, se si aggiungi
                        if seq1_in_seq2(exp_seq, seq2, eps):
                            extended_set.add(exp_seq)
                        # cerca altre sequenze
                        n += 1
                        if n < len(nodes_seq1):
                            tot_time += nodes_seq1[n].get_time_to()

        i += 1  # incrementa il primo while

    return extended_set


def prune_sequence(sequence_set, extended_set):
    """
    elimina le sequenze di sequence_set che sono incluse nelle sequenze di extended_set
    """
    tmp_set = set()
    for seq in sequence_set:
        # se una sotto-sequenza e' trovata viene ignorata, altrimenti e' aggiunta al set temporaneo
        found = False
        for ext in extended_set:
            if seq1_in_seq2(seq, ext, 0):  # eps e' 0 perche' le sequenze sono identiche
                found = True
                break
        if not found:
            tmp_set.add(seq)
    # alla fine aggiungi tutto il set esteso, si puo' includere nel ciclo precedente
    for ext in extended_set:
        tmp_set.add(ext)
    return tmp_set


def compute_similarity(seq, n_sp1, n_sp2):
    sim = 0
    for s in seq:
        nodes = s.get_nodes()
        seq_sim = 0
        for n in nodes:
            seq_sim += n.get_num_staypoints()
        seq_sim = seq_sim * (2 ** (len(nodes) - 1))
        sim += seq_sim
    sim = sim / (n_sp1 * n_sp2)
    return sim
