from Classes.entities import Sequence, Node


# eps errore di tempo per sequenze simili, time_thr soglia per considerare due nodi consecutivi come parte di una
# sequenza
def sequence_matching(seq1, seq2, max_length, time_thr, eps):
    sequence_set = one_length_seq_set(seq1, time_thr)
    for s in sequence_set:
        if not seq1_in_seq2(s, seq2, eps):
            sequence_set.remove(s)
    step = 1
    while step <= max_length:
        extended_set = set()
        for s in sequence_set:
            if len(s.get_nodes()) - 1 is step:
                extended_set = extend_sequence(s, time_thr, eps, seq1, seq2, extended_set)
        # prune_sequence effettua la potatura di sequence_set e poi unisce i due set
        sequence_set = prune_sequence(sequence_set, extended_set)
        step += 1
    return sequence_set


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


def one_length_seq_set(seq, time_thr):
    sequence_set = set()
    nodes = seq.get_nodes()
    for i in range(len(nodes) - 1):
        node = nodes[i]
        j = i + 1
        tot_time = nodes[j].get_time_to()
        while j < len(nodes) and tot_time <= time_thr:
            node_j = Node(nodes[j].get_clust_id(), tot_time, nodes[j].get_num_staypoints(), nodes[j].get_leav_time())
            s = Sequence()
            s.add_node(node)
            s.add_node(node_j)
            sequence_set.add(s)
            j += 1
            tot_time += nodes[j].get_time_to()
    return sequence_set


def seq1_in_seq2(seq1, seq2, eps):
    node_s1 = seq1.get_nodes()
    node_s2 = seq2.get_nodes()

    for i in range(len(node_s2)):
        if node_s1[0].get_clust_id() is node_s2[i].get_clust_id() and len(node_s1) <= (len(node_s2) - i):
            b1 = False #segnala se non cercare la sequenza (False=cerca, True=non cercare)
            j = 1
            n = i
            while j < len(node_s1) and not b1:
                k = n + 1
                tot_time = node_s2[k].get_time_to()

                while k < len(node_s2) and (
                        tot_time >= (node_s1[j].get_time_to() - eps) or tot_time <= (
                        node_s1[j].get_time_to() + eps)) and not b1:
                    if node_s2[k].get_clust_id() is node_s1[j].get_clust_id():
                        b1 = True
                        n = k
                    else:
                        k += 1
                        tot_time += node_s2[k].get_time_to()

                if b1:
                    j += 1
                    b1 = False
                else:
                    #se si e' usciti dal ciclo e non si e' trovata la sequnenza
                    #o una sua continuazione, e' inutile continuare a cercare
                    b1=True

            if j is len(node_s1):
                return True

    return False


def extend_sequence(seq, time_thr, eps, seq1, seq2, extended_set):
    '''
    eps e' usato come errore per riconoscere un passo simile
    time_thr e' usato per considerare un passo come successore di una sequenza
    A partire da seq, cerca in seq1 un modo per espanderla
        Se lo trovi verifica che sia presente in seq2
        Se viene trovato, inseriscilo in extended_set
    Restituisci extended_set
    '''
    nodes_seq=seq.get_nodes()
    nodes_seq1=seq1.get_nodes()
    
    i=0
    print("\nRicerca seq in seq1")
    while i< ( len(nodes_seq1) - len(nodes_seq) ):
        #cerca l'inizio di seq in seq1
        if nodes_seq[0].get_clust_id is nodes_seq[i].get_clust_id:
            #verifica di aver trovato seq, come la funzione seq1_in_seq2()
            b1=False #segnala se non cercare la sequenza (False=cerca, True=non cercare)
            j = 1
            n = i #n e' da quale punto cercare il nodo successivo
            while j < len(nodes_seq) and not b1:
                k = n + 1
                tot_time = nodes_seq1[k].get_time_to()

                while k < len(nodes_seq1) and (
                        tot_time >= (nodes_seq[j].get_time_to() - eps) or tot_time <= (
                        nodes_seq[j].get_time_to() + eps)) and not b1:
                    if nodes_seq1[k].get_clust_id() is nodes_seq[j].get_clust_id():
                        b1 = True
                        n = k
                    else:
                        k += 1
                        tot_time += nodes_seq1[k].get_time_to()

                if b1:
                    j += 1
                    b1 = False
                else:
                    #se si e' usciti dal ciclo e non si e' trovata la sequnenza
                    #o una sua continuazione, e' inutile continuare a cercare
                    b1=True
                    
            if j is len(nodes_seq):
                #espandi la sequenza seq
                print("\nTrovata una sequenza, espandendo...")
                n +=1
                tot_time = nodes_seq1[n].get_time_to()
                
                while n < len(nodes_seq1) and tot_time <= time_thr:
                    #copia seq
                    exp_seq= Sequence()
                    for node in nodes_seq:
                        tmp_node=Node( node.get_clust_id(), node.get_time_to(), node.get_num_staypoints(), node.get_leav_time() )
                        exp_seq.add_node(tmp_node)
                    #espandi
                    new_node=Node( nodes_seq1[n].get_clust_id(), nodes_seq1[n].get_time_to(), 
                                  nodes_seq1[n].get_num_staypoints(), nodes_seq1[n].get_leav_time() )
                    exp_seq.add_node(new_node)
                    #controlla che sia in seq2, se si aggiungi
                    if seq1_in_seq2(exp_seq, seq2, eps):
                        extended_set.add(exp_seq)
                    #cerca altre sequenze
                    n+= 1
                    tot_time += nodes_seq1[n].get_time_to()
                
        i +=1 #incrementa il primo while
    
    return extended_set()


def prune_sequence(sequence_set, extended_set):
    """
    elimina le sequenze di sequence_set che sono incluse nelle sequenze di extended_set
    """
    tmp_set= set()
    print("\nInizio pruning")
    for seq in sequence_set:
        #se una sotto-sequenza e' trovata viene ignorata, altrimenti e' aggiunta al set temporaneo
        found=False
        for ext in extended_set:
            if seq1_in_seq2(seq, ext, 0): #eps e' 0 perche' le sequenze sono identiche
                found=True
                break
        if not found:
            tmp_set.add(seq)
    print("\nPruning effettuato")
    #alla fine aggiungi tutto il set esteso, si puo' includere nel ciclo precedente
    for ext in extended_set:
        tmp_set.add(ext)
    return tmp_set







