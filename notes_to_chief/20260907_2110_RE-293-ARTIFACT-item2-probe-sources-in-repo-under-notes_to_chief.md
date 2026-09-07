# RE-293 ARTIFACT — ซอร์สของ probe ทั้งสี่ตัวอยู่ในรีโปแล้ว (ไม่ต้อง `git add` ไม่ต้องแตะ `.gitignore`)

- ใบ: `RE-293 PLAYER-STR-DERIVATION-SOURCE-001` (ข้อ 2 · ปิดแล้ว)
- คู่กับจดหมายผล `notes_to_chief/20260907_2043_RE-293-RESULT-item2-no-addition-anywhere-and-STANDARD_BUFF-is-the-per-level-stat-table.md`
- ผู้ทำ: RE runner บนเครื่องสะพาน · วางของ 2026-09-07T21:10+07:00
- เจ้าของใบ/ผู้บริโภคผล: **LANE-CS (CLASS/SKILL)**

## 🔴 คำแก้ของผู้ทำเอง (ผิดในจดหมาย `2043` — แก้ตรงนี้ ไม่ลบของเดิม)

จดหมาย `2043` เขียนว่า *"สคริปต์ read-only วางไว้ที่ `pf_bridge\staged\` (ต้องมีคนบนเครื่องสะพาน `git add`)"*
**ประโยคนั้นถูกครึ่งเดียวและทำให้เข้าใจผิด** — เจ้าของชี้ทางที่ถูกให้แล้ว วัดซ้ำแล้วยืนยันตามนี้:

| | `.gitignore` | `$ALLOWLIST` ใน `pf_git_sync.ps1` | ไฟล์ใหม่เดินทางเองไหม |
|---|---|---|---|
| `staged/**` | เปิด (`!/staged/**` บรรทัด 61) | **ไม่มี** | **ไม่** — ต้องมีคน `git add` ก่อน |
| `notes_to_chief/**` | เปิด (`!/notes_to_chief/**` บรรทัด 55) | **มี** (บรรทัด 165) | **ใช่ รอบ sync ถัดไป** |

และ `$NAME_GUARD_WAIVER` (บรรทัด 130-135) มี `'notes_to_chief/|.py'` อยู่แล้ว ⇒ **ไฟล์ `.py` ใต้ `notes_to_chief/` ผ่านทั้ง `.gitignore` ทั้ง name guard ทั้ง ALLOWLIST**
⇒ **นี่คือเลนเดียวที่ของใหม่ออกไปได้โดยไม่ต้องแตะ `.gitignore` เลย** · แบบอย่างที่ทำมาก่อน: `notes_to_chief/reference_codex_attr/` (อ้างใน `.gitignore` บรรทัด 205-206)

🟠 ข้อสังเกตถึง LANE-K/COO (ไม่ใช่คำตัดสินของผู้ทำ): `$NAME_GUARD_WAIVER` มี `'staged/|.py'` ด้วย แต่ `staged` **ไม่อยู่ใน `$ALLOWLIST`** ⇒ waiver ตัวนั้นไม่มีทางทำงานกับไฟล์ใหม่ได้เลย เป็นกับดักที่อ่านแล้วชวนให้เชื่อว่า `staged/` ส่งของออกได้ (ผู้ทำเชื่อไปแล้วหนึ่งครั้งในรอบนี้)

## ของที่วางแล้ว (ไฟล์ `.py` จริง ไม่ใช่ซอร์สในบล็อกโค้ด ⇒ ไม่มีความเสี่ยงคัดลอกตกหล่น)

โฟลเดอร์: `pf_bridge/notes_to_chief/reference_re293_re296_probes/`

| ไฟล์ | ไบต์ | sha256 |
|---|---|---|
| `re293_item2_disasm_probe.py` | 1,251 | `01c642b70eb3fb8930cf2c475c04f51a5bac076de967fb5eaa44e707d89bd203` |
| `re293_item2_xref.py` | 1,220 | `15f3aabe0b4842bba0a8fdef9de4bfd93f7cee4e1a52cd7c2048a8813fa5e2ab` |
| `re293_item2_attr82_writers.py` | 1,308 | `aeb252b3d797f2282372de5a5cb4d0e0d9a8dc65f5d3af7d6242cb73e49715ed` |
| `re293_item2_strings.py` | 741 | `87b0fe2da64f1131986c6cc02542ac5055fb0d964c869b09ec31a789d7203afa` |

**ตรวจแล้วว่าเท่ากับต้นฉบับใน `staged/` bit ต่อ bit ทั้งสี่ไฟล์** (เทียบ sha256 หลังคัดลอก · 4/4 MATCH) ตามมาตรฐานเดียวกับที่ `RE-289` ทำไว้ (`.gitignore` บรรทัด 126: *"Source is byte-identical to the one in that letter, sha256 eab4ce35…"*)
สำเนาใน `staged/` **ยังอยู่ที่เดิม ไม่ได้ลบ ไม่ได้ `git mv`** (กฎ `0945`) — ถือเป็นสำเนาที่เดินทางไม่ได้ ให้ใช้ชุดใน `notes_to_chief/` เป็นตัวจริง

## PKG_ENV (ตาม `NOW.md` `1941` — ห้าม pip กลางรอบ)

```
python >= 3.10
capstone >= 5.0.7      (ติดตั้งแล้วบน VM ของบริดจ์ ตรวจรอบนี้)
pefile  >= 2024.8.26   (ติดตั้งแล้วบน VM ของบริดจ์ ตรวจรอบนี้)
```

## วิธีรัน (อ่านอย่างเดียวทั้งหมด · รับ path ของอิมเมจทาง argv ไม่มี path ฝังในโค้ด)

```
python3 re293_item2_disasm_probe.py  <GameClient>/GameClient.local.bin 0x00588810:0x00588960:BINDER
python3 re293_item2_xref.py          <GameClient>/GameClient.local.bin 0x00588810
python3 re293_item2_attr82_writers.py <GameClient>/GameClient.local.bin
python3 re293_item2_strings.py       <GameClient>/GameClient.local.bin 0xF14B70 0xF14B94 0xF2C5F0
```

อิมเมจที่ผลในจดหมาย `2043` วัดไว้: `GameClient\GameClient.local.bin` 14,759,424 ไบต์ sha256 `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`

## คำรับรองด้านความปลอดภัยของสคริปต์ (สแกนแล้วทั้งสี่ไฟล์)

- **ไม่มี** การเปิดไฟล์เพื่อเขียน · ไม่มี `.write(` · ไม่มี `os.remove` / `shutil` / `subprocess`
- **ไม่มี** เครือข่าย (`urllib` / `requests` ไม่ปรากฏ)
- **ไม่มี** path ฝังตายของเครื่องใคร (ไม่มี `C:\`, `/home/`, `/sessions/`) — อ่านจาก `sys.argv` ล้วน
- อ่าน `GameClient/` แบบ read-only เท่านั้น · ไม่แตะ `SERVER\` `external\` `gamedata\` หรือคิวใด ๆ

## nonclaims

1. **ไม่ได้อ้างว่าไฟล์เหล่านี้ควรเป็น tool ถาวร** — การตัดสินว่าอะไรอยู่ `tools_bridge/` ถาวรเป็นงาน LANE-K/COO (ดูจดหมาย `*_TO-K-promoting-the-re293-re296-probes-*` ฉบับเดียวกันของรอบนี้)
2. **ไม่ได้แก้ `.gitignore` ไม่ได้รัน `git` ที่เขียนอะไร ไม่ได้ `git mv` ไม่ได้ลบไฟล์ใด**
3. ตัวเลข sha256 ทั้งหมดวัดบนเครื่องสะพานในรอบนี้ ทำซ้ำได้ด้วย `sha256sum`
