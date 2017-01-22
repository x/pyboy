class CartridgeReadException(Exception):
    pass


class Cartridge():

    MAX_SIZE = 0x200000
    """
    int, max size in bytes a rom could be
    """

    def __init__(self, fname):
        f = open(fname, 'rb')
        self.mem = f.read()
        if len(self.mem) > self.MAX_SIZE:
            raise CartridgeReadException("Invalid rom file: Too large")
        f.close()

    def __getitem__(self, index):
        return self.mem[index]

    def get_rom_bank_mode_byte(self):
        return self.mem[0x147]


