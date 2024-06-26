
# __author__ = "One solo developer"
# __authors__ = ["Mahmoud Alasmar"]
# __contact__ = "mahmoud.asmar@metu.edu.tr"
# __date__ = "2024/05/26"
# __license__ = "GPLv3"
# __maintainer__ = "developer"
# __status__ = "Production"
# __version__ = "0.0.1"

import matplotlib.pyplot as plt
import networkx as nx
import time
from adhoccomputing.GenericModel import GenericModel
from adhoccomputing.Generics import Event, EventTypes, ConnectorTypes
from adhoccomputing.Experimentation.Topology import Topology
from adhoccomputing.Networking.LinkLayer.GenericLinkLayer import GenericLinkLayer
from adhoccomputing.Networking.NetworkLayer.GenericNetworkLayer import GenericNetworkLayer
from adhoccomputing.DistributedAlgorithms.Waves.AwerbuchDFS import WaveAwerbuchComponent
from adhoccomputing.Networking.LogicalChannels.GenericChannel import GenericChannelWithLoopback, GenericChannel
from adhoccomputing.DistributedAlgorithms.Election.Spira import ElectionSpiraComponent
from GallagerHumbletSpira import MinimumSpanningTreeGHSComponent
from LamportShostakPeaseBroadcast import LamportShostakPeaseBroadcast
from KruskalTest import *

number_mesg = 0
topo = Topology()


class AdHocNode(GenericModel):

    def on_init(self, eventobj: Event):
        print(
            f"Initializing {self.componentname}.{self.componentinstancenumber}")

    def on_message_from_top(self, eventobj: Event):
        self.send_down(Event(self, EventTypes.MFRT, eventobj.eventcontent))

    def on_message_from_bottom(self, eventobj: Event):
        self.send_up(Event(self, EventTypes.MFRB, eventobj.eventcontent))

    def __init__(self, componentname, componentid, topology=None):
        super().__init__(componentname, componentid, topology=topo)
        self.components = []
        # SUBCOMPONENTS
        self.appllayer = MinimumSpanningTreeGHSComponent(
            "ApplicationLayer", componentid, topology=topology)
        self.netlayer = GenericNetworkLayer(
            "NetworkLayer", componentid, topology=topology)
        self.linklayer = GenericLinkLayer("LinkLayer", componentid)
        self.components.append(self.appllayer)
        self.components.append(self.netlayer)
        self.components.append(self.linklayer)

        # CONNECTIONS AMONG SUBCOMPONENTS
        self.appllayer.connect_me_to_component(
            ConnectorTypes.DOWN, self.netlayer)
        self.netlayer.connect_me_to_component(
            ConnectorTypes.UP, self.appllayer)
        self.netlayer.connect_me_to_component(
            ConnectorTypes.DOWN, self.linklayer)
        self.linklayer.connect_me_to_component(
            ConnectorTypes.UP, self.netlayer)

        # Connect the bottom component to the composite component....
        self.linklayer.connect_me_to_component(ConnectorTypes.DOWN, self)
        self.connect_me_to_component(ConnectorTypes.UP, self.linklayer)


def main():

    # run several times to see result, sometimes deadlocks occur
    # you should see the branch edges with green text
    # n = 10
    # G = nx.Graph()
    # for i in range(n):
    #     G.add_node(i)

    # G.add_edge(0, 1, weight=5)
    # G.add_edge(0, 3, weight=6)
    # # G.add_edge(0, 4, weight=1)
    # G.add_edge(1, 2, weight=14)
    # G.add_edge(1, 3, weight=7)
    # G.add_edge(1, 4, weight=8)
    # G.add_edge(2, 4, weight=19)
    # G.add_edge(2, 3, weight=32)

    # G.add_edge(0, 1, weight=5)
    # G.add_edge(0, 2, weight=9)
    # G.add_edge(0, 3, weight=11)
    #
    # G.add_edge(1, 3, weight=7)
    # G.add_edge(1, 4, weight=15)
    #
    # G.add_edge(2, 3, weight=3)
    #

    # w = 50
    # for i in range(n):
    #     for j in range(i):
    #         if i*j % 2 == 1:
    #             G.add_edge(i, j, weight=w)
    #         w += 1
    # DISTRIBUTED TEST
    start = time.time()
    w = 50
    n = 80
    G = nx.random_geometric_graph(n, 0.5)
    for (u, v) in G.edges():
        G.edges[u, v]['weight'] = w
        w += 1
    options = {'font_size': 15,
               'node_size': 800,
               }

    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, **options)
    # labels = nx.get_edge_attributes(G, 'weight')
    # nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, **options)

    topo.construct_from_graph(G, AdHocNode, GenericChannel)
    topo.start()
    end = time.time()

    plt.savefig("graph.png")
    plt.show()  # while (True): pass

    # KRUSKALS FOR VERIFICATION
    # print("===== KRUSKAL TEST =====")
    # g = Graph(n)
    # w = 60
    # for (u, v) in G.edges():
    #     g.addEdge(u, v, w)
    #     w += 1
    # # Function call
    # g.KruskalMST()
    print(f"Time: {end - start}")


if __name__ == "__main__":
    main()
