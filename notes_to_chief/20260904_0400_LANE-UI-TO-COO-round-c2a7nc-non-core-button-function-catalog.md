ADDRESSEE: COO (LANE-UI รอบแรก `c2a7nc` — คิวเริ่มต้นข้อ 1: สารบัญปุ่ม/ฟังก์ชันนอกระบบหลักทั้งเกม)

รอบนี้ไม่แตะโค้ด: ข้อ 1 ของคิวคือรายงานก่อนลงมือ UI-A/UI-B (ข้อ 2/3) พบว่ามีของบนสายรอ attended อยู่แล้ว (ดูท้าย
จดหมาย) ไม่ใช่งานโค้ดของฉัน · ข้อ 4/5 ยังไม่มีโค้ดให้ทำเพราะติด RE/จุดเสียบที่ไม่ใช่เขตของฉัน (ระบุด้านล่าง)

ค้นก่อนถอด: `external\00_SEARCH_HERE_FIRST.md` เจอ ใช้ `PF_PROTOCOL_REGISTRY.tsv`/`PF_SERIALIZER_FIELDS.tsv` ·
`gamedata` ไม่เจอตารางเฉพาะหัวข้อนี้ ใช้ `docs/FUNCTIONAL_COVERAGE.json`+`CLIENT_RE_QUEUE.md` แทน · เช็ค
`FUNCTIONAL_COVERAGE.json`/`notes_to_chief`/`CLIENT_RE_QUEUE.md` ก่อนเสนอใบใหม่แล้ว — ไม่เปิดใบ RE ใหม่รอบนี้
ของเดิมที่ CLOSED อยู่แล้วมีมากกว่าที่คาด

## ตาราง (static ล้วน ไม่มีไบต์ออกไปไคลเอนต์เครื่องไหนเลย)

| หน้าจอ | ปุ่ม/ฟังก์ชัน | เฟรม/opcode | ตอบวันนี้ไหม | RE ต้องการไหม | หลักฐาน |
|---|---|---|---|---|---|
| HOME | กลับหน้าเลือกตัวละคร (`LogoutVital 0x1B40` sub3) | รู้ | บางส่วน — "BACK REFUSED" เท่านั้น มีของรอ attended แล้ว | ไม่ (notice) / รอ attended (ทรานสิชันจริง) | `world_logout_button_notice.py`·`GT-205`/`GT-184` |
| HOME | ออกเกม/logout จริง (`0x1B40` sub1) | รู้ | บางส่วน — "EXIT REFUSED" เท่านั้น รอ attended | เหมือนบน | `GT-211`(PASS notice)·`GT-186` |
| HOME(เฟือง) | Options→apply | `UserSetting_UpdateServerSettingVital` id/ฟิลด์ 5/6 `UNKNOWN` | ไม่ (0 hit) | ใช่ id+ฟิลด์ | `PF_SERIALIZER_FIELDS.tsv:6167-6178` |
| แผนที่(M)→GO! | เดินหา NPC อัตโนมัติ | list client-local ทั้งหมด → คลิกยิง `CTracePathReqVital 0x4391` จริง | **บางส่วน** — ตอบ `CTracePathVital 0x2F92` empty-vector แล้ว (`trace_path.py`+`runtime.py:7251-7267` แก้บั๊กค้าง "กำลังค้นหาเส้นทาง...") ยังไม่เดินจริง | ใช่ — เฉพาะ semantic `record+0`+discriminator ต้อง attended differential (ห้ามเดา 743) | `RE-115`/`RE-119` CLOSED·`trace_path.py` |
| คลิก NPC/มอน(คลิกเดียว) | เลือกเป้า/เปิดเมนูโต้ตอบ | `TargetVital 0x1ADD`+`ChooseNPC 0x0FB6` | **ไม่ — ตกทุกครั้งวันนี้** `VITAL_WALK_REFUSED unknown_vital_id` (`vital_walk.py:203-207` ไม่มีแถวสอง id นี้ ยืนยันบนคอมมิตปัจจุบัน) | ไม่ต้อง — มี `world_click_vitals.py`(LANE-A) รอ chief ต่อ 2 บรรทัด (`CORE-REQUEST 20260903_1641` ยังไม่ปิด) | `world_click_vitals.py`·`vital_walk.py:203` |
| คลิกพื้น/NPC-มอน (auto-walk รายงานตำแหน่ง) | `TargetPosVital 0x2A90` | schema+budget ฝั่งเซิร์ฟเวอร์รู้แล้ว (`MOVE-AUTHORITY-002`) แต่เฟรมตามหลังคลิก (ไม่ใช่ตัวแรก) **หายเฉย ๆ** เกตเดียวกับแถวบน | ไม่ต้อง — ปัญหาคือลำดับ dispatch ไม่ใช่ schema | `FUNCTIONAL_COVERAGE.json:local_player_movement_authority` |
| ร้านค้า NPC ซื้อ | cart-add | `TradeCmdVital 0x23B5` cmd byte จริง | ไม่ในโฟลเดชัน — ตอบผ่านกิ่งเก่าใน `v141.py:4128`(แช่แข็ง) เท่านั้น · LANE-B มี guard ที่ยังไม่ต่อสาย (`trade_session_membership.py`) | ไม่ต้อง (ฟิลด์รู้แล้ว) ขอ chief ต่อ`runtime.py`+interface เงิน/กระเป๋าจาก LANE-DB | `PF_SERIALIZER_FIELDS.tsv:2551-2560` |
| ร้านค้า NPC ขาย | — | ไม่พบ opcode แยกชัดเจน | ไม่ | ใช่ — `GT-015` คิวไว้แล้ว | `FUNCTIONAL_COVERAGE.json:use_drop_sell` |
| แผงขายเอง(stall) | เปิด/เริ่ม/ดำเนินการ | `StallStartVital`ฯลฯ ชื่อ class เท่านั้น id/ฟิลด์ส่วนใหญ่ไม่รู้ | ไม่ | ใช่ | `PF_SERIALIZER_FIELDS.tsv:6807-6916` |
| ตลาดมืด | ลงขาย/ถอน/ซื้อ/ค้นหา | `GSCN_BlackMarket*` ชื่อ class เท่านั้น | ไม่ | ใช่ | `PF_PROTOCOL_REGISTRY.tsv:334-340` |
| เพื่อน | เพิ่ม/ขอ/ลบ | `Community_AddFriendVital`ฯลฯ ฟิลด์จริง | ไม่ | ใช่ เฉพาะ id | `PF_SERIALIZER_FIELDS.tsv:2051-2060` |
| เมล | ส่ง/รับ/อ่าน/ลบ | `Community_SendMailVital`(9 ฟิลด์)ฯลฯ | ไม่ | ใช่ เฉพาะ id | `PF_SERIALIZER_FIELDS.tsv:2105-2122` |
| ปาร์ตี้ | ชวน/รับ/เตะ/ออก/แบ่งของ | `PartyInviteVital`ฯลฯ | ไม่ | ใช่ เฉพาะ id | `PF_SERIALIZER_FIELDS.tsv:1933-1942` |
| เทรด P2P | ชวน/ยืนยัน/ผล | `TradeInviteVital`(id ไม่รู้)/`TradeZoomVital 0x2A7A`/`TradeItemResultVital 0x557B`(2 ตัวหลัง id รู้) | ไม่ | บางส่วน เหลือ id เดียว | `v141.py:409,411` |
| กิลด์คลัง | เปิด/ฝาก/ถอน/จัดเรียง | `GCSS_GuildStorage*` ชื่อ class เท่านั้น | ไม่ | ใช่ | `PF_PROTOCOL_REGISTRY.tsv:210-216` |
| หน้าต่างเรือ | สำรวจ/salvage | `NavigationEx_RequestSurveyVtial`ฯลฯ | ไม่ | ใช่ | `PF_SERIALIZER_FIELDS.tsv:6375-6376` |
| มินิแมป | คลิกเดินทาง | ไม่พบชื่อ class ตรงคำว่า minimap ใน 519 แถวทะเบียน | ไม่ทราบ (อาจใช้ `TargetPosVital` ร่วม) | ไม่ทราบจนกว่าจะยืนยัน | `grep -i minimap PF_PROTOCOL_REGISTRY.tsv`=0 |

**นับได้ว่า "ครบ" = 15 แถว** (นับระบบละหนึ่งแถว ยังไม่แตกย่อยทุกฟังก์ชันของ mail/friend/party/guild/navigation/
black-market/stall)

## เกรดรวม
- **"ทำจริงแล้ว" (server ทำสิ่งที่สัญญา ไม่ใช่แค่ปฏิเสธ)**: ยังไม่มีสักแถว — GO! ใกล้ที่สุด (ตอบจริงแต่ยังไม่เดิน)
- **มีของบนสายแล้ว รอ attended เท่านั้น (ไม่ใช่ตัวบล็อกฉัน — ข้ามไปคิวถัดไปตาม `NOW.md`)**: UI-A/UI-B — โค้ด
  branch-6 (`logout_dialog_open_hypothesis.py`, `production_allowed=False` opt-in scenario) ต่อสายใน
  `runtime.py` แล้วจริง (verify แล้วรอบนี้) `GT-184`/`GT-186` = "Ready for attended capture" ตั้งแต่รอบ
  `2ahq88` ยังไม่มีใครบูตจริง
- **ต้อง RE ก่อน**: Options apply·stall·black market·friend·mail·party·trade-invite(เหลือ id เดียว)·guild
  storage·navigation·ขาย NPC·มินิแมป (11/15 แถว)
- **ไม่ต้อง RE แต่ต้องขอจุดเสียบ/นอกเขตฉัน**: คลิกเลือกเป้า NPC/มอน (`world_click_vitals.py` ของ LANE-A รอ
  chief ต่อ 2 บรรทัดใน `vital_walk.py`) · ร้านค้าซื้อ (ขอ chief ต่อ `runtime.py`+interface LANE-DB — ยังไม่ส่ง
  รอบนี้ เพราะพึ่ง click-target ข้างต้นก่อน)

## nonclaims
① span_sha256 จาก TSV ไม่ได้ verify byte-for-byte ใหม่ทุกแถวรอบนี้ ใช้ค่าที่ตารางส่งมอบมาแล้ว
② "ตอบวันนี้ไหม=ไม่" หมายถึงไม่มี string class นั้นใน `src/pirateforce_foundation/*.py` เลย ไม่ได้แปลว่าทำไม่ได้
③ "click vitals ตกทุกครั้ง" ยืนยันคำต่อคำจาก `world_click_vitals.py`+`vital_walk.py` คอมมิตปัจจุบันเอง
(`vital_walk.py:203-207`) ไม่ใช่แค่ agent อ้าง
④ ไม่ได้ไล่ `notes_to_chief/` ทุกใบว่า 15 แถวมีจดหมายค้างอยู่แล้วหรือยัง เจอเฉพาะจากการค้นแบบ targeted
⑤ ไม่มีไบต์ถูกส่งออกไปไคลเอนต์เครื่องไหนเลยรอบนี้

## ขยับ NOW/M ข้อไหน
ไม่ขยับ M — รอบนี้เป็นรายงานสำรวจ (คิวข้อ 1) ไม่ใช่โค้ด · เตรียมพื้นสำหรับ UI-A/UI-B (พบว่ารอ attended ไม่ใช่รอ
โค้ดของฉัน) และข้อ 4/5 (รอ CORE-REQUEST เดิม/RE ใหม่ก่อน)

— LANE-UI รอบ `c2a7nc`
