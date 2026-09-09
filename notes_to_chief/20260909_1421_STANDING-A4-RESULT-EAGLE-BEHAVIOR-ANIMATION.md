งานเป้าหมายยืน — ยังไม่มีเลขใบ ขอให้ LANE-K ตั้งเลขและผูกจดหมายนี้
ADDRESSEE: LANE-B, LANE-K, chief · จาก Codex static RE
เวลา: 2026-09-09T14:21:06+07:00 · STANDING A4 · PARTIAL / NEW-PROGRESS

# A4 — Tornado Eagle มี behavior/animation crosswalk จริง 5 selector; original selector policy ยังเปิด

ปิดช่อง static ที่ใบ A4 `0022` ทิ้งไว้: ถ้า ActionVital ของ Tornado Eagle ใช้ selector หนึ่งในห้าค่าที่แถว MOBS ของมันถืออยู่ Client build นี้มี BEHAVIOR row จริง และ parser ส่งชื่อ animation ของแถวนั้นเข้า `CActorTask_PlayActionEvent` โดยตรง ไม่ต้องสร้าง BEHAVIOR row สังเคราะห์

## IMAGE / A — selector ไป animation task

- inbound ActionVital `0x1AEA` อ่าน u32 ที่ object `+0x30` ณ `0x7517A5`, ส่งค่านั้นเข้า BEHAVIOR lookup `0x7517B0 -> 0x702A10`, แล้วทาง ordinary สร้าง UseBehavior ที่ `0x751809 -> 0x47AB30`
- BEHAVIOR loader `0x491650..0x491882` อ่าน named column `s_ANIMATION` และ `0x49187D -> 0x48F150` แปลรายการ `name;frame`
- parser `0x48F150..0x48F2DE` คำนวณ signed delta จาก frame ก่อนหน้า หารค่าคงที่ double `30.0`, เก็บเป็น float32 ใน animation subrecord; นี่เป็น task threshold ตามโค้ด ไม่ใช่ข้ออ้าง wall-clock seconds
- factory `0x48D3FF -> 0x487CE0`, vtable slot `+0x18 -> 0x47C750`, และ `0x47C7B6 -> 0x471EB0` สร้าง `CActorTask_PlayActionEvent`; constructor คัด threshold/name record ไป task และ Start `0x475170..0x47528A` เรียก owner virtual `+0x28` ด้วย animation string
- ทางนี้พิสูจน์ consumer ของชื่อ animation และ task scheduling boundary ไม่พิสูจน์ว่าทุกรุ่น model มีคลิปนั้น โหลด resource สำเร็จ หรือเห็นภาพจริง

Selected IMAGE spans (half-open; exact local/original image SHA-256 `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`):

| span | file offset | SHA-256 |
|---|---:|---|
| `00491650..00491882` BEHAVIOR animation read | `00090A50` | `9bc2d7fd5533c1becbd59ea97a6f3a5a8e6fd9af2de4b400cee9ac9b01a372` |
| `0048F150..0048F2DE` animation parser | `0008E550` | `6b4d489221250eb4dacf4b407bf111cb21c7c1529e3906e26193b75510353262` |
| `0047C750..0047C7CE` PlayActionEvent factory | `0007BB50` | `dbd84001c53899d52a8987456b611ffd4d911cb733ce1b45f57b5dc202e26a55` |
| `00471EB0..00471F47` PlayActionEvent ctor | `000712B0` | `287e34b64289595550a4a21d6564e91528d51b165c1ca6ad168063193f3aba93` |
| `00475170..0047528A` PlayActionEvent Start | `00074570` | `34953c77c1a2dcc804d010f10405cc503540074784aaa062f17bcad990478f31` |
| `00F13D38..00F13D50` `s_ANIMATION` literal | `00B12138` | `a595510b35e56ff8abfa239b59425b14eec6d14399fb20ace95342ab767d63dd` |
| `00F0DA00..00F0DA12` `BEHAVIOR` literal | `00B0BE00` | `1187c14f7e23c58d346ebe83ac7f804b28970f8ec68d5f451b684a9ddc1ce31d` |

## DATA / A — exact same-build Tornado Eagle crosswalk

ผม parse ใหม่จาก decoded source `B_CONSTDATA_TH.pc_.dec` 8,443,000 bytes, SHA-256 `496dfb2ef2cf517482a7b426c9dd5edf0278564fe11195b96f36df90607f0d2d` ไม่ได้เชื่อ TSV อย่างเดียว

MOBS row 31 (`0035E734..0035E8DC`, SHA `880afb97823b4df4b5e001aea62896f3d8894cae0c2b9c336ab3bcf74f48eeee`) ให้ `s_ID_MODEL_CLASS=M011`, `s_OUTFIT=M011_000_000_SP3`, `n_RANK=1`, `n_AI_COMBAT=214`, `s_SKILLS=3220;3226;3221;3231;3233`.

| selector | exact `s_ANIMATION = s_ANIMATION2` | parser threshold sequence `(frame delta)/30` | other source-named fields |
|---:|---|---|---|
| 3220 | `_F_SENTRY_000;15` → `_F_ATTACK_000;75` | `0.5, 2.0` | range 130; class 32; amount 1; area 130; `HIT(95)`; hit-keyframe `S_H_PHYSICS_PUNCH;0;33` |
| 3226 | `_F_SENTRY_000;15` → `_F_ATTACK_003;84` | `0.5, 2.3` | range 1100; amount 1; emit `4980;0` → `3040;45` |
| 3221 | `_F_SENTRY_000;15` → `_F_ATTACK_001;75` | `0.5, 2.0` | range 100; amount 1; `HIT(95)`; casting FX `S_O_EAGLECLAW;15`; emit `4981;0` → `3033;31` |
| 3231 | `_F_FLEX_000;45` → `_F_ATTACK_002;71` → `_F_ATTACK_002;97` | `1.5, 0.8666667, 0.8666667` | range 600; amount 1; emit `4982;0` → `3045;56` → `3045;82` |
| 3233 | `_F_FLEX_000;130` | `4.3333333` | range 500; amount 1; emit `4984;0` → `3048;120` |

Exact raw BEHAVIOR row spans/hashes:

- 3220 `0008E766..0008E8B4` `ede580b57736608d835f70b94a8897069666574fa81a2c7573ed4b51e71511e4`
- 3221 `0008E8B4..0008EA0E` `7366a69eb0e8f4af357bc3cccebdc9f37161cc6f721fe1f3ad11033ae3de13cb`
- 3226 `0008EEEC..0008F018` `80c9c13b2beebf0d6b87e34aa70ad69b30130ff34abeab3712ba63271544df19`
- 3231 `0008F4C8..0008F63C` `9a8108f928e4710b1b7aa3d0b4d4c54bd0b0ccc7f1e3e6eb3caed518af989822`
- 3233 `0008F7B0..0008F898` `b3d814537399476f001cb58e2ae80bbf59f8a29f3a76dfed8e9fd4a2df3acfed`

SKILL_CONTEXT มีแถวทั้งห้าและแต่ละแถวมี `GO(0) -> CHASE(self-id)`; raw row hashesถูกตรึงใน verifier. AI_COMBAT row 214 (`003321EC..00332414`, SHA `4a4cc106771a2dcfe0f0557fa0105ea4db75652e7e19a35b35f19a42a8ff33f4`) มี action arguments `5,5,2,4,1,3,3,1`, ทุกค่าตกในช่วง 1..5 ของรายการสกิล

**ขอบเขตสำคัญ:** การอ่าน `CHASE(n)` ว่า “slot n ของ MOBS.s_SKILLS” ยังเป็นสมมติฐาน D ตามคำตัดสิน Panya `2032` และ module `mob_ai_rules.py` ก็เก็บ integer โดยไม่ resolve. ดังนั้นตารางข้างบนพิสูจน์ selector→animation เมื่อ selector ถูกเลือกแล้ว แต่ยังไม่พิสูจน์ว่า original server เลือกแถวใดในแต่ละ AI_COMBAT condition. ชื่อ `range`, `area`, `HIT`, `emit` เป็นชื่อคอลัมน์ต้นทาง ไม่ใช่หลักฐาน damage/target/FX ที่เห็นจริง

## Reproducibility

จาก `pf_bridge`:

```powershell
& 'C:\Users\Panya\AppData\Local\Programs\Python\Python314\python.exe' -B .\staged\standing_a4r_verify.py
```

ผล: `PASS rows=12 raw_row_hashes=12 binary_spans=7 calls=6 pins=3 known_answers=5 traps=2`; verifier เป็น stdlib-only และตรวจ image/source ก่อน-หลัง

- verifier SHA-256 `40ad5776cf813e4d7129d43770d148b072a79d53b9c19d8e67df6b1d3dcffaeb`
- verifier log SHA-256 `536e66bc6befe8b72271e08b8c039c985fa053d71194519377d9b9aad20f3854`
- data probe SHA-256 `26a7cc36c494e0b499c9505226e915e068c484fd6179080331576cc826603105`
- data probe log SHA-256 `3d351717d712a0335c71090c99033d620796bfcf8841cb25697c2083ce0338d7`

BUILD_PROPOSED: LANE-B ใช้ selector ที่ data-backed หนึ่งค่าใน ActionVital ของ Tornado Eagle ได้โดยไม่สร้าง registry row; จุดเริ่มที่ย้อนง่ายที่สุดคือ 3220 แล้ววัดบนจอว่าได้ sentry→attack_000 หรือไม่ พร้อมผูก CHitResult และ full UpdateAttr HP ตาม A4 `0022` | acceptance token = selector/performer/target เดียวกัน + clip observed + number + resident/HUD HP reduction + second cycle | ถ้าคลิปไม่ออกหรือ model/resource gate ปฏิเสธ ให้หยุดและเก็บเป็น falsification ไม่สลับ selector แบบสุ่ม

PARTIAL: ปิด same-build selector→animation task mapping; original selector policy, CHASE slot semantics, model resource success, choreography, number/HP ordering และ visible result ยังต้อง attended proof

สภาพแท่น: ไม่เปิดเกม/server ไม่แตะ DB/ServerProject/lease/Git/คิว/reference. ตรวจ RE lock เป็น RELEASED และ image hashเดิมก่อนเริ่ม

SCOREBOARD: NONE | Standing A4 exact Tornado Eagle selector-to-animation crosswalk | IMAGE+DATA only; next=attended proof or next standing item
