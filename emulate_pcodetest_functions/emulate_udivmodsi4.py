"""Emulate function udivmodsi4, compiled in Ghidra's pcodetests

Original source code:
https://github.com/foss-for-synopsys-dwc-arc-processors/gcc/blob/91ce9d4245fc4b46a7cf48749ed76b4c0a40b05c/libgcc/config/arc/lib1funcs.S#L326-L540
"""
from java.math import BigInteger
from ghidra.pcode.emu import PcodeEmulator, EmulatorUtilities
from ghidra.program.model.lang import RegisterValue
from ghidra.program.model.symbol import SymbolUtilities


def compute_udivmodsi4(a, b):
    #udivmodsi4 = SymbolUtilities.getLabelOrFunctionSymbol(currentProgram, "u4_divide", None)
    udivmodsi4 = SymbolUtilities.getLabelOrFunctionSymbol(currentProgram, "__udivmodsi4", None)
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
    thread.setCounter(udivmodsi4.getAddress())
    controlledReturnAddr = currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(0x0badc0de)
    # Initialize registers
    set_reg("r0", a)
    set_reg("r1", b)
    set_reg("r2", 0)
    set_reg("r3", 0)
    set_reg("r6", 0)
    set_reg("blink", controlledReturnAddr.offset)
    result = None
    # Run the emulation
    while monitor.isCancelled() is False:
        executionAddress = thread.getCounter()
        if executionAddress == controlledReturnAddr:
            result = get_reg('r0')
            print("Emulation complete, result is {}".format(result))
            break
        # Print current instruction and the registers we care about
        intr = getInstructionAt(executionAddress)
        instr_str = str(intr)
        if ".d" in instr_str:
            # Decode the delay slot
            instr_str += " [with delay slot: {}]".format(getInstructionAt(executionAddress.add(intr.getLength())))
        desc = "{} ({:30s})".format(executionAddress, instr_str)
        for reg in ('r0', 'r1', 'r2', 'r3', 'r4'):
            desc += " {}={:#010x}".format(reg, get_reg(reg))
        print(desc)
        # single step emulation
        try:
            thread.stepInstruction()
        except Exception as e:
            printerr("Emulation Error: '{}'".format(e))
            break
    return result


def validate_udivmodsi4(a, b, expected, delta=None):
    print("Computing {:#x}/{:#x}...".format(a, b))
    result = compute_udivmodsi4(a, b)
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


def test_udivmodsi4():
    assert validate_udivmodsi4(1, 1, 1)
    assert validate_udivmodsi4(0x1010101, 0x1010101, 1)
    assert validate_udivmodsi4(0xfefefeff, 0x1010101, 0xfe)
    assert validate_udivmodsi4(0, 0x1010101, 0)
    assert validate_udivmodsi4(0x1010101, 2, 0x808080)
    assert validate_udivmodsi4(0xffffffff, 0xffffffff, 1)
    assert validate_udivmodsi4(0xffffffff, 1, 0xffffffff)


test_udivmodsi4()
