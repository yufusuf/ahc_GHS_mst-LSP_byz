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
        self.is_commander = self.id == 0
        self.is_byzantine = self.id == 3 or self.id == 5
        # set this to byzantine node count
        self.k = 2
        self.received_list = [set()] * self.k
        self.values = []
        self.decided = False

    def on_init(self, eventobj: Event):
        """
        Commander initiates the algorithm sends its decided value to other nodes

        """
        if self.is_commander:
            time.sleep(0.5)
            for i in range(self.N):
                if i != self.id:
                    msg = self.prepare_payload(
                        ApplicationLayerMessageTypes.BROADCAST, i, (True, 0))
                    self.send_down(Event(self, EventTypes.MFRT, msg))
            print(
                f"[ROUND 0] Node commander {self.id} has decided on value 1")
            self.decided = True

    def on_message_from_bottom(self, eventobj: Event):
        """
        Calls the broadcast_handler
        """
        if self.decided:
            return
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
        (value, pulse) = message.payload
        print(
            f"[ROUND {pulse}] Node {self.id} received message from Node {source}, value: {value}")
        if pulse < self.k:
            self.received_list[pulse].add(source)
            self.values.append(value)
            value = not value if self.is_byzantine else value
            self.do_broadcast(value, pulse)
        print(
            f"[ROUND {pulse}] Node {self.id} is deciding on values: f{self.values} => {sum([int(i) for i in self.values]) > len(self.values)//2}")

    def do_broadcast(self, value, pulse):
        """

        sends broadcast messages to other nodes 

        :param value: value to be broadcasted

        """
        print(
            f"[ROUND {pulse}] Node {self.id} broadcasting to {list(filter(lambda x: x not in self.received_list[pulse] and x != self.id, range(self.N)))}")
        for i in range(self.N):
            if i != self.id and i not in self.received_list[pulse]:
                time.sleep(0.01)
                msg = self.prepare_payload(
                    ApplicationLayerMessageTypes.BROADCAST, i, (value, pulse + 1))
                self.send_down(Event(self, EventTypes.MFRT, msg))
