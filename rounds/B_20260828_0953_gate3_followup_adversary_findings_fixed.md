# round `B_20260828_0953` (`3iq8jk` follow-up) - lane B - COMBAT -- pf-adversary
findings on the gate-3 widening fixed after PR #189/#292 already merged

**opened:** 2026-08-28 09:44 (+07:00) - **closed:** 2026-08-28 ~09:55 (+07:00)
**branches:** `claude/admiring-galileo-3iq8jk` (pirate-force-server, second commit +
merge-main) - `claude/friendly-ride-3iq8jk` (pf_bridge, this file)

**ผู้เล่นจะเห็นอะไรต่างจากเมื่อวาน:** ไม่มีอะไรต่างบนจอ -- นี่คือการแก้เอกสาร/เทสตามที่ `pf-adversary`
พบ ไม่ใช่ behavior ใหม่

## 0 สิ่งที่เกิดขึ้น: PR merge เร็วกว่า pf-adversary

รอบก่อน (`3iq8jk`, ปิด 09:42) เปิด `pf-adversary` เป็น background agent ก่อน push ตามกฎ แต่ automerge
workflow merge PR `pirate-force-server#189`/`pf_bridge#292` เสร็จก่อนที่ agent จะตอบกลับ (2 นาทีเศษ) --
ผลจาก `pf-adversary` มาถึงหลัง merge แล้ว บทเรียนสำหรับรอบถัดไป: ถ้าจะรอผลจริงๆ ต้องรอ**ก่อน** push ไม่ใช่
push แล้วรอไปพร้อมกัน (รอบนี้ทำสองอย่างพร้อมกันเพราะ stop-hook บังคับให้ commit ก่อน agent จะตอบ)

## 1 ผลจาก pf-adversary: ปลอดภัยจริง + พบ 2 จุดที่ควรแก้จริง

**ยืนยันความปลอดภัย:** เกต 3 ที่ขยายไปยัง unreachable ในโปรดักชันวันนี้จริง (พิสูจน์อีกทางจาก
`session.py`: `is_unmoved_baseline` ยังกันก่อนที่ `make_backpack_attr` จะได้รับกระเป๋าที่ไม่ใช่ golden) --
ไม่มี caller อื่นของ `make_backpack_attr` เสียหาย (grep แล้วมีแค่ `legacy_bridge.py` + 3 เทส) --
`require_known_backpack` ยัง raise จริงสำหรับ move/swap/merge ทั้งสามฟังก์ชัน (พิสูจน์ด้วยสคริปต์แยก)

**2 จุดที่แก้จริง:**
1. Docstring พูดเกินจริงว่า "golden ทั้งสองอันยัง byte-pin เหมือนเดิม" -- ที่จริง `make_backpack_attr`
   เช็คแบบ inline แค่ `INITIAL_BACKPACK` เท่านั้น ส่วน `MERGED_V111_BACKPACK` พิสูจน์แยกอีกชั้นใน
   `tests/test_item_lifecycle.py`'s golden-hash comparison -- **ความไม่สมมาตรนี้มีอยู่ก่อนรอบนี้แล้ว** ไม่ใช่
   ของใหม่ แต่ prose พูดเกินจริง แก้ให้ตรงในทั้ง `inventory.py`, `mob_pickup.py`, และ comment ในเทส
2. ไม่มีเทสไหนเรียก `make_backpack_attr` ตรงๆ (จุดที่แก้จริงรอบก่อน) ด้วยกระเป๋าที่โครงสร้างพัง เพื่อพิสูจน์
   ว่าด่าน 3 ยังปฏิเสธ malformed shape หลังขยายแล้ว -- เพิ่มเทสใหม่
   `test_make_backpack_attr_still_rejects_a_structurally_invalid_bag`

**ข้อสังเกตเพิ่มเติมที่ไม่ใช่บั๊ก:** `docs/FUNCTIONAL_COVERAGE.json`'s `monster_spawn_and_loot` capability
notes (ประวัติสะสมยาวตั้งแต่รอบ 100 กว่า) ยังเขียนว่าทั้งสามด่านไม่ขยับ -- ไม่ใช่ปัญหาที่รอบนี้สร้าง (ไฟล์นี้
ไม่ได้อัปเดตทุกรอบมานานแล้ว) แต่แก้ตามธรรมเนียมที่สาย B เคยต่อท้าย narrative นี้มาก่อน (round `vvkff9`,
`3dxv22`) -- ต่อท้ายย่อหน้าใหม่บันทึกสถานะด่านปัจจุบัน

## 2 PR merge ก่อนแล้ว -> เปิด PR ใหม่ตามกฎ

`pirate-force-server#189` (`5fa2fd3`) และ `pf_bridge#292` (`24bb457`) **merged=true** ทั้งคู่ก่อนรอบนี้
เริ่มแก้ -- คอมมิตแก้ที่สองของ `pirate-force-server` (`51d30d8`) จึงอยู่บน branch เดิมที่ merge ไปแล้ว ตาม
กฎ "PR ที่ merge แล้วไม่ใช่ PR เดิมอีกต่อไป" เปิด PR ใหม่: `pirate-force-server#192`
(`[LANE-B] round 3iq8jk follow-up: pf-adversary fixes for the gate-3 widening`) -- merge main
(`824e80b`, ไม่ชนกัน, ไฟล์คนละไฟล์) แล้ว push, เทสผ่านซ้ำ 108 passed

`pf_bridge` ฝั่งนี้: merge main (`48afae9`→`55983fc` ผ่าน fast-forward, ดึงมาจาก Lane A/GM/COO -- อ่านแล้ว
ไม่มีอะไรถึงสาย B โดยตรง) แล้วเขียนไฟล์นี้ + STATUS letter เป็นรอบใหม่ (ไม่มี PR pirate-force-server ฝั่งนี้
เพราะ pf_bridge ไม่มีโค้ดแก้ มีแค่เอกสารรอบ)

## 3 เทส (รันจริง)

`python3 -m unittest tests.test_mob_pickup tests.test_item_lifecycle tests.test_item_move_generalized
tests.test_item_move_hypothesis`: **108 passed** (เพิ่มจาก 107 ด้วยเทสใหม่)
สวีตเต็ม: `python3 -m unittest discover -s tests`: **3873 tests, 18 errors (เดิม, capstone/pefile)**
ไม่มี regression

## เกณฑ์สองชั้น

wire/DB: ไม่มีของใหม่รอบนี้ -- แก้เอกสาร/เทสเท่านั้น
client-observable: ไม่มีของใหม่รอบนี้

## nonclaim

รอบนี้ไม่รันเกมจริง ไม่แตะ `runtime.py`/`app.py`/`current/pf_login_game_server_v141.py`/
`scenarios/world_*.json` -- ไม่มีการเปลี่ยน behavior ใดๆ เพิ่มเติมจากรอบก่อน มีแค่ prose/เทสแก้ให้ตรงกับ
สิ่งที่โค้ดทำจริง

## write zone

`pirate-force-server`: `src/pirateforce_foundation/inventory.py` (docstring precision), `src/
pirateforce_foundation/mob_pickup.py` (docstring precision), `tests/test_mob_pickup.py` (1 comment แก้ +
1 เทสใหม่), `docs/FUNCTIONAL_COVERAGE.json` (ต่อท้าย 1 ย่อหน้า)
`pf_bridge`: `rounds/B_20260828_0953_...md` (ไฟล์นี้), `notes_to_chief/20260828_0953_LANE-B-STATUS-...md`
(ใหม่)

## CORE-REQUEST

none

## เปิดใบให้สาย C

none
