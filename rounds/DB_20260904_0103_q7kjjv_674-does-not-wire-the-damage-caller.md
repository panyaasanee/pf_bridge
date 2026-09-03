# DB round (`q7kjjv`) — 2026-09-04T01:03+07:00 (TZ=Asia/Bangkok)

ต่อจาก `rounds/DB_20260903_2336_bv0t1z_r306_item4_design_not_bug.md` — รอบนั้นตอบคิวเก่า (R306 ข้อ 4)
ว่าเป็นดีไซน์ ไม่ใช่บั๊ก และรายงานว่าคิวถัดไปคือ `1101` (HP/เลเวลถาวร) ที่รอ M4 ปลดล็อกเต็มจาก LANE-B

**บรรทัดเดียวของรอบนี้: อ่าน `NOW.md` แล้วพบคำสั่งเดี่ยวจากใบ `COO-DECISION 20260903_2348` — วัดบน main
ว่า `#674` ให้ `apply_hp_damage` มีผู้เรียกจาก aggro tick จริงหรือยัง วัดแล้วพบว่า "ไม่ใช่" ด้วยเหตุผลที่
ถูกต้อง (hold ที่ COO อนุมัติเองรอบ `2050`) ⇒ `1101` ยังล็อกต่อ ไม่มีโค้ดให้แก้ในเขตเขียนของ DB รอบนี้**

## NOW.md — รอบนี้ขยับข้อไหน

อ่าน `NOW.md` เป็นไฟล์แรกก่อนแตะอะไร (ฉบับ "ตรวจล่าสุด 2026-09-04 00:47 +07:00 โดย COO")

- **ไม่ขยับบรรทัดใดของ `NOW.md`** — ไม่มีสิทธิ์แก้ไฟล์นั้นเอง คิว DB ในบรรทัด M4 (`rounds/DB_..._2205_...`
  §8 / `2348`) ยังคงเดิม: `1101` รอ M4 ปลดล็อกเต็ม ⇒ ยัง "ไม่ใช่" ตามที่วัดรอบนี้ ไม่มีอะไรถึงเกณฑ์ย้าย
  "รอ Panya ติ๊ก"
- **P-0 · P-1 · P-2 · P-3 · GM-A/B · UI-A · UI-B · `/speed` · M4 ตัวเนื้อ (Door B, aggro tick การเขียนจริง)**
  นอกเขตของสายนี้ ไม่แตะแม้ไฟล์เดียว — รอบนี้อ่านเพื่อวัดเท่านั้น
- 🔴 **รอบนี้ไม่แตะโค้ดเลยทั้งสองรีโป** — อ่าน `runtime.py`, `lane_hooks/lane_b_mob_ai_tick.py`,
  `mob_ai_player_damage.py` (ทั้งหมดนอกเขตเขียนของ LANE-DB อ่านได้ แก้ไม่ได้) และ `store.py` เฉพาะบรรทัด
  `apply_hp_damage` ของตัวเอง (อ่านอย่างเดียว ไม่แก้ — behavior เดิมถูกอยู่แล้ว ไม่ใช่ตัวต้องสงสัยรอบนี้)

## 1. ล็อกรอบ

- 01:03+07 (ก่อนอ่านกล่องจดหมายและก่อนแตะโค้ด) list PR สถานะ open ทั้งสองรีโปหัวข้อขึ้นต้น `[LANE-DB]`:
  ไม่มีใบไหนเปิดค้างในทั้งสองรีโป (`pirate-force-server` มีแค่ `#689 [LANE-E]` · `pf_bridge` ว่างเปล่า)
  ⇒ ไม่ต้องปลดล็อกใคร ไม่ใช่ takeover
- ตัดกิ่งจาก `origin/main` สดของ `pf_bridge` (`b4380693`) commit `rounds/DB_20260904_0103_q7kjjv_claim.md`
  (สามบรรทัด: `q7kjjv` · `2026-09-04T01:03+07:00` · `claim`) push แล้วเปิด `pf_bridge#1036
  [LANE-DB] round q7kjjv: claim` ไม่มี `PF-AUTOMERGE: v4` ใน body ตอนเปิด
- list ซ้ำทันทีหลังเปิด: `[LANE-DB]` open ใน `pf_bridge` มีใบเดียวคือ `#1036` ของผมเอง ⇒ ไม่แพ้ ทำงานต่อ
- รอบนี้ไม่มีโค้ด ⇒ ไม่มี PR ฝั่ง `pirate-force-server` ให้เปิด ข้ามขั้นตอน "ตรวจซ้ำก่อนเปิด PR เซิร์ฟเวอร์"

## 2. กล่องจดหมาย

`grep "ADDRESSEE: LANE-DB"` บน `origin/main` สด แล้วหักใบที่มี `.CONSUMED.txt` คู่ ⇒ ใบเดียวค้าง:
`20260903_2348_COO-DECISION-lane-db-r306-item-4-is-design-per-2130-line-cut-from-now-and-measure-whether-674-unblocks-1101.md`
ตอบแล้ว + สร้าง stub `.CONSUMED.txt` คู่ (ดู §3)

ส่งออกหนึ่งใบ:
`20260904_0103_LANE-DB-STATUS-674-wired-the-tick-not-the-damage-caller-1101-stays-locked.md`
(ADDRESSEE: COO, cc chief/LANE-B) — STATUS ไม่ใช่ ASK เพราะไม่มีอะไรเกินอำนาจหรือย้อนไม่ได้ที่ต้องให้
COO ตัดสินใหม่ (COO อนุมัติ hold นี้เองไปแล้วที่ `20260903_2050` ก่อนรอบนี้เริ่ม)

## 3. ทำอะไร

### 3.1 คำถามของใบ `2348`

`#674` (aggro tick เขียน HP แบบ floored read-back · merge `2026-09-03T18:49+07:00`) ทำให้
`apply_hp_damage` มีผู้เรียกจริงจาก tick แล้วหรือยัง — วัดสดบน `origin/main` ของ `pirate-force-server`
ที่ `cbcb8705` (fetch รอบนี้)

### 3.2 ไล่สายจากจุดเรียกใน `runtime.py` ลงไปถึง `store.apply_hp_damage`

1. `src/pirateforce_foundation/runtime.py:6443-6448` — จุดเรียก `lane_b_mob_ai_tick.maybe_tick()` จริง
   หนึ่งเดียว (ยืนยันด้วย `grep -n "maybe_tick" runtime.py`) เรียกทุกเฟรมที่ `parsed.nested_id ==
   legacy.TARGET_POS_VITAL` ผ่าน gate ที่ `:6376-6385` (scene folder ตรงกัน + `module_production_allowed`)
   — gate นี้เปิดจริงแล้วตาม `#668`/ticket 1648 (คอมเมนต์ในไฟล์ยืนยัน) — แต่ส่งอาร์กิวเมนต์แค่ 4 ตัวตำแหน่ง
   (`self.mob_ai_register, self.mob_combat_ledger, performer, (x, y, z)`) **ไม่มี `store=`/`character_id=`**
2. `src/pirateforce_foundation/lane_hooks/lane_b_mob_ai_tick.py:197-205` — ลายเซ็น `maybe_tick` มี
   `store: Any = None, character_id: Any = None` เป็นออปชันนอลสองตัวสุดท้าย ⇒ ค่าเริ่มต้นเป็น `None` จาก
   ข้อ 1
3. `lane_b_mob_ai_tick.py:249-266` — เมื่อ `store is None and character_id is not None` (ไม่ใช่เคสนี้)
   หรือ `store is not None and character_id is None` (ก็ไม่ใช่) ฟังก์ชันมีกิ่งจัดการทั้งคู่ แต่เคสจริงบน
   main คือ **ทั้งสองเป็น `None`** ⇒ ไม่เข้ากิ่งไหนเลย ตกไปที่บรรทัดถัดไป
4. `lane_b_mob_ai_tick.py:269-270` — `if store is not None: mob_ai_player_damage.apply_tick_damage(store,
   character_id, results)` — `store` เป็น `None` เสมอจากข้อ 1+2 ⇒ **เงื่อนไขนี้เป็นเท็จทุกครั้งในโปรดักชัน
   วันนี้** `apply_tick_damage` (ซึ่งเป็นตัวเดียวที่เรียก `store.apply_hp_damage` จริงตาม
   `mob_ai_player_damage.py:370`) ไม่เคยถูกเรียก

### 3.3 ทำไมยังไม่ต่อสาย — ไม่ใช่ของขาด เป็น hold ที่มีอยู่แล้ว

`lane_b_mob_ai_tick.py:164-193` (ค่าคงที่ `LANE_B_MOB_AI_TICK_WIRING`) — LANE-B เขียนบรรทัดที่ต่อสาย
`store=`/`character_id=` ไว้ตรงตัวอยู่แล้ว พร้อมป้าย `MOB_AI_PLAYER_DAMAGE_WIRING_ON_HOLD` ว่าตั้งใจไม่วาง
จนกว่า COO ตอบใบ `pf_bridge/notes_to_chief/20260903_1952_LANE-B-ASK-COO-damage-door-built-rate-is-one-hp-per-frame.md`
— วัดต่อ: **COO ตอบไปแล้วจริงที่ `20260903_2050_COO-DECISION-lane-b-hold-approved-...md`**: "อนุมัติการพัก"
เกตให้สดต้องรอ `RE-222`/Door B (เฟรม `UpdateAttrVital` ที่ผู้เล่นเห็นหมัดคู่กับ HP ขยับ) ยังไม่ flip — ตรงกับ
`NOW.md` บรรทัดคิว M4 ("Door B ... รอบ 01:31 ห้ามส่งจริง ค่าสดจากจุดอ่าน chief `0047` ข้อ 1")

### 3.4 สรุปคำตอบ

**ไม่ใช่** — `#674` ต่อสายให้กลไก tick (การอัปเดต `mob_ai_register`) ทำงานจริงทุกเฟรม แต่ไม่ได้ต่อสายไปถึง
`apply_hp_damage` เพราะเป็น hold ที่ COO อนุมัติเองด้วยเหตุผลที่ถูกต้อง (เขียน HP ย้อนไม่ได้ไปพื้น 1 HP โดย
ผู้เล่นไม่เห็นเฟรม = ไม่ใช่คอมแบตที่ทดสอบได้) ⇒ ตามใบ `2348`: `1101` (HP/เลเวลถาวร) **ยังล็อกต่อ**

## 4. ทำไมรันชุดเต็มศูนย์ครั้ง

**ไม่ได้แตะโค้ดของสายไหนเลยทั้งสองรีโปรอบนี้** — ไม่มี diff ให้ทดสอบ ไม่มี commit โค้ดให้รันชุดเต็ม รอบนี้
เป็นรอบวัด/อ่านล้วนตามคำสั่งของใบ `2348`

## 5. หลักฐาน — สองชั้นแยกกัน

### 5.1 client-observable

🔴 **ศูนย์** — รอบนี้ไม่ใช่งานสร้างของใหม่ เป็นการวัดคำถามที่ COO ตั้งไว้เท่านั้น ไม่มี byte ไหนเปลี่ยน
ไม่มีอะไรให้เข้าคิว GT

### 5.2 wire-DB

- `src/pirateforce_foundation/runtime.py:6443-6448` (`origin/main` `cbcb8705`) — จุดเรียก `maybe_tick`
  จริงหนึ่งเดียว ส่ง 4 อาร์กิวเมนต์ตำแหน่ง ไม่มี `store=`/`character_id=` (อ่านโค้ดตรง ไม่ใช่การรันเทส)
- `src/pirateforce_foundation/lane_hooks/lane_b_mob_ai_tick.py:197-205,249-270` — ลายเซ็นออปชันนอล +
  กิ่ง `if store is not None:` ที่เป็นเท็จเสมอจากค่าเริ่มต้น
- `src/pirateforce_foundation/lane_hooks/lane_b_mob_ai_tick.py:164-193` — ค่าคงที่ `LANE_B_MOB_AI_TICK_WIRING`
  ยืนยันว่า LANE-B ตั้งใจพักบรรทัดนี้ไว้ ไม่ใช่ลืม
- `pf_bridge/notes_to_chief/20260903_2050_COO-DECISION-lane-b-hold-approved-...md` — COO อนุมัติการพักไปแล้ว
  ก่อนรอบนี้เริ่ม (อ่านยืนยัน ไม่ได้ตัดสินเอง)
- `pf_bridge#1036` — claim PR ของรอบนี้ (จะเติม marker ท้ายรอบหลัง §7 เสร็จ)

## 6. nonclaims

1. **ไม่ได้ตัดสินว่า hold ควรปลดเมื่อไร** — เป็นของ COO/LANE-B (Door B, `RE-222`) ไม่ใช่ของ DB วัดได้แค่ว่า
   วันนี้ปลดหรือยัง = ยัง
2. **ไม่ได้อ่าน `mob_ai_player_damage.py` ทั้งไฟล์ละเอียด** — อ่านเฉพาะส่วนที่ยืนยันว่า `apply_tick_damage`
   เป็นตัวเรียก `store.apply_hp_damage` จริง (`:370`) ไม่ได้ตรวจ logic การคำนวณดาเมจข้างในลึกกว่านั้น
3. **ไม่ได้รันเทสของ LANE-B รอบนี้** — นอกเขตเขียน อ่านโค้ดอ้างอิงเท่านั้น ไม่ได้อ้างว่ารันแล้วผ่าน/ไม่ผ่าน
4. **ไม่ได้ตรวจว่ามีจุดเรียก `maybe_tick` อื่นนอกจาก `runtime.py:6443-6448`** — `grep -n "maybe_tick"` ทั้ง
   repo (นอก tests) เจอจุดเดียว เชื่อว่าครบ แต่ไม่ได้ตรวจแบบ static-call-graph tool
5. **ไม่มีจดหมายค้างส่ง COO นอกจากใบเดียวที่ส่งรอบนี้**

## 7. ชุดเทสของรอบ และสถานะ PR ณ ตอน push

- ระหว่างทำงาน: ไม่มีโค้ดให้รัน อ่านไฟล์ที่มีอยู่แล้วเพื่ออ้างอิงเท่านั้น (§3, §5.2)
- ชุดเต็ม: **ไม่รัน** — เหตุผลใน §4 (ไม่มี commit โค้ด)
- `pirate-force-server`: ไม่มี PR รอบนี้ (ไม่มีโค้ด)
- `pf_bridge#1036`: เติม `PF-AUTOMERGE: v4` ทันทีหลัง push ไฟล์รอบนี้ (ขั้นถัดไปของรอบ — ไม่มี PR ฝั่ง
  เซิร์ฟเวอร์ให้รอ)

## 8. รอบหน้าทำอะไร

1. **อ่าน `NOW.md` ล่าสุดใหม่ก่อนตัดสินใจ** เสมอ
2. ถ้า Door B / `RE-222` flip แล้วและ `store=`/`character_id=` ถูกต่อสายจริงใน `runtime.py` (นอกเขต DB
   สังเกตได้จาก `main`) ⇒ `1101` (HP/เลเวลถาวร) ปลดล็อก เริ่มคิวนั้นทันที (schema/typed columns สำหรับ HP
   ปัจจุบัน/max และ level ตามใบ `20260901_1101`/`1112` — ตรวจ `store.py` ว่ามีคอลัมน์อยู่แล้วหรือยังต้อง
   migration ใหม่)
3. ถ้ายัง — ตรวจกล่องจดหมายว่า COO/LANE-B มีอะไรใหม่ ถ้าไม่มีงานอื่นในเขตเขียนของ DB ที่ทำได้โดยไม่ต้องรอ
   ให้เขียนไฟล์รอบสั้น ๆ ว่าไม่มีอะไรทำ (อย่าหาเรื่องทำนอกเขต)
