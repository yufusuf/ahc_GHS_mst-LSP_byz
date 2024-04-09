.. include:: substitutions.rst

|GHS_mst-LSP_byz|
=========================================



Background and Related Work
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Present any background information survey the related work. Provide citations.

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
        :linenos:
        :caption: lsp algorithm _[Fokking2013]
Example
~~~~~~~~

Provide an example for the distributed algorithm.

Correctness
~~~~~~~~~~~

Present Correctness, safety, liveness and fairness proofs.


Complexity 
~~~~~~~~~~

Present theoretic complexity results in terms of number of messages and computational complexity.





    
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
