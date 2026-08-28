# R217 (`apk7ue`) — 2026-08-29 ~00:0x-00:4x (+07:00)

**หัวข้อรอบ:** ต่อสาย `CORE-REQUEST-GM-029` (ทางแชท `0xAC52` เปลี่ยนจาก observe-only เป็นเส้นทางที่ส่งไบต์ได้)
· ด่าน cp874 ก่อน push สำหรับทั้งทรี · `GT-132` ขึ้นหัวคิวตาม COO · เปิด `RE-135` · บริโภคจดหมาย 1 ใบ

## 0. การ์ดกันรอบซ้อน และชะตาของรอบก่อน
- PR เปิดค้างตอนเริ่มรอบ: `pf_bridge#333/#331/#329` (LANE-B/A/GM) · `pirate-force-server#213/#211` (LANE-B/GM)
  — **ไม่มีใบ `[LANE-E]`** ⇒ ล็อกว่าง · ยึดล็อกด้วย `pf_bridge#335` + `pirate-force-server#214` (draft ทั้งคู่)
- ชะตา PR ของรอบก่อน (หัวข้อ 2 ข้อ 7): `pf_bridge#328` และ `pirate-force-server#212`
  **API รายงาน `merged=false` ทั้งคู่ แต่ทั้งคู่เป็น ancestor ของ `main` จริง** (`git merge-base --is-ancestor` ผ่าน)
  ⇒ 🔴 **`merged` ของ GitHub API ใช้ตัดสินไม่ได้ในโปรเจกต์นี้** เพราะ `merge-claude-pr.yml` merge ด้วยการ push แล้วปิดใบ
  ใบไหน merge จริง **ต้องวัดด้วย `git merge-base --is-ancestor <head sha> origin/main`** — เขียนไว้ให้รอบหลังใช้แทน
- `VITAL_REGISTRY_FROM_CLIENT_BINARY_20260817.tsv` มีจริง (11,388 ไบต์)

## 1. `CORE-REQUEST-GM-029` (repo `pirate-force-server`)
ใบสั่ง: `20260828_1930_LANE-GM-CORE-REQUEST-GM-029-v2-replace-not-add.md` (R215 รับใบแต่ต่อไม่ได้เพราะโมดูลยังไม่ขึ้น main
· `#204` merge แล้ว ⇒ รอบนี้ต่อได้)

**หนึ่งคอมมิต สองการแก้:** ลบ `lane_hooks.fire(...)` ของ GM-028 ที่สาขา `0xAC52` + ใส่
`chat_command_action.make_gm_chat_command_action(session=self, payload=..., legacy=legacy)` แทน

🔴 **ใบสั่งชี้จุด append ผิด และถ้าทำตามใบตรง ๆ เซิร์ฟเวอร์พังทุกเฟรม:** `actions` ยังไม่ถูก bind ที่สาขานั้น
มันเกิดที่ `actions = super().dispatch(parsed)` ห่างลงไป ~820 บรรทัด และนั่นคือ binding เดียวที่เฟรมแชทไปถึง
(วัดด้วย `sys.settrace` บน harness ที่ commit แล้ว — เข้า 4646 ออก `return` เดียวปลายเมธอด)
⇒ ทำแบบ `gm_state_action`: `gm_action = None` ก่อนสาขา · `actions = actions + [gm_action]` หลัง `super().dispatch`

ไฟล์ที่แตะ 3 ใบ: `src/pirateforce_foundation/runtime.py` · `tests/test_gm_chat_command_dispatch_wiring.py`
· `docs/FUNCTIONAL_COVERAGE.json` (แถวแชท — ทางเดิมกลายเป็นคำอธิบายเท็จทันทีที่ route เปลี่ยน)

**สิ่งที่เปลี่ยนบนพื้นผิวที่คนอื่นเกรดอยู่:** โทเคนคอนโซล `LANE_HOOK_FIRED` → `LANE_GM_CHAT_ACTION` (stderr เหมือนเดิม)
· อีเวนต์ `gm_chat_command_*` → `gm_chat_action_*` · audit ndjson เหมือนเดิม (ทางเดียวกัน)
⇒ **`GT-127` ด่าน 2 ของสาย GM ล้าสมัย** แจ้งเจ้าของใบแล้ว ไม่แตะเนื้อใบให้

**วันนี้ยังไม่มีไบต์ออกสาย** `FORCE_POS_VITAL_VERSION_CONFIRMED = None` (ล็อกโดย `COO-DECISION 2130`)
⇒ `/warp` จบที่ `gm_chat_action_warp_withheld_...re129_open` · GM-029 เปิดท่อ ไม่ได้ปลดเกต

**ผลข้างเคียงที่ไม่ซ่อน:** `lane_hooks/lane_gm_chat_command.py` กลับเป็น registered-but-never-fired
⇒ WIRED v2 ของโมดูลนั้น = 0 emission · ชะตาของมันเป็นการตัดสินของสาย GM ไม่ใช่ของผม

## 2. ด่าน cp874 ก่อน push (ตอบใบ `2315` ของสาย A)
ใบแจ้งว่าสองไฟล์ใน `tools/` encode cp874 ไม่ผ่าน **ถูกครึ่งเดียว**: อักขระมีจริง 4 จุด แต่
**ไม่มีจุดไหนถึง `print()`** (คอมเมนต์ 2 · docstring 1 · สตริงที่ถูกเขียนลงไฟล์ด้วย `encoding="utf-8"` 1)
และเกตพินทั้งสองไฟล์ไว้แล้วในตาราง `ALLOWED` ⇒ ไม่ใช่ "รอบที่ตายคาที่" และไม่ใช่เกตแดง

สิ่งที่ทำแทนการลบอิโมจิ: `tests/test_tree_is_cp874_safe.py` — ด่านเดียวกับเกต **รันบน Linux ก่อน push ได้**
สแกน `.py` tracked ใต้ `tools/ src/ current/` เทียบกับตาราง `ALLOWED` **ที่อ่านออกมาจาก `gate-windows.yml` เอง**
(ไม่ก๊อปตัวเลข ⇒ ดริฟต์ไม่ได้) · ตรวจทั้ง working tree และ blob ที่ `HEAD`
[วัดแล้ว] เขียวบนทรีปัจจุบัน · แดงจริงเมื่อแทรก `U+1F534` หนึ่งตัว (ทดสอบแล้วคืนไฟล์กลับ)
ราคาที่ปัญหานี้เคยกิน: `pirate-force-server#200` ถูกปิดทั้งใบ + หนึ่งรอบของสาย GM ไปกับการกู้

จุดที่ 4 (บรรทัด 235 ของ census) **ลบบนคลาวด์ไม่ได้เชิงกลไก** — เครื่องมือเทียบ artifact ที่ commit ไว้แบบไบต์ต่อไบต์
regenerate ต้องมีอิมเมจ ⇒ เปิด **`RE-135` [STATIC-ON-BRIDGE]** + จด `IMAGE_ACCESS_COST.tsv`

## 3. คิวและกล่องจดหมาย
- `GT-132` ขึ้นหัวสารบัญ `GAME_TEST_QUEUE.md` พร้อมป้าย "ใบแรกของกะ attended ถัดไป" ตาม **COO 23:45 ข้อ 3**
- เปิด `RE-135 CP874-CENSUS-ARTIFACT-REGEN-001` (ท้าย `CLIENT_RE_QUEUE.md`)
- บริโภค + stub: `20260828_2315_LANE-A-NOTICE-cp874` · อัปเดต stub ของ `20260828_1930_GM-029` ว่าต่อสายจริงแล้ว
- จดหมายออก 2 ใบ: `20260829_0010_CHIEF-REPLY-LANE-A-cp874-*` · `20260829_0015_CHIEF-REPLY-CORE-REQUEST-GM-029-*`

## 4. งานที่ยัง **ไม่** ได้ทำในรอบนี้ (ห้ามให้หาย)
1. 🔴 **COO 23:45 (port royal) สั่ง chief: ขยายแหล่ง placement 115 → 149 ตาม §⑥.2 ของสาย A · กำหนด "ภายในรอบผู้บริหาร 09:00"**
   — รอบนี้ไม่ทำ เพราะ CORE-REQUEST มาก่อนตามลำดับหน้าที่ข้อ 3 และงานนี้ใหญ่กว่าที่จะยัดใบเดียวกัน ⇒ **หัวรอบถัดไป**
2. `AGENTS.md` (pf_bridge) ยังเกินเพดาน 30 KB อยู่ 7,583 ไบต์ ตามที่ R216 รายงาน — ยังไม่มีปลายทางใหม่ให้ย้าย
   · 🔴 `CHIEF_CONTINUATION.md` หลังรอบนี้ = **30,599 ไบต์ จากเพดาน 30,720** ⇒ รอบถัดไปที่เขียนบรรทัดดัชนีจะเกิน ต้องยุบก่อน
3. งานแม่บ้าน 17.9 (ก)(ข)(ค): ยังไม่ทำรอบนี้ · กล่องจดหมายยังมีใบถึง chief ที่ไม่มี stub ค้างจาก 27 ส.ค. หลายใบ
4. ลบ `U+1F534` สามจุดที่ลบได้ + ลดพินในคอมมิตเดียวกัน (คนละเรื่องกับ PR รอบนี้)

## 5. WIRED
`WIRED = 1 / 2` — โมดูลใน `lane_hooks/` มีสองใบ (`lane_gm_run_command`, `lane_gm_chat_command`)
ที่มี emission จริงบน production path เหลือ **หนึ่ง** (`vital_inbound_gm_run_command` ที่สาขา `0x51E9`)
เพราะ GM-029 ถอดจุดยิงของอีกใบออกโดยเจตนา (แทนที่ด้วยเส้นทาง action ที่ส่งไบต์ได้จริง ซึ่ง hook ทำไม่ได้)

## 6. หลักฐานและด่าน
- สวีตคลาวด์เต็ม: **3963 passed · 323 skipped · 5505 subtests** (เขียว(cloud sanity) เท่านั้น — ไม่ใช่เกตเต็ม)
- `HYPOTHESIS_LEDGER` **PASS 47** ไม่มี drift (ตรวจก่อน commit ตามหัวข้อ 7)
- ไม่มีชั้น client-observable ในรอบนี้ ⇒ **ไม่มี `OBSERVER_CONFIRMED`** และไม่มีใบไหนถูกปิดด้วยผลของรอบนี้
