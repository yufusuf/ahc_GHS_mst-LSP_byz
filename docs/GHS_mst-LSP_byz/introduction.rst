.. include:: substitutions.rst

Introduction
============
In this document two fundamental algorithms in the domain of distributed systems are presented: the Gallager-Humblet-Spira (GHS) algorithm and the Lamport-Shostak-Pease (LSP) broadcast algorithm. The GHS algorithm is devised to efficiently construct minimum spanning trees (MSTs) within connected, undirected graphs, optimizing connectivity while minimizing resource utilization. It offers a decentralized approach to MST construction, crucial for large-scale distributed systems becuase it has potential to optimize messaging costs within networks. On the other hand, the LSP broadcast algorithm ensures reliable and ordered message dissemination among processes in distributed systems, essential for maintaining system-wide consistency and facilitating coordinated communication. By exploring the workings, significance, and implications of these algorithms, this paper aims to provide insights into their roles and their implementations.

.. admonition::  Gallager-Humblet-Spira (GHS) minimum spanning tree algorithm 

    The primary problem addressed by the GHS algorithm is the efficient construction of a minimum spanning tree within a connected, undirected graph. This entails determining the optimal set of edges that connect all vertices of the graph while minimizing the total edge weight. This algorithm is essentialy the distributed version of the Kruskal's minimum spanning tree algorithm. In the context of distributed computing it is more difficult to identify outgoing edges from fragments (connected sub-graph of mst). First, for one process to determine whether they are in the same fragment, communication is necessary. Next, they need to collaborate to find the lowest-weight outgoing edge for the fragment. Lastly, the fragment on the other side of the edge needs to be informed for the merging of these fragments. [Fokking2013]_. 
    
    Solving the problem of constructing a minimum spanning tree is crucial for network management and communication efficiency in distributed systems. By efficiently establishing optimal connectivity, the GHS algorithm enables streamlined data transmission, resource utilization, ultimately enhancing system reliability and performance. One use case of this algorithm is to find optimal broadcasting on a network. Failure to address this problem can lead to suboptimal network configurations, increased resource overhead, and diminished system efficiency.

    Naive approaches to MST construction in distributed systems often fail due to challenges such as concurrency management, message ordering, synchronization, fault tolerance, and scalability. One example might be using a basic flooding algorithm to broadcast messages, by finding an mst this operation would utilize resources much more efficiently. The complexities mentioned arise from the decentralized and asynchronous nature of distributed environments, necessitating sophisticated algorithms like GHS to navigate the inherent challenges effectively.

    Previous approaches to MST construction may have been hindered by limitations in scalability, fault tolerance, or adaptability to dynamic environments. The GHS algorithm distinguishes itself by offering a decentralized, fault-tolerant approach to MST construction, effectively addressing the challenges posed by distributed systems while ensuring scalability and efficiency.

    The GHS algorithm employs a distributed methodology for constructing minimum spanning trees, utilizing message passing, merging strategies, and incremental tree construction. While the algorithm offers scalability, it may encounter limitations in highly dynamic environments or scenarios with frequent network disruptions.

.. admonition:: Lamport-Shostak-Pease (LSP) broadcast algorithm

   The primary problem tackled by the LSP broadcast algorithm is the components within a system may fail in unpredictable ways, leading to inconsistencies in system behavior and communication. The difficulty lies in achieving consensus among the system's components, even when some of them are faulty or malicious. The Byzantine fault problem is not only theoretically intriguing but also practically significant. Solving this problem is crucial for ensuring the reliability and resilience of distributed systems in various domains, including finance, telecommunications, and healthcare.

   Naive approaches to fault tolerance, such as relying solely on redundancy or cryptographic methods, often fall short in the face of Byzantine failures. The unpredictable behavior of faulty components and the lack of a centralized authority complicate the task of reaching consensus among distributed nodes.
   
   There exist various algorithms designed to handle crash failures, which function by recognizing the absence of messages from a crashed process within a specified timeframe. However, detecting Byzantine processes poses a significantly greater challenge due to their ability to continue sending messages. In general, identifying whether a process is deviating from the specified behavior of the distributed algorithm being executed is far from straightforward [Fokking2013]_. Consequently, achieving a consensus algorithm that consistently terminates correctly in the presence of Byzantine processes requires a different approach: synchronizing the network. By imposing synchronicity on the network, there is a guarantee of an upper bound on the consideration of messages. This ensures that consensus can be reached within a finite timeframe [Fokking2013]_.

   Lamport-Shostak-Pease algorithm works for networks where if number of rogue processes are less than third of the all processes. Then on an assumed synchronous network non-malicious processes can decide on a value with LSP broadcast algorithm.

Our primary contributions consist of the following for both algorithms:

- Detailed implementation of the algorithms on the AHCv2 platform.
- Performance evaluation of the algorithms across diverse network topologies and usage scenarios.
- Comparative analysis of the algorithms with previous approaches, highlighting strengths, weaknesses, and key insights.

.. [Fokking2013] Wan Fokkink, Distributed Algorithms An Intuitive Approach, The MIT Press Cambridge, Massachusetts London, England, 2013
