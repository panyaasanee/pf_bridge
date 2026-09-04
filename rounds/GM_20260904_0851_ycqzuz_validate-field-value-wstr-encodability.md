# รอบ `ycqzuz` (LANE-GM) -- 2026-09-04T08:51+07:00

## ข้อ A (ตรวจชะตา PR รอบก่อน)
รอบก่อน (`4fxkam`) -- `pf_bridge#1082` และ `pirate-force-server#714`: `merged=true` ทั้งคู่
(ยืนยันด้วย `git merge-base --is-ancestor` บนโคลนที่ `git fetch origin main` แล้ว ไม่ใช่ฟิลด์ API)
งานอยู่บน main แล้ว ไปต่อ ไม่ต้อง cherry-pick

## ข้อ B (กล่องจดหมาย)
- `ADDRESSEE: LANE-GM` ที่ยังไม่มี `.CONSUMED.txt`: ไม่มีใบใหม่ (ตรวจด้วย grep วันนี้ทั้งไฟล์)
- ใบของตัวเองที่รอคำตอบ ยังไม่มีคำตอบใหม่: `20260904_0729_LANE-GM-CORE-REQUEST-GM-053-*`
  (รอ chief), `20260904_0752_LANE-GM-ASK-COO-*` (รอ COO) -- ไม่ใช่ตัวบล็อกรอบนี้ตามกฎ "อย่ารอ"
- บริโภคใบ `20260904_0305_CHIEF-TO-LANE-GM-three-attr-wire-sentences-are-now-false-and-one-contract-has-two-answers.md`
  รอบนี้ (ค้างจากสองรอบก่อน -- ดูหัวข้อ "งานของรอบนี้")

## งานของรอบนี้: `validate_field_value` ปิดช่องโหว่ "สองคำตอบ" ที่สอง (wstr)

จดหมาย `0305` มีสามข้อ:
1. สามประโยคที่บอกว่าจุดอ่านของ chief "ยังไม่มี" -- **แก้ไปแล้วในรอบก่อนหน้า** (`3qh50k`/`4fxkam`)
   ตรวจซ้ำวันนี้: `grep -n "does not exist yet\|NOT YET BUILT" gm/attr_wire.py` เจอเฉพาะประโยค
   ที่พูดถึง "จุดอ่านที่สอง" (`current_login_attr_bytes`) ซึ่งยังไม่มีจริง -- ถูกต้องตามสภาพจริง ไม่ใช่ของค้าง
2. `validate_field_value` สองคำตอบ (x=1 `name` รับ lone surrogate ผ่าน แต่ `encode_field` โยน
   `UnicodeEncodeError`) -- **ค้างสองรอบ (`tof9cw`, `4fxkam`) รอบนี้ปิด** (ดูรายละเอียดด้านล่าง)
3. แยก `no_source_registered` ออกจาก `missing_named_rows` -- **แก้ไปแล้วในรอบก่อนหน้า** (`4fxkam`)
   ตรวจซ้ำวันนี้: `gm/attr_wire.py:1113-1116` มีการแยกจริง

### การแก้ (ข้อ 2)
เพิ่ม probe `value.encode("utf-16le")` ในสาขา `wstr` ของ `validate_field_value` แล้วจับ
`UnicodeEncodeError` แปลงเป็น `AttrWireError` ที่มีชื่อฟิลด์กำกับ -- แพทเทิร์นเดียวกับที่ f32 ใช้
`struct.pack` เป็นตัวถาม (รอบ `3qh50k`, D8) เพราะเป็น call เดียวกับที่ `encode_field` เรียกจริง
(`value.encode("utf-16le")` ที่ `encode_field` บรรทัด 772 -- `grep -n 'body = value.encode'`)
จึงรับประกันว่าตรงกันเสมอ

### pf-adversary (สั่งต้นรอบ ผลคืนก่อน push)
รันบน git worktree แยก ไม่แตะ checkout จริง ตรวจ: probe ตรงกับตัว encoder เป๊ะ · ไม่ false-positive
กับอักษรไทย/CJK/astral character (มีแค่ lone surrogate ที่ถูกปฏิเสธ) · ราคา ~376ns ไม่ใช่ hot path
· ไม่มีช่องโหว่แบบเดียวกันเหลือใน u*/i32/blob · เทสใหม่ตายจริงเมื่อ revert (ตรวจด้วยมือ)
· ไม่แตะไฟล์นอกเขต

**สิ่งที่ผลจับได้ -- ไม่ใช่บั๊กโค้ด แต่เป็นคำอ้างเกินจริงในดอกสตริง/คอมเมนต์ร่างแรก**: ร่างแรกเขียนว่า
`UnicodeEncodeError` "ไม่ใช่ `ValueError`" และ "หลุด `except ValueError, RuntimeError` ใน `runtime.py`"
เทียบเท่ากับช่องโหว่ `OverflowError` ของ f32 -- **ผิด**: `UnicodeEncodeError` **เป็น** `ValueError`
subclass จริง (`issubclass(UnicodeEncodeError, ValueError) is True`) และ `runtime.py` ยังไม่มีจุดเรียก
`encode_field`/`encode_block` เลย (grep ว่าง) ⇒ ไม่มี `except ValueError` ใดถูกข้ามจริง เหตุผลจริงที่
ต้องแก้คือ `live_named_values`/`live_login_bytes` จับเฉพาะ `AttrWireError` ในโมดูลเดียวกัน ค่าที่หลุด
`validate_field_value` จะถูก seed เข้า `RawBlockCache` ได้โดยไม่มีใครจับ -- แก้ดอกสตริง+คอมเมนต์+เทส
ให้พูดเหตุผลที่ถูกก่อน push แล้ว (ตรวจด้วย `python3 -c "import ...; issubclass(...)"` และ
`grep -n "encode_field\|encode_block" runtime.py` เอง ยืนยันตรงกับที่ adversary รายงาน)

ระหว่างแก้คอมเมนต์ยังเจอ cp874 แดง (ตัวอักษร `§` หลุดเข้าไปตอนพิมพ์ "letter `0305` §2") --
`tools_bridge/pf_gate_preflight.py --repo` จับได้ก่อน push แก้เป็น "item 2" ธรรมดา preflight เขียวแล้ว

**เขต GM ทั้งหมด**: `gm/attr_wire.py` (`validate_field_value` สาขา wstr + ดอกสตริง)
`tests/test_gm_attr_wire.py` (เทสใหม่หนึ่งตัวใน `ValidatorIsOneAnswerTests`) `docs/GM_LANE.md`

## ผู้เทสจะทำอะไรได้ที่เมื่อวานทำไม่ได้
ไม่มี -- รอบนี้ไม่แตะเส้นทางที่ผู้เทสไปถึงได้ (x=1 ยังไม่มีจุดเรียกจาก `runtime.py`)
ปิดช่องโหว่ภายในของโมดูลเพื่อไม่ให้ `RawBlockCache` ถูก seed ผิดถ้าประตูนี้เปิดใช้งานในอนาคต

## nonclaim
1. ไม่ได้บูตเซิร์ฟเวอร์/เกม ไม่มีไบต์ `0x309A` ออกจากประตูใดที่ไม่เคยออกอยู่แล้ว
2. ไม่อ้างว่า `/speed`/(b'')/M2/M3/M4/P-2/P-3 ขยับ -- ทั้งหมดบล็อกภายนอกเหมือนเดิม
3. ไม่อ้างว่า `UnicodeEncodeError` เคยหลุดตาข่ายจริงใน `runtime.py` -- ไม่เคย เพราะยังไม่มีจุดเรียก
   ให้หลุด (ร่างแรกของรอบนี้เขียนผิด pf-adversary จับได้ แก้ก่อน push แล้ว)
4. ไม่แตะ `runtime.py` / `app.py` / `pf_login_game_server_v141.py` / canonical DB /
   `scenarios/world_*.json` / `scenarios/combat_*.json` / `live_named_attr_values.py`

## ผลชุดเต็ม (commit สุดท้ายจริง หลังแก้ตามผล adversary แล้ว)
`git fetch origin main` (`2cdee26`, อยู่ใน HEAD แล้ว ไม่ต้อง merge) → `python3 -m pytest tests/ -q`
บน commit `c01bad30e66eb592ed82d6b04aed130bee3d4f24`:
**9,518 passed · 328 skipped · 18,649 subtests passed · exit 0** (376 วินาที)
เขียว(cloud sanity) เท่านั้น -- ยังไม่เห็นผลเกต Windows/Actions จากที่นี่ ห้ามอ่านบรรทัดนี้ว่าเกตเขียว

## backlog (รอบหน้าอ่านตรงนี้)
1. รอ COO: ใบ `0752` สามข้อ (x=9, 18 แถวที่ไม่มีประตู, Door B adjudicator)
2. รอ chief: `CORE-REQUEST-GM-053` (mask ต่อคอนเนกชัน) · จุดอ่านที่สอง `current_login_attr_bytes`
   · เลขใบ GT (b'') · ใบ RE ที่สองของ P-2 (`0217`) ยังไม่ออก
3. P-3 สารบัญปุ่ม GMUI 3 หน้า -- รอ client image (คลาวด์ไม่มี) ยังบล็อกภายนอก
4. RE-222 ยังเปิดอยู่ (สาย RE ยังไม่ตอบ) -- ไม่ใช่ของ LANE-GM รอเฉย ๆ
5. `live_named_attr_values.py` ยังเขียน "26" ไม่ใช่ "27" (นอกเขต ใบ `0554` ยังไม่มีคำตอบจาก chief)

## สถานะท้ายรอบ
push แล้ว รอ merge PR **#719** (`pirate-force-server`) -- **เปิดแล้ว รอ gate** (marker `PF-AUTOMERGE: v4`
ยืนยันด้วย `pull_request_read` แล้วว่าอยู่ใน body จริง · `mergeable_state=unstable` = เกตกำลังวิ่ง)
`pf_bridge#1092` = claim ของรอบนี้ -- เติม marker ตอนจบรอบ = ปลดล็อก
🔴 **ไม่ได้เขียนว่าเสร็จ และไม่ได้อยู่บน main** -- รอบถัดไปวัดด้วย `merged=true` ตามข้อ A
