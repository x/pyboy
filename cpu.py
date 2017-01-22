"""
http://pastraiser.com/cpu/gameboy/gameboy_opcodes.html
"""
class Container():
    def __repr__(self):
        return "0x%x" % self.value


class Register(Container):

    def __init__(self):
        self._value = 0x00

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, byte):
        self._value = byte


class RegisterPair(Container):

    def __init__(self, hi_reg, lo_reg):
        self._hi = hi_reg
        self._lo = lo_reg

    @property
    def value(self):
        # do I need to mask these?
        return (self._hi.value << 8) + self._lo.value

    @value.setter
    def value(self, word):
        self._hi.value = (word & 0xFF00) >> 8
        self._lo.value =  word & 0x00FF


class ProgramCounter(Register):
    pass


class StackPointer(Register):
    pass


class CPU():

    CLOCK_SPEED = 0x400000
    """int, operations per second
    """

    REGISTERS = ['A', 'F', 'B', 'C', 'D', 'E', 'H', 'L']
    """list, 8-bit registers
    """

    REGISTER_PAIRS = ['AF' 'BC', 'DE', 'HL']
    """list, 16-bit register pairs
    """

    def __repr__(self):
        """
        >>> CPU(A=0x12, H=0x45, clock=8)
        CPU(A=0x12, H=0x45, clock=8)
        """
        kvs = []
        for k in ['A', 'F', 'B', 'C', 'D', 'E', 'H', 'L', 'PC', 'SP']:
            v = getattr(self, k)
            if v.value:
                kvs.append('%s=%s' % (k, v))
        if self.clock:
            kvs.append('clock=%s' % self.clock)
        return 'CPU(' + ', '.join(kvs) + ')'


    def __getitem__(self, index):

        return self.mem[index]

    def __setitem__(self, index, value):
        # don't allow writing to read only memory
        if index < 0x8000:
            return

        # writing to ECHO (0xE000 - 0xFCFF) also writes in RAM (C000-DDFF)
        elif 0xE000 <= index < 0xFE00:
            self.mem[index] = value
            self.mem[index - 0x2000] = value

        # this area is restricted
        elif 0xFEA0 <= index < 0xFEFF:
            return

        else:
            self.mem[index] = value


    def __init__(self, **kwargs):

        # basic registers
        self.A = Register()
        self.B = Register()
        self.C = Register()
        self.D = Register()
        self.E = Register()
        self.F = Register()
        self.H = Register()
        self.L = Register()

        # special registers
        self.PC = ProgramCounter()
        self.SP = StackPointer()

        # register pairs (a 16-bit interface for two 8 bit registers)
        self.AF = RegisterPair(self.A, self.F)
        self.BC = RegisterPair(self.B, self.C)
        self.DE = RegisterPair(self.D, self.E)
        self.HL = RegisterPair(self.H, self.L)

        # always initialize the clock to 0
        self.clock = 0

        # allow kwargs to initialize state
        self.set(**kwargs)

    def set(self, clock=0, **container_kwargs):
        if clock:
            self.clock = clock
        for k, v in container_kwargs.items():
            getattr(self, k).value = v

    def set_initial_values(self):
        self.PC.set(0x100)
        self.SP.set(0xFFFE)
        self.AF.set(0x01B1)
        self.BC.set(0x0013)
        self.DE.set(0x00D8)
        self.HL.set(0x014D)

    def execute_next_opcode(self):
        pass

    def update_timers(self):
        pass

