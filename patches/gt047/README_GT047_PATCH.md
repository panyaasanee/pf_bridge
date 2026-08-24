# GT-047 จ็อบ 0 — แพตช์การ์ด `field_offset` ของ `pf_validate_capture_fields.py` (chief R144 · 2026-08-24 +07:00)

**ปลายทาง:** แทนที่ `pf_bridge\external\pf_validate_capture_fields.py` บนเครื่องสะพาน (ไฟล์เดิมไม่อยู่ใน VCS)
**ที่มา:** source เดิมส่งเข้ามาทางจดหมาย `notes_to_chief/20260824_0916_GT047-validator-source.py.md`
(sha256 LF `0166337CBC8E9E561D9D3CD5F02364F4ED43C49070644D5423387E87B793D8C8` · 47,884 bytes — ตรวจตรงแล้ว)

## sha pins (LF)

| ไฟล์ | sha256 | bytes |
|---|---|---|
| `pf_validate_capture_fields.py` (ฉบับแพตช์) | `cafa5f69401eaf152f7ae4e646ce76eb3016c3d6b71e76c494819a029877011b` | 58,656 |
| `verify_gt047_guard_patch.py` | `3f7a153835152b76d9e885bde6676c65ca395a4724c14f1a1a7da63d93c3a95f` | 4,849 |

## อะไรเปลี่ยน (แพตช์ล้วน — โค้ดเดิมไม่ถูกแตะแม้บรรทัดเดียว มีแต่เพิ่ม)

1. **`validate_field_offset_mirror(field_rows, static_open)`** (ใหม่) — เรียกเป็นบรรทัดสุดท้ายของ `build_schemas()` ก่อน return:
   - message ที่ closed (ไม่ static-open) ทุกใบ: order set ของ W ต้องเท่า R
   - ทุกคู่ (message, order): `field_offset` `tag` `span_start` `span_end` ต้องตรง **byte-for-byte** —
     ยกเว้น 40 คู่ใน `VA_DEPENDENT_MIRROR_PAIRS` (pin ในโค้ด) ที่ยอมให้ตรงหลัง normalize VA (`0x??????` 6–8 หลัก → `VA`)
   - `len` และ `span_sha256` ต้องตรง byte-for-byte เสมอ ทุกคู่
   - pin census: static-open messages = **181** · closed pairs = **859** — เปลี่ยนเมื่อไหร่ = แดง
     (กัน mutation ชนิด `+0x14` → `UNKNOWN(+0x99)` ที่หนีการ์ดด้วยการพา message เข้า skip set)
2. **self-test ใหม่ 6 เคสท้าย `validate_schema_mutation_regressions()`** — ต้องแดงทุกเคส มิฉะนั้น validator ตายเอง:
   W-leg `+0x14→+0x99` (เคสจ็อบ 3 ของ tester เป๊ะ) · R-leg `+0x20→+0x77` · flip `UNKNOWN(+0x99)` ·
   one-leg VA edit (`ReliveVital:W:1`) · one-leg `span_sha256` tamper · **membership swap** (flip `Activity_BasicVital` ออก + `Attribute` เข้า static_open แบบรักษา count) — ทุกเคส assert ค่า fixture เดิมก่อน กัน drift เงียบ
3. **pin membership digest**: `EXPECTED_STATIC_OPEN_MEMBERSHIP_SHA256` = sha256 ของรายชื่อ static-open ทั้ง 181 ใบเรียงแล้ว —
   count pin อย่างเดียวกันการสลับสมาชิกแบบรักษาจำนวนไม่ได้ (adversary รอบสองสาธิตด้วยการแก้ 3 แถว) · digest กันได้

## เหตุที่การ์ดยึดอินเวเรียนต์นี้ (วัดจริง ไม่ใช่เดา)

วัดบน `external/PF_SERIALIZER_FIELDS.tsv` (sha256 `99282bdf3f492eaebdbab4918aecc0e37bf8efb42b904b18e1ba306767b5c123`) ทั้ง 6,931 แถว:
mirror W↔R สมบูรณ์ 859/859 บนตารางบริสุทธิ์ · 40 คู่ที่ raw ต่างกันมาจาก VA ฝังตามทิศเท่านั้น
⇒ การ์ดอธิบายทั้งเคสผ่าน (ตารางจริง) และเคสตก (mutation หนึ่งขา) — วินัย RE-056

## วิธี apply + ตรวจ (ฝั่งสะพาน · Windows)

1. ตรวจ sha256 ของสองไฟล์ในโฟลเดอร์นี้ตรงกับตารางข้างบน
2. สำรองไฟล์เดิม แล้วสำเนา `pf_validate_capture_fields.py` ทับตัวใน `pf_bridge\external\`
3. `py -3 verify_gt047_guard_patch.py --external <พาธ external>` → ต้องจบ `ALL 8 CHECKS PASS` exit 0
   🔴 **quote บรรทัดแรก (`validator sha256=…`) ลงจดหมายผลเสมอ** — ผูกผลกับไฟล์ที่รันจริง
4. rerun GT-047 จ็อบ 3: mutation `TargetPosVital:W:1 +0x14→+0x99` บนสำเนา TSV → validator ต้อง**แดง** (exit ไม่ใช่ 0) — เก็บ log ก่อน/หลัง
5. rerun จ็อบ 1–2 ตามใบเดิมใน `GAME_TEST_QUEUE.md`

## nonclaims

- ไม่ครอบ mutation สมมาตรที่แก้ทั้งขา W และ R เหมือนกัน
- ไม่ครอบการแก้ VA ที่ฝังในสตริงของ 40 คู่ pinned (ชั้นนั้นพึ่ง `span_sha256` mirror + GT-054 verify กับอิมเมจ)
- ไม่ครอบ `gate_condition` / `file_off_claim` (สอง legs ต่างกันเกิน mirror โดยชอบ · validator ไม่อ่านสองคอลัมน์นี้)
- เขียวบน cloud = ชั้น schema เท่านั้น (ไม่มี capture บน cloud) · จ็อบ 1–3 ตัวจริงต้องรันบนสะพาน
- การ์ดที่แดงบน corruption ไม่ยกสถานะอะไรเป็น `VALIDATED` — F1/F2/F3 ของใบ GT-047 ติดทุกตัวเลขเหมือนเดิม
