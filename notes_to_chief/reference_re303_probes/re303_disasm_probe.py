#!/usr/bin/env python3
"""RE-293 item2 read-only probe: walk POTENTIAL open site 0x005888D5 -> find(key) -> ActorAttr+0x82."""
import hashlib, sys
from pathlib import Path
import pefile
from capstone import CS_ARCH_X86, CS_MODE_32, Cs

IMAGE = Path(sys.argv[1])
data = IMAGE.read_bytes()
pe = pefile.PE(data=data, fast_load=True)
base = int(pe.OPTIONAL_HEADER.ImageBase)
secs = [(base+int(s.VirtualAddress), int(s.PointerToRawData), int(s.SizeOfRawData), s.Name.decode(errors='replace').rstrip('\x00')) for s in pe.sections]
def off(va):
    for st, raw, size, n in secs:
        if st <= va < st+size:
            return raw + va - st
    raise ValueError(hex(va))
md = Cs(CS_ARCH_X86, CS_MODE_32); md.detail=False
print(f"IMAGE={IMAGE.name} size={len(data)} base=0x{base:08X} sha256={hashlib.sha256(data).hexdigest()}")
for st,raw,size,n in secs: print(f"  sect {n:<8} va=0x{st:08X} raw=0x{raw:08X} size=0x{size:X}")
for arg in sys.argv[2:]:
    a,b,label = arg.split(':')
    s,e = int(a,16), int(b,16)
    blob = data[off(s):off(e)]
    print(f"=== {label} [0x{s:08X},0x{e:08X}) len={e-s} span_sha256={hashlib.sha256(blob).hexdigest()} ===")
    for ins in md.disasm(blob, s):
        print(f"0x{ins.address:08X}  {ins.mnemonic:<9} {ins.op_str}")
