.. include:: substitutions.rst

Implementation, Results and Discussion
======================================

Implementation and Methodology
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To implement the Minimum Spanning Tree (MST) algorithm, we developed a simulation within a Python environment emulating an ad hoc network setting. In this simulation, each node was represented as an individual process capable of communication through a custom messaging system. The central focus of this implementation was the creation and handling of specific message types, including INITIATE, CONNECT, TEST, REPORT, ACCEPT, and REJECT messages.

The simulation was designed to validate the algorithm's functionality across two distinct network topologies: fully connected and randomized networks. In the fully connected topology, every node had direct communication links with every other node, simulating a dense network structure. Conversely, the randomized network topology featured varying degrees of connectivity and randomness, reflecting real-world ad hoc network scenarios.

The performance of the implemented MST algorithm was rigorously evaluated and analyzed in the results section. This evaluation considered metrics such as message complexity, convergence time. Also, to check if the found mst was correct, classical Kruskal's algorithm ran on network to compare results. 

For LSP i could only be able to implement where k = 1, because I couldnt find a simple way to implement complex recursive steps taken to compute the broadcasting without the help of keeping global states across network in ahc library. This led to solutions to trivial cases of mitigation of 1 byzantine node in N>3 nodes of networks.

Results
~~~~~~~~

The implementation was evaluated using an Intel i5-12400F processor. Convergence time and message complexity were measured and recorded in a table for analysis. The evaluation utilized the NetworkX library to simulate two distinct network topologies: a random graph and a fully connected graph. The fully connected graph, where nodes communicate extensively, resulted in increased message passing and longer convergence times compared to the random graph topology where not every node is connected to each other.

.. list-table:: GHS algorithm performance and message complexity
   :widths: 25 25 25 25 25
   :header-rows: 1

   * - node count 
     - time(random-graph) 
     - time(fully-connected) 
     - message count(random-graph)
     - message count(fully-connected)
   * - 10 
     - 0.2
     - 0.2
     - 76
     - 114
   * - 40 
     - 0.4
     - 0.5
     - 783
     - 1589
   * - 50 
     - 0.5
     - 0.82
     - 1089
     - 2430
   * - 60 
     - 0.77
     - 0.8
     - 1615
     - 3585
   * - 80 
     - 1.6
     - 2.26
     - 3040
     - 6340


Discussion
~~~~~~~~~~

The results of the study demonstrate the effectiveness of the GHS algorithm for constructing minimum spanning trees (MSTs) across various network topologies. By implementing the GHS algorithm in simulated ad hoc networks with different structures, including fully connected and random graphs, we observed its capability in efficiently identifying MSTs.

Furthermore, the evaluation validated the theoretical computations regarding message counts associated with the GHS algorithm. The measured message complexity aligned with the expected theoretical values, affirming the algorithm's computational efficiency and correctness in terms of message exchange.

Overall, the findings underscore the practical utility and reliability of the GHS algorithm for MST construction, offering valuable insights into its performance across diverse network configurations. Further exploration could focus on optimizing the algorithm's execution and scalability for larger network sizes and complex topologies.


