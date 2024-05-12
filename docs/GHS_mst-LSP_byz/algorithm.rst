.. include:: substitutions.rst

|GHS_mst-LSP_byz|
=========================================



Background and Related Work
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Distributed minimum spanning tree (MST) algorithms are designed to efficiently construct a minimum spanning tree in a decentralized network, where nodes communicate and collaborate to collectively form the tree structure without centralized coordination. The goal is to connect all nodes in the network with the minimum total weight of edges, ensuring efficient communication and connectivity.

In traditional centralized MST algorithms like Kruskal's and Prim's, a single processor or node manages the construction of the MST using global information about edge weights and connectivity. However, in distributed settings, each node only has partial knowledge of the network topology and must communicate with neighboring nodes to collaboratively determine the MST.

Several distributed MST algorithms have been developed to address these challenges, including variations of classical MST algorithms adapted for distributed environments such as Borůvka's algorithm, Prim's algorithm, and Kruskal's algorithm. Additionally, specialized algorithms like the Gallager-Humblet-Spira (GHS) algorithm are designed specifically for distributed execution, using techniques like fragment identification and merging to construct the MST efficiently.

These algorithms are essential for various distributed computing applications, including network routing, resource allocation, and fault-tolerant communication systems, where efficient and reliable network connectivity is crucial. Understanding the principles and intricacies of distributed MST algorithms is fundamental for designing and implementing robust distributed systems.

The Lamport-Shostak-Pease (LSP) algorithm, proposed by Leslie Lamport, Marshall Shostak, and Robert Pease, is a seminal algorithm for solving the Byzantine Generals' Problem in distributed computing. The Byzantine Generals' Problem involves a scenario where a group of generals, each commanding a portion of a Byzantine army, must coordinate their attack or retreat plans via messengers. The challenge arises when some generals may be traitorous (Byzantine), providing conflicting information or deliberately misleading messages.

The goal of the Byzantine Generals' Problem is to achieve consensus among the loyal generals despite the potential presence of Byzantine traitors. The LSP algorithm demonstrates how a distributed system can reach agreement even in the presence of Byzantine faults, provided that a strict majority (more than two-thirds) of the participants are honest and reliable.

Key features of the LSP algorithm include:

    **Reliable Consensus:** The algorithm ensures that loyal generals agree on a common plan of action (attack or retreat) despite the presence of Byzantine traitors attempting to disrupt the consensus.

    **Majority Voting:** By leveraging a strict majority (more than two-thirds) of honest generals, the algorithm guarantees that the loyal generals can outvote and ignore conflicting or malicious messages from the traitorous minority.

Distributed Algorithm: |GHS_mst-LSP_byz| 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. admonition:: Algorithm Definition

    **Gallager-Humblet-Sphira Algorithm:**

    The GHS minimum spanning tree :ref:`Algorithm <MinimumSpanningTree>` [Gallager1983]_ , proposed by  Gallager, Humblet and Spira, aims to find a minimum spanning tree over connected network. Each node knows its edge weights initially.


    state(SN) of the nodes:

    1. **sleep:** state of the nonitiators
    2. **find:** state of process looking to find its lowest-weight outgoing edge.
    3. **found:** state of process has found its lowest-weight outoing edge


    edge types(SE):

    1. **basic:** undecided wheter the edge is part of mst or not
    2. **branch:** part of mst
    3. **rejected:** not part of mst

    fragments:

    1. each fragment has assigned a level(LN) and id(FN).

    message types:
    
    1. **connect**
    2. **initiate**
    3. **test**
    4. **report**
    5. **accept**
    6. **reject**
    7. **change-root**



    .. _MinimumSpanningTree:

    .. code-block:: RST
        :linenos:
        :caption: GHS minimum spanning tree algorithm [Gallageri1983]_.

        Procedure Wakeup:
            Select edge m with minimum weight
            Set SE(m) to Branch
            Set LN to 0
            Set SN to Found
            Initialize find-count to 0
            Send Connect(0) on edge m

        Procedure OnReceiveConnect(L, edge j):
            If SN equals Sleeping:
                Execute Wakeup
            If L < LN:
                Set SE(j) to Branch
                Send Initiate(LN, FN, SN) on edge j
                If SN equals Find:
                    Increment find-count
            Else if SE(j) equals Basic:
                Queue the message
            Else:
                Send Initiate(LN + 1, w(j), Find) on edge j

        Procedure OnReceiveInitiate(L, F, S, edge j):
            Set LN to L
            Set FN to F
            Set SN to S
            Set in-branch to j
            Set best-edge to nil
            Set best-wt to infinity
            For each edge i != j with SE(i) equals Branch:
                Send Initiate(L, F, S) on edge i
                If S equals Find:
                    Increment find-count
            If S equals Find:
                Execute Test

        Procedure Test:
            If there is an adjacent edge in Basic state:
                Set test-edge to the minimum-weight adjacent edge in Basic state
                Send Test(LN, FN) on test-edge
            Else:
                Set test-edge to nil
                Execute Report

        Procedure OnReceiveTest(L, F, edge j):
            If SN equals Sleeping:
                Execute Wakeup
            If L > LN:
                Queue the message
            Else if F != FN:
                Send Accept on edge j
            Else:
                If SE(j) equals Basic:
                    Set SE(j) to Rejected
                If test-edge equals j:
                    Send Reject on edge j
                Else:
                    Execute Test

        Procedure OnReceiveAccept(edge j):
            Set test-edge to nil
            If w(j) < best-wt:
                Set best-edge to j
                Set best-wt to w(j)
            Execute Report

        Procedure OnReceiveReject(edge j):
            If SE(j) equals Basic:
                Set SE(j) to Rejected
            Execute Test

        Procedure Report:
            If find-count equals 0 and test-edge is nil:
                Set SN to Found
                Send Report(best-wt) on in-branch

        Procedure OnReceiveReport(w, edge j):
            If j != in-branch:
                Decrement find-count
                If w < best-wt:
                    Set best-wt to w
                    Set best-edge to j
                Execute Report
            Else:
                If SN equals Find:
                    Queue the message
                Else if w > best-wt:
                    Execute ChangeRoot
                Else if w equals best-wt equals infinity:
                    Halt the execution

        Procedure ChangeRoot:
            If SE(best-edge) equals Branch:
                Send ChangeRoot on best-edge
            Else:
                Send Connect(LN) on best-edge
                Set SE(best-edge) to Branch

        Procedure OnReceiveChangeRoot:
            Execute ChangeRoot    


    **Lamport-Shostak-Pease Algorithm:**

    .. _LSPbroadcast:

    .. code-block:: RST

        Procedure Broadcast(m):
            If isLeader:
                send every value to other node
            Else:
                execute Broadcast(m-1), which will cause every other node to act as a commander and send its value
                execute Decide()

        Procedure Decide():
            Decide on value from based on majority of values received from every other node in older executions of the algorithm.
            



Example
~~~~~~~~
    **Gallager Humblet Spira**

    .. image:: ./figures/graph.png
       :alt: Graph
    set every node as an initiator  MinimumSpaningTree algorithm proceeds as follows:

    - `0` and `1` sends <**connect**, 0> to each other. They both make channel 01 a branch edge. Since
      they are at the same level they send <**initiate**, 5, 1, `find`> to each other. Next `0` and `1` send <**test**, 5, 1> to `2` and `3` respectively

    - `4` sends  <**connect**, 0>  to `1`, making channel 14 a branch edge. Since fragment at `1` is at level 1, `1` replies with <**initiate**, 5, 1>, then `4` sends <**report**, infinity> to its new parent `1`.

    - `2` and `3` sends <**connect**, 0> to each other. They both make channel 23 a branch edge. Since
      they are at the same level they send <**initiate**, 3, 1, find> to each other. Next `2` and `3` send <**test**, 3, 1> to `0` and `1` respectively.

    - Since the fragments of `2` and `3` are at the same level as the fragments of `0` and `1`, but have a different name, `2` and `3` reply to the test message from `0` and `1`, respectively, with an accept message. As a result, `0` sends to <**report**, 9> its parent `1`, while `1` sends <**report**, 7> to its parent `0`. Because 7 is smaller than 9, `1` sends <**connect**, 1> to `3`.

    - Since the fragments of `1` and `0` are at the same level as the fragments of `2` and `3` but have a different name, `0` and `1` can reply to the test message from `2` and `3` respectively, with an accept message. As a result, `3` sends <**report**, 7> to its parent `2` while `2` sends <**report**, 9> to its parent `3`. As 7 is smaller than 9, `3` sends <**connect**, 1> to `1`.

    - By the crossing <**connect**, 1> messages between `1` and `3`, the channel between these processes becomes a branch edge as well as the core edge of the new fragment, which has level 2. Messages <**initiate**, 7, 2, find> are forwarded through the branch edges. The channels 03 and 02 are tested (in this order) from either side, both times leading to a reject. Finally, all processes report infinity, and the algorithm terminates.

    Example source: [Fokking2013]_


   example run of algorithm generated by ahc library:

   .. image:: ./figures/example_mst_run.png
    

    

   **Lamport Shostak Pease**

    Consider a fully connected network comprising four processes: g, p, q, r, and a constant k=1. Let's examine one possible execution of the Lamport-Shostak-Pease broadcast algorithm with Broadcast(1) on this network scenario.

    During pulse 1, the general g broadcasts and makes a decision for the value 1. Consequently, after pulse 1, both lieutenants p and q adopt the value 1. These lieutenants construct a multiset (1, 1, b), incorporating the outcomes of three recursive calls of Broadcast(0) involving the processes p, q, and r. Here, b can differ between p and q due to potential variations in their computations within Broadcast(0).

    Given that the majority of values in these multisets are 1, both p and q subsequently decide on the value 1.

    example run of algorithm generated by ahc library:

    .. image:: ./figures/lsp_example_run.png

Correctness
~~~~~~~~~~~

    **Gallager Humblet Spira** 

    To simplify, we assume that each channel in the network has a distinct weight, ensuring that the minimum spanning tree is unique. Alternatively, we could permit channels to share the same weight and establish a specific ordering for such cases by using the IDs of the channel endpoints. The Gallager-Humblet-Spira algorithm is a decentralized adaptation of Kruskal's renowned algorithm for computing minimum spanning trees, originally devised for single-processor systems. Briefly describing Kruskal’s algorithm, it partitions the graph into fragments—connected subgraphs of the minimum spanning tree. Within this framework, a channel in the network is considered an outgoing edge for a fragment if only one of the connected processes belongs to that fragment. Kruskal's approach relies on the observation that the smallest-weight outgoing edge c of a fragment F is always included in the minimum spanning tree. If this were not true, extending the minimum spanning tree to incorporate c would introduce a cycle encompassing both c and another outgoing edge d from F. Substituting d with c in the minimum spanning tree would yield an alternative spanning tree of the network with a reduced total weight of its edges compared to the original minimum spanning tree, leading to a contradiction [Fokking2013]_ . Following this, when we find the minimum outgoing edges from distributed nodes we can form an mst.



Complexity 
~~~~~~~~~~

    **Gallager Humblet Spira** 

    The worst-case message complexity of the GHS (Gallager, Humblet, and Spira) algorithm is characterized by its dependence on both the number of edges (E) and the number of nodes (N) in the graph, denoted as O(E + N log N).

    The term E in this complexity formula accounts for the total number of messages resulting from the rejection of channels during the execution of the algorithm. Specifically, each channel that exists outside the minimum spanning tree (MST) is processed through either a test-reject or test-test pair, generating up to 2(E - (N-1)) messages in total. [Fokking2013]_

    Furthermore, the factor N log N arises from the interactions related to the initiation of processes and the subsequent message exchanges. Each process receives at most log N join (initiate) messages as the algorithm progresses. With each initiation, the level of a process increases within the algorithm's execution.

    Notably, a fragment at level l within the algorithm contains at least 2^l nodes. As processes receive initiate messages, they respond with various actions, such as tests triggering accepts, reports, changeroot, and connect operations. The cumulative effect of these interactions leads to a maximum of 5N log N messages throughout the execution of the algorithm.

    In summary, the O(E + N log N) message complexity of the GHS algorithm encapsulates the message exchanges required for channel rejection and process interactions, considering the structure and connectivity of the graph in relation to the MST and process levels. This complexity analysis provides insights into the computational overhead and communication requirements associated with executing the GHS algorithm on a given graph topology.

    **Lamport Shostak Pease**

    This algorithm becomes quite costly because of its recursive design, particularly when dealing with large-scale networks and when k>2. The requirement for the network topology to be fully connected and to broa cast extensively leads to a substantial increase in the total number of messages exchanged between nodes. Consequently, the total message count can grow to the order of n^k, where n represents the number of nodes in the network, and k number of byzantine nodes.
    





    
.. 
    **Example**

    DRAW FIGURES REPRESENTING THE EXAMPLE AND EXPLAIN USING THE FIGURE. Imagine a distributed system with three processes, labeled Process A, Process B, and Process C, connected by communication channels. When Process A initiates a snapshot, it sends a marker along its outgoing channel. Upon receiving the marker, Process B marks its local state and forwards the marker to Process C. Similarly, Process C marks its state upon receiving the marker. As the marker propagates back through the channels, each process records the messages it sends or receives after marking its state. Finally, once the marker returns to Process A, it collects the markers and recorded states from all processes to construct a consistent global snapshot of the distributed system. This example demonstrates how the Chandy-Lamport algorithm captures a snapshot without halting the system's execution, facilitating analysis and debugging in distributed environments.


    .. **Correctness:**
    
    .. *Termination (liveness)*: As each process initiates a snapshot and sends at most one marker message, the snapshot algorithm activity terminates within a finite timeframe. If process p has taken a snapshot by this point, and q is a neighbor of p, then q has also taken a snapshot. This is because the marker message sent by p has been received by q, prompting q to take a snapshot if it hadn't already done so. Since at least one process initiated the algorithm, at least one process has taken a snapshot; moreover, the network's connectivity ensures that all processes have taken a snapshot [Tel2001]_.

    .. *Correctness*: We need to demonstrate that the resulting snapshot is feasible, meaning that each post-shot (basic) message is received during a post-shot event. Consider a post-shot message, denoted as m, sent from process p to process q. Before transmitting m, process p captured a local snapshot and dispatched a marker message to all its neighbors, including q. As the channels are FIFO (first-in-first-out), q received this marker message before receiving m. As per the algorithm's protocol, q took its snapshot upon receiving this marker message or earlier. Consequently, the receipt of m by q constitutes a post-shot event [Tel2001]_.

    .. **Complexity:**

    1. **Time Complexity**  The Chandy-Lamport :ref:`Algorithm <ChandyLamportSnapshotAlgorithm>` takes at most O(D) time units to complete where D is ...
    2. **Message Complexity:** The Chandy-Lamport :ref:`Algorithm <ChandyLamportSnapshotAlgorithm>` requires 2|E| control messages.


    .. **Lai-Yang Snapshot Algorithm:**

    The Lai-Yang algorithm also captures a consistent global snapshot of a distributed system. Lai and Yang proposed a modification of Chandy-Lamport's algorithm for distributed snapshot on a network of processes where the channels need not be FIFO. ALGORTHM, FURTHER DETAILS

.. [Fokking2013] Wan Fokkink, Distributed Algorithms An Intuitive Approach, The MIT Press Cambridge, Massachusetts London, England, 2013
.. [Tel2001] Gerard Tel, Introduction to Distributed Algorithms, CAMBRIDGE UNIVERSITY PRESS, 2001
.. [Lamport2019] Lamport, L., Shostak, R., & Pease, M. (2019). The Byzantine generals problem. In Concurrency: the works of leslie lamport (pp. 203-226).
.. [Gallager1983] Gallager, R. G., Humblet, P. A., & Spira, P. M. (1983). A distributed algorithm for minimum-weight spanning trees. ACM Transactions on Programming Languages and systems (TOPLAS), 5(1), 66-77.
