Simulating a Migen design
#########################

Migen allows you to easily simulate your FHDL design and interface it with arbitrary Python code. The simulator is written in pure Python and interprets the FHDL structure directly without using an external Verilog simulator.

Migen lets you write testbenches using Python's generator functions. Such testbenches execute concurrently with the FHDL simulator, and communicate with it using the ``yield`` statement. There are four basic patterns:

    #. Reads: the state of the signal at the current time can be queried using ``(yield signal)``;
    #. Writes: the state of the signal after the next clock cycle can be set using ``(yield signal.eq(value))``;
    #. Clocking: simulation can be advanced by one clock cycle using ``yield``;
    #. Composition: control can be transferred to another testbench function using ``yield from run_other()``.

A testbench can be run using the ``run_simulation`` function from ``migen.sim``; ``run_simulation(dut, bench)`` runs the generator function ``bench`` against the logic defined in an FHDL module ``dut``.

Passing the ``vcd_name="file.vcd"`` argument to ``run_simulation`` will cause it to write a VCD
dump of the signals inside ``dut`` to ``file.vcd``.

Examples
********

For example, consider this module::

  class ORGate(Module):
    def __init__(self):
      self.a = Signal()
      self.b = Signal()
      self.x = Signal()

      ###

      self.comb += self.x.eq(self.a | self.b)

It could be simulated together with the following testbench::

  dut = ORGate()

  def testbench():
    yield dut.a.eq(0)
    yield dut.b.eq(0)
    yield
    assert (yield dut.x) == 0

    yield dut.a.eq(0)
    yield dut.b.eq(1)
    yield
    assert (yield dut.x) == 1

  run_simulation(dut, testbench())

This is, of course, quite verbose, and individual steps can be factored into a separate function::

  dut = ORGate()

  def check_case(a, b, x):
    yield dut.a.eq(a)
    yield dut.b.eq(b)
    yield
    assert (yield dut.x) == x

  def testbench():
    yield from check_case(0, 0, 0)
    yield from check_case(0, 1, 1)
    yield from check_case(1, 0, 1)
    yield from check_case(1, 1, 1)

  run_simulation(dut, testbench())

Pitfalls
********

There are, unfortunately, some basic mistakes that can produce very puzzling results.

When calling other testbenches, it is important to not forget the ``yield from``. If it is omitted, the call would silently do nothing.

When writing to a signal, it is important that nothing else should drive the signal concurrently. If that is not the case, the write would silently do nothing.
