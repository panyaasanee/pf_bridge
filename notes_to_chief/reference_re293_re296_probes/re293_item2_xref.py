import sys, struct, pefile
from pathlib import Path
IMAGE=Path(sys.argv[1]); data=IMAGE.read_bytes()
pe=pefile.PE(data=data, fast_load=True); base=pe.OPTIONAL_HEADER.ImageBase
secs=[(base+s.VirtualAddress, s.PointerToRawData, s.SizeOfRawData, s.Name.decode(errors='replace').rstrip('\x00')) for s in pe.sections]
def sec_of(va):
    for st,raw,size,n in secs:
        if st<=va<st+size: return (st,raw,size,n)
    return None
targets=[int(a,16) for a in sys.argv[2:]]
text=[s for s in secs if s[3]=='.text'][0]
tst,traw,tsize,_=text
for t in targets:
    hits=[]
    # E8/E9 rel32
    for i in range(traw, traw+tsize-5):
        op=data[i]
        if op in (0xE8,0xE9):
            rel=struct.unpack_from('<i',data,i+1)[0]
            va=tst+(i-traw)
            if va+5+rel==t: hits.append((va,'call' if op==0xE8 else 'jmp'))
    # absolute dword anywhere
    packed=struct.pack('<I',t)
    for st,raw,size,n in secs:
        start=raw; end=raw+size
        idx=data.find(packed,start)
        while idx!=-1 and idx<end:
            hits.append((st+(idx-raw),f'abs:{n}'))
            idx=data.find(packed,idx+1)
    print(f"TARGET 0x{t:08X}: {len(hits)} hit(s)")
    for va,k in hits[:60]: print(f"   0x{va:08X}  {k}")
