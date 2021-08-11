from nmigen import *


class BugTest(Elaboratable):
    def __init__(self):

        self.wire1 = Signal(1)
        self.wire2 = Signal(1)

        self.counter = Signal(3)
        self.domain = 'new_clk'

    
    def elaborate(self, platform):
        m = Module()

        dom = ClockDomain(self.domain, async_reset = True, local = True)

        m.d.comb += [
            ClockSignal(self.domain).eq(self.wire1 ^ self.wire2),
            ResetSignal(self.domain).eq(ResetSignal('sync'))
        ]

        with m.FSM(reset = 'RESET', domain = self.domain):

            with m.State('RESET'): 
                m.next = 'NEXT'
                m.d[self.domain] += self.counter.eq(self.counter + 1)  


            with m.State('NEXT'): 
                m.next = 'NEXT2'
                m.d[self.domain] += self.counter.eq(self.counter + 1)  

            with m.State('NEXT2'):
                m.next = 'RESET'    
                m.d[self.domain] += self.counter.eq(self.counter + 1)  

        return m

class ClkGen(Elaboratable):
    def __init__(self):
        self.outwire = Signal(1)

        self.d_in = Signal(1)
        self.d_out = Signal(1)

    def elaborate(self, platform):
        m = Module()

        m.d.sync +=  self.d_out.eq(self.d_in)

        with m.FSM(reset = 'RESET'):
            with m.State('RESET'): 
                m.d.comb += self.outwire.eq(0)
                m.next = 'NEXT'

            with m.State('NEXT'):
                m.d.comb += self.outwire.eq(ClockSignal('sync') ^ self.d_out)

        return m