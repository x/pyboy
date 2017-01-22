from enum import Enum

class MemoryStartException(Exception):
    pass


class RomBankMode(Enum):
    NO_BANKING = 0
    MBC1       = 1
    MBC2       = 2


class Memory():

    MEM_SIZE = 0x10000
    """
    int, size in bytes of the gameboy's memory
    """

    def __init__(self):
        self.mem = bytearray([0x00] * self.MEM_SIZE)
        self.mem[0xFF05] = 0x00
        self.mem[0xFF06] = 0x00
        self.mem[0xFF07] = 0x00
        self.mem[0xFF10] = 0x80
        self.mem[0xFF11] = 0xBF
        self.mem[0xFF12] = 0xF3
        self.mem[0xFF14] = 0xBF
        self.mem[0xFF16] = 0x3F
        self.mem[0xFF17] = 0x00
        self.mem[0xFF19] = 0xBF
        self.mem[0xFF1A] = 0x7F
        self.mem[0xFF1B] = 0xFF
        self.mem[0xFF1C] = 0x9F
        self.mem[0xFF1E] = 0xBF
        self.mem[0xFF20] = 0xFF
        self.mem[0xFF21] = 0x00
        self.mem[0xFF22] = 0x00
        self.mem[0xFF23] = 0xBF
        self.mem[0xFF24] = 0x77
        self.mem[0xFF25] = 0xF3
        self.mem[0xFF26] = 0xF1
        self.mem[0xFF40] = 0x91
        self.mem[0xFF42] = 0x00
        self.mem[0xFF43] = 0x00
        self.mem[0xFF45] = 0x00
        self.mem[0xFF47] = 0xFC
        self.mem[0xFF48] = 0xFF
        self.mem[0xFF49] = 0xFF
        self.mem[0xFF4A] = 0x00
        self.mem[0xFF4B] = 0x00
        self.mem[0xFFFF] = 0x00
        self.bank_mode = None

    def set_rom_bank_mode(self, b):
        if b == 0:
            self.bank_mode = RomBankMode.NO_BANKING
        elif b in (1, 2, 3):
            self.bank_mode = RomBankMode.MBC1
        elif b in (5, 6):
            self.bank_mode = RomBankMode.MBC2
        else:
            raise MemoryStartException("Don't recognize bank mode %d" % b)
        # TODO
        if self.bank_mode is not RomBankMode.NO_BANKING:
            raise NotImplementedError("Rom banking doesn't work yet...")

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

    def get_TIMA(self):
        """Timer accumulator"""
        return self[0xFF05]

    def get_TMA(self):
        """Timer reset value"""
        return self[0xFF06]

    def get_TMC(self):
        """Timer Controller, sets the timer count up frequency"""
        return self[0xFF07]


