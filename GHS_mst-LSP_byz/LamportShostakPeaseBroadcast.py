from enum import Enum
from adhoccomputing.Generics import *
from adhoccomputing.GenericModel import GenericModel, GenericMessageHeader, GenericMessage
from adhoccomputing.Networking.LogicalChannels.GenericChannel import GenericChannelWithLoopback
import networkx as nx
import matplotlib.pyplot as plt
import sys


class ApplicationLayerMessageTypes(Enum):
    BROADCAST = "BROADCAST"


class LamportShostakPeaseBroadcast(GenericModel):
    def __init__(self, componentname, componentinstancenumber, context=None, configurationparamters=None, num_worker_threads=1, topology: nx.Graph = None):
        super().__init__(componentname, componentinstancenumber, context,
                         configurationparamters, num_worker_threads, topology)
        self.id = componentinstancenumber
        self.topology = topology
        self.N = self.topology.G.number_of_nodes()
        self.round = 1
        self.received_list = set()
        self.values = []
        self.is_commander = self.id == 0
        self.is_byzantine = self.id == 3
        self.k = 1

    def on_init(self, eventobj: Event):
        if self.is_commander:
            for i in range(self.N):
                if i != self.id:
                    msg = self.prepare_payload(
                        ApplicationLayerMessageTypes.BROADCAST, i, 0)
                    self.send_down(Event(self, EventTypes.MFRT, msg))

    def on_message_from_bottom(self, eventobj: Event):
        self.broadcast_handler(eventobj)

    def prepare_payload(self, msg_type, destination, payload):
        hdr = GenericMessageHeader(msg_type,
                                   self.id,
                                   destination)
        msg = GenericMessage(hdr, payload)
        return msg

    def broadcast_handler(self, eventobj: Event):
        if self.k <= -1:
            return

        message: GenericMessage = eventobj.eventcontent
        source = message.header.messagefrom
        value = message.payload
        self.values.append(value)
        self.received_list.add(source)
        print(
            f"[ROUND {self.k}] Node {self.id} received message from Node {source}, payload: {message.payload}, received_list: {self.received_list}")

        for i in range(self.N):
            if i != self.id and i not in self.received_list:
                if self.is_byzantine:
                    value = 1 if value == 0 else 0
                msg = self.prepare_payload(
                    ApplicationLayerMessageTypes.BROADCAST, i, value)
                self.send_down(Event(self, EventTypes.MFRT, msg))
        self.k -= 1
        if self.k == -1:
            votes_count = sum(self.values)
            print(
                f"Node byzantine:({self.is_byzantine}) {self.id} has decided on value {votes_count > len(self.values)//2}, values: {self.values}")
