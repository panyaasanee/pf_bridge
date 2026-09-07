# CLIENT RE QUEUE -- ARCHIVE 20260907 (closed tickets moved verbatim from `CLIENT_RE_QUEUE.md` by LANE-K round rlapyk; each has a one-line stub left in place; nothing here is deleted)


## 🔬 RE-238 SELECTOR-CATEGORY-TO-ALT-HP-PAIR-MAPPING-001  [✅ **PASS/DONE — SCENE_NAME.n_SCENE_TYPE=8 keys 126/127/128/304/305 pinned** · คำต่อคำจากจดหมาย `notes_to_chief/20260904_1709_RE-238-RESULT-SCENE-TYPE-8-MAPPED.md` (2026-09-04T17:09+07:00) · พับโดย LANE-K รอบ `dmef5j` 2026-09-07T04:09+07:00 · เดิม OPEN -- ร่างโดย LANE-GM รอบ `zq18m1` (ใบ `notes_to_chief/20260904_1154_LANE-GM-RE-0x430E10-TICKET-selector-category-to-alt-hp-pair-mapping.md`) ตาม `COO-DECISION 20260904_1046` ข้อ 2 · **วางคิวและมอบหมายโดย chief รอบ `wjqykr` (R338) 2026-09-04T14:09+07:00** · ผู้ทำ: **สาย RE** (RE runner local, ไม่ต้องจอง) · **LANE-GM บริโภคผลเอง** · 🔴 `[STATIC-ON-BRIDGE]` ต้องดิสแอสเซมบลีอิมเมจ ⇒ ทำบนคลาวด์ไม่ได้]

> 🔴 **เลขใบเปลี่ยนจากชื่อร่างชั่วคราว `RE-0x430E10` เป็น `RE-238`** — ชื่อร่างไม่ใช่เลขใบและตัวนับใบค้นไม่เจอ
> (chief ยืนยัน `notes_to_chief/20260904_1409_CHIEF-TO-LANE-GM-your-0x430E10-ticket-is-re238-paste-the-body.md`) ·
> ตัวนับร่วมสองคิวคืน `237` ⇒ ใบนี้ `238` · `RE-238`/`GT-238` = **0 hit ทั้งสามที่ก่อนวาง** ·
> **LANE-GM ยกเนื้อใบลงเองรอบนี้** ทุกจุดที่เคยเขียน `RE-0x430E10` ในใบต้นทางแทนด้วย `RE-238` ข้างล่างนี้ ·
> โค้ด/เทสของสายนี้เองไม่เคยอ้าง**ชื่อใบ** `RE-0x430E10` เลย (ตรวจแล้ว `grep -rn "RE-0x430E10\|RE_0x430E10" pirate-force-server/src pirate-force-server/tests` = 0 hit) ⇒ ไม่มีจุดต้องแก้นอกไฟล์นี้ —
> 🔴 **ต่างจากที่อยู่นอกเรื่อง**: `attr_wire.py` มี `0x430E10` (VA ของฟังก์ชันไคลเอนต์ ไม่ใช่ชื่อใบ) อยู่หลายสิบจุด
> โดยตั้งใจ (คอมเมนต์อธิบายกลไก selector) — จุดเหล่านั้น**ไม่ใช่**การอ้างถึงใบนี้และไม่ต้องแก้เป็น `RE-238`

- อิมเมจที่ต้องยึด: `GameClient/GameClient.local.bin` 14,759,424 ไบต์
  sha256 `9627211412AC60D50AD189CE5A629443CE928EC23A9F8D219DFB2B157028B623`
  (ค่าเดียวกับที่ `PF_CHUNK2_Q1_ACTORATTR_MASK_FINDINGS_20260819.md` ปักไว้ — ตรวจ sha ก่อนอ่าน)

### ทำไมใบนี้ถึงมีอยู่
`FIELDS` row x=9 (`category_5C`, +0x5C ของ BasicAttr) ค่าที่ส่งเข้าฟังก์ชัน `0x430E10` แล้วผลลัพธ์
เทียบกับ `8` เพื่อเลือกว่า HP ของไคลเอนต์อ่านจาก `+0x44/+0x48` (ปกติ) หรือสลับไปอ่าน
`ActorAttr +0x1A8/+0x1AC` (x=52/x=53) แทน `[PROVEN VA=0x5BD3C0..0x5BD3DB]` (call site เดียวกับ
`0x4564B3` ที่เขียน cached byte `actor+0x358`) นี่คือกลไกเดียวที่ `GT-218` วัดว่าฆ่าไคลเอนต์ได้
(HP `0/1` เมื่อ mask ไม่ครบ) รั้วสองชั้นที่เซิร์ฟเวอร์มีวันนี้ (`gm/attr_wire.make_update_attr_frame`,
`_refuse_selector_change`) **ไม่มีตัวไหนอ่าน `0x430E10` เอง** — ตัวหนึ่งเทียบ "ค่าที่จะส่ง == ค่าที่
login ส่งมา" (การเปลี่ยนแปลง ไม่ใช่เงื่อนไข) อีกตัวเทียบ "x9 == 8" ตรง ๆ (ค่านำเข้า ไม่ใช่ผลลัพธ์ของ
ฟังก์ชัน) ทั้งสองมีผลข้างเคียงที่ระบุไว้แล้ว (false positive ที่ฉาก 8 "Silver Harbour", false negative
กับทุกฉากอื่นที่ผลลัพธ์ `0x430E10` เป็น 8 พอดี) เพราะเซิร์ฟเวอร์ไม่มีทางประเมินเงื่อนไขจริง

### คำถามเดียว (ตอบได้แค่บางส่วนก็ปิดบางส่วนได้ ไม่ต้องครบ)

**Q — `0x430E10` แมพค่า `category_5C` (u16) ตัวไหนเป็น 8**
ขอ **decode ฟังก์ชัน `0x430E10` เต็มตัว** (ไบต์ + คำสั่งที่ถอดได้ + span sha256) แล้วตอบ:
- เป็นการเทียบ/lookup โดยตรง (เช่น `switch`/jump table หรือ `if (cat==N) return 8`) หรือเป็น
  การคำนวณ (เช่น bitmask/หาร/ดัชนีเข้าตาราง static)
- ถ้าเป็น lookup โดยตรง: **ชุดค่า `category_5C` ทั้งหมดที่คืนผล 8** (รายการ ไม่ใช่ตัวอย่าง)
- ถ้าฟังก์ชันอ่านตาราง static เพิ่มเติม (ไม่ใช่ input เดียว) ขอ VA + span ของตารางนั้นด้วย
- `category_5C` เป็นรหัสอะไร (scene id / scene category / actor type / อื่น) **ถ้าบอกได้จากโค้ด
  เอง** — ห้ามอนุมานจากชื่อคอลัมน์เดิม (`SELECTOR_NOTE_R301` ในรีโป server ตีกลับชื่อ "scene_id"
  ไปแล้วครั้งหนึ่งเพราะไม่มีหลักฐานในอิมเมจ)

### เกณฑ์ปิดใบ (ชั้นเดียว — static IMAGE เท่านั้น ไม่มีชั้น client-observable และไม่ต้องมี)
- ยกไบต์ + คำสั่งที่ถอดได้ของ `0x430E10` เต็มฟังก์ชัน พร้อม `span_sha256` เทียบกับอิมเมจข้างบน
- ตอบชนิดของฟังก์ชัน (lookup ตรง/คำนวณ) ด้วยคำสั่งที่ยกมา ไม่ใช่ด้วยการเดา
- ถ้าตอบได้: รายการค่า `category_5C` ที่คืนผล 8 ครบทุกตัว (ไม่ใช่ตัวอย่างเดียว)

### ราคาที่ประหยัดได้ถ้าไม่ทำ / ถ้าคำตอบเป็น "ตารางใหญ่เกินไม่คุ้ม"
วันนี้เซิร์ฟเวอร์ปฏิเสธ (stand-down มีบรรทัดคอนโซล) ทุกครั้งที่ x=9 กำลังจะเปลี่ยนค่า — ราคาคือ
ผู้เล่นต้องรีล็อกอินก่อนตี (`COO 1046` ข้อ 3 สั่งใส่ในขั้นตอน `GT-224` แทนการแก้โค้ด) ถ้าใบนี้ตอบ
"ชุดค่าที่คืน 8" ได้ครบ เซิร์ฟเวอร์จะเขียนรั้วจริงแทนรั้ว "ค่าเดียวกับ login เท่านั้น" ได้ — ปลด
ข้อจำกัดรีล็อกอินสำหรับผู้เล่นที่เปลี่ยนฉากแล้วยังอยู่ในหมวดหมู่ HP-ปกติเดิม ถ้าคำตอบคือ "คำนวณ
ซับซ้อนเกิน static" ก็ปิดใบด้วยคำตอบนั้นได้ — รั้วปัจจุบันยืนต่อตามที่ `COO 1046` ข้อ 1 ยืนยันแล้ว

### สิ่งที่ใบนี้ **ไม่** ขอ
- ไม่ขอ decode `0x5BD3C0..0x5BD3DB` (call site) ซ้ำ — decode แล้วใน `PF_CHUNK2_Q1` (`[PROVEN]`)
- ไม่ขอชื่อ "ที่ถูกต้อง" ให้ x=9 — ชื่อ `category_5C` ยืนตาม `SELECTOR_NOTE_R301` (no renames)
- ไม่ขอผลจากจอ/capture — ใบนี้ static ล้วน คนละชั้นกับ `RE-222` (attended, เครื่อง Panya)
- ไม่ขอให้เสนอรั้วเซิร์ฟเวอร์ใหม่ — เขียนโค้ดเป็นงานของ LANE-GM รอบถัดไปเมื่อมีผล ไม่ใช่ของใบนี้

- ค้นแล้วก่อนเปิด (LANE-GM กรอกเอง): `external/00_SEARCH_HERE_FIRST.md`, `gamedata/00_SEARCH_HERE_FIRST.md`
  **เจอไฟล์ ไม่เจอคำตอบ** (`430E10` ไม่ปรากฏในทั้งสองไฟล์) · `external/*.tsv`
  (`PF_PROTOCOL_REGISTRY.tsv`, `PF_SERIALIZER_FIELDS.tsv` ฯลฯ) **ไม่เจอ** ·
  `VITAL_REGISTRY_FROM_CLIENT_BINARY_20260817.tsv` **ไม่เจอ** ·
  `pirate-force-server/reports/PF_CHUNK2_Q1_ACTORATTR_MASK_FINDINGS_20260819.md` **เจอ** ผู้เรียก
  สองจุด + สแปนอิมเมจ แต่ตัวฟังก์ชัน `0x430E10` เอง **ไม่เคยถูก decode** — รายการ "เรียกแต่ไม่ decode"
  ข้อ 12 ของรายงานเดียวกันระบุ `0x430E10` ไว้ตรง ๆ
- links: `COO-DECISION 20260904_1046` (สั่งเปิดใบนี้) ·
  `COO-DECISION 20260904_0846` (รั้ว selector เดิม) ·
  `notes_to_chief/20260904_1409_CHIEF-TO-LANE-GM-your-0x430E10-ticket-is-re238-paste-the-body.md` (ตั้งเลข `RE-238`) ·
  `pirate-force-server/reports/PF_CHUNK2_Q1_ACTORATTR_MASK_FINDINGS_20260819.md`
  (§7.2, ข้อ 12, บรรทัด 143/150-151/200-201/433) ·
  `pirate-force-server/reports/PF_HP_DEATH001_HP_DEATH_AND_RESPAWN_STATIC_20260819.md` ·
  `pirate-force-server/src/pirateforce_foundation/gm/attr_wire.py` (`SELECTOR_NOTE_R301`,
  `make_update_attr_frame`, `_refuse_selector_change`)
- numbering: ตัวนับร่วม (กฎ ②) คืน `237` ⇒ ใบนี้ `238` · `RE-238`/`GT-238` = 0 hit ทั้งสามที่ก่อนวาง
- result: (สาย RE กรอก: ชนิดฟังก์ชัน + คำสั่งที่ถอด + span sha256 + รายการค่าที่คืน 8 ถ้ามี +
  timestamp)

---

### result: (พับโดย LANE-K รอบ `dmef5j` 2026-09-07T04:09+07:00 คำต่อคำจากจดหมาย
`notes_to_chief/20260904_1709_RE-238-RESULT-SCENE-TYPE-8-MAPPED.md`
— สถานะที่จดหมายเขียนเอง: **RE-238 PASS/DONE — SCENE_NAME.n_SCENE_TYPE=8 keys 126/127/128/304/305 pinned**)

คำต่อคำจากจดหมาย: `0x430E10` คือ **`SCENE_NAME.n_ID -> n_SCENE_TYPE`** — เป็น **lookup โดยตรงผ่าน named
gamedata table ไม่ใช่สูตรคำนวณ ไม่ใช่ switch/jump table ใน image** · ค่าที่คืน 8 ครบคือ **126, 127, 128, 304, 305**
· image `GameClient/GameClient.local.bin` 14,759,424 ไบต์ sha256 `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`
· ticket input `CLIENT_RE_QUEUE.md` sha256 `792a6ea3…d704b` · บล็อก RE-238 normalized sha256 `06eee0a1…972ff`
· เริ่ม `2026-09-04T17:02:15.621+07:00` ปิด `2026-09-04T17:09:11.598+07:00`

BUILD_IMPACT (ยกคำต่อคำ): LANE-GM แทน guard แบบ `x9 == 8` ด้วย lookup ที่เทียบ `category_5C` กับ exact set
`{126,127,128,304,305}` ได้ · ต้องรักษา sentinel rule ของ `0` แยกจาก set · **ห้ามตั้งชื่อ `n_SCENE_TYPE=8` เกินหลักฐาน**
Nonclaims: ไม่อ้างชื่อเชิงเกมของ type 8 · ไม่มีชั้น client-observable (ไม่เปิดเกม ไม่มี capture ใหม่) ·
ไม่อ้างว่า server guard ปัจจุบันถูกแก้แล้ว

🔴 **หมายเหตุ LANE-K**: ผลนี้ค้างพับมาตั้งแต่ **2026-09-04T17:09** (2 วันครึ่ง) ⇒ หัวใบบอก `OPEN` ทั้งที่ตอบแล้ว


## RE-263 PAIR-RELATION-ZERO-GATE-REACHABILITY-AND-DEFAULT-BIT-001  [**CLOSED BOUNDED-NEGATIVE** 2026-09-05T13:12+07:00 โดย LANE-GM รอบ `0dlc07` (ผู้ทำ `pf-static-re` บนคลาวด์) -- **เส้นทางที่สองของ P-2 ปิด แต่ไม่ใช่ด้วยเหตุผลที่ใบเดาไว้**: ข้อ 1 ของใบเดาว่า predicate ถูกข้ามไปกับ typed `CNetNPC` tail -- **หักล้างแล้ว** predicate ถูกเรียกบนเลน identity บวกที่ `0x00444018` (เลนที่ FieldMob ตกลงมา) · ที่ทำให้เป็นทางตัน = จุด emit สไตล์ชื่อสองจุด (`0x00443FE9`/`0x00443FF2`) **ไม่ได้อยู่ใน predicate เลย** เกตด้วย receiver = local `CMyActor` singleton (ป้ายชื่อของผู้เล่นเอง) มอนไปไม่ถึงตลอดกาล · และ operand ของ gate เป็นค่าคงที่ `0` ทุก actor เพราะ presence bit ไม่เคยถูกส่ง (เซิร์ฟเวอร์ compose ไม่ได้ด้วย: `compose_sparse_block({39:0})` -> `field_not_approved_for_the_sparse_path` **รันจริงแล้ว**) · ไม่กระทบ `P2_COLOR_WIRING_BLOCKERS` -- `unaddressed_blockers()` ยังคืน `('faction_is_a_fallback_operand_only',)` (วัดรอบนี้) · ผลเต็ม: `notes_to_chief/20260905_1312_LANE-GM-RE-263-RESULT-second-route-is-a-dead-end.md` · 🔴 **ใบนี้แก้คำผิดของตัวเอง** (ดูบรรทัด "ค้นแล้ว" ข้างล่าง) · ป้ายเดิม `[STATIC-ON-BRIDGE]` (artifact ที่ commit ไว้แล้ว ไม่ต้องรอเครื่อง Panya เว้นแต่ผลชี้ว่าต้องอ่าน disassembly ที่ยังไม่มีในสะพาน แล้วให้แก้ป้ายเป็น `[NEEDS-CLIENT-IMAGE]`) · **เจ้าของใบ/ผู้บริโภคผล = LANE-GM** (เหมือน `RE-222` เดิม) · ผู้ทำ = `pf-static-re` บนคลาวด์ · **ไม่บล็อกใคร** -- P-2 ยังรอ `faction_is_a_fallback_operand_only` เหมือนเดิม ใบนี้แค่เปิดทางที่สองที่ยังไม่มีใครเดิน]

> numbering: ตัวนับร่วมสองคิว คืนสูงสุดที่ `261` (`RE-261`) · `262` = `GT-262` (จองแล้ว) ⇒ ใบนี้ `263`
> ที่มา: `notes_to_chief/20260905_1150_LANE-GM-TO-CHIEF-re-ticket-request-pair-relation-zero-gate-reachability.md` (รอบ `srn7ksvmt`)

## ค้นแล้วก่อนเปิดใบ (ผลการ grep -- กติกา `AGENTS.md` §7 · `COO 0646` ข้อ 2 -- ยกจากจดหมายต้นทาง)
**เจอ** -- `notes_to_chief/reference_codex_attr/PF_A2_ATTR_FIELD_DELTA.tsv` rows 6-7 (`grep -n "0x0043C531" notes_to_chief/reference_codex_attr/PF_A2_ATTR_FIELD_DELTA.tsv`): span `0x0043C531`-`0x0043C547` -- อยู่ใน `RELATIONSHIP_PREDICATE_SPAN` เดียวกับที่ `RE-195` วัด (`0x0043C380`-`0x0043C63C`) และมาก่อน `FACTION_COMPARATOR_SOLE_CALL_SITE_VA` (`0x0043C5E0`) · ~~ทดสอบ `ActorAttr+0x98` bit `0x04000000`~~ **← ผิด แก้โดยผลของใบนี้เอง (RE-263): `+0x98` เป็นฟิลด์ **หนึ่งไบต์** `uint8_enum` (`storage_width=1` `tag=0x0B`) และ `0x04000000` คือ **presence bit ใน mask word ที่ `+0x1B4`** ไม่ใช่บิตข้างใน `+0x98` · ไบต์ที่เผยแพร่ในสแปนเป็น `cmp byte ptr [esi+0x98], 0` (`0x0043C531`) กับ `cmp byte ptr [edi+0x98], 0` (`0x0043C53A`) ไม่ใช่ bit test · `gm/attr_wire.py:463` ของเราเองเข้ารหัสถูกอยู่แล้ว (`1 << 26` บน mask, `offset=0x098`)** · semantic name ที่ TSV ตั้งเอง: `CNetActor_pair_relation_zero_gate__CMyActor_value_1_selects_LABEL_NAME_FontStyleID_56_else_55` (พูดถึง FontStyleID ตรง ๆ 56 vs 55) · status = `PROVEN_ROLE_ONLY` (คำของ TSV เอง: "structural/consumer role is proved but the broader gameplay noun or full value domain is not unique") · แถวนี้มาจาก census คนละรอบ **ไม่เคยถูก cross-reference กับ `faction_is_a_fallback_operand_only` มาก่อน**
**ไม่เจอ** -- `grep -rn "FontStyle" gamedata/ external/ archive/ notes_to_chief/consumed/` [วัดแล้ว chief `cwde5m`/R353 addendum, แทนบรรทัดฉบับแรกที่ตัดสินโดยหมวดหมู่ ไม่ใช่ grep จริง — `AGENTS.md` บรรทัด "ประโยคปฏิเสธต้องมี grep กำกับ"]: hit จริง 49 ไฟล์ ทั้งหมดอยู่ใน `archive/` เป็นประวัติของ `RE-191`/style 63 RGB และของจดหมาย `20260831_2245_KA1B-TO-CHIEF-nameboard-fontstyle-selector-presentation-only.md` (ดูหมายเหตุด้านล่าง) -- **ไม่มีแถวไหนใน `gamedata/tables/` เอง** ตอบคำถามสามข้อของใบนี้โดยตรง (reachability ของมอน server-sent ผ่าน gate นี้) `external/00_SEARCH_HERE_FIRST.md`/`gamedata/00_SEARCH_HERE_FIRST.md` เอง ไม่มีแถวชี้มาที่ span `0x0043C400`-`0x0043C547`
🔴 **สิ่งที่เจอใน archive/ ที่ต้องอ่านก่อนตอบใบนี้ (ไม่ใช่ nonclaim ปกติ)**: `archive/notes_to_chief_2026-08/20260831_2245_KA1B-TO-CHIEF-nameboard-fontstyle-selector-presentation-only.md:34` -- **`FontStyle 55 = ขาว, 56 = ชมพูตัวหนา` วัดจากจอจริงแล้ว (MEASURED, client-observable, probe 27 ส.ค.)** ไม่ใช่แค่ IMAGE layer เหมือนแถวอื่นของ TSV เดียวกัน -- ใบนี้ **ไม่ได้ถามความหมายของ 55/56** (รู้แล้ว) แต่ถามว่า**เซิร์ฟเวอร์ไปถึง gate ที่เลือกระหว่างสองค่านั้นได้ไหม**สำหรับมอน (คนละคำถามกับที่ `2245` ปิดไปแล้วสำหรับผู้เล่น) -- ห้ามอ่านผลของใบนี้เป็นการค้นความหมายสี ความหมายรู้แล้ว

## ตรวจไม่ให้ทับ `RE-195` (ปิดแล้ว บังคับตาม `AGENTS.md` §7 "ก่อนเปิดใบ RE ต้อง grep... สิ่งที่ค้นเจอแล้วต้องถูกตัดออกจากคำถามของใบ")
`RE-195` (`CLIENT_RE_QUEUE.md:3914`, CLOSED BOUNDED-NEGATIVE) วัดตาราง style **56/58/59/60/61 ครบแล้ว** แต่บรรทัดสรุปของมันเอง (อ้างที่ `CLIENT_RE_QUEUE.md:5313`) ระบุตรง ๆ ว่า **"ไม่มีแถวชื่อ ชมพู"** ในตารางนั้น -- คือ RE-195 วัดตระกูล 56/58/59/60/61 ในความหมาย "reachable ทางไหน" แต่ตัวแยก **55 vs 56** (ซึ่งคือคำถามของใบนี้) ไม่ได้อยู่ในผลของมัน ⇒ **คำถามของใบนี้ไม่ถูกตัดออก ยังเป็นคำถามที่ยังไม่มีคำตอบจริง** ไม่ใช่การถามซ้ำ

## คำถามของใบ (จาก `PROVEN_ROLE_ONLY` ไปสู่คำตอบที่ใช้ได้จริง)
1. มอนที่ผ่านทาง `field_mobs`/`load_roster` (measured-bypass identity class เดิม) เคยไปถึง gate นี้จริงไหม หรือ gate นี้ถูกข้ามไปพร้อมกับ typed `CNetNPC` tail ทั้งก้อน (อ่าน disassembly/RTTI จริง ไม่ใช่เดาจากชื่อ)
2. ถ้าไปถึง -- ไคลเอนต์อ่านค่า default ของ `ActorAttr+0x98` bit `0x04000000` อย่างไรเมื่อเซิร์ฟเวอร์ไม่เคยส่งบิตนี้เจตนา (เราไม่เคยส่งบิตนี้)
3. gate นี้กับ faction comparator (`0x0043C5E0`) เป็นเส้นทาง**คู่ขนาน**ที่ predicate เดียวกันเช็คก่อนถึงจุดไหน หรือเป็นเส้นทาง**แยกกันคนละผล** (ถ้าขนาน อาจเป็นทางที่สองที่ไปถึง FontStyleID ได้โดยไม่ผ่าน faction เลย)

## เกณฑ์ปิดใบ (ชั้น static เท่านั้นในไฟล์นี้)
- ปิดใบ **PASS/ANSWERED** ได้เมื่อทั้งสามข้อข้างบนมีคำตอบจาก disassembly/RTTI จริง (ไม่ใช่จากชื่อ semantic ที่ TSV ตั้งเอง) พร้อม VA/offset ที่อ้างอิงได้
- ปิดใบ **BOUNDED-NEGATIVE** ได้ถ้าข้อ 1 ตอบว่า "ไม่ถึง" (มอน server-sent ข้าม gate นี้ไปกับ typed tail ทั้งก้อน) -- คำตอบนี้ถือว่าปิดใบเช่นกัน (ปิด P-2 เส้นทางที่สองนี้เป็น dead end ไม่ใช่ความล้มเหลวของใบ) และไม่ต้องตอบข้อ 2/3 ต่อ
- ปิดใบ **NEEDS-CLIENT-IMAGE** ได้ถ้า `pf-static-re` พบว่าต้องอ่าน disassembly ที่ไม่มีในสะพาน -- แก้ป้ายแล้วส่งต่อคิว RE runner ตามปกติ ไม่ใช่การปิดใบ

## ใบนี้ไม่ขอ
ไม่ขอเปลี่ยนคำตอบของ `P2_COLOR_WIRING_BLOCKERS` (`unaddressed_blockers()` ยังคืน 1 ตัวเหมือนเดิม) · ไม่ขอแตะ `gm/name_color_gate.py` เพิ่มจากที่ปักไว้แล้วในรอบ `srn7ksvmt` (ดู PR เซิร์ฟเวอร์ของรอบนั้น) · ไม่อ้างว่าเร่งด่วนกว่าใบอื่นในคิว · ไม่ขอความหมายของ FontStyle 55/56 (รู้แล้ว MEASURED — ดูช่องค้นด้านบน)

## ห้ามสรุปสิ่งเหล่านี้ (nonclaims)
① `PROVEN_ROLE_ONLY` เป็นคำตัดสินของ `PF_A2_ATTR_FIELD_DELTA.tsv` เอง (ชั้น IMAGE) ไม่ใช่คำตัดสินของใบนี้ ② ห้ามเดาคำตอบข้อ 3 (ขนาน/แยกกัน) จากชื่อ semantic ที่ TSV ตั้งเอง ("`pair_relation_zero_gate`" เป็นชื่อที่คนตั้งใบ TSV ให้ ไม่ใช่ผลจาก disassembly ของใบนี้) ③ การที่ span อยู่ใน `RELATIONSHIP_PREDICATE_SPAN` เดียวกับ `RE-195` **ไม่ได้แปลว่า** reachability ของทั้งสองจุดเหมือนกัน (ดูหัวข้อ "ตรวจไม่ให้ทับ RE-195" ด้านบน) ④ ไม่มีข้อมูล capture ของมอนจริงในใบนี้ — สามข้อคำถามตอบได้จาก static เท่านั้น ถ้าตอบไม่ได้จาก static ⇒ ป้าย `[NEEDS-CLIENT-IMAGE]`

## ถ้าผลออกทางลบ
ข้อ 1 ตอบ "ไม่ถึง" (มอน server-sent ข้าม gate นี้ไปกับ typed `CNetNPC` tail ทั้งก้อน) ⇒ **ปิดใบ BOUNDED-NEGATIVE** ตามเกณฑ์ข้างบน ไม่ใช่ความล้มเหลว — เป็นคำตอบที่ปิดเส้นทางที่สองของ P-2 ให้ชัดว่าไม่ใช่ทางออก และ `faction_is_a_fallback_operand_only` (ของ `RE-222`) ยังเป็นทางเดียวที่เหลือเหมือนเดิม · ไม่ว่าผลออกทางใด **ไม่กระทบ `P2_COLOR_WIRING_BLOCKERS`** โดยตรง (ใบนี้ไม่ได้ขอแก้บล็อกนั้น)

## ผลไปถึงใคร
จดหมายผลจ่าหน้า **LANE-GM** (cc chief) · LANE-GM บริโภคเองและปิดหัวใบนี้ในรอบของตัวเอง (§5)

### result:
(ว่าง)

---


## RE-270 SAILING-RESULT-STORE-KEY-COLUMN-DERIVATION-001  [✅ **CLOSED / BOUNDED-POSITIVE (static answered)** · คำต่อคำจากจดหมาย `notes_to_chief/20260906_1330_RE-270-RESULT-SAILING-RESULT-STORE-IS-KEYED-BY-N-ID-COLUMN-ZERO.md` (2026-09-06T13:30+07:00) · พับโดย LANE-K รอบ `dmef5j` 2026-09-07T04:09+07:00 · เดิม 🔴 **OPEN** · **เจ้าของใบ/ผู้เขียนเนื้อใบ/ผู้บริโภคผล = LANE-A** · ตั้งเลขโดย chief (LANE-E) รอบ `6z131u`/R362 ตาม `COO-DECISION 20260905_2349` ข้อ 3 + `20260906_0147` ข้อ 3 · เนื้อใบมาจากจดหมาย `notes_to_chief/20260906_0004_LANE-A-TO-CHIEF-re-ticket-request-*` คำต่อคำ · ป้ายเส้นทางของบ้าน **[STATIC-ON-BRIDGE]** (ต้องเปิดอิมเมจ client จึงเป็นงานบนเครื่องสะพาน ไม่ใช่คลาวด์ · `CHIEF.md` §1) — LANE-A เสนอคำว่า `[NEEDS-CLIENT-IMAGE]` ใน `0004` ซึ่งไม่ใช่หนึ่งในสามป้ายที่ `pf_re_queue_taglint.py` รู้จัก chief จึงแปลงเป็นป้ายบ้านให้ ความหมายเดียวกัน · **ไม่บล็อก `GT-233` v3** (`2349` ข้อ 3 ระบุชัดว่า "ไม่เลือก (ก) เป็นเงื่อนไขบูต")]

**ทำไมต้องมีใบนี้**: `RE-265` ปิด BOUNDED-NEGATIVE โดยวัดได้ว่า record `+0x14` ถูก lookup ใน store ที่ client สร้างจากตาราง `SAILING_RESULT` จริง **แต่ไม่เคยวัดว่า store นั้นคีย์ด้วยคอลัมน์ไหน** (pf-adversary รอบ `tk4hr7` D3: `n_ID` เป็นสมมติ ไม่ใช่ค่าที่วัด) · `GT-233` v3 ใช้นัดเดียวที่มีทดสอบสองสมมติฐานพร้อมกัน (dock 153 = `n_ID` · dock 154 = `n_AREA`) — ใบนี้ตอบคำถามเดียวกันจาก disassembly แทนที่จะต้องเดาจากผลบนจอ

## ค้นแล้วก่อนเปิดใบ (`AGENTS.md` §7 grep-before-RE · LANE-A รายงานใน `0004`)
**ไม่เจอ** -- `external/PF_PROTOCOL_REGISTRY.tsv` · `external/PF_SERIALIZER_FIELDS.tsv` · `external/00_SEARCH_HERE_FIRST.md` grep `0072F700`/`0x0072F700` = 0 hit ⇒ ไม่มี layout ที่พิสูจน์แล้วบนสะพานสำหรับ VA นี้ (chief ยืนยันซ้ำรอบ `6z131u`: คำสั่งเดียวกัน 0 hit)

## คำถาม
`SAILING_RESULT` store ที่ client สร้างที่ `0x0072FE50` (`RE-265` วัดไว้) คีย์ด้วยคอลัมน์ไหนของ `CONSTDATA_TH__SAILING_RESULT.tsv` — อ่าน key จาก loop ที่ `0x0072F700` ตอนสร้าง store · ผู้สมัคร: `n_ID` (สมมติเดิม ไม่เคยวัด) · `n_AREA` (สมมติใหม่ `2349`) · composite/packed index ที่ TSV export ไม่เก็บ (ยังไม่ตัดทิ้ง)

## เกณฑ์ปิดใบ
- ปิดได้เมื่อชี้คอลัมน์ได้หนึ่งคอลัมน์พร้อม provenance (VA + `span_sha256` + บรรทัด disassembly ที่อ่าน field นั้นจริง) — หรือพิสูจน์ว่า key ไม่ได้มาจากคอลัมน์เดี่ยว (composite/packed) พร้อมสูตรที่อ่านได้
- **ผลลบเป็นผลที่ใช้ได้**: "อ่าน loop แล้วแยกไม่ออกว่าคอลัมน์ไหน" = ปิดแบบ `BOUNDED-NEGATIVE` พร้อมขอบเขตที่ค้นไปจริง
- ปิดโดยไม่มีชั้น client-observable = `BOUNDED-NEGATIVE` เท่านั้น ห้ามเขียน DONE (ชั้น client-observable ของเรื่องนี้คือ `GT-233` v3 ไม่ใช่ใบนี้)

## nonclaims ของใบนี้
ไม่ขอให้ตัดสินว่า `GT-233` v3 ควรบูตหรือไม่ (บูตได้แล้ว ไม่รอใบนี้) · ไม่ขอคำตอบว่าหน้ารายงานกัปตันเปิดด้วยอะไร (คนละคำถาม ถ้าจะถามต้องเป็นใบใหม่) · ไม่ขอให้แก้โค้ดเซิร์ฟเวอร์

ATTENDED: ใบนี้เป็น static ล้วน — **ไม่ต้องเปิดเกม ไม่ต้องจับ `LOCK_GAME` ไม่กินคิวเครื่องของผู้เทส**
ATTENDED: สิ่งที่ต้องมีบนเครื่อง = อิมเมจ client + disassembler เท่านั้น (RE runner งานปกติ) — อ่าน `0x0072F700` ถึง `0x0072FE50`
ATTENDED: ผลที่ส่งกลับ = ชื่อคอลัมน์ + VA + `span_sha256` — หรือคำว่า "อ่านแล้วแยกไม่ออก" พร้อมเขตที่ค้น

### result:
(พับโดย LANE-K รอบ `dmef5j` 2026-09-07T04:09+07:00 คำต่อคำจากจดหมาย
`notes_to_chief/20260906_1330_RE-270-RESULT-SAILING-RESULT-STORE-IS-KEYED-BY-N-ID-COLUMN-ZERO.md`
— หัวข้อ "สถานะที่ขอให้ chief ปิด" ของจดหมายเขียนว่า:)

**`RE-270` → CLOSED / BOUNDED-POSITIVE (static answered) · checkpoint = method ceiling ของชั้น static
(ตอบครบคำถามเดียวของใบแล้ว) ⇒ ห้าม rerun image เดิมกับคำถามนี้จนกว่า chief จะเปลี่ยน objective**

คำตอบหนึ่งบรรทัด: `SAILING_RESULT` store ที่ `0x0072FE50` คีย์ด้วย **`n_ID`** (คอลัมน์ที่ 0 ของ record)

BUILD_IMPACT (ยกคำต่อคำ): **ไม่มีการแก้โค้ดในรอบนี้** (ใบเป็นคำถาม static ล้วน) · ผลที่ LANE-A ใช้ได้ทันที:
ถ้าจะ provision ให้ record `+0x14` ของ `NavigationEx_AddSurveyDataVtial` lookup ติด ต้องส่งค่าที่เป็น
**`n_ID` ของแถว `SAILING_RESULT`** (1..138 ตามไฟล์ที่ commit) — **ไม่ใช่ `n_AREA`** (ค่า `126` ฯลฯ) ·
สมมติฐาน dock 154 = `n_AREA` ของ `COO-DECISION 20260905_2349` **ถูกหักล้างจากฝั่ง static แล้ว**
แต่ `GT-233` v3 ยังเป็นชั้นที่ยืนยันบนจอ

🔴 **หมายเหตุ LANE-K**: `NOW.md` `PANYA 1910` สั่ง **"GT-233 ปิด ห้าม trial `AddSurveyData`"** ⇒ เสมียนยก
BUILD_IMPACT มาคำต่อคำตามหน้าที่ แต่ **ไม่ได้แปลว่าให้ใครไปทำ** — ใครจะใช้ผลนี้ต้องอ่าน NOW ก่อน

> 🔴 **ห้ามสายอื่นใช้เลข `RE-270`** · numbering: คำสั่งนับเลขของบ้าน (`grep -ohE '\b(GT|RE)-[0-9]{3}\b' GAME_TEST_QUEUE.md CLIENT_RE_QUEUE.md archive/*QUEUE*ARCHIVE*.md | ... | tail -1`) คืน **267** รอบ `6z131u` ⇒ เลขว่างตัวแรกคือ 268 **แต่ chief ข้ามไป 270** โดยเจตนา: `GT-268` (LANE-A ฉาก 304 census) และ `GT-269` (LANE-GM P-3 GMUI) ถูกประกาศเป็นของสองสายนั้นไปแล้วในจดหมาย `FROM_CHIEF_R361_TO_ALL_20260906_0040.md` (เนื้อใบยังไม่ลงไฟล์ จึงยังไม่นับในคำสั่งข้อ ②) — การหยิบ 268/269 มาใช้จะชนกับสองสายที่กำลังเขียนเนื้อใบอยู่
> 🔵 ตัวนับร่วมกับ `GAME_TEST_QUEUE.md` · ใบนี้ไม่จองเลขล่วงหน้า — เนื้อใบมาครบก่อนลงไฟล์ตามข้อ ① ของกติกาไฟล์นี้


## RE-283 GMUI-THREE-PAGES-BUTTON-TO-OPCODE-MAP-001  [✅ **ปิดครบทั้ง 5 ข้อแล้ว** (คำของจดหมายเอง) · `notes_to_chief/20260907_0331_RE-283-RESULT-FINAL-BUTTON-OK-SENDS-GM_RunGMCommandVital-NO-LOGTYPE-ON-THE-WIRE.md` (2026-09-07T03:31+07:00) · พับโดย LANE-K รอบ `dmef5j` 2026-09-07T04:09+07:00 · เดิม 🔴 **OPEN** · 🔺 `[NEEDS-CLIENT-IMAGE]` (ต้องอ่าน `.model`/`.project` + โค้ดไคลเอนต์จริง ไม่ใช่งานคลาวด์) · **เจ้าของใบ/ผู้เขียนเนื้อใบ/ผู้บริโภคผล = LANE-GM** · ตั้งเลขโดย LANE-K รอบ `zqq4qz` 2026-09-06T16:09+07:00 (คำขอค้างจากรอบ `rsmsia`/`n3s0rg`) · เนื้อใบมาจากจดหมาย `notes_to_chief/20260904_1328_LANE-GM-RE-TICKET-gmui-three-pages-button-to-opcode-map.md` คำต่อคำ · อ้าง: `COO-DECISION 20260904_0245` ข้อ 1 · `COO-DECISION 20260904_1149` · `PANYA-DECISION 20260904_0233` ข้อ 3] [🔒 **CLOSED — เจ้าของใบ LANE-GM บริโภคผลแล้วและขอปิดหัวใบ** · ปิดโดย LANE-K รอบ `70l5du` 2026-09-07T05:10+07:00 · จดหมาย `notes_to_chief/20260907_0500_LANE-GM-TO-K-re283-final-consumed-close-the-head.md` (2026-09-07T04:24+07:00) · เจ้าของใบวาง `.CONSUMED.txt` + สำเนาไป `consumed/` เองแล้วในรอบ `vxr32s` · ใช้ผลไปแล้ว: ชื่อจริงของหน้าต่าง GM ทั้งสามหน้าอยู่ใน `gm/gmui_catalog.py` แทน placeholder · สาม fact ที่ยังไม่ใช้ (เจ้าของใบเขียนว่ารอบหน้าเป็นงานแรก): (1) ปุ่ม GM ทุกปุ่มส่งเฟรมเดียวกัน `0x51E9` `GM_RunGMCommandVital` ⇒ เซิร์ฟเวอร์ต้อง dispatch ตามบิตที่ `+0x10` ไม่ใช่ตาม opcode (2) ไคลเอนต์ตัด `/` ตัวแรกทิ้งก่อนส่ง (3) `n_LogType` (97 ชนิด) ไม่มีบนสาย · nonclaim ของเจ้าของใบ: **ไม่อ้างว่า `GT-279` ขยับ** — ใบนั้นค้างที่ `capture_raw_gm_command` ไม่เขียนไฟล์ ซึ่งเป็นคนละข้อกับที่ `RE-283` ตอบ]

**หัวเรื่อง**: สารบัญปุ่ม GMUI ทั้งสามหน้า — ปุ่มไหนอยู่หน้าไหน และแต่ละปุ่มส่ง opcode อะไร

### ค้นแล้ว: เจอ/ไม่เจอ
- `pf_bridge/external/00_SEARCH_HERE_FIRST.md` — **ค้นแล้ว: ไม่เจอ** สารบัญ widget/ปุ่มของ GMUI
  ไม่มี artifact ใดใน `external/` ที่ผูก widget → หน้า → opcode
- `pf_bridge/gamedata/00_SEARCH_HERE_FIRST.md` + `gamedata/tables/` — **ค้นแล้ว: เจอบางส่วน**
  - `TEXTDATA_TH__GMTOOL.tsv` = 97 แถว `n_ID / n_LogType / s_MESSAGE` (ประเภท log ของ GM tool)
    🔴 นี่คือ **ประเภท log ของปฏิบัติการ GM ไม่ใช่ปุ่ม** ไม่มี artifact ไหนผูกแถวเหล่านี้กับ widget
    (คัดลอกเข้ารีโปเซิร์ฟเวอร์แล้วที่ `gm/data/gm_tool_log_types.tsv` พิน sha)
  - `TEXTDATA_TH__UI_MESSAGE.tsv` — สตริง `GMUI` โผล่แถวเดียว (id 1549) ไม่มีรายชื่อปุ่ม
- `patches/gm_plugin/GameMaster.cpp` (GM-DATA-001/002) + `docs/GM_LANE.md` —
  **ค้นแล้ว: เจอ** `GMUI.project` ประกาศ `GMUI_1` · `GMUI_1.model` เป็นไฟล์เดียวใน 534 `.model`
  ที่มีแท็บลูกชื่อ `GMUI_BASIC` · **ไม่มี** `GMUI_BASIC.model`
  ⇒ ชื่อหน้าที่มี artifact รองรับ = **หนึ่งหน้า** (`GMUI_BASIC`) จากสามหน้าที่เจ้าของเห็นบนจอ

### ทำไมสายนี้ทำเองไม่ได้
โคลนคลาวด์ของสายนี้ **ไม่มี client image · ไม่มี capture corpus · ไม่มีหน้าจอ** สารบัญที่ `0245`
สั่งต้องอ่านจาก image: `.model`/`.project` บอกว่า widget ตัวไหนอยู่แท็บไหน และโค้ดของไคลเอนต์บอกว่า
widget ตัวไหนยิงเฟรมอะไร ทั้งสองอย่างอ่านที่นี่ไม่ได้ สายนี้จะ **ไม่เดา** แถวสารบัญ

### คำถามของใบนี้ (ตอบเป็นตาราง)
สำหรับ **ทั้งสามหน้า** ของ GMUI (หน้าที่รู้ชื่อแล้ว = `GMUI_BASIC` · อีกสองหน้าต้องได้ชื่อจาก image):
1. **ชื่อหน้า** ทั้งสาม ตามที่ `GMUI_1.model` (หรือไฟล์ `.model`/`.project` ที่เกี่ยวข้อง) ประกาศจริง
2. ต่อหนึ่งหน้า: **รายชื่อ widget ที่กดได้** (ชื่อ resource ตามที่ shipped data สะกด) และป้ายบนจอถ้ามี
3. ต่อหนึ่ง widget: **เฟรมที่ไคลเอนต์ส่งเมื่อกด** — vital id (hex) และ layout ถ้าอ่านได้
   ตอบว่า "ไม่ส่งอะไรออกสาย" ก็เป็นคำตอบที่ใช้ได้ ต้องบอกว่ารู้ได้อย่างไร
4. widget ที่กดแล้ว **ต้องกรอกค่าก่อน** (ช่องกรอก/ดรอปดาวน์) ให้ระบุว่าค่านั้นไปอยู่ฟิลด์ไหนของเฟรม
5. ถ้า widget ไหนผูกกับแถวใน `TEXTDATA_TH__GMTOOL` (97 ประเภท log) ให้ระบุ `n_LogType`
   ไม่ผูก = ตอบว่าไม่ผูก 🔴 ห้ามจับคู่ด้วยความหมายของข้อความ ต้องมีหลักฐานจาก image

### เกณฑ์ปิดใบ (สองชั้น)
- ชั้น wire/static: ตารางครบสามหน้า ทุกแถวมี provenance (ไฟล์ + offset/VA หรือชื่อ resource)
  แถวที่ตอบไม่ได้ต้องเขียนว่า "ตอบไม่ได้ เพราะ ..." ไม่ใช่เว้นว่าง
- ชั้น client-observable: **ไม่ใช่เกณฑ์ของใบนี้** — ใบนี้เป็น static ล้วน ใบ GT ต่อปุ่มจะเปิดทีละใบ
  ตาม `0245` เมื่อรู้แล้วว่าปุ่มมีกี่ตัว

### ใบนี้เป็นใบเดียว ไม่ใช่ใบต่อปุ่ม — เพราะอะไร
`0245` สั่ง "ปุ่มที่ต้องการ RE ให้ออกใบ RE ทีละใบ" ซึ่งถูกต้องเมื่อรู้รายชื่อปุ่มแล้ว
ตอนนี้ยังไม่รู้แม้แต่จำนวน ⇒ ใบนี้คือใบที่ทำให้ "ทีละใบ" เป็นไปได้ ใบต่อปุ่มจะตามมาหลังใบนี้ปิด

### links
`src/pirateforce_foundation/gm/gmui_catalog.py` (รอบ `zjbjys`, สร้างไปแล้วโดยไม่รอใบนี้ — ถือแถวที่มี
artifact รองรับจริง 7 vital + 97 ประเภท log + ตารางปุ่มว่างโดยเจตนา + `assert_backed()`)

### result:
(พับโดย LANE-K รอบ `dmef5j` 2026-09-07T04:09+07:00 คำต่อคำจากจดหมาย
`notes_to_chief/20260907_0331_RE-283-RESULT-FINAL-BUTTON-OK-SENDS-GM_RunGMCommandVital-NO-LOGTYPE-ON-THE-WIRE.md`
— หัวจดหมายเขียนเองว่า **"ต่อจาก PARTIAL · ปิดครบทั้ง 5 ข้อแล้ว"**)

- **ข้อ 3 — เฟรมที่ส่งจริง: `GM_RunGMCommandVital`** (ยืนยันด้วยโซ่ static ครบ ไม่ใช่การอนุมานจาก `RE-091`)
- **ข้อ 5 — `n_LogType` (97 ชนิดใน `TEXTDATA_TH__GMTOOL`): ไม่มีบนสาย (bounded negative)**
- ข้อความที่ผู้เล่นพิมพ์ในช่อง Cheatcode ถูกส่ง **โดยตัด `/` ตัวแรกทิ้งแล้ว** — เซิร์ฟเวอร์ต้องไม่คาดหวัง `/` นำหน้า
- ฝั่งรับของไคลเอนต์ใช้ handler `0x00A106C0` ที่ **แชร์กัน 11 คลาส** ⇒ ไคลเอนต์ไม่ทำอะไรเป็นพิเศษเมื่อได้รับ `0x51E9` กลับ

BUILD_IMPACT (ยกคำต่อคำ): ไม่มีการแก้โค้ดโดย RE runner · ปลดบล็อกฝั่งความรู้ให้สาย GM เขียน handler ฝั่งเซิร์ฟเวอร์
ของ `0x51E9` ได้ครบ: อ่าน presence byte → อ่าน (u32 บิตฟังก์ชัน, u32 ตัวเลข, u8 แฟล็ก, string, string) แล้ว
dispatch ตามบิต · `n_LogType` เลือกฝั่งเซิร์ฟเวอร์เอง

Nonclaims (ยกคำต่อคำ): ไม่อ้างว่าเซิร์ฟเวอร์ต้องตอบอะไรกลับ · ไม่อ้างความหมายของสตริงที่สอง (`+0x38`) ·
ไม่อ้างว่า 17 บิตครบทุกฟังก์ชันของ GMUI · **ไม่ได้ยืนยันด้วย capture จริง** (`PF_FIELD_VALIDATION` ของเฟรมนี้
ยังเป็นเรื่องของชั้น attended) · read-only ล้วน

🔴 **หมายเหตุ LANE-K**: `NOW.md` (`0405`) บันทึกไว้แล้วว่า P-3 `GT-279` **"ปุ่มส่ง `0x51E9` จริง แต่
`capture_raw_gm_command` ไม่เขียนไฟล์ (RE-283 `0331`)"** ⇒ ชั้น attended ยังไม่ปิด ใบนี้ปิดเฉพาะชั้น static

> 🔴 **ห้ามสายอื่นใช้เลข `RE-283`** · numbering: ตัวนับร่วมสองคิว + `archive/*QUEUE*ARCHIVE*` คืน **282** (`RE-282`, ตั้งเลขรอบเดียวกัน `zqq4qz`) ⇒ ใบนี้ **283** · ตรวจ 0 hit ของ `GT-283`/`RE-283` ทั้งสามที่ก่อนวาง [ตรวจโดย LANE-K รอบ `zqq4qz`]

<!-- moved by LANE-K round spppsd 2026-09-07T14:22+07:00 from CLIENT_RE_QUEUE.md, verbatim, nothing deleted -->

<!-- RE-259 moved verbatim by LANE-K round spppsd 2026-09-07T14:22+07:00 -->
## RE-259 UPDATEATTRVITAL-0X309A-IS-IT-EVER-SENT-FOR-CNETNPC-001  [PASS -- LANE-DB ปิดแล้ว 2026-09-05, ดู pf_bridge/notes_to_chief/20260905_1323_RE-259-RESULT-UPDATEATTR-TARGETS-CMYACTOR-ONLY.md, ตัดกลุ่ม 1+2 (9 VA) ออกจากรายการค้างของ piece 3, ไม่เปิดใบใหม่ (player-only)]

> numbering: ตัวนับร่วมสองคิว + `archive/*QUEUE*ARCHIVE*` คืนสูงสุดที่ `256` (`RE-256`) · `257`/`258` ถูกจองโดยใบ GT สองใบในรอบเดียวกันนี้ => ใบนี้ `259` · `RE-259`/`GT-259` = **0 hit ทั้งสามที่ก่อนวาง** [วัดแล้ว chief `pv4zg1`/R352]
> ที่มา: `notes_to_chief/20260904_1748_LANE-DB-RE-TICKET-piece3-resend-adjudication-11-outlier-vas-sharpened.md` ข้อ (ก) -- จดหมายฉบับนั้นสั่งชัดว่าต้องเป็น **สองใบคนละรูป** ใบนี้ = กลุ่ม 1+2 (9 VA) · กลุ่ม 3 (x=26,27) = `RE-260` **ห้ามรวมสองใบเข้าด้วยกัน**

## ค้นแล้วก่อนเปิดใบ (ผลการ grep -- กติกาใหม่ `AGENTS.md` §7 · `COO 0646` ข้อ 2)
**เจอ**
- `VITAL_REGISTRY_FROM_CLIENT_BINARY_20260817.tsv:66` = `0x309A UpdateAttrVital` [วัดแล้ว chief] (ไฟล์อยู่ราก `pf_bridge` ไม่ใช่ใน `external/`)
- `archive/CLIENT_RE_QUEUE_ARCHIVE_20260827_closed.md:1025` และ `:1032-1036` (`RE-061`/`RE-062` ปิดแล้ว) -- **ตัดคำถามออกไปแล้วครึ่งใบ** [วัดแล้ว chief]: handler ของ `UpdateAttrVital` = `0x5F2400` · resolve target ด้วย **class id ใน generic attribute map** (`lookup 0x463800` / `insert 0x463720`) ไม่ใช่ `[actor+0x3E8]` ไม่ใช่ identity tag `0x32` · bind thunk `0x4698B0` **type-check `CMyActor`** แล้วอ่าน slot ที่ `0x4698DF` โดยไม่สร้าง · slot สร้างที่ `CMyActor` ctor (`0x44CA71`/`0x44CBC1`) · image SHA `9627...B623`
  => 🔺 ชุดนี้ derive จาก attr block ของ `CSkillAttr` (class id `0x1661`) ไม่ใช่ ActorAttr ของ 9 VA นี้ -- **PER-CLASS (§14 ข้อ 13 ค) ห้ามเหมา** ใบนี้จึงยังเปิดจริง แต่คำถามแคบลงตามหัวข้อล่าง
- `notes_to_chief/reference_codex_attr/pf_rederive_attr_semantics.py:5432-5448` = บล็อก `("CNetNPC", {...})` ของ x=7: `source_load_va=0x0045C109` · `producer_va=0x0045C11A` · span `[0x0045BF40,0x0045C15D)` · `span_sha256=afb5662a3f1a81c98de8ed77d82262747b8563ce25be88d041c8dea89e52fb72` · semantic `MOBS.n_SPEED_WALK_...` [วัดแล้ว chief] · `:5471-5472` `("BasicAttr",0x68)/(0x6C) -> "CNetNPC"` มีอยู่แล้วในไฟล์เดียวกัน [วัดแล้ว chief]
- `CLIENT_RE_QUEUE.md:4158` `RE-198` (vital_version byte) · `:3841` `RE-194` (ค่าของ x=7) · `:3756` `RE-193` (ค่า default 7 ฟิลด์) -- แตะคลาสเดียวกันแต่ **คนละคำถามทั้งสามใบ** ไม่มีใบใดถามว่า "ส่งถึง actor คลาสอะไร" [วัดแล้ว chief] => ไม่ใช่ใบซ้ำ

**ไม่เจอ**
- `ค้นใน pf_bridge\external\ แล้ว: ไม่เจอ` -- `grep -rn "CNetNPC\|CMyActor" external/` = **0 hit ทั้งต้นไม้** [วัดแล้ว chief] ⇒ ตอบจาก `external/` ไม่ได้ นี่คือเหตุผลของป้าย `STATIC-ON-BRIDGE`
- `ค้น gamedata แล้ว: ไม่เจอ` -- `grep -in "ActorAttr\|UpdateAttr\|CNetNPC" gamedata/` = **0 hit** [วัดแล้ว chief] (ตรงขอบเขต: เรื่อง wire ไม่ใช่ตารางข้อมูลเกม)
- บรรทัดที่มีทั้ง `UpdateAttrVital|0x309A` และ `CNetNPC|CMyActor` พร้อมกันทั้ง `pf_bridge` = มีแต่ **จดหมายต้นทางเอง** (`...1748...md:73`) กับบันทึกรอบของ LANE-DB (`rounds/DB_20260904_1733_...md:99`) ⇒ เป็นคำถาม ไม่ใช่หลักฐาน [วัดแล้ว chief]
- `persistence_attr_compose.py` **ไม่มีอยู่ในต้นไม้ `pf_bridge`** (`grep -rn RESEND_ADJUDICATED` เจอเฉพาะร้อยแก้วใน `rounds/`+`notes_to_chief/`) [วัดแล้ว chief] ⇒ เลขบรรทัดสองแหล่งขัดกันเอง (จดหมายว่า `:95-113` · `rounds/DB_20260904_1434_f9p5fw...md:49` ว่า "บรรทัด 420") **ห้ามผู้ทำอ้างเลขบรรทัดใดเลย** [ทั้งสองเลข = [เสนอ] ของต้นทาง]
- negative check ของจดหมาย (11 VA + 15 span vs `external/PF_SERIALIZER_FIELDS.tsv` range-intersection = ไม่ตรงสัก span) = **[เสนอ] ของ LANE-DB ยังไม่ทำซ้ำ** · ส่วนที่ chief ยืนยันเองได้: `grep -in "0045C11A\|0045C0D6\|0045C0F9\|0045BF40\|00464AAF" external/` = **0 hit** [วัดแล้ว chief] -- สอดคล้องกัน แต่คนละวิธี ไม่ใช่การ verify วิธีเดิม (G1)

## คำถามเดียว (หนึ่งใบหนึ่งคำถาม ห้ามพ่วง)
เส้นทาง `0x309A`/`UpdateAttrVital` **address ถึง actor คลาส `CNetNPC` ได้หรือไม่ หรือรับเฉพาะ player-class (`CMyActor`) เท่านั้น** -- เดินต่อจากสิ่งที่ปิดแล้ว: (1) type-check `CMyActor` ที่ bind thunk `0x4698B0` เป็น gate เดียวบนเส้นทางหรือไม่ · (2) target resolution ของ handler `0x5F2400` (`0x463800`/`0x463720`) ยอมรับ receiver ที่ไม่ใช่ `CMyActor` ไหม · (3) มี bind/apply site อื่นของ `0x309A` นอก `0x4698B0` อีกไหม

## เกณฑ์ปิดใบ (ชั้นเดียว -- static IMAGE เท่านั้น ไม่มีชั้น client-observable)
- **PASS**: รายชื่อ call site + VA ของ gate ทุกจุดตั้งแต่ handler ถึง apply พร้อม `span_sha256` ทุกช่วง + image sha + `generation_id` แล้วตอบว่า `CNetNPC` เข้าถึงได้/ไม่ได้
- **bounded negative = คำตอบเต็ม ไม่ใช่ผลรอง**: ถ้าพิสูจน์ได้ว่า "player-class เท่านั้น" ⇒ กลุ่ม 1 (x=7,11,12) + กลุ่ม 2 (x=15,30,46,49,50,51) รวม **9 แถวตกประเด็นทั้งชุด** โดย LANE-DB ไม่ต้องวัดอะไรเพิ่ม
- เดินครบแล้วตัน ⇒ ระบุ VA ที่ตัน + บอกว่าอะไรจะปลดล็อก (capture ชนิดไหน หรือใบ static ถัดไป)

## ใบนี้ไม่ขอ
ไม่ขอ **ค่า** ของฟิลด์ใดเลย (`RE-194`/`RE-193` ปิดแล้ว ห้ามขอซ้ำ) · ไม่ขอเรื่อง x=26/27 (= `RE-260` **ห้ามรวม**) · ไม่ขอชั้น client-observable · **ห้ามบูตไคลเอนต์เพื่อปิดใบนี้** · ไม่ขอให้แตะโค้ด

## ห้ามสรุปสิ่งเหล่านี้ (nonclaims -- ยกจากจดหมายต้นทางครบทั้งสี่ข้อ ห้ามตัด)
1. ห้ามเขียนว่าผลใบนี้ทำให้ `RESEND_ADJUDICATED` เติมได้แม้แถวเดียว -- เซตว่าง **โดยเจตนา** และต้องว่างต่อไปหลังใบนี้ปิด
2. negative check กับ `PF_SERIALIZER_FIELDS.tsv` **ไม่** พิสูจน์ว่าไม่มี codec ใดแตะที่อยู่เหล่านี้ในอิมเมจ ~10MB -- พิสูจน์แค่ว่าไม่อยู่ในสารบัญที่สำรวจไว้
3. ยังไม่มีใครตรวจว่า `0x309A` เคยส่งให้ `CNetNPC` จริง -- นั่นคือคำถามของใบนี้ ห้ามตั้งต้นว่ารู้คำตอบ
4. ห้ามเดาความหมาย x=26/27 จากชื่อฟิลด์ (`state_record_forced_flag`/`source_state_appearance_byte`)
5. `[chief เติม]` ผล `RE-061`/`RE-062` เป็นของ `CSkillAttr` (`0x1661`) **PER-CLASS ห้ามเหมา** · และกลุ่ม 1 เป็น **คำเตือน ไม่ใช่คำตอบ**: x=7/11/12 มาจาก MOBS template ของ `CNetNPC` คนละแหล่งกับ construction default ของ 17 แถวที่ใช้ `default_writer_va` กลาง (`0x00464AAF-0x00464E16`) -- resend ค่าเดียวกันให้ NPC อาจผิดตัว
6. `[chief เติม]` G8: ทุกแถวในผลติดป้าย `[วัดแล้ว]`/`[เสนอ]` · G1: ห้ามปิดข้อใดด้วยแหล่งเดียว

## แยกจากใบไหน
`RE-198`/`RE-194`/`RE-193` (คนละคำถาม ปิดแล้วทั้งสาม) · `RE-241` (มอนเดินเข้า `CNetNPC` จริงในชั้น static/wire -- ใบนี้ถามฝั่ง **ส่ง attr** ไม่ใช่ฝั่ง census) · `RE-260` (กลุ่ม 3 -- จดหมายต้นทางห้ามปนกับใบนี้โดยตรง)

## ถ้าผลออกทางลบ
"player-class เท่านั้น" = **ปิด PASS** และ redirect: LANE-DB ตัด 9 แถวออกจากรายการค้างของ piece 3 ได้ทันที เหลือเฉพาะกลุ่ม 3 ที่ `RE-260` ถือ · ถ้าตอบว่า `CNetNPC` เข้าถึงได้จริง ⇒ เป็นคำเตือนแรง (ห้าม resend default กลางให้ NPC) และ LANE-DB ต้องเปิดใบใหม่เรื่อง per-class default -- **ใบถัดไป ไม่ใช่ใบนี้**

## ผลไปถึงใคร
จดหมายผลจ่าหน้า **LANE-DB** (cc chief, COO) · บรรทัดแรกเขียนว่า `ขอให้ LANE-DB กรอก ### result: และปิดหัวใบเอง` (§5) · ไม่ผูก deadline (`PANYA-DECISION 20260904_0233` บันไดไมล์สโตนไม่มีกำหนดวัน)

### result:
(ว่าง -- รอ RE runner)

---


---

<!-- RE-260 moved verbatim by LANE-K round spppsd 2026-09-07T14:22+07:00 -->
## RE-260 ACTORATTR-0X99-0X9A-CONCRETE-OWNER-CLASS-001  [DONE -- LANE-DB ปิดแล้ว 2026-09-05, ดู pf_bridge/notes_to_chief/20260905_1327_RE-260-RESULT-CONCRETE-OWNER-BOUNDED-AT-GENERIC-ACTORATTR.md, x=26/x=27 คงนอก RESEND_ADJUDICATED, ไม่เปิดใบใหม่, ห้าม rerun image เดิมจนกว่าจะมีหลักฐานชนิดใหม่]

> numbering: ตัวนับร่วมสองคิว + `archive/*QUEUE*ARCHIVE*` คืนสูงสุดที่ `256` (`RE-256`) · `257`/`258` ถูกจองโดยใบ GT สองใบรอบเดียวกัน · `259` = `RE-259` => ใบนี้ `260` · `RE-260`/`GT-260` = **0 hit ทั้งสามที่ก่อนวาง** [วัดแล้ว chief `pv4zg1`/R352]
> ที่มา: `notes_to_chief/20260904_1748_LANE-DB-RE-TICKET-piece3-resend-adjudication-11-outlier-vas-sharpened.md` ข้อ (ข) = **กลุ่ม 3 เท่านั้น (x=26, x=27)** · 🔺 จดหมายห้ามรวมใบนี้กับ `RE-259` โดยตรง ("คนละระดับ ห้ามปนกัน") -- ใบนี้เริ่มจากศูนย์ ใบโน้นเดินบนเส้นทางที่มีของอยู่แล้ว

## ค้นแล้วก่อนเปิดใบ (ผลการ grep -- กติกาใหม่ `AGENTS.md` §7 · `COO 0646` ข้อ 2)
**เจอ**
- `notes_to_chief/reference_codex_attr/PF_A2_ATTR_FIELD_DELTA.tsv:8-9` = `ActorAttr@0x99` (R และ W) · `:10-11` = `ActorAttr@0x9A` (R และ W) [วัดแล้ว chief -- เปิดอ่านทีละแถวเอง ไม่ใช่เชื่อบทสรุป] แถวทั้งสี่ให้: `applies_to_class=UNKNOWN_CONCRETE_OWNER_OF_ActorAttr` · `scope_status=UNKNOWN` · `EXPLICIT_AUDIT_OPEN_NO_COMPLETE_TYPED_OWNER_CENSUS` · `scope_blocker="the field behavior/meaning is bounded, but no complete typed owner/consumer-class census proves which concrete class attaches and consumes this Attr field"` · สายสืบทอด `PcRefObject>Attribute>DBAttribute>BasicAttr>ActorAttr` · field name `state_record_forced_flag` (`@0x99`) / `source_state_appearance_byte` (`@0x9A`) · tag `0x0B` len 1 · gate `+0x1BC != 0 AND +0x1B4 & 0x00002000` · `default_writer_va=0x00464D5D` · image sha `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`
  => **สิ่งที่ตารางให้แล้ว ถูกตัดออกจากคำถามใบนี้แล้ว** (พฤติกรรม/ตำแหน่ง/gate/ค่า default) เหลือเฉพาะ **ใครเป็นเจ้าของคลาสรูปธรรม**
- `external/PF_SERIALIZER_FIELDS.tsv:8-9` -- **เจอแถวชื่อ `ActorAttr` จริง แต่เป็น `EMPTY`** (`wire_empty_argument_value_copier@0x0043BB80` · span `[0x0043BB80,0x0043BB91)` · sha `b625098be0bbf3e36927c8dce2ccf3cf171563fc8f1465a41039974b332c19c0`) [วัดแล้ว chief] ⇒ สารบัญ serializer **ไม่ให้เจ้าของคลาส** ห้ามอ้างแถวนี้ว่าตอบใบนี้แล้ว
- `CLIENT_RE_QUEUE.md:3756` `RE-193` (ปิดแล้ว) ครอบ x=14,25,36,41,42,43,54 -- 🔺 **ใกล้มากแต่ไม่ใช่**: x=42 ของใบนั้นคือ `u8_9B_pairB (0x09B)` ไม่ใช่ `@0x99`/`@0x9A` [วัดแล้ว chief: `grep -n "0x099\|0x09A\|0x09B" CLIENT_RE_QUEUE.md` คืน `3756`/`3806` ซึ่งเป็น `0x09B` ทั้งคู่]

**ไม่เจอ**
- `ค้นใน pf_bridge\external\ แล้ว: ไม่เจอเจ้าของคลาส` -- `grep -rn "CNetNPC\|CMyActor" external/` = **0 hit ทั้งต้นไม้** [วัดแล้ว chief] ⇒ census คลาสรูปธรรมทำจากสะพานไม่ได้ นี่คือเหตุผลของป้าย `STATIC-ON-BRIDGE`
- `ค้น gamedata แล้ว: ไม่เจอ` -- `grep -in "ActorAttr\|UpdateAttr\|CNetNPC" gamedata/` = **0 hit** [วัดแล้ว chief]
- `grep -rn "ActorAttr@0x99\|ActorAttr@0x9A\|state_record_forced_flag\|source_state_appearance_byte"` ใน `CLIENT_RE_QUEUE.md` / `GAME_TEST_QUEUE.md` / `archive/` = **0 hit ทั้งสามที่** [วัดแล้ว chief] ⇒ ไม่เคยมีใบไหนถามสองฟิลด์นี้เลย ไม่ใช่ใบซ้ำ
- ไม่มี RTTI / string / consumer class ผูกกับสองฟิลด์นี้แม้แต่ตัวเดียวในคลัง commit -- [วัดแล้ว LANE-DB ในจดหมาย `1748` · chief ยืนยันซ้ำเฉพาะคอลัมน์ของ `PF_A2_ATTR_FIELD_DELTA.tsv` ข้างบน ไม่ได้ census เอง]

## คำถามเดียว (หนึ่งใบหนึ่งคำถาม)
**คลาสรูปธรรมใดเป็นผู้ attach และผู้บริโภคของ `ActorAttr@0x99` และ `ActorAttr@0x9A`** -- ตอบด้วย RTTI/vtable/type node + span ของ consumer จริง ไม่ใช่ด้วยชื่อฟิลด์ ไม่ใช่ด้วยการอนุมานจากคลาสฐาน `ActorAttr`

## เกณฑ์ปิดใบ (ชั้นเดียว -- static IMAGE เท่านั้น ไม่มีชั้น client-observable)
- **PASS**: ชื่อคลาสรูปธรรม + เส้นทาง attachment (RTTI/vtable/type node) + VA ของจุดบริโภคจริง + `span_sha256` ทุกช่วง + image sha + `generation_id` · ถ้ามีมากกว่าหนึ่งคลาส ให้ **แยกหนึ่งแถวต่อหนึ่งคลาส** ตามที่คอลัมน์ `scope_next_step` ของตารางสั่งไว้เอง
- **bounded negative รับเป็นคำตอบปิดใบ**: "census เดินครบแล้วยังไม่ผูกคลาสรูปธรรมได้ เพราะตันที่ VA/โครงสร้างใด" ปิดใบได้ -- และมีค่าเท่าผลบวก เพราะมันเปลี่ยนสถานะจาก "ไม่มีใครลอง" เป็น "ลองแล้วตันตรงนี้" แล้ว LANE-DB จะรู้ว่าต้องรอ capture ชนิดใดแทน
- 🔺 ทั้งสองฟิลด์ต้องตอบ **แยกกัน** (`@0x99` หนึ่งข้อ `@0x9A` หนึ่งข้อ) ห้ามตอบรวมเป็นข้อเดียว แม้จะได้คลาสเดียวกัน

## ใบนี้ไม่ขอ
ไม่ขอ **ค่า**/พฤติกรรม/ตำแหน่งของฟิลด์ (ตารางปิดไปแล้ว: `PROVEN_EXACT`/`PROVEN_ROLE_ONLY`) · ไม่ขอเรื่องเส้นทาง `0x309A`/`CNetNPC` (= `RE-259`) · ไม่ขอชั้น client-observable · **ห้ามบูตไคลเอนต์เพื่อปิดใบนี้** · ไม่ขอให้แตะโค้ด

## ห้ามสรุปสิ่งเหล่านี้ (กติกาหลักฐาน)
- 🔺 **ห้ามเดาความหมายจากชื่อฟิลด์** `state_record_forced_flag`/`source_state_appearance_byte` -- ชื่อพวกนี้เป็น role name ที่ codex ตั้ง ไม่ใช่หลักฐานว่าใครเป็นเจ้าของ (nonclaim ข้อ 4 ของจดหมายต้นทาง ยกมาทั้งข้อ)
- 🔺 ห้ามอ้าง `external/PF_SERIALIZER_FIELDS.tsv:8-9` ว่าตอบใบนี้แล้ว -- แถวนั้นเป็น `EMPTY` ให้ span ของ copier ไม่ให้เจ้าของ
- 🔺 ห้ามเหมาผลของ `RE-193` (`@0x9B`) มาใช้กับ `@0x99`/`@0x9A` -- PER-CLASS/PER-FIELD (§14 ข้อ 13 ค) ต่อให้ไบต์ติดกัน
- 🔺 ห้ามอ้างว่าใบนี้เติม `RESEND_ADJUDICATED` ได้ -- เซตนั้นยังต้องว่างหลังใบนี้ปิด (nonclaim ข้อ 1 ของต้นทาง)
- 🔺 ต้องอ่านคอลัมน์ `nonclaim`/`residual_*` ของทุกแถว Codex ที่ยกมา แล้วคัดลอกข้อความนั้นลงในผล (§14 ข้อ 13 ข) -- แถว `:8-11` มีข้อความ `structural/consumer role is proved but the broader gameplay noun or full value domain is not unique`
- G8: ทุกแถวในผลติดป้าย `[วัดแล้ว]`/`[เสนอ]` · G1/G6: ห้ามปิดด้วยการอ่านครั้งเดียวหรือแหล่งเดียว ต้องมี `span_sha256` ทุกช่วง

## แยกจากใบไหน
`RE-259` (กลุ่ม 1+2 · 9 VA · คนละระดับของคำถาม -- จดหมายต้นทางสั่งห้ามรวม) · `RE-193` (7 ฟิลด์ ปิดแล้ว ไม่มี `@0x99`/`@0x9A`) · `RE-194` (ค่าของ x=7) · `RE-241` (`CNetNPC` ในชั้น census ของมอน ไม่ใช่ owner ของ Attr field)

## ถ้าผลออกทางลบ
bounded negative ⇒ LANE-DB ยังคง **ไม่** เติม `RESEND_ADJUDICATED` และปิด piece 3 ค้างไว้ตามเดิมโดยมีเหตุผลที่ระบุ VA ได้ (แทนที่จะเป็น "ไม่มีใครเคยลอง") · ถ้าคำตอบออกมาเป็น NPC-only ⇒ ผลนี้ไปเสริม `RE-259` แต่ **ไม่แทนกัน** สองใบยังต้องปิดแยก

## ผลไปถึงใคร
จดหมายผลจ่าหน้า **LANE-DB** (cc chief, COO) · บรรทัดแรกเขียนว่า `ขอให้ LANE-DB กรอก ### result: และปิดหัวใบเอง` (§5) · ไม่ผูก deadline (`PANYA-DECISION 20260904_0233`)

### result:
(ว่าง -- รอ RE runner)

---


---

<!-- RE-265 moved verbatim by LANE-K round spppsd 2026-09-07T14:22+07:00 -->
## RE-265 WHAT-OPENS-THE-CAPTAIN-DOCK-REPORT-WINDOW-001  [**CLOSED BOUNDED-NEGATIVE / STATIC ANSWERED** 2026-09-05T19:32+07:00 โดย RE runner บนเครื่อง Panya · ปิดหัวโดย chief (LANE-E) รอบ `rz1fxh`/R358 ตาม `COO-DECISION 20260905_1949` ข้อ 1 · ผลเต็ม: `notes_to_chief/20260905_1932_RE-265-RESULT-COMMON-CONFIRM-OPENS-AFTER-SAILING-RESULT-KEY.md` · **คำตอบหนึ่งบรรทัด**: `NavigationEx_AddSurveyDataVtial` ไม่ได้เปิดหน้าเอง — module tick ของ client เป็นคนเปิด `Common_Confirm` แต่มีเกตที่ GT-233 ไม่ได้ provision: record `+0x14` ต้องเป็น key ที่ lookup ตาราง `SAILING_RESULT` แล้ว**คืนแถวจริง** row ว่าง = ออกก่อนเกตระยะ (ระยะ 37 หน่วยจึงไม่พอ) → กดยืนยัน → client ยิง `EnterInstanceVital` เอง · **ปิดเป็น BOUNDED-NEGATIVE ไม่ใช่ DONE** เพราะไม่มีชั้น client-observable — ชั้นนั้นเป็นของ `GT-233` (READY-v2 ข้างล่าง) · checkpoint = **cross-layer ceiling**: ห้าม RE runner rerun image เดิมจนกว่า chief จะเปลี่ยน objective · **เจ้าของใบ/ผู้บริโภคผล = LANE-A** · **เจ้าของใบ/ผู้เขียนเนื้อใบ/ผู้บริโภคผล = LANE-A** · เนื้อใบเต็มวางโดย chief (LANE-E) รอบ `cooif2`/R357 ตาม `notes_to_chief/20260905_1638_LANE-A-RE-265-TICKET-BODY-*.md`]

> 🔴 **ทำไมต้องมีใบนี้**: `GT-233` R318 วัดเป็นลบบนจอ (`notes_to_chief/20260905_1319_KA1A-R318-RESULTS-*.md` · `OBSERVER_CONFIRMED 2026-09-05T12:48+07:00`) -- record `NavigationEx_AddSurveyDataVtial` 73 ไบต์ผ่าน parser ของไคลเอนต์แล้ว (ไม่มี `ErrorData` ทั้งรอบ) และเรือเข้าใกล้พิกัดใน record ถึง **37 หน่วย** แต่ **หน้ารายงานกัปตันไม่เด้ง** ⇒ สมมติฐานหลักของ `RE-227` ("ไคลเอนต์เช็กระยะเองแล้วเปิดหน้าเอง") ถูกหักล้างบนจอ

**สถานะ**: OPEN · **ผู้เปิดใบและผู้บริโภคผล**: LANE-A · **ผู้ตอบ**: RE runner (ข้อ ก/ข) · ข้อ (ค) LANE-A ตอบบางส่วนแล้วบนคลาวด์

**สิ่งที่ต้องไม่ทำระหว่างรอผล** (`COO-DECISION 20260905_1348` ข้อ 2/5): ห้ามบูต `GT-233` ซ้ำ · ห้ามสร้างสวิตช์ `PF_M2_SURVEY_XYZ` หรือทาง BACKUP ใด ๆ (ปิดถาวร) · ห้ามเขียนโค้ดตามสมมติฐาน (ก) หรือ (ข) ก่อนผลออก

### คำถาม -- สามข้อ ตอบแยกกันได้
**(ก) [คำถามหลัก] ในไบนารีของไคลเอนต์ อะไรสั่งเปิด UI "รายงานกัปตัน เรือเทียบท่า"** -- ไล่จาก string table → UI id → caller → เป็น handler ของ vital ตัวไหน หรือ Lua ตัวไหน ต้องการเป็นคำตอบ: ชื่อ/VA ของจุดที่เรียกเปิดหน้าต่าง + สายเรียกย้อนกลับหนึ่งชั้นว่าใครเรียกมัน

**(ข) handler `NavigationEx_AddSurveyDataVtial` เก็บ record ไว้ที่ไหน และใครอ่านต่อ** -- เร็กคอร์ด 73 ไบต์ ×8 ของเราผ่าน parser แล้วไปนอนอยู่ที่โครงสร้างไหน มีใครอ่านมันไหม หรือเขียนแล้วไม่มีผู้อ่าน

**(ค) ตารางทริกเกอร์ของฉาก 126 -- index tag `0x0F` id 2/3/7/35/48/57/69 คืออะไร** -- **LANE-A ตอบบางส่วนแล้วในรอบ `ihjytc`**: `gamedata/scene/Bg3001/Bg3001.placements.tsv` (sha256 `571c147f...c3dc9bdb8`, ตรงกับ world_scene_registry_001.json แถว 126) มี placement/definition ของ NPC/Mob_Set เท่านั้น ไม่มีคอลัมน์ตารางทริกเกอร์ · จากเจ็ด id ที่ R318 เห็น (2,3,7,35,48,57,69) มีแค่ 2 กับ 7 ที่บังเอิญตรงกับ `template_ids` ของ placement -- 3/35/48/57/69 ไม่มีอยู่เลย ⇒ **"trigger id = placement template id" ผิด**, id ที่ยิงจริงยังเป็นคนละ namespace (ยืนยัน `RE-234` ข้อ 3 ด้วยตัวเลข) · ตารางทริกเกอร์จริงต้องมาจากไฟล์ตระกูลอื่นของ `Bg3001` ที่ยังไม่ถูกสกัดเข้ารีโป -- ที่เหลือยังเป็นของ RE runner

### เกณฑ์ปิดใบ (สองชั้นตามกติกาบ้าน)
- ชั้น STATIC: ตอบ (ก) ด้วย VA/ชื่อฟังก์ชันพร้อม provenance (ไฟล์ + span_sha256) ไม่ใช่คำบรรยาย
- ชั้น client-observable: ใบ GT ที่ออกตามผล (chief ตั้งเลขทีหลัง) ทำให้หน้ารายงานกัปตันเด้งบนจอได้จริงหนึ่งครั้ง
- ปิดโดยไม่มีชั้นที่สอง = `BOUNDED-NEGATIVE` เท่านั้น ห้ามเขียน DONE

### สองสมมติฐานที่ถือเท่ากันจนกว่าใบนี้จะตอบ (`1348` ข้อ 5)
- (ก) เซิร์ฟเวอร์เดิมตอบ `0x1FB2` ด้วยเฟรมสั่งเปิดหน้ารายงาน (opcode ยังไม่รู้) -- `RE-234` พิสูจน์แค่ว่า *response ของ `TriggerVital` เอง* เป็น success no-op ห้าไบต์ ไม่ได้ปิดความเป็นไปได้ของเฟรมชนิดอื่น
- (ข) `AddSurveyData` ไม่ใช่ตัวเปิดหน้านี้เลย

### result:
**CLOSED BOUNDED-NEGATIVE 2026-09-05T19:32+07:00** -- `notes_to_chief/20260905_1932_RE-265-RESULT-COMMON-CONFIRM-OPENS-AFTER-SAILING-RESULT-KEY.md`

- (ก) ตอบแล้ว: ตัวเปิดคือ local module tick `NavigationExModule_Client` `[0x007321C0,0x00732586)` → opener `0x005AB5F0` สร้าง dialog `Common_Confirm` · callback `[0x00730FE0,0x00731083)` ต้องการ `+0x94==1` แล้วคัด record `+0x12` ลง `NavigationEx_EnterInstanceVital+0x14` — **client ยิงเอง เซิร์ฟเวอร์ห้ามส่งให้**
- (ข) ตอบแล้ว: dispatcher `0x00732590` insert ลง primary map `module+0x1C` (key = record u16 `+0x12`) → promoter `0x00731410` คัดลง secondary map `module+0x3C` → tick อ่านต่อ (`record+0x10==1`) · record มีผู้อ่านสองชั้น ไม่ใช่ "เขียนแล้วไม่มีคนอ่าน"
- (ค) **BOUNDED NEGATIVE**: `Bg3001.placements.tsv` 38 แถว ไม่มีคอลัมน์ trigger · ไม่มี scene-126 trigger crosswalk ในคลังปัจจุบัน · **ห้าม join ด้วยเลขเท่ากัน**
- **BUILD_IMPACT (LANE-A บริโภค)**: ห้าม retry เฟรมเดิมที่ใส่เพียง `record+0x12=2/3` · ต้อง derive/provision **valid SAILING_RESULT key** ที่ `record+0x14` และรักษา promoter conditions · **ห้ามเลือก row จากเลขที่เท่ากัน** (nonclaim 2 ของผล)
- **คำท้วงเชิงกระบวนการที่ chief รับ**: ใบนี้ไม่มีหัวข้อ "ค้นแล้วก่อนเปิดใบ" ตาม `AGENTS.md:98` — รอบนี้ RE runner รับไว้เพราะ `COO 1845` รับแล้ว · **ใบที่ chief วางต่อจากนี้ทุกใบต้องมีช่องนี้** (`COO 1949` ข้อ 1 · `RE-266` ข้างล่างมีแล้ว)

> 🔴 **ห้ามสายอื่นใช้เลข `RE-265`** · เนื้อใบเต็มเขียนโดย LANE-A รอบ `ihjytc` (`notes_to_chief/20260905_1638_LANE-A-RE-265-TICKET-BODY-*.md`)
> 🔴 **ห้ามบูต `GT-233` ซ้ำจนกว่าใบนี้จะตอบ** (`COO-DECISION 20260905_1348` ข้อ 1-2 · ทาง BACKUP ปิดถาวร)

- numbering: `RE-265`/`GT-265` = **0 hit ทั้งสามที่** (`GAME_TEST_QUEUE.md` · `CLIENT_RE_QUEUE.md` · `archive/*QUEUE*ARCHIVE*`) ก่อนจอง **[วัดแล้ว รอบก่อน]** · ตัวนับร่วมสองคิว + archive คืนสูงสุดที่ `264` (`GT-264` วางในรอบเดียวกัน) ⇒ ใบนี้ `265`

---

---

<!-- RE-266 moved verbatim by LANE-K round spppsd 2026-09-07T14:22+07:00 -->
## RE-266 0X709E-DOWNSTREAM-AND-GETWORLDINFO-REPLY-WAIT-001  [🔧 **BOUNDED-NEGATIVE / STATIC ANSWERED — พับโดย LANE-K รอบ `ek1gk9` 2026-09-07T09:5x+07:00** คำต่อคำจากบรรทัดสถานะของจดหมายผล `notes_to_chief/20260905_2242_RE-266-RESULT-NO-DIRECT-SELECT-UI-NO-GETWORLD-REPLY-FLAG.md` (RE runner บนเครื่อง Panya 2026-09-05T22:42+07:00): “สถานะ: BOUNDED-NEGATIVE / STATIC ANSWERED (ไม่เขียน DONE เพราะไม่มี client-observable ตามเกณฑ์ใบ)” · 🔴 ผู้เทสเขียนเองว่า **ไม่ใช่ DONE** — ห้ามอ่านเป็น PASS · K คัดลอกคำของผู้เทส ไม่ได้ตัดสินเอง · 🟠 บันทึกเดิมก่อนพับ (ไม่ลบ ขีดฆ่าไว้ตามธรรมเนียมบ้าน = ถอนแล้วโดยเจตนา ไม่ใช่สถานะสด): ~~🔴 **OPEN**~~ · **เจ้าของใบ/ผู้เขียนเนื้อใบ/ผู้บริโภคผล = LANE-UI** · ตั้งเลขโดย chief (LANE-E) รอบ `rz1fxh`/R358 ตาม `COO-DECISION 20260905_1845` ข้อ 4 · เนื้อใบเต็มเขียนโดย LANE-UI รอบ `4j99rh` (`notes_to_chief/20260905_1405_LANE-UI-RE-TICKET-0x709E-handler-gate-already-answered-by-re075-real-gap-is-getworldinfo-wait.md`) · ป้ายชั้น: **ข้อ 1 = `[STATIC-ON-BRIDGE]`** (artifact ที่ commit แล้ว) · **ข้อ 2 = `[STATIC-ON-BRIDGE]` และมีแนวโน้มสูงที่จะจบด้วย `[NEEDS-CLIENT-IMAGE]`** · **ตัวบล็อกของ `GT-184`/`GT-186`** (ทั้งสองใบพลิกเป็น `BLOCKED-ON-RE-266` รอบเดียวกัน)]

**ทำไมต้องมีใบนี้**: `COO-DECISION 20260905_1352` ข้อ 3 สั่งใบ RE แคบใบเดียวสองคำถาม หลัง R311+R319 วัดเป็นลบบนจอ (HYP-PF-040 FALSIFIED) · LANE-UI ค้นก่อนแล้วพบว่าคำถาม (ก) ของ `1352` **ถูกตอบไปแล้วโดย `RE-075`** ใบนี้จึงเหลือเฉพาะปลายที่ `RE-075` ไม่ได้เดิน กับคำถาม (ข) ที่ยังไม่มีใครตอบเลย

## ค้นแล้วก่อนเปิดใบ (`AGENTS.md` §98 · `RE_STATIC_SEARCH_RULES.md`)
**เจอ** -- `RE-075` (DONE/PASS 2026-08-26, `archive/notes_to_chief_2026-08-19_to_26/20260825_2318_RE-075-RESULT-FALSE-BRANCH-NOOP-ZERO-FIELD-GATE.md`) ปิดเกตสองชั้นของ `0x709E` ครบ: ชั้น 1 `apply 0x005F1190` อ่าน live-state `[0x1093198]+0x34C` เช็ก `cStateCreateActor` ไม่ตรง = `mov al,1; ret 4` ทันที · ชั้น 2 `0x004B2A50` ต้องการ `vital+0x14 == 0x1E` · `RE-196`/`RE-197`/`RE-189` CLOSED · `VITAL_REGISTRY...tsv:191`, `external/PF_PROTOCOL_REGISTRY.tsv:73`, `PF_SERIALIZER_FIELDS.tsv:1123-1128`, `PF_FIELD_VALIDATION.tsv:144-145` · `PF_TAG_CENSUS.tsv` = 0 hit
**ไม่เจอ** -- ไม่มีรายงาน static ใดเดิน downstream ของ true-branch (`0x4B04A0`/`0x5DD890` ที่ `RE-075` T3 ทิ้งค้าง) · ไม่มีใบใดปิดคำถาม (ข) ของ `1352` · `serializer_status` ของ `0x3D4B` ใน `PF_PROTOCOL_PRIORITY.tsv:67` = **OPEN**

## คำถาม -- สองข้อ เรียงลำดับบังคับ
1. **downstream ของเกตที่ `RE-075` เปิดค้างไว้** -- ตาม call ไป `0x4B04A0`/`0x5DD890` (true-branch ของเกตทั้งสองชั้น): เขียน/เรียกอะไรที่แตะ UI/state transition จริงหรือไม่ — เป้าหมายคือรู้ว่า **ถ้าส่ง `0x709E` ที่ state ถูก + `+0x14=0x1E` จริง** จะพาไปหน้าเลือกตัวละครได้หรือไม่ในทางทฤษฎี ก่อนจะจ่ายเวลา attended รอบใหม่
2. **`0x3D4B` (`GetWorldInfoVital`) ฝั่ง R** -- ไล่ `CALL_UNCLASSIFIED:0x005DFD00` และ `0x00708E20` เท่าที่ artifact ที่ commit แล้วพาไปได้: มี pending-reply flag/state ที่ gate การเปิด dialog ต่อไปหรือไม่ · **ไล่ต่อไม่ได้เพราะต้องใช้ disassembly ที่ไม่ได้ commit ⇒ แปะป้าย `[NEEDS-CLIENT-IMAGE]` ตรงจุดนั้น ห้ามเดา**
3. ใบนี้ **ไม่ขอให้ตอบคำถาม (ก) ของ `1352` ซ้ำ** — `RE-075` ตอบครบทั้งสองเกตแล้ว

## เกณฑ์ปิดใบ (ชั้น static เท่านั้น)
- ข้อ 1 ปิดได้เมื่อ: ไล่ downstream สำเร็จพร้อม provenance (`path:บรรทัด`/VA + `span_sha256`) **หรือ** สรุปว่าต้องมีไบนารีไคลเอนต์ถึงไล่ต่อได้ (`[NEEDS-CLIENT-IMAGE]`) -- ทั้งสองแบบถือว่าปิด
- ข้อ 2 ปิดได้แบบเดียวกัน · **ผลลบ/ผลไม่คืบก็เป็นผลที่ใช้ได้** (`RE-189` ธงไว้แล้วว่ามีแนวโน้มจบด้วย "ต้อง attended")
- ปิดโดยไม่มีชั้น client-observable = `BOUNDED-NEGATIVE` เท่านั้น ห้ามเขียน DONE
- 🔴 **ชั้น client-observable ไม่อยู่ในใบนี้** — ถ้าผลชี้ว่าต้อง attended ถึงจะปิดคำถาม (ข) ได้ **LANE-UI ต้องเปิดใบ GT คู่ในรอบเดียวกันที่บริโภคผล** (`AGENTS.md` §7 · `COO-DECISION 20260904_2142` ข้อ 3 · ขอเลขจาก chief)

## ใบนี้ไม่ขอ
ไม่ขอให้เดาว่า `0x709E` เป็น vital ที่ถูกสำหรับปุ่มนี้หรือไม่ (`RE-075` nonclaim 4) · ไม่ขอให้บูตซ้ำ (`1352` ข้อ 2) · ไม่ขอให้ลองลำดับ "ส่งหลัง ACK" (เป็นการเดาลำดับ ไม่ใช่ผลวัด)

### result:
(ว่าง)

> 🔴 **ห้ามสายอื่นใช้เลข `RE-266`** · numbering: `RE-266` = 0 hit ทั้งสามที่ (`CLIENT_RE_QUEUE.md` · `GAME_TEST_QUEUE.md` · `archive/*QUEUE*ARCHIVE*`) ก่อนตั้ง **[วัดแล้ว รอบ `rz1fxh`/R358]** · ใบนี้มีหัวข้อ "ค้นแล้วก่อนเปิดใบ" ตาม `AGENTS.md` §98 ตามที่ RE runner ท้วงใน `1932`

<!-- RE-278 moved verbatim by LANE-K round spppsd 2026-09-07T14:22+07:00 -->
## RE-278 LV-LIVE-UPDATE-FRAME-001  [🔧 **DONE (static) / POSITIVE + BOUNDED-NEGATIVE — พับโดย LANE-K รอบ `73i74a` 2026-09-07T10:09+07:00** คำต่อคำจากหัวจดหมายผล `notes_to_chief/20260906_2313_RE-278-RESULT-LEVEL-ONLY-TRAVELS-IN-BASICATTR-MASK-BIT-0x0002-RESEND-THE-WHOLE-MASK.md` (RE runner บนเครื่อง Panya 2026-09-06T23:13+07:00): "**สถานะ: DONE (static) / POSITIVE + BOUNDED-NEGATIVE · ชั้น client-observable เป็นของ `GT-200`/ใบเทสของสาย GM ไม่ใช่ใบนี้**" · K คัดลอกคำของผู้เทส **ไม่ได้ตัดสินเอง** และไม่ได้แตะเนื้อใบ · 🟠 บันทึกเดิมก่อนพับ (ไม่ลบ ขีดฆ่าไว้ตามธรรมเนียมบ้าน = ถอนแล้วโดยเจตนา ไม่ใช่สถานะสด): ~~🔴 **OPEN**~~ · **เจ้าของใบ/ผู้เขียนเนื้อใบ/ผู้บริโภคผล = LANE-GM** · ตั้งเลขโดย LANE-K รอบ `n3s0rg` 2026-09-06T14:10+07:00 ตาม `COO-DECISION 20260906_1346` ข้อ 3(ก) · เนื้อใบมาจากจดหมาย `notes_to_chief/20260906_0434_LANE-GM-TO-CHIEF-slash-lv-lands-gt-body-and-re-question.md` ข้อ 2 คำต่อคำ]

**คำถาม**: เฟรม server->client เฟรมไหนที่ทำให้ไคลเอนต์ v141 อัปเดต **เลเวลของตัวผู้เล่นเอง** ระหว่าง session โดยไม่ต้อง relog — และถ้าเป็น `UpdateAttrVital` (`0x309A`) จริง ต้องส่งกี่ฟิลด์ (mask ไหนบ้าง) ถึงจะไม่ตกอยู่ในรูปแบบ sparse ที่ `GT-193`/`GT-218` วัดว่าฆ่าไคลเอนต์

**grep แล้ว: เจอ/ไม่เจอ** (คำต่อคำจาก LANE-GM)
- เจอ: `attr_wire.py:424` แถว x=2 `basic 0x0002 @+0x5E tag 0x12 u16 level GetLv` (`RE-117`) — layout ของ *ฟิลด์* มีแล้ว
- เจอ: `RE-222` Q0 ยืนยัน apply เป็น full-object copy ⇒ bit ที่ไม่เซ็ต = 0 บนไคลเอนต์
- **ไม่เจอ**: เฟรมอื่นใดที่พาเลเวลอย่างเดียว · ไม่เจอใน `VITAL_REGISTRY_*.tsv` และ `external/PF_SERIALIZER_FIELDS.tsv` ว่ามี vital ที่ตั้งเลเวลตัวเดียวได้
- `GT-200` (ไคลเอนต์วาดเลเวลจากฟิลด์นี้จริงไหม) ยังไม่มีผล — ถ้า RE นี้ตอบก่อน ใบนั้นถูกกลืน

**ทำไมสายนี้ไม่เดาเอง**: `/warp <x> <y>` ปิดไคลเอนต์มาแล้ว (`1744`) และ sparse `0x309A` ฆ่าตัวละครใน 1 เฟรม (`GT-193`) · รอบนี้จึงส่งแค่ประโยคแชท ไม่ส่งบล็อกแอตทริบิวต์เลย

**links**: `RE-117` (layout ฟิลด์ level) · `RE-222` (full-object copy apply) · `GT-193`/`GT-218` (sparse `0x309A` ฆ่าไคลเอนต์) · `GT-200` (ค้าง, คำถามเดียวกันว่าไคลเอนต์วาดจากฟิลด์นี้จริงไหม) · `GT-277` (`/lv` เขียนแถวได้แล้ว, ใบนี้ต่อยอดถามเรื่อง live-update ไม่ต้อง relog)

### result:
**DONE (static) / POSITIVE + BOUNDED-NEGATIVE** -- พับโดย LANE-K รอบ `73i74a` 2026-09-07T10:09+07:00 · คัดลอกจาก `notes_to_chief/20260906_2313_RE-278-RESULT-LEVEL-ONLY-TRAVELS-IN-BASICATTR-MASK-BIT-0x0002-RESEND-THE-WHOLE-MASK.md` คำต่อคำ

> **สถานะ: DONE (static) / POSITIVE + BOUNDED-NEGATIVE · ชั้น client-observable เป็นของ `GT-200`/ใบเทสของสาย GM ไม่ใช่ใบนี้**
>
> **คำตอบสองบรรทัด**
> 1. ไม่มีเฟรมไหนพา "เลเวลอย่างเดียว" — ฟิลด์เลเวลอยู่ที่ `BasicAttr+0x5E` (u16, tag `0x12`) และถูกส่ง **ก็ต่อเมื่อ**บิต `0x0002` ของ mask u16 ที่ `+0x70` ถูกเซ็ต · โคเดกของคลาสนี้มี **ตัวเดียวทั้งอิมเมจ** (`0x004656F0`, ถูกอ้างที่เดียวคือสล็อต vtable `0x00F0E794`) ⇒ ทุกเฟรมที่พา `BasicAttr` ใช้ทางเดียวกันหมด
> 2. เหตุที่ sparse ฆ่าไคลเอนต์: **ตัวอ่านไม่ได้ zero-fill** — มันข้ามฟิลด์ที่บิตไม่เซ็ตไปเฉย ๆ · ศูนย์มาจาก "อ็อบเจกต์ถูกสร้างใหม่ (ทุกไบต์ 0) ก่อนอ่าน" + apply เป็น full-object copy (`RE-222` Q0) ⇒ **บิตไหนไม่ส่ง = ฟิลด์นั้นกลายเป็น 0 บนไคลเอนต์** ⇒ ต้องส่ง mask ชุดเดียวกับตอนล็อกอิน ค่าปัจจุบันครบทุกช่อง เปลี่ยนแค่ `+0x5E`

🟡 **ชั้นที่ขาด (K ไม่ปั๊มให้ครบ)**: จดหมายเขียนเองว่าชั้น **client-observable ยังไม่วัด** และเป็นของ `GT-200`/ใบเทสของสาย GM ⇒ ใบนี้ปิดในฐานะใบ static เท่านั้น

> 🔴 **ห้ามสายอื่นใช้เลข `RE-278`** · numbering: ตัวนับร่วมสองคิว + `archive/*QUEUE*ARCHIVE*` คืน **277** (`GT-277`, วางพร้อมกันรอบเดียว) ⇒ ใบนี้ **278** · ตรวจ 0 hit ของ `GT-278`/`RE-278` ทั้งสามที่ (`GAME_TEST_QUEUE.md` · `CLIENT_RE_QUEUE.md` · `archive/`) ก่อนวาง [ตรวจโดย LANE-K รอบ `n3s0rg`]

<!-- RE-282 moved verbatim by LANE-K round spppsd 2026-09-07T14:22+07:00 -->
## RE-282 CHARCREATE-CLASS-S-SCORE-STARTING-STATS-SEMANTICS-001  [**CLOSED DONE/BOUNDED-NEGATIVE** 2026-09-06T23:22+07:00 โดย RE runner บนเครื่อง Panya -- `POTENTIAL` มี 0 แถวจริงในไฟล์ที่ไคลเอนต์ shipped มาเอง (คลาย `.pc_` ใหม่ยืนยัน ไม่ใช่บั๊กตัวแตกไฟล์เดิม) + สำมะโนครบทั้ง 120 ตาราง CONSTDATA: ไม่มีตารางสแตทเริ่มต้นต่อคลาสเลยสักตาราง ⇒ `DEFAULT_PRIMARY_STAT = 100` คงเดิม · เส้นทาง `s_SCORE` **ไม่รันซ้ำ** (ชน method ceiling ของ `RE-229` แล้ว ตามคำห้าม rerun ของใบนั้นเอง) -- ผลเต็ม: `notes_to_chief/20260906_2322_RE-282-RESULT-POTENTIAL-IS-EMPTY-IN-THE-SHIPPED-CLIENT-NO-PER-CLASS-STAT-TABLE.md` -- พับโดย LANE-K รอบ `hf1gs9` · **เจ้าของใบ/ผู้เขียนเนื้อใบ/ผู้บริโภคผล = LANE-DB** · ตั้งเลขโดย LANE-K รอบ `zqq4qz` 2026-09-06T16:09+07:00 (คำขอค้างจากรอบ `rsmsia`/`n3s0rg` — จดหมายเดิมส่งถึง chief ไม่ใช่ K โดยตรง แต่รูปแบบไฟล์ตรง `*RE-TICKET*` ตามนิยามคำขอเลขใบของ `prompts/LANE-K.md`) · เนื้อใบมาจากจดหมาย `notes_to_chief/20260904_0542_LANE-DB-RE-TICKET-piece-2-starting-stats-has-no-committed-source-table.md` คำต่อคำ · อ้าง: `COO-ORDER 20260904_0329` ข้อ 2 · `PANYA-DECISION 20260904_0328` ข้อ 1]

**หัวเรื่อง**: piece 2 ("ค่าเกิดจาก CHARCREATE_CLASS/STANDARD_STATUS แทน DEFAULT 100") ไม่มีตารางที่ commit แล้วให้ค่าได้จริง

### วัดมาแล้ว ไม่ใช่สมมติฐาน
พยายามเริ่มชิ้น 2/5 ก่อนชิ้น 5/5 แล้วพบว่าสองตารางที่ `PANYA-DECISION 20260904_0328`
ระบุชื่อไว้ไม่มีคอลัมน์ STR/CON/DEX/INT/PER/HP/MP เริ่มต้นต่อคลาสเลย:

1. `gamedata/tables/CONSTDATA_TH__STANDARD_STATUS.tsv` — 255 แถว, คอลัมน์คือ
   `n_ID` (เลเวล), `n_EXP_CURRENTLV`, `n_POINT_ABILITY`, `n_DEADLOSS`, `n_PVP_EXP`,
   `n_PVP_SP`, `n_PVP_MONEY`, `n_DEFENCE_CONSTANT` — เป็นตาราง EXP/แต้มความสามารถ
   **ต่อเลเวล** ไม่ใช่สแตทเริ่มต้นต่อคลาส `n_POINT_ABILITY` คือแต้มที่ได้ตอนเลเวลอัพ
   (0 ที่เลเวล 1) ไม่ใช่ค่า STR/CON/DEX/INT/PER ที่มีอยู่แล้ว
2. `gamedata/tables/CONSTDATA_TH__CHARCREATE_CLASS.tsv` คอลัมน์ `s_SCORE` (6 ตัวเลขคั่น `;`
   ต่อแถว เช่น Gladiator `4;3;4;1;1;2`) เป็นตัวเลือกเดียวที่ดูเหมือนสแทท แต่ **ไม่เคยถูก RE
   เลยในโปรเจกต์นี้** — `LANE-CS` (`class_catalog.py` ที่ commit แล้วบน main) เขียนไว้ตรง ๆ ใน
   docstring ของตัวเองว่า "s_SCORE's semantics have never been RE'd" และอ้าง
   `reports/PF_JOB001_CHARCREATE_CLASS_STATIC_BOUNDARY_20260816.md` ที่นับ s_SCORE รวมอยู่ใน
   "37 other columns" โดยไม่ถอดรหัสสักตัว
3. `gamedata/tables/CONSTDATA_TH__POTENTIAL.tsv` — ตารางเดียวที่
   `docs/FUNCTIONAL_COVERAGE.json` เรียกว่าผู้สมัครจริงสำหรับ ability stat — **มีแต่ header
   ไม่มีแถวข้อมูลเลยใน snapshot นี้**

### ผลคือ
ไม่มีแหล่งค่าที่ commit แล้วให้ resolve HP_max/MP_max/STR/CON/DEX/INT/PER เริ่มต้นต่อคลาสได้
โดยไม่เดา (`COO-DECISION 20260901_1059` ห้ามส่งค่าเดา)

### ขอ RE
s_SCORE หกตัวเลขคืออะไร (ลำดับ STR/CON/DEX/INT/PER + ตัวที่หก?) หรือ POTENTIAL.tsv มีแถวจริงใน
ไบนารีไคลเอนต์ที่ยังไม่ถูกดึงเข้า `gamedata/tables/` หรือไม่ — สองเส้นทางไหนก็ได้ที่ยืนยันได้ ไม่ใช่
สมมติฐานสาย DB เอง (ขอบเขตของสายนี้ไม่ครอบ static RE)

### result:
**DONE / BOUNDED-NEGATIVE** (`notes_to_chief/20260906_2322_RE-282-RESULT-POTENTIAL-IS-EMPTY-IN-THE-SHIPPED-CLIENT-NO-PER-CLASS-STAT-TABLE.md`, RE runner บนเครื่อง Panya, 2026-09-06T23:22+07:00):
1. `POTENTIAL` (11 คอลัมน์ ห้าแกนสแตท) มี **0 แถวในไฟล์ `B_CONSTDATA_TH.pc_` ต้นฉบับของไคลเอนต์เอง** — คลาย
   `.pc_`/LZMA ใหม่เอง (sha256 ตรงกับสำเนา commit แล้ว) พาร์สเฮดเดอร์ตารางที่ `0x00312F06` ได้ `ROWS=0`
   และตารางถัดไป (`STANDARD_BUFF`) เริ่มพอดีที่ปลายเฮดเดอร์ ⇒ ไม่ใช่ตัวพาร์สเดินหลง ไม่ใช่บั๊กแตกไฟล์เดิม
2. สำมะโนครบทั้ง 120 ตารางใน CONSTDATA: มีแค่ 3 ตารางที่ถือคอลัมน์ห้าแกน/HP-MP (`POTENTIAL` 0 แถว ·
   `STANDARD_BUFF` 256 แถว · `STANDARD_MOB` 255 แถว) และ**ไม่มีตารางใดมีมิติ "ต่อคลาส"** ⇒ ไคลเอนต์ไม่ได้
   ship ค่าสแตทเริ่มต้นต่อคลาสมาเลย
- **BUILD_IMPACT**: `DEFAULT_PRIMARY_STAT = 100` คงเดิม — ทางตันฝั่ง static แล้ว ถ้าจะเดินต่อต้องเป็นการ
  ตัดสินใจเชิงออกแบบ (เจ้าของเคาะค่า) หรือหลักฐานชนิดใหม่ (attended/คลิป) ไม่ใช่ใบ RE เพิ่ม
- เส้นทาง `s_SCORE` ของใบนี้ **ไม่ถูกรัน** — `RE-229` ปิดคำถามเดียวกันไปแล้วเป็น method ceiling พร้อมคำห้าม
  rerun ตรงๆ จนกว่า chief จะเปลี่ยน objective
- nonclaims เต็มอยู่ในจดหมายผล (ไม่อ้างค่าที่เซิร์ฟเวอร์เดิมใช้ · ไม่อ้างว่า `STANDARD_MOB` ใช้กับผู้เล่นไม่ได้
  · ไม่อ้างไฟล์ภาษาอื่น · ขอบเขตเฉพาะ `B_CONSTDATA_TH.pc_`)

> 🔴 **ห้ามสายอื่นใช้เลข `RE-282`** · numbering: ตัวนับร่วมสองคิว + `archive/*QUEUE*ARCHIVE*` คืน **281** (`GT-281`, ตั้งเลขรอบเดียวกัน `zqq4qz`) ⇒ ใบนี้ **282** · ตรวจ 0 hit ของ `GT-282`/`RE-282` ทั้งสามที่ก่อนวาง [ตรวจโดย LANE-K รอบ `zqq4qz`]

<!-- RE-285 moved verbatim by LANE-K round spppsd 2026-09-07T14:22+07:00 -->
## RE-285 TRIGGER-GETCONTACTMODE-ARGUMENT-SEMANTICS-001  [🔧 **CLOSED / BOUNDED-NEGATIVE — พับโดย LANE-K รอบ `ek1gk9` 2026-09-07T09:5x+07:00** คำต่อคำจากบรรทัดสถานะของจดหมายผล `notes_to_chief/20260906_2303_RE-285-RESULT-TRIGGER-NAMESPACE-DOES-NOT-EXIST-IN-THE-CLIENT-AT-ALL.md` (2026-09-06T23:03+07:00): “สถานะ: CLOSED / BOUNDED-NEGATIVE ทั้งสองเส้นทาง (static-on-bridge + client-image) · checkpoint = method ceiling — ห้าม rerun อิมเมจเดิมกับคำถามนี้” · 🔴 **ห้าม rerun อิมเมจเดิมกับคำถามนี้** (คำของผู้เทส) · K คัดลอก ไม่ได้ตัดสินเอง · 🟠 บันทึกเดิมก่อนพับ (ไม่ลบ ขีดฆ่าไว้ตามธรรมเนียมบ้าน = ถอนแล้วโดยเจตนา ไม่ใช่สถานะสด): ~~🔴 **OPEN**~~ · 🔺 `[STATIC-ON-BRIDGE]` เป็นเส้นทางแรก และ `[NEEDS-CLIENT-IMAGE]` เป็นเส้นทางที่สอง (สองเส้นทาง หนึ่งใบ เหมือนรูปแบบ `RE-273`) · **เจ้าของใบ/ผู้เขียนเนื้อใบ/ผู้บริโภคผล = LANE-Q** · ตั้งเลขโดย LANE-K รอบ `zqq4qz` 2026-09-06T16:09+07:00 · เนื้อใบมาจากจดหมาย `notes_to_chief/20260906_0435_LANE-Q-RE-TICKET-DRAFT-getcontactmode-trigger22-semantics-unknown.md` คำต่อคำ (จดหมายจ่าหน้าถึง LANE-E/chief แต่รูปแบบไฟล์ตรง `*RE-TICKET*` ตามนิยามคำขอเลขใบของ `prompts/LANE-K.md`)]

**หัวเรื่อง**: `Trigger.GetContactMode` semantics unknown -- last of `lua_api/trigger.py`'s twelve stubbed names with no cross-lane dependency once its return value is known

### Why this ticket
`Trigger.GetContactMode` is the last of `lua_api/trigger.py`'s twelve still-stubbed names that is not
already blocked on another lane's wire frame or on Quest state. It has exactly one call site in the
real 616-file corpus and no cross-lane dependency once its return value is known -- a pure per-trigger
read, same shape as the `TriggerStatusRegistry` methods already real. The one thing missing is what the
number it returns MEANS.

### Search already done (all four required sources, before drafting)
- `gamedata/tables/`: `grep -rli "contact.*mode\|contactmode"` -- **0 hits**.
- `external/`: same grep -- **0 hits**.
- `archive/`: same grep -- 2 hits, both `20260824_0055_LUA-NPC-EXTRACTED-616OK-289OK.md` (a corpus
  extraction status note, matches on an unrelated word inside it, not on contact-mode semantics --
  read in full, no relevant content).
- `notes_to_chief/consumed/`: same grep -- **0 hits**.
- The one call site, read in full (`gamedata/lua/t_popmo_ui1.lua`):
  ```
  if(Player.GetItemNum(Trigger.Var3) < Trigger.Var4)then
      if(Trigger.GetContactMode(22) == 1)then
          Player.ShowMessage(859)
      end
      return 0
  else
      ...
  end
  ```
  The `22` is a literal argument, not `Trigger.VarN` -- unlike every other `Trigger.*` call in the
  corpus, which all read the trigger's OWN `Var1..Var20` fields. This suggests `22` may address a
  DIFFERENT trigger's contact state (cross-trigger read), not the calling trigger's own -- a shape
  `lua_api/trigger.py`'s current registry (keyed by `(scene, own trigger_id)` only) does not yet
  support and would need to, if confirmed.

### Two paths, one ticket (same shape as `RE-273`)
1. **`[STATIC-ON-BRIDGE]` first**: `pf-static-re` on the committed `PF_LUA_API_SPEC.md`/
   `PF_GAMEDATA_LUA_API.tsv` provenance columns (`binding_status`/`delegate_va`/`registration_va`) for
   `Trigger.GetContactMode` -- does the client-side native implementation of this API name resolve to
   a VA already disassembled under `external/`? Not found by this round's grep (those TSVs are the
   bridge repository's business, not vendored into the server clone this session has).
2. **`[NEEDS-CLIENT-IMAGE]` if (1) comes up empty**: RE runner reads whatever native code backs
   `Trigger.GetContactMode` in the client binary for what "contact mode" enumerates and whether the
   argument addresses the calling trigger or an arbitrary one by id.

### `ATTENDED:` (stub only -- NOT ready to queue, names its own missing prerequisite per nonclaim 3)
- Stand at the placement that runs `t_popmo_ui1.lua` (scene/placement TBD -- this ticket's own path 1/2
  must resolve the id-to-file mapping first via the OTHER open ticket, `RE-273`; this block is a stub
  until that lands, named here so the ticket is not silently missing it).
- Trigger the script with fewer than `Trigger.Var4` of item `Trigger.Var3` in inventory.
- Read whether message 859 appears, and whether trigger id 22 in the same scene shows any
  observable state change beforehand that would explain a "contact mode" of 1 vs. not-1.
- Pass: message 859's appearance correlates with trigger 22's own observable state. Fail (still
  informative): no observable correlate exists in this capture, narrowing to pure binary RE.

### nonclaims
1. Does not claim the literal `22` is definitely a cross-trigger reference -- only that it is the one
   observable fact this round's read of the single call site found, and that it does not match every
   other `Trigger.*` call in the corpus (which all read `Trigger.VarN`).
2. Does not claim this is high priority -- one call site, one file, versus `Quest.*`'s 25 names across
   221-366 files each.
3. Does not claim the ATTENDED block above is ready to queue -- it names its own missing prerequisite
   (the id-to-file mapping ticket, `RE-273`) rather than guessing a scene/placement.

**links**: `RE-273` (trigger-id-to-lua-file mapping, this ticket's own prerequisite) · `lua_api/trigger.py` `STILL_STUBBED` dict

### result:
(ว่าง)

> 🔴 **ห้ามสายอื่นใช้เลข `RE-285`** · numbering: ตัวนับร่วมสองคิว + `archive/*QUEUE*ARCHIVE*` คืน **284** (`GT-284`, ตั้งเลขรอบเดียวกัน `zqq4qz`) ⇒ ใบนี้ **285** · ตรวจ 0 hit ของ `GT-285`/`RE-285` ทั้งสามที่ก่อนวาง [ตรวจโดย LANE-K รอบ `zqq4qz`]

---

<!-- ย้ายทั้งก้อนโดย LANE-K รอบ `dccuar` 2026-09-07T15:24+07:00 · คำต่อคำ ไม่ตัดไม่ย่อ -->

## RE-280 ITEMOPERATEVITALRES-EQUIP-WORN-FLAG-AND-W9-CROSSCHECK-001  [🔧 **DONE (ask 1 + ask 2 + ask 3) — พับโดย LANE-K รอบ `73i74a` 2026-09-07T10:09+07:00** คำต่อคำจากหัวจดหมายผล `notes_to_chief/20260906_2258_RE-280-RESULT-0x39-IS-A-SHIFT-BIT-INDEX-FF-MEANS-NOT-EQUIPPED.md` (RE runner บนเครื่อง Panya 2026-09-06T22:58+07:00): "**สถานะ: DONE (ask 1 + ask 2 + ask 3) / static ล้วน · ชั้น client-observable ยังเป็นของบล็อก ATTENDED ในใบเอง**" · K คัดลอกคำของผู้เทส **ไม่ได้ตัดสินเอง** และไม่ได้แตะเนื้อใบ · 🟠 บันทึกเดิมก่อนพับ (ไม่ลบ ขีดฆ่าไว้ตามธรรมเนียมบ้าน = ถอนแล้วโดยเจตนา ไม่ใช่สถานะสด): ~~🔴 **OPEN**~~ · 🔥 **PANYA-ORDER `20260906_0156` เส้นตาย 23:00 — บล็อกแขน (ข)** · **เจ้าของใบ/ผู้เขียนเนื้อใบ/ผู้บริโภคผล = LANE-DB** · ตั้งเลขโดย LANE-K รอบ `zqq4qz` 2026-09-06T16:09+07:00 ตาม `COO-DECISION 20260906_1547` ข้อ 4(1) ("ตั้งเลข RE ของ DB `1449` ก่อนใบอื่นทั้งหมด") · เนื้อใบมาจากจดหมาย `notes_to_chief/20260906_1449_LANE-DB-RE-TICKET-itemoperatevitalres-equip-worn-flag-and-w9-crosscheck.md` คำต่อคำ · จากสาย: LANE-DB รอบ `xqi5p4` ต่อจาก `rounds/DB_20260906_1316_rjqssc_...md` §7]

**หัวเรื่อง**: ItemOperateVitalRes (0x4C13) สำหรับ "สวมอาวุธ" (op=5): field `ItemAttr@+0x39` worn-flag ความหมายคืออะไร + cross-check ว่า W9 คือ plain itembag codec จริงหรือไม่สำหรับฟังก์ชันนี้โดยเฉพาะ

### ค้นใน `pf_bridge\external\` แล้ว: เจอ <อะไร> / ไม่เจอ
เจอ `external/PF_SERIALIZER_FIELDS.tsv:769-794` (26 แถว ItemOperateVitalRes) และ `external/PF_PROTOCOL_REGISTRY.tsv:47` (vtable/handler/serializer VA) — **ไม่มี layout ที่ครบพอสร้าง encoder** (ดู §1)

### ค้น gamedata แล้ว: เจอ <อะไร> / ไม่เจอ
ไม่เกี่ยว — นี่คือคำถามระดับ wire/static-image ไม่ใช่ตารางข้อมูลเกม

### บริบท (ทำไมใบนี้เปิด)
`ItemOperateVitalReq` (0x4BED) op=5 (สวม), value=8, identity=0x4 ("Blade") ยืนยันซ้ำ 3 ครั้งจริง
(`notes_to_chief/20260906_1255_KA1A-R321-RESULTS-*.md` §2 ภาคผนวก A) แต่ server ไม่ตอบ (RE-272
CAPTURED). `PANYA-ORDER 20260906_1312` สั่งให้ LANE-DB ตอบ op=5 ด้วย `ItemOperateVitalRes` (0x4C13,
`VITAL_REGISTRY_FROM_CLIENT_BINARY_20260817.tsv:125`, คู่กับ 0x4BED ที่ `:123`) รอบนี้ (`xqi5p4`) พยายาม
ประกอบ encoder แล้วพบว่ายังไม่พอ — รายละเอียดสองชั้นด้านล่าง

### §1 ชั้น static-image (pf-static-re agent รอบนี้, ไม่ใช้ client binary): NOT PROVABLE จาก TSV อย่างเดียว
`external/PF_SERIALIZER_FIELDS.tsv:769-794` (26 แถว, ฟังก์ชัน `0x005EDA20-0x005EDC31`): จาก 13 W-order
field มีแค่ 5 ที่มี tag/size/source ครบ (W1 tag `0x08` size 1 จาก `+0x30` · W2 tag `0x0B` size 1 จาก
`STACK+0x19` · W4 tag `0x08` size 1 จาก `STACK+0x1A` · W6 tag `0x32` size 8 จาก `DEREF(...)+0x24...+0x10`
PHI-branched · W8 tag `0x08` size 1 จาก `DEREF(...)+0x24...+0x18` PHI-branched) — อีก 8 แถวเป็น
`UNKNOWN`: W3/W12 `indirect_call_not_proven_serializer_slot` (`:772,:789`) · W5/W7
`invalid_parameter_import_call_wire_effect_unproved` (`:775,:778`, CRT `_invalid_parameter_noinfo`) ·
W9 `direct_call_not_proven_serializer` เรียก `0x0046F4D0` (`:783`) · W10/W11 atomic
increment/decrement ที่ vtable+0x04/+0x0C (`:785,:787`) · W13 `direct_call_not_proven_serializer` เรียก
`0x005ED2F0` (`:794`, ไม่มี closure ในทั้ง `pf_bridge` ที่อธิบายที่อยู่นี้เลย)

สถานะโครงการเองยืนยันซ้ำ: `notes_to_chief/reference_codex_attr/PF_V5_P1_OPEN.tsv:77` และ
`PF_PROTOCOL_PRIORITY.tsv:47` ระบุ `ItemOperateVitalRes` เป็น `OPEN` ทั้ง base/effective
serializer/structural status, blocker `DYNAMIC_DISPATCH_OR_SUBCALL_UNRESOLVED`,
`applied_overlay_chain=BASE_ONLY` (ยังไม่ได้ apply overlay ที่ reclassify การเรียก `0x0046F4D0` เป็น
non-wire แบบที่ `PF_A2_POOL_46F4D0_DELTA.tsv` ทำให้ 4 ข้อความอื่นแล้ว — grep `"ItemOperateVital"` ใน
ไฟล์ delta นั้น = 0 hit) · `PF_FIELD_VALIDATION.tsv:92` ระบุ capture layer `NOT_OBSERVED` — ไม่เคยมี
frame 0x4C13 จริงถูกจับจากฝั่ง server เลย (ตรงกับที่ server ไม่เคยตอบ op=5)

### §2 หลักฐานที่แรงกว่า: `tests/test_equip_state_static.py` (commit แล้วในรีโป server, gate ด้วย
`GAME_INSTALL_TREE.skip_unless_present()` — ต้องเครื่อง Panya ถึงจะรัน แต่ assertion ถูก pin sha256
ไว้แล้วในไฟล์นี้เอง ไม่ใช่ของใหม่ที่ใบนี้ขอ) ให้ข้อเท็จจริงที่แคบกว่าและตรงประเด็นกว่าทั้ง §1:

1. `test_item_operate_result_optional_bag_is_plain_not_collection` (บรรทัด 316-337): พิสูจน์แล้วว่า
   ฟังก์ชัน `item_operate_result_codec` (=`0x005EDA20`, ตัวเดียวกับ ItemOperateVitalRes) เรียก
   `0x46F4D0` (`plain_itembag_factory`) จริง สร้างกล่อง 0x68-byte ("plain ItemBag") ไม่ใช่ 0x90-byte
   `CollectionBagAttr` — **นี่คือคำตอบของ RE ask #1 ใน §1 สำหรับฟังก์ชันนี้โดยเฉพาะ (ไม่ใช่ analogy
   ข้ามข้อความแบบที่ `PF_V5_P1_OPEN.tsv` เตือน)** แต่ยังไม่ได้ผูกกลับเข้า `PF_A2_POOL_46F4D0_DELTA.tsv`
   หรือปลด `OPEN` status ใน `PF_V5_P1_OPEN.tsv:77`/`PF_PROTOCOL_PRIORITY.tsv:47`
2. `test_character_equipment_ui_requests_collection_bag_not_equipped_bag` (บรรทัด 267-313): ช่อง
   อุปกรณ์บนจอ (equipment UI) **ไม่ได้อ่านจาก `ItemBagAttr_Equiped`** แต่คำนวณจาก `CollectionBagAttr`
   ที่ map ทุก `ItemAttr` ใน backpack ที่ byte `+0x39` (ตรงกับ `ItemAttrState.raw_u8_39` ใน
   `inventory.py`) ผ่าน `mov dl, byte ptr [ecx+0x39]` แล้ว `shl edx, cl` (บรรทัด `0x5833AF`/`0x5833FE`)
   — คือใช้ค่า `+0x39` เป็น**shift count**สร้าง bitmask ของช่องที่สวมอยู่ ไม่ใช่คอนเทนเนอร์แยก
3. `notes_to_chief/reference_codex_attr/PF_ATTR_FIELD_SEMANTICS.tsv:478` ยืนยัน `+0x39` ค่า sentinel
   คือ `0xFF` (ตรงกับ `ItemAttrState.raw_u8_39` default ใน `inventory.py:27`) แต่ "gameplay identity
   is not uniquely bound to Data or an exact UI slot" — **ความหมายของค่าที่ไม่ใช่ 0xFF (ตัวเลขอะไรคือ
   'สวมอาวุธ'/'สวมโล่'/ฯลฯ) ยังไม่มีใครพิสูจน์**

### §3 สรุป: คำถามที่เหลือแคบกว่าที่ §1 ทำให้ดูเหมือน (ไม่ใช่ "5 call site ไม่รู้ความหมาย" อีกต่อไป)
เพราะ §2 ข้อ 1-2 ตอบคำถาม "โครงสร้างเฟรมเป็นยังไง" ไปแล้ว (คือ codec เดียวกับที่ `inventory.py`/
`item_operate_res_hypothesis.py` พิสูจน์แล้วสำหรับ pickup — ItemAttr ก้อนเดียวในกล่อง plain itembag)
คำถามที่เหลือจริง ๆ มีข้อเดียวที่ block arm (b): **ต้องตั้งค่า `raw_u8_39` (หรือฟิลด์ไหน) เป็นเลขอะไร
ในเฟรมตอบ เพื่อให้ client คำนวณ bitmask แล้วโชว์ "Blade" เป็นอาวุธที่สวมอยู่ในช่องอุปกรณ์บนจอ**

### สิ่งที่ขอให้ RE runner ตอบ (เรียงตามลำดับความสำคัญ)
1. **[หลัก]** ในเครื่อง Panya: หา call site หรือ const-data ที่เขียนค่า `+0x39` ที่ไม่ใช่ `0xFF` ให้
   `ItemAttr` จริง (grep VA รอบ ๆ `0x5833AF`/`0x5833FE`/`0x46B466` — จุดที่ตั้งค่า sentinel `0xFF` เอง
   อาจอยู่ใกล้จุดที่ตั้งค่าอื่นด้วย) แล้วตอบ: ค่า N ที่ไม่ใช่ 0xFF หมายถึง "สวมอยู่ที่ shift-bit N" ใช่
   หรือไม่ และมีตารางแม็ป N → equip-type (weapon/shield/head/...) ที่ไหนไหม (เทียบกับ
   `n_EQUIPTYPE`/`n_SLOT_RHAND` ใน `src/pirateforce_foundation/data/creation_gear_by_class.tsv` — ค่า
   value=8 ที่ client ส่งมาใน `ItemOperateVitalReq` op=5 บังเอิญตรงกับ `n_EQUIPTYPE=8` ของ
   `n_CLASS_ID=16` แถวเดียวในตารางนั้น — **สังเกตการณ์เฉยๆ ไม่ใช่ข้อสรุป** อาจเป็นเรื่องบังเอิญ)
2. **[รอง, เพื่อปิด status ให้ตรงของจริง ไม่ใช่เพื่อ arm (b)]** ยืนยัน/ปฏิเสธว่า W3/W5/W7/W10/W11/W12/W13
   ใน `PF_SERIALIZER_FIELDS.tsv:769-794` ล้วนเป็น non-wire lifecycle/refcount/CRT-param-check
   artifact (ตามรูปแบบที่ `PF_A2_POOL_46F4D0_DELTA.tsv`/`PF_A2_INVALID_PARAMETER_NONWIRE_DELTA.tsv`
   ทำกับ 4 ข้อความอื่นแล้ว) **เฉพาะสำหรับฟังก์ชันนี้** ไม่ใช่โดย analogy แล้วเติมแถว
   `ItemOperateVitalRes` เข้าไฟล์ delta ทั้งสอง ถ้าจริง — จะปลด `OPEN` status ใน `PF_V5_P1_OPEN.tsv:77`
3. resolve `0x005ED2F0` (W13, `:794`) — ไม่มี closure ไหนในทั้ง `pf_bridge` อธิบายที่อยู่นี้เลย

### เกณฑ์ที่ทำให้ตอบได้ (ไม่ต้องเปิดเกม ไม่ต้องแคปเจอร์สด — static ล้วนถ้าเครื่อง Panya มี binary)
ตอบข้อ 1 อย่างเดียวก็พอให้ LANE-DB เขียน encoder ได้ (มีโครงสร้างเฟรมพร้อมจาก §2 แล้ว เหลือแค่ค่า
`raw_u8_39` ที่ถูกต้อง) — ข้อ 2/3 เป็นการปิดบัญชี status ให้ตรงความจริง ไม่ block arm (b)

### nonclaims
1. ไม่อ้างว่า value=8/identity=4 ที่ client ส่งมาคือ n_EQUIPTYPE จริง — สังเกตค่าตรงกันหนึ่งแถวเท่านั้น
2. ไม่อ้างว่า `test_equip_state_static.py` เคยรันจริงในรอบนี้ (gate ด้วย binary ที่ cloud clone ไม่มี) —
   อ่านเนื้อไฟล์/assertion ที่ commit ไว้เท่านั้น
3. ไม่อ้างว่าโครงสร้างเฟรม (tag/size ตาม §2) พิสูจน์แล้วสำหรับ "สวม" โดยเฉพาะ — พิสูจน์แล้วสำหรับ
   "pickup" (`item_operate_res_hypothesis.py`/RE-059) เท่านั้น ยังไม่มี capture ของเฟรมตอบ "สวม" จริง
   (`PF_FIELD_VALIDATION.tsv:92`: `NOT_OBSERVED`) — สมมติว่าโครงสร้างเดียวกันใช้ได้กับ "สวม" ด้วย เป็น
   ข้อสันนิษฐานที่สมเหตุสมผล (โค้ดฝั่ง client ใช้ handler เดียวกันสำหรับทุกกรณีของ 0x4C13) ไม่ใช่ข้อพิสูจน์

**links**: `notes_to_chief/20260906_1316_...rjqssc...md` §7 · `notes_to_chief/20260906_1255_KA1A-R321-
RESULTS-*.md` §2 · `notes_to_chief/reference_codex_attr/PF_ATTR_FIELD_SEMANTICS.tsv:478` ·
`notes_to_chief/reference_codex_attr/PF_V5_P1_OPEN.tsv:77` · `notes_to_chief/reference_codex_attr/
PF_A2_POOL_46F4D0_DELTA.tsv` · `pirate-force-server tests/test_equip_state_static.py:267-337` ·
`pirate-force-server src/pirateforce_foundation/inventory.py:21-28`

### ATTENDED: (วางโดย LANE-K รอบ `x91eo8` คำต่อคำจากจดหมาย
`notes_to_chief/20260906_1737_LANE-DB-TO-K-attended-block-RE-280-equip-worn-flag-client-memory-observation.md`
· ตามที่ `COO-DECISION 20260906_1651` สั่งให้ DB ส่งก่อนปิดรอบ — บล็อกนี้ตอบคำถามหลักของ `RE-280`
เอง (หา call site ที่เขียนค่า `+0x39`) ไม่ใช่เวอร์ชันเต็มที่ `1651` ร่างไว้ (สลับเฟรมตอบเซิร์ฟเวอร์ 4
แบบ) ซึ่งยังรอ seam `1452` + encoder ก่อน — DB ตรวจสดแล้วว่ายังไม่มีเฟรมตอบให้เลือกหลายแบบจริง
[สมมติของสาย LANE-DB - รอ COO ยืนยัน])

1. บูต: ปกติ ไม่มีธง server (ยังไม่มี encoder ให้ตั้งธง) — แนบ debugger/memory-watch ที่ VA `0x5833AF`/
   `0x5833FE`/`0x46B466` เหมือนชุดจับ RE-272 เดิม
2. พิมพ์/กด: สวม "Blade" 1 ครั้ง (ลากจากกระเป๋าลงช่องอาวุธ) อ่านค่าที่ breakpoint เขียนลง `ItemAttr+0x39`
   ทันที — เวลาเหลือทำซ้ำได้สูงสุด 4 ไอเทมคนละช่อง (โล่/หมวก/...) อย่างละครั้ง
3. ดูค่าอะไร: N (ไม่ใช่ `0xFF`) ที่เขียนต่อไอเทมแต่ละชิ้น จับคู่กับช่องที่จอโชว์เอง (client แสดงเองฝั่ง
   client ไม่ต้องรอ server ตอบ)
4. ผ่าน/ไม่ผ่าน: ได้คู่ (item, N) อย่างน้อย 1 คู่ตรงกับช่องบนจอ = ผ่าน พอให้ DB เขียน encoder ได้ ·
   relog/server-frame-variant ยังทดสอบไม่ได้จนกว่า seam `1452` ขึ้น main (nonclaim ข้างบน)

nonclaims ของบล็อกนี้ (จาก LANE-DB คำต่อคำ):
1. ไม่อ้างว่านี่คือบล็อกแบบที่ `1651` ขอเป๊ะ (เฟรมตอบเซิร์ฟเวอร์ 4 แบบสลับด้วยแชท/relog) — สิ่งนั้นต้องมี
   seam `1452` + encoder ก่อน ยังไม่มีทั้งคู่ตรวจสดแล้ว
2. ไม่อ้างว่า VA `0x46B466` เป็นจุดตั้งค่า sentinel ที่พิสูจน์แล้ว — คัดลอกมาจากคำถามเดิมของ `RE-280` เอง
   (`1449` §RE ask 1) ยังไม่มีคำตอบ
3. ไม่อ้างว่า relog จะยังเห็นของสวมอยู่ — ไม่มี wire เขียน DB จริงตอนนี้ ข้อ 4 จึงตัดส่วน relog ออกจาก
   เกณฑ์ผ่าน (ต่างจากร่างเดิมของ `1651` โดยเจตนา)

### result:
**DONE (ask 1 + ask 2 + ask 3)** -- พับโดย LANE-K รอบ `73i74a` 2026-09-07T10:09+07:00 · คัดลอกจาก `notes_to_chief/20260906_2258_RE-280-RESULT-0x39-IS-A-SHIFT-BIT-INDEX-FF-MEANS-NOT-EQUIPPED.md` คำต่อคำ

> **สถานะ: DONE (ask 1 + ask 2 + ask 3) / static ล้วน · ชั้น client-observable ยังเป็นของบล็อก ATTENDED ในใบเอง**
>
> **คำตอบหนึ่งบรรทัดสำหรับแขน (ข):** เฟรมตอบต้องส่ง `ItemAttr+0x39 = N` โดย **N ไม่ใช่ `0xFF`** — client เอา N ไปทำ `mask = 1 << N` ตรง ๆ (`0x005833F9`/`0x005833FE`) ไม่มีการ lookup ตารางใด ๆ ระหว่างทาง ⇒ **N คือดัชนีบิตของช่องอุปกรณ์ ไม่ใช่รหัส equip-type**

🟡 **ชั้นที่ขาด (K ไม่ปั๊มให้ครบ)**: จดหมายเขียนเองว่าชั้น **client-observable ยังเป็นของบล็อก `ATTENDED:` ในใบเอง** ⇒ ใบนี้ปิดในฐานะใบ static เท่านั้น

> 🔴 **ห้ามสายอื่นใช้เลข `RE-280`** · numbering: ตัวนับร่วมสองคิว + `archive/*QUEUE*ARCHIVE*` คืน **279** (`GT-279`, ตั้งเลขรอบ `rsmsia`) ⇒ ใบนี้ **280** · ตรวจ 0 hit ของ `GT-280`/`RE-280` ทั้งสามที่ (`GAME_TEST_QUEUE.md` · `CLIENT_RE_QUEUE.md` · `archive/*QUEUE*ARCHIVE*.md`) ก่อนวาง [ตรวจโดย LANE-K รอบ `zqq4qz`] · เร่งด่วน: `PANYA-ORDER 0156` เส้นตาย 23:00 +07:00 คืนนี้ (`COO-DECISION 20260906_1547` ข้อ 4(1) สั่งตั้งเลขนี้ก่อนใบอื่นทั้งหมด)

- ~~RE-282 CHARCREATE-CLASS-S-SCORE-STARTING-STATS-SEMANTICS-001~~ -> `archive/CLIENT_RE_QUEUE_ARCHIVE_20260907_closed.md` (**CLOSED DONE/BOUNDED-NEGATIVE** 2026-09-06T23:22+07:00 โดย RE runner ... · ย้ายทั้งก้อนคำต่อคำโดย LANE-K รอบ `spppsd` 2026-09-07T14:22+07:00 · ไม่มีอะไรถูกลบ)


## RE-286 TRIGGERRESULT-DIRECTION-AND-CALLER-CHAIN-001  [🔧 **DONE (ตอบครบทั้ง 3 ข้อ) — พับโดย LANE-K รอบ `73i74a` 2026-09-07T10:09+07:00** คำต่อคำจากหัวจดหมายผล `notes_to_chief/20260907_0326_RE-286-RESULT-INBOUND-TRIGGER-STATE-APPLY-NO-COMMON-CONFIRM-IN-THREE-LEVELS.md` (RE runner บนเครื่อง Panya 2026-09-07T03:26+07:00): "**สถานะ: DONE (ตอบครบทั้ง 3 ข้อ) · static ล้วน ไม่เปิดเกม ไม่จับ `LOCK_GAME`**" · K คัดลอกคำของผู้เทส **ไม่ได้ตัดสินเอง** และไม่ได้แตะเนื้อใบ · 🟠 บันทึกเดิมก่อนพับ (ไม่ลบ ขีดฆ่าไว้ตามธรรมเนียมบ้าน = ถอนแล้วโดยเจตนา ไม่ใช่สถานะสด): ~~🔴 **OPEN**~~ · 🔺 `[STATIC-ON-BRIDGE]` (ต้องมี `GameClient.local.bin` จริง -- ไม่ใช่ attended, ไม่ต้องเปิดเกม, ไม่ต้องจับ `LOCK_GAME`) · **เจ้าของใบ/ผู้เขียนเนื้อใบ/ผู้บริโภคผล = LANE-UI** · ตั้งเลขโดย LANE-K รอบ `camatf` 2026-09-06T22:17+07:00 · เนื้อใบมาจากจดหมาย `notes_to_chief/20260906_2124_LANE-UI-TO-K-re-body-triggerresult-direction-and-caller.md` คำต่อคำ] -- moved to `tickets/RE-286.md` (>8,192 B, verbatim, per `PANYA-ORDER 1448` + `.gitignore !/tickets/` merged R373 · เขียนตั้งแต่รอบ `camatf` แต่เขียนสตับคิวไม่ได้เพราะเซสชันนั้นไม่มี git (ดู `notes_to_chief/20260906_2217_LANE-K-ASK-COO-tool-write-ceiling.md`) -- เติมสตับให้จริงโดย LANE-K รอบ `hf1gs9` 2026-09-06T23:17+07:00)

### result:
**DONE (ตอบครบทั้ง 3 ข้อ)** -- พับโดย LANE-K รอบ `73i74a` 2026-09-07T10:09+07:00 · คัดลอกจาก `notes_to_chief/20260907_0326_RE-286-RESULT-INBOUND-TRIGGER-STATE-APPLY-NO-COMMON-CONFIRM-IN-THREE-LEVELS.md` คำต่อคำ (จดหมายมี `.CONSUMED.txt` ของ LANE-UI แล้ว หัวใบเป็นส่วนที่ยังค้าง)

> **สถานะ: DONE (ตอบครบทั้ง 3 ข้อ) · static ล้วน ไม่เปิดเกม ไม่จับ `LOCK_GAME`**
>
> **คำตอบสามบรรทัด**
> 1. **inbound จริง** — handler `0x006018A0` เป็น handler **เฉพาะตัว** (ไม่แชร์กับใครใน 519 คลาส) และมัน **อ่านฟิลด์ที่มาจากสาย** (`+0x3C`, `+0x3E`, `+0x3F`, `+0x5C`) แล้วเอาไปแก้สถานะทริกเกอร์ในฉาก · ไม่มีโค้ดฝั่งไคลเอนต์ที่ไหนสร้างอ็อบเจ็กต์นี้เพื่อส่งออกเลย
> 2. **ไม่ใช่ candidate ของ "รายงานกัปตัน"** — เดิน caller/callee graph **3 ชั้น** จาก handler แล้ว **ไม่พบทั้ง opener `0x005AB5F0` และสตริง `"Common_Confirm"` (`0x00F19F44`) / `"Common_Confirm%d"` (`0x00F2BE9C`)**
> 3. `+0x18` (qword tag `0x32`) **ไม่ใช่** ตัวเดียวกับ `+0x12` ของ `AddSurveyData` — **ตัวที่ทำหน้าที่ "trigger/dock id" คือ `+0x3C` (u16, tag `0x0F`)** ซึ่ง apply เอาไป lookup ทริกเกอร์จริง · `+0x18` ไม่ถูกอ่านในเส้นทางรับเลย

> numbering: ตัวนับร่วมสองคิว + `archive/*QUEUE*ARCHIVE*` คืน **285** (`RE-285`, ตั้งเลขรอบ `zqq4qz`) ⇒ ใบนี้ **286** · ตรวจ 0 hit ของ `GT-286`/`RE-286` ทั้งสามที่ (live สองคิว + `archive/*QUEUE*ARCHIVE*` + `tickets/`) ก่อนวาง [ตรวจโดย LANE-K รอบ `camatf`]


