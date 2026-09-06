# R383 · รอบ `3py8sa` · LANE-E (chief) — เทสที่ต้องมี `pf_bridge` ข้าง ๆ ได้ถูกรันบน CI เป็นครั้งแรก

เริ่ม 2026-09-07T06:22+07:00 · claim `pf_bridge#1641` · กิ่ง `claude/ecstatic-cray-3py8sa` (bridge) · `claude/eloquent-edison-3py8sa` (server)
ล็อกรอบ: list PR เปิดของ `pf_bridge` แล้วไม่มีหัว `[LANE-E] round <id>: claim` ใบใด (เห็น `#1639` UI · `#1638` K · `#1637` CS · `#1636` B · `#1634` Q · `#1632` GM ซึ่งเป็นของสายอื่น และ `#1629`/`#1595`/`#1583`/`#1493` ที่เป็น addendum ไม่ใช่ claim) ⇒ จับล็อกเอง ไม่ใช่ takeover
ยืนยันต้นรอบ: `VITAL_REGISTRY_FROM_CLIENT_BINARY_20260817.tsv` มีจริง (11,388 B) · heartbeat สะพาน `2026-09-07T06:14:02+07:00` ห่างจากเวลาเริ่มรอบ 8 นาที (< 60) · `git status` ไม่มี `LOCK_*.txt`

## รอบนี้ขยับ NOW ข้อไหน
บรรทัด **`chief (0546 หนึ่งงานต่อรอบ)`** ข้อ **(3) job checkout สองรีโป + `PF_BRIDGE_DIR`** — งานเดียวของรอบตามที่ COO สั่ง (ข้อ (1)(2) ลงแล้วที่ R382 · `#1627`/server `#989`)
ไม่ขยับ M ข้อใด: M2 ติดที่เฟรม `0x1FB2` ของ LANE-A · M3 ติดที่ `GT-288` ของ LANE-B · รอบนี้เป็นงานแพลตฟอร์มล้วนตามลำดับที่ COO เขียน

## จดหมายที่บริโภครอบนี้ (stub อยู่ใน commit เดียวกัน)
1. `20260907_0445_COO-DECISION-gm0455-chief-work-order-rfe-then-two-repo-job-LANE-E.md` — ลำดับงาน chief ทั้งแถว ⇒ รอบนี้ทำข้อ 3 ของใบนั้น (ข้อ 1/2 ลงแล้ว R382 · ข้อ 4-8 ตามลำดับเดิม รอบถัดไป)
2. `20260907_0546_COO-DECISION-b0512-canonical-db-trap-LANE-E.md` — เข้าคิวเป็นข้อ (9) ไม่แซง 1-8 · ทำซ้ำเองแล้วว่าจริง: รอบนี้ลบ `state/*.sqlite3` ก่อนรันชุดเต็ม ด้วยเหตุผลเดียวกับที่ใบเขียน

## ปัญหาที่รอบนี้ปิด (วัด ไม่ใช่เชื่อ)
`gate-windows.yml` checkout รีโปเซิร์ฟเวอร์รีโปเดียว ⇒ เทสทุกตัวที่ปักการ์ดด้วย precondition ที่ resolve เข้าไปใน `pf_bridge` ข้าง ๆ **skip ทุกคอมมิต ตลอดมา** ด้วยข้อความที่อ่านแล้วเหมือน skip ปกติ — ไม่มีเครื่องไหนบนโลกประเมินมันเลย (LANE-UI ใบ `0335` ข้อ D1 · COO สั่งเป็นข้อ 3)

วัดบนโคลนคลาวด์รอบนี้ (ฐาน `550a36d`) สองแบบ ไม่ได้อ้างจากใบ:
- **A/B ตรง** บน 46 ไฟล์เทสที่เอ่ยชื่อ precondition ของสะพาน: ไม่มีสะพานข้าง ๆ → `1122 passed / 173 skipped / 7180 subtests` · มีสะพาน → `1249 passed / 44 skipped / 7827 subtests` (+ 2 failed ที่เป็น main-red ของ UI `ui_wire_name_census` ไม่ใช่ของรอบนี้)
  ⇒ **129 เทส + 647 subtest พลิกจาก skip เป็นรันจริง**
- **ชุดเต็มไม่มีสะพาน** (`12673 passed / 538 skipped / 30543 subtests` · 448 s): skip ที่ถือคีย์ของสะพาน = **166 ใบ** (`bridge_gamedata` 109 · `external_re_tables` 26 · `lua_corpus_runnable` 11 · `ui_wire_census_inputs` 10 · `bridge_gm_install_bat` 4 · `bridge_serializer_table` 3 · `bridge_sibling` 2 · `bridge_attr_corpus` 1)

🔴 nonclaim: 166 ≠ 129 และรอบนี้ **ไม่อธิบายส่วนต่าง 37 ใบด้วยการเดา** — ส่วนหนึ่งเป็นคีย์ที่ยังขาดของอย่างอื่นแม้มีสะพานแล้ว (`lua_corpus_runnable` ต้องมี `lupa` ซึ่งอิมเมจคลาวด์ไม่มี) ที่เหลือคือสิ่งที่รันรายงานครั้งแรกบน Windows จะตอบเอง นี่คือเหตุผลที่ COO สั่งให้รอบแรกเป็น "รายงานอย่างเดียว" · ตัวเลข 214 ในใบ UI `0335` วัดคนละแบบกับสองตัวเลขนี้ ไม่ได้ยืนยันและไม่ได้หักล้าง

## สิ่งที่ส่งขึ้น (PR ฝั่งเซิร์ฟเวอร์ ใบเดียว 4 ไฟล์)
1. `tools/pf_bridge_guarded_tests.py` — **derive** รายชื่อไฟล์เทสจาก registry ใน `tests/pf_preconditions.py` ไม่ใช่รายชื่อตายตัว (รายชื่อตายตัวจะผิดเงียบ ๆ วันแรกที่สายเพิ่มเทสที่ปักการ์ด) · เดินลง `parts` ของ `AllOfThese` แบบ recursive (`test_script_lua_corpus.py` ถึงคอร์ปัส Lua ผ่านทางนั้นทางเดียว) · มีตัวกันวน · **คืน exit 2 ไม่ใช่ 0 เมื่อ derive ไม่ได้ไฟล์เลย** เพราะรายการว่างที่ส่งเข้า pytest = รันศูนย์เทสแล้วเขียว ซึ่งคือความพังที่งานนี้เกิดมาเพื่อปิด
2. `.github/workflows/bridge-guarded-tests.yml` — clone `pf_bridge` ลง **พาเรนต์ของ workspace** (ที่ `ROOT.parent / 'pf_bridge'` ชี้จริง · `actions/checkout` เขียนออกนอก workspace ไม่ได้ แต่ `git clone` ได้) แล้วรันเฉพาะไฟล์ที่เครื่องมือพิมพ์ออกมา · `windows-latest` เดียวกับเกตจริง
3. `tests/test_pf_bridge_guarded_tests.py` — **21 เทส** (7 การ derive · 5 การสแกนไฟล์ · 5 บนของจริง · 4 รูปร่างของ workflow — ตัวที่ 5 คือ `bash -n` ที่ถอดออกด้วยเหตุผลข้างล่าง)
4. `.gitignore` — `!/tools/pf_bridge_guarded_tests.py` · **จับได้ก่อน commit**: `/tools/*` เป็น allowlist ⇒ เครื่องมือใหม่จะไม่ถูก track เงียบ ๆ และ workflow จะเรียกไฟล์ที่ไม่มีอยู่บน CI

### สามการตัดสินใจที่ต้องบันทึกเหตุผล
- **แยกไฟล์ workflow ไม่ใช่เพิ่ม job ใน `gate-windows.yml`**: `merge-claude-pr.yml` อ่าน conclusion ของ **job ชื่อ `gate`** ใน run ของ workflow `gate-windows` และ `publish-status` เขียนคำตัดสินหนึ่งใบต่อคอมมิตจาก run เดียวกัน ⇒ job ใหม่ในไฟล์นั้นจะอยู่ในรัศมีของทั้งสอง · แยกไฟล์ = reaper มองไม่เห็นโดยโครงสร้าง ซึ่งคือความหมายที่แท้จริงของ "รายงานอย่างเดียว" · เทสปัก: job ต้องไม่ชื่อ `gate`
- **ไม่ต้องมี token ข้ามรีโป**: อ่าน GitHub API รอบนี้ — `panyaasanee/pf_bridge` และ `panyaasanee/pirate-force-server` **`visibility=public` ทั้งคู่** ⇒ clone แบบ anonymous ได้ · **คำปฏิเสธของ R371 (ห้ามสร้าง `PF_BRIDGE_NOTES_TOKEN`) ยังยืน ไม่ได้ถูกกลับ** งานนี้ไม่ต้องใช้ secret ใด ๆ เลย · ถ้าวันหนึ่งสะพานกลายเป็น private ขั้น "พิสูจน์ว่า clone ลงถูกที่" จะแดงดัง ๆ แทนที่จะเขียวบนศูนย์เทส
- **`run:` เป็น bash ไม่ใช่ pwsh**: runner ของ Windows มี bash และ `bash -n` ตรวจได้บนโคลนคลาวด์ · R382 วัดแล้วว่าไวยากรณ์ PowerShell ตรวจไม่ได้จากที่ไหนเลยที่เอเจนต์รันอยู่ — ตรวจครบทั้ง 5 ก้อนรอบนี้ พร้อมด่าน yaml key ซ้ำ และ ASCII

## หลักฐาน / การตรวจก่อน push
- `pytest tests/test_pf_bridge_guarded_tests.py` = **21 passed** (ก่อนถอด method `bash -n` คือ 22) · มิวแทนต์สามตัว **ตายทั้งสาม**: (ก) ถอด recursive ลง `parts` → `test_the_walk_recurses_into_composite_parts` แดง (ข) ถอด short-circuit ของรายชื่อว่าง → `test_no_names_means_no_files_rather_than_every_file` แดง (ค) `return 2` → `return 0` ตอน derive ว่าง → `test_an_empty_derivation_exits_2_and_never_0` แดง
- yaml ไม่มี key ซ้ำ (loader ที่ปฏิเสธ key ซ้ำ) · `bash -n` ผ่านทั้ง 5 ก้อน `run:` · ไฟล์เป็น ASCII ล้วน · job ชื่อ `bridge-guarded` ไม่ใช่ `gate` · `PF_BRIDGE_GUARDED_BLOCKING` ส่งขึ้นเป็น `'0'`
- `python3 tools_bridge/pf_gate_preflight.py --repo /home/user/pirate-force-server` = **PREFLIGHT PASS**
- ชุดเต็ม `pytest tests/` ครั้งเดียวต่อรอบบนต้นไม้ที่ merge `origin/main` แล้ว (คอมมิต `069dfa4`) = **2 failed / 12848 passed / 383 skipped / 31227 subtests · 484 s** · ลบ `state/*.sqlite3` ก่อนรัน ตามใบ `0546` ข้อ (9)
  - สองใบที่แดงคือ `test_ui_wire_name_census.py::BuildRowsTests::test_pinned_tier_counts` และ `::CommittedArtifactTests::test_committed_artifact_matches_a_fresh_rederive` = **main-red ของ LANE-UI ที่ NOW ระบุไว้แล้ว** (`#987` ต้อง merge main + `--emit` ก่อน) ไม่ใช่ของรอบนี้ — วัดยืนยันแล้วว่าแดงบนฐาน `550a36d` ก่อนที่รอบนี้จะแตะอะไร
  - คอมมิตหลังจากนั้น (`df7c2b2`) **ลบ method เทสหนึ่งตัวออกอย่างเดียว** ไม่เพิ่มโค้ด ⇒ รันไฟล์ที่แตะซ้ำ `21 passed` · เขียนไว้ตรง ๆ ว่าชุดเต็มรันบน `069dfa4` ไม่ใช่ `df7c2b2` ไม่กลบด้วยคำว่า "เขียว"
- 🔴 **`[skips]` ของ preflight จับของจริงและรอบนี้ยอมตาม**: เทส `bash -n` ที่ผมเขียนไว้ใช้ `@unittest.skipUnless(shutil.which("bash"), ...)` = skip ที่ขึ้นกับเครื่อง ซึ่งคือสิ่งที่ปิด PR `#503` มาแล้ว และไม่มีเลข pin ค่าไหนถูกทั้งบน runner ที่มี bash และสะพานที่ไม่มี ⇒ **ถอด method นั้นออก เหลือ 21 เทส** และทิ้งคอมเมนต์แทนที่ไว้ว่าตัดสินแล้ว ไม่ใช่ลืม (ตัว `bash -n` เองยังรันมือครบ 5 ก้อนในรอบนี้)
- 🔴 **สิ่งที่จะเกิดขึ้นกับรันรายงานครั้งแรก และต้องไม่มีใครตกใจ**: job ใหม่จะ**แดงตั้งแต่รันแรก**ด้วยสองใบ `ui_wire_name_census` ข้างบน เพราะบนเครื่องที่ **มี** สะพานอยู่ข้าง ๆ เทสคู่นี้ถูกประเมิน ส่วนบนเกตวันนี้มัน skip — นี่คือหนี้ที่งานนี้เกิดมาเพื่อ**เปิดเผย** ไม่ใช่ความผิดของ PR ใด · เจ้าของคือ LANE-UI (`#987`) · และนี่คือเหตุผลรูปธรรมว่าทำไมรอบแรกต้องเป็น "รายงานอย่างเดียว" ตามที่ COO สั่ง
- 🔴 บทเรียนของรอบนี้ที่เกือบกินเวลาไปฟรี: มิวแทนต์ตัวที่สามทิ้ง `.pyc` ค้างไว้ ทำให้เทสที่ควรเขียวหลังคืนไฟล์ยังแดง — ไม่ใช่เทสเปราะ แต่เป็น bytecode เก่า ลบ `tools/__pycache__` แล้วเขียว 22/22 ตามเดิม

## QUEUE_TRIAGE
รอบนี้ **ไม่แตะไฟล์คิว** ตามคำสั่ง COO `1546` และ `1259` (เลขใบ/เนื้อใบ/พับผล/archive = LANE-K) · งานรอบนี้เป็น CI ล้วน ไม่มีอะไรที่ผู้เล่นเห็นบนจอให้เทส จึงไม่มีใบใหม่ที่ควรเข้าคิว attended — ตัวมันเองพิสูจน์ได้จบบน CI ไม่ต้องใช้เครื่องคุณ
READY/PENDING ที่ไม่อยู่ใน NOW รอเครื่องคุณ: ไม่มีเพิ่มจากรอบนี้ (NOW ระบุ `GT-288` B ใบแรก แล้ว `GT-276` CS · `GT-220`/`GT-223` — ทุกใบยังรอ `HEADLESS_PROOF:` ของเจ้าของใบ ไม่ใช่ของ chief)

## WIRED
`WIRED = 0 โมดูลใหม่ที่มี emission จริงบน production path รอบนี้ / เลน production_allowed เท่าเดิม` — รอบนี้ไม่แตะ `runtime.py` และไม่เพิ่มเลน (งาน CI ล้วนตามคำสั่ง หนึ่งงานต่อรอบ)
`TWO_SESSIONS_SAME_SCENE:` ไม่เกี่ยว — ไม่มีโค้ดรันไทม์ในใบนี้ ไม่มีสถานะต่อ session และไม่มีเฟรมออกสาย

## หนี้ที่ค้างและใครถือ (เขียนไว้ให้นับ ไม่ใช่ให้ลืม)
- CORE-REQUEST ที่ยังไม่ได้เดินสาย (B ×2 · GM ×3 · DB ×1 — ระบุใน R382) ยัง**ไม่ขยับรอบนี้** เพราะ COO ใบ `0445` เขียนตรง ๆ ว่าห้ามใบไหนแซงลำดับ chief และรอบนี้คือข้อ 3 ของลำดับนั้น — ไม่ใช่การลืม เป็นการเรียงตามคำสั่ง
- `CHIEF_CONTINUATION.md` เหลือหัวเพียง ~535 B ใต้เพดาน 30,720 B ⇒ **งานแม่บ้านใบแรกของรอบถัดไป** (R382 เขียนไว้แล้วและยังจริง)
- `AGENTS.md` 44,385 B เทียบเพดาน 30 KB = ข้อ (4) ของลำดับ COO

## รอบหน้าทำอะไร
1. **อ่านผลรันรายงานครั้งแรกของ `bridge-guarded-tests` บน Windows** แล้วรายงานตัวเลขจริง (กี่ใบแดง อะไรแดง) — เขียวหนึ่งรอบแล้วจึงพลิก `PF_BRIDGE_GUARDED_BLOCKING` เป็น `'1'` ตามเงื่อนไข COO
2. ผล `pf-adversary` ของรอบนี้ (ดูสถานะข้างล่าง) — จ่ายเป็นงานแรกถ้าคืนหลังปลดล็อก
3. ข้อ (4) ของลำดับ COO: ตัด `AGENTS.md` < 30 KB + ด่านเกินเพดานสัมบูรณ์ · พร้อมงานแม่บ้าน `CHIEF_CONTINUATION.md`

## สถานะ PR (ตามจริง ห้ามเขียนว่าเสร็จ)
- `pirate-force-server#997` (`df7c2b2`): เปิดแล้ว ไม่ draft มี `PF-AUTOMERGE: v4` ตั้งแต่เปิด ยืนยันด้วย GET แล้วว่า marker อยู่จริงหนึ่งบรรทัด — **รอ gate** ยังไม่อยู่บน main (รอบถัดไปยืนยันด้วย `git merge-base --is-ancestor <sha> origin/main`)
- `pf_bridge#1641` = claim ของรอบนี้ ปลดล็อกด้วยการเติม marker หลัง PR เซิร์ฟเวอร์เปิดครบ
- `ADVERSARY_PENDING`: สั่ง `pf-adversary` ไว้ตั้งแต่ต้นรอบบนไฟล์ทั้งสอง ผลยังไม่คืนตอนปลดล็อก ⇒ **ห้ามอ่านไฟล์นี้ว่า "ผ่าน adversary"** · รอบถัดไปหยิบผลเป็นงานแรกตาม COMMON

SCOREBOARD: COMING | เทส 129 ใบที่ตรวจว่าโลก/ฉาก/ใบสั่งของเกมยังตรงกับหลักฐานบนสะพาน จะถูกเครื่องตรวจให้ทุก PR แทนที่จะถูกข้ามเงียบ ๆ ทุกคอมมิตเหมือนที่ผ่านมา | pirate-force-server PR (รอบนี้) + pf_bridge#1641
