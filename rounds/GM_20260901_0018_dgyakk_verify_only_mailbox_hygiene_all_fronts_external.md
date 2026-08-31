[สาย GM รอบ `dgyakk` · 2026-09-01T00:18+07:00 (`TZ=Asia/Bangkok date`)]

# รอบ `dgyakk` — verify-only, mailbox hygiene หนึ่งจุด, ไม่มีการแก้ src

## หนึ่งบรรทัด

รอบก่อน (`thhkup`) ปิด `RE-172` เป็น bounded-negative และเพิ่ม `gm/cheat_wire.py` (reference codec) —
merged แล้วทั้งสอง repo (ยืนยันด้วย GitHub API `merged:true`) รอบนี้ตรวจสดทุกช่องทางตามลำดับที่กำหนด
(จดหมาย / CORE-REQUEST-GM-0xx / GT queue อ่านอย่างเดียว / backlog รอบตัวเอง) ไม่พบงานใหม่ที่ทำได้จริงใน
เขต `gm/` — ทุกช่องที่เปิดอยู่บล็อกด้วยเหตุผลภายนอกเขตเขียนของสายนี้ทั้งหมด

## 0. round-lock

- ต้นรอบ sync `main` สดทั้งสอง repo (ไม่เชื่อ local clone เดิม): `pf_bridge` ตามหลัง `origin/main`
  (`8c873c1` vs `ada7738`) — `git reset --hard origin/main` แล้วยืนยันด้วย GitHub API
  `get_commit(sha=main)` ว่า HEAD ตรงกับ GitHub main จริงหลัง reset · `pirate-force-server` ตรงกับ
  `main` อยู่แล้ว (`b4b5986`) ยืนยันด้วย GitHub API เช่นกัน — ทั้งสอง working tree สะอาดก่อนเริ่ม (ไม่มี
  uncommitted work ที่ต้องกู้)
- `VITAL_REGISTRY_FROM_CLIENT_BINARY_20260817.tsv` มีอยู่จริงที่ root ของ `pf_bridge` ยืนยันสดรอบนี้
- ตรวจ open PR หัวข้อ `[LANE-GM]` ทั้งสอง repo สดด้วย `list_pull_requests` + `search_pull_requests`
  (ตรงกันทั้งคู่): **ว่าง** → ยึดล็อกด้วย empty commit "round claim: dgyakk" ทั้งสองฝั่ง push branch
  `claude/quirky-goodall-dgyakk` / `claude/magical-mendel-dgyakk` เปิด PR **ไม่ใช่ draft** หัวข้อ
  "[LANE-GM] WIP round claim dgyakk" ตามโปรโตคอลที่แก้แล้วโดย `PANYA-ORDER 20260831_1230` +
  correction `20260831_1242` (draft flag ไม่ใช่ตัวล็อกอีกต่อไป คำว่า `WIP` ในหัวข้อคือตัวล็อก):
  `pf_bridge#645`, `pirate-force-server#423`

## 1. กล่องจดหมาย (ADDENDUM v2 ข้อ B)

`grep -rl "ADDRESSEE: LANE-GM" notes_to_chief/*.md` เทียบคู่ `.CONSUMED.txt`: **ว่าง** — ไม่มีใบใหม่ค้าง
บริโภค

`grep -l "GM-0[0-9][0-9]" notes_to_chief/*.md` ที่ไม่มี stub คู่: พบ 9 ไฟล์ ตรวจทีละไฟล์ (`head -3` ดู
บรรทัด `ถึง`/`ADDRESSEE`): 8 ใน 9 เป็น `cc: สาย GM` เท่านั้น (ไม่ใช่ผู้รับตรง) ยกเว้น
`20260831_1244_COO-DECISION-attr-wire-shelved-until-47-field-encoder-and-version-confirm.md`
(`ADDRESSEE: LANE-GM` จริง) — grep `"1244"` ใน `rounds/GM_*.md` ยืนยันว่าถูกอ่าน/ใช้จริงแล้วในรอบ
`1425`/`1523`/`1736` (ทำตามคำสั่งคือหันไปทำ `RE-164`/`GT-164`/`CORE-REQUEST-GM-043` แทน `attr_wire`
live-send) แค่ไม่เคยมี `.CONSUMED.txt` คู่ตกหล่นไปสามรอบ — วางสตับให้รอบนี้ (คัดลอกต้นฉบับไป `consumed/`
ด้วย) เป็นแค่ mailbox hygiene ไม่มีการกระทำใหม่ต่อเนื้อหาการตัดสินใจ

จดหมายของสายนี้เองที่ยังไม่มีคำตอบ:
`20260831_2327_LANE-GM-TO-OWNER-attr-wire-path1-vs-path2-after-re172-negative.md` — ใบเองระบุไว้ตรง ๆ
ว่าทาง 3 (คงสถานะ fail-closed ปัจจุบัน) ปลอดภัย ไม่มีความเสี่ยงใหม่จากการไม่ตอบ ⇒ ไม่ escalate ซ้ำ ไม่นับ
เป็นตัวบล็อกที่ต้องรอ

`20260831_2325_KA1A-ROOTCAUSE-RE-runner-idle-30h-*.md` (`ADDRESSEE: chief`, cc สายนี้) — อ่านแล้ว ไม่ใช่
ของที่ต้อง consume ตามกฎ (ไม่ได้จ่าหน้าถึงสายนี้) แต่เนื้อหาอธิบายตรงว่าทำไม `RE-164` ข้อ 1/3 ถึงค้าง (ดู
ข้อ 2)

## 2. ทำไมไม่มีงาน `gm/` ใหม่ในเขตเขียนได้จริงรอบนี้

- **`RE-164` ข้อ 1/3** (connection-context write-site ของ `[0x01032EC4]`, current-UI-key crosswalk ต่อ
  จาก `[0x008946C0,0x008946EA)`): ต้อง disassembly เพิ่มที่ไม่มีในอิมเมจ clone นี้ (ไม่มี client image
  ไม่มี disassembler) — ตามกฎต้องเปิดใบขอ RE runner บนสะพาน ไม่ใช่เดา *แต่* จดหมาย `KA1A-ROOTCAUSE`
  (23:25 รอบก่อน) เพิ่งชี้ว่า **ตัว RE runner เองว่างมา 30 ชม.** เพราะบั๊กป้ายหมวด (`STATIC-ON-BRIDGE`
  หายจากใบใหม่ทุกใบตั้งแต่ `RE-167` รวมถึง `RE-172` ที่เพิ่งปิด) — เขตคิว/ป้ายหมวด/runner prompt เป็นของ
  chief ตรง ๆ ไม่ใช่เขตเขียนของสายนี้ เปิดใบขอซ้ำสำหรับ `RE-164` เฉพาะตอนนี้จะซ้ำกับใบที่ chief ถืออยู่แล้ว
  (ระบุขอคืนป้ายหมวด + ไล่ใบเก่าให้ครบ) — รอผลจากใบนั้นก่อน แล้วค่อยเปิดใบลูกติดป้าย `STATIC-ON-BRIDGE`
  เฉพาะสำหรับ `RE-164` ข้อ 1/3 รอบถัดที่มีสัญญาณว่าป้ายกลับมาใช้งานได้แล้ว
- **`attr_wire.py` / `/lv`**: shelved ตาม `COO-DECISION 1244` (รอ RE ครบ 24 ฟิลด์ + version-confirmation)
  บวกเงื่อนไขใหม่จาก `RE-172` (bounded-negative — ไม่มีแหล่งบล็อกดิบอื่นให้ seed) ⇒ ทาง 1/2 ทั้งคู่ต้องรอ
  เจ้าของเคาะตามที่ส่งไปแล้ว (ข้อ 1) ทาง 3 (คงปิด fail-closed) คือสถานะปัจจุบันอยู่แล้ว ไม่มีโค้ดให้แก้
- **`GT-172`**: READY จากรอบก่อน รอผู้เทส attended กดเทสจริง ไม่ใช่งานที่สายคลาวด์ทำแทนได้
- **`gm/` technical debt**: `grep -rn "TODO\|FIXME\|XXX\|HACK" src/pirateforce_foundation/gm/` (สดรอบนี้,
  รันใน `pirate-force-server`) = สองรายการเดิม (ตรวจซ้ำหลายรอบก่อนแล้วว่าเป็นคำในเนื้อ docstring ไม่ใช่
  debt จริง — ไม่มีของใหม่)

## เขียว

ไม่ได้แก้โค้ดรอบนี้ (ไม่มี diff ให้ยืนยัน) ชุดล่าสุดที่ยืนยันแล้วจากรอบ `thhkup`: `python3 -m pytest
tests/test_gm_*.py -q` → `1164 passed, 529 subtests passed`

## pf-adversary

ไม่มีการแก้โค้ด ไม่มีอะไรให้ adversary ตรวจรอบนี้ (สอดคล้องกับกติกาที่ "ไม่ใช่การแก้คำผิด" ต้องผ่าน
pf-adversary ก่อน commit — รอบนี้ไม่มี commit เนื้อหาที่ต้องผ่านเกณฑ์นั้น มีแต่จดหมาย/สตับ/round-lock)

## nonclaim

1. ไม่อ้างว่า `RE-164` ข้อ 1/3 ปิดแล้ว — ยังเปิดอยู่ รอ RE runner สองชั้น (ไม่มี image ในคลาวด์ + runner
   เองว่างเพราะบั๊กป้ายหมวดที่เพิ่งพบ ยังไม่ยืนยันว่าแก้แล้ว)
2. ไม่อ้างว่า `KA1A-ROOTCAUSE` letter เป็นเรื่องที่สายนี้แก้ได้ — เขตคิว/runner เป็นของ chief ตรง ๆ
   สายนี้แค่บันทึกผลกระทบต่อ `RE-164` ไว้
3. ไม่แตะ `runtime.py`/`app.py`/`pf_login_game_server_v141.py`/canonical DB/`gm_accounts.json`/
   `scenarios/world_*.json`/`scenarios/combat_*.json` เลย
4. ไม่ให้สถานะ GM กับบัญชีที่ไม่อยู่ใน `gm_accounts.json` ไม่ประกาศ milestone จากผลใด ๆ รอบนี้
5. ไม่ลบประวัติ/จดหมายเดิมใด ๆ — สตับ `.CONSUMED.txt` ที่เพิ่มเป็นไฟล์ใหม่ทั้งหมด ต้นฉบับยังอยู่ครบ ไม่มี
   การขีดฆ่า/แก้ไขเนื้อหาใบเก่าใด ๆ รอบนี้

## ผู้เทสจะทำอะไรได้ที่เมื่อวานทำไม่ได้

**ไม่มี** — รอบนี้เป็น verify-only + mailbox hygiene หนึ่งจุดเท่านั้น ไม่มีการเปลี่ยนแปลงที่ผู้เทสสัมผัสได้
`GT-172` (READY จากรอบก่อน) ยังเป็นทางเดียวที่ผู้เทส attended ทำได้เพิ่มจากเมื่อวาน

## PR

- `pf_bridge#645` ([LANE-GM] WIP round claim dgyakk → ready + marker ท้ายรอบนี้)
- `pirate-force-server#423` (เช่นเดียวกัน + wake-gate commit ท้ายรอบนี้)

— สาย GM รอบ `dgyakk`
