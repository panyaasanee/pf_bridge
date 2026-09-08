import sys, pefile, re, collections
from capstone import *
PATH=sys.argv[1]
pe=pefile.PE(PATH, fast_load=True); IB=pe.OPTIONAL_HEADER.ImageBase
sec=[s for s in pe.sections if s.Name.rstrip(b'\x00')==b'.text'][0]
va=IB+sec.VirtualAddress; raw=sec.PointerToRawData; size=sec.SizeOfRawData
data=open(PATH,'rb').read()[raw:raw+size]
md=Cs(CS_ARCH_X86,CS_MODE_32)
c=collections.Counter()
for ins in md.disasm(data, va):
    if ins.mnemonic!='call': continue
    o=ins.op_str
    s=re.sub(r'0x[0-9a-f]+','N',o)
    c[s]+=1
for s,n in c.most_common(20): print("%7d  %s"%(n,s))
