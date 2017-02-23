"""
http://pastraiser.com/cpu/gameboy/gameboy_opcodes.html
"""
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
        CPU(A=0x12, H=0x45, clock=0x08)
        """
        kvs = sorted(self.registers.items(), key=lambda x: self.REGISTERS.index(x[0]))
        kvs += [('PC', self.pc), ('SP', self.sp), ('clock', self.clock)]
        kvs = filter(lambda x: x[1], kvs)
        return 'CPU(' + ', '.join(map('%s=0x%02x'.__mod__, kvs)) + ')'

    def __getitem__(self, key):
        if key in self.REGISTERS:
            return self.registers[key]
        if key in self.REGISTER_PAIRS:
            high_key, low_key = key
            return (self.registers[high_key] << 8) + self.registers[low_key]
        raise KeyError("%s not a register" % key)

    def __setitem__(self, key, value):
        if key in self.REGISTERS:
            self.registers[key] = value
            return None
        if key in self.REGISTER_PAIRS:
            high_key, low_key = key
            self.registers[high_key] = (value & 0xFF00) >> 8
            self.registers[low_key]  = value & 0x00FF
            return None
        raise KeyError("%s not a register" % key)

    def __init__(self, **kwargs):

        self.pc = None
        self.sp = None

        # always initialize the clock to 0
        self.clock = 0

        # initalize registers to None
        self.registers = {k: None for k in self.REGISTERS}

        # allow kwargs to initialize state
        self.set(**kwargs)

    def set(self, SP=None, PC=None, clock=None, **register_kwargs):
        if clock:
            self.clock = clock
        if SP:
            self.sp = SP
        if PC:
            self.pc = PC
        for k, v in register_kwargs.items():
            self[k] = v

    def set_startup_values(self):
        self.pc    = 0x100
        self.sp    = 0xFFFE
        self['AF'] = 0x01B1
        self['BC'] = 0x0013
        self['DE'] = 0x00D8
        self['HL'] = 0x014D

