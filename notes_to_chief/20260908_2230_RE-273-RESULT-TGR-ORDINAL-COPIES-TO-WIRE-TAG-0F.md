ถึง LANE-Q (เจ้าของใบ/ผู้บริโภคผล), สำเนา LANE-K / chief

# RE-273 — DONE / POSITIVE: embedded TGR ordinal -> TriggerVital tag 0x0F

รอบ START 2026-09-08T22:20:21.085+07:00; ticket START 22:21:27.922+07:00. ทำ static บน bridge เท่านั้น ไม่มีการเปิดเกม/server หรืออ่าน DB.

## ขอบเขตและคำตัดสิน

ทำข้อที่ LANE-Q เปิดต่อในจดหมาย 20260906_1525 และ LANE-K พับลง addendum 2026-09-07T20:20: ordinal ในระเบียน `.tgr` เป็นฟิลด์เดียวกับ TriggerVital tag 0x0F หรือไม่?

**ใช่: ไคลเอนต์อ่าน embedded u16 ordinal เข้า record+0x4E แล้วคัดลอก 16 บิตนั้นไป vital+0x14; serializer เขียน +0x14 ด้วย tag 0x0F ความยาว 2 ไบต์. ไม่ใช่ vector index.** เป็น positive field crosswalk จาก data flow ไม่ใช่จับคู่เพราะค่าตัวเลขตรงกัน ขอเจ้าของใบปิดข้อ static ที่แคบลงนี้; ไม่แก้คิวเอง.

แก้ความเข้าใจ: 0x006007C0 เป็น codec ไม่ใช่ handler โหลด TGR. หลักฐานเชื่อมมาจาก outbound producer. Handler 0x00710440 มีไบต์ B0 01 C2 04 00 (return true), จึงห้ามใช้ผลนี้อ้างว่า server ส่ง TriggerVital แล้ว client รัน Lua.

## หลักฐานตรวจซ้ำได้

| ขั้น | ตำแหน่งและ field crosswalk |
|---|---|
| เลือก resource | `.tgr` ที่ VA 0x00F31488 ถูกใช้สร้าง global string 0x01082698; loader 0x005FD970 ใช้ string นี้ แล้ว call 0x005FD890 ที่ 0x005FDA11 |
| สร้างระเบียน | 0x005FD890 อ่าน version/count แล้ววน allocate ระเบียน; call record codec 0x005FCE60 ที่ 0x005FD8FD ก่อนเก็บ pointer ใน resource vector |
| อ่าน field | read branch ของ 0x005FCE60 อ่าน name/model ด้วย 0x00899CD0 (u32 length + bytes), byte สามตัวเข้า +0x48/+0x49/+0x4A, u16 เข้า +0x4C, แล้ว `lea ecx,[esi+0x4E]` ที่ 0x005FD025 / call read2 0x00899C00 ที่ 0x005FD02B |
| ผูก manager | 0x005FE1FE เก็บ resource pointer ที่ manager+0x1C; 0x005FE214 เรียก .tgr loader บน resource เดียวกัน |
| เลือกระเบียน | sender 0x005FF730 อ่าน manager+0x1C ที่ 0x005FF7D0; 0x005FF7FA `mov esi,[eax+edi*4]` โหลด record pointer จาก vector. EDI เป็น index แต่ไม่ได้ถูกนำไปเขียน vital ID |
| คัดลอก ID | 0x005FF831 call allocator 0x005FF120; **0x005FF836 `mov dx,word ptr [esi+0x4E]`; 0x005FF83A `mov word ptr [eax+0x14],dx`**; enqueue 0x005DD800 ที่ 0x005FF85E |
| ชนิด vital | allocator 0x005FF120 เรียก ctor 0x00600760; ctor ตั้ง vtable 0x00F31714 ซึ่ง registry ผูกกับ TriggerVital และ codec 0x006007C0 |
| ลงสาย | 0x006007CD push 2; 0x006007D3 lea eax,[esi+0x14]; 0x006007D7 push 0x0F; 0x006007D9 call 0x0089A600 |

ตัวอย่างยืนยันโครงสร้างไฟล์ (ไม่ใช่หลักฐานจับคู่ numeric): Bg0002.tgr version=6, count=60; ระเบียนแรกมี name length=24, model length=10, flags=00 01 01, type=1; embedded ordinal อยู่ offset **0x33**, ค่า **1**. ลำดับการอ่านข้างบนเป็นตัวพิสูจน์ว่า offset นี้เข้า record+0x4E.

Verifier read-only: `python pf_bridge\staged\re273_ordinal_wire_verify.py` จาก project root. ผล PASS: instruction pins 16 จุด, parse header/first record, SHA input ก่อน/หลังเท่ากัน. ระหว่างเขียน verifier แก้ transcription ของ register ณ 0x005FF7D0 จาก ecx เป็น esi ให้ตรง instruction จริง; ไม่ได้แก้ไบนารีหรือ tweak การทดลองเกม.

Span SHA256 (end-exclusive):

- [005FCE60,005FD2D5): 117388bfb0a7626244e1387209764690c44c72729cd7355a02aa501ca2bea5e0
- [005FD890,005FD96C): a60bc574a9a01948fc86579cf2d4228b92acee384eb6075f61b739ff5cf153c8
- [005FE18F,005FE219) positive segment: 4c161a9ada1a590d1fa0a71ddcde913774ffb9216066517778a67507b1b28c19
- [005FF730,005FF8B0): 7a52265259320c372af00cdcba7484aa77abe7060c6bfac58ae675a8d91989a2
- [006007C0,0060082B): 2f30bd87df466c5df7df89818704ab636c9b875f4b5c74c01b62553a92791a12
- [00899CD0,00899D34): 2faf97a56d50f08e854fc8998d949712da9a80ba6ee9670f2951a14a27cbc2d4
- [00710440,00710445): f4c6d7ae520f88aecb3ea65952e885437fa4a6ce4b5c3439a161d1c5d8e42863

## ค้นก่อนถอด / reuse

- ค้น recursive pf_bridge/external ด้วย `trigger_ordinal|006007C0|TriggerVital`: พบ PF_SERIALIZER_FIELDS.tsv, PF_PROTOCOL_REGISTRY.tsv, PF_PROTOCOL_PRIORITY.tsv, PF_FIELD_VALIDATION.tsv; ให้ layout/registration ไม่ใช่ TGR-record-to-wire producer chain. ใช้ registry/serializer เดิมหลังตรวจ SHA.
- ค้น recursive pf_bridge/gamedata ด้วย pattern เดียวกัน: ไม่มี hit; ผลลบจำกัดเฉพาะ pattern/ขอบเขตนี้ ไม่ใช่อ้างว่าไม่มี mapping ทั้งระบบ. ใช้ผลค้นตาราง/Lua เดิมที่ใบระบุ ไม่สแกนซ้ำทั้ง corpus.
- ต่อจากผล 20260906_1340_RE-273-RESULT-TGR-FILE-IS-THE-TRIGGER-ID-TO-LUA-TABLE.md; ตรวจ SHA ของ TGR/image เดิมก่อนใช้. ไม่ทำซ้ำ parser sweep 267 ไฟล์ และไม่ยกระดับความครบถ้วนของตารางเดิม.

## Input SHA256 / post-check

ก่อนและหลังงานตรงกัน:

- GameClient/GameClient.local.bin: 9627211412AC60D50AD189CE5A629443CE928EC23A9F8D219DFB2B157028B623
- GameClient/Data/Scene/Save/Bg0002/Bg0002.tgr: 6122EB79EB9C5E94019D33608F2573A3FFA49E572B42970609EA7327FCEE924B
- pf_bridge/CLIENT_RE_QUEUE.md: D63947CBAFE56E94DAC79FB4765F3DB01E5FF8089FB0FFB76428B79C5562244A
- pf_bridge/NEW_ORDERS.txt: B29BB569451E5C983D97694BEABF09506866C1DEE17A22CC480273FE08B4E284
- external/PF_PROTOCOL_REGISTRY.tsv: 27DAAC0C6FBBC45D88281C31B98E3A8B56F421BD1E8BC16F970FDFF5716CFB4D
- external/PF_SERIALIZER_FIELDS.tsv: 99282BDF3F492EAEBDBAB4918AECC0E37BF8EFB42B904B18E1BA306767B5C123

Mailbox root/consumed time-ordered read/hash manifest: 7712 files, 44095783 bytes, SHA256 7A0946810FC1D1640E6168945BAB8AF60BDCC4B5C72F3ECB034EB21A5A4E169A. No mailbox content deleted/renamed.

## Nonclaims / BUILD_IMPACT

- ไม่พิสูจน์การรัน Lua จริง, client-observable, capture, server behavior หรือ GT ผ่าน; ไม่มี wire/DB evidence ในรอบนี้.
- ไม่พิสูจน์ ordinal unique ข้ามฉาก, signed-domain >32767, ทุก TGR version/record validity หรือ 72 parser variants ที่ยังไม่ตอบจากผลเดิม.
- ไม่ใช้ linear-disassembly sweep เป็นหลักฐานผลลบ; ข้อสรุปหลักเป็น positive read/copy/write chain.
- BUILD_IMPACT: เจ้าของสาย Q ใช้ embedded ordinal (พร้อมบริบท scene/resource) แทน record index เพื่อเชื่อมกับ tag 0x0F ได้ใน build ถัดไป. การผูก Lua ใช้ mapping ใน TGR ตามหลักฐานเดิมและขอบเขต parser เดิม; ต้องทดสอบ behavior แยก. รอบนี้ไม่มี server build/source change และไม่มีสิทธิ์อ้าง feature/charter PASS.
- Checkpoint: narrowed ordinal-wire job DONE; ไม่มี time checkpoint หรือ method-ceiling rerun ค้างในข้อนี้. เจ้าของใบตัดสินสถานะรวมเอง.
