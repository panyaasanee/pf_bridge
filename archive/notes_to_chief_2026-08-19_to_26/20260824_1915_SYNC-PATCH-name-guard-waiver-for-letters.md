# แจ้ง chief · 2026-08-24 19:12 (+07:00) — แพตช์ pf_git_sync.ps1: ยกเว้น name guard ให้จดหมาย

**ผู้เขียน:** ผู้ช่วย (cloud) · **สถานะ:** 🟢 **ทำเสร็จและพิสูจน์แล้ว — ไม่ต้องเปิดใบ**
**คำสั่ง:** คุณ Panya เคาะ 2026-08-24 ~19:0x ("ช่วยแก้ให้หน่อย")

## อาการ

`notes_to_chief/20260824_1222_BETTER-PLAN-use-the-29-capture-validated-messages-not-static-only.md`
ถูก sync ปฏิเสธ **81 รอบติดต่อกัน** ด้วยเหตุ `name looks proprietary`
เพราะชื่อไฟล์มีสตริง `capture` ซึ่งอยู่ใน `$BAD_NAME_PARTS`
⇒ จดหมายฉบับนี้ **ไม่เคยเดินทางถึง chief เลย** (เนื้อหาไม่สูญ — ฉบับแก้ 1244 CORRECTION ผ่านไปแล้ว)

เปลี่ยนชื่อไฟล์แก้ไม่ได้: rename = delete + add และ sync ปฏิเสธทุก commit ที่มี deletion

## ต้นเหตุ

`$BAD_NAME_PARTS` คือการ **เดาเนื้อหาจากชื่อไฟล์** จึงยิงพลาดกับงานเขียน —
จดหมายชื่อ "...capture-validated..." เป็น *ข้อความที่พูดถึง* capture ไม่ใช่ตัว capture

## สิ่งที่แก้

`pf_git_sync.ps1` (37,278 -> 38,518 B · CRLF/ASCII เดิม · สำรองไว้ที่
`agent_kit/pf_git_sync.ps1.pre_patch3_20260824`)

```
$NAME_GUARD_WAIVER = @('notes_to_chief/|.md')
```

ยกเว้น **เฉพาะด่านชื่อ** เท่านั้น · ด่านนามสกุล (`$BAD_EXTENSIONS`) และด่านขนาด 2 MB
**ยังใช้กับ path ที่ได้รับการยกเว้นครบทุกข้อ** · path นอกลิสต์ยังเจอด่านเต็มเหมือนเดิม

## หลักฐานว่าใช้ได้ (รอบ 19:12:02)

```
[4]  name guard waived - text letter, not a binary : notes_to_chief/20260824_1222_BETTER-PLAN-...md
[4]  candidates=2  deletions=0  refusals=0
[4]  committed 2 path(s)
[4]  pushed 1 commit(s)
```

รอบ 19:07:04 ก่อนแพตช์: `refusals=1` · `candidates after the guard: 0` · `nothing to push`

## G3 — ใครใช้กลไกนี้อีก

ด่านนี้กันของสามอย่าง: `GameClient*.bin` · คลัง capture · DB canonical
ทั้งสามถูกด่านนามสกุล (`.bin/.sqlite3/.db/.pcap/.exe/.dll`) จับอยู่แล้วอีกชั้น
การยกเว้นครั้งนี้จำกัดที่ `.md` ในโฟลเดอร์จดหมายเท่านั้น จึงไม่เปิดทางให้ทั้งสามอย่างนั้น

## 🟡 กับดักที่ยังเหลือ (ยังไม่แก้ — รอคุณ Panya เคาะ)

อีก 4 ไฟล์ที่ชื่อจะติดด่านเดียวกันถ้าถูกแก้ไข (ตอนนี้ยังไม่เคยติด — ตรวจ sync.log ทั้งไฟล์แล้ว
ด่านชื่อเคยปฏิเสธของอยู่ชิ้นเดียวคือจดหมายข้างบน):

```
external/pf_validate_capture_fields.py
staged/1027_gt047_capture_validate_baseline.ps1
staged/gt047_patch_run_20260824_1438/pf_validate_capture_fields.py
staged/re059_extract_capture.py
```

ทั้งสี่เป็น **เครื่องมือที่ตรวจ capture ไม่ใช่ capture** — เป็นกรณีเดียวกันเป๊ะ
แต่เป็นไฟล์โค้ด ไม่ใช่จดหมาย ผู้ช่วยจึง **ไม่ขยายขอบเขตเอง** ตามกติกา G8
ถ้าคุณ Panya เคาะ เพิ่มบรรทัดเดียวใน `$NAME_GUARD_WAIVER`

## G2 — ใคร commit

sync commit ให้เองรอบ 19:12:02 (`pf_git_sync.ps1` อยู่ใน `$SHARED_TRACKED`) · ไม่มีใครต้องทำอะไรเพิ่ม
