# R113 — LOOT-ROLL-001 (GT-037) + การยิงทดสอบท่อ PR ฝั่ง repo โค้ดครั้งแรก

- **เวลา:** 2026-08-20 ~17:59–18:xx UTC (เริ่มจาก clone ~17:59)
- **รันบน:** Claude Code Routine (cloud) · Linux 6.18 x86_64 · Python 3.11.15 · pytest 9.1.1
- **branch รอบนี้:** `pf_bridge` → `claude/keen-goodall-hd5un3` · `pirate-force-server` → `claude/eloquent-gates-hd5un3`
- **ฐาน:** bridge `fd737cf` (= main หลัง R112 merge) · server `2842fb9` (= main, gate เขียว run 32383555993)

## 1. การ์ดกันรอบซ้อน — ว่าง แต่มีเรื่องต้องรายงาน: **overlap สามเซสชันจริงครั้งแรก**

การ์ดต้นรอบ (GitHub MCP `list_pull_requests`, ไม่ใช่ `gh` — `gh` ไม่มีในอิมเมจ ยืนยันซ้ำจาก R112):
- `pirate-force-server` open = **0** · `pf_bridge` open = **0** (ครั้งแรก timeout หนึ่งครั้ง ยิงซ้ำสำเร็จ)
⇒ ทำงานได้ — แต่ระหว่างสำรวจพบว่า **มีสามเซสชัน "รอบ 112" ถูก trigger ภายใน ~3 นาที**:

| เซสชัน | เวลา (UTC) | ผล |
|---|---|---|
| `claude/hopeful-knuth-fps3tp` | PR #3 เปิด 18:01:19 | **merged อัตโนมัติ 18:01:30** (11 วินาที) — คือ R112 ตัวจริงบน main |
| `claude/hopeful-knuth-xt9cn1` | PR #4 เปิด 18:02:36 | **ปิดอัตโนมัติ 18:02:46** — `mergeable=false` · branch เก็บไว้ · **แล้วมันแก้เอง: merge main → PR #5 → merged 18:09:07** ✅ |
| เซสชันนี้ (`keen-goodall`/`eloquent-gates`) | clone ~17:59 | เริ่มงานช้ากว่า จึงเห็นทั้งสอง PR จบไปแล้ว ⇒ กลายเป็น R113 |

### สิ่งที่ overlap ครั้งนี้พิสูจน์ (ของจริง ไม่ใช่การซ้อม)
1. ✅ **`merge-claude-pr` ฝั่ง bridge ทำงานจริงแล้วทั้งสองทาง**: ทางเขียว (PR #3 merge ใน 11 วิ)
   และทางชน (PR #4 comment+ปิด+เก็บ branch ใน 10 วิ) — nonclaim ใหญ่ของ v4 ("ไม่เคยรันจริง") ปิดได้ครึ่งหนึ่ง
   (ฝั่ง bridge ปิดแล้ว · ฝั่ง server ยังไม่เคยมี PR — รอบนี้คือตัวทดสอบ)
2. 🔴 **บรรทัดดัชนีต่อท้าย `CHIEF_CONTINUATION.md` ยังชนกันได้** เมื่อสองรอบ append พร้อมกัน —
   v4 เขียนว่า "git merge บรรทัดต่อท้ายคนละบรรทัดได้เอง" **วัดแล้ว: ไม่จริงสำหรับ concurrent EOF append**
   (PR #4 ตายเพราะ main ขยับใต้ branch แล้ว diff ทับบรรทัดเดียวกัน) · กฎหนึ่งรอบหนึ่งไฟล์ช่วย "ไฟล์รอบ" ไว้ได้จริง
   — งานไม่หาย (branch อยู่) เสียแค่ล็อก ตามดีไซน์
3. 💰 **ต้นทุน — แก้ข้อเท็จจริงของตัวเอง:** ตอนแรกรอบนี้เขียนว่างานของ xt9cn1 "ถูกทิ้งทั้งใบ" · **ผิด**
   ตรวจซ้ำก่อน push พบว่ามันไม่ยอมแพ้: **merge main เข้า branch ตัวเองแล้วเปิด PR #5 ใหม่ → merge สำเร็จ 18:09:07Z**
   ⇒ งานไม่หายแม้แต่รอบเดียว · ราคาจริงคือ **เวลาและ token ของการทำงานซ้ำ** ไม่ใช่งานที่หายไป
   ⇒ และมันฝากข้อเสนอ v5 ไว้ด้วย: **ใส่ท้าย branch ที่สุ่มไม่ซ้ำลงในชื่อไฟล์รอบทุกใบ** เพราะสองเซสชัน
   เลือกเลขรอบและชื่อไฟล์เดียวกันเป๊ะได้ (กฎหนึ่งรอบหนึ่งไฟล์กันเคสนั้นไม่ได้) — **chief รอบนี้เห็นด้วย**
   · ถ้า cadence จริงคือรายชั่วโมง เหตุการณ์นี้ไม่ควรเกิดอีก
   **ข้อเสนอต่อ Panya: ตรวจหน้า routines ว่ามี routine ซ้ำหลายตัว หรือมีการกด run manual ติดกัน** —
   สามเซสชันใน 3 นาทีไม่ใช่จังหวะของตารางรายชั่วโมง · ห้ามแก้ด้วยล็อกชั้นสอง (กติกา v4) — รายงานอย่างเดียว

### ของจาก xt9cn1 — **เข้า main แล้วเรียบร้อย ไม่ต้องกู้อะไร**
เซสชันนั้นวัดได้ว่า **proxy ฉีด credential ให้ `curl` ด้วย ไม่ใช่แค่ git/MCP** (rate limit 15,000/ชม. = authenticated)
หักล้างบันทึก R109/R110 ที่ว่า "อ่าน Actions API ไม่ได้" — ตรงกับที่ R112 (merged) วัดผ่าน MCP
ทั้งหมดอยู่ใน `rounds/R112_xt9cn1_automerge_proven_and_concurrent_round_evidence.md` บน main แล้ว
(รอบนี้ merge main เข้า branch ตัวเองก่อน push — **ชนบรรทัดดัชนีจริงตามคาด** แก้ด้วยการเก็บทั้งสองบรรทัด ไม่ทิ้งของใคร)

## 2. PROBE รอบนี้ (ยืนยันของ R112 ทุกข้อ)

| ข้อ | ผล |
|---|---|
| `gh` CLI | ❌ ไม่มี (`which gh` exit 1) — เหมือน R112 |
| API ผ่าน GitHub MCP | ✅ ใช้งานจริงทั้งการ์ด PR, Actions list, file contents |
| ทาง D `ci-status` | ✅ fetch ได้ · 3 คำตัดสิน · ใบของ `2842fb9` sha ตรง = `success` (run 32383555993) |
| clone shallow | ✅ ยืนยันข้อค้นพบ R112: clone เริ่มที่ 53 commits · `git fetch --unshallow` → 176 commits สำเร็จ |

## 3. งานหลักรอบนี้: **LOOT-ROLL-001 (GT-037)** — งาน dev headless ที่คิวค้างตั้งแต่รอบ 102

เหตุผลที่เลือก: คิวเขียนเองว่า "งาน dev headless ของ chief — ไม่กินคิวสะพาน ไม่ต้องเปิดเกม · chief จะเริ่มรอบถัดไป"
แล้วรอบ 103–112 หมดไปกับ infra ทั้งหมด ⇒ นี่คือ backlog ที่แก่ที่สุดที่ pre-approved แล้ว
(Door 2 ของดราฟต์ R100 · pure logic ถึง Grade A ได้โดยไม่มี client — ตรงกับข้อจำกัดของ cloud พอดี)

### สิ่งที่สร้าง (ไฟล์ใหม่ 5 + แก้ 1 — ตรงตามประกาศใน PR)
| path | คือ |
|---|---|
| `src/pirateforce_foundation/loot_roll.py` | roller ล้วน ๆ: decode `prefix*100000+n_ID` (27/28/54/87 · item 22/24/25/26) fail closed ทุกทาง · DROPS_NORMAL 30 slot อิสระ · DROPS_EQUIPMENT/SPECIALLY roll เดียว+weighted pick แบบ cumulative-threshold walk ที่ enumerate ขอบได้ · E_DROPS_QUALITY normalize ด้วยผลรวมจริง (แถว 1201 รวม 1000) · **DROPS_QUEST = named refusal ไม่ implement** (client มีแค่ 311/2478 ชุด) · RNG ฉีดจากภายนอก deterministic |
| `tests/test_loot_roll.py` | 66 เทส + 71 subtests: determinism ปักผลตายตัว · ทุก refusal ตามชื่อ · ขอบ rate 0/100/0.5 · ขอบ weighted pick ทุกตัว · แถว 1201 · money slot [INFERENCE] · ตาราง input ไม่ถูก mutate |
| `tools/verify_loot_roller.py` | verifier อิสระ 30 guards re-derive ทุกอย่างด้วยโค้ดแยก · negative control พิสูจน์แล้วว่า guard กัดจริง (mutate 3 จุด → แดงทุกครั้ง) |
| `tests/golden/loot_roll_tables_r100.json` | excerpt เฉพาะแถวที่ factpack R100 ตีพิมพ์แล้ว + provenance block (ตารางจริงอยู่ใน client const-data ที่เครื่องนี้ไม่มี) |
| `reports/PF_LOOT_ROLL001_SERVER_SIDE_ROLLER_20260820.md` | รายงาน + NONCLAIMS ครบ (สูตรของเรา · ไม่แตะ wire/client/DB · coverage ไม่ขยับ · Door 3/4 ยังไม่มี wire path) |
| `.gitignore` (แก้) | +2 บรรทัด allowlist: `!/tools/verify_loot_roller.py` · `!/reports/PF_LOOT_ROLL001_...md` (deny-all กินไฟล์ใหม่ — ดูข้อ 4) |

### การอ่านที่ factpack ไม่ระบุแล้วต้องเลือกเอง (จดครบเพื่อให้เถียงได้ทีหลัง)
ลำดับ roll ตามลำดับใน factpack · rate เทียบ `draw < rate/100` เข้ม · quantity flat span · multi-pick แบบ with-replacement ·
quality ผูกเฉพาะ DROPS_EQUIPMENT · rank จับคู่แบบ **เท่ากันเป๊ะ ไม่ใช่ bitmask** (mob rank 0 จำนวน 1506/3210 ตัว →
named refusal ไม่แต่ง quality ให้) · แถว quality 8 แถวที่ไม่มี level band ตีพิมพ์ = unbounded + ติด tag inference ·
`n_DROPS_*=0` = named refusal `drop_set_id_zero` · DROPS_EQUIPMENT แถว 1 ใน factpack เป็น excerpt ตัด (2/15 entries) — fixture จดไว้ตรง ๆ

## 4. บทเรียน guard-mapping ที่จ่ายครั้งเดียวใช้ได้ทุกรอบ (ลูกมือสำรวจทั้ง repo)

commit ที่เพิ่มไฟล์ใหม่ใน repo โค้ด ต้องรู้ห้าเรื่องนี้ (วัดจริงรอบนี้ ไม่ใช่คาดเดา):
1. `.gitignore` เป็น **deny-all + allowlist**: ไฟล์ใหม่ใต้ `tools/` และ `reports/` **git มองไม่เห็น**
   จนกว่าจะเติม `!/tools/<ชื่อ>` / `!/reports/<ชื่อ>` — โมดูล `src/`, `tests/`, `tests/golden/` เข้าอัตโนมัติ
2. `test_npc_interaction_wire.py:328` ห้ามคำ `quest/shop/store5/price/reward/trade` (word-boundary,
   รวม comment/docstring) ในทุกไฟล์ `src/pirateforce_foundation/*.py` — `DROPS_QUEST` ปลอดภัย (underscore)
   แต่คำเดี่ยวไม่ปลอดภัย · guard นี้ไม่สแกน `tests/` `tools/` `reports/`
3. cp874 tripwire ของ gate สแกนทุก `.py` ที่ tracked ใต้ `tools/ src/ current/` ทุกตัวอักษร —
   ไฟล์ใหม่ต้อง pure-cp874 (ASCII ปลอดภัยสุด)
4. ledger/coverage เป็น declaration-driven: ไฟล์ใหม่ที่ไม่ถูก cite ไม่ทำอะไรแดง ·
   แต่ถ้า cite เมื่อไหร่ ต้อง re-pin `GRADE_SUBSET_SHA256`/`CANONICAL_CONTENT_SHA256` พร้อมกัน
5. commit ที่แตะ `.gitignore`/report ⇒ ต้องรันก่อน: `tests/test_foundation_legacy_seam.py` (กฎเหล็กเดิม)

## 5. สวีต sanity ฐาน (ก่อนแตะอะไร) — ที่ server `2842fb9`

สูตร gate (exclude 43 โมดูล client-image ด้วย `grep -lE 'GameClient|capture_v141'`) หลัง unshallow:
**926 passed, 4 skipped (declared), 1300 subtests passed, 0 failed** = **เขียว(cloud sanity)** บนต้นไม้ที่ยังไม่แตะ

## 6. สวีตหลังเพิ่มไฟล์ + seam test (หลังแก้ `.gitignore`)

- seam + word-guard เฉพาะทาง: `test_foundation_legacy_seam.py test_npc_interaction_wire.py test_names_fold003_thunk_census.py`
  → **62 passed, 5 skipped (declared), 1207 subtests** — กฎเหล็ก "แตะ .gitignore/report ต้องรัน seam ก่อน" ทำแล้ว
- สวีตเต็มสูตร gate: **992 passed, 4 skipped (declared เดิมทั้ง 4), 1371 subtests, 0 failed** = **เขียว(cloud sanity)**
  (ฐานก่อนแตะ: 926 passed — ส่วนเพิ่มทั้งหมดคือเทสใหม่ของ lane นี้)
- cp874: ทั้ง 5 ไฟล์ pure ASCII พิสูจน์ด้วย encode ไม่ใช่ด้วยการรันแล้วดู · โมดูลไม่มี token ต้องห้ามของ guard ใดเลย

## 7. nonclaims ของรอบ

- **เขียว(cloud sanity) เท่านั้น — ไม่ใช่ gate** · gate ตัวจริงรันบน Actions เมื่อ PR เปิด และนั่นคือ
  **การยิงทดสอบท่อ server-side (PR → gate-windows → merge-claude-pr) ครั้งแรกในประวัติ** — R112 ทดสอบเฉพาะฝั่ง bridge
- roller ไม่แตะ wire/DB/dispatch — **ยังไม่มีทางส่งผล roll ถึงผู้เล่น** (Door 3/4 ไม่มี wire path — ดูดราฟต์ R100)
- coverage row `monster_spawn_and_loot` **อยู่ที่ `not_started` เหมือนเดิม** — ledger/coverage ไม่ถูก cite จึงไม่ re-pin อะไร
- token cost ของเซสชัน xt9cn1 ที่โดนทิ้ง: **วัดตัวเลขไม่ได้จากที่นี่** (มองไม่เห็น usage ของเซสชันอื่น) —
  จดเป็นข้อจำกัด ไม่ใช่ตัวเลข · กติกา "วัดต้นทุนรอบที่ข้าม" ต้องอ่านจากหน้า usage ของ Panya เอง
- ผล merge ของ PR รอบนี้ **ยังไม่รู้ ณ เวลาเขียน** — รอบถัดไปอ่านจากการ์ด PR ต้นรอบ + `ci-status` ตามสี่กฎ

## 8. สรุป PR รอบนี้

- `pf_bridge`: rounds/R113 (ใหม่) + ดัชนีต่อท้าย CHIEF_CONTINUATION 1 บรรทัด + GT-037 status ในคิว + จดหมาย R113 — 4 path
- `pirate-force-server`: 5 ไฟล์ใหม่ + `.gitignore` — 6 path · gate จะตัดสิน · workflow จะ merge/ปิดเอง
