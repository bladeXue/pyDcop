from unittest.mock import MagicMock

import pytest

from pydcop.algorithms import ComputationDef, AlgorithmDef
from pydcop.computations_graph.objects import ComputationNode
from pydcop.infrastructure.computations import (
    MessagePassingComputation,
    register,
    message_type,
    SynchronousComputationMixin,
    SynchronizationMsg,
    ComputationException,
    DcopComputation,
)

FooMsg = message_type("FooMsg", ["data"])


class SynchC(SynchronousComputationMixin, MessagePassingComputation):
    def __init__(self, name, neighbors):
        super().__init__(name)
        self._neighbors = neighbors
        self._msg_sender = MagicMock()

    @property
    def neighbors(self):
        return self._neighbors

    @register("FooMsg")
    def on_foo(self, sender, msg, t):
        pass

    def on_new_cycle(self, messages, cycle_id):
        print(f"new cycle {cycle_id}")


# FIXME: need to add cycle id in message ?
# TODO: send message


def test_on_start_is_a_cycle():
    # As a computation will generally send messages during the startup phase (i.e. the
    # on_start method) , this phase must also be considered as a cycle.

    c = SynchC("test", ["bar"])
    c.on_new_cycle = MagicMock()
    assert c.current_cycle == 0
    c.start()
    assert c.current_cycle == 0


def test_receive_one_neighbor():

    c = SynchC("test", ["bar"])
    c.on_new_cycle = MagicMock()
    c.start()
    assert c.current_cycle == 0

    # First cycle, c receives a message from its single neighbor,
    # on_cycle_message must be called.
    msg1 = FooMsg(1)
    msg1.cycle_id = 0
    c.on_message("bar", msg1, 42)
    assert c.current_cycle == 1
    c.on_new_cycle.assert_any_call({"bar": (msg1, 42)}, 0)

    # Second cycle, c receives a message from its single neighbor,
    # on_cycle_message must be called again.
    c.on_new_cycle.reset_mock()
    msg2 = FooMsg(2)
    msg2.cycle_id = 1
    c.on_message("bar", msg2, 43)
    c.on_new_cycle.assert_any_call({"bar": (msg2, 43)}, 1)
    assert c.cycle_count == 2


def test_receive_two_neighbors():

    c = SynchC("test", ["bar", "yup"])
    c.on_new_cycle = MagicMock()
    c.start()

    # First cycle, c receives a message from both neighbors,
    # on_cycle_message must be called.
    msgbar1 = FooMsg(1)
    msgbar1.cycle_id = 0
    c.on_message("bar", msgbar1, 42)
    msgyup1 = FooMsg(1)
    msgyup1.cycle_id = 0
    c.on_message("yup", msgyup1, 43)

    assert c.cycle_count == 1
    c.on_new_cycle.assert_called_once_with(
        {"bar": (msgbar1, 42), "yup": (msgyup1, 43)}, 0
    )


def test_receive_2_neighbors_shifted():

    c = SynchC("test", ["bar", "yup"])
    c.on_new_cycle = MagicMock()
    c.start()

    msgbar1 = FooMsg(1)
    msgbar1.cycle_id = 0
    c.on_message("bar", msgbar1, 42)
    # Foo send the message for next cycle before we receive the message from yup
    msgbar2 = FooMsg(2)
    msgbar2.cycle_id = 1
    c.on_message("bar", msgbar2, 45)

    # We received two messages from foo, but none from yup : no new cycle.
    assert c.cycle_count == 0
    c.on_new_cycle.assert_not_called()

    # Now we receive the message from yup, which ends the first cycle:
    msgyup1 = FooMsg(1)
    msgyup1.cycle_id = 0
    c.on_message("yup", msgyup1, 43)

    assert c.cycle_count == 1
    c.on_new_cycle.assert_called_once_with(
        {"bar": (msgbar1, 42), "yup": (msgyup1, 43)}, 0
    )

    # Yup send its message for the second cycle:
    c.on_new_cycle.reset_mock()
    msgyup2 = FooMsg(1)
    msgyup2.cycle_id = 1
    c.on_message("yup", msgyup2, 50)

    assert c.cycle_count == 2
    c.on_new_cycle.assert_called_once_with(
        {"bar": (msgbar2, 45), "yup": (msgyup2, 50)}, 1
    )


def test_sending_cycle_messages():
    c = SynchC("test", ["bar"])

    def on_cycle(messages, cycle_id):
        return [("bar", FooMsg(3))]

    c.on_new_cycle = on_cycle

    c.start()

    # When receiving a message from bar, we switch to the next cycle and
    # should thus send the message for this cycle
    msgbar1 = FooMsg(1)
    msgbar1.cycle_id = 0
    c.on_message("bar", msgbar1, 42)

    expected_msg_with_cycle = FooMsg(3)
    expected_msg_with_cycle.cycle_id = 1

    c.message_sender.assert_called_once_with(
        "test", "bar", expected_msg_with_cycle, None, None
    )


def test_sending_automatic_cycle_sync_message():

    c = SynchC("test", ["bar"])

    def on_cycle(messages, cycle_id):
        # We do not send any algo-level message in this cycle,
        # but, when the cycle is over,  a sync message but still be sent to our
        # neighbors so that they can switch to the next cycle.
        pass

    c.on_new_cycle = on_cycle

    c.start()

    # When receiving a message from bar, we switch to the next cycle and
    # should thus send an automatic sync message for this cycle.
    msgbar1 = FooMsg(1)
    msgbar1.cycle_id = 0
    c.on_message("bar", msgbar1, 42)

    c.message_sender.assert_called_once_with(
        "test", "bar", SynchronizationMsg(), None, None
    )


def test_receiving_automatic_sync_message():

    c = SynchC("test", ["bar"])
    c.on_new_cycle = MagicMock()
    c.start()

    sync_msg = SynchronizationMsg()
    sync_msg.cycle_id = 0
    c.on_message("bar", sync_msg, 42)

    # Received a sync message from our single neighbor, we should switch cycle
    assert c.cycle_count == 1
    c.on_new_cycle.assert_called_once_with({}, 0)


def test_sending_automatic_cycle_sync_message_2_neighbors():

    c = SynchC("test", ["bar", "yup"])

    def on_cycle(messages, cycle_id):
        return [("bar", FooMsg(3))]

    c.on_new_cycle = on_cycle

    c.start()

    # When receiving a message from all neighbors, we switch to the next cycle and
    # should thus send an automatic sync message for this cycle to yup, as we did not
    # send any algo-level message to him on `on_cycle`.
    msgbar1 = FooMsg(1)
    msgbar1.cycle_id = 0
    c.on_message("bar", msgbar1, 42)

    msgyup1 = FooMsg(1)
    msgyup1.cycle_id = 0
    c.on_message("yup", msgyup1, 42)

    c.message_sender.assert_any_call("test", "yup", SynchronizationMsg(), None, None)
    assert c.message_sender.call_count == 2


def test_receiving_duplicate_message_fails():
    c = SynchC("test", ["bar", "yup"])
    c.start()

    msgbar1 = FooMsg(1)
    msgbar1.cycle_id = 0
    c.on_message("bar", msgbar1, 42)

    msgbar2 = FooMsg(2)
    msgbar2.cycle_id = 0

    # Receiving a second message from the same neighbor and for the same cycle: error.
    with pytest.raises(ComputationException) as comp_exception:
        c.on_message("bar", msgbar2, 42)
    assert "two messages from bar" in str(comp_exception)


def test_receiving_out_of_order_messages_fails():

    c = SynchC("test", ["bar", "yup"])
    c.start()

    msgbar2 = FooMsg(2)
    msgbar2.cycle_id = 3

    # Receiving a message for an unexpected cycle: error.
    with pytest.raises(ComputationException) as comp_exception:
        c.on_message("bar", msgbar2, 42)
    assert "but received message for cycle 3" in str(comp_exception)


def test_receiving_message_from_unknown_computation_fails():

    c = SynchC("test", ["bar", "yup"])
    c.start()

    msgbar2 = FooMsg(2)
    msgbar2.cycle_id = 0

    # Receiving a message for an unexpected cycle: error.
    with pytest.raises(ComputationException) as comp_exception:
        c.on_message("wrong", msgbar2, 42)
    assert f"a message from wrong" in str(comp_exception)


def test_cycle_id_is_added_when_using_post_msg():

    c = SynchC("test", ["bar", "yup"])

    c.post_msg("foo", FooMsg(1))

    expected = FooMsg(1)
    expected.cycle_id = 0

    c.message_sender.assert_any_call("test", "foo", expected, None, None)


def test_mixing_message_from_post_and_return():
    #TODO
    pass

## Tests with derivind DcopComputation


class SynchDcopC(SynchronousComputationMixin, DcopComputation):
    def __init__(self, name, neighbors):
        super().__init__(name, neighbors)
        self._msg_sender = MagicMock()

    @register("FooMsg")
    def on_foo(self, sender, msg, t):
        pass

    def on_new_cycle(self, messages, cycle_id):
        print(f"new cycle {cycle_id}")


def test_receive_one_neighbor_dcop_computation():

    comp_def = ComputationDef(
        ComputationNode("test", neighbors=["bar"]), AlgorithmDef("fake", {})
    )
    c = SynchDcopC("test", comp_def)
    c.on_new_cycle = MagicMock()
    c.start()

    # First cycle, c receives a message from its single neighbor,
    # on_cycle_message must be called.
    msg1 = FooMsg(1)
    # This is automatically done when sending from a Synchronous Computation:
    msg1.cycle_id = 0
    c.on_message("bar", msg1, 42)
    assert c.cycle_count == 1
    c.on_new_cycle.assert_any_call({"bar": (msg1, 42)}, 0)

    # Second cycle, c receives a message from its single neighbor,
    # on_cycle_message must be called again.
    c.on_new_cycle.reset_mock()
    msg2 = FooMsg(2)
    msg2.cycle_id = 1
    c.on_message("bar", msg2, 43)
    c.on_new_cycle.assert_any_call({"bar": (msg2, 43)}, 1)
    assert c.cycle_count == 2


def test_receive_two_neighbors_dcop_computation():

    comp_def = ComputationDef(
        ComputationNode("test", neighbors=["bar", "yup"]), AlgorithmDef("fake", {})
    )
    c = SynchDcopC("test", comp_def)
    c.on_new_cycle = MagicMock()
    c.start()

    # First cycle, c receives a message from both neighbors,
    # on_cycle_message must be called.
    msgbar1 = FooMsg(1)
    msgbar1.cycle_id = 0
    c.on_message("bar", msgbar1, 42)
    msgyup1 = FooMsg(1)
    msgyup1.cycle_id = 0
    c.on_message("yup", msgyup1, 43)

    assert c.cycle_count == 1
    c.on_new_cycle.assert_called_once_with(
        {"bar": (msgbar1, 42), "yup": (msgyup1, 43)}, 0
    )


def test_cycle_id_is_added_when_using_post_to_all_neighbors_dcop_computation():

    comp_def = ComputationDef(
        ComputationNode("test", neighbors=["bar", "yup"]), AlgorithmDef("fake", {})
    )
    c = SynchDcopC("test", comp_def)
    c.start()

    c.post_to_all_neighbors(FooMsg(1))

    expected = FooMsg(1)
    expected.cycle_id = 0

    c.message_sender.assert_any_call("test", "yup", expected, None, None)
    c.message_sender.assert_any_call("test", "bar", expected, None, None)
