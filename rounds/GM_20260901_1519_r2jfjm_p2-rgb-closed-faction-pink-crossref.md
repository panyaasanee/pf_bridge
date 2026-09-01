# LANE-GM round r2jfjm (scheduled, no attended watching) -- 2026-09-01T15:19+07:00

## NOW.md check (บังคับก่อนทุกอย่าง)

อ่าน `NOW.md` แล้ว (ตรวจล่าสุดโดย COO 14:47+07:00, มี 3 ข้อด่วน + คิวต่อท้าย)
รอบนี้ขยับ NOW ข้อไหน: **P-2 ขยับบางส่วน** (คำถาม RGB ปิด แต่ยังไม่ปิดข้อ P-2 ทั้งข้อ) ข้ออื่นไม่ขยับ:

- **P-1**: ไม่ใช่ของสาย GM
- **P-2**: RGB question ที่ `COO-DECISION 1241` สั่งไว้ปิดแล้วรอบนี้ (ดูรายละเอียดล่าง) แต่ NOW.md เอง
  บอกไว้แล้วว่า "โค้ด+เทสฝั่งเซิร์ฟเวอร์เสร็จแล้ว เหลือรอ Panya รัน GT" ไม่ใช่กติกาของ P-2 (P-2 ยังไม่มี
  โค้ดเลย) จึงไม่ใช้กฎ "ไม่ใช่ตัวบล็อกสาย" ข้อนั้น -- P-2 ยังเปิดค้างจริง รอ chief ตอบ CORE-REQUEST-GM-048
  ที่เปิดรอบนี้
- **P-3**: นอกเขต repo ทั้งสอง (native DLL)
- **GM-A**: `GT-192` เปิดแล้ว (chief R288) พร้อมรัน attended รอ Panya -- ไม่ใช่ตัวบล็อกสาย ตามกฎใหม่
- **GM-B**: LANE-DB ถือเต็มแล้ว
- **UI-A/UI-B**: ของ LANE-A

## ก่อนเริ่ม: ยืนยันไฟล์อ้างอิง

`../pf_bridge/VITAL_REGISTRY_FROM_CLIENT_BINARY_20260817.tsv` มีจริง (ตรวจด้วย `ls -la` รอบนี้)

## Part A -- ชะตา PR รอบก่อน (t2qkn3)

`pf_bridge#717` merged=true (2026-09-01T07:29:13Z) · `pirate-force-server#478` merged=true
(2026-09-01T07:37:06Z) -- งานรอบก่อนอยู่บน main แล้ว ไม่ต้อง cherry-pick อะไร

## round-lock

ไม่มี PR `[LANE-GM]` เปิดค้างก่อนเริ่ม (`list_pull_requests(state=open)` ทั้งสอง repo -- ว่างทั้งคู่
สำหรับ `[LANE-GM]`; server repo มี `[LANE-A] #481` และ `[LANE-E] #482` เปิดอยู่ ไม่ใช่ล็อกของสายนี้
ไม่แตะ) เปิด draft PR ยึดล็อกก่อนทำงาน: `pf_bridge#723`, `pirate-force-server#483` (commit เปล่า
"round claim: r2jfjm" ก่อนหน้า)

## Part B -- กล่องจดหมาย

ใบ `ADDRESSEE: LANE-GM` ที่ยังไม่มี `.CONSUMED.txt`: ไม่มี (ตรวจด้วย `grep -l "ADDRESSEE: LANE-GM"`
เทียบคู่ `.CONSUMED.txt` ทีละไฟล์ ครบทุกไฟล์)

แต่พบใบที่ยังไม่บริโภคจริงหนึ่งใบ (ที่มาถึงหลัง `t2qkn3` ปิดรอบ, จ่าหน้า "ถึง: chief, LANE-GM" ไม่ใช้
header `ADDRESSEE:` แบบเดียวกันเป๊ะ แต่เนื้อหาเป็นผลของใบ RE-191 ที่สายนี้เปิดเองรอบ `h6rsgl` --
ผู้เปิดใบบริโภคผล):

`20260901_1439_CODEX-RE191-RESULT-FONTSTYLE63-RGBA.md` -- บริโภคแล้ว วางสตับ + สำเนาไป `consumed/`

## ทำไมได้งานจริงรอบนี้

ใบนี้ตอบคำถาม RGB ที่ `COO-DECISION 20260901_1241` สั่ง chief จัดสรร RE/Codex เวลาให้ปิด (รอบที่สาม
ที่สายนี้ขอ) -- priority-1 ของลำดับงานมีของจริงให้ทำ

## รายละเอียด

**RGB จริงของ fontstyle 61/62/63 (proven, DATA+IMAGE cross-ref):**

| FontStyleID | RGBA | คำบรรยาย |
|---:|---|---|
| 61 | (255,100,100,255) | แดง (fighting) |
| 62 | (255,159,113,255) | ส้ม (normal) |
| 63 | (179,179,179,255) | เทา (candidate: dead) |

ตรงกับเกณฑ์เจ้าของเป๊ะ (ปกติ=ส้ม, สู้=แดง, ตาย=เทา) และ**ไม่มีตัวไหนชมพู** -- ปิดคำถาม RGB ที่ COO
สั่งไว้ได้จริง

**แต่ใบเองเขียนเพดานไว้ชัด**: ไม่พิสูจน์ว่า live actor ผ่าน gate 63 จริงสำหรับ "ตาย" และห้าม hardcode
style ID -- client เลือกจาก identity/relationship/death path เอง (ยืนยันด้วยตาราง
`PF_ATTR_NAME_COLOR_SELECTOR.tsv` ที่มีอยู่แล้ว: เป็นโค้ดฝั่งไคลเอนต์ล้วน ไม่มีฟิลด์ wire ชื่อ
FontStyleID ที่เซิร์ฟเวอร์ส่งตรง ๆ เท่าที่ค้นทั้งสอง repo)

**พบใหม่รอบนี้ (ไม่มีรอบ GM ก่อนหน้าอ้างถึง):** ค้น (อ่านอย่างเดียว นอกเขตเขียนของสายนี้)
`src/pirateforce_foundation/npc_hostile_hypothesis.py:11-30` (GT-032, attended PASS, ไม่ใช่ของสาย
GM) พบกลไกสีที่สอง -- faction/relation comparator (`0x4A1D50`, BasicAttr bit `0x0400` ที่ `+0x68`)
ที่ไคลเอนต์จริงเคยเรนเดอร์เป็น **"pink/red name"** สำหรับ faction pairing ที่วัดได้หนึ่งคู่ (player
faction 1 vs NPC faction 6) -- ตรงกับสิ่งที่เจ้าของสั่งห้ามตรง ๆ (`NOW.md` P-2: "ห้ามชมพู")

เปิด `CORE-REQUEST-GM-048` ถึง chief ถามว่า P-2 ควรผูกกับกลไกไหน (FontStyleID selector หรือ faction
comparator) ก่อนสายไหนเขียนโค้ดสี และถ้าเป็น faction ขอรายชื่อ pairing ที่เคยวัดว่าชมพูเป็น
block-list

## ที่ไม่ทำในรอบนี้ (เจตนา ไม่ใช่ลืม)

- ไม่เขียนโค้ดสีมอนสเตอร์ใด ๆ -- ยังไม่รู้ว่าเป็นกลไกไหน เขียนตอนนี้ = การเดา ขัด `RE-109`
  `BUILD_IMPACT: NONE` เหมือนเดิม
- ไม่แตะ `npc_hostile_hypothesis.py`/`runtime.py`/`app.py`/`pf_login_game_server_v141.py`/
  canonical DB/`scenarios/world_*.json`/`scenarios/combat_*.json` -- อ่านอย่างเดียว นอกเขตเขียนของ
  สายนี้ทั้งหมด

## กฎรอบเปล่า (rule F)

ไม่เข้าเงื่อนไข F -- รอบนี้บริโภคจดหมายจริงหนึ่งใบ + พบข้อเท็จจริงใหม่ + เปิดใบขอใหม่ (ตัวเลือก ข
"ใบ RE/STATIC ที่ตอบได้จากซอร์ส/factpack" อยู่แล้วในความหมายกว้าง: cross-reference จากซอร์สที่มีอยู่
ไม่ใช่ verify-only)

## ผู้เทสจะทำอะไรได้ที่เมื่อวานทำไม่ได้

**ไม่มี** -- รอบนี้ไม่มีการแก้ wire/behavior ใด ๆ เป็นการบริโภคจดหมาย + ค้นข้ามเขต + เปิดใบขอเท่านั้น

## nonclaims

1. ไม่อ้างว่า faction comparator กับ FontStyleID selector เป็นกลไกเดียวกัน -- ตั้งข้อสังเกตให้ chief
   ตัดสิน
2. ไม่อ้างว่า RE-191 ปิด P-2 ทั้งใบ -- ปิดเฉพาะคำถาม RGB ที่ COO สั่งไว้
3. ไม่แตะ `runtime.py`/`app.py`/`pf_login_game_server_v141.py`/canonical DB/
   `scenarios/world_*.json`/`scenarios/combat_*.json`/`npc_hostile_hypothesis.py`
4. ไม่ให้สถานะ GM กับบัญชีนอก `gm_accounts.json` ไม่ประกาศ milestone
5. ไม่ลบประวัติ/จดหมายเดิม -- สตับใหม่เท่านั้น ต้นฉบับสำเนาไว้ที่ `consumed/` ครบ
6. src/scenarios/tests ไม่มีการแก้รอบนี้ (เฉพาะจดหมาย/round notes/docs) -- ไม่เรียก pf-adversary
   ตามบรรทัดฐานรอบ `dgyakk`/`bmedw1`/`kv02mn`/`t2qkn3`

## PR

`pf_bridge#723` / `pirate-force-server#483`

Companion: `pirate-force-server` (branch `claude/upbeat-fermi-r2jfjm`, docs-only change --
`docs/GM_LANE.md` round entry)

PF-AUTOMERGE: v4

— สาย GM รอบ `r2jfjm`
