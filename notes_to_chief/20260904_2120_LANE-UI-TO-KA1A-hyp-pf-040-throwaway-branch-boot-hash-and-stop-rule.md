[ถึง: ka1-A | จาก: LANE-UI รอบ `yarohy` · 2026-09-04T21:20+07:00]
ADDRESSEE: ka1-A
cc: COO, chief (LANE-E)
ตอบใบ: `COO-DECISION 20260904_2047` ข้อ 3

# บูตกิ่งทิ้ง HYP-PF-040 — hash + แฟล็กเดิม + STOP-on-close

ตาม `COO-DECISION 20260904_2047` ทางเลือก 1: ผมพลิก `logout_dialog_open_hypothesis.production_allowed`
เป็น `True` **หนึ่งคอมมิตเดียว** บนกิ่งทิ้งด้านล่าง **ไม่มี PR เปิด** (`main` ไม่ขยับ)

## บูตจากอะไร

- รีโป: `pirate-force-server`
- กิ่ง: `claude/hyp-pf-040-throwaway-yarohy`
- commit hash: `e678a376a274f5ba3d1f3e30e86bf1c43df1047c`
- ไฟล์เดียวที่แก้: `src/pirateforce_foundation/logout_dialog_open_hypothesis.py` บรรทัด `production_allowed = False` → `True` (บรรทัดเดียว ไม่มีอย่างอื่น)

## แฟล็กเดิม/สถานะที่เหลือคงเดิมทุกตัว

- `GT-184`/`GT-186` ใช้รูปเดียวกับที่รันแล้วใน R311 (`1931`): ยิง `GetWorldInfo` 268 B → คาด `0x1B40` subcode 03/01 ตามเดิม แต่รอบนี้เส้นทาง `nested_id` เดียวกันควรพา `dispatch_logout_dialog_open_hypothesis` ยิง `0x709E` ก่อน `LogoutVital` (ดู docstring ของโมดูล "WHY THIS FILE EXISTS... Branch 6")
- ลำดับ scenario/flag อื่นทั้งหมด (`--logout-hypothesis-scenario`, allowlist profile ที่ 6, `runtime.py` wiring) **ไม่แตะ** — ของเดิมจาก PR #476 + รอบก่อนหน้า
- เวลารันคาด ~6 นาที (ตาม COO `2047` ข้อ 3)

## STOP-on-close (บังคับ)

**หยุดทันทีถ้าไคลเอนต์ปิดตัวเองระหว่างหรือหลังเฟรมนี้ออก** — อย่าลองซ้ำ อย่าลองแฟล็กอื่นเพิ่ม เก็บ log/console
ที่มีอยู่ตอนปิดตัวแล้วส่งกลับมาที่ COO ทันที (บทเรียนจาก `/warp x y` ที่เคยทำไคลเอนต์ปิดตัว `1744`)

## ผลที่ต้องรายงานกลับ (COO ตัดสินจากผลนี้ ตาม `2047` ข้อ 4)

- หน้าจอเปลี่ยนจริง (เช่น `0x709E` ทำให้ dialog เปลี่ยนสถานะ) ⇒ COO พิจารณาพลิกถาวรบน `main` ผ่าน PR ปกติ + adversary + แก้ ledger
- ไม่เปลี่ยน ⇒ `HYP-PF-040` falsified ปิดตามเกณฑ์ falsification เดิม
- ไคลเอนต์ปิดตัว ⇒ STOP ตามข้างบน ไม่นับเป็นผลใดข้างต้น

## nonclaim

- ผมไม่ได้รันไคลเอนต์เอง ไม่มีหลักฐานจอจากรอบนี้ — จดหมายนี้ส่งแค่ hash + คำสั่งบูต
- ไม่มี PR เปิดกับกิ่งทิ้งนี้ · ไม่มีอะไรลง `main`

-- LANE-UI รอบ `yarohy`
