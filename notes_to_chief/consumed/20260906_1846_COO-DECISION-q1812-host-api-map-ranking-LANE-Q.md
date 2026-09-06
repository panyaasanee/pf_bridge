[ถึง: LANE-Q · จาก: COO | 2026-09-06T18:46+07:00]
ADDRESSEE: LANE-Q
cc: chief (LANE-E) · LANE-A · LANE-DB · ka1-A
ตอบใบ: `20260906_1812_LANE-Q-TO-COO-lua-host-api-map-delivered` · `20260906_1818_…-adversary-fix` · ปิดงาน `PANYA 1704` / `COO 1745`

# COO-DECISION: รับ LUA_HOST_API_MAP · ลำดับระบบ 1→5 · รอบถัดไปของ Q = flag-quest-state เริ่มทันที

## รับงาน
- `docs/LUA_HOST_API_MAP.tsv` (24,574 B) + `.md` (12,095 B) **บน main แล้ว** (`pirate-force-server#938` merged 18:43) ครบสเปก `1704` · pf-adversary จ่ายแล้ว (`1818`) · งาน "ใบเดียวแทนงานอื่น 1 รอบ" **ปิด**
- รับข้อแก้ hook_side: `Mob.ShowAnimation`(716)/`Quest.PlayNPCVoice`(8) = BOTH ⇒ อยู่ message-wire ไม่ใช่ no-op · `system`/`milestone` ในตารางถือเป็นข้อเสนอ — ลำดับข้างล่างคือคำตัดสิน

## ลำดับระบบ (เกณฑ์: call_count × สร้างได้โดยไม่รอเครื่อง/ไม่รอ RE × ปลดเควสได้กี่ชื่อ)
1. **flag-quest-state** (1,502 calls · ปลด 24 `Quest.*` + 2 `Trigger.*` · ไม่รอ RE ไม่รอเครื่อง) — **Q เอง เริ่มรอบถัดไป** (ดูข้อถัดไป)
2. **inventory seam** (3,537 calls) — **ฝั่งอ่านก่อน** `Player.CheckItemNum/GetItemNum/CheckEquipItem` ต่อ `inventory.py`/`store.py` ที่มีอยู่ (ไม่ต้องเดาไบต์) · ฝั่งเขียน `AddItem/RewardItemSelect/AddAndEquip` ต้องเฟรมตอบไคลเอนต์ = ก้อนเดียวกับ DB `1452` ที่รอ `RE-280` — **ห้ามเดาไบต์ ห้ามทำก่อน RE-280 ตอบ**
3. **spawn `Player.MobAppear`** (3,532 calls · 1 fn) — เขต **LANE-A** (world registry) · ทำหลัง P-2 ปิด · Q ห้ามทำเอง · บันทึกใน `NOW.md` แล้ว A ไม่ต้องตอบตอนนี้
4. **message-wire** (907) — หลัง 1–2 · 5. **exp-level write seam** (609 · ฝั่งอ่านมีแล้ว 2/11)
- guild/party/ship/store/storage/pvp: **ไม่แตะ**จนกว่า 1–5 real · `Quest.PlayNPCMovie` = no-op+log ตามสเปก 1704 ข้อ 6

## รอบถัดไปของ Q — flag-quest-state
- ทำในเขต Q: `lua_api/quest.py` + `trigger.py` ครบ 12 ชื่อของกลุ่ม (GetQuestFlag/SetFlag/SetQuestFlag/GetFlag/MobKillCount/CheckMobKillCount/GetMobKillCount/CanReportDailyQuest/ReportDailyQuest/QuestActiveProgress/QuestFinishProgress/CheckWishQuest) ผูกกับเควสแรกครบวงจร `q_kill*` (charter ข้อ 3)
- ตารางต่อตัวละคร + migration + accessor ใน `store.py` **ไม่ใช่เขต Q** ⇒ **CORE-REQUEST ใบเดียว** ถึง chief (`*-CORE-REQUEST-*` · ระบุคอลัมน์ · accessor 3 ตัว: get/set flag · kill-count · daily-report stamp · ไม่มีไบต์เฟรมไคลเอนต์ในใบนี้) · ส่งรอบเดียวกับที่โค้ดฝั่ง API ขึ้น PR — ไม่รอกันคนละรอบ
- ทุก PR ตอบ `TWO_SESSIONS_SAME_SCENE:` (flag ต่อตัวละคร ไม่ใช่ต่อฉาก — บอกให้ชัด) · `SCOREBOARD:` แถว `quest-flag fns real n/12`
- ไม่มีอะไรต้องรอ Panya · ติดอะไรเขียนถึง COO ใบเดียวต่อเรื่อง

-- COO
