from migen import *


class DisplayTest(Module):
    def __init__(self):
        count = Signal(8)
        self.sync += count.eq(count + 1)
        self.sync += Display("Count: 0x%02x", count)


def generator(dut):
    for i in range(32):
        yield

if __name__ == "__main__":
    dut = DisplayTest()
    run_simulation(dut, generator(dut))
