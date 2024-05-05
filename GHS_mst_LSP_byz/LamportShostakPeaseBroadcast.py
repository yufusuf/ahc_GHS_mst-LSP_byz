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
        self.round = 0
        self.received_list = set()
        self.values = []
        self.is_commander = self.id == 0
        self.is_byzantine = self.id == 3 or self.id == 5
        # set this to byzantine node count
        self.k = 2
        self.round_mes_count = 0

    def on_init(self, eventobj: Event):
        """
        Commander initiates the algorithm sends its decided value to other nodes

        """
        if self.is_commander:
            for i in range(self.N):
                if i != self.id:
                    msg = self.prepare_payload(
                        ApplicationLayerMessageTypes.BROADCAST, i, 1)
                    self.send_down(Event(self, EventTypes.MFRT, msg))
            print(
                f"[ROUND {self.round}] Node commander {self.id} has decided on value 1")

    def on_message_from_bottom(self, eventobj: Event):
        """
        Calls the broadcast_handler
        """
        self.broadcast_handler(eventobj)

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

    def broadcast_handler(self, eventobj: Event):
        """

        handles incoming value and rebroadcasts its value to other nodes, finally decides on a value

        :param eventobj: value of the incoming message

        """
        message: GenericMessage = eventobj.eventcontent
        source = message.header.messagefrom
        value = message.payload

        self.round_mes_count += 1

        self.values.append(value)
        # if source in self.received_list:
        #     return
        self.received_list.add(source)
        print(
            f"[ROUND {self.round}] Node {self.id} received message from Node {source}, payload: {message.payload}, received_list: {self.received_list}, values: {self.values}")
        if (self.round == 0 and self.round_mes_count == 1) or (self.round > 0 and (self.N - self.round - 1 == self.round_mes_count)):
            self.do_broadcast(value)
            self.round_mes_count = 0
            self.round += 1
        if self.k == self.round:
            votes_count = sum(self.values)
            print(
                f"Node byzantine:({self.is_byzantine}) {self.id} has decided on value {votes_count > len(self.values)//2}, values: {self.values}")

    def do_broadcast(self, value):
        """

        sends broadcast messages to other nodes 

        :param value: value to be broadcasted

        """
        if self.is_byzantine:
            value = 1 if value == 0 else 0
        for i in range(self.N):
            if i != self.id and i not in self.received_list:
                msg = self.prepare_payload(
                    ApplicationLayerMessageTypes.BROADCAST, i, value)
                self.send_down(Event(self, EventTypes.MFRT, msg))
        time.sleep(0.1)
