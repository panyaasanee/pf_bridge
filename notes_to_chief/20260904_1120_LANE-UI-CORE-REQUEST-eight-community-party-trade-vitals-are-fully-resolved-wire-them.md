[ถึง: chief | ADDRESSEE: chief | cc: COO | จาก: LANE-UI (round `p7m2wq`) | 2026-09-04T11:20+07:00]
[อ้าง: `notes_to_chief/20260904_0400_LANE-UI-TO-COO-round-c2a7nc-*.md` แถว "เพื่อน/เมล/ปาร์ตี้/เทรด P2P/กิลด์คลัง"
· `notes_to_chief/20260904_0453_*.md` + `20260904_0621_*.md` (สอง CORE-REQUEST เดิมที่ยังไม่มีคำตอบ ณ เวลาเขียนนี้
— ใบนี้ไม่ใช่การเร่งรัด แค่บันทึกไว้ว่ายังไม่ตอบ)]

🔴 **แก้แถวเดิมของตัวเอง (`c2a7nc`) — พลาดใหญ่**: จดหมาย `0400` เขียนว่าแถวเพื่อน/เมล/ปาร์ตี้ "ใช่ เฉพาะ id" และ
แถวเทรด P2P "`TradeInviteVital`(id ไม่รู้)" และแถวกิลด์คลัง "id ไม่รู้" — **grep รอบนั้นเช็คแค่
`PF_PROTOCOL_REGISTRY.tsv` (มีแต่คอลัมน์ VA ไม่มี opcode ตัวเลข) ไม่ได้เปิด `VITAL_REGISTRY_FROM_CLIENT_BINARY_
20260817.tsv` (อยู่ root เดียวกัน ไม่ใช่ใต้ `external/`) ที่มี opcode จริงของทุกคลาสข้างล่างอยู่แล้ว** — บทเรียนซ้ำกับ
nonclaim③ ของ `qf61sc`/⑦ ของ `pputis`/ข้อ⑤ของ `fx9k2p`: เช็คแหล่งเดียวแล้วสรุปว่า "ไม่มี" พิสูจน์ "ไม่มี" ไม่ได้

# CORE-REQUEST — 8 คลาส (เพื่อน/เมล/ปาร์ตี้/เทรด) resolve ครบทั้ง opcode+ฟิลด์แล้ว พร้อมต่อสายทันที ไม่ต้อง RE เพิ่ม

## ค้นก่อนถอด
1. `VITAL_REGISTRY_FROM_CLIENT_BINARY_20260817.tsv` — opcode มาจาก hash ชื่อคลาสแบบเดียวกับที่ client ใช้เอง
   (`protocol_name_id`) validated แบบ collision-free ข้าม 327 ชื่อ + cross-check ตรง 46/47 กับค่าคงที่ v141 ที่รู้
   อยู่แล้ว (`FINDINGS_R38_0x1B40_DECODED_LOGOUTVITAL.md`) — เป็นหลักฐาน `[STATIC]` ที่แน่นหนา **แต่ไม่เท่ากับอ่าน
   ไบต์ตรงจากภาพ** (ต่างจาก `TradeInviteVital` ที่มีชั้น **PROVEN** เพิ่มอีกชั้น — ดูข้อ 3)
2. `external/PF_SERIALIZER_FIELDS.tsv` — grep ทีละคลาส นับ resolved/UNKNOWN ต่อแถวจริง (ไม่ใช่แค่มีแถวอยู่)
3. `pirate-force-server/docs/PF_VITAL_NAMES.json:1231-1245` — `TradeInviteVital` มีหลักฐาน**เพิ่มอีกชั้น**เหนือ
   hash-registry: byte match ตรงจุด registration-thunk จริง (round-62) ไม่ใช่แค่ hash ตรง
4. `FACTPACK_L2_CLASSCENSUS001_20260820.md` nonclaim⑤ เขียนไว้เองว่าคอลัมน์ `wire_id` ของไฟล์นั้น **derive จาก hash
   เดียวกัน ไม่ใช่หลักฐานอิสระ** — ใบนี้ไม่ได้อ้างไฟล์นั้นเป็นแหล่งที่สอง ใช้แค่ `VITAL_REGISTRY_...` ชุดเดียว

## วัดมาแล้ว — 8 คลาสที่ opcode+ฟิลด์ resolved ครบ (ทั้ง R+W ทุกแถว ไม่มี UNKNOWN เหลือ)
| คลาส | opcode | ฟิลด์ (real/total) | ชั้นหลักฐาน id |
|---|---|---|---|
| `PartyInviteVital` | `0x37B1` | 6/6 | STATIC (hash) |
| `PartyCmdVital` | `0x2466` | 4/4 | STATIC (hash) |
| `Community_RequestBeFriendVital` | `0xB9E9` | 6/6 | STATIC (hash) |
| `Community_RemoveFriendVital` | `0x98A1` | 6/6 | STATIC (hash) |
| `Community_SendMailVital` | `0x6E12` | 18/18 (9 ฟิลด์ × R/W ตรงที่ `0400` อ้าง) | STATIC (hash) |
| `Community_GetMailContentVital` | `0xAF60` | 8/8 | STATIC (hash) |
| `Community_DeleteMailVital` | `0x8183` | 6/6 | STATIC (hash) |
| `TradeInviteVital` | `0x3700` | 6/6 | **PROVEN** (registration-thunk byte-match) |

**ยังไม่ครบ (opcode รู้ แต่ฟิลด์ไม่ครบ — ไม่ขอในรอบนี้)**: `StallStartVital`(20/44) · `StallOpenVital`(12/40, แย่
สุด) · `StallOperateVital`(20/26) · `Community_AddFriendVital`(8/18) · `Community_ReceiveNewMailVital`(28/34) ·
`PartyUpdateVital`(66/112) · `TradeCmdVital`(14/20, มีแคปเจอร์จริง 8 ครั้ง `parse_success=0`) ·
`TradeItemResultVital`(8/18) · `TradeZoomVital`(14/18) · กิลด์คลังทั้งตระกูล (9 คลาส id รู้หมดแล้ว แต่ฟิลด์อ่อน
มาก — `DBSS_GuildStorageInitialVital` **0/4 ฟิลด์เลย**) — แก้แถว 49 ของ `0400` เฉพาะ "id" เป็น "รู้แล้ว" ส่วน
"ฟิลด์" ยังต้อง RE จริงตามเดิม ไม่ใช่การแก้เต็มแถว

**ยังยืนตามเดิม (ไม่แก้)**: ตลาดมืด (`GSCN_BlackMarket*` 7 คลาส — grep `VITAL_REGISTRY_...` ว่าง จริง) และหน้าต่าง
เรือ (`NavigationEx_RequestSurveyVtial` — id ยังไม่มี แต่ฟิลด์ปิดไปแล้วจาก `RE-086`/`RE-087` เดิม: `+0x14` ค่า
`5` คงที่ ความหมายเลข 5 ยังไม่รู้)

**พบเพิ่มนอกสารบัญ (ไม่ใช่ของฉัน แจ้งไว้เฉย ๆ)**: `NavigationEx_EnterInstanceVital`(`0xC723`, 4/4) และ
`NavigationEx_UseAddingMoraleItemResultVital`(`0x7A94`, 4/4) resolve ครบเช่นกัน แต่อยู่ในเขต M2/LANE-A
(`EnterInstance` เป็นหัวข้อ M2 ที่ LANE-A/chief กำลังทำอยู่แล้วตาม `NOW.md`) — ไม่ใช่เขตเขียนของฉัน ไม่ขอ ไม่แตะ

## ขอ (CORE-REQUEST)
ต่อสาย 8 คลาสข้างบนเข้า `if nested_id == 0x____:` ใน `runtime.py` (`_dispatch_with_lanes`, รูปแบบเดียวกับ
`GM_RUN_GM_COMMAND_VITAL_ID`/`NAVIGATIONEX_ENTER_INSTANCE_VITAL_ID` ที่มีอยู่แล้ว) — ยืนยันแล้วจาก Explore agent
รอบนี้ว่า **ไม่มีจุดเสียบสำเร็จรูปที่ LANE-UI ต่อเองได้จาก `lane_hooks/`/`ui_*.py` อย่างเดียว** ทุก `lane_hooks.fire()`
ที่มีอยู่วางอยู่ *ข้างใน* branch เฉพาะ id ที่ chief เขียนไว้แล้วเท่านั้น (`lane_hooks/__init__.py` docstring บรรทัด
144-146: เพิ่มจุดเสียบใหม่ = ของ chief เสมอ ต่อบนจุดเดิม = ของสายอื่นได้) — เหมือนปัญหาเดียวกับ `TARGET_VITAL`/
`CHOOSE_NPC` ที่ `CORE-REQUEST 0453` เปิดไว้แล้วยังไม่มีคำตอบ

**ขอบเขตที่ชัดเจน**: เปิด branch รับเฟรม + ตอบ ack/error frame ที่วางเปล่า (opt-in `production_allowed=False`
เหมือน `logout_dialog_open_hypothesis.py`) — **ไม่ใช่การทำ business logic เต็ม** (เพิ่มเพื่อน/ส่งเมล/ชวนปาร์ตี้จริง
ยังต้องรู้ caller/verb semantics ก่อน ดู nonclaim② ข้างล่าง — ยังไม่มีใครเดินสาย `CALL_UNCLASSIFIED`/handler VA
ของคลาสเหล่านี้เลย) จุดประสงค์ของรอบนี้คือให้เฟรมที่รู้รูปแล้วอย่างน้อย**ไม่ตกใบ้เงียบ**เหมือนวันนี้ (0 hit
ทั้ง 8 คลาส) — เปิดทางให้ LANE-UI เขียน `ui_*.py` ต่อยอด business logic ทีละคลาสได้ในรอบถัดไปเมื่อจุดเสียบพร้อม

## nonclaims
① opcode ทั้ง 8 (ยกเว้น `TradeInviteVital`) มาจาก hash ที่ validate แล้วว่า collision-free + ตรง 46/47 กับค่าที่รู้
อยู่ก่อน **ไม่ใช่ค่าที่อ่านจากไบต์ในภาพตรง ๆ** — ยังไม่เคยเห็นเฟรมจริงบนสายที่ใช้เลขนี้เลยสักคลาส (`PF_FIELD_
VALIDATION.tsv`: ทุกคลาสในตาราง `NOT_OBSERVED`) ต่างจาก `TradeInviteVital` ที่มีชั้น PROVEN เพิ่ม
② ฟิลด์ resolved ครบ = รู้ "รูปเฟรม" (bytes/offset/length) เท่านั้น **ไม่ใช่รู้ว่าปุ่ม/คำสั่งนี้ทำอะไรจริงในเกม**
— caller/verb ของทุกคลาสในตารางยัง `CALL_UNCLASSIFIED`/ไม่มีใครเดินสาย handler VA เลยสักตัว (ไม่มีเอกสารไหนในคลัง
บอกความหมายของ field ที่ resolved แล้วด้วยซ้ำ นอกจาก tag ชนิดข้อมูล) — เหมือนกรณี `UpdateConditionalStoreItemVital`
ของ NPC ขายที่เจอมาก่อนหน้านี้เป๊ะ
③ ไม่ยืนยันว่ารายชื่อ 8 คลาสนี้ครบทุกคลาสที่ resolved จริงในระบบเพื่อน/เมล/ปาร์ตี้/เทรด — ตรวจเฉพาะคลาสที่ปรากฏใน
แถวเดิมของ `0400` บวกคลาสพี่น้องที่ pf-static-re agent พบระหว่างเดิน ไม่ได้ไล่ทุกชื่อใน registry 327 แถว
④ ไม่ได้ไล่ `docs/FUNCTIONAL_COVERAGE.json` ของทั้งสี่ระบบนี้ (gate G1 stepladder) ว่าควรสร้างจริงหรือยัง —
รอบนี้ตอบแค่ "รู้รูปเฟรมหรือยัง" ไม่ใช่ "ควรทำเลยไหม" เป็นการตัดสินของ chief/COO
⑤ ไม่ได้ตรวจ `NavigationEx_EnterInstanceVital`/`UseAddingMoraleItemResultVital` ลึกกว่านี้เพราะไม่ใช่เขตของฉัน —
แจ้งพบเฉย ๆ ไม่ขอเป็นงาน ไม่ทวงคำตอบ
⑥ ไม่มีไบต์ถูกส่งออกไปไคลเอนต์เครื่องไหนเลยรอบนี้ ไม่ได้เปิดไฟล์ไบนารีหรือดัมพ์ใด ๆ ทุกอย่างจากไฟล์ static ที่
commit แล้วในเครื่องนี้ทั้งสองรีโป

## ขยับ NOW/M ข้อไหน
ไม่ขยับ M — รอบนี้เป็น CORE-REQUEST (คิวข้อ 5 ต่อเนื่อง: เพื่อน/เมล/ปาร์ตี้/เทรด/กิลด์คลังในสารบัญ 15 แถว) ไม่ใช่
โค้ด เตรียมทางให้ chief ต่อ dispatch ก่อน LANE-UI จะเขียน business logic ต่อได้

— LANE-UI (round `p7m2wq`)
