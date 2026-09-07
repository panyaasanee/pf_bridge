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


<!-- moved verbatim from CLIENT_RE_QUEUE.md by LANE-K round kq7m3d 2026-09-07T18:22+07:00 -- 9 closed blocks, nothing deleted, one-line stub left in place for each -->
<!-- CORRECTION (LANE-K round kq7m3d addendum 2026-09-07T18:48+07:00, pf-adversary D1): the sentence above was FALSE when it was written.  The RE-256 move over-ran its block by six lines and carried the pointer stubs of RE-259 and RE-260 in with it, so those two lines WERE removed from CLIENT_RE_QUEUE.md and RE-260 became ungreppable there.  Both have been restored to the queue byte-identical to 87267dd:989-994.  11 items left the queue this round, not 9.  Nothing in this file was deleted to fix it. -->

## 🆕🔬 RE-122 PLAYER-STANDARD-STATUS-AND-CHARCREATE-SCORE-VALUES-001 [STATIC-ON-BRIDGE] [🟢 **DONE / BOUNDED-NEGATIVE (static-only)** — คำต่อคำจากหัวข้อ "## สถานะ" ของจดหมายผล `notes_to_chief/consumed/20260828_0815_RE-122-RESULT-SCORE-IS-SIX-AXIS-MP-UNPROVEN.md` (RE runner 2026-08-28T08:15+07:00): "**DONE / BOUNDED-NEGATIVE (static-only)** — ปิด T0–T4 ตามเกณฑ์ทางเลือกของใบ `PLAYER-STANDARD-STATUS-AND-CHARCREATE-SCORE-VALUES-001`; current corpus ไม่ให้ provenance ที่พอสำหรับเติม MP/STR/CON/DEX/INT/PER constants และห้ามนำค่า probe/buff/UI score ไป production" · พับโดย LANE-K รอบ `k01t0u` 2026-09-07T12:15+07:00 · K คัดลอกคำของผู้ทำ **ไม่ได้ตัดสินเอง** · 🔴 หัวใบนี้**ไม่เคยมีสถานะเลย** ตั้งแต่จดหมายผลลงวันที่ 2026-08-28 — ค้าง **10 วัน**]: **ค่า MP current/max และ STR/CON/DEX/INT/PER จริงของตัวละคร level 1 class 1 (Gladiator) คือเท่าไหร่ — ไม่ใช่ตำแหน่ง wire (ปิดแล้ว) แต่เป็นตัวเลข**

> 🔢 หมายเหตุเลข: shared counter (RE/GT ร่วมกัน) สูงสุดที่ใช้อยู่ตอนนี้คือ `GT-121`; grep ยืนยันก่อนเปิดใบ
> (2026-08-28T07:30+07:00): `RE-122`/`GT-122` = 0 hits ใน `CLIENT_RE_QUEUE.md`/`GAME_TEST_QUEUE.md` ⇒ ใบนี้จอง `122`

### ที่มา
CORE-REQUEST-023 รอบ `x6a85q` (R208, ต่อจาก R203/R204 ที่วาง class+level ไว้แล้ว): PANYA-DECISION
`20260828_0125` สั่งให้ตัวละครบูตทุกครั้งต้องมี "probe base 1" ครบ (MP, STR/CON/DEX/INT/PER รวมอยู่ด้วย)
chief ต่อสาย **movement speed** ได้ (owner เคยเห็นค่า 400 บนจอเอง จาก probe fork ของเธอ — client-observable
value, ไม่ใช่ของประดิษฐ์) แต่ **MP/STR/CON/DEX/INT/PER ต่อไม่ได้** เพราะไม่มีค่าตัวเลขจริงใน repo นี้เลย —
ตรวจแล้ว (G1, สองแหล่งอิสระ):
- `reports/PF_JOB001_CHARCREATE_CLASS_STATIC_BOUNDARY_20260816.md`: ตาราง `CHARCREATE_CLASS` มี 37 คอลัมน์
  (ไอคอน/รูปลักษณ์/equipment/`s_SKILL_*`) — **ไม่มีคอลัมน์ `s_SCORE` หรือ stat score ใด ๆ เลย**
- `reports/PF_STATS_PROG001_CHARACTER_STATS_AND_PROGRESSION_STATIC_20260818.md` §8.4: บอกตรง ๆ ว่า
  "the actual per-level curves... remain unknown and would require decoding [external] data files, which
  this milestone did not do" — `STANDARD_STATUS`/`POTENTIAL` มีชื่อคอลัมน์ (`n_STRENGH`/`n_CONSTITUTION`/
  `n_AGILITY`/`n_INTELLECT`/`n_PERCEPTION`/`n_HPMAX`/`n_STAMINAMAX`) แต่ **ไม่เคย decode ค่าจริง**

wire POSITION ของทั้งหกช่องนี้ **ปิดแล้วจริง** (ห้ามทำซ้ำ ใบนี้ไม่ใช่ RE ตำแหน่ง):
- MP current/max: `BasicAttr +0x4C/+0x50`, u32 tag `0x14`, mask `0x0010/0x0020` — ยืนยันสองแหล่งอิสระตรงกัน
  (`RE-117`, disasm ตรง `BasicAttr::Serialize 0x004656F0`; และ `PF_STATS_PROG001` §4 gate `0x465772/0x465786`)
- STR/CON/DEX/INT/PER: `ActorAttr +0x82/0x84/0x86/0x88/0x8A`, u16 tag `0x12`, mask `0x20/0x40/0x80/0x100/0x200`
  (`PF_STATS_PROG001` §5 gate `0x46631F..0x46638A`) — ยังไม่มีแหล่งที่สองยืนยันเฉพาะ 5 ช่องนี้ (แหล่งเดียว G1)

### objective
1. หา `STANDARD_STATUS`/`POTENTIAL` (หรือตารางเทียบเท่า) ใน `gamedata`/`external` ที่ RE-117 เคยค้นแล้วไม่พบ
   คอลัมน์ MP สำหรับมอน — รอบนี้ค้นเฉพาะแถว **ผู้เล่น class 1 (Gladiator) level 1** อาจอยู่คนละไฟล์กับ `MOBS`
2. ถ้าเจอค่าเป็นสูตร (level/class formula) ให้ยืนยันด้วยการคำนวณที่ level 1 ก่อน ห้ามข้ามไปสูตรทั่วไปโดยไม่ยืนยัน
   จุดฐาน (G6: ห้ามประกาศความหมายจากการอ่านครั้งเดียว — ต้องมีสองแหล่งหรือ static+cross-check เหมือน speed)
3. ยืนยัน STR/CON/DEX/INT/PER wire position (`PF_STATS_PROG001` §5) ด้วยแหล่งที่สองอิสระถ้าทำได้ (ตอนนี้มีแหล่งเดียว)
4. ถ้าชนเพดาน static (ต้องใช้ `GameClient.local.bin`/capture corpus ที่คลาวด์นี้ไม่มี) ให้เขียน bounded negative
   แยกข้อ ระบุว่าต้องใช้เครื่องสะพานจริงถึงจะปิดต่อได้ — **ห้ามเดาค่าส่งขึ้น production เด็ดขาด** (RE-117's
   nonclaim #3 วางกฎเดียวกันไว้แล้วสำหรับฝั่งมอน: "ห้ามประดิษฐ์ค่าหรือยืมสูตร PC" — ฝั่งผู้เล่นเองก็ห้ามประดิษฐ์
   เช่นกัน ไม่มีทางลัด)

### กติกาบังคับ (เหมือนทุกใบ static)
อิมเมจ/ไฟล์อ่านอย่างเดียว · ทุกข้อสรุปมี provenance (offset/แถว/span SHA) · ชนเพดานให้เขียน bounded negative
แล้วปิด ไม่เดาต่อ · ไม่เปิดเกม ไม่จับ `LOCK_GAME` ไม่แตะ canonical DB

### เกณฑ์จบใบ
ค่า MP current/max และ STR/CON/DEX/INT/PER ของ level 1 class 1 พร้อม provenance พอให้ chief เติมลง
`player_wire.py`'s `PLAYER_LOGIN_MOVEMENT_SPEED`-style constants ได้ (wire position พร้อมอยู่แล้ว เหลือแค่ค่า)
**หรือ** bounded negative ที่ชัดเจนว่าต้องใช้เครื่องสะพาน ⇒ ปิดใบพร้อมบรรทัด `BUILD_IMPACT:`

**ทำไมมีค่า:** ตัวละครที่บูตวันนี้ MP=0/1 (ไม่เคยส่ง) และไม่มี STR/CON/DEX/INT/PER เลย — ยังไม่ "สมประกอบ"
ตามที่เจ้าของสั่งไว้ใน `PANYA-DECISION 0125` เต็มรูปแบบ (มีแค่ class+level+speed จาก R203/R208) ปิดใบนี้แล้ว
เติมค่าเป็นการแก้ constant บรรทัดเดียวในโค้ดที่มีอยู่แล้ว ไม่ต้องหา wire position ใหม่

---

## 🆕🔬 RE-128 SCENE-ORDINAL-TO-MOBS-NID-TABLE-LOCATION-001 [STATIC-ON-BRIDGE] [🟢 **PASS/DONE — DIRECT+INSTANCE CLINE SELECTORS PINNED** — คำต่อคำจากบรรทัด "สถานะที่ควรกรอก" ของจดหมายผล `notes_to_chief/consumed/20260828_2314_RE-128-RESULT-DIRECT-AND-INSTANCE-CLINE-SOURCES.md` (RE runner 2026-08-28T23:14+07:00) · verdict ในจดหมายฉบับเดียวกัน: "**PASS/DONE** — ตัว client เลือก `n_CLINE_TYPE` สองทางจริง: ฉากปกติอ่านจาก `SCENE_NAME`; ฉาก instance อ่านจาก `INSTANCE` ด้วย instance id ที่ active อยู่ แล้วใช้ `(n_CLINE_TYPE,n_CREATURE_TYPE)` เข้า `CLINE` เหมือนกัน" · พับโดย LANE-K รอบ `k01t0u` 2026-09-07T12:15+07:00 · K คัดลอกคำของผู้ทำ **ไม่ได้ตัดสินเอง** · 🔴 หัวใบนี้**ไม่เคยมีสถานะเลย** ตั้งแต่จดหมายผลลงวันที่ 2026-08-28 — ค้าง **10 วัน** · เนื้อใบเต็มอยู่ที่ `tickets/RE-128.md` — หัวใบที่นั่นพับด้วยคำเดียวกันรอบนี้]: **ไฟล์/ตารางไหนของไคลเอนต์เก็บ mapping "เลขชุดต่อฉาก (1..115) → `MOBS.n_ID` (ถึง 10,080)" — ตัวที่หายไปทั้งโปรเจกต์ และเป็นตัวเดียวที่ทำให้ Port Royal เกิด NPC ผิดตัวทุกจุด** -- moved to `tickets/RE-128.md` (>8,192 B, verbatim, per `PANYA-ORDER 1448` + `.gitignore !/tickets/` merged R373 · LANE-K round `x91eo8` 2026-09-06T18:10+07:00)

## 🔬 RE-209 QUEST-SETTER-PROLOGUE-11-BYTES-ESI-PROVENANCE-001 [✅ **DONE / POSITIVE (bounded) — พับผลโดย LANE-K รอบ `x91eo8` 2026-09-06T18:2x+07:00** จากจดหมาย `notes_to_chief/20260906_1821_RE-209-RESULT-two-bytes-are-a-jcc-esi-single-object-branch-b-closes.md` (สถานะที่เสนอโดยผู้ทำ RE runner คำต่อคำ) (เดิม: OPEN **ย่อเหลือ 2 ไบต์**) -- เปิดโดย LANE-A รอบ `8z9h9n` 2026-09-02T11:0x+07:00 · **ย่อขอบเขตโดย LANE-A รอบ `f6e5kd` 2026-09-03** หลังบริโภคใบผล `notes_to_chief/20260902_1039_RE-202-RESULT-CNETNPC-RUNTIME-BIT-NOT-BASICATTR.md` · ผู้ทำ: **สาย RE** (ผู้ทำสายเดียว ไม่ต้องจอง) · **LANE-A บริโภคผลเอง (ยังไม่บริโภค ณ ตอนพับ — รอ LANE-A อ่านผล)** · 🔴 `[STATIC-ON-BRIDGE]` ต้องดิสแอสเซมบลีอิมเมจ ⇒ ทำบนคลาวด์ไม่ได้]

> 🔵 **สองในสามของใบนี้ตอบแล้ว — เหลือ 2 ไบต์ (LANE-A รอบ `f6e5kd` 2026-09-03T14:35+07:00)**
> ใบผล `20260902_1039` (ซึ่งไม่มีใครอ่านอยู่ 28 ชั่วโมง จน chief ส่งต่อในใบ `20260903_1207`) ปิดไปแล้วสองข้อ:
> **(1) `span_sha256`** `f808c0d6…2bc5` ของสแปนเต็ม ตรงกับอิมเมจ `9627…b623` — เกณฑ์ข้อที่สองของใบนี้ **ปิด**
> **(2) 3 ไบต์แรก** `0x0045BC80..0x0045BC82` — ใบยก `0x0045BC81  mov esi, ecx` ⇒ `ESI` = `this` **ก่อน** ประตู
> ⇒ สาขา "`push ebx; mov esi,edx` ⇒ ต้องทบทวน ข." **ตายแล้ว** และ caller ยืนยันชนิดซ้ำ (`[QuestNPCModule+0x18]` → `CNetNPC` → `ECX`)
> **สิ่งที่ยังเหลือ และเป็นทั้งใบตอนนี้: 2 ไบต์ `0x0045BC87..0x0045BC88`** (ช่องว่างหลังประตู ก่อน `movsx` ที่ `0x0045BC89`)
> ใบ `1039` มีแต่ประโยคสรุปว่า "ไม่มีการ dereference ไป attached attr ระหว่างทาง" — **ไม่ได้ยกไบต์มาแสดง**
> ⇒ ถ้าสองไบต์นั้นคือ `8B F1` (`mov esi,ecx`) ประตูที่ `BC83` อ่านออบเจ็กต์คนละตัวกับ `+0x360/+0x364` และ **ข. ต้องทบทวน**
> ⇒ ถ้าเป็น jcc/nop/อะไรก็ตามที่ไม่เขียน `ESI` ⇒ **ข. ปิดสนิท** และ `RE-202` ไม่มีข้อจำกัดเหลือเลย
> 🔴 **ห้ามอ่านการย่อนี้ว่า "ตอบแล้ว"** — ยังไม่มีใครเห็นสองไบต์นั้น และ 12 ไบต์ที่ `0x45BC90` ก็ยังไม่มีใครอ่านเหมือนเดิม

ใบนี้ถือ **ขั้นตอนเดียวที่ `RE-202` ปิดไม่ลง** ไว้ไม่ให้หายไปกับใบที่ปิดแล้ว (pf-adversary รอบสอง ข้อ 6)
`RE-202` ตอบ **ข.** (`+0x70` เป็นของ `CNetNPC`) และมีหลักฐานอิสระหนุน แต่ *เส้นทางพิสูจน์ผ่าน ESI*
ยังมีรู: literal ที่ commit ไว้ปัก **29 จาก 60 ไบต์** ของสแปน `0x0045BC80..0x0045BCBC` เท่านั้น

**คำถามเดียวของใบนี้: 11 ไบต์แรก `0x0045BC80..0x0045BC8A` ประกอบด้วยคำสั่งอะไรบ้าง**
(prologue 3 ไบต์ก่อนประตู + ช่องว่าง 2 ไบต์หลังประตู)

- ถ้า 3 ไบต์แรกไม่ได้เขียน ESI และ 2 ไบต์กลางเป็น jcc ⇒ ESI ตัวเดียวตลอด ⇒ **ข. ปิดสนิท**
- ถ้า 3 ไบต์แรกเป็น `push ebx; mov esi,edx` (`8B F2`) หรือ 2 ไบต์กลางเป็น `mov esi,ecx` (`8B F1`)
  ⇒ ประตูอ่านออบเจ็กต์คนละตัวกับที่ `+0x360/+0x364` ใช้ ⇒ **คำตอบของ `RE-202` ต้องกลับมาทบทวน**
  (และงาน quest mark ฝั่งเซิร์ฟเวอร์กลับมามีทางเดินอีกครั้ง)

**เกณฑ์ปิดใบ (ชั้นเดียว ชั้น static เท่านั้น — ไม่มีชั้น client-observable และไม่ต้องมี)**
- ดิสแอสเซมบลี `0x0045BC80..0x0045BC8A` จากอิมเมจ `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`
  ยกไบต์ + คำสั่งที่ถอดได้มาทั้งช่วง แล้วตอบว่า ESI ถูกเขียนก่อนถึง `0x0045BC83` หรือไม่ และหลังจากนั้นหรือไม่
- ยืนยัน `span_sha256` `f808c0d68b1a782d3441e118a25a94ee73e1f4aea37824b06fd2e2c6fb112bc5`
  ของสแปนเต็มกับอิมเมจไปด้วย (`RE_STATIC_SEARCH_RULES.md` §1 ซึ่ง `RE-202` ทำไม่ได้จากคลาวด์)

**ราคาที่ประหยัดได้ถ้าไม่ทำ:** ไม่มี — ใบนี้เล็กมาก (11 ไบต์) และเป็นสิ่งเดียวที่กั้นไม่ให้คำตอบของ
`RE-202` เป็นข้อสรุปที่พิสูจน์ครบ · ถ้าผลออกมาขัดกับ ข. LANE-A จะเปิด `RE-202` ใหม่เองในรอบถัดไป

- links: `RE-202` (ปิดแล้ว ใบผล `notes_to_chief/20260902_1035_RE-202-RESULT-*`) ·
  `notes_to_chief/reference_codex_attr/pf_rederive_attr_semantics.py:7094-7097, 7492-7495` ·
  `PF_ATTR_QUEST_MARK_SELECTOR.tsv` คอลัมน์ `support_spans`
- ค้นใน `pf_bridge\external\` แล้ว: **ไม่เจอ** (ค้นจากคลาวด์: ไม่มีดิสแอสเซมบลีของสแปนนี้ที่ commit ไว้
  นอกจาก literal สี่ตัวข้างบน ซึ่งไม่ครอบคลุม 11 ไบต์ที่ถาม) · ค้น `gamedata` แล้ว: **ไม่เกี่ยว** (คำถามอยู่ในโค้ด ไม่ใช่ตาราง)

### result: (พับโดย LANE-K รอบ `x91eo8` คำต่อคำจากจดหมาย
`notes_to_chief/20260906_1821_RE-209-RESULT-two-bytes-are-a-jcc-esi-single-object-branch-b-closes.md`
— สถานะที่เสนอ: **DONE / POSITIVE (bounded)**)

สรุปหนึ่งบรรทัดจากจดหมาย: 2 ไบต์ที่ `0x0045BC87..0x0045BC88` คือ `74 2F` = `je 0x0045BCB8` (jcc) —
ไม่เขียน `ESI` ⇒ `ESI` เป็นออบเจ็กต์ตัวเดียวตลอดฟังก์ชัน ⇒ สาขา ข. ของ `RE-202` (`+0x70` เป็นของ
`CNetNPC`) ปิดสนิท ไม่ต้องทบทวน · `span_sha256` ตรง (`f808c0d6…2bc5`) · BUILD_IMPACT: ไม่มี (LANE-A
ไม่ต้องเปิด `RE-202` ใหม่) · ชั้นเดียว (static ล้วน ตามที่ใบกำหนดเองว่าไม่ต้องมีชั้น client-observable)

🔴 **หมายเหตุจาก LANE-K**: จดหมายผลเก่า
`notes_to_chief/20260902_1143_RE-209-RESULT-prologue-proves-one-ESI-object.md` (ไม่มี `.CONSUMED.txt`
มาตั้งแต่ 2026-09-02) ตอบคำถามคนละขอบเขต — **ก่อน**ที่ LANE-A จะย่อใบเหลือ 2 ไบต์ในรอบ `f6e5kd`
(ดูบล็อกขีดฆ่า/เตือนด้านบน "ห้ามอ่านการย่อนี้ว่าตอบแล้ว") ⇒ ไม่ใช่คำตอบของคำถามปัจจุบัน ถือเป็นประวัติ
ไม่ใช่หลักฐานที่ใช้ปิดใบนี้ — พับ/บันทึกไว้เป็นข้อสังเกตเท่านั้น ไม่ได้ใช้แทนจดหมาย `1821` ข้างบน

- numbering: `RE` สูงสุดในไฟล์นี้ = 208 · grep `RE-209` ทั้งรีโปพบเฉพาะใบนี้ ⇒ `209`
- result: (สาย RE กรอก: ไบต์ + คำสั่งที่ถอดได้ของ `0x0045BC80..0x0045BC8A` · ESI ถูกเขียนหรือไม่ · sha ตรงหรือไม่ · timestamp)

## 🔬 RE-227 CAPTAIN-REPORT-ON-ISLAND-CONTACT-001 [🔴 **primary hypothesis REFUTED-ON-SCREEN (R318 `1319`) · covered by `RE-265`** — แก้หัวใบโดย LANE-A รอบ `ihjytc` 2026-09-05T16:4x+07:00 ตาม `COO-DECISION 20260905_1348` ข้อ 4]

> 🔴 **หัวใบเดิมของบรรทัดนี้คือ `DONE / BOUNDED` ปิดโดย LANE-A รอบ `2mnd7b` 12:0x — ~~ปิด~~ ถอนแล้ว ไม่ใช่แก้คำผิด**
> **เพราะอะไร**: `GT-233` R318 (`notes_to_chief/20260905_1319_KA1A-R318-RESULTS-*.md`) ยิง 8 เร็กคอร์ด 73 ไบต์ผ่าน parser ของไคลเอนต์ (0 `ErrorData` ⇒ `RE-256` ถูก) แล้วแล่นเรือเข้าใกล้เกาะ **37 หน่วย** (Prison Exile ×3) และ **144 หน่วย** (Spice Paradise ×3) — ทั้งสองระยะต่ำกว่าเกณฑ์ ≤500 ที่ชั้น ① ของใบนี้อ้าง — และ **หน้ารายงานกัปตันไม่เด้งสักครั้ง** (Panya ยืนยันด้วยตา 12:48)
> ⇒ ชั้น ① "client เช็กระยะเอง ≤500 แล้วเปิดหน้าต่างในเครื่อง" = **REFUTED บนจอ** ไม่ใช่ `shipped` · ห้ามคงคำว่า shipped ไว้ในหัวใบนี้อีก (`COO-DECISION 20260905_1348` ข้อ 4)
> **อะไรที่ยังยืน**: กลไกฝั่งเซิร์ฟเวอร์ที่ขึ้น main แล้ว (`world_m2_provisioning_trial.py`/`navigationex_survey_record.py` · PR `#753`/`#760`/`#797`/`#810`) **ส่งเร็กคอร์ดออกได้จริงและไคลเอนต์รับได้จริง** — สิ่งที่หักล้างคือคำอธิบายว่า "อะไรเปิดหน้าต่าง" ไม่ใช่โค้ดที่ส่ง
> **ใครตอบต่อ**: `RE-265 WHAT-OPENS-THE-CAPTAIN-DOCK-REPORT-WINDOW-001` (สามคำถาม · เนื้อใบส่งเป็นจดหมาย `20260905_16xx_LANE-A-RE-265-TICKET-BODY-*.md` รอบ `ihjytc`) · ห้ามบูต `GT-233` ซ้ำจนใบนั้นตอบ · ทาง BACKUP XYZ ปิดถาวร
> **สองสมมติฐานที่เหลือถือเท่ากัน** จนกว่า `RE-265` ตอบ (`1348` ข้อ 5): (ก) เซิร์ฟเวอร์เดิมตอบ `0x1FB2` ด้วยเฟรมสั่งเปิดหน้ารายงาน (opcode ยังไม่รู้ — `RE-234` พิสูจน์แค่ว่า *response ของ TriggerVital เอง* เป็น no-op ไม่ได้ปิดเฟรมชนิดอื่น) (ข) `AddSurveyData` ไม่ใช่ตัวเปิดหน้านี้ · **ห้ามเขียนโค้ดตามสมมติฐานใดก่อนผล**
> `M2_OBSERVED_ISLAND_TRIGGER_IDS` ยัง log-only ตามเดิม ไม่มีอะไรเปลี่ยนในโค้ดจากการแก้หัวใบนี้

> ~~**ปิดยังไง (ข้อความเดิม 2026-09-05T12:0x คงไว้ทั้งก้อน ห้ามลบ)**~~ — อ่านต่อได้ข้างล่าง ขีดฆ่าเฉพาะข้อสรุป ไม่ใช่หลักฐาน:

> **ปิดยังไง**: ชั้น ① STATIC (AddSurveyData → proximity ≤500 → local prompt → confirm ส่ง `EnterInstance` body `12 <u16> 0B 06`) ยืนตามผลเดิม (`notes_to_chief/20260904_0724_RE-227-RESULT-*.md`) และ**เป็นกลไกที่ขึ้น main แล้วจริง**: `world_m2_provisioning_trial.py`/`navigationex_survey_record.py` (PR เซิร์ฟเวอร์ `#753`/`#760`/`#797`/`#810`, ล่าสุด `RE-256` ปิด outer-presence byte) — `GT-233` READY รอเครื่อง Panya ยืนยัน E2E บนจอ
> ชั้น ② (ทาบกับสาย) ของคำถามเดิม**เปลี่ยนรูปคำถาม ไม่ใช่ปิดตามเกณฑ์เดิมที่ตั้งไว้แต่แรก** — เกณฑ์เดิมสมมติว่า `TriggerVital 0x1FB2` (id `153`/`154`) อาจเป็นอีกเส้นทางยืนยัน สมมติฐานย่อยนั้นถูกแยกเป็นใบ `RE-234` ไปแล้วตั้งแต่รอบ `0foax0` และตอนนี้ `RE-234` กลับผลแล้ว (`notes_to_chief/20260904_1953_RE-234-RESULT-*.md`, DONE/MIXED): (ก) `GT-228`/R308 (`notes_to_chief/20260904_1331_KA1A-R308-RESULTS-*.md`) วัดว่าเรือชนเกาะจริงยิง `TriggerVital` id **`2`**(Prison Exile)/**`3`**(Spice Paradise) — **ไม่ใช่** `153`/`154` ตามที่ใบนี้เดาไว้แต่แรก (ก) ถูกหักล้าง (ข) `RE-234` พิสูจน์ static ว่า natural handler ของ `TriggerVital` response เป็น **success no-op ห้าไบต์** ไม่เปิดหน้าต่างอะไรเลย ⇒ เส้นทางคู่แข่งที่ใบนี้เปิดค้างไว้ (`0x1FB2` response) **ไม่ใช่กลไกจริง** ยืนยันซ้ำว่ามีทางเดียวคือ AddSurveyData
> ⇒ ~~**CANCELLED (secondary hypothesis) / DONE (primary hypothesis, shipped)**~~ **ขีดฆ่า 2026-09-05 รอบ `ihjytc`** — ครึ่ง secondary (`covered by RE-234`) ยังยืน · ครึ่ง primary กลายเป็น **REFUTED-ON-SCREEN** ตามหัวใบข้างบน · ~~เหลือเฉพาะการยืนยัน on-screen ซึ่งเป็นของ `GT-233`~~ การยืนยันนั้นเกิดขึ้นแล้วและ**ให้ผลลบ** (R318)

## 🔬 RE-227 CAPTAIN-REPORT-ON-ISLAND-CONTACT-001 [⚫ **SUPERSEDED-BY: ก้อน `REFUTED-ON-SCREEN` ด้านบน -- ไม่ใช่ใบเปิด อย่าหยิบไปรัน** · ยุบโดย LANE-A (เจ้าของใบ) รอบ `qvdk7n` 2026-09-07T10:22+07:00 ตามคำขอ `notes_to_chief/20260907_0925_LANE-K-TO-A-re227-re234-collapse-your-duplicate-blocks.md` และ `COO-DECISION 20260907_0845` ข้อ 3 · **แก้เฉพาะบรรทัดหัวใบ เนื้อใบข้างล่างคงไว้คำต่อคำเป็นบันทึก ไม่ลบหลักฐาน** · ถ้อยคำเดิมของหัวก้อนนี้: `PARTIAL -- ยังไม่ปิด (OPEN) · ร่างโดย LANE-A รอบ xv20xj · [STATIC-ON-BRIDGE]`]
> 🔴 **ก้อนนี้ถูกแทนที่ — ดูก้อน `REFUTED-ON-SCREEN` ด้านบน (บรรทัด 667) · อย่าหยิบไปรัน** [บรรทัดชี้ทางวางโดย LANE-K รอบ `ek1gk9` 2026-09-07T09:5x+07:00 ตาม `COO-DECISION 20260907_0845` ข้อ 3 (เอาข้อ (ก))] · K **ไม่ได้ยุบ ไม่ได้ลบ ไม่ได้แก้เนื้อใบ** — เนื้อใบเป็นของเจ้าของใบ (LANE-A) · จดหมายผลที่ปิดใบนี้: `notes_to_chief/20260904_0724_RE-227-RESULT-NAVIGATIONEX-STATIC-CAPTURE-PENDING.md` · 🔴 RE runner: หัวใบก้อนนี้ยังเขียนว่า OPEN แต่ **ไม่ใช่สถานะปัจจุบันของใบ** — หยิบไปรันคือทำงานซ้ำ

> 🟡 **สถานะ 2026-09-04T07:24+07:00 (กรอกโดย chief รอบ `8nh6q5`/R334 ตาม `COO-DECISION 20260904_0746` ข้อ 2 · ถ้อยคำตามที่ runner เขียนท้ายใบ ไม่แก้)**
>
> `RE-227 PARTIAL — STATIC PASS: NavigationEx AddSurveyData -> client proximity <=500 -> local prompt -> confirm sends EnterInstance body 12 <opaque-u16> 0B 06; CAPTURE/GT-228 REQUIRED FOR ACTUAL WIRE + SCENE-CHANGE JOIN`
>
> - จดหมายผลเต็ม: `notes_to_chief/20260904_0724_RE-227-RESULT-NAVIGATIONEX-STATIC-CAPTURE-PENDING.md` (มี span_sha256 ครบทุกสแปน + nonclaim 7 ข้อ)
> - **ปิดได้ครึ่งเดียว = ชั้น ① สถิต** · ชั้น ② (ทาบกับสาย) ยังค้าง ⇒ **ใบยังเปิด ห้ามใครยกใบนี้ไปเป็นฐานของใบอื่นแบบปิดแล้ว**
> - 🔴 **ห้าม runner rerun ใบนี้จนกว่าจะมีผล `GT-228`** (หรือ chief แก้ objective อย่างมีสาระ) — เพดานเป็น method/cross-layer ไม่ใช่ time checkpoint
> - 🔴 **ครึ่ง (ก) ของคำถามเดิมถูกหักล้างแล้ว**: contact branch ของ NavigationEx docking tick **ไม่ส่ง** `TriggerVital 0x1FB2` · เส้นทางจริงคือเซิร์ฟเวอร์ provision `NavigationEx_AddSurveyDataVtial` (byte `+0x10`=1 · u16 opaque `+0x12` · XYZ f32) แล้วไคลเอนต์เช็กระยะ `<=500` เองในเครื่อง · **ฝั่งเราไม่เคยส่ง record นี้ = เหตุที่หน้าต่างไม่เด้งบน R307** · `0x1FB2` ลดเป็นสมมติฐานรอง (nonclaim 1 ของ runner ยังเปิด ไม่ใช่การตัดทิ้ง)
> - route tag เดิมไม่มีในหัวใบ (runner ขอไว้ในจดหมายผล ข้อ `route note`) ⇒ เติม `[STATIC-ON-BRIDGE]` รอบนี้

> 🔢 **เลขใบตั้งโดย chief (LANE-E) รอบ `3kwnnr`/R332 2026-09-04T05:2x+07:00 ตาม `COO-DECISION 20260904_0344` ข้อ 3** — ตัวนับร่วมสองคิว + archive คืน `226` (ใบ `GT-226` ของรอบเดียวกัน) ⇒ ใบนี้ `RE-227` · `RE-227` = 0 hit ทั้งสามที่ก่อนวาง · เนื้อใบวางทั้งก้อนตามที่ LANE-A ร่าง ไม่แก้ถ้อยคำใด ๆ นอกจากเติมเลขใบ · **เจ้าของใบและผู้บริโภคผล = LANE-A**


- **ถาม (สองข้อ ข้อเดียวกันคนละครึ่ง)**
  - **(ก) ขาออกจากไคลเอนต์**: ตอนเรือ **ชน/เข้าเขตเกาะ** (ไม่ใช่คลิก — เจ้าของยืนยันสด `0409`)
    ไคลเอนต์ส่งอะไร · เป็น `TriggerVital 0x1FB2` ที่ถือ **trigger id ของแถวเกาะ** (`153` Prison Exile Island ·
    `154` Spice Paradise Island — ที่มาของเลขสองตัวนี้อยู่ข้างล่าง) หรือเป็น opcode อื่นทั้งดุ้น
    หรือไม่ส่งอะไรเลยและหน้าต่างเป็นของไคลเอนต์ล้วน (เช็คระยะเอง ไม่มีไบต์ออกจนกด "ยืนยัน")
  - **(ข) ขาเข้าจากเซิร์ฟเวอร์ + ขายืนยัน**: เฟรมไหนเปิดหน้า "รายงานกัปตัน เรือเทียบท่า [ชื่อเกาะ]" ·
    ปุ่ม "ยืนยัน" ส่งไบต์อะไรกลับ · เฟรมไหนทำให้ฉากเปลี่ยนจริง (เป็น `TeleportVital` เดิมหรือคนละตัว)

- **ทำไมใบนี้แคบกว่าที่เคยขอ (`RE-086`/`RE-087` ปิดไปแล้วเมื่อ 27 ส.ค.)**
  เพราะรอบนี้ตัดสองกิ่งทิ้งแล้ว: (1) "ผู้เล่นคลิกเกาะ" ตัดออกทั้งกิ่งจากคำเจ้าของ ·
  (2) "id ไหนคือเกาะ" ตอบแล้วจากตารางที่คอมมิต ไม่ต้องเปิดอิมเมจเพื่อหาเลข
  เหลือคำถามเดียวจริง ๆ คือ **รูปเฟรม** ไม่ใช่ "กลไกคืออะไร"

- **เลข `153`/`154` มาจากไหน (grade A · ทำซ้ำได้ ไม่ต้องมีอิมเมจ)**
  `gamedata/tables/TEXTDATA_TH__Trigger_TIP.tsv` แถว **152-167 เป็นบล็อกปลายทางการเดินทางติดกันทั้งบล็อก**
  แยกจาก prop รอบข้างด้วยสามอย่างพร้อมกัน:
  1. **ชื่อ** ตรงตัวอักษรกับ `s_SCENE_NAME` ใน `TEXTDATA_TH__SCENE_NAME_TIP.tsv` และเรียงตามลำดับฉาก
     (152 Port Royal · 153 Prison Exile Island · 154 Spice Paradise Island · 155 Slave Market Island · … 161 Hell Volcanic Island)
  2. **เพดานเลเวล** ในข้อความ tip เท่ากับ `n_SCENE_LV` ของแถวฉากเดียวกันใน `CONSTDATA_TH__SCENE_NAME.tsv`
     **ครบ 10 แถว** (0/0/25/45/60/70/81/86/92/100) — สองตารางคนละชุดตรงกันสิบตัวเลข
  3. **ไม่มีคำกริยาใช้งาน** — 148/149/150/151 ข้างบน และ 169-175 ข้างล่าง เขียน `[วิธีใช้: ดับเบิ้ลคลิกซ้าย]` ทุกแถว
     บล็อก 152-167 **ไม่มีสักแถว** มีแต่เงื่อนไขเลเวล ⇒ เข้ากับ "ชนแล้วเด้งเอง ไม่ต้องคลิก"
  คำสั่งทำซ้ำ: `awk -F'\t' 'NR>1 && $1>=148 && $1<=175 {print $1"\t"$2"\t|"$3"|"}' gamedata/tables/TEXTDATA_TH__Trigger_TIP.tsv`

- **สิ่งที่ยังไม่ใช่หลักฐาน (nonclaim บังคับของใบนี้)**
  ไม่เคยมีใครเห็นไบต์ของเฟรม `0x1FB2` ที่ถือ id `153` หรือ `154` เลยสักครั้ง · 5 เฟรมที่ R307 จับได้ถือ id
  40/51/3/57/36 ซึ่งเป็น prop ทั้งห้า · ข้อ 3 ข้างบนเป็น **ความเข้ากันได้ ไม่ใช่การพิสูจน์** ·
  ห้ามใบนี้หรือใครอ้างว่า "`0x1FB2` คือเฟรมเทียบท่า" จนกว่าจะมี hex + `span_sha256`

- **อิมเมจที่ต้องยึด (ถ้าตอบด้วย static RE)**
  `GameClient.local.bin` 14,759,424 ไบต์ sha256 `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`
  ทางเข้าที่แนะนำ: ตัวอ่าน/ตัวเขียน `TriggerVital 0x1FB2` ใน `external/PF_PROTOCOL_REGISTRY.tsv` ·
  แล้วไล่ไปที่หน้าต่างที่ใช้สตริง "รายงานกัปตัน"/"เทียบท่า" ใน `TEXTDATA_TH__UI_MESSAGE.tsv`

- **เกณฑ์ปิดสองชั้น**
  ① **สถิต**: ลำดับ tag ของเฟรม (ก) และ (ข) ครบทุกฟิลด์ พร้อม `span_sha256` ของสแปนที่อ่าน (`RE_STATIC_SEARCH_RULES.md` §1)
  ② **ทาบกับสาย**: hex จริงจากใบ capture ของรอบเดียวกัน (ใบ capture ที่ผมร่างคู่กันมา) ตรงกับรูปเฟรมของ ① ทุกไบต์
  🔴 ปิดด้วยชั้นเดียวไม่ได้ · ตอบได้ครึ่งเดียวให้ปิดแบบ **bounded** และระบุว่าอีกครึ่งค้างอยู่ที่ไหน

- **ทางลัดที่ถูกกว่า และควรลองก่อนเปิดอิมเมจ**
  log-only responder ของรอบนี้ (`lane_hooks/lane_a_island_trigger_log.py`, PR เซิร์ฟเวอร์รอบ `xv20xj`)
  พิมพ์ trigger id + ชื่อจากตารางทุกเฟรม `0x1FB2` ที่เข้ามา และพิมพ์คำว่า `ISLAND` เมื่อ id ตรงแถวเกาะ
  ⇒ **ถ้าใบ capture ได้บรรทัด `LANE_A_TRIGGER_VITAL id=153 name=Prison Exile Island ISLAND` มาใบเดียว
  ครึ่ง (ก) ของใบนี้ปิดทันทีโดยไม่ต้องเปิดอิมเมจ** เหลือแต่ครึ่ง (ข)
  🔴 responder ตัวนั้น **ยังไม่ถูกเรียก** จนกว่า chief จะวางจุดยิงหนึ่งบรรทัด (CORE-REQUEST ในใบ PR รอบนี้)

- **ผู้ทำ**: chief มอบหมาย (สายเดียว ห้ามเขียน "X หรือ Y") · ผลกลับมาถึง **LANE-A** แล้วผมสร้าง responder จริงในรอบที่ผลถึง

---

## 🔬 RE-234 CLIENT-RESPONSE-PATH-FOR-TRIGGERVITAL-1FB2-ISLAND-001 [🔵 **DONE / MIXED PASS + BOUNDED-NEGATIVE — ปิดโดย LANE-A รอบ `2mnd7b` 2026-09-05T12:0x+07:00**]

> ผล: `notes_to_chief/20260904_1953_RE-234-RESULT-TRIGGERVITAL-NOOP-ID-ONLY-UNSAFE.md` (repro verifier ~~`pf_bridge/staged/re234_static_verify.py` PASS 18/18~~ — **ถอนการอ้าง 2026-09-07 โดย LANE-K รอบ `okh8oz` ดูบรรทัดถัดไป**)
> 🔴 **ถอนหลักฐานหนึ่งชิ้น — ไม่ใช่ถอนข้อสรุป** ตามคำขอเจ้าของใบ `notes_to_chief/20260907_0722_LANE-A-TO-K-re234-result-cites-a-file-git-never-saw.md`: บรรทัดที่ 9 ของใบผลอ้าง `staged/re234_static_verify.py` พร้อม SHA-256 `e54989a6…` แต่ **ไฟล์นั้นไม่มีในรีโป** · K วัดเองรอบนี้: `git ls-tree -r --name-only origin/main | grep -c re234_static_verify` = **0 hit ทั้งสองรีโป** (`pf_bridge` main `3de72a1` · `pirate-force-server` main `736535f`) · โคลนคลาวด์เป็น shallow จึงยืนยันได้แค่ "ไม่อยู่บน main ปัจจุบัน" ไม่ใช่ "ไม่เคยมี" ⇒ **หลักฐานส่วน repro verifier ไม่มี artifact ที่ commit แล้วรองรับ** · คำต่อคำจากเจ้าของใบ: "ข้อสรุปหลักของ `RE-234` ข้อ (3) — 'id อย่างเดียวเป็น classifier ที่ไม่ปลอดภัย' — ยังยืนอยู่โดยไม่ต้องพึ่งบรรทัดนี้เลย" ⇒ ข้อ (1)(2)(3) ข้างล่าง **ไม่เปลี่ยนสถานะแม้หนึ่งตัว** · ต้นฉบับจดหมายผลไม่ถูกแก้ (จดหมายเป็นบันทึกของผู้เขียน ไม่ใช่เขตของ K) — มีสำเนาคำเตือนข้างตัวจดหมายที่ `notes_to_chief/20260904_1953_RE-234-RESULT-TRIGGERVITAL-NOOP-ID-ONLY-UNSAFE.md.LANEK-RETRACTION.txt`
> **(1)** natural handler ของ `TriggerVital` response = `[0x00710440,0x00710445)` **success no-op ห้าไบต์** (`B0 01 C2 04 00`) — ไม่อ่าน ไม่เปิด UI ไม่มีผลบนจอ
> **(2)** ของสองเส้นทางที่ใบนี้ถาม มีทางเดียวที่พิสูจน์ว่าเปิดหน้ารายงานกัปตันได้จริง = **AddSurveyData + proximity ≤500** (`RE-227`) · `TriggerVital` response **ไม่ใช่** เส้นทางนั้น (พิสูจน์แล้วจากข้อ 1)
> **(3) BOUNDED-NEGATIVE**: พิสูจน์ไม่ได้ว่า `TriggerVital` id `2`/`3` เป็น namespace เดียวกับ `TEXTDATA_TH__Trigger_TIP` (~~`GT-228` เห็น id `3` ทั้งตอนชนเกาะและตอนแล่นเรือปกติ~~ 🔴 **ประโยคในวงเล็บนี้ถูกหักล้าง 2026-09-07T13:32+07:00** ตาม `notes_to_chief/20260907_1245_COO-DECISION-a1152-re234-item3-refuted-LANE-K.md` และ **LANE-K วัดซ้ำเองบนใบผลต้นทาง** `notes_to_chief/20260904_1331_KA1A-R308-RESULTS-gt228-pass-box-B-island-contact-fires-triggervital-id-2-at-prison-exile-and-id-3-at-spice-paradise-not-153-154.md` **บรรทัด 25** (เฟรม `0x1FB2` ทั้ง session = 6 เฟรม: `rx112 13:08:52 id=35` *แล่นเข้าหาเกาะ 2 ยังไม่แตะ* · `rx130`/`rx152`/`rx248 id=2` · `rx433`/`rx491 id=3`) และ **บรรทัด 35** (`LANE_A_TRIGGER_VITAL id=35 name=Thorn Flower PROP no_responder bytes_out=0`) ⇒ **ใน `GT-228` ไม่มี id 3 ตอนน้ำเปล่าเลยสักครั้ง** เฟรมน้ำเปล่าคือ id 35 · 🟡 **แต่ข้อสรุปของข้อ (3) ไม่ได้ตกไปด้วย และ K ไม่ได้ถอนมัน**: แหล่งของ *id 3 นอกบริบทชนเกาะ* คือ **R307 ไม่ใช่ `GT-228`* — `notes_to_chief/20260903_1901_KA1A-R307-RESULTS-gt215-220-214-192-200-217-213-pass-gt187-no-result-with-eight-new-findings-class-drop-lifetime-atlantis-dock-trigger.md` **บรรทัด 90** คำต่อคำ: `trigger ids seen: 40, 51, 3, 57, 36` ระหว่างแล่นใกล้เกาะ โดยเซิร์ฟเวอร์ไม่ตอบเลย (5 sent, 0 answered) · เนื้อใบ `RE-234` ข้อ (3) ข้างล่างเองก็เขียนว่า *"R307's real id=3 capture during ordinary sailing"* ⇒ ที่ผิดคือ **การอ้างใบ** ไม่ใช่ข้อเท็จจริงที่อยู่ข้างหลัง [แก้โดย LANE-K รอบ `du6wre` · การอ้าง R307 บรรทัด 90 เป็นสิ่งที่ **K ค้นเพิ่มเอง ไม่ได้อยู่ในคำสั่ง COO `1245`** — แจ้ง COO ในจดหมายรอบแล้ว]) ⇒ `lane_hooks/lane_a_island_trigger_log.py`'s `M2_OBSERVED_ISLAND_TRIGGER_IDS` **เป็น log-only, ไม่มี BUILD_IMPACT ต่อ production** แต่ถือเป็นตัวจำแนกที่ไม่ปลอดภัยถ้าใครเอาไปใช้ตัดสินโลก — บันทึกเป็นงานสำรอง (แคบ scope ด้วย scene/context ก่อนใช้อ้างอิงเกาะ) ยังไม่ทำรอบนี้ (ไม่บล็อกอะไร)
> ปิด `RE-227` ในรอบเดียวกันโดยอ้างผลนี้ (ดูหัวใบ `RE-227` ด้านบน)

## 🔬 RE-234 CLIENT-RESPONSE-PATH-FOR-TRIGGERVITAL-1FB2-ISLAND-001  [⚫ **SUPERSEDED-BY: ก้อน `DONE / MIXED` ด้านบน -- ไม่ใช่ใบเปิด อย่าหยิบไปรัน** · ยุบโดย LANE-A (เจ้าของใบ) รอบ `qvdk7n` 2026-09-07T10:22+07:00 ตามคำขอ `notes_to_chief/20260907_0925_LANE-K-TO-A-re227-re234-collapse-your-duplicate-blocks.md` และ `COO-DECISION 20260907_0845` ข้อ 3 · **แก้เฉพาะบรรทัดหัวใบ เนื้อใบข้างล่างคงไว้คำต่อคำเป็นบันทึก ไม่ลบหลักฐาน** · ถ้อยคำเดิมของหัวก้อนนี้: `OPEN -- [STATIC-ON-BRIDGE] · เจ้าของใบ/ผู้เขียนเนื้อใบ = LANE-A · ผู้บริโภคผล = LANE-A`]
> 🔴 **ก้อนนี้ถูกแทนที่ — ดูก้อน `DONE / MIXED` ด้านบน (บรรทัด 752) · อย่าหยิบไปรัน** [บรรทัดชี้ทางวางโดย LANE-K รอบ `ek1gk9` 2026-09-07T09:5x+07:00 ตาม `COO-DECISION 20260907_0845` ข้อ 3 (เอาข้อ (ก))] · K **ไม่ได้ยุบ ไม่ได้ลบ ไม่ได้แก้เนื้อใบ** — เนื้อใบเป็นของเจ้าของใบ (LANE-A) · จดหมายผลที่ปิดใบนี้: `notes_to_chief/20260904_1953_RE-234-RESULT-TRIGGERVITAL-NOOP-ID-ONLY-UNSAFE.md` · 🔴 ดูการถอนหลักฐานที่ก้อนบนด้วย (`notes_to_chief/20260907_0722_LANE-A-TO-K-re234-result-cites-a-file-git-never-saw.md`) · RE runner: หัวใบก้อนนี้ยังเขียนว่า OPEN แต่ **ไม่ใช่สถานะปัจจุบันของใบ** — หยิบไปรันคือทำงานซ้ำ

> 🔢 **เลขใบตั้งโดย chief (LANE-E) รอบ `wjqykr`/R338 2026-09-04T14:0x+07:00** ตาม `COO-DECISION 20260904_1345` ข้อ 3(ง) และ `20260904_1346` ข้อ 2(จ) · ตัวนับร่วมสองคิวคืน `233` (`GT-233` รอบเดียวกัน) ⇒ ใบนี้ `234` · `RE-234`/`GT-234` = **0 hit ทั้งสามที่ก่อนวาง**
> **เนื้อใบเติมแล้วโดย LANE-A รอบ `0foax0` 2026-09-04T18:1x+07:00** (ข้อ 3 เพิ่มใหม่จากงานรอบนี้) · ใบนี้ **แทน** `0343` ข้อ 3 ฉบับเดิมที่ไล่จาก id 153/154 — คำทำนาย 153/154 ตกไปแล้วตาม `GT-228` ห้ามอ้างต่อ

- **คำถาม (ฉบับแคบ)**: (1) ไคลเอนต์ทำอะไรกับ **response** ของ `TriggerVital 0x1FB2` id 2/3 — มี handler ที่อ่านคำตอบของเซิร์ฟเวอร์ไหม หรือเป็นการแจ้งทางเดียว (2) เส้นทางที่เปิดหน้า "รายงานกัปตัน" มีกี่ทาง — `AddSurveyData` + เช็กระยะ ≤500 ในเครื่อง (สมมติฐานหลักตาม `RE-227`) เทียบกับ response ของ `0x1FB2` (ทางสำรอง) (3) [เพิ่ม LANE-A `0foax0`] id 2/3 ใน `TriggerVital` เป็น namespace เดียวกับ `TEXTDATA_TH__Trigger_TIP` (แถว 2 "Edmund Hidden Treasure" / แถว 3 "Seafood Cargo", R307's real id=3 capture during ordinary sailing) จริงไหม หรือคนละช่องเลขที่บังเอิญชนกัน — ถ้าคนละ namespace, `lane_hooks/lane_a_island_trigger_log.py`'s `M2_OBSERVED_ISLAND_TRIGGER_IDS` override ต้องแคบลง (เช่น กรองด้วย scene_id/context ที่ยิง แทนการจับคู่ id เปล่า ๆ)
- **ทำไม**: ถ้า `GT-233` ไม่เด้ง ใบนี้คือทางเดียวที่บอกว่ากลไกผิดที่ provisioning หรือผิดที่การไม่ตอบ trigger · ข้อ 3 ทำไม: ตอนนี้ responder log-only พิมพ์ ISLAND ผิดให้เฟรม Seafood Cargo ของจริง (R307) เป็นความเสี่ยงที่ยอมรับไว้ชั่วคราว ไม่ใช่ถาวร
- **route**: `STATIC-ON-BRIDGE` (ต้องดิสแอสเซมภาพไคลเอนต์ ทำบนคลาวด์ไม่ได้)
- **ห้ามอ้าง**: ชื่อ prop ใน `TEXTDATA_TH__Trigger_TIP` เป็นคนละ namespace จนกว่าจะพิสูจน์ตรงข้าม (`COO 1345` ข้อ 1)
- **ลิงก์**: `pirate-force-server#753` (โค้ดที่ใบนี้จะตัดสิน) · `20260904_1331_KA1A-R308-RESULTS-*` · `20260904_1345_COO-DECISION-*`

---

## 🔬 RE-248 SELECTACTOR-0x5DFF60-TWO-U16-TAG-0x12-WHICH-IS-SCENE-001  [🔧 **PASS/DONE — พับโดย LANE-K รอบ `ek1gk9` 2026-09-07T09:5x+07:00** คำต่อคำจากหัวจดหมายผล `notes_to_chief/20260905_0053_RE-248-RESULT-FIELD-A-IS-SCENE-FIELD-B-IS-LEVEL.md` (RE runner local 2026-09-05T00:53+07:00): “PASS/DONE: FIELD_A (`+0x20`) = scene id; FIELD_B (`+0x22`) = character level” · K คัดลอกคำของผู้เทส **ไม่ได้ตัดสินเอง** และไม่ได้แตะเนื้อใบ · 🟠 บันทึกเดิมก่อนพับ (ไม่ลบ): 🟠 **OPEN** -- 🔴 `[STATIC-ON-BRIDGE]` (ต้องเปิด client image = เครื่อง Panya) · เลขใบตั้งโดย chief (LANE-E) รอบ `epkucn`/R344 ตาม `LANE-DB-ASK-CHIEF 20260904_2212` + `COO-DECISION 20260904_2152` ข้อ 3 (อนุมัติ RE ใบแคบ **ยกเว้นข้อห้าม "ห้ามเปิด RE ก่อน" ของ `1947` ใบนี้ใบเดียว**) · ผู้ทำ = **ka1-A / RE runner (local)** · **ผู้บริโภคผล = LANE-DB** · ใบ GT คู่ของมันมีเลขแล้ว = `GT-245` (`COO 20260904_1948` ข้อ 3) จึงครบกติกา RE->GT ของ `2142` ข้อ 3]

> 🔢 ตัวนับร่วมสองคิว + `archive/*QUEUE*ARCHIVE*` คืนสูงสุดที่ `247` (`GT-247`, วางรอบเดียวกัน) => ใบนี้ `248` · `RE-248`/`GT-248` = 0 hit ทั้งสามที่ก่อนวาง

## คำถามเดียว (ถ้อยคำตาม `COO 2152` ข้อ 3)
> serializer `0x5DFF60` (`SelectActorVital`/`CreateActorVital` -- ชื่อเดียวกันตามคอมเมนต์ `get_preset_actor_wire()` ใน `current/pf_login_game_server_v141.py`) เขียน `u16 tag 0x12` **สองตัวนี้** จากตัวแปรชื่ออะไร และหน้าเลือกตัวละครอ่าน**ตัวไหน**ไปพิมพ์ชื่อฉาก

## ค้นก่อนถอด (ผู้ทำต้องกรอกในผล ห้ามเว้น)
- `external/00_SEARCH_HERE_FIRST.md` -> grep `SelectActorVital` / `0x5DFF60` ใน `external/PF_SERIALIZER_FIELDS.tsv` **ทำแล้วโดย LANE-DB (`2212` §0.5)**: เจอสองแถวตรงโครงสร้าง -- `order 17` tag `0x12` `field_offset DEREF(DEREF(STACK@0x005EBAE0+0x18)+0x10)+0x20` len 2 · `order 18` เหมือนกันที่ `+0x22` · span `[0x005DFF60,0x005E01C6)` · sha256 `de9de2a04f4ac3ec8e6c07550336eea2be18954143c5c0de1823a4a2171e3f8a` · **ตารางนี้ไม่บอกชื่อตัวแปร/ความหมาย** (`formal_reaching_def` มีแค่ `self`/`edi` ไม่ใช่ payload) => คำถามยังเปิดจริง
- `notes_to_chief/reference_codex_attr/` (README ก่อนเสมอ) -- แถวใดแตะ `+0x20`/`+0x22` ของ actor wire ให้ยกมาพร้อมคอลัมน์ `nonclaim`
- capture: `archive/stray_captures_20260819/` มีไฟล์เดียวที่มี `CreateActorVital` และค่าทั้งคู่เท่ากัน => **ไขว้ไม่ได้จาก capture ที่มี** (LANE-DB ตรวจแล้ว)

## เกณฑ์ปิดใบ (ชั้นเดียว -- static IMAGE เท่านั้น ไม่มีชั้น client-observable)
- ปิด **PASS** ได้เมื่อ: ชี้ได้ว่า `+0x20` หรือ `+0x22` ตัวใดถูก **อ่าน** โดยเส้นทางที่พิมพ์ชื่อฉากในหน้าเลือกตัวละคร พร้อม VA ของจุดอ่าน + ชื่อ/ที่มาของตัวแปรต้นทางที่จุดเขียน + `image_sha256`
- ปิด **BOUNDED-NEGATIVE** ได้เมื่อ: เดินสายอ่านครบแล้วยังแยกไม่ออก -- ต้องระบุว่าเส้นทางตันที่ VA ใด และอะไรจะปลดล็อกได้ (capture ชนิดไหน)

## ใบนี้ไม่ขอ
ไม่ขอความหมายของฟิลด์อื่นในโครงสร้างเดียวกัน · ไม่ขอ `astr`/`wstr` · ไม่ขอค่าที่ถูกต้องของ scene id ใด ๆ · ไม่ขอให้แตะโค้ด

## ห้ามสรุปสิ่งเหล่านี้ (กติกาหลักฐาน)
- 🔴 ห้ามสรุปจากตัวอย่างเดียวที่มี (`get_preset_actor_wire()` สร้างที่ Port Royal เสมอ ค่าทั้งคู่ = `1`) -- G1/G6
- 🔴 ห้ามอ้าง `external/PF_SERIALIZER_FIELDS.tsv` ว่าตอบใบนี้แล้ว (มันยืนยันตำแหน่ง ไม่ใช่ความหมาย -- คำเตือนของตารางเอง)
- 🔴 ผลของ Codex เป็นหลักฐานชั้น IMAGE ห้ามยกเป็น client-observable (§14 ข้อ 13 ก/ข)

## แยกจากใบไหน
`RE-119` (ปิดแล้ว) ให้โครงสร้าง actor wire -- ใบนี้ถามเฉพาะว่าฟิลด์ไหนในสองตัวคือ scene · `GT-245` คือใบ attended ที่รอผลนี้ (หน้าเลือกตัวแสดงฉากจริง)

## ถ้าผลออกทางลบ
`SCENE_FIELD` ใน `src/pirateforce_foundation/persistence_scene_field_patch.py` **คงค่า `None` ต่อไป** (ไบต์ออกเท่าเดิมทุกไบต์) และ `GT-245` ยัง BLOCKED -- ห้ามใครเดาฟิลด์เพื่อปลดใบ

## ผลไปถึงใคร
จดหมายผลจ่าหน้า **LANE-DB** (cc chief, COO) · LANE-DB บริโภคเองและปิดหัวใบนี้ในรอบของตัวเอง (§5 "ใครเปิดใบคนนั้นบริโภค" -- chief ตั้งเลขให้ แต่เจ้าของเนื้อคือ DB) · แก้ `SCENE_FIELD` เป็น `FIELD_A`/`FIELD_B` บรรทัดเดียว

---

## 🔬 RE-256 ADDSURVEYDATA-OUTER-PRESENCE-BYTE-VALUE-001  [✅ **DONE -- ตอบแล้ว 2026-09-05 10:07 +07:00** · ปิดหัวโดย chief (LANE-E) รอบ `pv4zg1`/R352 ตามใบผล `notes_to_chief/20260905_1007_RE-256-RESULT-PRESENCE-ONE-SINGLE-RECORD-VERSION-ZERO.md` · คำตอบ: outer byte tag `0x0B` = **pointer-presence boolean** (`cmp dword ptr [esi+0x14],0` / `setne al` ที่ `0x00733586-0x0073358E`) ⇒ หนึ่ง record = `0B 01` · ไม่มี record = `0B 00` · **ไม่ใช่ record count** · `vital_version` ของคลาสนี้ต้องเป็น `0` แบบ exact equality (`0x005F3EFC/0x005F3F01`) · BUILD_IMPACT ลงโค้ดแล้วโดย LANE-A รอบ `vwekfq` = server `#810` (`c3454949`) บน main `b49a4e45` [วัดแล้ว `--is-ancestor` exit 0 · chief `pv4zg1`] · ผู้บริโภคผล = LANE-A (บริโภคแล้ว) ⇒ `GT-233` ปลดหัวเป็น READY ในรอบเดียวกัน · เดิม: 🟠 **OPEN** -- 🔴 `[STATIC-ON-BRIDGE]` (ต้องเปิด client image = RE runner บนเครื่อง Panya · LANE-A บนคลาวด์ไม่มีไบนารี `LANE-A 0435` · `COO-DECISION 20260905_0645` รับทาง 2) · เลขใบตั้งโดย chief (LANE-E) รอบ `rs8uyz`/R350 ตาม `LANE-A-RE-TICKET 20260905_0430` (ฉบับแก้ทับ 05:15 หลัง pf-adversary) + `COO-DECISION 20260905_0645`/`0646` · ผู้ทำ = **RE runner (local)** สายเดียว · **เจ้าของใบ/ผู้บริโภคผล = LANE-A** · ตัวบล็อกของ `GT-233` (BLOCKED-ON-LAYOUT) และของบันได **M2**]

> 🔢 ตัวนับร่วมสองคิว + `archive/*QUEUE*ARCHIVE*` คืนสูงสุดที่ `255` (`GT-255`) => ใบนี้ `256` · `RE-256`/`GT-256` = 0 hit ทั้งสามที่ก่อนวาง

## ค้นแล้วก่อนเปิดใบ (ผลการ grep -- กติกาใหม่ `AGENTS.md` §7 · `COO 0646` ข้อ 2)
- `external/PF_SERIALIZER_FIELDS.tsv:6377-6388` -- **เจอ** สแปน+SHA ตรงกับที่ `RE-227` อ้าง (`[0x00733570,0x00733614)` · `f8c7510018...af178c`) ให้ **tag/ยาว/gate** ของ presence byte `0x0B` (1 ไบต์ · ALWAYS) แต่ **ไม่ให้ค่า**
- `archive/notes_to_chief_2026-08/20260827_0115_RE-086-RESULT-*` -- **เจอ** ร้อยแก้วตรงกัน: outer serializer ส่ง presence byte แล้วเรียก nested vtable slot `+0x10` (63 คำสั่ง · gap/error 0/0)
- ⇒ **สิ่งที่ค้นเจอถูกตัดออกจากใบนี้แล้ว** ฉบับ 04:30 ถามข้อที่ commit อยู่แล้ว สาย A แก้ทับเอง เหลือเฉพาะข้อที่ยังไม่มีใครวัด

## คำถาม (สี่ข้อ ทั้งหมดตอบด้วย static)
1. **ค่า** ของ presence byte ชั้นนอกเมื่อ collection มี record หนึ่งตัว -- `1` · จำนวน record · หรืออย่างอื่น (ห้ามเดา)
2. ลำดับ **อ่าน** ต่างจากลำดับ **เขียน** ไหม (ตาราง W ให้ไบต์ก่อน call · R ให้ call ก่อนไบต์ เรียงตาม file offset) -- ฟังก์ชันเดียวสองทิศ หรือคนละทาง
3. `CALL 0x0072EC50` และช่อง `INDIRECT(DEREF(DEREF(DEREF(OBJ+0x14))+0x10))` เขียน/อ่านอะไรลงสาย · ตัวไหนคือ nested record serializer `[0x0072e590,0x0072e691)` ที่ `RE-227` พิน · มีอะไรคั่นกลางอีกไหม
4. คลาสนี้อ่าน record ได้กี่ตัวต่อข้อความ และ `vital_version` ที่ผู้อ่านยอมรับคือค่าใด (เราส่ง 0)

## เกณฑ์ปิดใบ (ชั้นเดียว -- static IMAGE เท่านั้น)
ค่า/ลำดับ พร้อม SHA ของสแปนที่อ่าน (recompute ได้) · **bounded-negative รับเป็นคำตอบปิดใบ**: "ค่าไม่ได้ถูกกำหนดตายตัวในโค้ด" ปิดใบได้ แล้ว LANE-A เดินทาง "ลองสองค่า" ในรอบ attended แทน

## ใบนี้ไม่ขอ
ชั้น client-observable ไม่อยู่ในใบนี้ · ห้ามบูตไคลเอนต์เพื่อปิดใบนี้ · ถ้าคำตอบทำให้ตั้งค่าได้ LANE-A จะขอบูตหนึ่งครั้ง**พ่วง** `GT-233` ไม่ใช่บูตแยก

## ห้ามสรุปสิ่งเหล่านี้ (กติกาหลักฐาน)
- `0xC4AF` **มีหลักฐานบนจอหนึ่งชิ้น** (`ErrorData=50351` = id ของคลาสเอง · R313 02:07 · `navigationex_survey_record.py:116-211`) ⇒ **ตั้งต้นว่า `msg_id` ถูก** ใบนี้ไม่ได้เปิดมาตรวจ `msg_id`
  🔴 **แต่ห้ามเขียนว่า "พิสูจน์แล้วสองชั้น"** (แก้ตาม pf-adversary D9 รอบ `rs8uyz`/R350 · ถ้อยคำเดิมของ chief ผิด): ครึ่งที่สองของคู่คือ **เฟรมที่เราส่งเอง** ซึ่งเป็น *ตัวกระตุ้น* ไม่ใช่พยานอิสระ มันขัดกับตัวเองไม่ได้ ⇒ มี **หนึ่งการสังเกต + หนึ่งข้อโต้แย้ง (name hash)** ไม่ใช่สองชั้นตาม G5
  ⇒ ถ้าผลของใบนี้ทำให้สงสัย `msg_id` ขึ้นมาจริง **ให้เขียนมา ไม่ใช่กลืนไว้** · control ที่ยังไม่มีใครรัน = ส่ง id ผิดโดยตั้งใจ แล้วดูว่ากล่อง error ยังขึ้นชื่อคลาสนี้ไหม (ถ้าขึ้น = 50351 ไม่ได้ระบุ id ของเรา)
- ห้ามยก `0306` ("encoder ตรง capture ⇒ layout ไม่ใช่ตัวผิด") เป็นฐาน -- **ถอนแล้ว** (`LANE-A 0555` · adversary D2 · `COO 0645`/`0646` ข้อ 1)
- ห้ามเหมาค่าที่วัดได้จากคลาสอื่นมาใช้กับคลาสนี้ (กฎ PER-CLASS)
- G8: ทุกแถวในผลติดป้าย `[วัดแล้ว]`/`[เสนอ]`

## แยกจากใบไหน
`RE-227` (กลไก provisioning · ยังไม่ถูกหักล้าง) · `RE-086`/`RE-087`/`RE-090` (ผลเดิม commit แล้ว ห้ามขอซ้ำ) · `#797` วางโค้ดรองรับไว้แล้ว (`outer_leading_byte` · `None` = ไบต์เดิมเป๊ะ ไม่มีอะไรบนสายเปลี่ยนจนกว่าใบนี้จะตอบ)

## ถ้าผลออกทางลบ
ปิดเป็น bounded-negative พร้อมระบุว่า static อ่านไม่ได้เพราะอะไร · LANE-A เปิดรอบ attended "ลองสองค่า" พ่วง `GT-233`

## ผลไปถึงใคร
จดหมายผลจ่าหน้า **LANE-A** (cc chief, COO) · LANE-A บริโภคเองและปิดหัวใบนี้ในรอบของตัวเอง (§5 "ใครเปิดใบคนนั้นบริโภค") · ถ้าผลขอ attended capture ⇒ LANE-A เปิดใบ GT ในรอบเดียวกัน (`COO 2142`)

---

---

<!-- CORRECTION, LANE-K round kq7m3d addendum 2026-09-07T18:5x+07:00 (pf-adversary D1): the RE-256 move in this round over-ran its block by six lines and carried the two pointer stubs below in with it, which removed them from CLIENT_RE_QUEUE.md and made RE-260 ungreppable from the queue.  They have been restored to the queue byte-identical.  They are NOT part of the RE-256 block and say nothing about it; they are left here rather than deleted because this lane deletes nothing.  11 items left the queue this round, not 9. -->

- ~~RE-259 UPDATEATTRVITAL-0X309A-IS-IT-EVER-SENT-FOR-CNETNPC-001~~ -> `archive/CLIENT_RE_QUEUE_ARCHIVE_20260907_closed.md` (PASS -- LANE-DB ปิดแล้ว 2026-09-05, ดู pf_bridge/notes_to_chief/202609 ... · ย้ายทั้งก้อนคำต่อคำโดย LANE-K รอบ `spppsd` 2026-09-07T14:22+07:00 · ไม่มีอะไรถูกลบ)

- ~~RE-260 ACTORATTR-0X99-0X9A-CONCRETE-OWNER-CLASS-001~~ -> `archive/CLIENT_RE_QUEUE_ARCHIVE_20260907_closed.md` (DONE -- LANE-DB ปิดแล้ว 2026-09-05, ดู pf_bridge/notes_to_chief/202609 ... · ย้ายทั้งก้อนคำต่อคำโดย LANE-K รอบ `spppsd` 2026-09-07T14:22+07:00 · ไม่มีอะไรถูกลบ)


<!-- moved from CLIENT_RE_QUEUE.md by LANE-K round 0sw9f6 2026-09-07T21:23+07:00 -- seven tickets, verbatim, nothing edited except this note -->

## RE-290 CAVATARNPC-NAMEBOARD-CTOR-SLOT-001  [✅ **PASS / BOUNDED-POSITIVE** — **`PASS / BOUNDED-POSITIVE` เท่านั้นคือคำของผู้ทำคำต่อคำ** (`notes_to_chief/20260907_1027_RE-290-RESULT-cavatarnpc-builds-the-same-nameboardnpc-as-cnetnpc.md` 2026-09-07T10:27+07:00) · **`CLOSED` ไม่ได้อยู่ในจดหมายผล** — เป็นคำขอของ**เจ้าของใบ** LANE-B ข้อ 4.1 (`notes_to_chief/20260907_1046_LANE-B-re290-consumed-gt288-set2-stays.md` "ปิด `RE-290` ในคิว") ⇒ **CLOSED (ตามคำขอเจ้าของใบ ไม่ใช่คำของผู้ทำ)** · พับโดย LANE-K รอบ `wb8tfv` 2026-09-07T11:10+07:00 · เจ้าของใบ LANE-B บริโภคผลแล้ว · 🟠 **[แก้โดย LANE-K รอบ `k01t0u` 2026-09-07T12:15+07:00 หลัง pf-adversary D5]** หัวใบนี้เคยเขียน `CLOSED` และ ~~🔴 **OPEN**~~ ค้างอยู่พร้อมกันในวงเล็บเดียว (รอบ `wb8tfv` เติม `CLOSED` แต่ลืมขีดฆ่า `OPEN` ทั้งที่ทำให้ `RE-222` ในคอมมิตเดียวกัน) ⇒ `grep OPEN` คืนใบนี้ผิด · ขีดฆ่าไว้ไม่ลบ ตามธรรมเนียมบ้าน · และ **`CLOSED` ถูกย้ายออกจากวงเล็บที่เขียนว่า "คำของผู้ทำคำต่อคำ"** เพราะผู้ทำไม่ได้เขียนคำนั้น · 🔺 `[STATIC-ON-BRIDGE]` (อ่านไบนารีไคลเอนต์บนเครื่องสะพาน read-only -- **ไม่ใช่ attended ไม่เปิดเกม ไม่จับ `LOCK_GAME` ไม่กินเวลาเครื่องเจ้าของ** ⇒ ไม่มีบล็อก `ATTENDED:` และไม่ต้องมี `HEADLESS_PROOF:` ตาม `NOW.md` `0159` ซึ่งบังคับเฉพาะใบ attended) · **เจ้าของใบ/ผู้เขียนเนื้อใบ/ผู้บริโภคผล = LANE-B (COMBAT)** · ผู้ทำ = RE runner บนเครื่องสะพาน · ตั้งเลขโดย LANE-K รอบ `rlapyk` 2026-09-07T06:11+07:00 (ภายในรอบที่เห็นคำขอ) · เนื้อใบมาจากจดหมาย `notes_to_chief/20260907_0512_LANE-B-TO-K-re-body-does-cavatarnpc-build-a-name-board.md` คำต่อคำ · ผูกกับ `GT-288` ชุด 2 (ผู้สมัคร `actor_type 5`)]

**`CAvatarNPC` (actor_type 5) สร้างป้ายชื่อหรือเปล่า** · หนึ่งดวอร์ดตอบได้

### grep แล้ว: ไม่เจอ (ตามกฎ "grep ก่อนออกใบ")
- `external/00_SEARCH_HERE_FIRST.md` · `external/PF_PROTOCOL_REGISTRY.tsv` · `external/PF_SERIALIZER_FIELDS.tsv`
- `FACTPACK_L2_CLASSCENSUS001_20260820.tsv` (แถว 214) · `notes_to_chief/reference_codex_attr/`
- `tools/pf_actor_type_dispatch_static.py` · `tools/pf_hp_death_respawn_static.py` · `tools/pf_runtimeres_death_encoder_static.py`
- `reports/PF_MPAUDIT_FOLLOWUP001_ACTOR_TYPE_DISPATCH_STATIC_20260818.md` เอง
**ไม่มีที่ไหนในสองรีโปเก็บค่า `+0x7C` ของ `CAvatarNPC`**

### คำถามเดียว
อ่านหนึ่งดวอร์ด: **`[0xF0DFF8 + 0x7C]`** (`0xF0DFF8` = vtable ของ `CAvatarNPC` ตามรายงานบรรทัด 53)
แล้วบอกว่าเท่ากับอะไร · เทียบกับสองค่าที่รายงานปักไว้แล้วในหัวข้อ 4 (บรรทัด 175-177):
`CNetActor +0x7C = 0x456580` (สร้าง `NameBoardPlayer` ขนาด `0x78`) · `CNetNPC +0x7C = 0x45C560` (สร้าง `NameBoardNPC` ขนาด `0xC0`)

- ถ้า = `0x45C560` ⇒ `CAvatarNPC` ได้ป้ายเดียวกับ 4 ⇒ ผู้สมัคร AT5 ของ `GT-288` ชุด 2 อ่านได้จริง
- ถ้าเป็นค่าอื่น ⇒ บอกด้วยว่าฟังก์ชันนั้นจองกี่ไบต์และเป็นคลาสป้ายอะไร
- ถ้าเป็น 0 / ไม่สร้างอะไร ⇒ **AT5 ไม่มีป้ายชื่อ** ⇒ B ต้องถอนผู้สมัคร actor_type ออกจากชุด 2 ทั้งอัน

### ทำไมถึงต้องรู้ (และทำไมไม่ใช่ใบที่หยุดงาน)
รอบ `b08g3z` เปลี่ยนผู้สมัครจาก 3 เป็น 5 เพราะ 3 **พิสูจน์แล้วว่าไม่สร้างอ็อบเจกต์เลย**
(รายงานบรรทัด 61: `actor_type 3` ถูกปฏิเสธถ้า global `0x1032EC4` ไม่ใช่ศูนย์ ⇒ factory คืน NULL)
5 ดีกว่า 3 แน่นอน แต่ **ยังไม่ได้พิสูจน์ว่ามีป้าย** — บรรทัด 168/170 ที่มักถูกอ้างเป็น **getter** ของชื่อ
ไม่ใช่ตัวสร้างบอร์ด · รายงานบรรทัด 292 พูดเองว่าการเข้าถึง `CAvatarNPC` จากสตรีมฝั่งเซิร์ฟเวอร์ "ยังไม่ได้ trace"
B บันทึกเป็น nonclaim ไว้ตรงที่ค่าคงที่อยู่แล้ว และเดินงานต่อโดยไม่รอ (ตามกฎ "เขียนคำถาม แล้วเดินต่อ")

### ผลกระทบต่อ `GT-288` ถ้าใบนี้ยังไม่ตอบตอนบูต
ผู้เทสต้องได้รับแจ้งในใบว่า **"AT5 ไม่มีป้ายชื่อ" เป็นผลที่เป็นไปได้ และต้องบันทึกเป็นผลนั้น
ห้ามบันทึกเป็น FAIL ของสี** — ไม่งั้นจะได้ FAIL ปลอมแบบเดียวกับที่ AT3 เคยจะให้

nonclaim: ใบนี้เป็นงาน static ล้วน ตอบจาก binary ได้ ไม่ต้องใช้เครื่องเจ้าของ ไม่ต้องบูตเกม

### result:
**PASS / BOUNDED-POSITIVE** — คำต่อคำจาก `notes_to_chief/20260907_1027_RE-290-RESULT-cavatarnpc-builds-the-same-nameboardnpc-as-cnetnpc.md` (RE runner รอบ `RE-RUNNER-20260907_0942`) · พับโดย LANE-K รอบ `wb8tfv` 2026-09-07T11:10+07:00 — **K คัดลอก ไม่ได้ตัดสิน ไม่ได้รันอะไรเอง**

```
[0xF0DFF8 + 0x7C] = 0x0045C560
```

- **= ค่าเดียวกับ `CNetNPC +0x7C` ที่ใบปักไว้เป๊ะ** ⇒ `CAvatarNPC` (actor_type 5) สร้าง `NameBoardNPC` ⇒ ผู้สมัคร AT5 ของ `GT-288` ชุด 2 อ่านป้ายชื่อได้จริง ⇒ **ไม่ต้องถอนผู้สมัคร `actor_type` ออกจากชุด 2**
- ตรวจไขว้ที่ตัวฟังก์ชัน (คำต่อคำ): `0x0045C560` → file `0x5B960` · `push 0xC0` = ขนาด `NameBoardNPC` · `0x00456580` → file `0x55980` · `push 0x78` = ขนาด `NameBoardPlayer` — **ตรงกับตัวเลขที่ใบปักไว้ทั้งคู่**
- VA→file คำนวณจาก PE header ของไบนารีเอง (`e_lfanew=0x128` · `ImageBase=0x00400000` · `.rdata` VA `0x00C3B000` raw `0x00839400`)

🟡 **ชั้นที่ครบ: static (ไบนารีไคลเอนต์) · ชั้นที่ขาด: client-observable NOT MEASURED** — ใบนี้เป็นใบ static โดยนิยาม (`[STATIC-ON-BRIDGE]`) ไม่มีชั้นจอให้วัด ⇒ นี่คือรูปที่ถูกของใบนี้ ไม่ใช่ชั้นที่ขาด

**nonclaims ของผล — ✅ สามข้อแรกคำต่อคำจากเจ้าของใบ LANE-B ข้อ 3 · 🟠 ข้อที่สี่ (`external/`) เป็น**สำนวนของ K เอง** ไม่ใช่คำของใคร (ป้ายเดิมเขียนว่า "K ไม่เติมไม่ตัด" ซึ่ง**ผิด** — แก้โดย LANE-K รอบ `k01t0u` 2026-09-07T12:15+07:00 หลัง pf-adversary D3)**:
- ไม่ได้พิสูจน์ว่า AT5 **ระบายสีชื่อ** ได้ตามที่ P-2 ต้องการ · พิสูจน์แค่ว่า **มีป้ายชื่อให้ระบาย** (ด่านโครงสร้าง)
- ไม่ได้พิสูจน์ว่า AT5 เรนเดอร์บนจอ (นั่นคือสิ่งที่ `GT-288` ชุด 2 บนเครื่องเจ้าของต้องตอบ)
- ค่าในโคเด็กซ์กับค่าที่ RE อ่าน มาจากไบนารีที่มี sha256 เดียวกัน ⇒ ยืนยันซ้ำ **ภายในไบนารีเดิม** เท่านั้น
- 🔴 ข้อจำกัดที่ RE runner เขียนเอง: รอบชนเส้นนาที 38 ก่อนแยกได้ว่า 6 ไฟล์ใน `external/` ตรง**คำไหน** ⇒ **ไม่อ้างว่าเป็นผลลบสมบูรณ์** · grep แคบที่ขอ LANE-B ทำแล้วในจดหมาย `1046` (ค่าเดิมอยู่ใน `notes_to_chief/reference_codex_attr/` **ไม่ใช่** `external/` ตามที่ RE เขียน และ `PF_MONSTER_PRESENTATION.tsv` **ไม่มีไฟล์นี้ในรีโป**)

🔴 **[เติมโดย LANE-K รอบ `k01t0u` หลัง pf-adversary D3] nonclaims ของ *ผู้ทำ* (RE runner) ที่รอบ `wb8tfv` ตกไป — คำต่อคำจาก `notes_to_chief/20260907_1027_RE-290-RESULT-cavatarnpc-builds-the-same-nameboardnpc-as-cnetnpc.md` หัวข้อ `## nonclaims`:**
1. **ไม่ได้พิสูจน์ว่าเซิร์ฟเวอร์เดินถึง `CAvatarNPC` จริง** — รายงานบรรทัด 292 บอกเองว่ายังไม่ trace ผลนี้ตอบแค่ "คลาสนี้ถ้าถูกสร้าง มันสร้างบอร์ด" ไม่ได้ตอบว่า "สตรีมของเราทำให้มันถูกสร้าง"
3. **ไม่ได้ดิสแอสเซมบลีทั้งฟังก์ชัน** — อ่าน prologue 64 ไบต์แรกเพื่อดูขนาดที่จองเท่านั้น และ **ไม่ได้ใช้ linear disassembler เป็นหลักฐานของผลลบใด ๆ**
5. ชั้นผล = static บน binary ล้วน **ไม่มีชั้น client-observable** — ไม่มีจอ ไม่มีเฟรม
🔴 **ทำไมข้อ 1 สำคัญกับผู้เทส `GT-288` ชุด 2**: หัวใบเขียนว่า "ถ้าสีไม่ขึ้น = FAIL ของ**สี** จริง ๆ" — nonclaim ข้อ 1 บอกว่า**ยังมีทางออกที่สามที่ยังไม่ถูกปิด**: สตรีมของเราอาจไม่เคยสร้าง `CAvatarNPC` เลย ซึ่งกรณีนั้นคำตอบที่ถูกไม่ใช่ทั้ง PASS ของสีและ FAIL ของสี · **K ไม่ตัดสิน** ว่าผู้เทสต้องทำอะไร — คืนคำของผู้ทำให้ครบเท่านั้น

> 📌 [LANE-K รอบ `wb8tfv`] สิ่งที่ RE runner ขอใน BUILD_IMPACT ข้อ 2 (ถอดข้อความ "AT5 ไม่มีป้ายชื่อ..." ออกจากเนื้อใบ `GT-288`) **K ไม่ลบของเดิม** (กติกาเหล็กข้อ 2 "ห้ามลบอะไรทั้งสิ้น") — ติดป้ายว่า **ถูกแทนที่แล้วโดย `RE-290`** ไว้ในหัวใบ `GT-288` แทน

> numbering: ตัวนับร่วมสองคิว + `archive/*ARCHIVE*` + `tickets/` คืนสูงสุด **289** (`RE-289`, ตั้งเลขรอบ `70l5du`) ⇒ ใบนี้ **290** · ตรวจ 0 hit ของ `GT-290`/`RE-290` ทั้งสี่ที่ (live สองคิว + `archive/*ARCHIVE*` + `tickets/` + `notes_to_chief/FROM_CHIEF_*`/`*COO-DECISION*`) ก่อนวาง [ตรวจโดย LANE-K รอบ `rlapyk`]

---

## RE-292 GM-RUNGMCOMMAND-0X51E9-LEADING-PAIR-AND-PRESENCE-SLOT-001  [🔧 **PASS / BOUNDED-POSITIVE — พับโดย LANE-K รอบ `spppsd` 2026-09-07T14:22+07:00** คำต่อคำจากหัวจดหมายผล `notes_to_chief/20260907_1315_RE-292-RESULT-first-0B-is-vital-version-presence-is-the-second-pair.md` (RE runner บนเครื่องสะพาน รอบ `RE-RUNNER-20260907_1100-OWNER-ORDERED-FULL-SWEEP`): "สถานะ: **PASS / BOUNDED-POSITIVE** — ตอบครบทั้งสองครึ่งของคำถามเดียวของใบ" · K คัดลอกคำของผู้ทดสอบ **ไม่ได้ตัดสินเอง** และไม่ได้แตะเนื้อใบ · 🟠 บันทึกเดิมก่อนพับ (ไม่ลบ ขีดฆ่าไว้ตามธรรมเนียมบ้าน): ~~🔴 **OPEN**~~ · 🔺 `[STATIC-ON-BRIDGE]` (อ่านไบนารี/ไฟล์ที่มีอยู่แล้วบนเครื่องสะพาน read-only -- **ไม่ใช่ attended ไม่เปิดเกม ไม่จับ `LOCK_GAME` ไม่กินเวลาเครื่องเจ้าของ** ⇒ ไม่มีบล็อก `ATTENDED:` และไม่ต้องมี `HEADLESS_PROOF:` ตาม `NOW.md` `0159` ซึ่งบังคับเฉพาะใบ attended) · **เจ้าของใบ/ผู้เขียนเนื้อใบ/ผู้บริโภคผล = LANE-GM** · ผู้ทำ = RE runner บนเครื่องสะพาน · ตั้งเลขโดย LANE-K รอบ `4af3qf` 2026-09-07T07:12+07:00 (ภายในรอบที่เห็นคำขอ 06:14) · เนื้อใบมาจากจดหมาย `notes_to_chief/20260907_0614_LANE-GM-TO-K-gt279-real-frames-do-not-satisfy-the-re088-pin.md` คำต่อคำ · ผูกกับ `GT-279` (เฟรมจริงสามใบจาก R322B) และ `RE-088` (pin ของ decoder) · ไม่ต้องขอเครื่องเจ้าของ: มีไบต์จริงสามใบแล้ว]

**เฟรม `0x51E9` จริงสามใบจาก R322B ไม่ผ่าน pin `RE-088` ของ decoder ที่ ship อยู่**

### สิ่งที่วัดได้ (เจ้าของใบวัดเอง รอบ `wxh2tw`)
ป้อนไบต์จริงเฟรมที่ 1 (`0B 00 0B 01 14 01000000 14 00000000 0B 01 48 00000000 48 00000000`) แล้ว section decode ในไฟล์ capture เขียนว่า
`# decode: FAILED against RE-088 pin -- presence=0 but 24 trailing byte(s) remain`
decoder อ่าน `0B 00` คู่แรกเป็น **presence** แล้วสรุปว่าไม่มี body ทั้งที่เหลืออีก 24 ไบต์

เทียบ `RE-283` FINAL (presence → u32 บิตฟังก์ชัน · u32 ตัวเลข · u8 แฟล็ก · string ×2) ไบต์จริงเข้ารูปเป๊ะ **ถ้านับ presence ที่คู่ที่สอง**:
`0B 00`(?) · `0B 01`=presence · `14 01000000`=บิตฟังก์ชัน · `14 00000000`=ตัวเลข · `0B 01`=แฟล็ก · `48 00000000` ×2 = string ว่าง
เฟรมที่ 3 (วาร์ป) ต่างตรงที่คาด: `14 00100000`=0x1000 · `48 02000000 3000`= UTF-16 "0"

⇒ **มีฟิลด์นำหน้าที่ pin `RE-088` ไม่รู้จัก** (ครั้งแรกที่เฟรม `0x51E9` จริงมาชนกับ pin)

### คำถามเดียวของใบ
**ไบต์คู่แรก `0B xx` ของ `0x51E9` คือฟิลด์อะไร และ presence อยู่ที่คู่ไหน**

### grep แล้ว (ตามกฎ "grep ก่อนออกใบ")
เจ้าของใบอ้าง `RE-283` FINAL (layout ที่พิสูจน์แล้ว) และ pin `RE-088` ของ decoder เป็นฐานเปรียบเทียบ — สองแหล่งนี้มีอยู่แล้วในรีโป ใบนี้ไม่ได้ถามซ้ำสิ่งที่ทั้งสองแหล่งตอบไว้ แต่ถามฟิลด์ที่**ทั้งสองแหล่งไม่ครอบคลุม** (คู่แรก)

### nonclaims (จากเจ้าของใบ ห้ามตัดออก)
- ไม่อ้างว่ารู้ความหมายของคู่แรก
- ไม่อ้างว่า decoder ผิด (อาจมี wrapper ชั้นนอก) — อ้างเฉพาะว่า **pin กับไบต์จริงไม่ตรง และวัดได้**
- ไม่อ้างว่า `GT-279` ผ่าน · เจ้าของใบไม่แก้เนื้อใบเอง
- **รอบที่ออกใบไม่แตะ decoder** — layout ของ vital นี้เป็นเขตสาย RE ตาม prompt ของ LANE-GM เอง

### result:
**PASS / BOUNDED-POSITIVE** -- พับโดย LANE-K รอบ `spppsd` 2026-09-07T14:22+07:00 · คัดลอกจาก `notes_to_chief/20260907_1315_RE-292-RESULT-first-0B-is-vital-version-presence-is-the-second-pair.md` คำต่อคำ · **K ไม่ได้รันอะไรเองและไม่ได้ตัดสินผล**

> RE-292 RESULT — คู่แรก `0B xx` = **`vital_version`** ของซองจดหมาย · presence = **คู่ที่สอง**
>
> สถานะ: **PASS / BOUNDED-POSITIVE** — ตอบครบทั้งสองครึ่งของคำถามเดียวของใบ
>
> (หลักฐานเต็ม ตาราง VA และ nonclaims อยู่ในจดหมายต้นฉบับ — K ไม่ย่อความ ไม่ตีความ)

> numbering [LANE-K รอบ `4af3qf`]: คำสั่งค้นหาเดียวตามกติกาหัวไฟล์ข้อ ② คืนสูงสุด **291** ⇒ ใบนี้ **292** · ตรวจ 0 hit ของ `GT-292`/`RE-292` ครบสี่ที่ (live สองคิว + `archive/*ARCHIVE*` + `tickets/` + `notes_to_chief/FROM_CHIEF_*`/`*COO-DECISION*` + `NOW.md`) ก่อนวาง

---

## RE-294 STALL-VITAL-TAIL-CALLS-WRITE-BYTES-OR-NOT-001  [🔧 **PASS / DONE — พับโดย LANE-K รอบ `spppsd` 2026-09-07T14:22+07:00** คำต่อคำจากหัวจดหมายผล `notes_to_chief/20260907_1350_RE-294-RESULT-stallopen-writes-nothing-extra-stallstart-writes-via-766C00.md` (RE runner บนเครื่องสะพาน รอบ `RE-RUNNER-20260907_1100-OWNER-ORDERED-FULL-SWEEP`): "สถานะ: **PASS / DONE** — ตอบคำถามเดียวของใบครบทั้งสองคลาส" · K คัดลอกคำของผู้ทดสอบ **ไม่ได้ตัดสินเอง** และไม่ได้แตะเนื้อใบ · 🟠 บันทึกเดิมก่อนพับ (ไม่ลบ ขีดฆ่าไว้ตามธรรมเนียมบ้าน): ~~🔴 **OPEN**~~ · 🔺 `[STATIC-ON-BRIDGE]` (อ่านไบนารี/ไฟล์ที่มีอยู่แล้วบนเครื่องสะพาน read-only -- **ไม่ใช่ attended ไม่เปิดเกม ไม่จับ `LOCK_GAME` ไม่กินเวลาเครื่องเจ้าของ** ⇒ ไม่มีบล็อก `ATTENDED:` และไม่ต้องมี `HEADLESS_PROOF:` ตาม `NOW.md` `0159` ซึ่งบังคับเฉพาะใบ attended) · **เจ้าของใบ/ผู้เขียนเนื้อใบ/ผู้บริโภคผล = LANE-UI** · ผู้ทำ = RE runner บนเครื่องสะพาน · ตั้งเลขโดย LANE-K รอบ `4af3qf` 2026-09-07T07:12+07:00 (ภายในรอบที่เห็นคำขอ 06:29) · เนื้อใบมาจากจดหมาย `notes_to_chief/20260907_0629_LANE-UI-TO-K-re-body-stall-tail-calls-write-bytes-or-not.md` คำต่อคำ · แทนที่ `GT-262` ที่ยกเลิกไปแล้ว (จดหมาย `0456`) · `RE-261` ยังเปิดอยู่ ไม่ทับกัน (`RE-261` = static completeness ของกลุ่ม Stall/GuildStorage โดยรวม · ใบนี้ = คำถามเดียวเรื่อง call graph ของ serializer สามตัว)]

aimเดียว: **call ที่ตามหลัง prefix ที่ติดแท็กแล้วของ `StallStartVital` (`0x0076AC20`) และ `StallOpenVital` (`0x0076ACB0`) เขียนไบต์ลงบัฟเฟอร์ serializer ตัวเดียวกับ prefix หรือไม่** (คำต่อคำจากหัวข้อ "คำถามเดียวที่ขอให้ RE runner ตอบ" ของจดหมายเจ้าของใบ)

🔴 **เนื้อใบเต็ม (grep แล้ว 6 ข้อ · เกณฑ์ตัดสินที่ขอ · ที่สายนี้จะไม่ทำจนกว่าจะได้คำตอบ) อยู่ที่ `tickets/RE-294.md`** — ใบเกิน 8,192 B ตั้งแต่เกิด ตามเพดานต่อใบใน `NOW.md` (แบบเดียวกับ `GT-288`) · ห้ามตอบใบนี้โดยไม่อ่านไฟล์นั้น: ข้อ 2 (`external/PF_PROTOCOL_PRIORITY.tsv:510-513`) และข้อ 4 (สองแหล่งขัดกันเรื่อง `0x76A630`) เปลี่ยนรูปคำตอบทั้งใบ

### result:
**PASS / DONE** -- พับโดย LANE-K รอบ `spppsd` 2026-09-07T14:22+07:00 · คัดลอกจาก `notes_to_chief/20260907_1350_RE-294-RESULT-stallopen-writes-nothing-extra-stallstart-writes-via-766C00.md` คำต่อคำ · **K ไม่ได้รันอะไรเองและไม่ได้ตัดสินผล**

> RE-294 RESULT — `StallOpenVital` **ไม่เขียนเพิ่ม** · `StallStartVital` **เขียน** ผ่าน `0x00766C00` (ถอดครบแล้ว)
>
> สถานะ: **PASS / DONE** — ตอบคำถามเดียวของใบครบทั้งสองคลาส
>
> (หลักฐานเต็ม ตาราง VA และ nonclaims อยู่ในจดหมายต้นฉบับ — K ไม่ย่อความ ไม่ตีความ)

> numbering [LANE-K รอบ `4af3qf`]: ต่อจาก `RE-293` ในรอบเดียวกัน ⇒ ใบนี้ **294** · ตรวจ 0 hit ครบสี่ที่ก่อนวาง
> 📌 [LANE-K รอบ `4af3qf`] หมายเหตุของเจ้าของใบถึง COO ที่ **ไม่ใช่เนื้อใบ** แต่ห้ามให้หาย: `external/PF_PROTOCOL_PRIORITY.tsv` มีคอลัมน์ `OPEN`/`CLOSED` + ชื่อเหตุผลต่อคลาส ครบ 519 คลาส แต่ **ไม่ได้อยู่ในแผนที่สามไฟล์ที่ `prompts/COMMON_LANE_ROUND.md` สั่งให้ทุกสาย grep ก่อนออกใบ RE** ⇒ ทุกสายกำลังออกใบโดยไม่เห็นคอลัมน์ที่บอกว่า "ข้อนี้ปิดไปแล้วหรือยัง" · เจ้าของใบขอให้พิจารณาเพิ่มเป็นไฟล์ที่สี่ · K ส่งต่อในจดหมายรอบถึง COO (`prompts/` แก้ได้เฉพาะ Panya ตาม `NOW.md`)

---

## RE-295 QUEST-REWARD-ROUNDING-AND-LV-LEVEL-SOURCE-001  [🔧 **PASS / DONE — พับโดย LANE-K รอบ `spppsd` 2026-09-07T14:22+07:00** คำต่อคำจากหัวจดหมายผล `notes_to_chief/20260907_1425_RE-295-RESULT-multiply-is-double-truncate-and-Lv-reads-player-level.md` (RE runner บนเครื่องสะพาน รอบ `RE-RUNNER-20260907_1100-OWNER-ORDERED-FULL-SWEEP`): "สถานะ: **PASS / DONE** — ตอบครบทั้งสี่ข้อที่ใบขอ (Q2, Q1ก, Q1ข, `AddLvCriteriaExp`, และข้อแถม 4)" · K คัดลอกคำของผู้ทดสอบ **ไม่ได้ตัดสินเอง** และไม่ได้แตะเนื้อใบ · 🟠 บันทึกเดิมก่อนพับ (ไม่ลบ ขีดฆ่าไว้ตามธรรมเนียมบ้าน): ~~🔴 **OPEN**~~ · 🔺 `[STATIC-ON-BRIDGE]` (อ่าน client image ที่มีอยู่แล้วบนเครื่องสะพาน read-only — **ไม่ใช่ attended ไม่เปิดเกม ไม่จับ `LOCK_GAME` ไม่กินเวลาเครื่องเจ้าของ** ⇒ ไม่มีบล็อก `ATTENDED:` และไม่ต้องมี `HEADLESS_PROOF:` ตาม `NOW.md` `0159` ซึ่งบังคับเฉพาะใบ attended · เจ้าของใบระบุเองว่า "ไม่กินคิวรถบัส") · **เจ้าของใบ/ผู้เขียนเนื้อใบ/ผู้บริโภคผล = LANE-Q** · ผู้ทำ = RE runner บนเครื่องสะพาน · ตั้งเลขโดย LANE-K รอบ `73i74a` 2026-09-07T10:09+07:00 (ภายในรอบที่เห็นคำขอ 09:05) ตาม `COO-DECISION 20260907_0845` ("LANE-Q: เขียน **เนื้อใบ RE** (ส่ง K ตั้งเลข) ถามสองข้อในใบเดียว") · เนื้อใบมาจากจดหมาย `notes_to_chief/20260907_0905_LANE-Q-TO-K-re-body-how-the-client-rounds-and-where-Lv-reads-level.md` **คำต่อคำ K ไม่แก้สำนวนใด ๆ และไม่ได้ตัดสินคำถามของใบ**]

หัวข้อ: **รางวัลเควสปัดเศษอย่างไร และ `Lv` อ่านเลเวลจากไหน** (`AddCriteriaExp 0x00608D10` · `AddLvCriteriaSkillPoint 0x006092B0`)

🔴 **เนื้อใบเต็ม (สองคำถาม · ผล grep 5 ข้อที่เจอ + 3 ข้อที่ไม่เจอ · ลำดับความสำคัญของคำตอบ · nonclaims) อยู่ที่ `tickets/RE-295.md`** — ใบเกิน 8,192 B ตั้งแต่เกิด (11,550 B) ตามเพดานต่อใบใน `NOW.md` (แบบเดียวกับ `GT-288`/`RE-294`) · ห้ามตอบใบนี้โดยไม่อ่านไฟล์นั้น: หัวข้อ "grep แล้ว" บอกไว้ 5 ข้อว่า**ห้ามตอบด้วยของที่มีแล้ว** (VA ครบห้าในหก · ตารางที่ถูกอ่าน · ตัวคูณเป็น float32 · arity 0 · `delegate_body6` ไม่ใช่ลายเซ็น)

### result:
**PASS / DONE** -- พับโดย LANE-K รอบ `spppsd` 2026-09-07T14:22+07:00 · คัดลอกจาก `notes_to_chief/20260907_1425_RE-295-RESULT-multiply-is-double-truncate-and-Lv-reads-player-level.md` คำต่อคำ · **K ไม่ได้รันอะไรเองและไม่ได้ตัดสินผล**

> RE-295 RESULT — คูณที่ **double** แล้ว **ตัดทิ้ง** · `Lv` อ่านเลเวลจาก **ออบเจกต์ผู้เล่น** · `AddLvCriteriaExp` **มีอยู่จริง**
>
> สถานะ: **PASS / DONE** — ตอบครบทั้งสี่ข้อที่ใบขอ (Q2, Q1ก, Q1ข, `AddLvCriteriaExp`, และข้อแถม 4)
>
> (หลักฐานเต็ม ตาราง VA และ nonclaims อยู่ในจดหมายต้นฉบับ — K ไม่ย่อความ ไม่ตีความ)

> numbering: ตัวนับร่วมสองคิว + `archive/*ARCHIVE*` + `tickets/` คืนสูงสุด **294** (`RE-294`, ตั้งเลขรอบ `4af3qf`) ⇒ ใบนี้ **295** · ตรวจ 0 hit ของ `GT-295`/`RE-295` ทั้งสี่ที่ (live สองคิว + `archive/*ARCHIVE*` + `tickets/` + `notes_to_chief/` + `NOW.md`) ก่อนวาง · hit เดียวที่เจอคือประโยคในไฟล์รอบของ K เอง (`rounds/K_20260907_0909_*` ข้อ 4 "ตั้งเลข `GT-295` ให้ใบ `SKILL-ATTR-...`") ซึ่ง**ไม่ใช่ใบ** และ `COO-DECISION 20260907_0845` (cs0815) สั่งไว้ชัดว่าใบนั้น **ยังไม่ตั้งเลข** จนกว่า CS แจ้งว่าประตูคลาสลงแล้ว ⇒ เลข 295 ไม่ได้ถูกจอง [ตรวจโดย LANE-K รอบ `73i74a`]

---

## RE-297 BG3001-TGR-BOX-ANCHOR-AND-UNITS-001  [🔧 **PASS / BOUNDED-POSITIVE — พับโดย LANE-K รอบ `spppsd` 2026-09-07T14:22+07:00** คำต่อคำจากหัวจดหมายผล `notes_to_chief/20260907_1505_RE-297-RESULT-pos-is-the-centre-and-extent-is-full-width.md` (RE runner บนเครื่องสะพาน รอบ `RE-RUNNER-20260907_1100-OWNER-ORDERED-FULL-SWEEP`): "สถานะ: **PASS / BOUNDED-POSITIVE** — ข้อ 1 ตอบแน่นอนหนึ่งทาง · ข้อ 3 ตอบได้ · ข้อ 2 ตอบไม่ได้ (บอกเหตุผล) · ข้อ 4 ยังเปิด" · K คัดลอกคำของผู้ทดสอบ **ไม่ได้ตัดสินเอง** และไม่ได้แตะเนื้อใบ · 🟠 บันทึกเดิมก่อนพับ (ไม่ลบ ขีดฆ่าไว้ตามธรรมเนียมบ้าน): ~~🔴 **OPEN**~~ · 🔺 `[STATIC-ON-BRIDGE]` (อ่านไฟล์ข้อมูลไคลเอนต์ read-only ไม่เปิดเกม ⇒ **ไม่มีบล็อก `ATTENDED:` ไม่กินเวลาเครื่องเจ้าของ ไม่ต้องมี `HEADLESS_PROOF:`** — คำของเจ้าของใบ) · **เจ้าของใบ/ผู้เขียนเนื้อใบ/ผู้บริโภคผล = LANE-A (WORLD)** · ผู้ทำ: **สาย RE** · ตั้งเลขโดย LANE-K รอบ `k01t0u` 2026-09-07T12:15+07:00 (คำขอเข้ามา 2026-09-07T10:22 — ตั้งเลขในรอบแรกที่ K เห็นคำขอ) · เนื้อใบมาจากจดหมาย `notes_to_chief/20260907_1022_LANE-A-TO-K-re-ticket-body-tgr-extent-is-full-or-half-width.md` **คำต่อคำ K ไม่แก้สำนวนแม้คำเดียว**]:

## หัวข้อใบ
`BG3001-TGR-BOX-ANCHOR-AND-UNITS-001` · `[STATIC-ON-BRIDGE]` (อ่านไฟล์ข้อมูลไคลเอนต์ read-only ไม่เปิดเกม ไม่กินเวลาเครื่องเจ้าของ ⇒ ไม่มีบล็อก `ATTENDED:` ไม่ต้องมี `HEADLESS_PROOF:`)

## ทำไมต้องมีใบนี้
`RE-289` คืนกล่องมาแล้ว (ord 1/2/3) และ LANE-A commit ตารางลง `world_m2_trigger_vital_response.ISLAND_EXTENT_BOXES` แล้ว (`pirate-force-server#1015`)
แต่ **ใบไม่ได้บอกสองอย่างที่ตัดสินว่ากล่องอยู่ตรงไหนจริง**:
1. `pos` (`+0x0E` f32*3) เป็น **จุดกึ่งกลาง** ของกล่อง หรือ **มุมต่ำ** (min corner)
2. `extent` (`+0x1A` f32*3) เป็น **ความกว้างเต็ม** หรือ **ครึ่งความกว้าง** (half-extent)

รอบนี้เลือก "กึ่งกลาง + กว้างเต็ม" (`pos ± extent/2`) และเขียนไว้ในโมดูลว่าเป็นการเดา
**ข้อ 1 ไม่ fail-closed**: ถ้า `pos` เป็นมุมต่ำจริง กล่องที่ commit ไปไม่ใช่สับเซตของกล่องจริง ⇒ เรือที่ (-6000, 5500, 86) จะถูกนับว่า "ชนเกาะ" ทั้งที่อยู่นอกกล่องจริง = false island ซึ่งเป็นความล้มเหลวที่ M2 ห้ามมี

## grep แล้ว: เจอ/ไม่เจอ
- `external/` (345 ไฟล์ชื่อจริง) grep `TELCHK` / `.tgr` = **0 hit** (ยืนยันซ้ำสิ่งที่ `RE-273` และ `RE-289` วัดไว้)
- `external/PF_SERIALIZER_FIELDS.tsv` = layout ของ serializer บนสาย ไม่ใช่ไฟล์ฉาก ⇒ ไม่มีคำตอบ
- `gamedata/scene/Bg3001/` มีไฟล์เดียว `Bg3001.placements.tsv` ถอดจาก `.npc` ล้วน ไม่มีอะไรจาก `.tgr`
⇒ **ไม่มีคำตอบเดิมให้ reuse**

## คำถาม (ตอบได้จากไฟล์ข้อมูลล้วน ไม่ต้องเปิดเกม)
1. **หา discriminator ในข้อมูลเอง**: มี trigger record ใดใน `.tgr` ของฉากใดก็ได้ ที่ `pos` อยู่ **ติดขอบกรอบฉาก** จนกล่องแบบ "กึ่งกลาง" จะล้นออกนอกฉาก แต่แบบ "มุมต่ำ" จะพอดี (หรือกลับกัน)? หนึ่งเรคคอร์ดแบบนั้นตัดสินข้อ 1 ได้ทันที
2. **ทาบกับ NavMesh/collision ของฉาก** ถ้ามีไฟล์ที่ commit แล้ว: ขอบกล่องแบบไหนตรงกับขอบเกาะจริง
3. **`extent_z`**: ทุกเรคคอร์ดมี `pos.z = 86.0` ซึ่งเป็น **ค่าต่ำสุดของกรอบฉาก** พอดี · ถ้า `pos.z` เป็นพื้นเสมอ นั่นเป็นหลักฐานว่า z วัด **ขึ้นจากพื้น** ไม่ใช่กึ่งกลาง ⇒ ขอให้ยืนยัน/หักล้างด้วยฉากอื่นที่ trigger ลอยเหนือพื้น
4. **`Trigger.Var1`/`Var2` อยู่ที่ไหน** — `t_telchk_lv.lua` ใช้ทั้งสองตัว (`Var1` = marker ปลายทาง, `Var2` = เลเวลขั้นต่ำ) แต่ `RE-289` ไม่ได้แตะ `flags[5]` และ tail 372 ไบต์ ⇒ **ห้ามเดาว่าอยู่ใน block**

## หลักฐานในรีโปที่เอนไปทาง "ครึ่งความกว้าง" (pf-adversary ขุดจากไฟล์ของสาย A เอง)
`src/pirateforce_foundation/world_m2_sea_destination.py:162-164` เก็บท่าจอดของฉาก 126 จาก `CONSTDATA_TH__MARKER.tsv`:

| berth | pos | กล่องใกล้สุด | กล่องกว้างเต็ม | กล่องครึ่งกว้าง |
|---|---|---|---|---|
| MARKER[17] | (3050, 232, 90) | ord 1 (3098.2, 2207.5) | **นอก** แกน y 625.5 | ใน |
| MARKER[18] | (-5072, 4000, 90) | ord 2 (-5426.19, 5129.33) | **นอก** แกน y 129.33 | ใน |

สองจุดไม่ใช่ข้อพิสูจน์ (ท่าจอดขาเข้าไม่จำเป็นต้องอยู่ในกล่องขาออก) แต่เอนไปทางเดียวกันทั้งคู่ และ z ต่างจาก trigger แค่ 4 หน่วย

## เกณฑ์ผ่าน
ตอบข้อ 1 ได้แน่นอนหนึ่งทาง พร้อมเรคคอร์ดอ้างอิงอย่างน้อยหนึ่งใบที่แยกสองสมมติฐานออกจากกัน · ข้อ 3 ตอบได้หรือระบุว่าตอบไม่ได้พร้อมเหตุผล

## สิ่งที่ใบนี้ **ไม่** ถาม
- ไม่ถาม crosswalk ordinal ↔ wire trigger id (ใบแยก ยังไม่มีเลข)
- ผลใบนี้ **ยังไม่พอ** เติม `ISLAND_CONTACT_DISCRIMINATOR` เหมือนกัน — ตัวนั้นรอ crosswalk

## ขอเพิ่มจากรอบก่อน (ยังค้าง ไม่ใช่คำถามของใบ)
`staged/re289_tgr_extract.py` และ `staged/RE-289_Bg3001_tgr_full_dump.txt` ที่ RE runner ขอให้ commit
**ไม่มีอยู่ในรีโป** — LANE-A วัดเองรอบนี้: `ls staged/ | grep -i re289` = 0 hit บน `origin/main`
ไฟล์อยู่บนเครื่องสะพานเท่านั้น ⇒ โคลนคลาวด์ commit ให้ไม่ได้ · ขอ K หรือ chief ที่มีเครื่องสะพานหยิบเข้ารีโป
ไม่งั้นใบถัดไปชนกำแพงเดิมตามที่จดหมายผลเตือนไว้เอง

### result:
**PASS / BOUNDED-POSITIVE** -- พับโดย LANE-K รอบ `spppsd` 2026-09-07T14:22+07:00 · คัดลอกจาก `notes_to_chief/20260907_1505_RE-297-RESULT-pos-is-the-centre-and-extent-is-full-width.md` คำต่อคำ · **K ไม่ได้รันอะไรเองและไม่ได้ตัดสินผล**

> RE-297 RESULT — `pos` = **จุดกึ่งกลาง** · `extent` = **ความกว้างเต็ม** (ที่ LANE-A เลือกไว้ ถูกแล้ว)
>
> สถานะ: **PASS / BOUNDED-POSITIVE** — ข้อ 1 ตอบแน่นอนหนึ่งทาง · ข้อ 3 ตอบได้ · ข้อ 2 ตอบไม่ได้ (บอกเหตุผล) · ข้อ 4 ยังเปิด
>
> (หลักฐานเต็ม ตาราง VA และ nonclaims อยู่ในจดหมายต้นฉบับ — K ไม่ย่อความ ไม่ตีความ)

> numbering [LANE-K รอบ `k01t0u`]: ตัวนับร่วมสองคิว + `archive/*.md` (93 ไฟล์) + `tickets/` + เลขที่จองใน `FROM_CHIEF_*`/`COO-DECISION` คืนสูงสุด **296** ⇒ ใบนี้จอง **297** · `grep -rl 'GT-297\|RE-297'` ทั้งรีโป (นอก `.git/`) = **0 hit**
> 🟡 **[LANE-K รอบ `k01t0u`] ชี้ทาง ไม่ใช่การตัดสิน**: ท้ายเนื้อใบเจ้าของใบเขียนว่า `staged/re289_tgr_extract.py` ไม่มีในรีโป (`ls staged/ | grep -i re289` = 0 hit — K วัดซ้ำเองรอบนี้: `ls staged/*.py` คืน `re059_extract_capture.py` ไฟล์เดียว ⇒ **ข้อนี้ของเจ้าของใบถูกต้อง**) แต่ **parser ตัวเดียวกันอยู่ในรีโปแล้วที่ `tools_bridge/re289_tgr_extract.py`** (4,211 B · เข้ามารอบ `wb8tfv` · sha256 `eab4ce35f6ee39947bd2a09de0adeb488544a4cf88d4a455d8ced177bb0db283`) ⇒ ผู้ทำใบนี้ **ไม่ต้องรอคนบนเครื่องสะพาน** เพื่ออ่าน `.tgr` — อีกสองชิ้นที่จดหมายผล `RE-289` อ้าง (`staged/RE-289_Bg3001_tgr_full_dump.txt` · `staged/re273_tgr_parse.py`) **ยังไม่มีจริง** · K ไม่ได้ตัดสินว่า parser นั้นเพียงพอหรือไม่
> 🔴 [LANE-K รอบ `k01t0u`] K **ไม่ได้รับรอง** ตัวเลข/ตาราง/ข้อสรุปใดๆ ในเนื้อใบ — ทุกบรรทัดเหนือบรรทัดนี้เป็นคำของ LANE-A คำต่อคำ

---

## RE-298 BG3001-TGR-ORDINAL-AND-THE-TWO-UNDECODED-0X1FB2-FRAMES-001  [🔧 **PASS / BOUNDED-POSITIVE — พับโดย LANE-K รอบ `dccuar` 2026-09-07T15:24+07:00** คำต่อคำจากหัวจดหมายผล `notes_to_chief/20260907_1426_RE-298-RESULT-open-water-frame-is-trigger-35-and-ordinal-is-a-stored-field.md` (RE runner บนเครื่องสะพาน รอบ `RE-RUNNER-20260907-1416`): "สถานะ: **PASS / BOUNDED-POSITIVE** — ตอบข้อ 1 ด้วยไบต์ (ข้อที่บล็อก) และตอบข้อ 2 ได้ครบทั้งสองแขนที่ใบเขียนไว้" · K คัดลอกคำของผู้ทดสอบ **ไม่ได้ตัดสินเอง** และไม่ได้แตะเนื้อใบ · 🔴 จดหมายผลเขียนว่าให้ **LANE-A** กรอก `### result:` เอง (§5 "ใครเปิดใบคนนั้นบริโภค") แต่ `NOW.md` `PANYA 1910` เขียนว่า **พับผล = LANE-K** ⇒ K ยึด `NOW.md` ตามลำดับความจริงของ `COMMON_LANE_ROUND` และพับให้ · **การบริโภคผลของ LANE-A (เอาไปเติม `ISLAND_CONTACT_DISCRIMINATOR`) ยังเป็นของ LANE-A ไม่ใช่ของ K** · 🟠 บันทึกเดิมก่อนพับ (ไม่ลบ ขีดฆ่าไว้ตามธรรมเนียมบ้าน): ~~🔴 **OPEN**~~ · 🔺 `[STATIC-ON-BRIDGE]` (อ่านไฟล์/แคปเจอร์ read-only ไม่เปิดเกม ⇒ **ไม่มีบล็อก `ATTENDED:` และไม่ต้องมี `HEADLESS_PROOF:`** — คำของเจ้าของใบ) · **เจ้าของใบ/ผู้เขียนเนื้อใบ/ผู้บริโภคผล = LANE-A (WORLD)** · ผู้ทำ: **สาย RE** · ตั้งเลขโดย LANE-K รอบ `du6wre` 2026-09-07T13:32+07:00 (คำขอเข้ามา 2026-09-07T11:52 · LANE-A สั่งไว้ว่า *อย่าเพิ่งจัดคิวจนกว่า COO ตอบ* ⇒ อนุมัติแล้วโดย `notes_to_chief/20260907_1245_COO-DECISION-a1152-re234-item3-refuted-LANE-K.md` ⇒ ตั้งเลขในรอบแรกหลังคำอนุมัติ) · เนื้อใบมาจากจดหมาย `notes_to_chief/20260907_1152_LANE-A-TO-K-re-ticket-body-tgr-ordinal-and-the-two-undecoded-frames.md` **คำต่อคำ K ไม่แก้สำนวนแม้คำเดียว** (แทนเฉพาะ `RE-<เลข>` ด้วย `RE-298` ตามหน้าที่ตั้งเลข)]

> numbering [LANE-K รอบ `du6wre`]: ตัวนับร่วมสองคิว + `archive/*.md` + `tickets/` + เลขที่จองใน `FROM_CHIEF_*`/`*COO-DECISION*` คืนสูงสุด **297** ⇒ ใบนี้จอง **298** · `grep -rl 'GT-298\|RE-298'` ทั้งรีโป (นอก `.git/`) = **0 hit** ก่อนวาง
> 🔴 K **ไม่ได้รับรอง** ตัวเลข/พิกัด/ข้อสรุปใดในเนื้อใบ — ทุกบรรทัดข้างล่างเป็นคำของเจ้าของใบ (LANE-A)

### 🔶 บล็อกที่ **LANE-K เขียนเอง** ตามคำสั่ง `COO-DECISION 20260907_1245` ข้อ 2 (ไม่ใช่คำของ LANE-A — อย่านับเป็นเนื้อใบของเจ้าของ)
> **สองแขนของใบนี้ ต้องอ่านก่อนจัดคิว** (COO สั่งคำต่อคำ: *ห้ามออกใบที่บังคับ (ข) ทั้งที่ (ก) อาจพอ — ราคาต่างกันคนละชั้น และแขน (ก) ไม่กินเครื่องเจ้าของ*)
> - **แขน (ก) — raw ยังอยู่บนเครื่องคุณ Panya ⇒ งานอ่านไฟล์ล้วน ไม่เปิดเกม ไม่ต้องมีคนนั่งดู**: `GameClient\capture_r308_20260904_125449\capture_v141\GAME_20260904_130510_526308_52808.txt` sha256 `65692E9D…3CBE64FA` · 1,084,786 B (บรรทัด 7 และ 41 ของใบผล `20260904_1331_KA1A-R308-RESULTS-gt228-*.md`) ⇒ **ลองแขนนี้ก่อนเสมอ**
> - **แขน (ข) — ไฟล์นั้นหายแล้วเท่านั้น**: จึงออกใบ attended รอบใหม่ · 🔴 ห้ามข้ามไป (ข) โดยไม่ได้ลอง (ก)
> - ~~🔴 **ในรีโปไม่มีข้อมูลนี้ ห้ามนั่งหาซ้ำ**: ภาคผนวก hex ของใบผลมีเฉพาะ `rx130-134` · `rx151-155` · `rx250-254` · `rx433-437` ⇒ **`rx112` และ `rx248` ที่ใบนี้ถาม ไม่มี hex อยู่ในรีโป**~~
>   🔴🔴 **บรรทัดข้างบนเป็นเท็จ และ LANE-K เป็นคนเขียนมันเอง — ถอนทั้งบรรทัด 2026-09-07T13:5x+07:00 รอบ `du6wre` (addendum หลังปลดล็อก · `pf-adversary` จับได้ D1)**
>   ใบผลเดียวกันมีภาคผนวกที่ห้า **`=== all 0x1FB2 frames in session 2` ที่บรรทัด 140-146** ซึ่งมี **hex เต็ม 69 ไบต์ของทั้งหกเฟรม รวม `rx112` และ `rx248`** · คำสั่งวัดซ้ำ: `sed -n '140,146p' notes_to_chief/20260904_1331_KA1A-R308-RESULTS-gt228-*.md`
>   ⇒ **แขน (ก) ไม่ต้องใช้เครื่อง Panya ด้วยซ้ำ — ข้อมูลอยู่ในรีโปนี้แล้ว** · 🔴 **ห้ามไปแขน (ข) เด็ดขาด**
>
> - 🔵 **ค่าที่ LANE-K ถอดเองจากภาคผนวกนั้น 2026-09-07 รอบ `du6wre`** — 🔴 **นี่คือการวัดของเสมียน ไม่ใช่ `RESULT:` ของใบ ไม่ใช่การปิดใบ** คำตัดสินยังเป็นของผู้ทำ (สาย RE) และเจ้าของใบ (LANE-A) · วางไว้เพื่อไม่ให้ใครไปขอเครื่องเจ้าของเพื่อของที่มีอยู่แล้ว
>   **ตัวควบคุมของการถอด**: decoder ตัวเดียวกันคืน `rx130 (-4451.56, 4531.08)` · `rx152 (-5613.79, 4162.54)` · `rx433 (-1563.47, -5275.13)` ซึ่ง **ตรงกับค่าที่ใบผลตีพิมพ์ไว้เองที่บรรทัด 27-29 ทุกตัว** ⇒ decoder อ่านถูกรูปเฟรม
>   ```
>   rx112: id=35 trigger_xyz=(-752.17, 3138.06, 186.0)   ship TargetPos=(-872.04, 3175.01, 86.0)
>   rx248: id=2  trigger_xyz=(-6412.74, 4629.52, 186.0)  ship TargetPos=(-6231.26, 4871.58, 86.0)
>   ```
>   เทียบกับ `_ISLAND_EXTENT_BOXES` (`pirate-force-server/src/pirateforce_foundation/world_m2_trigger_vital_response.py:602-612`): **`rx112` (จุดน้ำเปล่า) อยู่นอกกล่องทั้งสามใบ** ทั้งพิกัด trigger และพิกัดเรือ · **`rx248` อยู่ในกล่อง ordinal 2**
>   ⇒ ถ้อยคำในใบข้อ 1 เขียนไว้เองว่า *"ถ้าจุดน้ำเปล่านั้นอยู่**นอก**กล่องทั้งสาม ⇒ กล่องแยก 'ชนเกาะ' ออกจาก 'น้ำเปล่า' ได้จริง"* — 🔴 **K ไม่สรุปแทน** ผู้ทำ/เจ้าของใบต้องตรวจการถอดนี้เองแล้วออก `RESULT:` ตามเกณฑ์ของใบ
> - 🟡 บริบทของข้อ 1: ประโยค *"`GT-228` เห็น id 3 ทั้งตอนชนเกาะและตอนน้ำเปล่า"* ที่เคยอยู่ใน `RE-234` ข้อ (3) และ `RE-289` **ถูกหักล้างแล้วในรอบเดียวกันนี้** (ใบผล `GT-228` บรรทัด 25/35: เฟรมน้ำเปล่าคือ `rx112 id=35` = `Thorn Flower PROP`) · แต่ข้อสรุป *"id เปล่าจำแนกไม่ได้"* ยังยืนบนแหล่ง **R307** (บรรทัด 90: `trigger ids seen: 40, 51, 3, 57, 36`)

### ↓↓↓ เนื้อใบคำต่อคำของเจ้าของใบ (LANE-A) เริ่มที่บรรทัดถัดไป ↓↓↓

`RE-298` **BG3001-TGR-ORDINAL-AND-THE-TWO-UNDECODED-0X1FB2-FRAMES-001** `[STATIC-ON-BRIDGE]`
เจ้าของใบ/ผู้บริโภคผล = **LANE-A (WORLD)** · ผู้ทำ = RE runner บนเครื่องสะพาน (read-only)

## ค้นก่อนออกใบ (LANE-A ทำแล้วรอบ `9r1ang` — ห้ามขุดซ้ำ · นี่คือเหตุผลที่ใบนี้แคบ)
ใบฉบับร่างแรกของรอบนี้ถามสามข้อ · **ข้อที่ใหญ่ที่สุดตอบได้เองจากของที่ commit แล้ว** จึงตัดออก:
จดหมาย `20260904_1331_KA1A-R308-RESULTS-gt228-...md` (`OBSERVER_CONFIRMED 13:22`) หัวข้อ (ข) + ตาราง (ก)
มีพิกัด 13 จุดพร้อม id ที่ไคลเอนต์ส่ง · LANE-A คำนวณแล้ว: **ทั้ง 13 จุดอยู่ในกล่องของ ordinal ที่เลข
เท่ากับ id และไม่อยู่ในกล่องอื่นเลย · สลับป้ายเกาะ ⇒ ตกทั้ง 13** (commit ที่ `pirate-force-server#1026`)
⇒ crosswalk ordinal ↔ wire id **มีหลักฐานแล้ว** ใบนี้ไม่ต้องถามซ้ำ

## คำถามของใบ (สองข้อ · ผลลบมีค่าทั้งคู่)

**1. พิกัดของสองเฟรมที่จดหมายไม่ได้ถอด**
`GT-228` นับเฟรม `0x1FB2` ทั้ง session ได้ 6 เฟรม แต่หัวข้อ (ข) ถอด xyz แค่ 4 เฟรม เหลือ:
- `rx112 13:08:52 id=35` — **เฟรมน้ำเปล่า** (แล่นเข้าหาเกาะ 2 ยังไม่แตะ)
- `rx248 13:13:26 id=2`
ขอถอด `trigger_xyz` + `TargetPos` ของสองเฟรมนี้จาก raw capture
`GameClient\capture_r308_20260904_125449\capture_v141\GAME_20260904_130510_526308_52808.txt`
(sha256 ที่จดหมายจด: `65692E9D…3CBE64FA` · 1,084,786 B) ตามรูปเฟรมของจดหมาย
`0F <u16 id> 00 0B 04 2A x 2A y 2A z`
🔴 **จุด `id=35` คือจุดที่สายนี้ต้องการที่สุด**: วันนี้พิสูจน์ได้แค่ว่ากล่องแยก**เกาะสองใบ**ออกจากกัน
ถ้าจุดน้ำเปล่านั้นอยู่**นอก**กล่องทั้งสาม ⇒ กล่องแยก "ชนเกาะ" ออกจาก "น้ำเปล่า" ได้จริง ซึ่งเป็นสิ่งที่
`ISLAND_CONTACT_DISCRIMINATOR` มีไว้ทำ · ถ้าอยู่**ใน**กล่อง ⇒ ตัวจำแนกเป็น no-op **บอกมาตรง ๆ ผลลบนี้มีค่าสูงสุดในใบ**

**2. ordinal มาจากไหน** — เรคคอร์ด trigger ใน `Bg3001.tgr` พก **ฟิลด์ id ของตัวเอง** ไหม
หรือเลขบนสายมาจาก **ลำดับที่อ่านเจอในไฟล์** ล้วน ๆ
- มีฟิลด์: ค่าของ `TELCHK_LV [01]/[02]/[03]` คืออะไร ตรงกับ 1/2/3 ไหม
- ไม่มีฟิลด์: นับจาก 0 หรือ 1 · มีเรคคอร์ด trigger ชนิดอื่นคั่นก่อนสามตัวนี้ไหม (ถ้าคั่น ตารางที่
  commit ไปเลื่อนทั้งแผง) · ข้อนี้ทำให้ผลข้อ 1 กลายเป็นกลไก ไม่ใช่แค่ความบังเอิญ 13 จุด

## ค้นก่อนถอด (LANE-A ทำแล้ว ห้ามขุดซ้ำ)
- `gamedata/scene/Bg3001/` มีไฟล์เดียว `Bg3001.placements.tsv` (38 แถว จาก `.npc`) — **ไม่มีอะไรจาก `.tgr`**
- `external/00_SEARCH_HERE_FIRST.md` + `PF_SERIALIZER_FIELDS.tsv`: grep `TELCHK`/`.tgr` = **ไม่มี layout ของ `.tgr`**
  ⇒ ใบนี้ไม่ใช่ใบที่ถามสิ่งที่มี layout อยู่แล้ว
- `staged/`: `ls staged/ | grep -i re289` = 0 hit

## input (read-only ห้ามแตะ `GameClient\`)
raw capture ข้างบน (ข้อ 1) · `GameClient\Data\Scene\Save\Bg3001\Bg3001.tgr` (ข้อ 2 · sha256 ที่ `RE-289` วัด:
`e0022e94e6b780cd0d364ec83e328c5f76b7e1215daf57cc24b51e93153a525f` — ต่างจากนี้ = บอกในผล)

## เกณฑ์ผ่าน
- **PASS** = ตอบข้อ 1 ด้วยไบต์ (xyz ของสองเฟรม หรือ "หาเฟรมไม่เจอในไฟล์ + เหตุผล")
- ตอบข้อ 2 ไม่ได้ ไม่ทำให้ใบตก · ตอบข้อ 1 ไม่ได้ = ใบตก (ข้อ 1 คือข้อที่บล็อก)

## สิ่งที่ใบนี้ **ไม่** ถาม
1. ไม่ขอให้ RE runner เติม `ISLAND_CONTACT_DISCRIMINATOR` · การเติมเป็นงานของ LANE-A รอบที่ผลกลับมา
2. ไม่ขอเฟรม `0x1FB2` ใหม่ · `RE-286` เป็นใบของเฟรมนั้น
3. ไม่ขอให้แตะกล่อง extent ที่ commit แล้ว

-- LANE-A รอบ `9r1ang`


### result:
**PASS / BOUNDED-POSITIVE** -- พับโดย LANE-K รอบ `dccuar` 2026-09-07T15:24+07:00 · คัดลอกจาก `notes_to_chief/20260907_1426_RE-298-RESULT-open-water-frame-is-trigger-35-and-ordinal-is-a-stored-field.md` คำต่อคำ · **K ไม่ได้รันอะไรเอง ไม่ได้ตีความ**

> RE-298 RESULT — เฟรมน้ำเปล่า `id=35` อยู่**นอกกล่องเกาะทั้งสาม** (ตัวจำแนกไม่ใช่ no-op) · `ordinal` เป็น**ฟิลด์ที่เก็บในเรคคอร์ด** ไม่ใช่ลำดับในไฟล์
>
> สถานะ: **PASS / BOUNDED-POSITIVE** — ตอบข้อ 1 ด้วยไบต์ (ข้อที่บล็อก) และตอบข้อ 2 ได้ครบทั้งสองแขนที่ใบเขียนไว้
>
> คำตอบหนึ่งบรรทัดสำหรับข้อที่ใบบอกว่าต้องการที่สุด: จุดของ `rx112 id=35` อยู่ **นอกกล่องของ ordinal 1/2/3 ทั้งสามใบ** ทั้งพิกัด trigger และพิกัดเรือ ⇒ ตามถ้อยคำของใบเอง: **กล่องแยก "ชนเกาะ" ออกจาก "น้ำเปล่า" ได้จริง `ISLAND_CONTACT_DISCRIMINATOR` ไม่ใช่ no-op** · และมีมากกว่านั้น: จุดนั้น **ไม่ใช่ "น้ำเปล่า" ในความหมายของไฟล์** — มันอยู่ใน**กล่องของ trigger `ordinal 35` (`Trigger OPNPLC_RAT_LV [35]`) พอดี และอยู่ในกล่องนั้นกล่องเดียวจากทั้ง 52 กล่องในฉาก** ⇒ `id` บนสายยังเท่ากับ ordinal ของกล่องที่เรืออยู่
>
> BUILD_IMPACT (คำต่อคำ): **ไม่มีการแก้ไฟล์ใด ๆ ในรอบนี้** · ผลต่อของที่ commit ไปแล้ว: **ยืนยันของเดิม ไม่ต้องแก้** — `_ISLAND_EXTENT_BOXES` ที่ `pirate-force-server#1015/#1026` ผ่านการทดสอบเพิ่มอีกสองจุดโดยไม่ต้องแก้ตัวเลขใด ๆ · **สิ่งที่ LANE-A ทำต่อได้ทันทีในรอบของตัวเอง**: เติม `ISLAND_CONTACT_DISCRIMINATOR` โดยถือข้อเท็จจริงข้อ 2 ไว้ด้วย — เฟรม `0x1FB2` เกิดกับ trigger ทุกชนิด ไม่ใช่เฉพาะเกาะ ⇒ ตัวจำแนกต้องตอบ "ไม่ใช่เกาะ" ไม่ใช่ "ไม่มีอะไร" เมื่อ id ตรงกับ ordinal ที่ไม่ใช่ 1/2/3 · 🟡 ข้อสังเกตเรื่องขอบ: `rx248` ห่างขอบกล่อง ordinal 2 บนแกน x แค่ **13.45 หน่วย** และ `rx130` ห่างขอบ **25.4 หน่วย**
>
> nonclaims ที่ห้ามตัดตอนพับ (ย่อชื่อข้อ ไม่ย่อความ — ฉบับเต็มหกข้ออยู่ในจดหมาย): 1. ไม่ได้พิสูจน์ว่าเซิร์ฟเวอร์ควรตอบอะไรตอนได้ `id=35` · 2. ไม่ได้พิสูจน์ว่า `ordinal` ในไฟล์ *คือ* wire id โดยนิยาม (15 จุดตรงกันหมด แต่ไม่ได้อ่านโค้ดไคลเอนต์ที่หยิบเลขไปใส่เฟรม — ชั้นนั้นเป็นใบ RE ใหม่) · 3. ไม่ได้อ้างว่าค่าท้ายเฟรมคืออะไร · 4. ไม่ได้อ้างว่า `z` ของ trigger (186.0) มีความหมายทางเรขาคณิต · 5. **ไม่ได้เปิดเกม ไม่มีชั้น client-observable ในผลนี้** · 6. `Player.TeleportCheck` = `STUB_NOOP` เป็นสถานะฝั่งเรา ไม่ใช่ข้ออ้างว่าไคลเอนต์ไม่เรียกสคริปต์
>
> (ตารางพิกัด · control 4 เฟรม · การทดสอบกับกล่องครบ 52 ใบ และหลักฐานเต็ม อยู่ในจดหมายต้นฉบับ — K ไม่ย่อความ ไม่ตีความ)

> 🔎 บล็อกของ LANE-K ในหัวใบ — ผู้ทดสอบตรวจแล้วและเขียนว่า: ค่าที่ K ถอดไว้เอง (`rx112 id=35` / `rx248 id=2` พร้อมพิกัดเรือ) **ตรงกับที่ผมถอดจาก raw ทุกตัวเลข** และข้อสรุปของ K ถูกต้อง · การถอนบรรทัด "ในรีโปไม่มีข้อมูลนี้" ของ K ก็ถูกต้อง · 🔴 **แต่ `RESULT:` ของใบคือฉบับของ RE runner ไม่ใช่บล็อกของ K** (K เขียนเองว่าไม่ใช่)

---

## RE-302 OUTGOING-VITAL-VERSION-PER-CLASS-AT-PLUS-0X10-001  [✅ **DONE — ตอบครบทั้ง 4 ข้อ (static ล้วน)** (คำต่อคำจากบรรทัด "สถานะ" ของจดหมายผล `notes_to_chief/20260907_1808_RE-302-RESULT-UPDATEATTR-VERSION-IS-ZERO-PER-CLASS-CTOR-CONSTANT.md` RE runner 2026-09-07T18:08+07:00) · พับหัวใบโดย LANE-K รอบ `kq7m3d` 2026-09-07T18:2x+07:00 · 🔺 `[STATIC-ON-BRIDGE]` (อ่าน client image / `PF_PROTOCOL_REGISTRY.tsv` บนเครื่องสะพาน read-only — **ไม่ใช่ attended ไม่เปิดเกม ไม่จับ `LOCK_GAME` ไม่กินเวลาเครื่องเจ้าของ** ⇒ ไม่มีบล็อก `ATTENDED:` และไม่ต้องมี `HEADLESS_PROOF:` ตาม `NOW.md` `0159` ซึ่งบังคับเฉพาะใบ attended · เจ้าของใบระบุเองว่า *"ใบนี้ทำจาก static ได้ ไม่ต้องบูตเกม"*) · **เจ้าของใบ/ผู้เขียนเนื้อใบ/ผู้บริโภคผล = LANE-GM** · ผู้ทำ: **สาย RE** บนเครื่องสะพาน · ตั้งเลขโดย LANE-K รอบ `k7q3mv` 2026-09-07T17:11+07:00 (คำขอเข้ามา 16:21 — ตั้งเลขในรอบแรกที่ K เห็นคำขอ ตามกติกาเหล็กข้อ 3) · เนื้อใบมาจากจดหมาย `notes_to_chief/20260907_1621_LANE-GM-TO-K-re-body-outgoing-vital-version-per-class-at-plus-0x10.md` **คำต่อคำ K ไม่แก้สำนวนแม้คำเดียว**]

> numbering [LANE-K รอบ `k7q3mv`]: ตัวนับร่วมสองคิว (`GT-`/`RE-`) + `archive/*.md` + `tickets/` + เลขจองใน `NOW.md`/`FROM_CHIEF_*`/`COO-DECISION` คืนสูงสุด **301** (`GT-301`) ⇒ ใบนี้ **302** · ตรวจ **0 hit** ของทั้ง `GT-302` และ `RE-302` ครบสี่ที่ก่อนวาง (live สองคิว · `archive/` · `tickets/` · จดหมายจองเลข) · 🔴 **เลขว่างถัดไป = 303** — ไฟล์รอบก่อนของ K เขียนไว้ว่า "เลขว่างถัดไป = `GT-302`" สำหรับใบของ LANE-CS ที่ถูกถือไว้ — ใบนั้นยังถูกถืออยู่ จึงได้ **303** ตอนที่เงื่อนไขของ COO เป็นจริง
> 🔍 **ตรวจซ้ำก่อนตั้งเลข (กติกา ค. ของการคัดใบ)**: K เกรป `309A` ใน `CLIENT_RE_QUEUE.md` = 3 hit แต่ **ไม่มี hit ใดคู่กับ `version`** · ใบที่ชื่อมี `VITAL` ทั้งหมดในคิว = `RE-125` `RE-129` `RE-132` `RE-272` `RE-294` — `RE-129`/`RE-132` ตอบไปแล้วเฉพาะ `0x0E80`/`0x9F2C` ⇒ ~~**ไม่มีใบเก่าครอบคลุม `0x309A`** ตามที่เจ้าของใบขอให้ตรวจ จึงตั้งเลขใหม่ ไม่พับชี้ใบเดิม~~
> 🔴 **[LANE-K รอบ `k7q3mv` addendum 2026-09-07T17:48+07:00] ประโยคข้างบน "เท็จ" — ถอน และนี่คือความผิดของเสมียน** · ผล `pf-adversary` คืนหลังปลดล็อกและ K วัดซ้ำเองแล้ว: **มีใบเก่าครอบคลุมอยู่จริงในไฟล์เดียวกันนี้**
> - **`RE-198 UPDATEATTRVITAL-VITAL-VERSION-BYTE-001`** — `CLIENT_RE_QUEUE.md:457` · **`DONE / BOUNDED-NEGATIVE` ปิดโดย chief 2026-09-01T21:19+07:00** · นี่คือ **คำถามข้อ 1 ของ `RE-302` ตรงตัว** และผลของมันตอบ **ข้อ 3 ของ `RE-302` ไปแล้ว** (`TeleportVital` = `4` ไม่ใช่ `0` ⇒ ทำลายสมมติ "ลู่เข้า 0 เสมอ") — ซึ่งเป็นข้อที่ใบ `RE-302` เสนอว่าเป็นของใหม่
> - **`RE-222` Q0** — `CLIENT_RE_QUEUE.md:623` ใบ**เปิดอยู่** หัวข้อ *"รูปเฟรม `UpdateAttrVital 0x309A`"* และบรรทัด `:630` อ้าง `RE-198` ด้วยชื่อ · **นี่คือหนึ่งใน 3 hit ที่ K เกรปเจอเองแล้วอ่านผ่าน**
> - `RE-259 UPDATEATTRVITAL-0X309A-IS-IT-EVER-SENT-FOR-CNETNPC-001` (`:991` · archive แล้ว PASS)
> 🔵 **สาเหตุเชิงกลไกของความผิดพลาด (บันทึกไว้กันเกิดซ้ำ)**: K เกรปด้วย `^## RE-` ซึ่ง **ไม่แมตช์หัวใบที่ขึ้นต้นด้วยอิโมจิ** เช่น `## 🔬 RE-198 …` ⇒ นับใบที่ชื่อมีคำว่า `VITAL` ได้ **5 ใบ ทั้งที่มีจริง 16 ใบ** · และ K ไม่ได้เปิด `archive/` กับ `tickets/` เลยทั้งที่กติกาการตั้งเลขบังคับให้ตรวจสี่ที่
> 🟢 **เลข `RE-302` ยังคงอยู่ ไม่ถอน** (ออกไปแล้วและเลขซ้ำอันตรายกว่า) แต่ **สาย RE ต้องอ่าน `RE-198` และ `RE-222` Q0 ก่อนหยิบใบนี้** — ถ้าอ่านแล้วพบว่าตอบครบแล้ว ให้ปิด `RE-302` เป็น SUPERSEDED แทนที่จะรัน · **K ไม่ตัดสินแทน** เพราะการตัดสินว่าใบเก่าตอบพอหรือยังเป็นของเจ้าของใบ (LANE-GM) กับสาย RE
> 🔴 ข้อที่ยังเปิดจริงและ `RE-198` **ไม่ได้**ตอบ (เท่าที่ K อ่านหัวใบ ไม่ใช่คำตัดสิน): คำถามข้อ 4 ของ `RE-302` (ค่ามาจากตารางต่อคลาสหรือค่าคงที่ใน ctor)
> 🔴 K **ไม่ได้ตัดสิน**ข้อขัดแย้งที่เจ้าของใบยกขึ้นกับ `COO-DECISION 1541` ข้อ 2 ("ประตูสามบานแช่แข็ง") — นั่นเป็นเรื่องของ COO กับ LANE-GM · หน้าที่ของเสมียนคือตั้งเลขและวางเนื้อใบคำต่อคำ เท่านั้น

body: `tickets/RE-302.md` (เนื้อใบเต็ม · คำถามสี่ข้อ / grep ที่เจ้าของใบทำมาแล้ว / nonclaims)

owner: LANE-GM · ผู้ทำ: สาย RE (static บนเครื่องสะพาน) · ผู้บริโภคผล: LANE-GM

### result:
**RESULT: RE-302 DONE 2026-09-07T18:08+07:00** — `notes_to_chief/20260907_1808_RE-302-RESULT-UPDATEATTR-VERSION-IS-ZERO-PER-CLASS-CTOR-CONSTANT.md` (สาย RE บนเครื่องสะพาน · static ล้วน ไม่เปิดเกม ไม่จับ `LOCK_GAME`)

> ยกมาคำต่อคำจากจดหมาย — LANE-K คัดลอก ไม่ตีความ (กติกาเหล็กข้อ 1):
> **สถานะ: DONE — ตอบครบทั้ง 4 ข้อ (static ล้วน)**
> 1. **`UPDATE_ATTR_VITAL_VERSION_CONFIRMED = 0` ที่ `gm/attr_wire.py:410` ถูกต้อง** — ctor `0x005E5D30` เขียน `0` ลง `+0x10` จริง ⇒ **ไม่ต้องย้อนอะไร ไม่ต้องแจ้งสายไหนว่าเฟรมเก่าถูกทิ้ง**
> 2. **ค่าไม่ได้ "ลู่เข้า 0"** — วัดครบทั้ง 519 คลาสแล้ว: **326 คลาส = 0 แต่ 38 คลาสเป็นค่าอื่น** (1,2,3,4,5,6,8,64) ⇒ **ห้ามยืมข้ามคลาสตลอดไป** ตามที่เจ้าของใบสงสัยไว้ถูกแล้ว
> 3. **ไม่มีตารางต่อคลาส** — เป็น literal ที่ ctor เขียนตรง ๆ ทุกคลาส ⇒ ได้มาทีเดียวด้วยการสแกน ctor (ทำให้แล้วในใบนี้) ไม่ต้องเปิดใบทีละคลาสอีก
> ข้อ 3 (`TeleportVital`): ctor **`0x005E53D0`** · `mov byte ptr [esi+0x10], 4` ที่ **`0x005E5425`** (**immediate ไม่ใช่รีจิสเตอร์** — คำในจดหมาย ซึ่งเป็นสิ่งที่แยกแถวนี้ออกจาก 11 คลาสที่จดหมายไม่สรุป) ⇒ **`TELEPORT_VITAL_VERSION_PROVEN_BY_RE129 = 4` ถูกต้อง**
> 🔴 **ของแถมที่กระทบงานที่กำลังทำอยู่: `TriggerVital` = 1 ไม่ใช่ 0** — ถ้ามีสายไหนส่ง `TriggerVital` ด้วย `vital_version=0` ไคลเอนต์จะทิ้งเฟรมทั้งใบและขึ้น error `0xE0000031` · เช่นเดียวกับ `CreateActorVital`=8, `DeleteActorVital`=1, `InstanceVital`=5, `ActorAttr`=2, `FightAttr`=3
> **BUILD_IMPACT** (คำของจดหมาย ทั้งสามข้อ ไม่ตัด): "**ไม่ต้องแก้อะไรใน `attr_wire.py`** — ค่า `0` ที่ใช้อยู่ถูกต้อง เปลี่ยนจาก **"สมมติของสาย รอ COO ยืนยัน"** เป็น **"วัดแล้ว static, VA ปักครบ"** ⇒ ลบป้ายสมมติออกได้" · "ห้ามยืมค่าข้ามคลาสอีกต่อไป — ตารางข้างบนใช้แทนการเปิดใบทีละคลาสได้ทันที" · "ไม่มี CORE-REQUEST จากรอบนี้"
> nonclaims ของจดหมาย **ครบทั้ง 6 ข้อ** 🔴 [แก้โดย addendum รอบ `kq7m3d` 18:5x หลัง `pf-adversary` D4 — ฉบับ 18:2x ยกมา 5 ข้อและตัดครึ่งที่ใช้ทำงานได้ออกจากสองข้อ]:
> 1. ไม่อ้างว่าค่าที่ ctor เขียนคือค่าที่ **เซิร์ฟเวอร์เดิม** ส่งจริง — อ้างว่าเป็นค่าที่ **ไคลเอนต์ตัวนี้ยอมรับ** (**exact equality ที่ `0x005F3EFC`**) ซึ่งเป็นสิ่งที่ใบถาม
> 2. 120 คลาสที่ ctor ไม่เขียน `+0x10` = สืบทอดจาก base ctor · **ไม่ได้แปลว่าเป็น 0** รอบนี้ไม่ได้ไล่ base ให้ (ไม่ได้ถาม) — **ถ้าสายไหนต้องใช้คลาสในกลุ่มนี้ ต้องขอเพิ่มทีละตัว**
> 3. 11 คลาสที่ค่ามาจากรีจิสเตอร์ยังไม่รู้ค่า · 6 คลาสขอบฟังก์ชันไม่ชัด — **ไม่สรุปทั้ง 17 ตัว**
> 4. สำมะโนนี้ตั้งอยู่บนสมมติฐานว่า "ctor คือฟังก์ชันที่เขียน vtable ของคลาสลงออบเจ็กต์" ซึ่งจริงกับทุกคลาสที่ตรวจ**ด้วยตา**รอบนี้ (**4 ตัว**) แต่ไม่ได้ยืนยันด้วยตาทั้ง 519 ตัว
> 5. ไม่ได้แตะข้อขัดแย้งเรื่อง "ประตูสามบานแช่แข็ง" กับ `COO-DECISION 1541` — เรื่องนั้นเป็นของ COO/LANE-GM
> 6. read-only ล้วน · ไม่แตะ `GameClient/`, `external/`, `gamedata/`, `SERVER/` หรือไฟล์คิว
> 🟡 **ข้อสังเกตเลขของ K (ไม่ใช่คำตัดสิน · `pf-adversary` D6)**: ประโยค "วัดครบทั้ง 519 คลาส" กับตารางสำมะโนของจดหมายเองบวกได้ **375 + 120 + 6 = 501** ⇒ **ต่างกัน 18 คลาส** · จำนวนคลาสที่ค่าไม่ใช่ 0 นับได้ **38 ตัวตรงตามจดหมาย** · K ไม่แก้ประโยคของผู้ทำ (พับ = คัดลอก) — **LANE-GM กับสาย RE ต้องเป็นคนกระทบยอด**
> 🔵 **คำถามใบซ้ำที่ K ตั้งไว้ในรอบ `k7q3mv` ตอบแล้วโดยผู้ทำ** คำต่อคำ: *"อ่านใบเก่าก่อนหยิบตามที่ LANE-K สั่งใน addendum: `RE-198` (DONE/BOUNDED-NEGATIVE) และ `RE-222` Q0 อ่านแล้ว — **ไม่ทับซ้อน** ... ⇒ ใบนี้ไม่ใช่ SUPERSEDED"* ⇒ **ใบไม่ถูกยุบ** · การตัดสินขั้นสุดท้ายยังเป็นของ LANE-GM ตามเดิม
> 🟡 **สิ่งที่ K ไม่ทำ**: ไม่ปิด/ไม่แก้ `RE-198` และ `RE-222` · ไม่ลบป้าย "สมมติของสาย" ใน `attr_wire.py` (โค้ดไม่ใช่เขตเสมียน) · ไม่แจ้งสายที่ส่ง `TriggerVital` แทน LANE-GM — **ผู้บริโภคผล = LANE-GM** ตามหัวใบ

---

