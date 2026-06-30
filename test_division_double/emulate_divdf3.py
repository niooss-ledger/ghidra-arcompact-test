"""Emulate function divdf3

Code inspired from section "Emulating a function" of
https://github.com/HackOvert/GhidraSnippets/blob/9bcd718e8958387ff5695194b83a52df4e0a3de7/README.md#emulating-a-function
"""
import struct
from java.math import BigInteger
from ghidra.pcode.emu import PcodeEmulator, EmulatorUtilities
from ghidra.program.model.lang import RegisterValue
from ghidra.program.model.symbol import SymbolUtilities


def compute_divdf3(a, b):
    divdf3 = SymbolUtilities.getLabelOrFunctionSymbol(currentProgram, "__divdf3", None)
    # Create an emulator
    lang = currentProgram.getLanguage()
    emu = PcodeEmulator(lang)
    EmulatorUtilities.loadProgram(emu, currentProgram)
    thread = emu.newThread()
    state = thread.getState()
    def set_reg(name, value):
        reg = lang.getRegister(name)
        state.setRegisterValue(RegisterValue(reg, BigInteger.valueOf(value)))
    def get_reg(name):
        reg = lang.getRegister(name)
        return state.inspectRegisterValue(reg).getUnsignedValue().longValue()
    thread.setCounter(divdf3.getAddress())
    controlledReturnAddr = currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(0x0badc0de)
    # Initialize registers
    r0, r1, r2, r3 = struct.unpack('<IIII', struct.pack('<dd', a, b))
    set_reg("r0", r0)
    set_reg("r1", r1)
    set_reg("r2", r2)
    set_reg("r3", r3)
    set_reg("r6", 0)
    set_reg("blink", controlledReturnAddr.offset)
    result = None
    # Run the emulation
    while monitor.isCancelled() is False:
        executionAddress = thread.getCounter()
        if executionAddress == controlledReturnAddr:
            result = struct.unpack('<d', struct.pack('<II', get_reg('r0'), get_reg('r1')))[0]
            print("Emulation complete, result is {}".format(result))
            break
        # Print current instruction and the registers we care about
        desc = "{} ({:30s})".format(executionAddress, str(getInstructionAt(executionAddress)))
        for reg in ('r0', 'r1', 'r2', 'r3', 'r6'):
            desc += " {}={:#010x}".format(reg, get_reg(reg))
        desc += " r1:r0={}".format(struct.unpack('<d', struct.pack('<II', get_reg('r0'), get_reg('r1')))[0])
        desc += " r2:r3={}".format(struct.unpack('<d', struct.pack('<II', get_reg('r2'), get_reg('r3')))[0])
        print(desc)
        # single step emulation
        try:
            thread.stepInstruction()
        except Exception as e:
            printerr("Emulation Error: '{}'".format(e))
            break
    return result


def validate_divdf3(a, b, expected, delta=None):
    print("Computing {}/{}...".format(a, b))
    result = compute_divdf3(a, b)
    if result is None:
        printerr("Emulation encountered an error")
        return False
    elif delta is None:
        if result != expected and not (str(result) == str(expected) == "nan"):
            printerr("Emulation produced unexpected output: {} != {}".format(result, expected))
            return False
    elif abs(result - expected) > delta:
        printerr("Emulation produced unexpected output: {} != {} +- {}".format(result, expected, delta))
        return False
    return True


def test_divdf3():
    assert validate_divdf3(1, 1, 1.0, delta=1e-6)
    assert validate_divdf3(1, 10, 0.1, delta=1e-7)
    assert validate_divdf3(-1, 10, -0.1, delta=1e-7)
    assert validate_divdf3(1, -10, -0.1, delta=1e-7)
    assert validate_divdf3(-1, -10, 0.1, delta=1e-7)
    assert validate_divdf3(1, 0, float('inf'))
    assert validate_divdf3(0, 0, float('nan'))
    assert validate_divdf3(float('inf'), 1, float('inf'))
    assert validate_divdf3(float('nan'), 1, float('nan'))
    assert validate_divdf3(float('nan'), 0, float('inf'))
    assert validate_divdf3(5 * pow(2., 1022), 0.00000001, float('inf'))  # (double overflow, returns r0=0x00000000 r1=0x7ff00000)
    assert validate_divdf3(5 * (2. ** 1020), 0.5 ** 10, float('inf'))
    assert validate_divdf3((2. ** 1023), 0.5 ** 1022, float('inf'))
    assert validate_divdf3(0.5**1074, 0.5, 0.5**1073) # => unimplemented instruction "asrs r0,r4,r7" and "abss r10,r4"


test_divdf3()
