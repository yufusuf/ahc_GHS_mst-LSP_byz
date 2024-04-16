from enum import Enum
from adhoccomputing.Generics import *
from adhoccomputing.GenericModel import GenericModel, GenericMessageHeader, GenericMessage
from adhoccomputing.Networking.LogicalChannels.GenericChannel import GenericChannelWithLoopback
import networkx as nx
import matplotlib.pyplot as plt
import sys

INF = sys.maxsize


class ApplicationLayerMessageTypes(Enum):
    INITIATE = "INITIATE"
    ACCEPT = "ACCEPT"
    CONNECT = "CONNECT"
    REPORT = "REPORT"
    TEST = "TEST"
    REJECT = "REJECT"
    CHANGEROOT = "CHANGEROOT"
    TERMINATE = "TERMINATE"


class NodeStatus(Enum):
    FIND = "FIND"
    FOUND = "FOUND"


class EdgeStatus(Enum):
    BASIC = "BASIC"
    BRANCH = "BRANCH"
    REJECTED = "REJECTED"


class Edge:
    def __init__(self, weight):
        self.weight = weight
        self.st = EdgeStatus.BASIC

    def change_state(self, st):
        self.st = st

    def __str__(self):
        return f"({self.weight}, {self.st})"
    __repr__ = __str__


class MinimumSpanningTreeGHSComponent(GenericModel):
    """
    Class for Minimum spanning tree implementation using GallagerHumbletSpira, ahc model
    """

    def __init__(self, componentname, componentinstancenumber, context=None, configurationparamters=None, num_worker_threads=1, topology=None):
        super().__init__(componentname, componentinstancenumber, context,
                         configurationparamters, num_worker_threads, topology)
        """
        constructor for MST model
        """
        self.parent = self.componentinstancenumber
        self.id = self.componentinstancenumber
        self.topology = topology
        self.connectq = []
        self.testq = []
        self.terminated = False

        # self.eventhandlers["test"] = self.test_handler
        # self.eventhandlers["connect"] = self.connect_handler

        # neighbor_id: (edge_weight, edge_status)
        self.edges: dict[int, Edge] = {}

        graph_edges = nx.get_edge_attributes(self.topology.G, 'weight')
        for node1, node2 in graph_edges:
            if node1 == self.id:
                self.edges[node2] = Edge(graph_edges[(node1, node2)])
            elif node2 == self.id:
                self.edges[node1] = Edge(graph_edges[(node1, node2)])

        self.fn = 0
        self.level = 0
        self.count = 0
        self.test_edge = -1
        self.best_edge = -1
        self.parent_report = 0
        self.best_weight = INF
        self.status = NodeStatus.FIND

    def find_lowest_weight_edge(self):
        """
        Returns the node that connected by lowest weight edge from the current node

        :return: `id` of the node that connected by this node
        """
        min = -1
        min_weight = INF

        for id in self.edges:
            if self.edges[id].weight < min_weight:
                min = id
                min_weight = self.edges[id].weight
        return min

    def find_lowest_weight_basic_edge(self):
        """
        Returns the node that connected by lowest weight basic edge from the current node

        :return: `id` of the node that connected by this node
        """
        min = -1
        min_weight = INF
        for id in self.edges:
            if self.edges[id].st == EdgeStatus.BASIC:
                if self.edges[id].weight < min_weight:
                    min = id
                    min_weight = self.edges[id].weight
        return min

    def prepare_test_message(self, destination, fn, level):
        hdr = GenericMessageHeader(ApplicationLayerMessageTypes.TEST,
                                   self.id,
                                   destination)
        payload = (fn, level)
        msg = GenericMessage(hdr, payload)
        return msg

    def prepare_payload(self, msg_type, destination, payload):
        """
        Prepares a payload to be sent to other nodes

        :param msg_type: :class:`ApplicationLayerMessageTypes`
        :param destination: id for the destination node
        :param payload: message to be sent

        """
        hdr = GenericMessageHeader(msg_type,
                                   self.id,
                                   destination)
        msg = GenericMessage(hdr, payload)
        return msg

    def on_init(self, eventobj: Event):
        self.status = NodeStatus.FOUND
        lowest_weight_edge = self.find_lowest_weight_edge()
        print(self.id, lowest_weight_edge)
        self.edges[lowest_weight_edge].change_state(EdgeStatus.BRANCH)
        self.count = 1
        msg = self.prepare_payload(
            ApplicationLayerMessageTypes.CONNECT, lowest_weight_edge, 0)
        self.send_down(Event(self, EventTypes.MFRT, msg))

    # def prGreen(skk): print("\033[92m {}\033[00m" .format(skk))

    def print_edges(self):
        """
        Prints branch edges of the current node
        """
        print(
            f"\033[92m{self.id} branch edges:\033[00m", end=" ")
        for n in self.edges:
            if self.edges[n].st == EdgeStatus.BRANCH:
                print(f"\033[92m{n}\033[00m",
                      f"\033[92m{self.edges[n]}\033[00m", end=", ")
        print()

    def on_exit(self, eventobj: Event):
        # print branch edges to terminal
        self.print_edges()

    def on_message_from_bottom(self, eventobj: Event):
        # time.sleep(0.01)
        message = eventobj.eventcontent
        hdr = message.header
        if hdr.messagetype == ApplicationLayerMessageTypes.CONNECT:
            self.connect_handler(eventobj)
        elif hdr.messagetype == ApplicationLayerMessageTypes.INITIATE:
            self.iniate_handler(eventobj)
        elif hdr.messagetype == ApplicationLayerMessageTypes.TEST:
            self.test_handler(eventobj)
        elif hdr.messagetype == ApplicationLayerMessageTypes.REPORT:
            self.report_handler(eventobj)
        elif hdr.messagetype == ApplicationLayerMessageTypes.ACCEPT:
            self.accept_handler(eventobj)
        elif hdr.messagetype == ApplicationLayerMessageTypes.REJECT:
            self.reject_handler(eventobj)
        elif hdr.messagetype == ApplicationLayerMessageTypes.CHANGEROOT:
            self.changeroot_handler(eventobj)
        elif hdr.messagetype == ApplicationLayerMessageTypes.TERMINATE:
            if not self.terminated:
                self.terminate_handler(eventobj)

    def terminate_handler(self, eventobj: Event):
        message: GenericMessage = eventobj.eventcontent
        source = message.header.messagefrom
        print(
            f"Node {self.id} received TERMINATE message from Node {source}, payload: {message.payload}")
        self.do_terminate()

    def do_terminate(self):
        self.terminated = True
        for n in self.edges:
            if self.edges[n].st == EdgeStatus.BRANCH or True:
                msg = self.prepare_payload(
                    ApplicationLayerMessageTypes.TERMINATE, n, ())
                self.send_down(Event(self, EventTypes.MFRT, msg))
        self.print_edges()

    def connect_handler(self, eventobj: Event):
        message: GenericMessage = eventobj.eventcontent
        source = message.header.messagefrom
        level = message.payload
        print(
            f"Node {self.id} received CONNECT message from Node {source}, payload: {message.payload}")
        if level < self.level:
            self.edges[source].change_state(EdgeStatus.BRANCH)
            # send initiate to source node
            msg = self.prepare_payload(
                ApplicationLayerMessageTypes.INITIATE, source, (self.fn, self.level, self.state))
            self.send_down(Event(self, EventTypes.MFRT, msg))
        elif self.edges[source].st == EdgeStatus.BRANCH:
            # form a new core branch
            msg = self.prepare_payload(
                ApplicationLayerMessageTypes.INITIATE, source, (self.edges[source].weight, self.level + 1, NodeStatus.FIND))
            self.send_down(Event(self, EventTypes.MFRT, msg))
        else:
            # que the message back for later processing
            # hdr = GenericMessageHeader(ApplicationLayerMessageTypes.CONNECT,
            #                            source,
            #                            self.id)
            # payload = message.payload
            # msg = GenericMessage(hdr, payload)
            # self.send_down(Event(self, EventTypes.MFRT, msg))
            if (source, level) not in self.connectq:
                self.connectq.append((source, level))

    def iniate_handler(self, eventobj: Event):
        message: GenericMessage = eventobj.eventcontent
        source = message.header.messagefrom
        (fn, level, st) = message.payload
        print(
            f"Node {self.id} received INITIATE message from Node {source}, payload: {message.payload}")
        self.fn = fn
        self.level = level
        self.state = st
        self.best_edge = -1
        self.best_weight = INF
        self.parent_report = 0
        self.count = 1
        self.parent = source

        for m in self.connectq:
            (frm, oldlvl) = m
            if oldlvl < self.level:
                self.edges[frm].change_state(EdgeStatus.BRANCH)
                self.connectq.remove(m)

        for n in self.edges:
            if n == source:
                continue
            if self.edges[n].st == EdgeStatus.BRANCH:
                msg = self.prepare_payload(
                    ApplicationLayerMessageTypes.INITIATE, n, (fn, level, st))
                self.send_down(Event(self, EventTypes.MFRT, msg))

        for m in self.testq:
            (frm, tfn, tlvl) = m
            if tlvl <= self.level:
                self.reply_test(tfn, frm)
                self.testq.remove(m)

        if st == NodeStatus.FIND:
            self.do_test()

    def report_handler(self, eventobj):
        message: GenericMessage = eventobj.eventcontent
        source = message.header.messagefrom
        (weight) = message.payload
        print(
            f"Node {self.id} received REPORT message from Node {source}, payload: {message.payload}")
        if source != self.parent:
            self.count += 1
            if weight < self.best_weight:
                self.best_weight = weight
                self.best_edge = source
            self.do_report()
        elif self.state == NodeStatus.FIND:
            self.parent_report = weight
        else:
            if self.best_weight < weight:
                self.do_changeroot()
            elif weight == INF:
                self.do_terminate()

    def do_report(self):
        if self.count == sum([int(self.edges[n].st == EdgeStatus.BRANCH) for n in self.edges]) and self.test_edge == -1:
            self.state = NodeStatus.FOUND
            msg = self.prepare_payload(
                ApplicationLayerMessageTypes.REPORT, self.parent, (self.best_weight))
            self.send_down(Event(self, EventTypes.MFRT, msg))
            if self.parent_report > 0 and self.best_weight < self.parent_report:
                self.do_changeroot()

    def changeroot_handler(self, eventobj):
        self.do_changeroot()

    def do_changeroot(self):
        if self.edges[self.best_edge].st == EdgeStatus.BRANCH:
            msg = self.prepare_payload(
                ApplicationLayerMessageTypes.CHANGEROOT, self.best_edge, ())
            self.send_down(Event(self, EventTypes.MFRT, msg))
        else:
            self.edges[self.best_edge].change_state(EdgeStatus.BRANCH)
            msg = self.prepare_payload(
                ApplicationLayerMessageTypes.CONNECT, self.best_edge, (self.level))
            self.send_down(Event(self, EventTypes.MFRT, msg))
            if (self.best_edge, self.level) in self.connectq:
                msg = self.prepare_payload(ApplicationLayerMessageTypes.INITIATE, self.best_edge, (
                    self.best_weight, self.level+1, NodeStatus.FIND))
                self.connectq.remove((self.best_edge, self.level))

    def accept_handler(self, eventobj):
        message: GenericMessage = eventobj.eventcontent
        source = message.header.messagefrom
        print(
            f"Node {self.id} received ACCEPT message from Node {source}, payload: {message.payload}")
        self.test_edge = -1
        if self.edges[source].weight < self.best_weight:
            self.best_weight = self.edges[source].weight
            self.best_edge = source
        self.do_report()

    def reject_handler(self, eventobj):
        message: GenericMessage = eventobj.eventcontent
        source = message.header.messagefrom
        print(
            f"Node {self.id} received REJECT message from Node {source}, payload: {message.payload}")
        self.edges[source].st = EdgeStatus.REJECTED
        self.do_test()

    def test_handler(self, eventobj):
        message: GenericMessage = eventobj.eventcontent
        source = message.header.messagefrom
        (fn, level) = message.payload
        print(
            f"Node {self.id} received TEST message from Node {source}, payload: {message.payload}")
        if level <= self.level:
            self.reply_test(fn, source)
        else:
            # hdr = GenericMessageHeader(ApplicationLayerMessageTypes.TEST,
            #                            source,
            #                            self.id)
            # payload = message.payload
            # msg = GenericMessage(hdr, payload)
            # self.send_down(Event(self, EventTypes.MFRT, msg))

            if (source, fn, level) not in self.testq:
                self.testq.append((source, fn, level))

    def reply_test(self, fn, source):
        """
        Procedure for handling incoming test messages

        :param fn: fragment id of the source node
        :param source: id of the source node
        """
        if self.fn != fn:
            msg = self.prepare_payload(
                ApplicationLayerMessageTypes.ACCEPT, source, ())
            self.send_down(Event(self, EventTypes.MFRT, msg))
        else:
            self.edges[source].st = EdgeStatus.REJECTED
            if source != self.test_edge:
                msg = self.prepare_payload(
                    ApplicationLayerMessageTypes.REJECT, source, ())
                self.send_down(Event(self, EventTypes.MFRT, msg))
            else:
                self.do_test()

    def do_test(self):
        # Procedure FindMinimalOutgoing
        """
        Finds minimial outgoing edge, if we dont have a basic edge 
        we report it, otherwise we send test message to that node

        """
        edge_index = self.find_lowest_weight_basic_edge()
        if edge_index == -1:
            self.test_edge = -1
            self.do_report()
        else:
            self.test_edge = edge_index
            msg = self.prepare_payload(
                ApplicationLayerMessageTypes.TEST, edge_index, (self.fn, self.level))
            self.send_down(Event(self, EventTypes.MFRT, msg))
