import sys, pefile
from pathlib import Path
IMAGE=Path(sys.argv[1]); data=IMAGE.read_bytes()
pe=pefile.PE(data=data, fast_load=True); base=pe.OPTIONAL_HEADER.ImageBase
secs=[(base+s.VirtualAddress, s.PointerToRawData, s.SizeOfRawData) for s in pe.sections]
def off(va):
    for st,raw,size in secs:
        if st<=va<st+size: return raw+va-st
    return None
for a in sys.argv[2:]:
    va=int(a,16); o=off(va)
    if o is None: print(f"{a}: NOT_MAPPED"); continue
    b=data[o:o+200]
    asc=b.split(b'\x00')[0]
    # utf16
    u=b''
    for i in range(0,200,2):
        if b[i:i+2]==b'\x00\x00': break
        u+=b[i:i+2]
    try: ud=u.decode('utf-16-le')
    except Exception: ud=''
    print(f"{a}: ascii={asc[:60]!r} utf16={ud[:60]!r}")
