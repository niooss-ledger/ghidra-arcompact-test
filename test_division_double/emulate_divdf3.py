"""Emulate function divdf3

Code inspired from section "Emulating a function" of
https://github.com/HackOvert/GhidraSnippets/blob/9bcd718e8958387ff5695194b83a52df4e0a3de7/README.md#emulating-a-function
"""
import struct
from ghidra.app.emulator import EmulatorHelper
from ghidra.program.model.symbol import SymbolUtilities


def compute_divdf3(a, b):
    divdf3 = SymbolUtilities.getLabelOrFunctionSymbol(currentProgram, "__divdf3", None)
    # Create an emulator
    emuHelper = EmulatorHelper(currentProgram)
    emuHelper.writeRegister(emuHelper.getPCRegister(), divdf3.getAddress().offset)
    controlledReturnAddr = currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(0x0badc0de)
    # Initialize registers
    r0, r1, r2, r3 = struct.unpack('<IIII', struct.pack('<dd', a, b))
    emuHelper.writeRegister("r0", r0)
    emuHelper.writeRegister("r1", r1)
    emuHelper.writeRegister("r2", r2)
    emuHelper.writeRegister("r3", r3)
    emuHelper.writeRegister("r6", 0)
    emuHelper.writeRegister("blink", controlledReturnAddr.offset)
    result = None
    # Run the emulation
    while monitor.isCancelled() is False:
        executionAddress = emuHelper.getExecutionAddress()
        if executionAddress == controlledReturnAddr:
            print("Emulation complete.")
            result = struct.unpack('<d', struct.pack('<II', emuHelper.readRegister('r0').longValue(), emuHelper.readRegister('r1').longValue()))[0]
            break
        # Print current instruction and the registers we care about
        desc = "{} ({:30s})".format(executionAddress, str(getInstructionAt(executionAddress)))
        for reg in ('r0', 'r1', 'r2', 'r3', 'r6'):
            reg_value = emuHelper.readRegister(reg).longValue()
            desc += " {}={:#010x}".format(reg, reg_value)
        desc += " r1:r0={}".format(struct.unpack('<d', struct.pack('<II', emuHelper.readRegister('r0').longValue(), emuHelper.readRegister('r1').longValue()))[0])
        desc += " r2:r3={}".format(struct.unpack('<d', struct.pack('<II', emuHelper.readRegister('r2').longValue(), emuHelper.readRegister('r3').longValue()))[0])
        print(desc)
        # single step emulation
        success = emuHelper.step(monitor)
        if not success:
            lastError = emuHelper.getLastError()
            printerr("Emulation Error: '{}'".format(lastError))
            break
    # Cleanup resources and release hold on currentProgram
    emuHelper.dispose()
    return result


def validate_divdf3(a, b, expected, delta=None):
    print("Computing {}/{}...".format(a, b))
    result = compute_divdf3(a, b)
    if result is None:
        printerr("Emulation encountered an error")
        return False
    elif delta is None:
        if result != expected:
            printerr("Emulation produced unexpected output: {} != {}".format(result, expected))
            return False
    elif abs(result - expected) > delta:
        printerr("Emulation produced unexpected output: {} != {} +- {}".format(result, expected, delta))
        return False
    return True


def test_divdf3():
    assert validate_divdf3(1, 1, 1.0, delta=1e-6)
    assert validate_divdf3(1, 10, 0.1, delta=1e-7)
    assert validate_divdf3(1, 0, 1.0)
    assert validate_divdf3(1, 10, 0.1)
    assert validate_divdf3(1, 0, 1)
    assert validate_divdf3(0, 0, float('nan'))
    assert validate_divdf3(float('inf'), 1, float('inf'))
    assert validate_divdf3(float('nan'), 1, float('nan'))
    assert validate_divdf3(float('nan'), 0, 0)
    assert validate_divdf3(5 * pow(2., 1022), 0.00000001, float('inf'))  # (double overflow, returns r0=0x00000000 r1=0x7ff00000)
    assert validate_divdf3(5 * (2. ** 1020), 0.5 ** 10)
    assert validate_divdf3((2. ** 1023), 0.5 ** 1022)
    assert validate_divdf3(0.5**1074, 0.5) # => unimplemented instruction!!!

test_divdf3()
