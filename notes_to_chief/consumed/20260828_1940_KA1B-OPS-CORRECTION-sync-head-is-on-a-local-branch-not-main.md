[ถึง: Panya, chief, COO, สาย A/B/GM | จาก: ผู้ช่วยเซสชัน attended "กะ3-A" (บัญชี [กะ3]) | 2026-08-28T19:40+07:00]

# OPS แก้ไข — สะพานยัง **ไม่** ออกจริง · เหตุคือ HEAD ของ `pf_bridge` ไม่ได้อยู่บน `main`

🔴 **ใบก่อนหน้าของผม `20260828_1921_KA1B-OPS-bridge-sync-unhalted-*` พูดถูกครึ่งเดียว — แก้ตรงนี้**
รอบ sync กลับมาเดินจริง (HALT ถูกปลด) แต่ **push ยังล้มทุกรอบ** ⇒ จดหมายและหลักฐานฝั่งเครื่อง
**ยังไม่ออกไป GitHub เลยตั้งแต่ ~15:2x** ใครอ่านจากคลาวด์จะไม่เห็นใบนี้จนกว่าจะแก้

## ① อาการที่วัดได้ (รอบ 19:21 / 19:26 / 19:31 เหมือนกันทั้งสามรอบ)
```
[3]  ahead=11 behind=25   ->  ahead=12 behind=0  ->  ahead=13 behind=6
[4]  committed 2 path(s)  /  committed 1 path(s) /  nothing new
[4]  push rejected as non-fast-forward - the chief got there first; rebasing once
[4]  SHOUT push failed again after a clean rebase:
     ! [rejected] main -> main (non-fast-forward)
     hint: a pushed branch tip is behind its remote counterpart
[7]  heartbeat  PUSH_FAILED_AFTER_REBASE  push twice
```
ข้อความ **"behind its remote counterpart"** ไม่ใช่อาการของ "ชนกับ chief" — มันแปลว่า ref ที่ถูก push ตามหลัง remote

## ② สาเหตุจริง (อ่านจาก `.git/` ตรง ๆ ไม่ได้รัน git — กฎข้อ 6)
```
.git/HEAD                     -> ref: refs/heads/local/a-smoke-20260828-bridge-r2
refs/heads/local/a-smoke-...  =  86eb8253fa5539817033aa65d5e1dd74c3827749   <- คอมมิตจริงอยู่ตรงนี้
refs/remotes/origin/main      =  0ac38d27162ccf3ae7671bdd545dd3110d398e4c
packed-refs refs/heads/main   =  45370816fec6e69323dbd032d99a641d4b0bdfa3   <- ค้างเก่า
```
**worktree ของ `pf_bridge` ถูกทิ้งไว้บน branch `local/a-smoke-20260828-bridge-r2`** (ของรอบ LANE-A local smoke r2
ที่ปล่อย `LOCK_GIT` เวลา 15:21 ว่า "bridge smoke r2 pushed")
⇒ `pf_git_sync` commit ลง branch นั้น · rebase branch นั้นสำเร็จ · แต่ `git push origin main` ยิงจาก
`refs/heads/main` ที่ยังค้างที่ `4537081` ซึ่งตามหลัง `origin/main` `0ac38d2` ⇒ ถูกปฏิเสธทุกครั้ง
`reflog` ยืนยัน: `rebase (finish): returning to refs/heads/local/a...` — **ไม่เคยกลับไป main**

⇒ ตอนนี้มี **13 คอมมิต** (จดหมาย/หลักฐานตั้งแต่ ~15:2x รวมใบ 1921 ของผมและใบนี้) **ค้างบน branch local ไม่ใช่ main**
มีอีก branch ค้างชื่อ `local/gm-smoke-20260828-bridge-r2` (`dc6140e`) — ยังไม่ได้ตรวจว่าเนื้อเข้า main ครบหรือยัง
`Pirate Force ServerProject` ก็อยู่บน `local/a-smoke-20260828-r2` เหมือนกัน (main local = origin/main = `336857cd`, fetch ล่าสุด 17:24)

## ③ สิ่งที่ต้องทำ — ต้องใช้มือคน (ผมห้ามรัน git บนโฟลเดอร์ที่ mount)
เจ้าของรันสามบรรทัดนี้ใน `pf_bridge` (Git Bash / PowerShell):
```
git -C "C:\Users\Panya\Desktop\Pirate Force\pf_bridge" checkout main
git -C "C:\Users\Panya\Desktop\Pirate Force\pf_bridge" merge --ff-only local/a-smoke-20260828-bridge-r2
git -C "C:\Users\Panya\Desktop\Pirate Force\pf_bridge" push origin main
```
ถ้า `merge --ff-only` ปฏิเสธ = ไม่ใช่เส้นตรง **ห้ามฝืน** ให้หยุดแล้วบอก chief ตัดสิน
หลังจากนั้นปล่อย `pf_git_sync` เดินเอง — ต้องเห็น `[4] pushed` ในรอบถัดไป

## ④ ที่เจอเพิ่มระหว่างตรวจ
`[4] refusals=25` ทุกรอบ = ไฟล์ `evidence_screens/*` **25 ใบ ขนาด > 2 MB ถูก guard ตัดออกจากการ commit ถาวร**
รวมชุด `REF_original_server_combat_1..5`, `GT078_*_FULLRES`, `GT084R2_*`, `GT101_error23065_*`,
`GT045v3r2_1129_*` (6.6 MB / 6.5 MB), `M1P_ingame_*`, `REF_ORIGINAL_SERVER_PortRoyal_*`
⇒ **ภาพอ้างอิงเซิร์ฟเวอร์เดิมชุดคอมแบตไม่เคยออกจากเครื่องเลย** ใครบนคลาวด์ที่อ้างถึงมันอยู่ กำลังอ้างของที่ตัวเองไม่เคยเห็น
ทางแก้ที่เสนอ (รอเจ้าของเคาะ): แปลงเป็น `.webp` คุณภาพ ~80 หรือย่อด้านยาว 1600px แล้ว commit ตัวย่อแทน

## ⑤ nonclaims
- ไม่อ้างว่า 13 คอมมิตนั้นมีอะไรบ้าง — อ่านจาก ref/reflog เท่านั้น ไม่ได้ `git log`
- ไม่อ้างว่า branch `local/gm-smoke-*` ไม่มีของใหม่ค้าง — ยังไม่ได้ตรวจ
- ไม่อ้างว่า `merge --ff-only` จะผ่าน — ถ้า `4537081` ไม่ใช่ ancestor ของ `86eb825` มันจะปฏิเสธ ซึ่งถูกแล้ว
- ไม่ได้รัน git · ไม่ได้แตะ `src/` · ไม่ได้ commit · ไม่ได้แตะเกม/DB/คิว

— กะ3-A
