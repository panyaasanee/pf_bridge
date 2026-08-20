# FINDINGS R23 — ตำแหน่งที่ถูกเซฟ "เดินทางกลับออกไปหา client" จริง ข้ามการรีสตาร์ท

รอบที่ 23 · 2026-08-17 12:06–12:1x ICT · job `046_r23_startgame_readback.ps1`
เครื่องมือใหม่: `pf_bridge\replay\pf_startgame_pos_probe.py`
สถานะ repo: **ไม่แตะ `src/` แม้แต่บรรทัดเดียว** · git porcelain 6 บรรทัดเท่าเดิม ·
canonical sha `673F4BFB…9708` ตรง baseline ทั้งก่อนและหลัง

---

## 0. คำถามของรอบนี้ (หนึ่ง milestone หนึ่ง claim)

รอบ 22 ปิดครึ่ง **ขาเข้า** ของ GT-005 ไปแล้ว: ส่งไบต์ `TargetPosVital` ลงสายจริง แล้ว
`character_positions` ขยับตามเป๊ะทุกหลัก และค่ายังอยู่หลัง server ดับ → **server เขียนเป็น**

แต่ครึ่งที่ผู้เล่นเห็นจริงยังไม่มีใครวัด:

> **ตอน login ครั้งถัดไป server อ่านแถวนั้นกลับออกมาใส่เฟรมที่เริ่มเกมไหม?**

ถ้าไม่ — ผู้เล่นเดิน แถวขยับ แต่พอเข้าเกมใหม่ก็ยังโผล่ที่เดิม แปลว่าคำว่า "persistence"
เป็นจริงกับ **ฐานข้อมูล** แต่เป็นเท็จกับ **ตัวเกม** ซึ่งเป็นคนละเรื่องกันคนละครึ่ง

---

## 1. สิ่งที่ซอร์สทำนายไว้ (อ่านอย่างเดียว ไม่แก้)

```
session.py:45        select_and_start() -> projector.start_game(selected, ...)   position=None
legacy_bridge.py:52  p = position or character.position
legacy_bridge.py:65  movement = self.movement_attr(character, p)
legacy_bridge.py:40  ... f32tag(p.x) f32tag(p.y) f32tag(p.z) f32tag(p.heading)
```

และ `character` มาจาก `store.select_character()` (`store.py:204`) ซึ่ง SELECT
`p.x, p.y, p.z, p.heading` ออกจาก `character_positions` ตรง ๆ
→ **ทำนาย:** `START_GAME_RES` ต้องพก quadruple ที่เซฟไว้ออกไปแบบ verbatim

รอบนี้มีไว้เพื่อ **พยายามหักล้างคำทำนายนี้บนสายจริง** ไม่ใช่เพื่อเชื่อ call graph

---

## 2. วิธีตัดสิน — ไม่เชื่อ parser ตัวไหนเลย

`f32tag` คือ `0x2A` + little-endian float ตรง ๆ (`v141.py:1135`)
ดังนั้น quadruple ที่คาดหวัง = **20 ไบต์** ที่คำนวณจากค่าใน DB แล้ว **ค้นหาเป็น substring ดิบ**
ในทุก container ที่ snappy-decompress ออกมา — เจอคือเจอ ไม่ต้องตีความ

แยกอีกชั้น: สแกนทุก run ของ f32 tag ที่ติดกัน ≥4 ตัวแล้ว decode รายงานไว้ด้วย
→ ถ้า **MISS** ก็ยังเห็นว่า server ส่งอะไรไปแทน และ `0x2A` ที่บังเอิญอยู่ใน payload
ของ float ก็ไม่มีทางถูกนับเป็นคำตัดสิน

---

## 3. การทดลอง — 2 boot บนไฟล์ DB **ใบเดียวกัน**

| | ทำอะไร | คาดหวัง |
|---|---|---|
| **BOOT 1** | probe A: เข้าเกม อ่านว่า `START_GAME_RES` พก **baseline** ไหม | HIT |
| | แล้วเดิน: splice `TargetPosVital` 9 เฟรม (เส้นทางเดียวกับรอบ 22) | แถวขยับ |
| | ปิด server | |
| **BOOT 2** | โปรเซสใหม่ ไฟล์ DB ใบเดิม | |
| | probe B: `START_GAME_RES` พก **ค่าที่ขยับแล้ว** ไหม | HIT ← **นี่คือ claim** |
| | probe C: **ค่าเก่า** ยังอยู่บนสายไหม | MISS ← **negative control** |

probe C คือหัวใจ: HIT ของ probe B จะมีความหมายก็ต่อเมื่อ **ค่าเก่าหายไปจริง ๆ**

---

## 4. ผล — A1 ผ่านครบ วัดสด ไม่ใช่ inference

```
SUMMARY  probeA(baseline_before)=0   send=0
         probeB(moved_after_restart)=0   probeC(old_gone_control)=3
         boot1_alive=True  boot2_alive=True

baseline = -9098.55078125,  -2866.86181640625, 186.0, 2.9943714141845703
moved    = -4529.2060546875,-3245.649169921875, 194.0, 0.09851964563131332
```

**ทั้งสาม probe ตกที่เฟรมเดียวกัน ออฟเซ็ตเดียวกัน มี f32 run เดียวในทั้งเฟรม:**

```
probe A   frame #2  wire=418B container=405B  needle=HIT@234
          run@234: [-9098.5508, -2866.8618, 186.0, 2.9944]     <- baseline
probe B   frame #2  wire=418B container=405B  needle=HIT@234
          run@234: [-4529.2061, -3245.6492, 194.0, 0.0985]     <- ขยับแล้ว
probe C   frame #2  wire=418B container=405B  needle=-1  (MISS)
          run@234: [-4529.2061, -3245.6492, 194.0, 0.0985]     <- ค่าเก่าไม่อยู่แล้ว
```

frame #2 คือคำตอบของ `StartGameReq` (32B เข้า → 418B ออก)
ขนาดเฟรมและออฟเซ็ตไม่ขยับเลยทั้งสามครั้ง — **เปลี่ยนแค่ 16 ไบต์ของค่าพิกัด**

### A1 (fact, วัดสด)
ตำแหน่งที่ถูกเขียนลง `character_positions` เดินทาง **กลับออกไปหา client**
ใน `START_GAME_RES` ครบทั้ง 4 ค่า (x, y, z, heading) **ข้ามการรีสตาร์ทของโปรเซส**
byte-exact — ไม่ใช่ปัดเศษ ไม่ใช่ใกล้เคียง

### A2 (fact, negative control)
ค่าเดิมหายจากสายจริง (probe C = MISS) → A1 ไม่ใช่ผลข้างเคียงของการที่ค่าบังเอิญอยู่ที่ไหนสักที่

### A3 (fact)
`boot1_alive=True` `boot2_alive=True` · stderr ทั้งสอง boot = 0B ·
`open sessions = 0` ตอนจบ (5 sessions ทั้งหมดถูกปิดครบ ไม่มี session รั่ว) ·
`integrity_check = ok` · จำนวนแถว accounts/characters/character_positions = 1 เท่าเดิม

### A4 (fact, กติกาความสะอาด)
canonical sha ตรง baseline ก่อนและหลัง · ไม่มี `-wal`/`-shm` ตกค้าง ·
`stray r23 db files in state\ = 0` · git porcelain 6 บรรทัดเท่าเดิม ·
สำเนา DB ถูก park ไว้ที่ `backup\pirateforce_r23_readback_20260817_121224.sqlite3`

---

## 5. 🔴 N1 — ของแถมที่สำคัญกว่าที่คิด: มีเฟรม "เตะกลับไปที่ศูนย์" ตามหลังมาทันที

**ระดับ: inference จากซอร์ส ยังไม่ได้วัดค่าไบต์ — อย่าจดเป็น fact**

`runtime.py:466` ในเส้นทางปกติ (ไม่ใช่ scene_load scenario) ส่งเฟรมที่สองตามหลัง
`START_GAME_RES` ทันที:

```python
tp_pc, tp_frame = legacy.make_login_teleport(1, 0)      # runtime.py:466
```

`make_login_teleport` (`v141.py:2431`) มีค่า default `x=0.0, y=0.0, z=0.0`
→ เฟรมนี้ **ไม่สนใจ `p` เลย** และบอก client ว่า scene 1, seq 0, พิกัด (0,0,0)
(สาขาที่ใช้ตำแหน่งจริงคือ `runtime.py:461` ซึ่งวิ่งเฉพาะตอนมี scene_load scenario)

แปลว่า **client ได้รับเฟรมที่พูดถึงตำแหน่งสองเฟรมติดกัน และสองเฟรมนั้นไม่ตรงกัน**

- เฟรมที่ 1 (`START_GAME_RES`) = ตำแหน่งที่เซฟไว้จริง ← รอบนี้พิสูจน์แล้ว
- เฟรมที่ 2 (teleport marker) = (0,0,0) ตายตัว ← อ่านจากซอร์ส ยังไม่ได้วัด

client จะเชื่อเฟรมไหนเป็นคำถามฝั่ง client ที่ probe นี้ตอบไม่ได้
**แต่นี่คือคำอธิบายอันดับหนึ่งที่ต้องสงสัยไว้ก่อน** ถ้า attended GT-005 แล้วเห็นตัวละคร
โผล่ผิดที่ทั้ง ๆ ที่ฐานข้อมูลถูกต้อง — จะได้ไม่ไปไล่หาบั๊ก persistence ที่ไม่มีอยู่จริง

**ทำไมรอบนี้ยังวัดไม่ได้:** เฟรมที่ตามมา (#3, 73B/container 62B) มี f32 run < 4
(`make_teleport_target` พก 3 float ไม่ใช่ 4) ตัวสแกนตั้ง `min_len=4` ไว้จึงไม่รายงาน
→ probe รอบหน้าปรับเป็น `min_len=3` แล้ววัดค่าจริง ใช้เวลา ~8 นาที **หนึ่ง boot พอ**

---

## 6. N2 — ข้อจำกัดของ probe นี้ (เขียนไว้กันตีความเกิน)

- probe นี้เข้าเกมด้วย **capture frames** ไม่ใช่ GameClient จริง → พิสูจน์ได้แค่ว่า
  **server ส่งอะไรออกไป** ไม่ได้พิสูจน์ว่า **client วาดตรงไหน**
- ตัวละครมีตัวเดียวในฐานข้อมูล canonical → ยังไม่ได้ทดสอบว่าเลือกตัวละครผิดตัวได้ไหม
- ไม่ได้ทดสอบว่าถ้าแถวใน `character_positions` หายไปเลยจะเกิดอะไร
  (`select_character` ใช้ INNER JOIN — เดาว่าจะ KeyError แต่ **ยังไม่ได้วัด**)
- ยืนยันเฉพาะตาราง `character_positions` เท่านั้น ตามกติกา "persistence ต้องระบุตาราง"

---

## 7. สิ่งที่ตั้งใจไม่ทำ

ไม่แก้ `src/` · ไม่เปิด hypothesis ใหม่ · ไม่แตะ ledger · ไม่เพิ่ม Domain 8 ·
ไม่เปิด GameClient · ไม่เปลี่ยนสถานะรายการใดในคิว · ไม่แก้ cron ตัวเอง ·
ไม่ commit (pf_bridge ไม่ได้อยู่ใน repo และ repo ไม่ถูกแตะเลย)

---

## 8. สรุปสำหรับ Panya หนึ่งบรรทัด

> **ชั้น wire/DB ของ GT-005 ปิดครบวงจรแล้ว** — เดินแล้วเซฟ (รอบ 22) และเข้าเกมใหม่แล้วได้ค่าที่เซฟคืน (รอบ 23)
> เหลือชั้นเดียวคือ GameClient ตัวจริง · และมีผู้ต้องสงสัยรออยู่แล้วหนึ่งราย: เฟรม teleport (0,0,0) ที่ตามหลังมา
