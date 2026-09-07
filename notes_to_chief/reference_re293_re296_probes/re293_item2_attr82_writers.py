import sys, pefile, struct
from capstone import *
from pathlib import Path
IMAGE=Path(sys.argv[1]); data=IMAGE.read_bytes()
pe=pefile.PE(data=data, fast_load=True); base=pe.OPTIONAL_HEADER.ImageBase
t=[s for s in pe.sections if s.Name.rstrip(b'\x00')==b'.text'][0]
tva=base+t.VirtualAddress; traw=t.PointerToRawData; tsz=t.SizeOfRawData
blob=data[traw:traw+tsz]
# byte-pattern: 66 89 <modrm mod=10> [sib] 82 00 00 00   (mov word ptr [reg+0x82], reg)
md=Cs(CS_ARCH_X86,CS_MODE_32)
hits=[]
i=0
pat=b'\x82\x00\x00\x00'
idx=blob.find(pat)
while idx!=-1:
    for back in range(2,9):
        s=idx-back
        if s<0: continue
        if blob[s]==0x66 and blob[s+1] in (0x89,0x8B):
            for ins in md.disasm(blob[s:s+12], tva+s):
                hits.append((tva+s, ins.mnemonic, ins.op_str)); break
            break
        if blob[s] in (0x89,0x8B,0x88,0x8A,0x66) and back<=3:
            for ins in md.disasm(blob[s:s+12], tva+s):
                if ins.mnemonic in ('mov','movzx') and '0x82]' in ins.op_str:
                    hits.append((tva+s, ins.mnemonic, ins.op_str))
                break
    idx=blob.find(pat, idx+1)
seen=set()
print(f"pattern hits (mov with +0x82 disp32) = {len(hits)}")
for va,m,o in hits:
    if va in seen: continue
    seen.add(va)
    print(f"0x{va:08X}  {m:<7} {o}")
