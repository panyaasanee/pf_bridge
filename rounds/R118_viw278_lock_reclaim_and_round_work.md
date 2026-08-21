# R118 (viw278) — ล็อกรอบหลุดตาม v5 อีกครั้ง (รอบที่สี่) แล้วยึดคืนด้วย draft PR

- **เวลา:** เริ่ม 2026-08-21 07:00 (+07:00) = 2026-08-21 00:00 UTC
- **รันบน:** Claude Code Routine (cloud) · Linux 6.18 x86_64 · Python 3.11
- **branch รอบนี้:** `pf_bridge` -> `claude/zealous-turing-viw278` · `pirate-force-server` -> `claude/quirky-ride-viw278`
- **ฐานต้นรอบ:** bridge `2c7e50a` (main หลัง R117 merge) · server `520e2cf`

---

## 1. การ์ดกันรอบซ้อน — ทำตาม v5 เป๊ะ แล้วเสียล็อกเป็นรอบที่สี่ติดกัน

ลำดับที่ทำ: `git fetch --all` -> ถาม API -> **PR เปิดค้าง 0 ใบทั้งสอง repo** -> claim commit
`9e40d22` "round claim: viw278" -> push -> เปิด **PR #15 แบบไม่ใช่ draft ตามตัวอักษรของ v5 ข้อ ①**

**ผล (วัดจากเวลาใน API ตรง ๆ):**

| เหตุการณ์ | เวลา UTC | เวลา +07:00 |
|---|---|---|
| PR #15 ถูกเปิด | `2026-08-21T00:00:37Z` | 07:00:37 |
| `merge-claude-pr` merge แล้วปิดมัน | `2026-08-21T00:00:47Z` | 07:00:47 |

⇒ **ล็อกอยู่ได้ 10 วินาที** แล้วหลุดตั้งแต่ยังไม่เริ่มงาน · `merged_by = github-actions[bot]`
เป็นอาการเดียวกันเป๊ะกับที่ R114(lx6eer) · R115(pb54cq) · R117(a25l7d) วัดไว้แล้ว
**นี่คือรอบที่สี่ที่บั๊กเดิมกินเวลาต้นรอบไปฟรี ๆ**

**สาเหตุเชิงกลไก (ยืนยันจากตัวไฟล์ workflow บน main รอบนี้):** `pf_bridge` ไม่มี gate ⇒
`merge-claude-pr.yml` merge ทันทีที่ event `opened` ⇒ PR ที่ไม่ใช่ draft **ไม่มีทางเป็นล็อกได้เลย**
ส่วน draft ถูกข้ามที่บรรทัด `[ "$DRAFT" = "false" ] || { echo "draft - skipped"; exit 0; }`

🔴 **ของที่ chief แก้เองไม่ได้ และต้องให้คุณแก้:** ข้อความ routine prompt ยังเป็น **v5** ⇒ ทุกรอบต่อจากนี้
จะเสียล็อกช่วงต้นรอบเหมือนกันหมด · แก้ได้ด้วยการเปลี่ยนคำในข้อ ③ ของ v5 เป็น
**"เปิด PR เป็น draft ตั้งแต่แรก"** แล้วเพิ่มบรรทัดปิดรอบว่า **"ก่อนจบรอบให้เอา draft ออก (ready for review)
แล้วค่อยแก้หัวข้อ"** — ลำดับนี้สำคัญ เพราะ `ready_for_review` ไม่ได้อยู่ใน `types:` ของ workflow
แต่ `edited` (แก้หัวข้อ/บอดี้) อยู่ ⇒ **การแก้หัวข้อคือสิ่งที่ปลุก merge job**
(หมายเหตุจาก R117: **แปลง PR ที่เปิดไปแล้วให้เป็น draft ไม่ได้** GitHub ปฏิเสธสิทธิ์)

**ท่าที่รอบนี้ใช้แทน:** commit งานจริงหนึ่งใบ -> push -> เปิด PR ใบใหม่ **เป็น draft ตั้งแต่แรก**
พร้อม marker `PF-AUTOMERGE: v4` ⇒ ถือล็อกได้ตลอดรอบ

---

## 2. เลขรอบ · กล่องจดหมาย · probe

**เลขรอบ:** ไฟล์ใน `rounds/` บน main ที่ fetch มา สูงสุด = **R117** ⇒ รอบนี้ = **R118** ไม่ชนกับใคร
ชื่อไฟล์มี session id `viw278` ตามกฎ v5 ②

**กล่องจดหมาย `notes_to_chief/`:** ไล่ด้วยกฎที่ถูก (ยกเว้น `FROM_CHIEF_*` และ `README.md` แล้วหา `.md`
ที่ไม่มี `.CONSUMED.txt` คู่กัน) ⇒ **ไม่มีจดหมายใหม่จากผู้เทสหรือจาก Panya** ใบล่าสุดยังเป็น
`20260820_2130_PANYA-STATUS-install-step2-code-repo-only.md` ที่บริโภคไปแล้ว
⇒ **รอบนี้ไม่แตะไฟล์ของผู้เทสเลย** นอกจากวางจดหมาย `FROM_CHIEF_R118_*` ของตัวเอง

| probe | ผล |
|---|---|
| โครงพี่น้อง `../pf_bridge/VITAL_REGISTRY_FROM_CLIENT_BINARY_20260817.tsv` | **มีจริง** |
| GitHub API (ผ่าน MCP) | **ใช้ได้** — list/create/read/update PR ครบ |
| `which gh` | **ไม่มี** (ตอบเป็นรอบที่เจ็ด — ขอให้ v6 ตัด probe ข้อนี้ทิ้งถาวรอีกครั้ง) |
| ทาง D `ci-status` | **มีชีวิต** — มีคำตัดสินบน branch `ci-status` ของ repo โค้ด · 🔴 **branch นี้อยู่ที่ `pirate-force-server` เท่านั้น ไม่มีใน `pf_bridge`** (ยิง probe ใน bridge จะได้ `couldn't find remote ref ci-status` ซึ่ง **ไม่ใช่** สัญญาณว่าทาง D ตาย — v6 ควรเขียนกำกับไว้) |

---

## 3. งานหลักของรอบ: **"main แดง" ที่ไม่ได้แดง** — และการทำให้มันโกหกไม่ได้อีก

### 3.1 สิ่งที่เจอ (เจอโดยบังเอิญ ตอนวัด baseline ก่อนแตะอะไร)

รันสวีตสูตร gate บน `main` ที่ **ยังไม่แตะอะไรเลย** ได้:

```
1 failed, 1205 passed, 4 skipped, 1879 subtests passed
FAILED tests/test_foundation.py::FoundationTests::test_upgrade_from_original_foundation_schema
E subprocess.CalledProcessError: Command '['git','show','5c200e2:migrations/001_initial.sql']'
  returned non-zero exit status 128
```

รอบ 117 วัดที่ commit เดียวกันได้ **1206 passed, 4 skipped ไม่มี failed**
⇒ อ่านเผิน ๆ คือ **"main แดงแล้ว"** ซึ่ง**ไม่จริงเลยแม้แต่นิดเดียว**

**สาเหตุจริง:** clone ของรอบคลาวด์เป็น **shallow** (`--depth`: รอบนี้เริ่มที่ **53 commit จาก 184**)
⇒ commit `5c200e2` ที่เทสไปอ่าน `migrations/001_initial.sql` **ไม่อยู่ในเครื่องนี้** ⇒ `git show` exit 128
⇒ เทสตายด้วย `CalledProcessError` ดิบ ๆ **ไม่มีคำอธิบาย ไม่มี skip ไม่มีอะไรบอกว่าเป็นเรื่องของเครื่อง**

พิสูจน์ว่าไม่ใช่ regression: `git fetch --unshallow` (184 commit) แล้วรันซ้ำ commit เดิม
⇒ **1206 passed, 4 skipped** ตรงกับรอบ 117 ทุกตัวเลข

🔴 **ทำไมเรื่องนี้ใหญ่กว่าเทสหนึ่งใบ:** ทุกรอบคลาวด์ที่ไม่ได้ `--unshallow` (และไม่มีอะไรบังคับให้ทำ)
จะเห็นสวีตแดงบนต้นไม้ที่ไม่มีใครแตะ แล้วมีทางเลือกสองทางที่**ผิดทั้งคู่**: รายงานคุณว่า main แดง
(เสียเวลาคุณกับความน่าเชื่อถือ) หรือเดาเองว่า "อ๋อ คงเป็นเรื่องเครื่อง" แล้วเดินต่อ (เดาถูกวันนี้ พังวันหลัง)
· และนี่คือ**สิ่งเดียวกันเป๊ะ**กับที่คำสั่งของคุณ 2026-08-20 ~15:45 ห้ามไว้:
*"เทสที่รันไม่ได้ต้องบอกว่ารันไม่ได้และบอกเหตุผล ห้ามหายเงียบ และห้ามแดงมั่ว"*

### 3.2 ขุดต่อแล้วพบว่าไม่ใช่ใบเดียว — **depth 1 แดงสี่ใบ**

clone ใหม่ที่ **depth 1** แล้วรันสวีตเดิม: **4 failed** ไม่ใช่ 1

| เทสที่แดง | เพราะ commit |
|---|---|
| `test_foundation.py::...test_upgrade_from_original_foundation_schema` | `5c200e2` (เก่ากว่า 53 commit — รอบคลาวด์ปกติก็แดงใบนี้) |
| `test_multiplayer_readiness_audit.py::VerifierRunsCleanTests::test_the_verifier_exits_zero_as_a_subprocess` | `5cc0eda` |
| `..::VerifierRunsCleanTests::test_the_json_mode_is_valid_json_and_hides_private_keys` | `5cc0eda` |
| `..::HistoricalSuiteSizeTests::test_the_pin_is_re_derived_from_the_commit_it_names` | `5cc0eda` |

สามใบล่างรัน `tools/pf_multiplayer_readiness_audit.py` ซึ่ง re-derive ขนาดสวีตจาก commit `5cc0eda`
· ตัวเครื่องมือเอง**ทำถูกแล้ว** (มี `HistoryUnavailable` แล้วตอบว่า "re-derive ไม่ได้ที่นี่")
แต่ **เทสที่ห่อมันอยู่กลายเป็นแดง** ทั้งที่มันไม่เคยได้เริ่มทำงานเลย

🔴 **`5cc0eda` อยู่ห่างจาก HEAD 38 commit ⇒ depth 53 มีมัน แต่ depth 1 ไม่มี**
นี่คือเหตุผลที่รอบคลาวด์ก่อน ๆ เห็นแค่ใบเดียว และเป็นเหตุผลที่ **ต้องเป็นล็อกสองดอก ไม่ใช่ดอกเดียว**

### 3.3 ของที่ ship (แก้ 6 ไฟล์ · **ไม่มีไฟล์ใหม่ ไม่มีการลบ**)

| path | ทำอะไร |
|---|---|
| `tests/pf_preconditions.py` | คลาสใหม่ `HistoricalGitObject` — precondition ตัวแรกที่ artifact **อยู่ใน git** ไม่ใช่ข้าง ๆ git · ถามด้วย `git cat-file -e <sha>^{commit}` · คำนวณใหม่ทุกครั้ง ไม่ cache · `git` ไม่มีในเครื่อง = ตอบ "ไม่มี" ไม่ใช่พังซ้ำ · **จงใจถาม `^{commit}` ไม่ใช่ `<sha>:<path>`** เพราะ path หายทั้งที่ commit อยู่ = ประวัติถูกเขียนทับ ต้องแดงดัง ๆ ห้ามกลายเป็น skip เงียบ |
| ” | สองรายการใหม่: `ORIGINAL_SCHEMA_HISTORY` (`5c200e2`) · `AUDIT_HEAD_HISTORY` (`5cc0eda`) — **แยกคีย์กัน** เพราะ clone หนึ่งอาจมีดอกหนึ่งแต่ไม่มีอีกดอก คีย์รวมจะ skip เทสที่รันได้ = อ่อนลงเงียบ ๆ |
| `tests/test_foundation.py` | เรียก `ORIGINAL_SCHEMA_HISTORY.require(self)` ก่อนแตะ git · เลิก hard-code sha ในสตริง ใช้ค่าจาก registry |
| `tests/test_multiplayer_readiness_audit.py` | สามใบข้างบนเรียก `AUDIT_HEAD_HISTORY.require(self)` · `test_two_runs_produce_identical_output` **ไม่ใส่การ์ด โดยตั้งใจ** — มันเทียบผลสองรอบของเครื่องมือกันเอง จริงบนทุกเครื่อง |
| `docs/PYTEST_SKIP_PINS.json` | ปักทั้งสองคีย์ (1 ใบ · 3 ใบ) พร้อมเหตุผลและชื่อเทสครบ ⇒ census แดงทั้งสองทิศ: skip เกินก็แดง · หายไปก็แดง |
| `tests/test_pytest_precondition_census.py` | คลาสเทสใหม่ `HistoricalGitObjectTests` — สร้าง git repo ของเล่นเอง · เทสว่าไม่ cache · revision ที่ไม่มีวันมี · โฟลเดอร์ที่ไม่ใช่ repo · `git` หาย · `require` skip พร้อม token · **และห้ามตัวเองยืนยัน `present` ของรายการจริง** (มันคือสิ่งที่ต่างกันระหว่างเครื่อง) |
| `tools/pf_npc_hp_link_headless_replay.py` | **erratum ในหัวไฟล์เท่านั้น** (ดูข้อ 4) |

### 3.4 หลักฐาน — วัดสามความลึก ไม่ใช่เล่าลอย ๆ (สูตร gate เดิม exclusion 43 โมดูล)

| clone | ผลสวีต | skip เรื่องประวัติ | census |
|---|---|---|---|
| **ประวัติเต็ม 184 commit** (= เครื่อง gate และสะพาน) | **1217 passed · 4 skipped · 0 failed** | **0 ใบ** — เทสทุกใบรันเต็มกำลัง | PASS |
| `clone --depth 53` = **สภาพจริงของรอบคลาวด์** (ได้ 56 commit) | 1216 passed · 5 skipped · 0 failed | เฉพาะ `original_schema_history` 1 ใบ · **สามใบของ audit รันจริง** | PASS |
| clone ใหม่ depth 1 | **1213 passed · 8 skipped · 0 failed** | `original_schema_history` 1 + `audit_head_history` 3 | PASS |

⇒ แถวกลางคือสิ่งที่พิสูจน์ว่า **การแยกสองคีย์ไม่ใช่การประดิษฐ์** — ที่ depth 56 การ์ดตัวที่สองไม่ทำงาน
และสามใบนั้นรันเต็มกำลังจริง ถ้ารวมเป็นคีย์เดียวมันจะถูก skip ทิ้งไปฟรี ๆ

- seam test (กฎเหล็กเมื่อแตะไฟล์ประกาศ): **22 passed, 217 subtests**
- `tools/pf_multiplayer_readiness_audit.py` บนประวัติเต็ม: **exit 0 · guards reproduced**
- ทั้ง 6 ไฟล์ **ASCII ล้วน** พิสูจน์ด้วยการ encode ไม่ใช่ด้วยการรันแล้วดู (ที่นี่ไม่มี cp874)
- 🔴 **เขียว(cloud sanity) เท่านั้น** — ไม่ใช่ gate เต็ม · คำตัดสินจริงมาจาก Actions ตอน PR เปิด

🔴 **สองอย่างเรื่องความลึก ที่ต้องเขียนไว้ตรง ๆ:**
① **`--depth N` ไม่ได้แปลว่า "N commit"** — `clone --depth 53` ได้ **56 commit** (นับตามสายพ่อแม่ ไม่ใช่นับหัว)
⇒ เวลาพูดถึงความลึก **ให้พูดพร้อมตัวเลขที่วัดได้จริง ไม่ใช่ตัวเลขที่ขอไป**
② clone ชั่วคราวอันแรกที่ผมใช้ทดลอง วัดตอนเพิ่ง clone ได้ **1 commit** แต่ต่อมาในเซสชันเดียวกันวัดได้ **56**
ทั้งที่ยังเป็น shallow และ reflog มีบรรทัดเดียว — **ผมอธิบายไม่ได้** ⇒ **ทิ้งมันทั้งใบ** แล้ว clone ใหม่
วัดความลึกทั้ง **ก่อนและหลัง** ทุกครั้ง (d1 อยู่ที่ 1 เท่าเดิมหลังรัน · d53 อยู่ที่ 56 เท่าเดิมหลังรัน
⇒ **ไม่มีเทสใบไหนไปทำให้ clone ลึกขึ้น** และ grep ทั้ง `tests/` `tools/` ยืนยันว่าไม่มีที่ไหนเรียก `git fetch`)
· **ตัวเลขทุกแถวข้างบนมาจาก clone ที่วัดความลึกคาบเกี่ยวทั้งก่อนและหลังการรันเท่านั้น**

## 4. งานรอง: ข้ออ้างเก่าสองจุดที่ **ตอนนี้ผิดแล้ว** — แก้พร้อมหลักฐาน

1. **`tools/pf_npc_hp_link_headless_replay.py` (repo โค้ด)** หัวไฟล์เขียนว่า *"HYP-PF-029 ไม่มี dispatch branch
   ใน `runtime.py` จึงไม่มี dispatcher ให้ขับ"* — **ไม่จริงแล้ว** NPC-HP-LINK-002 เพิ่ม branch ไปแล้ว
   (`runtime.py` บรรทัด ~2574 คีย์บน `CHAT_INPUT_VITAL_ID` → `_dispatch_npc_hp_link_hypothesis`
   และมี `tests/test_npc_hp_link_dispatch.py` เฝ้าอยู่ — **57 passed** รอบนี้) ⇒ เขียน ERRATUM ในหัวไฟล์
   **ข้อจำกัดของเครื่องมือยังเหมือนเดิม แต่เหตุผลเปลี่ยน** (จงใจพิสูจน์แค่ composer ให้ composer มีคนเฝ้าที่ไม่พึ่ง dispatcher)
2. **`pf_bridge/FACTPACK_R100_INREPO_LOOT_SPAWN_GAPLIST.md`** — ERRATUM E2 ของรอบ 115 แก้พินเก่าแล้วชี้ไป
   `runtime.py:586-596` · **พินใหม่นั้นก็เน่าไปแล้วเช่นกัน** (ตอนนี้คือ `runtime.py:614-624`) และพินเก่ายังค้าง
   อีกจุดในหัวข้อ 5 ที่ไม่เคยมีใครแก้ ⇒ เพิ่ม **E2b** พร้อมข้อสรุปที่ใหญ่กว่าตัวเลข:
   **เลิกอ้างช่วงบรรทัดในไฟล์ที่ทุกรอบแก้ ให้อ้างชื่อสัญลักษณ์แล้วให้คนอ่าน grep เอา** — E2 เน่าภายในสามรอบ

## 5. เลนลูท: ถามลูกมือให้ครบก่อนตัดสินใจ แล้ว **ตัดสินใจว่าไม่ยกเลนนี้ในรอบนี้**

`pf-static-re` ขุดจาก artifact ที่ commit แล้วล้วน ๆ (ไม่มีอิมเมจบนคลาว) — ของที่ได้กลับมา ย่อเป็นข้อสรุปเดียว:
**แถว `monster_spawn_and_loot` ยังยกไม่ได้อย่างซื่อสัตย์ในรอบนี้** และนี่คือเหตุผลที่ตรวจได้:

| ช่องว่าง | ข้อเท็จจริง |
|---|---|
| ตัวที่เราฆ่าได้ ไม่มีของให้ดรอป | identity `0x2001` = placement 0 = MOBS `n_ID 1` "Navy Transfer" · rank 0 · `n_DROPS_EQUIPMENT/NORMAL/SPECIALLY = 0` ทั้งสามช่อง |
| ไม่มีสะพานเชื่อม template → โปรไฟล์ลูท | `population.py` รู้ placement→template · `loot_roll.py` รู้ mob-row→roll · **ไม่มีอะไรต่อสองอันนี้เข้าหากัน** |
| ไม่มีตารางในฐานข้อมูลที่รับ "คำตัดสินการดรอป" | ทั้ง repo มี 7 ตาราง ไม่มีตารางลูท/มอนสเตอร์/HP เลย · ปลายทางที่มีจริงมีแค่ `character_backpack_items` และมี INSERT ทางเดียวคือตอนสร้างตัวละคร |
| ไม่มี wire สำหรับ "ของตกบนพื้น" | jump table ของ actor รับ `actor_type` 2..6 ไม่มีเคสของวัตถุ · GT-040 (STATIC-ON-BRIDGE) คือใบที่จะตอบเรื่องนี้ **และมันต้องใช้อิมเมจบนสะพาน** |
| roller ยังเป็นห้องสมุดที่ไม่มีใครเรียก **โดยมีคนเฝ้า** | `production_allowed = False` และ `tools/verify_loot_roller.py` มี guard ว่า **ห้ามโมดูลอื่นใน `src/` อ้างถึงมัน** ⇒ วันที่ต่อสาย guard ใบนี้ต้องถูกแก้พร้อมกันอย่างตั้งใจ ไม่ใช่แอบ |

⇒ **การยกแถวในรอบนี้จะเป็นการยกด้วยคำพูด ไม่ใช่ด้วยของ** จึงไม่ยก · แต่ข้อเท็จจริงเรื่อง `0x2001` ไม่มีดรอป
**ถูกส่งเข้าคิวเป็นคำเตือน** (ข้อ 6) เพราะมันคือสิ่งที่จะทำให้รอบเทสในอนาคตเสียเที่ยวฟรี
