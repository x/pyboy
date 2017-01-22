def _noop():
    pass

def _ld_r8_d8(s, t):
    pass

# ld A,B
def _ld_r8_r8(cpu, t, s):
    """
    >>> cpu = CPU(A=0xaa, B=0xbb)
    >>> _ld_r8_r8(cpu.A, cpu.B)()
    >>> cpu
    CPU(A=0xbb, B=0xbb, clock=4)
    """
    def _fn():
        cpu.clock += 4
        t.value = s.value
    return _fn

# ld A,(BC)
def _ld_r8_deref_r16(cpu, mem, t, s):
    """
    >>> from memory import Memory
    >>> mem = Memory()
    >>> mem[0xbbcc] = 0xdd
    >>> cpu = CPU(A=0xaa, B=0xbb, C=0xcc)
    >>> _ld_r8_deref_r16(mem, cpu.A, cpu.BC)()
    >>> cpu
    CPU(A=0xdd, B=0xbb, C=0xcc, clock=8)
    """
    def _fn():
        cpu.clock += 8
        t.value = mem[s.value]
    return _fn

# ld (BC),A
def _ld_deref_r16_r8(cpu, mem, t, s):
    """
    >>> from memory import Memory
    >>> mem = Memory()
    >>> cpu = CPU(A=0xaa, B=0xbb, C=0xcc)
    >>> _ld_deref_r16_r8(mem, cpu.BC, cpu.A)()
    >>> cpu
    CPU(A=0xaa, B=0xbb, C=0xcc, clock=8)
    >>> '0x%x' % mem[0xbbcc]
    '0xaa'
    """
    def _fn():
        cpu.clock += 8
        mem[t.value] = s.value
    return _fn

# ld A,(a16)
def _ld_r8_deref_a16(cpu, t, s):
    """
    """
    pass

# ld (a16),A
def _ld_deref_a16_r8(cpu, t, s):
    pass

# ld BC,d16
def _ld_r16_d16(cpu, t):
    """
    >>> cpu = CPU()
    >>> _ld_r16_d16(cpu.BC)(0xffee)
    >>> cpu
    CPU(B=0xff, C=0xee, clock=12)
    """
    def _fn(nn):
        cpu.clock += 12
        t.value = nn
    return _fn

def step_instruction(cpu, mem):
    return [
        # 0x00 NOP
        _noop

        # 0x01 LD BC,d16



    ]



