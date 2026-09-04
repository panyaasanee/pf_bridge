R335, LANE-E session `2vfbtf`
start: 2026-09-04T09:23+07:00

# ขยับ NOW ข้อไหน

`NOW.md` "งานด่วนตอนนี้" ไม่มีรายการที่จ่าหน้าถึง chief โดยตรงรอบนี้ — งานของรอบนี้ทั้งหมดมาจาก
`COO-DECISION 20260904_0848` (จ่าหน้าถึง chief ตรง ๆ) ซึ่งไม่ใช่ M1-M6 บนบันไดไมล์สโตน แต่เป็นหนี้
กระบวนการที่ COO จัดให้ "ทำ 0550 ข้อ 3 เป็นงานแรก" — ไม่ขยับ M2-M6 รอบนี้

# ทำอะไรไปบ้าง

## ข้อ 1 — `decide`/`finish`/`reap` ต้องตัดสินจาก run `pull_request` เท่านั้น (pirate-force-server, 1 ไฟล์)

**ก่อนแก้**: ยืนยันเอง (ไม่เชื่อ pf-adversary รอบก่อนเปล่า ๆ) ว่า `merge-claude-pr.yml` อ่าน conclusion ของ
job `gate` ไม่ใช่ของ run — ถูกต้องตามที่รายงานไว้ (`GATE=$(... .jobs[] | select(.name == $n) ...)`)

**ไล่ย้อนตามที่ `0848` ข้อ 1 สั่ง** (spawn agent แยก ไม่ปนกับ context หลัก): `gate-windows` ทุก run บน
`pirate-force-server` ตั้งแต่ 2026-09-01T00:00Z — push run 571 · pull_request run 512 · head_sha ที่มีทั้งสอง
ฝั่ง 510 · run-level conclusion ไม่ตรงกัน 27 sha · ยืนยันที่ระดับ **job `gate`** (ไม่ใช่ run-level) ทั้ง 27 ·
รูปแบบอันตราย (`push=success` / `pull_request=failure`) 16 ใน 27 · จับคู่กับ PR ที่ **merge จริง** (ไม่ใช่แค่มี
run) เหลือ **6 ใบที่ยืนยันแล้ว**:

| PR | head sha | push run (gate) | pull_request run (gate) | merged_at UTC | ห่างกัน |
|---|---|---|---|---|---|
| `#605` | `1802d29a` | success @15:59:49 | **failure** @16:01:19 | 16:00:13 | push ก่อน 18s |
| `#578` | `b77acc1a` | success @08:01:05 | **failure** @08:03:34 | 08:01:23 | push ก่อน 18s |
| `#581` | `81acbc78` | success @08:46:00 | **failure** @09:00:41 | 08:46:18 | push ก่อน 18s |
| `#590` | `28ecb2b2` | success @12:05:13 | **failure** @12:06:39 | 12:05:33 | push ก่อน 20s |
| `#606` | `faee8370` | success @16:20:03 | **failure** @16:22:30 | 16:20:25 | push ก่อน 22s |
| `#668` | `fc547458` | success @11:49:09 | **failure** @11:57:10 | 11:49:37 | push ก่อน 28s |

หลักฐานยืนยันอิสระ: `#668` มี PR ตามหลังของโปรเจกต์เองชื่อ `#670` "R324b: main is red on the tick gate
landing" ซึ่งเป็นงานเก็บกวาดของบั๊กที่ `#668` ก่อไว้พอดี

**ที่ยังไม่ได้ทำ**: ตรวจว่าอีกห้าใบ (`#605` `#578` `#581` `#590` `#606`) ยังมีความเสียหายค้างอยู่บน `main`
หรือไม่ (`#668` รู้แล้วว่ามี `#670` ซ่อมตาม) — ส่งต่อเป็นงานรอบถัดไป รายงานเต็มถึง COO แล้ว:
`notes_to_chief/20260904_0936_CHIEF-TO-COO-URGENT-push-run-merged-red-six-times-since-sep1.md`

**แก้**: สามจ๊อบ (`decide` เพิ่ม env `EVENT: ${{ github.event.workflow_run.event }}` แล้ว exit 0 ถ้าไม่ใช่
`pull_request` ก่อนแตะ PR ใด ๆ · `finish`/`reap` เติม `.event == "pull_request"` เข้าไปในตัวกรอง run ที่ใช้ตัดสิน
LIVE/GREEN ทั้งคู่ — เดิมสองจ๊อบนี้ไล่ทุก `gate-windows` run โดยไม่สนใจ event เลย ซึ่งเป็นบั๊กเดียวกันแต่ไม่ผูก
กับจังหวะแข่ง เจอเองระหว่างอ่านโค้ดตามคำสั่ง "verify the line yourself" ไม่มีใครบอก)

## ข้อ 2 — รั้ว claim-PR-มี-marker-แต่ไม่มีของจริง (pf_bridge, 1 ไฟล์)

ร่างแรก: claim PR (title ลงท้าย "claim") ที่ marker ติดมาตั้งแต่เปิดน่าจะมีคอมมิตเดียว (แค่ไฟล์ `_claim.md`)
เพราะงานจริงยังไม่ถูก push ลงกิ่งเดียวกัน — ใช้ `commits` จาก pulls API ลงทั้ง job `merge` (event path) และ
`reap` (schedule sweep) — ไม่แตะ `finish`/`decide` เพราะฝั่ง pf_bridge ไม่มีจ๊อบชื่อนั้น (คนละไฟล์กับข้อ 1)

🔴 **`pf-adversary` (สั่งต้นรอบ ผลคืนก่อนปล่อยล็อก) จับได้ว่าร่างแรกผิดสองข้อ**:
1. **`commits<=1` ไม่กัน `#1079` เองด้วยซ้ำ** — ประวัติจริงของ `#1079` มีสองคอมมิตตั้งแต่เปิด (claim + "merge
   main before push" ที่ข้อ 3 ของรอบนี้เพิ่งบังคับเป็นกฎ) เพราะสะพาน Windows commit ลง `main` ทุกไม่กี่นาที
   ทำให้ก้าวแรกที่บังคับให้ทำก่อน push ("merge main ติดกับ push") สร้างคอมมิตที่สองแบบไม่มีเนื้อได้ก่อนมีงาน
   จริงเลย ⇒ `COMMITS -le 1` เป็นเท็จตั้งแต่ต้น การ์ดไม่ทำงาน
2. **ไม่มีเพดานเวลา** ต่างจากทุก skip อื่นในไฟล์นี้ ⇒ ถ้ารอบตายกลางทางหลังทำผิดกติกา (ใส่ marker ตอนเปิดจริง)
   PR จะค้าง**ตลอดกาล**: merge ไม่ได้ (การ์ดกัน) ปิดก็ไม่ได้ (ไม่เคยไปถึงเส้นทาง mergeable/close เพราะการ์ด
   ออกก่อนเสมอ) — ตรงข้ามกับหลักการที่ทุก skip อื่นในไฟล์เขียนกำกับตัวเองไว้ชัดว่า "ต้องมีเพดาน"

แก้ทั้งสองข้อ: เปลี่ยนสัญญาณเป็น `changed_files<=1` (ไฟล์ diff จริงเทียบ `${DEFAULT_BRANCH}` — "merge main
ติดกับ push" ที่เป็น no-op จริงจะไม่ขยับเลขนี้ ต่างจาก `commits`) และเติมกรอบเวลา `PF_STALE_MINUTES` ให้
`reap`: ยังอยู่ในกรอบ = ปล่อยไว้ (รอบอาจยังทำงานอยู่) · เกินกรอบ = ปิดพร้อมคอมเมนต์บอกเหตุผล เก็บกิ่งไว้
(ทรงเดียวกับทุก close path อื่นในไฟล์นี้)

## ข้อ 3 — สามถ้อยคำ `AGENTS.md` §7 (pf_bridge, 1 ไฟล์)

เพิ่มสามบูลเล็ตต่อท้ายลิสต์เดิมของ §7 แทนการเขียนทับ: (ก) merge `origin/main` ติดกับ push เสมอ (ข) แตะ skip
ใด ๆ (เพิ่ม ลบ ย้าย) ต้องซ้อม `skip_census` (ค) ห้ามพิมพ์จำนวนของสายอื่นลงคอมเมนต์/fixture — แต่ละข้ออ้างอิง
กฎเดิมที่มันแก้/ขยาย ไม่ได้ลบของเก่า (หนี้ขนาดไฟล์ `AGENTS.md`/`CHIEF_CONTINUATION.md` ยังไม่ต้องจ่ายตามที่
`0848` บอก — ยังไม่จ่ายรอบนี้)

## ข้อ 4 — dispatcher พิมพ์ nested vital ทุกเฟรม (pirate-force-server, 2 ไฟล์)

`_say_dispatch_nested_vitals` ใหม่ใน `runtime.py`, เรียกเป็นบรรทัดแรกของ `dispatch()` ทุกครั้ง พิมพ์
`DISPATCH_NESTED_VITALS vital_count=<n> first_nested_id=0x<hex|none>` พร้อมประโยคเตือนว่า vital ถัดจาก
ตัวแรกไม่ถูกถอด **ไม่ได้ทำเกินคำสั่ง**: `parse_outer` (frozen v141) ถอด nested vital ตัวแรกตัวเดียวจริง
ตามคอมเมนต์ของมันเอง ("with more than one, boundaries require each vital's serializer schema") — ไม่มีทาง
เจนเนอริกที่จะถอด vital ตัวที่สองได้โดยไม่รู้สคีมาของตัวแรกก่อน จึงพิมพ์เท่าที่มีจริง (count + id ตัวแรก)
ไม่ใช่ "ทุก id" ตามตัวอักษร — เขียนเหตุผลไว้ในคอมเมนต์และ docstring ของเทสครบ

เทสใหม่ `tests/test_dispatch_nested_vital_visibility.py` 4 ตัว ผ่านเสมอ (รันจริงกับ dispatcher จริงผ่าน
`make_state_class`, ไม่ mock): เฟรม 1-vital พิมพ์ id ถูก · เฟรม 2-vital พิมพ์ count=2 + เตือน "NOT visible" ·
เฟรมไม่มี VitalData พิมพ์ `none` ไม่ crash · บรรทัดพิมพ์ทุกเฟรมจริง (ไม่ dedupe แบบ `_vital_walk_say`)

## ข้อ 5 — ตั้งเลข `RE-232` ให้ LANE-CS (pf_bridge, 1 ไฟล์)

`CLIENT_RE_QUEUE.md` — token grammar ของ `s_CAST_CONDITION`/`s_CAST_BEHAVIOR` ขอบเขต 8 สกิลในสารบัญ
(ไม่ขยายเต็ม 2,165 แถว) ตามที่ LANE-CS เสนอไว้ในใบ `0755` ข้อ 4 · ตัวนับร่วมสองคิวคืน `231` (`GT-231`) ⇒
`RE-232` · แจ้ง LANE-CS แล้ว

## แก้ branch ผิดกลางรอบ

เริ่มรอบด้วยการสร้างกิ่งเองชื่อ `claude/e-round-2vfbtf` (ตามธรรมเนียมในพรอมป์ที่สมมติว่าระบบสุ่มชื่อกิ่งให้
ทุกรอบ) แทนที่จะใช้กิ่งที่ระบบจริงกำหนดไว้แล้ว `claude/cool-johnson-ago0wg` — เปิด PR `pf_bridge#1095` ไปก่อน
พบตอนจะ push งานจริง แก้โดยย้ายงาน (uncommitted) มา checkout กิ่งที่ถูกต้อง fast-forward กับ main แล้ว
เดินต่อจากตรงนั้น · `#1095` ปล่อยไว้ให้ reaper เก็บเอง (ไม่มี marker ไม่มีความเสี่ยง ไม่ปิดมือ ตามกฎ "ห้ามปิด
PR เอง") · commit เดียวที่เคยขึ้นกิ่งนั้น (ไฟล์ claim เปล่า) ไม่มีผลกระทบอะไรอยู่แล้ว

# อะไรที่ไม่ได้พิสูจน์ / ยังไม่ได้ทำ

- ไม่ได้ตรวจว่า 5 ใน 6 ใบที่พบว่า merge ผิดทาง ยังมีความเสียหายค้างบน `main` หรือไม่ (มีแค่ `#668`/`#670`
  ที่รู้แน่ว่าถูกซ่อมแล้ว) — งานรอบถัดไป
- CORE-REQUEST `0453`/`0621` ของ LANE-UI (คิวต่อจากข้อ 1-5 ตาม `0848`) ยังไม่ได้ทำ — เวลาไปกับการไล่ย้อน
- CORE-REQUEST ของ LANE-DB (`0844`, boot-time backfill loop) รับทราบและตอบคำถามเดียวที่ถามแล้ว แต่ยังไม่เปิด
  PR — งานรอบถัดไปของผม
- `pf-adversary` สั่งต้นรอบ — **ผลคืนก่อนปล่อยล็อก จับได้ 1 ข้อจริง** (การ์ดข้อ 2 ผิดสองจุด แก้แล้ว ดูหัวข้อ
  ข้อ 2 ข้างบน) ที่เหลือ (workflow ฝั่งเซิร์ฟเวอร์, ถ้อยคำ `AGENTS.md`, `RE-232`, `_say_dispatch_nested_vitals`
  + เทส) รายงานว่าสะอาด รวมถึงรันชุดเต็มยืนยันเอง (8593 passed) ว่าบรรทัด print ใหม่ไม่ทำเทสที่เข้มงวดเรื่อง
  เนื้อคอนโซลที่อื่นพัง — ไม่มี `ADVERSARY_PENDING` เหลือค้างรอบนี้
- รันชุดเต็ม `pytest tests/` บน `pirate-force-server` ในสภาพไม่มี `pf_bridge` ข้าง ๆ (บังคับเพราะเพิ่มไฟล์เทส
  ใหม่) แล้ว **ทั้งสองช่อง**: `pytest_subset` **8600 passed, 83 skipped, 16681 subtests passed** exit 0 ·
  `skip_census` **`every skip is declared, named and pinned` / `RESULT: PASS`** exit 0 (modules excluded: 48
  ตรงกับ `pytest_subset`) — ไฟล์เทสใหม่ไม่มีคำว่า `GameClient`/`capture_v141` จึงไม่เข้าลิสต์ยกเว้น ไม่เพิ่ม
  skip ใด ๆ

# สถานะ PR (ปรับปรุงหลัง push — ดู FROM_CHIEF letter)

รอ push ครบก่อนเขียนส่วนนี้จริง

WIRED = ไม่เปลี่ยน (รอบนี้เป็น process/workflow/บันทึกล้วน ไม่มีจุดเสียบเลนใหม่ที่ production path นับ)
