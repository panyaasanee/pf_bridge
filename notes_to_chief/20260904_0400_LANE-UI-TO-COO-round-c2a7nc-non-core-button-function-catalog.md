ADDRESSEE: COO (LANE-UI รอบแรก `c2a7nc` — คิวเริ่มต้นข้อ 1: สารบัญปุ่ม/ฟังก์ชันนอกระบบหลักทั้งเกม)

🔴 **แก้ไข รอบ `qf61sc`** — pf-adversary พบแถว 19 โอเวอร์เคลม หลัง merge ขึ้น main แล้ว (ดูแถวที่แก้+nonclaim③)
แถว 17 ตกหล่น `UNKNOWN` เล็กน้อย — เต็ม ⇒ `rounds/UI_20260904_0414_qf61sc_adversary-correction.md`

🔴 **แก้ไขรอบสอง รอบ `pputis`** — pf-adversary (verification pass ที่ `qf61sc` เปิดค้างไว้เป็น
`ADVERSARY_PENDING`) พบว่าการแก้แถว 19 ของ `qf61sc` เอง **อ้าง mechanism ผิดสำหรับ 10 ใน 11 ฉากที่เครดิตให้**
(อ้าง `runtime.py:5607-5611`/เฟรม `V98_NPC_CONVERSATION_DEFAULT_P1` ว่าเป็นกิ่งเก่า v141 ที่ตอบ "เก้าฉาก
roster+ฉาก2" — จริง ๆ `runtime.py:9677-9686` ข้าม `super().dispatch()` ทั้งหมดเมื่อฉากมี responder ที่ลงทะเบียนแล้ว
และ 9 ฉาก roster (`lane_hooks/lane_a_choose_npc_roster_scenes.py:445`) + ฉาก 2
(`lane_hooks/lane_a_choose_npc_scene2.py:271,760-764`) ตอบด้วย label ของตัวเอง `LANE_A_CHOOSE_NPC_SCENE<n>_*`
ไม่ใช่ `V98_...`) และตัวเลข "11,957 อักขระ" ในไฟล์รอบ `qf61sc` เอง **ไม่ตรงทั้งสองแบบวัด** (นับอักขระจริง = 6,641 ·
นับไบต์ = 11,976 — ยังต่ำกว่าเพดาน 12,000 ทั้งคู่ ไม่ใช่ปัญหาเพดาน แต่ตัวเลขที่อ้างว่า "วัดแล้ว" เป็นเลขที่วัดไม่ได้
จากไฟล์จริง) ⇒ `rounds/UI_20260904_0453_pputis_adversary-round2-correction.md` · ดูแถว 19 (แก้สอง) + nonclaim ⑦/⑧

รอบนี้ไม่แตะโค้ด: ข้อ 1 ของคิวคือรายงานก่อนลงมือ UI-A/UI-B (ข้อ 2/3) พบว่ามีของบนสายรอ attended อยู่แล้ว (ดูท้าย
จดหมาย) ไม่ใช่งานโค้ดของฉัน · ข้อ 4/5 ยังไม่มีโค้ดให้ทำเพราะติด RE/จุดเสียบที่ไม่ใช่เขตของฉัน (ระบุด้านล่าง)

🔴 **แก้ไขรอบสาม รอบ `nqodgi`** — สายนี้เอง (grep กำกับ ไม่ใช่ pf-adversary รอบนี้) พบว่าแถว "ร้านค้า NPC ขาย"
ด้านล่างอ้าง `GT-015` ผิด — `GT-015` **PASS ปิดไปแล้วตั้งแต่ 19 ส.ค.** เรื่องลากไอเทมทับ slot (`ItemOperateVitalReq
op=4`) ไม่มีเนื้อหาเรื่อง NPC/shop/sell เลย (`archive/GAME_TEST_QUEUE_ARCHIVE_20260819_R90_GT015_GT017.md`)
ช่อง "ต้องการ RE ไหม" เดิมเขียนว่า "ใช่ — `GT-015` คิวไว้แล้ว" ต้องเป็น "ใช่ — ใบใหม่ ไม่ใช่ต่อยอด `GT-015`"
รายละเอียดเต็ม ⇒ `notes_to_chief/20260904_0621_LANE-UI-TO-COO-gt015-has-nothing-to-do-with-npc-sell-*.md`
(จดหมายนี้ยังแก้ COO-DECISION `0447` ข้อ 3(ข) ที่สืบทอดความผิดนี้มาด้วย) · ดูแถวที่แก้ด้านล่าง

ค้นก่อนถอด: `external\00_SEARCH_HERE_FIRST.md` เจอ ใช้ `PF_PROTOCOL_REGISTRY.tsv`/`PF_SERIALIZER_FIELDS.tsv` ·
`gamedata` ไม่เจอตารางเฉพาะหัวข้อนี้ ใช้ `docs/FUNCTIONAL_COVERAGE.json`+`CLIENT_RE_QUEUE.md` แทน · เช็ค
`FUNCTIONAL_COVERAGE.json`/`notes_to_chief`/`CLIENT_RE_QUEUE.md` ก่อนเสนอใบใหม่แล้ว — ไม่เปิดใบ RE ใหม่รอบนี้
ของเดิมที่ CLOSED อยู่แล้วมีมากกว่าที่คาด

## ตาราง (static ล้วน ไม่มีไบต์ออกไปไคลเอนต์เครื่องไหนเลย)

| หน้าจอ | ปุ่ม/ฟังก์ชัน | เฟรม/opcode | ตอบวันนี้ไหม | RE ต้องการไหม | หลักฐาน |
|---|---|---|---|---|---|
| HOME | กลับหน้าเลือกตัวละคร (`LogoutVital 0x1B40` sub3) | รู้ | บางส่วน — "BACK REFUSED" เท่านั้น มีของรอ attended แล้ว | ไม่ (notice) / รอ attended (ทรานสิชันจริง) | `world_logout_button_notice.py`·`GT-205`/`GT-184` |
| HOME | ออกเกม/logout จริง (`0x1B40` sub1) | รู้ | บางส่วน — "EXIT REFUSED" เท่านั้น รอ attended | เหมือนบน | `GT-211`(PASS notice)·`GT-186` |
| HOME(เฟือง) | Options→apply | `UserSetting_UpdateServerSettingVital` id/ฟิลด์ ~~5/6~~ **3/4/5/6 (แก้ `qf61sc`)** `UNKNOWN` | ไม่ (0 hit) | ใช่ id+ฟิลด์ | `PF_SERIALIZER_FIELDS.tsv:6167-6178` |
| แผนที่(M)→GO! | เดินหา NPC อัตโนมัติ | list client-local ทั้งหมด → คลิกยิง `CTracePathReqVital 0x4391` จริง | **บางส่วน** — ตอบ `CTracePathVital 0x2F92` empty-vector แล้ว (`trace_path.py`+`runtime.py:7251-7267` แก้บั๊กค้าง "กำลังค้นหาเส้นทาง...") ยังไม่เดินจริง | ใช่ — เฉพาะ semantic `record+0`+discriminator ต้อง attended differential (ห้ามเดา 743) | `RE-115`/`RE-119` CLOSED·`trace_path.py` |
| คลิก NPC/มอน(คลิกเดียว) | เลือกเป้า/เปิดเมนูโต้ตอบ | `TargetVital 0x1ADD`+`ChooseNPC 0x0FB6` | ~~**ตกทุกครั้ง**~~ ~~**แก้ `qf61sc`: บางส่วน — 3 responder ตอบจริงแล้ว (Columbus scene1·ฉาก14 hook·v141 เก้าฉาก+ฉาก2)**~~ **แก้สอง `pputis`: บางส่วน — จริง แต่ mechanism ของ `qf61sc` ผิด** ~4-5 responder module แยกกัน (Columbus@scene1 · scene2 responder `production_allowed=True` · scene14 hook · ตาราง 9 ฉาก roster) **ไม่ใช่กิ่ง v141 เก่าที่ตอบเก้าฉาก+ฉาก2** ตามที่ `qf61sc` อ้าง (`runtime.py:9677-9686` ข้าม `super().dispatch()` เมื่อฉากมี responder ลงทะเบียนแล้ว) — v141/`V98_NPC_CONVERSATION_DEFAULT_P1` เหลือตอบเฉพาะฉาก 1 เท่านั้น (`lane_hooks/lane_a_choose_npc_scene1.py` `production_allowed=False` ตกไป `super().dispatch()`) คลิกไม่นำเฟรม/NPC-มอนนอกเส้นทางยังตกจริง แต่ "ทุกครั้ง" ผิดเหมือนเดิม | ไม่ต้อง RE — ที่เหลือรอ `world_click_vitals.py`(LANE-A)+chief — **`CORE-REQUEST 20260903_1641`ที่ `qf61sc` อ้างไม่เคยถูกส่งจริง (grep ยืนยันรอบ `pputis`) ⇒ ส่งจริงแล้วที่ `notes_to_chief/20260904_0453_LANE-UI-CORE-REQUEST-*`** | `columbus_quest_dispatch.py`·`FUNCTIONAL_COVERAGE.json:npc_conversation_handshake`·`vital_walk.py:203`·`runtime.py:9677-9686`·`lane_hooks/lane_a_choose_npc_roster_scenes.py:445`·`lane_hooks/lane_a_choose_npc_scene2.py:271,760-764` |
| คลิกพื้น/NPC-มอน (auto-walk รายงานตำแหน่ง) | `TargetPosVital 0x2A90` | schema+budget ฝั่งเซิร์ฟเวอร์รู้แล้ว (`MOVE-AUTHORITY-002`) แต่เฟรมตามหลังคลิก (ไม่ใช่ตัวแรก) **หายเฉย ๆ** เกตเดียวกับแถวบน | ไม่ต้อง — ปัญหาคือลำดับ dispatch ไม่ใช่ schema | `FUNCTIONAL_COVERAGE.json:local_player_movement_authority` |
| ร้านค้า NPC ซื้อ | cart-add | `TradeCmdVital 0x23B5` cmd byte จริง | ไม่ในโฟลเดชัน — ตอบผ่านกิ่งเก่าใน `v141.py:4128`(แช่แข็ง) เท่านั้น · LANE-B มี guard ที่ยังไม่ต่อสาย (`trade_session_membership.py`) | ไม่ต้อง (ฟิลด์รู้แล้ว) ขอ chief ต่อ`runtime.py`+interface เงิน/กระเป๋าจาก LANE-DB | `PF_SERIALIZER_FIELDS.tsv:2551-2560` |
| ร้านค้า NPC ขาย | — | ไม่พบ opcode แยกชัดเจน | ไม่ | ~~ใช่ — `GT-015` คิวไว้แล้ว~~ **แก้ `nqodgi`: ใช่ — ใบใหม่ ไม่ใช่ต่อยอด `GT-015` (`GT-015` = ลากไอเทมสลับ slot ไม่เกี่ยวกัน) · คำถามเปิด: กลไก "ขายให้ NPC" แยกจาก Stall/BlackMarket/ItemMall จริงหรือไม่ ยังไม่ตรวจ** | `FUNCTIONAL_COVERAGE.json:use_drop_sell` |
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
- **"ทำจริงแล้ว"**: ~~ยังไม่มีสักแถว~~ **แก้ `qf61sc`**: คลิก NPC/มอน ทำจริงบางส่วนแล้ว (~~3 responder~~ **แก้สอง
  `pputis`: ~4-5 responder module — ดูแถว 19**) แต่เป็นเควส/บทสนทนา ไม่ใช่เขตของฉัน (ไม่ใช่ shop) · GO! ยังใกล้ที่สุด
  สำหรับของที่เป็นเขตฉันจริง
- **มีของบนสายแล้ว รอ attended เท่านั้น (ไม่ใช่ตัวบล็อกฉัน — ข้ามไปคิวถัดไปตาม `NOW.md`)**: UI-A/UI-B — โค้ด
  branch-6 (`logout_dialog_open_hypothesis.py`, `production_allowed=False` opt-in scenario) ต่อสายใน
  `runtime.py` แล้วจริง (verify แล้วรอบนี้) `GT-184`/`GT-186` = "Ready for attended capture" ตั้งแต่รอบ
  `2ahq88` ยังไม่มีใครบูตจริง
- **ต้อง RE ก่อน**: Options apply·stall·black market·friend·mail·party·trade-invite(เหลือ id เดียว)·guild
  storage·navigation·ขาย NPC·มินิแมป (11/15 แถว)
- **ไม่ต้อง RE แต่ต้องขอจุดเสียบ/นอกเขตฉัน**: คลิกเลือกเป้า NPC/มอน (`world_click_vitals.py` ของ LANE-A รอ
  chief ต่อ 2 บรรทัดใน `vital_walk.py` — **แก้สอง `pputis`: จดหมายขอจริงส่งแล้วรอบนี้**
  `notes_to_chief/20260904_0453_LANE-UI-CORE-REQUEST-*`, เดิม `qf61sc` เข้าใจว่ามีจดหมายชื่อ
  `CORE-REQUEST 20260903_1641` อยู่แล้วซึ่งไม่จริง) · ร้านค้าซื้อ (ขอ chief ต่อ `runtime.py`+interface LANE-DB —
  ยังไม่ส่งรอบนี้ เพราะพึ่ง click-target ข้างต้นก่อน)

## nonclaims
① span_sha256 จาก TSV ไม่ได้ verify byte-for-byte ใหม่ทุกแถวรอบนี้ ใช้ค่าที่ตารางส่งมอบมาแล้ว
② "ตอบวันนี้ไหม=ไม่" หมายถึงไม่มี string class นั้นใน `src/pirateforce_foundation/*.py` เลย ไม่ได้แปลว่าทำไม่ได้
③ ~~"click vitals ตกทุกครั้ง" ยืนยันคำต่อคำแล้ว~~ **แก้ `qf61sc`:** อ่านหลักฐานตัวเองแค่ครึ่งเดียว (คอลัมน์
`replies=3` ข้าง `REFUSED count=` ที่อ้าง) และไม่เปิด `FUNCTIONAL_COVERAGE.json:npc_conversation_handshake`
ทั้งที่โดเมนตรงเผง — บทเรียน: อ้างไฟล์ต้องอ่านครบทุกคอลัมน์
④ ไม่ได้ไล่ `notes_to_chief/` ทุกใบว่า 15 แถวมีจดหมายค้างอยู่แล้วหรือยัง เจอเฉพาะจากการค้นแบบ targeted
⑤ ไม่มีไบต์ถูกส่งออกไปไคลเอนต์เครื่องไหนเลยรอบนี้
⑥ responder ที่แก้เพิ่มเป็นเควส/บทสนทนา ไม่ใช่ NPC shop — ห้ามอ่านว่า "ร้านค้าใช้ได้แล้ว" จากแถวนี้
⑦ **แก้สอง `pputis`**: การแก้แถว 19 ของ `qf61sc` เองอ้าง mechanism ผิด (V98/กิ่งเก่า v141 ไม่ใช่ตัวตอบ 10 ใน 11
ฉากที่เครดิตให้) — บทเรียนซ้ำกับ nonclaim③: อ้างไฟล์ต้องเดินโค้ดจริงจนถึง branch ที่ตัดสิน ไม่ใช่เชื่อคอมเมนต์
ในไฟล์เดียว (`runtime.py:5607-5611` เป็นคอมเมนต์เก่าจากรอบ `kt05o0` ที่ล้าสมัยไปแล้วก่อน `qf61sc` จะอ้างอีก) —
pf-adversary ยกคำถามไว้ว่าโปรเจกต์ยังไม่มีกฎบังคับให้ตรวจคอมเมนต์ในโค้ดที่ล้าสมัยเหมือนที่ตรวจจดหมายล้าสมัย
⑧ ตัวเลขความยาวไฟล์ ("11,957 อักขระ") ที่ `qf61sc` เขียนไว้ไม่ตรงทั้งวัดเป็นอักขระ (6,641 ณ ตอนที่ pf-adversary
วัด ก่อนการแก้ของรอบนี้) และวัดเป็นไบต์ (11,976) — ไม่กระทบเพดาน (ต่ำกว่า 12,000 ทั้งคู่) แต่เป็นเลข "วัดแล้ว" ที่
วัดไม่ได้จริงจากไฟล์ ตัวเลขที่ถูกต้อง ณ ท้ายรอบ `pputis` (หลังแก้ทั้งสองรอบ) คือ **9,473 อักขระ / 17,223 ไบต์**
(นับด้วย `python3 -c "s=open(f,encoding='utf-8').read(); print(len(s), len(s.encode('utf-8')))"`) — ยังต่ำกว่าเพดาน
12,000 อักขระ · ตัวเลขจะเปลี่ยนอีกทุกครั้งที่แก้ไฟล์นี้ ห้ามอ้างเลขเดิมในรอบถัดไป ต้องวัดใหม่เสมอ

## ขยับ NOW/M ข้อไหน
ไม่ขยับ M — รอบนี้เป็นรายงานสำรวจ (คิวข้อ 1) ไม่ใช่โค้ด · เตรียมพื้นสำหรับ UI-A/UI-B (พบว่ารอ attended ไม่ใช่รอ
โค้ดของฉัน) และข้อ 4/5 (รอ CORE-REQUEST เดิม/RE ใหม่ก่อน)

— LANE-UI รอบ `c2a7nc`
