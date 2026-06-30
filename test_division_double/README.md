# Test ARCompact division on double

The program [`do_div.c`](./do_div.c) was compiled with:

```sh
arc-linux-gcc -O0 -mcpu=arc700 -o do_div.bin do_div.c
```

This produced an executable with function `__divdf3`, implemented in <https://github.com/foss-for-synopsys-dwc-arc-processors/gcc/blob/91ce9d4245fc4b46a7cf48749ed76b4c0a40b05c/libgcc/config/arc/ieee-754/divdf3.S#L185>.

To emulate it in Ghidra, launched with PyGhidra mode, the Python script from [`emulate_divdf3.py`](./emulate_divdf3.py) can be used.

This produces output with execution traces ([`emulate_divdf3.output.txt`](./emulate_divdf3.output.txt)), verifying that division on `double` variables is emulated correctly:

```text
Computing 1/1...
ram:000104d8 (asl r8,r3,0xc                 ) r0=0x00000000 r1=0x3ff00000 r2=0x00000000 r3=0x3ff00000 r6=0x00000000 r1:r0=1.0 r2:r3=1.0
ram:000104dc (lsr r12,r2,0x14               ) r0=0x00000000 r1=0x3ff00000 r2=0x00000000 r3=0x3ff00000 r6=0x00000000 r1:r0=1.0 r2:r3=1.0
ram:000104e0 (lsr r4,r8,0x1a                ) r0=0x00000000 r1=0x3ff00000 r2=0x00000000 r3=0x3ff00000 r6=0x00000000 r1:r0=1.0 r2:r3=1.0
ram:000104e4 (add3 r10,pcl=0x104e4,0x3b     ) r0=0x00000000 r1=0x3ff00000 r2=0x00000000 r3=0x3ff00000 r6=0x00000000 r1:r0=1.0 r2:r3=1.0
ram:000104e8 (ld.as r4,[r10,r4]             ) r0=0x00000000 r1=0x3ff00000 r2=0x00000000 r3=0x3ff00000 r6=0x00000000 r1:r0=1.0 r2:r3=1.0
ram:000104ec (ld.as r9,[pcl=0x104ec,0x2d0]  ) r0=0x00000000 r1=0x3ff00000 r2=0x00000000 r3=0x3ff00000 r6=0x00000000 r1:r0=1.0 r2:r3=1.0
ram:000104f0 (or r8,r8,r12                  ) r0=0x00000000 r1=0x3ff00000 r2=0x00000000 r3=0x3ff00000 r6=0x00000000 r1:r0=1.0 r2:r3=1.0
ram:000104f4 (mpyhu r5,r4,r8                ) r0=0x00000000 r1=0x3ff00000 r2=0x00000000 r3=0x3ff00000 r6=0x00000000 r1:r0=1.0 r2:r3=1.0
ram:000104f8 (and.f r7,r3,r9                ) r0=0x00000000 r1=0x3ff00000 r2=0x00000000 r3=0x3ff00000 r6=0x00000000 r1:r0=1.0 r2:r3=1.0
ram:000104fc (asl r4,r4,0xc                 ) r0=0x00000000 r1=0x3ff00000 r2=0x00000000 r3=0x3ff00000 r6=0x00000000 r1:r0=1.0 r2:r3=1.0
ram:00010500 (beq.d 0x000103d4              ) r0=0x00000000 r1=0x3ff00000 r2=0x00000000 r3=0x3ff00000 r6=0x00000000 r1:r0=1.0 r2:r3=1.0
ram:00010508 (sub r4,r4,r5                  ) r0=0x00000000 r1=0x3ff00000 r2=0x00000000 r3=0x3ff00000 r6=0x3ff00000 r1:r0=1.0 r2:r3=1.0
ram:0001050c (mpyhu r5,r4,r4                ) r0=0x00000000 r1=0x3ff00000 r2=0x00000000 r3=0x3ff00000 r6=0x3ff00000 r1:r0=1.0 r2:r3=1.0
ram:00010510 (breq.d r6,0x0,0x00010440      ) r0=0x00000000 r1=0x3ff00000 r2=0x00000000 r3=0x3ff00000 r6=0x3ff00000 r1:r0=1.0 r2:r3=1.0
ram:00010518 (asl r12,r1,0xb                ) r0=0x00000000 r1=0x3ff00000 r2=0x00000000 r3=0x3ff00000 r6=0x3ff00000 r1:r0=1.0 r2:r3=1.0
ram:0001051c (lsr r10,r0,0x15               ) r0=0x00000000 r1=0x3ff00000 r2=0x00000000 r3=0x3ff00000 r6=0x3ff00000 r1:r0=1.0 r2:r3=1.0
ram:00010520 (bset r8,r8,0x1f               ) r0=0x00000000 r1=0x3ff00000 r2=0x00000000 r3=0x3ff00000 r6=0x3ff00000 r1:r0=1.0 r2:r3=1.0
ram:00010524 (mpyhu r11,r5,r8               ) r0=0x00000000 r1=0x3ff00000 r2=0x00000000 r3=0x3ff00000 r6=0x3ff00000 r1:r0=1.0 r2:r3=1.0
ram:00010528 (add_s r12,r12,r10             ) r0=0x00000000 r1=0x3ff00000 r2=0x00000000 r3=0x3ff00000 r6=0x3ff00000 r1:r0=1.0 r2:r3=1.0
ram:0001052a (bset r5,r12,0x1f              ) r0=0x00000000 r1=0x3ff00000 r2=0x00000000 r3=0x3ff00000 r6=0x3ff00000 r1:r0=1.0 r2:r3=1.0
ram:0001052e (cmp r5,r8                     ) r0=0x00000000 r1=0x3ff00000 r2=0x00000000 r3=0x3ff00000 r6=0x3ff00000 r1:r0=1.0 r2:r3=1.0
ram:00010532 (cmp.eq r0,r2                  ) r0=0x00000000 r1=0x3ff00000 r2=0x00000000 r3=0x3ff00000 r6=0x3ff00000 r1:r0=1.0 r2:r3=1.0
ram:00010536 (lsr.cc r5,r5,0x1              ) r0=0x00000000 r1=0x3ff00000 r2=0x00000000 r3=0x3ff00000 r6=0x3ff00000 r1:r0=1.0 r2:r3=1.0
ram:0001053a (sub r4,r4,r11                 ) r0=0x00000000 r1=0x3ff00000 r2=0x00000000 r3=0x3ff00000 r6=0x3ff00000 r1:r0=1.0 r2:r3=1.0
ram:0001053e (mpyhu r11,r5,r4               ) r0=0x00000000 r1=0x3ff00000 r2=0x00000000 r3=0x3ff00000 r6=0x3ff00000 r1:r0=1.0 r2:r3=1.0
ram:00010542 (breq r7,r9,0x000104be         ) r0=0x00000000 r1=0x3ff00000 r2=0x00000000 r3=0x3ff00000 r6=0x3ff00000 r1:r0=1.0 r2:r3=1.0
ram:00010546 (lsr r8,r8,0x2                 ) r0=0x00000000 r1=0x3ff00000 r2=0x00000000 r3=0x3ff00000 r6=0x3ff00000 r1:r0=1.0 r2:r3=1.0
ram:0001054a (add r5,r6,0x3fe00000          ) r0=0x00000000 r1=0x3ff00000 r2=0x00000000 r3=0x3ff00000 r6=0x3ff00000 r1:r0=1.0 r2:r3=1.0
ram:00010552 (breq r6,r9,0x000104d0         ) r0=0x00000000 r1=0x3ff00000 r2=0x00000000 r3=0x3ff00000 r6=0x3ff00000 r1:r0=1.0 r2:r3=1.0
ram:00010556 (mpyu r12,r11,r8               ) r0=0x00000000 r1=0x3ff00000 r2=0x00000000 r3=0x3ff00000 r6=0x3ff00000 r1:r0=1.0 r2:r3=1.0
ram:0001055a (asl_s r2,r2,0x9               ) r0=0x00000000 r1=0x3ff00000 r2=0x00000000 r3=0x3ff00000 r6=0x3ff00000 r1:r0=1.0 r2:r3=1.0
ram:0001055c (sbc r6,r5,r7                  ) r0=0x00000000 r1=0x3ff00000 r2=0x00000000 r3=0x3ff00000 r6=0x3ff00000 r1:r0=1.0 r2:r3=1.0
ram:00010560 (mpyhu r5,r11,r2               ) r0=0x00000000 r1=0x3ff00000 r2=0x00000000 r3=0x3ff00000 r6=0x3fe00000 r1:r0=1.0 r2:r3=1.0
ram:00010564 (add.cs r0,r0,r0               ) r0=0x00000000 r1=0x3ff00000 r2=0x00000000 r3=0x3ff00000 r6=0x3fe00000 r1:r0=1.0 r2:r3=1.0
ram:00010568 (asl_s r0,r0,0x6               ) r0=0x00000000 r1=0x3ff00000 r2=0x00000000 r3=0x3ff00000 r6=0x3fe00000 r1:r0=1.0 r2:r3=1.0
ram:0001056a (asl r10,r11,0x17              ) r0=0x00000000 r1=0x3ff00000 r2=0x00000000 r3=0x3ff00000 r6=0x3fe00000 r1:r0=1.0 r2:r3=1.0
ram:0001056e (sub r0,r0,r12                 ) r0=0x00000000 r1=0x3ff00000 r2=0x00000000 r3=0x3ff00000 r6=0x3fe00000 r1:r0=1.0 r2:r3=1.0
ram:00010572 (lsr r7,r11,0x9                ) r0=0x20000000 r1=0x3ff00000 r2=0x00000000 r3=0x3ff00000 r6=0x3fe00000 r1:r0=1.0000001192092896 r2:r3=1.0
ram:00010576 (sub r5,r0,r5                  ) r0=0x20000000 r1=0x3ff00000 r2=0x00000000 r3=0x3ff00000 r6=0x3fe00000 r1:r0=1.0000001192092896 r2:r3=1.0
ram:0001057a (mpyh r12,r5,r4                ) r0=0x20000000 r1=0x3ff00000 r2=0x00000000 r3=0x3ff00000 r6=0x3fe00000 r1:r0=1.0000001192092896 r2:r3=1.0
ram:0001057e (xor.f 0x0,r1,r3               ) r0=0x20000000 r1=0x3ff00000 r2=0x00000000 r3=0x3ff00000 r6=0x3fe00000 r1:r0=1.0000001192092896 r2:r3=1.0
ram:00010582 (and r1,r6,r9                  ) r0=0x20000000 r1=0x3ff00000 r2=0x00000000 r3=0x3ff00000 r6=0x3fe00000 r1:r0=1.0000001192092896 r2:r3=1.0
ram:00010586 (add_s r1,r1,r7                ) r0=0x20000000 r1=0x3fe00000 r2=0x00000000 r3=0x3ff00000 r6=0x3fe00000 r1:r0=0.5000000596046448 r2:r3=1.0
ram:00010588 (bxor.mi r1,r1,0x1f            ) r0=0x20000000 r1=0x3fefffff r2=0x00000000 r3=0x3ff00000 r6=0x3fe00000 r1:r0=0.9999995827674866 r2:r3=1.0
ram:0001058c (brhs r6,0x7fe00000,0x000105f4 ) r0=0x20000000 r1=0x3fefffff r2=0x00000000 r3=0x3ff00000 r6=0x3fe00000 r1:r0=0.9999995827674866 r2:r3=1.0
ram:00010594 (add.f r12,r12,0x11            ) r0=0x20000000 r1=0x3fefffff r2=0x00000000 r3=0x3ff00000 r6=0x3fe00000 r1:r0=0.9999995827674866 r2:r3=1.0
ram:00010598 (asr r9,r12,0x5                ) r0=0x20000000 r1=0x3fefffff r2=0x00000000 r3=0x3ff00000 r6=0x3fe00000 r1:r0=0.9999995827674866 r2:r3=1.0
ram:0001059c (sub.mi r1,r1,0x1              ) r0=0x20000000 r1=0x3fefffff r2=0x00000000 r3=0x3ff00000 r6=0x3fe00000 r1:r0=0.9999995827674866 r2:r3=1.0
ram:000105a0 (add.f r0,r9,r10               ) r0=0x20000000 r1=0x3fefffff r2=0x00000000 r3=0x3ff00000 r6=0x3fe00000 r1:r0=0.9999995827674866 r2:r3=1.0
ram:000105a4 (tst r12,0x1c                  ) r0=0x00000000 r1=0x3fefffff r2=0x00000000 r3=0x3ff00000 r6=0x3fe00000 r1:r0=0.9999995231628418 r2:r3=1.0
ram:000105a8 (jne.d blink                   ) r0=0x00000000 r1=0x3fefffff r2=0x00000000 r3=0x3ff00000 r6=0x3fe00000 r1:r0=0.9999995231628418 r2:r3=1.0
Emulation complete, result is 1.0
...
```
