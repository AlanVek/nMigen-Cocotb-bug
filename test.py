from nmigen import *
import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge
from nmigen_cocotb import run
from module import BugTest, ClkGen

from random import getrandbits

results = []

async def init_test(dut):

    cocotb.fork(Clock(dut.clk, 10, 'ns').start())

    dut.rst <= 1
    dut.d_in <= 0

    await RisingEdge(dut.clk)
    await RisingEdge(dut.clk)
    await RisingEdge(dut.clk)

    dut.rst <= 0

    await RisingEdge(dut.clk)

async def one_iter(dut):
    await RisingEdge(dut.clk)
    results.append(dut.bug_recv.counter.value.integer)

@cocotb.test()
async def spacewire_test(dut):
    await init_test(dut)


    for _ in range(10):
        dut.d_in <= getrandbits(1)
        await one_iter(dut)
        await one_iter(dut)
        await one_iter(dut)
        await one_iter(dut)

    
    print('Counter:', results)    

if __name__ == '__main__':

    m = Module()

    m.submodules.bug_recv = bug_recv = BugTest()
    m.submodules.bug_trns = bug_trns = ClkGen()

    m.d.comb += [
        bug_recv.wire1.eq(bug_trns.d_out),
        bug_recv.wire2.eq(bug_trns.outwire)
    ]
    
    run(
        m,
        'test',
        ports = [
            bug_trns.d_in
        ],

        vcd_file = 'bug_test.vcd'
    )
