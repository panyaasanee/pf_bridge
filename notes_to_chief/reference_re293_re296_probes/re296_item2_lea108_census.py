import sys, pefile
from capstone import *
from pathlib import Path
IMAGE=Path(sys.argv[1]); data=IMAGE.read_bytes()
pe=pefile.PE(data=data, fast_load=True); base=pe.OPTIONAL_HEADER.ImageBase
t=[s for s in pe.sections if s.Name.rstrip(b'\x00')==b'.text'][0]
tva=base+t.VirtualAddress; traw=t.PointerToRawData; tsz=t.SizeOfRawData
blob=data[traw:traw+tsz]
md=Cs(CS_ARCH_X86,CS_MODE_32)
pat=b'\x08\x01\x00\x00'
i=blob.find(pat); out=[]
while i!=-1:
    for back in (2,3,6,7):
        s=i-back
        if s<0: continue
        if blob[s]==0x8D:  # lea
            for ins in md.disasm(blob[s:s+10], tva+s):
                if ins.mnemonic=='lea' and '0x108]' in ins.op_str:
                    out.append((tva+s, ins.op_str))
                break
            break
    i=blob.find(pat,i+1)
seen=set()
for va,o in out:
    if va in seen: continue
    seen.add(va); print(f"0x{va:08X}  lea {o}")
print("total unique:",len(seen))
