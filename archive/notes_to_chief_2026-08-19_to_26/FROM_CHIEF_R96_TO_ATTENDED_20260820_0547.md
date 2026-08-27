# จาก chief รอบ 96 → เซสชันหลัก ATTENDED (2026-08-20 05:4x)

**HEAD ตอนนี้ = `8dfd303`** (commit เดียวคืนนี้: REMOTE-PLAYER-ENCODER-001 + REMOTE-PLAYER-DISPATCH-001 · HYP-PF-025 · multiplayer ก้อน 2)
canonical DB ไม่ถูกแตะ (sha `6BFCEDD5..8FC7`) · ธงทั้งสองใบ RELEASED · inbox ว่าง · เลขจ็อบผู้เทส = **933** ต่อไป · chief ถัดไป = **158**... จริง ๆ คือ 159 (ผมใช้ 156/157/158 ไปแล้วรอบนี้)

## ⭐ ของใหม่คืนนี้: actor_type 2 (CNetActor) — "มีคนอื่นอยู่ในโลก" 5 เฟรมแรกในประวัติโปรเจกต์

**คิวรอบใหญ่ #9 มี GT-030 เพิ่มเข้ามา — พร้อมรันทันที**

**GT-030 REMOTE-PLAYER-VIS-001** — boot ท่า GT-024/027 เดิมเป๊ะ เปลี่ยนแค่ไฟล์:
`--remote-player-hypothesis-scenario scenarios\remote_player_hypothesis_visibility_probe.json` (+ `--db` สำเนา)
- ทริกเกอร์แชต **ascii 12 ตัวเดิม** → 5 เฟรม **ห่างกัน 15 วิ** (75 วิทั้งชุด ถ่ายทันทุกเฟรม)
- console ต้องเห็น label `HYP_PF_025_REMOTE_PLAYER_*` + event `remote_player_hypothesis_visibility_probe_sent` — เห็นชื่ออื่น = บูตผิดไฟล์
- **one-shot** · ยิงซ้ำ = `..._already_sent_no_reply` · ถ้า compose ถูกปฏิเสธ = `..._compose_refused_no_reply_<เหตุผล>` ใน log
- ⭐ **ก่อนยิง: หันกล้องทิศ +X จากจุดเกิด** (probe ทั้งสามอยู่แนวนั้น ห่าง ~112–412 หน่วย) ถ่าย baseline ก่อน 1 ใบ

**คำทำนายทีละเฟรม (ไม่ใช่ข้อเท็จจริง — นี่คือสิ่งที่ GT-030 วัด):**
- **t+0 SPAWN_BARE** (A `0x00A00001` ชื่อ `ProbePlayer01`): มีอะไรโผล่ไหม? รูปร่างอะไร? ป้ายชื่อขึ้นว่าอะไร ช่องไหน?
- **t+15 SPAWN_AVATAR** (B `0x00A00002` X+150, พก avatar ของตัวละครที่เลือก): **B ต่างจาก A ตรงไหน — นี่คือคำตอบว่า AvatarAttr จำเป็นไหม** ถ่ายให้เห็นทั้งคู่เฟรมเดียว
- **t+30 MOVE_A_1** (A, MovementAttr เดี่ยว mask 0x01): A ขยับไป X+300 ไหม? เดินหรือวาร์ป? (คำทำนายจาก CHUNK2-Q2: heading/mode/flags โดนรีเซ็ต 0)
- **t+45 MOVE_A_2** (A, mask 0x03 heading π/2): A หันหน้าไหม?
- **t+60 NEGATIVE_CONTROL** (C `0x00A00003` X−150, NPCAttr ผิดคลาสตั้งใจ ชื่อ `ProbeControl03`): มีตัวโผล่ไหม และ **ป้ายชื่อต้องว่าง**

**⛔ เกณฑ์หยุดทั้งเลนทันที:** เฟรม 5 **ขึ้นชื่อ** `ProbeControl03` (= ข้ออ้าง bind-gate ก้อน 1 ผิด รื้อทั้งหมด) หรือ server log มี `ErrorData=28317`
**pass ขั้นต่ำ:** ตอบได้ว่า (①) เฟรม 1 มีอะไรโผล่หรือไม่ (②) เฟรม 5 ป้ายชื่อว่างหรือไม่ — **ผลลบมีค่า** (ไม่โผล่เลย = spawn ด้วย ActorAttr mask 0 ไม่เรนเดอร์ ก็เป็นคำตอบ ไม่ใช่ fail)
🔴 **ไม่มีทาง despawn probe** — สามตัวค้างจนตัด connection · จบเทสปิด client แล้ว teardown ปกติ · run copy ทิ้งได้
🔴 HP probe = 100 ทุกตัว — ถ้าเห็นตัวไหน "ตาย" เอง = ผิดคาด จดละเอียด

⭐⭐ **nonclaim บังคับติดทุกผล: นี่คือดีไซน์ของเรา ไม่ใช่ของเซิร์ฟเวอร์ต้นฉบับ ซึ่งกู้ไม่ได้ตลอดกาล** (ไม่มี capture remote human player ในคลังเลย)

## ของที่ควรรู้

- รายละเอียดเต็มทีละคลิกอยู่ใน `GAME_TEST_QUEUE.md` (GT-030) · report ปิดงาน = `reports/PF_REMOTE_PLAYER_ENCODER001_ACTOR_TYPE_2_VISIBILITY_20260820.md`
- **GT-027/028/029** (damage NPC · slow sweep · dying countdown) ยัง PENDING เหมือนเดิม — รันได้ในรอบใหญ่เดียวกัน
- **GT-001 smoke ต้อง re-arm ที่ `8dfd303`** (commit แตะ src/ · แต่ทุกจุดหลังธง opt-in ที่ boot ปกติไม่ใช้ · full suite 1618 passed แล้ว)
- **HYP-PF-025 เหลือ 1 tracked version slot** — ถ้าอยากได้ variant (เปลี่ยนชื่อ probe · cadence probe · despawn) ต้องให้ chief เปิด/ขอ approval ก่อน
- **บทเรียนคืนนี้ (จดใส่ PLAYBOOK):** เพิ่มโมดูล src/ ที่ build actor entry ทำ census drift 3 จุด (runtimeres · stats · mpaudit closure) — จ็อบ 156/157 REFUSED to commit อย่างถูกต้อง (guard ทำงาน) · แก้ครบใน 158 · **เพิ่มโมดูลที่ census ใด ๆ นับ = ต้อง re-pin tool+report+test ในรอบเดียว**

## 🔴 คำถามค้างสำหรับ Panya (ก้อน 2 → ก้อน 3)

**ก้อน 2 ยัง "ไม่จบ" จนกว่า GT-030 รันและตัดสินว่าเห็นอะไร** — Panya สั่งไว้ว่า **จบก้อน 2 ต้องกลับมาเคาะก่อนเดินก้อน 3** · หลัง GT-030 มีผล จะมีคำถามให้ตัดสิน: probe เรนเดอร์เป็นคนไหม · avatar จำเป็นไหม · เดินหน้าก้อน 3 (transport เต็ม สองเซสชันจริง) หรือยัง
