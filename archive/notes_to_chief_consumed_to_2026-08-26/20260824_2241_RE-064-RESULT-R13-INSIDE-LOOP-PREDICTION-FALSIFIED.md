[ถึง: chief cloud (cc) และ Panya · จาก: RE runner LOCAL]

# RE-064 RESULT — PINNED · R13 INSIDE LOOP · TRAILER PREDICTION FALSIFIED

เวลา: 2026-08-24T22:34 ถึง 2026-08-24T22:41 (+07:00)  
ชนิดงาน: STATIC-ON-BRIDGE ล้วน · ไม่บูต server/client · ไม่จับ `LOCK_GAME` · ไม่ใช้ DB  
bridge HEAD ตอนจบ: `102c857e9bdd`

## คำตอบ objective หนึ่งประโยค

**pin ได้ — element = tag `0x32` กว้าง 8 ไบต์ แล้ว tag `0x08` กว้าง 1 ไบต์ · R13 `0x005ED2F0` = `INSIDE-loop` และเป็น loop-internal collection-insert helper ไม่ใช่ wire serializer/trailer · loop bound `[0x005EDBB2,0x005EDC1B)` วนตามค่า R10 ที่อ่านเข้า `[esp+0x50]` โดย `inc bl`/compare/back-edge · หลักฐาน main span `[0x005EDA20,0x005EDC31)` sha256 `b5f6a1586a810c0a98ceb7c925a0d4afa10cff41db661eb0947b8918f3a11d54` และ helper span `[0x005ED2F0,0x005ED370)` sha256 `73426afc91b102c7d69c27930bf8c43b013399639028c930fa7c613d4f65133a`**

## ช่องค้นบังคับ

- **ค้นใน `pf_bridge\external\` แล้ว:** เจอ `ItemOperateVitalRes` registry/serializer span, R10/R11/R12/R13 rows, tag widths, และ blocker เดิม `direct_call_not_proven_serializer`; ชุดส่งมอบไม่มี loop bound หรือการจำแนก R13 จึงเดินอิมเมจต่อ
- **ค้น gamedata แล้ว:** ไม่เจอ `ItemOperateVitalRes`, `005ED2F0`, หรือ `affected_identity` (ผล grep 0) และไม่ได้ใช้ gamedata ตัดสิน control flow

## จ็อบ 1 — control gate PASS

recursive CFG วิธีเดียวกับ target reproduce loop ที่ RE-059 รู้คำตอบแล้วได้ครบ:

- `ItemBagAttr` span `[0x0046F180,0x0046F3E9)` · file off `0x0006E580` · len 617 · sha256 `29e38267ab54c852e3f1338c2fb833e3b9d1a41903544a390489c264c09fa813` · 208 instructions · gap 3 alignment bytes · decode errors 0
- ขา read อ่าน update count แล้ว loop `[0x0046F30B,0x0046F377)`; counter `inc ebp` `0x0046F36F`; compare `bp,[esp+0x3C]` `0x0046F370`; back-edge `0x0046F375 -> 0x0046F30B`
- constructor `0x0046B410` เขียน vtable `0x00F0EBB0`; vtable slot `+0x34` resolve เป็น serializer `0x0046BD30`
- serializer span `[0x0046BD30,0x0046BEA1)` · off `0x0006B130` · len 369 · sha256 `b21137bde28452c08f8fa6a2eda18accf9c2d51b9b7d82a1b6997986feba86c1` · decode errors 0
- ลำดับ read ต่อ element ตรง RE-059 byte-for-byte: `0x32/8 + 0x14/4 + 0x0F/2 + 0x0F/2 + 0x08/1 + 0x08/1 + 0x0B/1`

ดังนั้น method ระบุ loop bound/counter และตาม indirect vtable call ไปถึง tag sequence ที่รู้คำตอบแล้วได้จริงก่อนใช้กับ target

## จ็อบ 2 — จำแนก R13

R13 = หมวด **(iii) loop-internal helper ของ element**:

- span `[0x005ED2F0,0x005ED370)` · file off `0x001EC6F0` · len 128 · sha256 `73426afc91b102c7d69c27930bf8c43b013399639028c930fa7c613d4f65133a`
- recursive CFG 53 instructions / 128 decoded bytes / gap 0 / decode errors 0
- function อ่าน vector begin/end/capacity ที่ `this+0x0C/+0x10/+0x14`, หารด้วย stride `0x20`, แล้วเลือก direct append call `0x005EAA50` หรือ grow call `0x005ECE00`
- direct-call set มีเพียงสองตัวนั้น; ไม่มี stream primitive `0x0089A640/0x0089A600`
- direct append เพิ่ม end pointer `+0x20` ที่ `0x005ED33B` แล้วเขียนกลับ `[this+0x10]` ที่ `0x005ED33E`

จึงเป็น collection insertion ของ record ที่ decoder เพิ่งประกอบ ไม่ได้กิน wire tag เพิ่ม

## จ็อบ 3 — target loop + element order

- R10 อ่านด้วย tag `0x08` ที่ call `0x005EDBA2` เข้า byte `[esp+0x50]`
- initial gate: compare `0x005EDBA9`, `jle 0x005EDC1B` ที่ `0x005EDBAD`
- loop body `[0x005EDBB2,0x005EDC1B)`
- R11: tag `0x32`, width 8, read call `0x005EDBBD`
- R12: tag `0x08`, width 1, read call `0x005EDBCD`
- decoder สร้าง record ชั่วคราว แล้ว call R13 ที่ `0x005EDC06` **ก่อน** เพิ่ม counter
- counter `inc bl` `0x005EDC0B`; compare `bl,[esp+0x50]` `0x005EDC0D`; signed back-edge `jl 0x005EDBB2` ที่ `0x005EDC19`

**คำทำนาย element order ถูก แต่คำทำนาย R13=TRAILER ผิด:** R13 ถูกเรียกหนึ่งครั้งต่อ decoded element และอยู่ใน body แน่นอน อย่างไรก็ดี R13 ไม่เพิ่ม wire field ดังนั้น wire element ยังคงมีเพียง `0x32/8` ตามด้วย `0x08/1`

## จ็อบ 4 — rider 15-byte PC prefix

capture `GAME_20260817_002429_300322_58470.txt` sha256 `2e43b7066130cf3c2ac43493aebd7bc9662085ce4fb6276809e6baf52a2a581e`, PC ordinal 101, len 71:

- capture prefix: `129D6E140000000008040B02120100`
- v141 prefix:    `129D6E140000000008040B02120100`
- verdict: **IDENTICAL 15/15 bytes**

## reproducibility

- `staged/re064_verify_cfg.py` sha256 `5aa0b1d3fbc575914aed6e3e13aa800f530e40b0fc583a8f192fced832161406` · final exit 0 · `RE064_VERDICT=PASS`
- `staged/re064_prefix_check.py` sha256 `a828e6662f8ff43728dc767bf7426e520ebee32a49d40b5ab0f3f12198a458cd` · final exit 0 · `PREFIX_VERDICT=IDENTICAL`
- exploratory recursive dump: `staged/re064_dump_cfg.py` sha256 `3933d5c01e4817e5cb6d69f3417297cc7549b6abf99adcedecd09d7a3334a562`
- PE word reader: `staged/re064_pe_words.py` sha256 `c3a62ad13a58a0007c545797cb722520c5f3748e492f6eb5f2a42038833519d1`
- ทุก script ASCII-only
- verifier รอบแรกหยุดเพราะผูก assertion ว่า ItemBag span ต้อง gap 0 ทั้งที่ recursive CFG ที่มีอยู่รายงาน alignment gap 3 อยู่แล้ว; แก้ guard ให้ pin gap 3 แบบ exact แล้ว final run exit 0 ข้างต้น — เป็น defect ของ verifier ที่เพิ่งเขียน ไม่ใช่ evidence mismatch

คำสั่งหลัก:

```powershell
py -3 staged\re064_verify_cfg.py "C:\Users\Panya\Desktop\Pirate Force\GameClient\GameClient.local.bin"
py -3 staged\re064_prefix_check.py --client "C:\Users\Panya\Desktop\Pirate Force\GameClient" --validator patches\gt047\pf_validate_capture_fields.py
```

## read-only SHA before = after

- `GameClient.local.bin`: `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`
- `PF_SERIALIZER_FIELDS.tsv`: `99282bdf3f492eaebdbab4918aecc0e37bf8efb42b904b18e1ba306767b5c123`
- `PF_PROTOCOL_REGISTRY.tsv`: `27daac0c6fbbc45d88281c31b98e3a8b56f421bd1e8bc16f970fdff5716cfb4d`
- `PF_TAG_CENSUS.tsv`: `63bc9a039b5b35e5b2e1f08ce99e91b05da6e6959b5b4f173eac66b88aea337a`
- `PF_PROTOCOL_PRIORITY.tsv`: `d9174bc27ebc1159a7b66ba3fc36b0d6025ecf72d9d963c3deee9bb780c3de55`
- `PF_INPUT_INVENTORY.tsv`: `729b5e73383de8fd6e0008875d4b9b685de2ad8d72a55118aa862093f10259d1`
- `PF_GAMEDATA_INDEX.tsv`: `a9ab5efd3826a54e0cad3cb86f0c872ebd1d61219721ee8514d42e9d2110b5bc`
- capture rider file: `2e43b7066130cf3c2ac43493aebd7bc9662085ce4fb6276809e6baf52a2a581e`

## client-observable / runtime

ว่างโดยเจตนา — ไม่เปิดเกม ไม่บูตเซิร์ฟเวอร์ ไม่มีภาพหรือ runtime claim และไม่ใช้เลขจ็อบ 9xx

## nonclaims

- ไม่ตั้ง semantics ให้ R11/R12/R13; รายงานเฉพาะ tag width, order และ control flow
- ไม่อ้างว่า original server เคยส่ง R10>0; capture จริง 5 เฟรมของ RE-059 ยังเป็น R10=0 ทั้งหมด
- ไม่พิสูจน์ producer direction, green-line handler, ข้อความบนจอ หรือกฎของ original server
- ไม่พิสูจน์ว่า encoder ฝั่ง server ปัจจุบันถูกหรือผิด และไม่แก้ encoder/ledger/queue/frame draft
- prefix identical พิสูจน์เฉพาะ 15 ไบต์ของ exact capture PC #101 เทียบ exact v141 candidate เท่านั้น ไม่พิสูจน์ session context ที่เหลือ

