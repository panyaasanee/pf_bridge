# R143 (mmtl2a) — GT-055 ปิด: แก้บั๊ก parser 0x36DB เป็น string8 · RE-056 ปิดเลน static · บริโภคจดหมาย 6 ใบหลัง sync กลับมาเดิน

- เวลา: 2026-08-24 ~01:4x–02:xxZ UTC (~08:4x–09:xx +07:00)
- session: mmtl2a · branch เอกสาร `claude/exciting-goldberg-mmtl2a` · branch โค้ด `claude/amazing-goodall-mmtl2a`
- ล็อก: draft PR #44 (`pf_bridge`) เปิดเป็น draft ตั้งแต่วินาทีแรกตาม v5 ข้อ ① — **ล็อกไม่หลุด**

## probe ต้นรอบ

1. GitHub API/tool: ✅ อ่านรายการ PR ได้ทั้งสอง repo (ว่างทั้งคู่) · เปิด draft PR ได้
2. ทาง D `ci-status`: ✅ มีชีวิตบน `pirate-force-server` (20 ไฟล์ใน `ci/`) · ❌ ไม่มี ref บน `pf_bridge` — ปกติ (gate อยู่ repo โค้ดเท่านั้น ไม่ใช่ความผิดปกติใหม่)
3. โครงพี่น้อง: ✅ `VITAL_REGISTRY_FROM_CLIENT_BINARY_20260817.tsv` อยู่จริง

## จดหมายเข้า 6 ใบ (ทั้ง 6 ใบมากับ sync 08:22 `0331655` หลัง sync ฝั่งสะพานตัน · ฉบับอัปเดตของใบ 0821 มากับ sync 08:47 `5b2d0ee` — บริโภคครบ สำเนา+stub แล้ว)

| ใบ | สรุป | สิ่งที่รอบนี้ทำ |
|---|---|---|
| 0229 GT-034 | NO-RESULT รอบสอง: computer-use `list_apps` timeout ×3 หยุดก่อน input แรก · scenario ไม่ถูกยิง (`StartGameReq=0`) · เสนอรอ Panya เทสด้วยตา **2026-08-26** | จดสถานะในคิว · ไม่ปิดใบ ไม่ redirect |
| 0241 GT-055 | **PASS/DONE**: `0x36DB` = tag `0x44` + uint32le byte_len + **string8** · `0xAC52` = tag `0x48` + uint32le byte_len + UTF-16LE · `UNTAGGED_*` = ขอบเขต helper ไม่ใช่ full-wire claim · **parser เราผิดจริงฝั่ง 0x36DB** — ใบสั่งให้ chief เสนอ patch | **แก้โค้ดในรอบนี้** (ดูข้างล่าง) |
| 0728 RE-056 | **DONE/METHOD-FAIL**: registrar `0x5F3DF0` = inbound `CreateById` prototype tree — control `PickupTerrainThing` ก็ถูก register ทั้งที่ outbound จริงคือ `0x006B0639`→`0x005DD800` นอก tree ⇒ วิธี registrar จำแนก outbound ไม่ได้ ⇒ เลน static ของ direction ปิดถาวร | จดสถานะปิดใบ · direction `TriggerCastSkillVital` ยังไม่ตัดสิน · ทางต่อ observe-only attended (พักตาม 16:56) — ไม่เปิดใบใหม่ |
| 0758 RECORDER | ซ่อนคอนโซล ffmpeg + frame proof ผ่าน · `TEMPLATE_video_recorder.ps1` commit ฝั่งสะพาน `234c51f` (ยังไม่ push ตอนนั้น) | จดว่า blocker "คอนโซลทับจอ" ของ GT-034 ถูกปิด |
| 0801 SYNC-UNBLOCK | หยุดที่ ff-only ตามคำสั่ง (local 1 / origin 17) | เป็นบันทึกเหตุการณ์ — ไม่มีงาน |
| 0821 SYNC-ROOT-CAUSE | ตัน 94 ครั้ง (ff-only + allowlist trap) · **แพตช์ทั้ง 5 จุด + ④ ลงมือแล้วโดยผู้ช่วย ตามคำสั่ง Panya ~08:3x — ห้ามเปิดใบซ้ำ** · `AGENTS.md` เคยขาดกฎ 7 ก้อน คืนครบแล้ว | ไม่เปิดใบ (ตามคำสั่งในจดหมาย) · ตรวจแล้วกฎ §9 ของ R137 รอด (บรรทัด 256) · จดพฤติกรรม sync ใหม่: ไฟล์ shared-tracked ถูก push อัตโนมัติ · อาจเห็นจดหมาย `SYNC_STUCK_*.md` โผล่เอง = ของแพตช์ ③ |

## งานหลักของรอบ — STRING8-DELETE-001: แก้ parser `DeleteActorVital 0x36DB` ตามคำตัดสิน GT-055

**หลักฐานสองชั้นก่อนแตะโค้ด:**
- capture (GT-055 อ่าน GT-018 raw บรรทัด 200–206 · corroborate GT-010/GT-011): 32 ASCII bytes ต่อเนื่อง ไม่มี `00` สลับ · parse แบบไม่มี tag ตัดทิ้งได้ (length 0x2044 เกิน record)
- static (TSV ที่ commit แล้ว `external/PF_SERIALIZER_FIELDS.tsv` แถว 462/466): field 4 ของ `DeleteActorVital` = `kind=basic_string<char>` helpers `0x0089A6D0`/`0x0089A740` serializer `0x005E4E10` — ตรงกับ guard ใน `pf_ui_state_refresh_static.py`

**สถานะโค้ด ณ จบรอบ: commit `fa1e804` push แล้ว · PR โค้ด #16 เปิดแล้ว รอ gate — ยังไม่เข้า `main`**
(merge อัตโนมัติโดย workflow เมื่อเขียว · ถ้ารอบหน้าเห็น GT-055 ปิดแต่ main ยังไม่มี `opaque_string8` ให้เช็ค PR #16 — งานอยู่บน branch `claude/amazing-goodall-mmtl2a` ครบแม้ PR ถูกปิดเพราะแดง)

**ไฟล์ที่แตะ (6 ไฟล์ · repo `pirate-force-server` · PR #16):**
1. `src/pirateforce_foundation/delete_actor.py` — `opaque_utf16le` → `opaque_string8` · เลิก refuse ความยาวคี่ (กฎ "ต้องคู่" มาจากการอ่าน UTF-16LE ที่ถูกหักล้าง) · ป้าย expect `wstring` → `string8` · docstring อ้าง GT-055 · กฎ host-side อื่นคงเดิมทั้งหมด (op 2 ต้อง empty · reject trailing data · length bounded)
2. `tests/test_delete_actor.py` — ตามชื่อ field ใหม่ · เพิ่มเทส 2: token ธรรมชาติ 32 ไบต์จาก capture + odd-length accepted · ตัด vector "คี่ต้อง reject" (ตอนนี้เป็น record ถูกกติกา)
3. `src/pirateforce_foundation/delete_actor_hypothesis.py` — ถ้อยคำ docstring/comment เท่านั้น (wstring → string8 · จดว่า GT-010 ผลิต natural 0x36DB ใบแรกแล้ว — ประโยค "ไม่เคยมี capture" เป็นสภาพ ณ วันดีไซน์) · **ไบต์ probe/pinned ไม่แตะ**
4. `tools/pf_ui_state_refresh_static.py` — ป้าย guard `wstring+0x1C` → `string8+0x1C` (ไบต์ guard ไม่แตะ)
5. `docs/HYPOTHESIS_LEDGER.json` — dated amendment ต่อท้าย `exact_value_or_transform` ของ HYP-PF-015 (แบบเดียวกับ R140) — ไม่เขียนประวัติทับ
6. `tools/verify_hypothesis_ledger.py` — re-pin `CANONICAL_CONTENT_SHA256` = `0A0E839A…AD9C` + คอมเมนต์เหตุผล (count คงที่ 42)

**สิ่งที่จงใจไม่แตะ:** ฝั่ง `0xAC52` (chat) — GT-055 ยืนยันว่าโค้ดเราถูกอยู่แล้ว (tag `0x48` + UTF-16LE + refuse คี่ **ยังถูก** เพราะเป็น wstring จริง) · `actor_wire.py` (`CreateActorDataEx` เป็นคนละ field GT-055 ไม่ได้ตัดสิน) · probe payload ไบต์ pinned ทุกตัว

**ผลตรวจ (ที่ tree สุดท้ายหลังแก้ adversary ครบ):** `verify_hypothesis_ledger.py` → `HYPOTHESIS_LEDGER PASS entries=42` · เลน delete+ledger 44 pass · **สวีตเต็ม 2019 pass / 324 skip / 0 fail — เขียว(cloud sanity)** (2017→2019 = เทสใหม่ 2 ใบ) · diff ไม่เพิ่มไบต์ non-ASCII (คู่ non-ASCII เดียวในของเดิมคือ literal ในเทสที่มีอยู่ก่อน)

**pf-adversary (ฝั่งโค้ด) — จับ defect จริง 3 ข้อ แก้ครบก่อน commit:**
- **D1 (สำคัญสุด · เป็น failure shape เดียวกับที่ R140 เคยโดนเป๊ะ):** re-pin แรกของ ledger รับรองประโยค "the opaque wstring" ที่ยังค้างอยู่ **4 จุด** (HYP-PF-015 evidence_gap+stop_rule · **HYP-PF-021 scope+stop_rule**) ใต้ sha ใหม่ ⇒ แก้ด้วย inline dated marker `[AMENDED 2026-08-24 GT-055/R143 ...]` ทั้ง 4 จุด (เปลี่ยนชื่อ field เป็น string8 · ตัวกฎไม่เปลี่ยน) + re-pin ครั้งที่สอง = `9E2A5D34…A707` + คอมเมนต์เล่าเหตุการณ์ในตัว verifier
- **D2:** docstring `delete_actor_hypothesis.py` ยังมีประโยคเท็จ "No natural 0x36DB wire was ever captured" (GT-010 จับได้แล้ว) ⇒ แก้เป็น "existed at design time … GT-010 later produced the first natural 0x36DB"
- **D3:** คอมเมนต์ probe ฉบับแก้แรกกลบความจริงว่า payload ของ probe `deltst01` เป็น **UTF-16LE ของชื่อ "DelTst01"** (pinned-by-history) — ใต้ codec ใหม่มันอ่านเป็น string8 blob 16 ไบต์มี NUL สลับ ไม่ใช่ชื่อ 8 ตัวอักษร ⇒ เขียนบล็อก PINNED-BY-HISTORY ระบุตรง ๆ · **ไบต์ไม่แตะ** (hash pin ปลายน้ำ + server ไม่ decode field นี้)
- ที่ adversary ยืนยันว่าแน่น: odd-length ไม่รั่วไปถึง path ที่ decode utf-16 ที่ไหนเลย (ack echo raw · soft delete คีย์ selector) · sha คำนวณตรงวิธี verifier · ไม่มีที่ไหน pin ชื่อ field เก่า · `actor_wire.py` (UTF-16LE จริง) ไม่ถูกแตะถูกต้องแล้ว
- หลังแก้: ledger PASS 42 · เลน delete+ledger 44 pass · **สวีตเต็ม 2019/324/0 เขียว(cloud sanity) รอบสอง**

**pf-adversary (ฝั่งเอกสาร pf_bridge) — จับ 8 ข้อ แก้ครบก่อน commit:**
- **D1 (HIGH):** เอกสารทุกฉบับพูดว่า "PR โค้ดรอ gate" ตอนที่โค้ดยังเป็น worktree ที่ไม่ commit — scar "อยู่บนเครื่อง ≠ อยู่ใน repo" ⇒ แก้ด้วย **ลำดับ**: commit `fa1e804` → push → เปิด PR #16 **ก่อน** commit เอกสาร แล้วเขียนเลข PR จริง + fallback ("ถ้ารอบหน้าไม่เห็น merge ให้เช็ค PR #16") ลงทุกจุด
- **D2:** ไฟล์รอบอ้างว่าผล adversary อยู่ในจดหมายแต่จดหมายไม่มี ⇒ เพิ่ม section ในจดหมาย + บรรทัด CHIEF_CONTINUATION
- **D3:** pin commit ตาย 2 จุดใน banner (`234c51f` local ถูก sync rebase เป็น `79024e6` · `936cc` พิมพ์ผิด ต้อง `936c4cc`) ⇒ แก้แล้ว
- **D4:** บรรทัดสถานะ R143 ใน CLIENT_RE_QUEUE แทรกผิดลำดับ (หลัง R137) ⇒ ย้ายไปหลัง R141
- **D5:** provenance จดหมายผิด (6 ใบมากับ sync 08:22 `0331655` ไม่ใช่ 08:47) ⇒ แก้แล้ว
- **D6:** เลข "เลน delete 43 pass" เป็นเลขก่อนแก้ (หลังแก้ = 44) ⇒ แก้แล้ว
- **D7:** stub ตั้งชื่อ `X.md.CONSUMED.txt` ขัด convention เดิม `X.CONSUMED.txt` ⇒ rename ทั้ง 6
- **D8:** ประโยค "client ปกติยิง token คู่เสมอ" เป็น universal claim บน capture เดียว ⇒ เขียนใหม่ให้ scoped
- ที่ adversary ยืนยันว่าแน่น: ไม่มีการลบ/ย้ายรายการคิว · ไม่ overclaim เทียบจดหมายต้นทาง · ไม่ขัดคำสั่ง 0821 · timestamps +07:00 ถูกทุกจุด · consumed copies byte-identical · ตัวเลขสวีต/ledger ตรงที่วัดจริง

**คำถามค้างใหม่ #2 (จาก adversary เอกสาร — เชิงระบบ ยกให้ Panya):** ไม่มีกลไกไหน *บังคับ* ให้ "PR โค้ดรอ gate" เป็นจริงตอนเอกสาร merge — สอง repo push อิสระต่อกัน รอบที่ตายกลางทางจะทิ้งคิวเขียวไว้บน main ที่ยังไม่แก้ · R143 อุดด้วยวินัยลำดับ (เปิด PR โค้ดก่อน commit เอกสาร) + fallback ในเอกสาร แต่มันเป็นวินัย ไม่ใช่กลไก

**คำถามค้างใหม่ #1 (จาก adversary โค้ด — ยังไม่ตัดสิน):** probe `op1_selector0_deltst01` ที่ server ยังส่งออกได้ในเลน echo เป็น **wrong-by-design** (ควร re-derive เป็น string8 8 ไบต์ + pin ใหม่ก่อนรอบ attended หน้า) หรือ **pinned-by-history** (เนื้อ payload พิสูจน์แล้วว่าไม่มีผลต่อ repaint `0x4BAEB0`)? — ไม่มีหลักฐานตัดสินตอนนี้ · จดรอ Panya/รอบหน้า ห้ามอ่าน probe นี้ว่า "ชื่อแบบที่ client จะส่งจริง"

## nonclaims ของรอบ

- การแก้ parser เป็นชั้น wire/host เท่านั้น — **ไม่ได้พิสูจน์** ว่า client เคยส่ง string8 ความยาวคี่จริง (capture มีแต่ 32 ไบต์คู่) · ที่แก้เพราะกฎ "ต้องคู่" ยืนบนการอ่าน codec ที่ผิด ไม่ใช่บนหลักฐาน
- ความหมายของ token 32 ไบต์ยัง unclaimed เหมือนเดิม (opaque)
- direction ของ `TriggerCastSkillVital` ยังไม่ตัดสิน — METHOD-FAIL ไม่ใช่หลักฐานทิศทาง
- ไม่ได้ตรวจ 188 ตาราง gamedata หรือ external เพิ่มเติมในรอบนี้
- เวลา +07:00 ในเอกสารรอบนี้เป็นการอ่านนาฬิการะบบ ณ ตอนเขียน (~09:0x) — banner คิวที่เขียนก่อนเช็คนาฬิกาเคยพิมพ์ ~16:xx แล้วแก้เป็น ~09:0x ในรอบเดียวกัน

## คิว (ข้อ ⑤ ของ prompt)

รอบนี้ **ไม่เพิ่มใบเทสใหม่**: เลน attended พักตามคำสั่ง Panya 16:56 · ผล GT-055/RE-056 เป็นการปิดใบ ไม่ใช่เปิด · การแก้ parser พิสูจน์จบชั้น wire ด้วยเทส headless แล้ว ไม่มีอะไรให้ตาคนดู (inbound strict parser — capture ที่มีทั้งหมดเห็นแต่ token 32 ไบต์ตัวเดิม ซึ่งบังเอิญเป็นความยาวคู่ · **ไม่ claim ว่า client ยิงคู่เสมอ** — odd-length ไม่เคยถูกวัด) ⇒ ที่ทำคืออัปเดตสถานะในคิวทั้งสองไฟล์ + banner R143
