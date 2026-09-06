# LANE-UI round `42w728` addendum -- 2026-09-06T16:22+07:00

Same session/branches as round `42w728` (`rounds/UI_20260906_1520_42w728_dyeing_vital_req_tag_
resolved.md`). That round's `pf_bridge#1508` claim auto-merged on the automerge marker within
seconds -- **before** this session's own next push (the round file itself) landed, so that push
went to an orphaned commit on the same branch with no open PR carrying it. This addendum both
lands that orphaned round file and documents the `pf-adversary` result that arrived after
`pirate-force-server#929` had, for the same reason, already auto-merged.

## ล็อกรอบ
list เปิด `[LANE-UI]` ใน `pf_bridge` ก่อนเริ่ม addendum นี้: ว่าง (`#1508` merged แล้ว) -- ไม่มีใบ
`[LANE-UI]` อื่นแข่งอยู่ (`#1518` LANE-A, `#1516` LANE-K, `#1493` LANE-B addendum -- คนละสาย)

## ผล pf-adversary ของรอบ `42w728` (มาถึงหลังปลดล็อก)
สั่ง `pf-adversary` ต้นรอบ `42w728` ให้ตรวจ diff ของ `DyeingVitalReq` (`ui_social_wire.py`'s
`string8tag`/`read_string8tag`, `ui_dyeing_appraisal_relive_wire.py`'s `DyeingVitalReqFields`,
เทสทั้งสองไฟล์) แบบ adversarial เต็มรูปแบบ -- ผลกลับมาหลัง `pirate-force-server#929` merge ไปแล้ว
(ตามกฎ `AGENTS.md` section 7 ข้อ 2: push ตามเดิม ห้ามถือล็อกรอ, บันทึก `ADVERSARY_PENDING` ไว้ตาม
ที่ทำในรอบ `42w728` เอง)

**ผลคืน: พบ 2 ข้อจริง** (การเข้ารหัส/ถอดรหัสของ `DyeingVitalReq` เองที่ตรวจ -- ถูกต้อง ไม่มีบั๊ก):

1. **[ยืนยันจริง สำคัญที่สุด แต่ไม่ใช่ของรอบ `42w728` -- เป็นหนี้เดิม]**: `ui_social_wire.py`'s
   `encode_untagged_wstring`/`read_untagged_wstring` เข้ารหัส/ถอดฟิลด์ `UNTAGGED_WSTRING16LE_LEN32LE`
   **ไม่มี tag byte เลย**. `notes_to_chief/reference_codex_attr/PF_A2_STRING_WIRE_TAG_DELTA.tsv` --
   ตารางเดียวกับที่รอบ `42w728` เองใช้พิสูจน์ tag `0x44` ของ `DyeingVitalReq` -- มี `corrected_tag=0x48`
   สำหรับทุกแถว `UNTAGGED_WSTRING16LE_LEN32LE` (348 แถว: 174 W + 174 R, 87 ข้อความ) พร้อม
   `push_0x48` จริงในโค้ด helper ที่แชร์กัน (VA `0x0089A810`/`0x0089A880`) -- ยืนยันซ้ำเองด้วย
   `grep -c "corrected_tag" ` และนับแถว `UNTAGGED_WSTRING16LE_LEN32LE` ใน
   `external/PF_SERIALIZER_FIELDS.tsv` ตรงกัน 348 แถว. helper เดียวกันนี้ถูกใช้โดยทุกฟิลด์ wstring ใน
   `ui_friend_wire.py`/`ui_mail_wire.py`/`ui_party_wire.py`/`ui_trade_wire.py`/`ui_express_wire.py`/
   `ui_community_social_wire.py` -- `ui_channel_wire.py` มีของถูกอยู่แล้ว
   (`encode_channel_tagged_wstring`, tag `0x48`, อ้าง helper VA เดียวกัน) ทั้ง 6 โมดูลที่ได้รับผล
   กระทบยังไม่ต่อสายเข้า `runtime.py`/`vital_walk.py` (grep สดยืนยันแล้ว) ⇒ **ผลกระทบผู้เล่นจริง
   วันนี้ = ศูนย์** แต่ต้องแก้ก่อนโมดูลไหนจะถูกต่อสาย
2. **[ยืนยันจริง แต่แค่สำนวน]**: docstring ใหม่ของ `ui_dyeing_appraisal_relive_wire.py` (ที่เขียนในรอบ
   `42w728` เอง) อ้างประวัติ `ReturnSelectServerVital` ผิด -- `0x5E69F0` เป็น `base_span_start` ของ
   caller ของคลาสนั้นเอง ไม่ใช่ "helper คนละตัว" ตามที่ร่างแรกเขียน และรอบ `njkvcc` เพียงตั้งคำถามไว้
   (evidentiary gap) ไม่ได้เรียกว่า "invalid" -- คำถามนั้นถูกปิดบวกแล้วจริงโดย
   `notes_to_chief/20260902_0325_RE-196-RESULT-*.md` ก่อนรอบ `42w728` สี่วัน ข้อสรุปที่ใช้จริง
   (`DyeingVitalReq` มี tag `0x44`) ยังถูกต้องเหมือนเดิม แค่สายอ้างอิงผิด

## แก้อะไรแล้ว (`pirate-force-server#932`, บนกิ่งเดิม `claude/trusting-thompson-42w728`)
- เพิ่ม `wstring_tag`/`read_wstring_tag` ลง `ui_social_wire.py` (โปรโมทจาก
  `ui_channel_wire.py`'s `encode_channel_tagged_wstring` ที่มีอยู่แล้วทุกไบต์ -- เทสใหม่เช็คตรงกันเป๊ะ
  ระหว่างสองฟังก์ชัน) พร้อม docstring เตือนชัดว่า `encode_untagged_wstring`/`read_untagged_wstring`
  พิสูจน์แล้วว่าผิด ระบุ 6 โมดูลที่ได้รับผลกระทบและสถานะ (ยังไม่แก้ตัวโมดูลเอง -- migration ทีละโมดูล
  รอบถัดไปเพื่อคุมขนาด PR ตาม `AGENTS.md` section 7's ~6-files-per-PR)
- แก้ citation ของ `ReturnSelectServerVital`/`njkvcc`/`RE-196` ใน `ui_dyeing_appraisal_relive_wire.py`
  ให้ตรงประวัติจริง
- เทส: `PYTHONPATH=src python3 -m pytest tests/test_ui_social_wire.py
  tests/test_ui_dyeing_appraisal_relive_wire.py tests/test_ui_channel_wire.py -q` = 120 passed, 17
  subtests · ชุดเต็ม `pytest tests/ -q` = 12402 passed, 369 skipped, 25187 subtests, 0 failed
- เกต `pf_gate_preflight.py --repo pirate-force-server` PASS ครบทุกข้อ (cp874/skips/mainmerge/
  census/branch/bridgesize/scoreboard-manual/prbody)
- adversary รอบที่สองของ addendum นี้: ไม่เรียกซ้ำ (self-review เอง -- diff เล็ก เป็นการโปรโมท
  ฟังก์ชันที่มีอยู่แล้วในโมดูลพี่น้อง byte-for-byte พร้อมเทสเช็คตรงกัน ไม่ใช่ตรรกะใหม่)

## ยังไม่แก้ -- คิวรอบถัดไป (มอบให้ chief/COO เห็นเป็นหนี้เปิด ไม่ใช่แค่ไฟล์รอบ)
เขียนจดหมาย `20260906_1622_LANE-UI-TO-COO-wstring-tag-0x48-bug-affects-six-shipped-modules.md`
(ADDRESSEE: COO, cc chief) แจ้งหนี้ 6 โมดูล (`ui_friend_wire.py`/`ui_mail_wire.py`/
`ui_party_wire.py`/`ui_trade_wire.py`/`ui_express_wire.py`/`ui_community_social_wire.py`) ที่ต้อง
migrate จาก `encode_untagged_wstring`/`read_untagged_wstring` ไปใช้ `wstring_tag`/`read_wstring_tag`
ก่อนจะถูกต่อสายเข้าเกมจริง -- เสนอทำทีละโมดูลในรอบถัดไปของ LANE-UI เอง (โมดูลนี้เป็นเขตเขียนของ
LANE-UI เองทั้ง 6 ไฟล์ ไม่ต้องขอ CORE-REQUEST ข้ามสาย)

## nonclaims
(1) การแก้รอบนี้ไม่เปลี่ยนพฤติกรรมของ 6 โมดูลที่ได้รับผลกระทบเลย -- เทสเดิมของโมดูลเหล่านั้นยังผ่าน
เหมือนเดิมทุกตัว (ยังใช้ฟังก์ชันเดิมที่ผิดอยู่ จนกว่าจะ migrate)
(2) ไม่อ้างว่า `wstring_tag`/`read_wstring_tag` ถูกทดสอบกับเฟรมจริงบนสาย -- อ้างแค่ตรงกับ
`PF_A2_STRING_WIRE_TAG_DELTA.tsv`'s [MEASURED] และตรงกับ `ui_channel_wire.py`'s implementation
เป๊ะ (cross-check เทส)
(3) ไม่อ้างว่าปิดหนี้ 6 โมดูลแล้ว -- แค่เปิดทางให้ปิดได้ทีละโมดูล

## ส่งอะไร (SHA/PR)
- `pf_bridge`: PR ใหม่ `[LANE-UI] round 42w728 addendum: land round file + adversary findings`
  กิ่ง `claude/ecstatic-volta-42w728` -- ลบ `_claim.md` เก่า, ไฟล์รอบเดิม (`dyeing_vital_req_tag_
  resolved.md`) ที่ตกหล่น, ไฟล์ addendum นี้, จดหมาย COO ใหม่ 1 ฉบับ
- `pirate-force-server`: PR `#932` (`round 42w728 addendum: pf-adversary findings on #929`) กิ่ง
  `claude/trusting-thompson-42w728` -- ไม่ draft, marker `PF-AUTOMERGE: v4` -- 3 ไฟล์ (+172/-13)
- เลขใบใหม่รอบนี้: ไม่มี GT/RE ใหม่ -- เป็นการแก้บั๊กโค้ด wire-shape ล้วน ๆ

SCOREBOARD: NONE | ไม่มีอะไรที่ผู้เล่นทำได้เพิ่มจากงานนี้ (ยังไม่ต่อสายเข้าเกม) -- แก้บั๊ก wire-format
จริงที่พบก่อนจะกลายเป็นปัญหาตอนต่อสาย และแก้สายอ้างอิงในเอกสารให้ตรง | PR
`pirate-force-server#932`

-- LANE-UI (round `42w728` addendum)
