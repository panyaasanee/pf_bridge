# RE-303 ARTIFACT — ซอร์ส probe ทั้งเจ็ดตัวที่ใช้เดินห่วงโซ่ (อยู่ในรีโปแล้ว ไม่ต้อง `git add`)

- คู่กับจดหมายผล `notes_to_chief/20260907_2150_RE-303-RESULT-teleportcheck-0x4477-opens-confirm-22-ok-echoes-marker.md`
- ผู้ทำ: RE runner บนเครื่องสะพาน · รอบ `RE-RUNNER-20260907_2137-OWNER-ORDERED-NO-CAP` · วาง 2026-09-07T21:55+07:00
- เจ้าของใบ/ผู้บริโภคผล: **LANE-A (WORLD)**

## ที่อยู่: `pf_bridge/notes_to_chief/reference_re303_probes/`

เลนนี้พาไฟล์ใหม่ขึ้น main เองในรอบ sync ถัดไป (คำเคาะ Panya 2026-09-07 21:2x): `.gitignore` บรรทัด 55 `!/notes_to_chief/**` + `$NAME_GUARD_WAIVER 'notes_to_chief/|.py'` (บรรทัด 132) + `$ALLOWLIST` (บรรทัด 165) ⇒ **ไม่ต้อง `git add` ไม่ต้องแตะ `.gitignore`**

| ไฟล์ | ไบต์ | sha256 |
|---|---|---|
| `re303_disasm_probe.py` | 1,251 | `01c642b70eb3fb8930cf2c475c04f51a5bac076de967fb5eaa44e707d89bd203` |
| `re303_xref.py` | 1,220 | `15f3aabe0b4842bba0a8fdef9de4bfd93f7cee4e1a52cd7c2048a8813fa5e2ab` |
| `re303_enclosing_fn.py` | 1,344 | `41aaf100cf27cf60a6ea0e8790c907be09b2c220d902de23b6644ad9d9d5d829` |
| `re303_string_multi_encoding_search.py` | 1,111 | `5346fca5184d10df8520bea6b2740a6d9658574fbff96a3e23df38ba64363fd0` |
| `re303_strings_at_va.py` | 741 | `87b0fe2da64f1131986c6cc02542ac5055fb0d964c869b09ec31a789d7203afa` |
| `re303_call_args.py` | 1,037 | `92c371ff6e9071cef932900a4cd5898ecb6924200de5ff5ae12409a6c5415c07` |
| `re303_immediate_scan.py` | 1,038 | `1f607abff024da03ea0ba9bcca0127befe225502994de1ac470f11a1f4b9e80f` |

(สามตัวแรกเป็นตัวเดียวกับที่รอบ `RE-293`/`RE-296` ใช้ วางซ้ำไว้ให้ครบชุดของใบนี้ sha ตรงกัน — `re303_disasm_probe.py` = `re293_item2_disasm_probe.py`, `re303_xref.py` = `re293_item2_xref.py`, `re303_strings_at_va.py` = `re293_item2_strings.py`)

## PKG_ENV (ตาม `NOW.md` `1941` ห้าม pip กลางรอบ)

```
python >= 3.10 · capstone >= 5.0.7 · pefile >= 2024.8.26
```

## คำสั่งที่ผลิตข้อสรุปแต่ละข้อในจดหมายผล

```
# ข้อ 2 - ผลลบเรื่อง string ไทย (3 encoding x ทุก section)
python3 re303_string_multi_encoding_search.py <GameClient>/GameClient.local.bin "รายงานกัปตัน" "กัปตัน" "Common_Confirm" "UI_CONFIRM"

# ข้อ 3.1/3.2 - ตัวเปิดหน้าต่าง และ mov edi,0x16
python3 re303_disasm_probe.py <GameClient>/GameClient.local.bin 0x005AB5F0:0x005AB830:OPENER 0x005F2190:0x005F23E0:HANDLER

# ข้อ 3.1 - ตัวเชื่อม UI_CONFIRM -> UI_MESSAGE
python3 re303_disasm_probe.py <GameClient>/GameClient.local.bin 0x00430450:0x004304C0:CONFIRM_TEXT

# ข้อ 3.3 - พูล/vtable ที่ยืนยันคลาส
python3 re303_disasm_probe.py <GameClient>/GameClient.local.bin 0x0044B980:0x0044BA80:POOL 0x0044BFA0:0x0044BFE0:OKCB
python3 re303_xref.py <GameClient>/GameClient.local.bin 0x01030838

# nonclaim 4 - สำมะโนผู้เรียกตัวเปิดหน้าต่างทั้งสองชั้น
python3 re303_call_args.py <GameClient>/GameClient.local.bin 0x005AB5F0 0x50
python3 re303_call_args.py <GameClient>/GameClient.local.bin 0x005AB830 0x30

# nonclaim 9 - ยืนยันว่า 22 ไม่เคยเข้ารหัสเป็น push
python3 re303_immediate_scan.py <GameClient>/GameClient.local.bin 22 push

# อ่านสตริงที่ VA ใด ๆ (ชื่อตาราง/คอลัมน์ในจดหมายผล)
python3 re303_strings_at_va.py <GameClient>/GameClient.local.bin 0xF15FAC 0xF0C50C 0xF0C59C 0xF0C3C4 0xF0C4A8 0xF0C48C 0xF0C220 0xF0C200
```

## nonclaims

1. สคริปต์ทั้งเจ็ด **อ่านอย่างเดียว** — ไม่มีการเขียนไฟล์ ไม่มี `subprocess`/`shutil`/`os.remove` ไม่มีเครือข่าย ไม่มี path ฝังตายของเครื่องใคร (รับ path ทาง `sys.argv`)
2. `re303_immediate_scan.py` ใช้การไล่ดิสแอสเซมเบิลเชิงเส้น — ในจดหมายผลใช้เป็น**ตัวช่วยค้นเท่านั้น ไม่ใช้เป็นหลักฐานผลลบ** (ระบุไว้ใน nonclaim 9 ของจดหมายผล)
3. ไม่ได้แก้ `.gitignore` ไม่ได้รัน `git` ที่เขียนอะไร ไม่ได้ `git mv` ไม่ได้ลบไฟล์ใด
