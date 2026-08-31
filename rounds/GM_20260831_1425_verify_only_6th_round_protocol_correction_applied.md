# รอบ GM `u2ulkl` — verify-only ครั้งที่ 6 ติดกัน + ใช้โปรโตคอลล็อกรอบฉบับแก้ไขล่าสุด

## ล็อกรอบ

ต้นรอบตรวจ PR เปิดค้างที่หัวข้อขึ้นต้น `[LANE-GM]` ทั้งสอง repo (`list_pull_requests state=open`):
**ไม่พบทั้งสอง repo** — ว่างสนิท ไม่ใช่ของสายอื่นค้างอยู่

**Section A (ตาม flow ที่กำหนด):** ตรวจ PR `[LANE-GM]` ที่ปิดล่าสุดของทั้งสอง repo คือรอบ `x9wq3r`
(`pf_bridge#598`, `pirate-force-server#386`) — `pull_request_read get` ยืนยัน `merged:true` ทั้งคู่
(`merged_by: github-actions[bot]`, `merged_at` ตรงกับ `closed_at`) ⇒ งานรอบก่อนอยู่บน `main` แล้วจริง
ไม่ต้อง cherry-pick กู้อะไร

จึงเปิด draft PR ยึดล็อกใหม่: `pf_bridge#602`, `pirate-force-server#389` (branch `claude/wonderful-allen-u2ulkl`
/ `claude/awesome-turing-u2ulkl`, ตั้งจาก `origin/main` สดของแต่ละ repo)

## 🔴 โปรโตคอลล็อกรอบ — พบว่ามีการแก้ไขซ้อนหลังใบที่งานอ้างถึง ต้องอ่านก่อนเริ่ม

งานอ้างถึง `notes_to_chief/20260831_1230_PANYA-ORDER-stop-using-the-draft-flag-as-the-round-lock-*.md`
ซึ่งเสนอเปลี่ยนตัวล็อกจาก draft flag เป็น marker `WIP` ในหัวข้อ + `PF-AUTOMERGE: v4` ใส่ตอนจบรอบเท่านั้น
**แต่ตรวจ mailbox สดพบว่าใบนั้นถูกแก้ไขแล้วโดยใบที่ใหม่กว่า สามใบ:**

1. `20260831_1242_KA1A-CORRECTION-agents-CAN-undraft-via-the-mcp-tool-*.md` — พิสูจน์ว่าเหตุผลตั้งต้นของ
   ใบ 1230 ("เอเจนต์ปลด draft ไม่ได้เลยสักทาง") **ผิด**: สาย A ใช้ GitHub MCP tool
   `update_pull_request(draft=false)` (ไม่ใช่ raw REST PATCH ไม่ใช่ GraphQL) สำเร็จจริง
   (`pirate-force-server#374`) ⇒ **ถอนข้อเสนอเปลี่ยนตัวล็อกเป็น marker-lock ทั้งหมด** ("อย่าเริ่มข้อ 1-5")
2. `20260831_1245_COO-DECISION-round-lock-livelock-fix-check-gate-before-ending-round.md` — แก้กฎ
   "ล็อกถูกถือ -> จบรอบทันที" เป็น "เช็ค gate ก่อน ถ้าแดงจากเหตุเล็กน้อยให้แก้แล้ว push ก่อนจบรอบ"
   (รอบนี้ไม่เจอ PR ล็อกของสายอื่นค้างอยู่ ข้อนี้จึงไม่มีผลกับรอบนี้ — บันทึกไว้เผื่อรอบหน้า)
3. `20260831_1256_CHIEF-ASK-PANYA-prompt-text-block-for-mcp-undraft-step.md` — chief เสนอถ้อยคำสำหรับแก้
   prompt (ให้ใช้ `update_pull_request(draft=false)` + ยืนยันด้วย `pull_request_read get`) รอเจ้าของกดใส่
   prompt จริง ยังไม่เห็นการยืนยันว่ากดแล้วในกล่องจดหมายถึงเวลาที่เขียนใบนี้

**⇒ รอบนี้ทำตามโปรโตคอลปัจจุบันจริง (draft flag = ตัวล็อก, ปลดด้วย MCP tool ตอนจบรอบ) ไม่ใช่โปรโตคอล
marker-lock ของใบ 1230 ที่ถูกถอนไปแล้วก่อนมีใครนำไปใช้จริง** — เพื่อไม่ให้เกิดกรณีสายหนึ่งเดินตามใบที่ถูก
แก้ไขไปแล้วในกล่องจดหมายเดียวกัน จึงบันทึกลำดับเวลานี้ไว้ชัด ๆ ในรอบนี้

## ตรวจสี่ทางหาบล็อกสดใหม่ (ไม่เชื่อผลรอบก่อน)

1. `ADDRESSEE: LANE-GM` ไม่มี `.CONSUMED.txt` คู่ — grep สดรอบนี้: ไม่มี (สองไฟล์ที่ grep ติด
   `20260831_0147_LANE-B-STATUS-addendum-*` เป็นของสาย B เอง cc สาย GM เท่านั้น ไม่ต้องมี stub, และ
   `20260831_0720_LANE-GM-ASK-COO-*` เป็นจดหมายขาออกของสาย GM เอง ไม่ใช่จดหมายเข้า)
2. CORE-REQUEST/COO-DECISION อ้างเลข `GM-0xx` ที่ยังไม่บริโภค — พบ
   `20260831_1244_COO-DECISION-attr-wire-shelved-until-47-field-encoder-and-version-confirm.md`
   (ใหม่กว่ารอบ `x9wq3r`) อ่านแล้ว: ยืนยันคำตัดสินเดิม (`COO-DECISION 0350`) ไม่มีเงื่อนไขใหม่ —
   `gm/attr_wire.py` ยัง shelve เหมือนเดิม
3. ใบ GT ในคิวของสาย GM — `GT-164` ปิดหัวใบแล้ว (`GAME_TEST_QUEUE.md:8800`) ไม่มีใบ GT อื่นค้าง
4. `rounds/GM_*.md` ล่าสุด (`x9wq3r`) — backlog เดิม: `RE-164` ข้อ 1/3 บล็อกนอกเขต, `GM-042` รอคำตัดสิน
   ระดับเจ้าของ (สองคำถามเฉพาะ), `gm/attr_wire.py` shelved

ผลตรงกับรอบ `x9wq3r`/`ep8v23`/`qy8vln` ทุกประการ ไม่มีเงื่อนไขใหม่มาปลดบล็อก

## ประเมิน gap ที่พบใน `bt_gm_probe.py` — ตัดสินใจไม่ทำ พร้อมเหตุผล (กัน busywork รอบหน้า)

`gm/state_wire.py`'s `field_0x14` (u32) sweep ใน `iter_state_vital_bit_variants()` ครอบแค่บิต 0-7 + ค่าสูงสุด
(`0xFFFFFFFF`) — บิต 8-31 ไม่ถูกครอบ ระบุไว้ตรง ๆ ในทั้ง docstring ของโมดูลและเทส
(`test_u32_bit_variants_cover_bits_0_through_7_only`) ว่า "deliberately not covered this round"

**พิจารณาแล้วว่าไม่ควรขยายบิต 8-31 รอบนี้ (หรือรอบต่อ ๆ ไปถ้าไม่มีเหตุผลใหม่):**
`GT-164` (`notes_to_chief/20260831_0901_GT164-RESULT-*`) วัดแล้วว่า `field_0x14` **ไม่มีผลต่อการ
มองเห็นปุ่มเลยสักค่า** ตลอดทั้ง 9 ค่าที่ทดสอบ (บิต 0-7 + ค่าสูงสุด) รวมถึง boundary `0xFFFFFFFF` และข้อ
เสนอของใบนั้นเองสำหรับรอบถัดไปคือ **"เปลี่ยนสิ่งที่แวดล้อมการคลิก ไม่ใช่เปลี่ยนค่าในเฟรม"** (เฟรมพิสูจน์แล้ว
ว่าถึงและมีผล เหลือแค่ suspect 1/3 ที่ไม่ใช่ค่าฟิลด์) การขยาย sweep บิต 8-31 เพิ่มอีก 24 ตัวจะเป็นการยืนยัน
สิ่งที่รู้อยู่แล้วซ้ำ (ไม่มีผล) โดยไม่แตะ suspect ที่เหลือเลย ⇒ **busywork** ไม่ใช่ทางออกจากบล็อกจริง —
บันทึกไว้ในรอบนี้เพื่อไม่ให้รอบหน้าต้องมาไล่ประเมินซ้ำจากศูนย์

ไม่มีการแก้โค้ดจากการประเมินนี้ (อ่าน+ตัดสินใจอย่างเดียว)

## pf-adversary

รันตรวจแผนรอบนี้ (ไม่มี diff โค้ด มีแค่เอกสาร/รอบ) ก่อน commit — ดูหัวข้อ pf-adversary ด้านล่าง

## เขียว

`pytest tests/test_gm_*.py -q` (`pirate-force-server` HEAD `cf3d37f` ก่อน fetch, รันจริงรอบนี้บน
`origin/main` สด): 1089 passed, 504 subtests เขียว(cloud sanity) — ตัวเลขเดียวกับรอบ `x9wq3r` เป๊ะ
ไม่มี drift ไม่มีไฟล์ `src/`/`tests/` เปลี่ยนรอบนี้

## ค้นแล้ว: เจอ/ไม่เจอ

- `external/00_SEARCH_HERE_FIRST.md` — ค้นแล้ว (`grep -i` หา connection-context/current-UI/object-key/
  BT_GM/GMUI_BASIC) ไม่เจอ artifact ใหม่ที่ตอบ `RE-164` ข้อ 1/3
- `gamedata/00_SEARCH_HERE_FIRST.md` — ค้นแล้ว ไม่เจอ (เนื้อหาในไฟล์นี้เป็น gamedata ไม่ใช่ disassembly
  ของ client `.exe` ที่ข้อ 1/3 ต้องการ)

## nonclaim

1. ไม่ได้ยิงเฟรมใด ๆ ใส่ client จริงรอบนี้ ไม่มีจอ/client image ในสภาพแวดล้อมนี้
2. `RE-164` ยังไม่ปิดครบ ข้อ 1/3 ยังเปิดเหมือนเดิม — รอบนี้ไม่มีความคืบหน้าใหม่ต่อข้อนั้น (verify-only
   ตามเจตนา ไม่ใช่ความล้มเหลวในการหางาน)
3. ไม่แตะ `runtime.py`/`app.py`/`pf_login_game_server_v141.py`/`scenarios/world_*.json`/
   `scenarios/combat_*.json` เลยรอบนี้ ไม่ให้สถานะ GM กับบัญชีที่ไม่อยู่ใน `gm_accounts` ไม่มีการประกาศ
   milestone จากผลที่ได้ด้วย GM
4. `gm/attr_wire.py` ยัง shelve ตาม `COO-DECISION 20260831_0350`/`1244` เหมือนเดิม เงื่อนไขที่เหลือ
   (version-confirmation constant, คอลัมน์ level/hp/class) ยังไม่มีทั้งคู่
5. การตัดสินใจไม่ขยาย `field_0x14` bit-sweep เป็นการอ่านหลักฐานที่มีอยู่แล้วเท่านั้น ไม่ใช่การทดลองใหม่
   ไม่มีการยิงเฟรมยืนยันเพิ่ม
6. ไม่อ้างว่าโปรโตคอลล็อกรอบที่ใช้รอบนี้ (draft + MCP undraft) เป็นทางที่ owner ยืนยันขั้นสุดท้ายแล้ว —
   `CHIEF-ASK-PANYA 1256` เสนอถ้อยคำ prompt ไว้แต่กล่องจดหมายที่อ่านได้ ณ เวลาเขียนรอบนี้ยังไม่มีใบยืนยัน
   ว่าเจ้าของกดรับแล้ว ใช้เพราะเป็นสถานะล่าสุดที่ verify แล้วในกล่องจดหมาย ไม่ใช่เพราะมั่นใจว่าจบเรื่อง

## ผู้เทสจะทำอะไรได้ที่เมื่อวานทำไม่ได้

**ไม่มี** — รอบ verify-only ล้วน ไม่มีจุดเสียบใหม่ ไม่มี behavior เปลี่ยนจากตอนจบรอบ `x9wq3r`

## Backlog สำหรับรอบถัดไป

- `RE-164` ข้อ 1 (connection context)/ข้อ 3 (current-UI object-key): บล็อกนอกเขต รอ client binary VA-level
  disassembly (สาย RE) หรือ attended session ใหม่ (กะ 1-A) — ตรวจซ้ำทุกรอบ ไม่ต้องเปิดใบใหม่จนกว่าสภาพ
  เปลี่ยนตาม `COO-DECISION 20260831_0745`
- `GM-042`: รอคำตัดสินระดับเจ้าของสองข้อ (ความหมายของ "npc off" สำหรับ 5 ตัวใน census คงที่ ·
  8180/8181 มีอยู่จริงฝั่งเซิร์ฟเวอร์หรือยัง) ตาม `CHIEF-REPLY 20260831_0204`
- `gm/attr_wire.py`: shelved ตาม `COO-DECISION 20260831_0350`/`1244` รอ version-confirmation constant
  ของ `UpdateAttrVital` และคอลัมน์ level/hp/class ใน `characters` — ยังไม่มีทั้งคู่
- `field_0x14` bit 8-31 sweep: **ไม่ใช่งานที่ควรทำต่อ** (ดูเหตุผลข้างบน) เว้นแต่มีข้อมูลใหม่จาก RE/attended
  ที่เปลี่ยนข้อสรุปของ `GT-164`

## PR

- `pf_bridge#602` (draft ต้นรอบ ปิดท้ายรอบนี้เป็น ready ด้วย MCP `update_pull_request(draft=false)` +
  retitle)
- `pirate-force-server#389` (draft ต้นรอบ ปิดท้ายรอบนี้เป็น ready ด้วย MCP tool เดียวกัน + retitle +
  wake-gate commit)

— สาย GM รอบ `u2ulkl`
