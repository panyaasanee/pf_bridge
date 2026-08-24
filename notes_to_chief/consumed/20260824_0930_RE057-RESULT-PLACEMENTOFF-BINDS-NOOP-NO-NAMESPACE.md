ถึง chief

# RE-057 RESULT — `Scene.PlacementOFF` bind เป็น no-op; ไม่มี namespace ใน client build นี้

เวลา: 2026-08-24T09:30+07:00  
สถานะเสนอ: **DONE / STATIC-LANE-CLOSED** — jobs 1–2 ปิด, jobs 3–4 **N/A เพราะ implementation ไม่อ่าน argument**

## คำตอบ objective ประโยคเดียว

ใน `GameClient.local.bin` ที่พินไว้ พารามิเตอร์ของ `Scene.PlacementOFF(N)` **ไม่ได้ชี้เข้า placement index หรือ namespace อื่นใดเลย**: string `PlacementOFF` VA `0x00F313A0` มี registration เดียวที่ `0x005F80A2`, record นั้นเก็บ delegate `0x0045FA00`, และ body ทั้งฟังก์ชันคือ `33 C0 C2 04 00` (`xor eax,eax; ret 4`) จึงทิ้ง Lua-state/argument โดยไม่อ่าน; `PlacementON` กับ `PlacementCancel` bind no-op ตัวเดียวกัน ทำให้ทั้งเคสเลขเกิน (Bg3001/2) และ control ที่อยู่ในช่วง (Bg3003/4) ถูกอธิบายด้วยกลไกเดียวกัน.

นี่เข้าเกณฑ์จบถาวรของใบ: **binding ชื่อ API → implementation resolve แล้ว แต่ namespace ของ 59/60/61 ไม่มีใน static เพราะ shipped implementation ไม่ทำ lookup ใด ๆ**. ห้ามเปิดใบ static เพิ่มเพื่อไล่ namespace เดิม; ถ้าจะรู้ว่า revision/runtime อื่นเคยทำอะไร ต้องเป็นงาน runtime/คนละ build และรอ Panya ตัดสิน.

## ช่องค้นบังคับ

- ค้นใน `pf_bridge\external\` แล้ว: อ่าน `00_SEARCH_HERE_FIRST.md` และ grep ชุดส่งมอบหา `PlacementOFF|PlacementON|PlacementCancel|CheckPlacementAlive`/trigger-scene binding — **ไม่เจอแถวคำตอบ** (ชุด external เป็น protocol/serializer เป็นหลัก). จึงเปิดอิมเมจตามใบ.
- ค้น gamedata แล้ว: ใช้ผล census เต็มของ R137 — crosswalk table เดียว `QUESTDATA_TH__QUEST.(n_SCENE,s_LUASCRIPT)` ไม่ครอบสคริปต์ PlacementOFF ทั้ง 19 ไฟล์, 188 ตารางไม่มีชื่อเป้าหมาย; ไม่ grep ตารางเดิมซ้ำ. ตรวจ decoded Lua สี่ไฟล์ซ้ำจาก raw ASCII tokens ได้ 26/38/17/31 calls, max 56/61/33/45 ตรง R136/prework.
- ค้นบนอิมเมจแล้ว: exact ASCII `PlacementOFF` เจอ **1** ที่ VA `0x00F313A0` (file off `0x00B2F7A0`), UTF-16LE = 0; dword ref ไป name VA เจอ **1** ที่ registration `0x005F80A2`. ชื่อสคริปต์ `t_clsplc_t1_for_bg300{1..4}` exact ASCII/UTF-16LE = 0 ทุกชื่อ.
- ค้นไฟล์ฉากต้นทางแล้ว: recursive raw-byte census ครบ **61 ไฟล์** ใต้ `GameClient\Data\Scene\Save\Bg300{1..4}\` (รวม `.npc/.tgr/.gat/.tmpkg/.gs_/.dmc/.bm_` และ sector files) หา `PlacementOFF` และชื่อสคริปต์ทั้งสี่ทั้ง ASCII/UTF-16LE = **0 hit ทั้งหมด**. รายชื่อ/size/sha256 ทุกไฟล์อยู่ใน `logs\re057_20260824\re057_probe.json`; manifest sha `f9aa96353abe1d4b7d575ed9c6b187841839e362f125908beaf56e6c30834588`.

## จ็อบ 1 — binding ที่ยืนยันจากอิมเมจ

ฟังก์ชัน registration `[0x005F8010,0x005F81C9)` มี record ต่อเนื่อง:

| API | name push | delegate store | delegate |
|---|---:|---:|---:|
| `PlacementON` | `0x005F8073` bytes `68 B0 13 F3 00` | `0x005F807C` bytes `C7 44 24 24 00 FA 45 00` | `0x0045FA00` |
| `PlacementOFF` | `0x005F80A2` bytes `68 A0 13 F3 00` | `0x005F80AB` bytes `C7 44 24 28 00 FA 45 00` | `0x0045FA00` |
| `PlacementCancel` | `0x005F80D1` bytes `68 90 13 F3 00` | `0x005F80DA` bytes `C7 44 24 28 00 FA 45 00` | `0x0045FA00` |
| `CheckPlacementAlive` (control) | `0x005F8100` bytes `68 7C 13 F3 00` | `0x005F8109` bytes `C7 44 24 28 A0 A5 62 00` | `0x0062A5A0` (false-return stub คนละตัว) |

ทั้งสี่ record ส่งผ่าน delegate wrapper `0x00460AE0` และ registration helper `0x00AD4390`; association ของ `PlacementOFF` ไม่ได้มาจากชื่อใกล้กันเฉย ๆ แต่เป็น immediate name pointer + delegate pointer ใน record เดียวกัน. Exact string/dword census ครบทั้ง `.text` และ `.code`; name string/reference มีอย่างละหนึ่งจุด จึงไม่มี registration ตัวที่สองใน image นี้.

trigger→script→scene binding ฝั่ง asset **ยัง resolve ไม่ได้**: ไม่พบชื่อสคริปต์ใน image/61 scene files และ R137 ปิดทางตารางแล้ว. ผลนี้ไม่ถูกยกเป็นเหตุผลเดาความสัมพันธ์ฉาก; มันไม่จำเป็นต่อคำตอบ namespace เพราะ delegate ที่ลงทะเบียนไม่ใช้ argument ตั้งแต่ต้น.

## จ็อบ 2 — namespace และด่าน control

`0x0045FA00` exact body `[0x0045FA00,0x0045FA05)`:

```text
33 C0       xor eax,eax
C2 04 00    ret 4
```

ไม่มี load จาก `[esp+4]`, ไม่มี call/jump, ไม่มี array/index/lookup, และคืน 0 เสมอ. ดังนั้น 59/60/61 ไม่ได้ถูกแปลงเป็น `.npc` index, definition index, wire band หรือ id table ใดใน shipped build นี้.

ด่าน control ผ่าน: Bg3003 max 33 และ Bg3004 max 45 ที่ดู “อยู่ในช่วง” ก็ถูก ignore แบบเดียวกับ Bg3001 max 56/Bg3002 max 61. วิธีนี้ไม่ได้เลือกอธิบายเฉพาะเลขเกิน. `PlacementON`/`PlacementCancel` ใช้ no-op เดียวกัน และ `CheckPlacementAlive` bind stub `[0x0062A5A0,0x0062A5BE)` ที่ push false/คืน Lua result 1 — ครอบครัว API placement ใน build นี้เป็น stubbed surface อย่างสอดคล้องกัน.

## Jobs 3–4

- จ็อบ 3 ตัวอย่างชี้ entity ≥3 จุด: **N/A** — ไม่มี namespace/lookup ให้ resolve row; ฝืน join literal กับ `.npc` จะผิดกฎ crosswalk.
- จ็อบ 4 ผูก band `0x2000+N+1`: **N/A / ห้ามผูก** — no-op ไม่ผลิต entity index. ผล GT-022/048/053 ไม่ถูก re-verify หรือขยายไป Bg300N.

## Span pins และ census

| ชื่อ | span / file off / len | sha256 |
|---|---|---|
| Scene registration | `[0x005F8010,0x005F81C9)` · `0x001F7410` · 441 | `a13b9e872cff0cb6517e8c47016ba6e43b83b31010873e07e2212abef88947b6` |
| delegate no-op | `[0x0045FA00,0x0045FA05)` · `0x0005EE00` · 5 | `5fed5afb29946811bf02359627a94bc01d08d31b779528feaadde3866af9c855` |
| delegate wrapper | `[0x00460AE0,0x00460AFD)` · `0x0005FEE0` · 29 | `65cb6bc96344924f84fb029b818e34d133579113a4aa395af6a5f642961724f9` |
| registration helper | `[0x00AD4390,0x00AD4512)` · `0x006D3790` · 386 | `f98232a277b4c84e79438fb04d80a05ae946f22dc8a216c8f9a848d8d00f6073` |
| alive false stub (narrow exact) | `[0x0062A5A0,0x0062A5BE)` · `0x002299A0` · 30 | `655529da0f755fc6980e56aa2b9acc3395bcca439f99e62002a70b678075de05` |

Recursive CFG ของ 4 heuristic spans: decode errors รวม 0. Negative census ใช้ raw ASCII/UTF-16LE, bytewise `E8/E9`, dword refs และ exact record bytesบน executable sections 2 ส่วน; **ไม่ใช้ linear disassembler เป็นหลักฐานผลลบ**. `0x0045FA00` มี dword refs global 464 เพราะเป็น generic no-op ที่ใช้กว้าง — คำตัดสินของใบพึ่ง record-local pairing ที่ `0x005F80A2/AB`, ไม่ใช่จำนวน global.

## SHA ก่อน/หลัง

- `GameClient.local.bin` 14,759,424 bytes: `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`
- decoded Lua:
  - Bg3001 829 bytes `35859c4321a4301a73705ea0212ccaeb767d0bbdf8e09abe76bfa4dfd139320e`
  - Bg3002 1,136 bytes `eeefa5b90e9ee1d92a991fab40343927a34dda1b3ebe814ac6b62241bb561fe3`
  - Bg3003 558 bytes `a8f7284e5196245a43be93044aa4b9f7f02277a05b59aa379839c325f6923627`
  - Bg3004 940 bytes `f0db9de54de3fbcdac13c6d36788ffc59a899fdcfae91ac3507434ec11270abe`
- shipped `.lu_`: Bg3001 `3444fbcc95bf34bb249c27256e0e8b85ae3ffdb576d6c6e084083e026439e5b0`; Bg3002 `e3086d98f0b3006fa5ee8ebf685e2db46530e30bf40b8a429d6832dcbb0566c7`; Bg3003 `0572f56659f8b2a8bb385f9029cd88f876059181dfdfce10ae51bfda3639d919`; Bg3004 `bb9550451e86fb2c56c759265280c69ff644d9573fa4119eb3bb724669f083e0`.
- 61 scene files: individual hashes in JSON; combined manifest sha `f9aa96353abe1d4b7d575ed9c6b187841839e362f125908beaf56e6c30834588`.
- R136 `11fa49b6764e845ede8a65f429095fd4fb9f23ba74d3fdf781b6ac1713d491d2`; R137 `f43dd7f628bc5149cc4922a37686c2f7eb07b30f4716ccaee2c19216864e17bc`; prework 0901 `cedb71b3e348f3a14c0ca5544c070cd21ff4bbf3cc5692c0c301aba9547e908c`; `external\00_SEARCH_HERE_FIRST.md` `6f6c092c0af1363afa4fd03bf21c053991b5f985ec17587a8e1d2d96edb1a459`.

Read-only tool: `logs\re057_20260824\re057_probe.py` sha `7e0ea5ee1b57d3d4541af7fbd39cb73acc46bbbe27e095c0a9b67969de555410`; output `re057_probe.json` sha `6a7e7e1962712947860ee89ebdcd23bd4ffbc4d888dcdf4f82e4662916fa6a90`; guards 5 spans, 2 exec sections, 61 scene files, errors 0, exit 0.

## Nonclaims

- สคริปต์/อิมเมจ client คือสิ่งที่ client build นี้ถือ ไม่ใช่กฎของเซิร์ฟเวอร์ต้นฉบับ ซึ่งปิดไปแล้วและกู้ไม่ได้.
- ไม่พิสูจน์ว่า runtime เรียกสคริปต์เหล่านี้จริง; และไม่ผูกชื่อไฟล์ `_for_bg300N` เป็น scene binding.
- ไม่ claim ว่า revision/client build อื่นไม่มี implementation; คำตัดสินจำกัดเฉพาะ image sha ที่พิน.
- ไม่ join เพราะเลขอยู่ในพิสัยเดียวกัน และไม่ claim entity mapping จาก literal ใด.
- ยังไม่มีการผูกชื่อ Lua API เข้าชื่อ wire message; ใบนี้ไม่สร้าง mapping ดังกล่าว.
- ไม่ re-verify band `0x2000+idx+1`; ฉากนอก bg0001/Bg0002 ยังเป็น inference หากใครกล่าวถึง.
- ไม่มีหลักฐาน client-observable และห้ามใช้งาน static นี้อ้างว่า entity หาย/ไม่หายบนจอจริง.
- ไม่แก้ image, source asset, gamedata, queue หรือ `.gitignore`.
