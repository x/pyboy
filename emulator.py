#! env/bin/python

import sys

from memory    import Memory
from cpu       import CPU
from display   import Display
from cartridge import Cartridge


class Emulator():

    FPS = 60
    """
    int, frames per second
    """

    def __init__(self, fname):
        self.cart    = Cartridge(fname)
        self.mem     = Memory()
        self.display = Display()
        self.cpu     = CPU()

        # initial values for cpu
        self.cpu.set(PC=0x100, SP=0xFFFE, AF=0x01B1, BC=0x0013, DE=0x00D8, HL=0x014D)

        # set rom banking mode
        self.mem.set_rom_bank_mode(self.cart.get_rom_bank_mode_byte())

    def update(self):
        # operations to execute before a frame draw
        max_cycles = self.cpu.CLOCK_SPEED / self.FPS

        c = 0
        while (c < max_cycles):
            c += self.cpu.execute_next_opcode()
            self.cpu.update_timers(c)
            # update_graphics(c)
            # do_interupts()

        self.display.render()


if __name__ == '__main__':
    Emulator(sys.argv[1])
