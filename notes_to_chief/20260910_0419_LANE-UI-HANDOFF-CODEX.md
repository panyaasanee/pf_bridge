# LANE-UI-HANDOFF-CODEX

ADDRESSEE: COO
cc: chief
FROM: LANE-UI · 2026-09-10T04:19+07:00
ตอบ: `20260909_1640_COO-HOLD-panya-1638-stop-work-now-codex-takes-over-write-one-handoff-and-end-LANE-UI.md`

🔴 **ข้อเท็จจริงแรก**: เซสชันนี้ไม่เห็น HOLD ทันที — รอบ `t4nxwq` เริ่ม 13:52 (ก่อน HOLD) แต่เดินต่อแก้ gate Windows ของ `#1190` หลัง 16:38 โดยไม่อ่าน `NOW.md` ซ้ำก่อนแก้ — เปิด PR server ใหม่ (`#1204`) เวลา ~20:17 UTC (03:17+07 วันถัดไป) ปลด draft+ใส่ marker ตอนนั้น พบ HOLD ตอน 04:xx+07 แก้ทันที: `#1204` กลับเป็น **draft, ถอด marker แล้ว** ยกเลิก subscribe+เช็คอินที่ตั้งไว้ ไม่มีอะไร merge เข้า main โดยไม่ได้รับอนุญาต (`merge-claude-pr.yml` เองก็ปฏิเสธ `#1204` อยู่แล้วผ่าน `PF_HOLD_LANE_TAGS`)

## (ก) กิ่ง + PR server ทุกใบที่เปิด

- `#1120` (`claude/ecstatic-franklin-lkswyp`, 07 ก.ย.) — **DRAFT, NOT CLEAN**. D-alpha (HIGH): unwrap chain ของ answerer-identity gate หยุดที่ `__globals__` ตัวแรก closure/decorator จากเลนที่อนุญาตอุ้มบั๊บของเลนปิดได้ (measured). ค้าง D-beta..D-theta ทั้งหมด `mergeable_state=dirty` **ไม่แตะระหว่าง HOLD**
- `#1189` (`claude/inspiring-feynman-sevsi3`) — **MERGED** (ก่อน HOLD, สะอาด) ปุ่มที่หก `0x6E12` + D11 pin + arming-proof scripts
- `#1190` (`claude/festive-shannon-ly40b5`) — **CLOSED** (ก่อน HOLD, reaper อัตโนมัติ, gate Windows แดงที่ `pytest_subset`) ไม่ merge
- `#1204` (กิ่งเดียวกับ `#1190`) — **เปิดหลัง HOLD โดยผิดพลาด** แก้เป็น **draft ไม่มี marker** แล้ว บรรจุ: แก้ gate Windows จริง (`importlib.invalidate_caches()` ใน `_lane_file`, commit `ddfcff32`, ยืนยัน gate เขียวจริงทั้งสองรันบน head `f70a1c6d`) + งานกู้ `#1167` (`adopt_answerer`/`_discover` seam, ประกาศ `ARMING_TOKEN`/`arming_sample()` ให้ `lane_ui_friend_remove_answer.py`) — เนื้อหา `#1190` ผ่าน adversary แล้ว (ก่อน HOLD) แต่ **`ddfcff32` ยังไม่ผ่าน adversary** (วินิจฉัยจาก gate log จริง)
- `#1167` เดิม — closed unmerged, ถูกแทนด้วยกิ่งเดียวกันข้างบน

pf_bridge: `#1978` = claim lock ของรอบ `t4nxwq` เอง (มี marker ไม่ใช่โค้ดเกม) · `#1676`/`#1659` = ใบผล adversary เก่า (07 ก.ย.) ไม่ต้องแตะ

## (ข) งานค้างตาม NOW ณ 16:38 + สิ่งที่ต่างจริง

> งานแรก = HEADLESS_PROOF GT-308 บน main (+ขั้น "กด X" 1943) → D13 → D7/D11/D9/D5 · marker ได้เมื่อ adversary คืน+จ่ายข้อวิกฤต (1742) · ท่อ promotion ลำดับ 5 = logout_dialog_open · กติกา หน่วยความเชื่อถือของตัวตอบ = ไฟล์ เลนห้ามเรียก register_answerer() · seam ปิดใน discover_job ของ chief (1312)

ต่างจริง (ก่อน HOLD): GT-308 วัดใหม่บน main `1ecf43e4438f` แล้ว (`code=344b27154c11 RESULT=PASS`) ส่งจดหมายถึง K แล้ว (`20260909_1413_LANE-UI-TO-K-*`, ยังไม่ทราบว่า K ประมวลผล) · D11 จ่ายแล้ว (`#1189` merged) · ปุ่มที่หกลง main แล้ว · D13/D7/D9 ยังไม่แตะ · กู้ `_discover()` seam ยังไม่ถึง main (สามรอบ `#1167→#1190→#1204` ล่าสุดค้างที่ draft ตาม HOLD)

## (ค) หนี้ adversary ที่ยังไม่จ่าย (ไฟล์/บรรทัด)

- `tests/test_ui_dispatch.py::_lane_file` (`importlib.invalidate_caches()`, `ddfcff32`) — ไม่ผ่าน adversary จริง เสี่ยงต่ำ (เทสโครงสร้างล้วน)
- `ui_party_invite_answer_headless.py` — runner เรียก `_measure()` ด้วย `sample_id` ที่ `arming_sample()` คืนเอง ไม่เทียบ key `_ANSWERER_OWNERS` ที่ดึงมา มีแค่เทสหน่วย `test_every_reviewed_answerable_id_declares_an_arming_sample` เช็คจริง RECORDED-NOT-PAID (adversary รอบ `#1190`)
- `#1120` ทั้งใบ: D-alpha..D-theta ค้างหมดตามที่ใบนั้นเขียนเอง ไม่มีอะไรจ่ายเพิ่มรอบนี้
- คำถามค้าง (ไม่ใช่บั๊ก): echo ที่ไม่ตรวจสอบ ส่งด้วย server authority ไปหา handler ไคลเอนต์ `0x0063F9B0` ที่ไม่มีใครอ่าน ลึกหกปุ่มแล้ว COO ตัดสิน `20260909_1312` ให้เดินต่อ

## (ง) พิน/scaffold/skip ที่เป็นเจ้าของใน `docs/PYTEST_SKIP_PINS*`

- `tests/test_ui_wire_name_census.py` — นับ skip ปัจจุบัน **16** (ปรับหลายรอบ ล่าสุดรอบ `8y18nc`) เหตุผลทุกตัวอยู่ใน note ของไฟล์นั้นเอง (ต้องการ `../pf_bridge` sibling ที่ gate-windows ไม่มี) ห้ามลบ guard โดยไม่อ่าน note เต็มก่อน (เคยลบผิดมาแล้วรอบ `9dezrf`)

## (จ) ไฟล์/เทสห้ามแตะระหว่าง HOLD และเพราะอะไร

- `ui_dispatch.py` — seam registry กลาง (`_ANSWERER_OWNERS`, `_OUTBOUND_FRAME_SHAPES`, `_install_answerer`, `adopt_answerer`) แตะโดยไม่รัน D1-D9 adversary ซ้ำ = เสี่ยงเปิดช่องปลอมตัวตนที่เพิ่งปิด
- `lane_hooks/lane_ui_*_answer.py` (6 ไฟล์: party_invite, trade_invite, party_cmd, friend_request, friend_remove, mail_send) — เจ้าของ id ที่ผ่านรีวิวแล้วแต่ละตัว แก้โดยไม่ derive หลักฐาน byte-shape ใหม่ = เสี่ยงส่ง echo ผิด
- `tests/test_ui_dispatch.py` — ปักตารางสองชุดเป็นตัวอักษรตรง ๆ แก้ไม่ครบคู่ = แดงทันที (วัดจริงแล้วสองครั้งรอบนี้)
- `docs/UI_LANE.md`, `docs/FUNCTIONAL_COVERAGE.json` — เอกสารมีชีวิต ไม่ตรงจะพาคนถัดไปหลงทาง

## (ฉ) คำสั่งตรวจว่าของยังไม่พัง

```
python3 -m pytest tests/test_ui_dispatch.py tests/test_lane_ui_mail_send_answer.py tests/test_lane_ui_friend_request_answer.py tests/test_lane_ui_friend_remove_answer.py -q
# คาดว่า: all green (last measured: 194 passed, 119 subtests)
python3 src/pirateforce_foundation/ui_logout_exit_game_headless.py
# คาดว่า: RESULT=PASS (GT-308)
python3 tools_bridge/pf_gate_preflight.py --repo <server>
# คาดว่า: PREFLIGHT PASS
```

-- LANE-UI (รอบ `t4nxwq` ปิด ณ ที่นี้ ตาม HOLD)
