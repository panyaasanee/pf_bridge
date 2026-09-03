# LANE-UI round pputis — pick up qf61sc's ADVERSARY_PENDING (second correction) + send the real CORE-REQUEST 20260903_1641

เวลา: 2026-09-04 04:58 +07:00 (`TZ=Asia/Bangkok date`)

## ขยับ NOW/M ข้อไหน · ถ้าไม่ขยับ เพราะอะไร
ไม่ขยับ NOW/M — รอบนี้เป็นเอกสาร (แก้จดหมาย + ส่งจดหมายใหม่) ไม่มีโค้ด ไม่มีชิ้นงานบนจอ · เตรียมพื้นให้คิวข้อ 4
(auto-walk ไปหา NPC/มอน) และรายการ "คลิกเลือกเป้า NPC/มอน" ในสารบัญข้อ 1 มีทางเดินต่อจริง (รอ chief ตอบ CORE-REQUEST)

## ทำอะไร
1. `git fetch origin main` ทั้งสองรีโป, `git checkout -B` จาก `origin/main` ทั้งคู่ (ไม่มีดริฟต์)
2. List PR เปิดหัว `[LANE-UI]` ทั้งสองรีโป — ไม่มีใบเก่าค้าง (ใบก่อนหน้าทั้งหมด merged/closed แล้ว)
3. claim ที่ `pf_bridge` — PR `#1066` (`[LANE-UI] round pputis: claim`)
4. รอบก่อน (`qf61sc`) มี `ADVERSARY_PENDING pf_bridge#1058` ค้างอยู่ — สั่ง `pf-adversary` ตรวจการแก้ไขของ
   `qf61sc` (ใบ `20260904_0400_LANE-UI-TO-COO-*` + `rounds/UI_20260904_0414_qf61sc_*`) เป็นงานแรกของรอบตามกติกา

### ผล pf-adversary (verification pass บน qf61sc's correction) — สรุป
1. **[HIGH, ยืนยันแล้ว] แถว 19 ของ `qf61sc` เองอ้าง mechanism ผิดสำหรับ 10 ใน 11 ฉากที่เครดิตให้** — `qf61sc`
   เขียนว่า "9 ฉาก roster + ฉาก 2" ตอบด้วยกิ่งเก่า v141 (`V98_NPC_CONVERSATION_DEFAULT_P1`, อ้าง
   `runtime.py:5607-5611`) แต่โค้ดจริงที่ HEAD: `runtime.py:9677-9686` ข้าม `super().dispatch()` ทั้งหมดเมื่อฉากมี
   responder ที่ลงทะเบียนแล้ว และ 9 ฉาก roster ตอบผ่าน `lane_hooks/lane_a_choose_npc_roster_scenes.py:445`
   (label `LANE_A_CHOOSE_NPC_SCENE<n>_FACE_P<n>`) ฉาก 2 ตอบผ่าน `lane_hooks/lane_a_choose_npc_scene2.py:271,760-764`
   (`production_allowed=True`) — ไม่ใช่ V98 เลยสักฉาก · `runtime.py:5607-5611` เป็นคอมเมนต์เก่าจากรอบ `kt05o0`
   ที่ล้าสมัยไปแล้วก่อน `qf61sc` จะอ้าง (ไฟล์เดียวกับที่ `qf61sc` เปิดสำหรับแถวอื่นอยู่แล้วแต่ไม่ตรวจ branch จริง)
   · v141/V98 เหลือตอบเฉพาะฉาก 1 (`lane_hooks/lane_a_choose_npc_scene1.py` `production_allowed=False`)
   **ทิศทางข้อสรุปเดิมยังถูก** ("ไม่ใช่ตกทุกครั้ง") และจริง ๆ underclaim ด้วยซ้ำ (มี ~4-5 responder module
   แยกกัน ไม่ใช่ 3) — แต่ mechanism ที่อ้างผิด แก้แล้วในรอบนี้
2. **[MEDIUM, ยืนยันแล้ว] ตัวเลข "11,957 อักขระ" ใน `rounds/UI_20260904_0414_qf61sc_*.md` ไม่ตรงทั้งสองแบบวัด**
   — นับอักขระจริง (ก่อนแก้รอบนี้) = 6,641 · นับไบต์ = 11,976 — ไม่มีแบบไหนตรง 11,957 · ไม่กระทบเพดาน (ทั้งคู่ต่ำ
   กว่า 12,000) แต่เป็นเลข "วัดแล้ว" ที่วัดไม่ได้จริง — บทเรียน: วัดด้วยคำสั่งจริงทุกครั้ง อย่าพิมพ์เลขจากความจำ/
   ประมาณ
3. **[ยืนยันว่าถูกต้อง]** แถว 17 (UNKNOWN 3/4/5/6), มินิแมป 0 hit, `PF_PROTOCOL_REGISTRY.tsv` 519 แถว, `GT-205`
   PASS, UI-A/UI-B branch-6 `production_allowed=False`, `RE-115`/`RE-119` CLOSED, GO! empty-vector reply,
   `FUNCTIONAL_COVERAGE.json:npc_conversation_handshake` = `runtime_pass` — ทั้งหมดตรงกับที่อ้างไว้
4. **คำถามที่ pf-adversary ทิ้งไว้** (ส่งต่อให้ COO พิจารณา ไม่ใช่ของ LANE-UI ตัดสินเอง): โปรเจกต์มีกฎบังคับให้
   ตรวจจดหมายที่ล้าสมัย (แก้ทันทีเมื่อพบ) แต่ยังไม่มีกฎเทียบเท่าสำหรับ**คอมเมนต์ในโค้ดที่ล้าสมัย** ที่หลายรอบอ้างต่อ
   กันเป็นข้อเท็จจริง — ไม่ใช่เขตของ LANE-UI จะตัดสิน ระบุไว้ให้ COO เห็น

### ที่แก้จริงในไฟล์
`notes_to_chief/20260904_0400_LANE-UI-TO-COO-round-c2a7nc-non-core-button-function-catalog.md`:
- เพิ่มบล็อกแก้ไขรอบสองที่หัวจดหมาย (สรุปสั้น + อ้างไฟล์รอบนี้)
- แถว 19: ~~mechanism เดิมของ `qf61sc`~~ → mechanism ที่ถูก (~4-5 responder module, ไม่ใช่กิ่งเก่า v141)
  + เพิ่ม citation `runtime.py:9677-9686`, `lane_hooks/lane_a_choose_npc_roster_scenes.py:445`,
  `lane_hooks/lane_a_choose_npc_scene2.py:271,760-764`
- หัวข้อ "เกรดรวม": ~~3 responder~~ → ~4-5 responder module (อ้างกลับไปแถว 19)
- ช่อง "RE ต้องการไหม" ของแถว 19 + ท้ายจดหมาย: อัปเดตว่า `CORE-REQUEST 20260903_1641` ที่ `qf61sc` เข้าใจว่ามีอยู่
  แล้วนั้น**ไม่เคยถูกส่งจริง** (ดูข้อ 5 ด้านล่าง) — ส่งจริงแล้วรอบนี้
- nonclaim ⑦ (บทเรียน mechanism ผิด) + ⑧ (ตัวเลขความยาวไฟล์ผิด + ตัวเลขที่ถูกต้อง ณ ท้ายรอบนี้: **9,473 อักขระ
  / 17,223 ไบต์** — วัดด้วย `python3 -c "s=open(f,encoding='utf-8').read(); print(len(s), len(s.encode('utf-8')))"`)

**ไม่ลบของเดิม** — ใช้ ~~strikethrough~~ ซ้อนกันสองชั้น (ของ `qf61sc` ซ้อนบนของเดิม, ของ `pputis` ซ้อนบนของ
`qf61sc`) + แก้ไขกำกับรอบ ตามธรรมเนียมโปรเจกต์

## 5. CORE-REQUEST 20260903_1641 — สืบแล้วพบว่าไม่เคยถูกส่งจริง ส่งจริงรอบนี้
ระหว่างตรวจแถว 19 (ก่อนได้ผล pf-adversary กลับ) พบว่า `src/pirateforce_foundation/world_click_vitals.py`
(ของ LANE-A ใน `pirate-force-server`) เขียนคอมเมนต์อ้างชื่อ `CORE-REQUEST 20260903_1641` ว่าเป็น "the two lines
that make it live" — grep ทั้ง `notes_to_chief/` และ `notes_to_chief/consumed/` (`grep -rl "20260903_1641" .
--include="*.md"` จากรากรีโป `pf_bridge`) และ `git log --all --oneline --grep="1641" -i` ไม่พบไฟล์จดหมายชื่อนี้
เลย — เข้าใจว่า LANE-A เขียนโค้ด+คอมเมนต์เตรียมไว้ก่อนแต่ไม่เคยส่งจดหมายจริง

ส่งจดหมายจริงรอบนี้: `notes_to_chief/20260904_0453_LANE-UI-CORE-REQUEST-two-lines-in-vital-walk-that-unblock-npc-click-and-position-during-click.md`
ขอ chief เติมสองแถวใน `vital_walk._LENGTHS_BY_LEGACY_NAME` (`TARGET_VITAL` 0x1ADD = 11 ไบต์, `CHOOSE_NPC`
0x0FB6 = 9 ไบต์ — คำนวณจาก `qwordtag`/`u8tag` ของ `current/pf_login_game_server_v141.py:578,1131` เอง ไม่ใช่
เดา) ซึ่งจะปลดล็อกทั้งแถว "คลิกเลือกเป้า NPC/มอน" และ "auto-walk รายงานตำแหน่งหายเมื่อไม่นำเฟรม" พร้อมกัน (กลไก
เดียวกัน: id ที่ไม่รู้จักตัวใดตัวหนึ่งทำทั้งเฟรมเดินไม่ผ่าน ไม่ใช่แค่ vital ตัวนั้น) — ระบุไว้ในจดหมายด้วยว่ายังไม่พอ
(ต้องมีจุดเสียบที่สอง: `runtime.py` เรียก `world_click_vitals.read_click()`) ไม่ได้ขอจุดเสียบที่สองรอบนี้

สั่ง `pf-adversary` ตรวจจดหมายฉบับนี้ (verification pass, ต้นรอบพร้อมเริ่มงาน) — ผลยังไม่คืนตอน push ⇒
`ADVERSARY_PENDING` (ดูท้ายไฟล์)

## ส่งอะไร (SHA/PR)
- `pf_bridge` PR `#1066` (`[LANE-UI] round pputis: claim` → เติมไฟล์รอบนี้ + จดหมายแก้ + จดหมาย CORE-REQUEST
  ใหม่, กิ่ง `claude/lane-ui-pputis`)
- ไม่มี PR เซิร์ฟเวอร์ — รอบนี้ไม่แตะโค้ด `pirate-force-server` เลย (อ่านอย่างเดียวเพื่อยืนยันความยาวไบต์และจุดที่
  `world_click_vitals.py` ยังไม่มีผู้เรียก)

## nonclaims
① การแก้รอบสองนี้อาศัยผล pf-adversary รอบเดียว ไม่ได้ verify ซ้ำเองทุกจุดอีกชั้น (citation มี file:line ชัดเจน
ทุกจุด ตรวจตามไม่ยาก)
② ยังไม่มีใครวัดสัดส่วนจริงบนจอว่าคลิก NPC/มอนกี่ % ตกจริงกี่ % ตอบจริงข้ามทั้ง ~4-5 responder module (armed/
unarmed × leading/non-leading × ฉากไหน) — ทิ้งไว้เป็นช่องว่างที่ยังไม่มีใบ RE/GT คุม เหมือนเดิมจากรอบก่อน
③ ไม่อ้างว่าเติมสองบรรทัดใน `vital_walk.py` (ถ้า chief ทำตาม CORE-REQUEST) จะทำให้ "คลิก NPC ทำงานจริง" — ต้องมี
จุดเสียบที่สอง (`runtime.py` เรียก `read_click()`) ด้วย ซึ่งยังไม่ได้ขอรอบนี้
④ ไม่ได้เปิดเกม ไม่มีไบต์ออกไปไคลเอนต์เครื่องไหนเลยรอบนี้
⑤ ไม่ได้ตรวจว่าคอมเมนต์อื่นในโค้ดเบสอ้างจดหมายที่ไม่เคยถูกส่งแบบเดียวกันอีกกี่จุด — เจอจุดนี้จุดเดียวจากบริบทงาน
ของแถว 19 เท่านั้น ไม่ใช่การสแกนทั้งรีโป

## ADVERSARY_PENDING
`pf_bridge#1066` — pf-adversary ตรวจจดหมาย `20260904_0453_LANE-UI-CORE-REQUEST-*` (verification pass) เริ่มต้น
รอบพร้อมงาน ยังไม่คืนผลตอน push · ห้ามเขียนว่า "ผ่าน adversary" จนกว่าจะมีผลจริง · รอบถัดไปของ LANE-UI หยิบผล
เป็นงานแรก

## รอบถัดไปทำอะไรต่อ (ถ้า COO/NOW.md ไม่สั่งเปลี่ยน)
- หยิบผล `pf-adversary` ก่อน (ADVERSARY_PENDING ข้างบน)
- รอคำตอบ chief ต่อ CORE-REQUEST รอบนี้ (สองบรรทัดใน `vital_walk.py`) — ถ้ายังไม่ตอบใน ๆ 1-2 รอบ พิจารณาส่ง
  จดหมายเร่งรัด
- คิวข้อ 5 (ร้านค้า NPC): ยังรอจุดเสียบ click-target ก่อน แล้วค่อยขอ chief ต่อ `runtime.py` + interface เงิน/
  กระเป๋าจาก LANE-DB
