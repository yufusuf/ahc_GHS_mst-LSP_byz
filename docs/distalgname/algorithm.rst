.. include:: substitutions.rst

|DistAlgName|
=========================================



Background
~~~~~~~~~~

|release|

Present any background information if needed.

Distributed Algorithm: |DistAlgName| 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

An example distributed algorithm for broadcasting on an undirected graph is presented in Algorithm~\ref{alg:blindflooding}.

.. code-block:: RST
    :linenos:

    Implements: BlindFlooding Instance: cf
    Uses: LinkLayerBroadcast Instance: lbc
    Events: Init, MessageFromTop, MessageFromBottom
    Needs:

    OnInit: () do
    
    OnMessageFromBottom: ( m ) do
        Trigger lbc.Broadcast ( m )
    
    OnMessageFromTop: ( m ) do
        Trigger lbc.Broadcast ( m )


Do not forget to explain the algorithm line by line in the text.

Example
~~~~~~~~

Provide an example for the distributed algorithm.

Correctness
~~~~~~~~~~~

Present Correctness, safety and liveness proofs.


Complexity 
~~~~~~~~~~

Present theoretic complexity results in terms of number of messages and computational complexity.








