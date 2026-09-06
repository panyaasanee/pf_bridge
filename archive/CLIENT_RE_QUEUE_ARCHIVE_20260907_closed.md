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
