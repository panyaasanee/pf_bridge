# LANE-A round lnq6xy (เริ่ม 2026-09-07T05:51+07:00 · claim `pf_bridge#1633`)

claim ไม่ใช่ takeover — 05:5x list PR เปิดของ `pf_bridge` ทั้งหมด (5 ใบ) **ไม่มี `[LANE-A]` ใบไหนค้าง**
(GM `#1632` · CS `#1629` · CS `#1595` · Q `#1583` · B `#1493` — ไม่ใช่ล็อกของสายนี้ ห้ามแตะ)

## 1. รอบนี้ขยับ NOW/M ข้อไหน

**NOW.md บรรทัด LANE-A (`0445`)**: "TIER 3 รับแล้ว → เนื้อใบ RE `Bg3001.tgr` ให้ K ตั้งเลข → **ใบ attended**
· `GT-151`+`GT-193` ตอบ K สองบรรทัด (**ค้าง 2 รอบ = ESCALATION**) · ห้ามส่งเฟรมเดา"
รอบนี้ปิดสองข้อที่เหลือของบรรทัดนั้นครบ:
- ✅ **`GT-151`+`GT-193` ตอบแล้วในจดหมายฉบับเดียว** ตามที่ `COO-DECISION 0445` ข้อ 1 สั่งเป๊ะ ๆ
  ⇒ **ไม่มี `COO-ESCALATION-LANE-A`** · ทั้งสองใบ = **ยกเลิก** (เหตุผลวัดเอง ไม่ใช่รับของ K มาทั้งดุ้น)
- ✅ **ใบ attended ขยับจริง**: `GT-266` (ใบ READY ใบเดียวของสายนี้) รอบก่อนวัดว่า **ไม่มี `HEADLESS_PROOF:`**
  ⇒ ตกรถบัสตาม `PANYA 0159` · รอบนี้ **รัน headless บน `origin/main` คอมมิต `550a36d` แล้วได้โทเคนจริง**
  ส่งบรรทัดให้ K วางในใบ ⇒ ใบกลับขึ้นรถบัสได้ทันทีที่ K วาง
- **M2**: ไม่ขยับให้ผู้เล่นเห็น · `RE-289` ตั้งเลขแล้ว (K รอบ `70l5du` · `tickets/RE-289.md`) **ผลยังไม่กลับ**
  ⇒ `ISLAND_CONTACT_DISCRIMINATOR` ยัง `None` ตามเดิม และ **ถูกต้องที่ยังเป็น `None`**
- **หนี้ adversary ของรอบก่อน**: จ่าย **A2 · A3(ครึ่งหลัง) · A4 · A5 · A6 · A7 · A8 · A9 + LOW สองข้อ** ครบในรอบนี้
  (เหลือเฉพาะ LOW ที่เป็นข้อความในไฟล์รอบเก่า ซึ่งแก้ย้อนหลังไม่ได้ ดูข้อ 6)

## 2. ทำอะไร

### (ก) จดหมายสองบรรทัดถึง K — `GT-151` + `GT-193` (บังคับโดย `COO-DECISION 0445`)
`notes_to_chief/20260907_0603_LANE-A-TO-K-gt151-and-gt193-both-cancelled.md`
- `GT-151` = **ยกเลิก** (ตอบซ้ำ · ฉบับแรกออก 04:26 ก่อนจดหมาย COO 19 นาที)
- `GT-193` = **ยกเลิก** · COO บอกว่า "ยืนยันซ้ำต้องบอกได้ว่าขั้นไหนยังวัดของจริง" ⇒ สายนี้ไปวัดเอง:
  ขั้นที่ใบยังเกรดได้คือ 9 กับ 10 เท่านั้น (ขั้น 4-7 หัวใบเขียนเอง "ห้ามเกรดเป็น FAIL เด็ดขาด")
  และทั้งสองขั้นเป็น**ทางปฏิเสธ** ซึ่งวันนี้ถูกปักไว้ headless บน main แล้วทั้งชุด:
  `tests/test_gm_speed_denied_nine_paths.py` มี `test_path_4_unparseable_value` (= รูปของขั้น 10)
  ถึง `test_path_11_row_not_touched` · `test_every_path_prints_both_console_lines`
  · `test_the_same_twelve_characters_on_every_path` ⇒ ตรงเกณฑ์ (ค) "มีผลใหม่ครอบคลุม"
  🔴 เขียนไว้ในจดหมายด้วยว่า **ถ้ายังอยากได้คำตอบบนจอ ให้เปิดใบใหม่ และเจ้าของควรเป็น LANE-GM**
  เพราะไฟล์ทั้งเจ็ดที่ใบอ้างอยู่ในเขต GM และ M2 คือมิลสโตนของสายนี้

### (ข) `HEADLESS_PROOF:` ของ `GT-266` — รันจริง ไม่ใช่เขียนว่าจะรัน
`notes_to_chief/20260907_0604_LANE-A-TO-K-gt266-headless-proof-line.md`
รันบนต้นไม้ `origin/main` เปล่า **ก่อน** commit งานของรอบ (`git merge-base --is-ancestor HEAD origin/main` = จริง):
```
PYTHONPATH=src python3 -c "from pirateforce_foundation.gm import warp_executor as w, warp_scene_persist as p; \
t=w.warp_no_coords_live_target(126); print(t.entry_marker, t.decreed_arrival_marker, t is not None, \
p.login_would_accept(126), p.FAIL_CONSOLE_TOKEN, p.OUTCOME_LOGIN_WOULD_REFUSE)"
-> marker=0 decreed_arrival=17 live_target=True login_would_accept=False
   persist_fail=GM_WARP_SCENE_PERSIST_FAILED.login_would_refuse   (commit 550a36d)
```
ทั้งสี่ค่าจับคู่กับสิ่งที่บล็อก `ATTENDED:` ของใบสั่งให้ผู้เทสมองหาทีละข้อ (`marker=0` คู่กับ
`decreed_arrival=17` · วาปสดไม่ใช่ stage · บรรทัด `GM_WARP_SCENE_PERSIST_FAILED ... login_would_refuse`
ที่ใบบอกว่า "ต้องเห็น") · ชื่อโทเคนดึงจากโมดูลโดยตรง ไม่ได้พิมพ์ตาม

### (ค) `pirate-force-server` — จ่ายหนี้ adversary เจ็ดข้อ (โค้ดจริง ไม่ใช่คำขอโทษในไฟล์รอบ)
ไฟล์: `src/pirateforce_foundation/world_m2_trigger_vital_response.py` +
`tests/test_world_m2_trigger_vital_response.py` เท่านั้น
- **A2** control ที่อ้าง `PF_PROTOCOL_REGISTRY.tsv:97,98,109,110,442` **ผิดแถวจริง** (98 = TriggerVital
  เอง = subject · 442 handler = `0x0073D360`) ⇒ แทนด้วย control ทั้งไฟล์ที่**แรงกว่า**:
  `awk -F'\t' '$8=="0x00710440"' | wc -l` = **69** จาก 520 แถว (TriggerVital เป็นหนึ่งใน 69
  ⇒ **68 คลาสอื่น** ยิงเข้า `mov al,1; ret 4` ก้อนเดียวกัน) · วัดเองรอบนี้ ไม่ได้ลอกเลขของ LANE-UI (73 ผิด)
- **A3 ครึ่งหลัง** `pf_bridge/staged/re234_static_verify.py` "PASS 18/18" — วัดแล้ว **ไม่มีไฟล์นี้ในรีโป**
  (`git ls-tree -r --name-only origin/main | grep re234_static_verify` = 0 hit) ⇒ **ลบการอ้างอิงทิ้ง**
  พร้อมเขียนไว้ว่าทำไมถึงลบ ไม่ใช่ลบเงียบ ๆ
- **A4** docstring สัญญา `TypeError` ที่ tier 3 ปฏิเสธก่อนจนไปไม่ถึง ⇒ **ไม่ย้ายการตรวจ** เพราะมี
  เทสสามใบปักลำดับนี้ไว้แล้วโดยตั้งใจ (`test_tier3_refuses_before_a_bad_registry_is_seen` ฯลฯ)
  ⇒ แก้ที่คำสัญญา: เขียนว่า raise นี้ **มีเงื่อนไข** และบนโมดูลที่ส่งจริงวันนี้เกิดขึ้นไม่ได้เลย
  🔴 **A4 ตามที่ adversary เขียนไว้ ผิดครึ่งข้อ**: `_table_for` **ไม่ได้** unreachable ทุกทาง —
  เทสเข้าถึงมันจริงผ่าน `measured_discriminator()` และ `registered_count` ตรวจแบบไม่มีเงื่อนไข
- **A5** เทสสองใบที่ "ผ่านเพราะ tier 3" ⇒ ใส่ `measured_discriminator()` + assert **ชื่อเหตุผลของ tier
  ที่ชื่อเทสอ้าง** + เพิ่มเทส control · มิวแทนต์ควักไส้ tier 1+2 เป็น `return None`: เดิมสองใบนี้**เขียว**
  วันนี้ **32 subtest แดง**
- **A6** `scene_guard_reason` ยุบ "ผิดชนิด" กับ "ผิดฉาก" ⇒ แยกเป็น `SCENE_REFUSED_NOT_AN_INT`
  ตามที่ `world_m2_survey_plan` ถูกแยกไว้ก่อนแล้ว ⇒ `"126"` จาก TEXT column ไม่ถูกรายงานว่า "ผิดฉาก" อีก
- **A7** คำว่า "รูปสามชั้นเดียวกันกับ `world_sea_edge_crossing.crossing_target`" **ถอนคำ**:
  ของมันปฏิเสธสองชั้นแล้วชั้นสาม **resolve** (ผ่านทั้งสอง id) · สิ่งที่ยืมมาคือ**ลำดับอาร์กิวเมนต์**กับ
  posture fail-closed ไม่ใช่ชั้นที่สาม
- **A8** สี่วิธีสะกด "นี่ int ไหม" ⇒ เหลือ **`_is_a_wire_int` ตัวเดียว** ใช้สะกดของ `world_m2_survey_plan`
  ⇒ ปิดความขัดแย้งที่ adversary วัดได้ (IntEnum 126 ถูกปฏิเสธเป็น scene แต่ผ่านเป็น trigger id)
- **A9** `126` เลิกเป็น literal ซ้ำ ⇒ `M2_ISLAND_CONTACT_SCENE_ID = SEA_EDGE_SOURCE_SCENE_ID` (import จริง)
- **LOW**: `sorted()` ใน `CANDIDATE_TRIGGER_IDS` **ปักแล้ว** (ดูข้อ 3 ว่าปักด้วยกลไก ไม่ใช่ด้วยการสะกด)

## 3. หลักฐาน (สองชั้น แยกกัน · ห้ามใช้ชั้นหนึ่งอ้างอีกชั้น)

**ชั้นมิวแทนต์ (โค้ดของรอบนี้)** — ล้าง `__pycache__`+`.pytest_cache` ก่อนทุกตัว · ฐาน = **42 passed / 72 subtests**
(เดิม 32/61 · +10 เทสใหม่):

| มิวแทนต์ | ก่อนรอบนี้ | หลังรอบนี้ |
|---|---|---|
| `_is_a_wire_int` → `type(value) is int` | (ไม่มีฟังก์ชัน) เดิม `type(x) is not int`→`isinstance` **รอด** | **1 failed** |
| ลบเงื่อนไข `bool` | — | **4 failed** |
| `SCENE_REFUSED_NOT_AN_INT` ชี้กลับไปที่ค่าเดิม | (ไม่มีค่าคงที่) | **1 failed** |
| ลบ `sorted()` ออกจาก `CANDIDATE_TRIGGER_IDS` | **รอด** | **1 failed** |
| `M2_ISLAND_CONTACT_SCENE_ID = 126` (literal) | (สะกดแบบนี้อยู่แล้ว) | **1 failed** |
| สลับลำดับ tier (id ก่อน scene) | 1 failed | **1 failed** |
| ตัด tier 3 ทิ้ง | 5 failed | **5 failed** |
| ควักไส้ tier 1+2 เป็น `return None` | เทส A5 สองใบ **เขียว** | **32 subtest แดง** |

🔴 **สองมิวแทนต์รอดตอนแรกและวิธีที่ปักไม่ใช่การ grep ตัวอักษร**: `sorted()` กับ literal `126`
วัดค่าอย่างไรก็แยกสองการสะกดไม่ออก (dict ของ hook เขียน `{2:…, 3:…}` อยู่แล้ว ⇒ `sorted` เป็น no-op
วันนี้ · และ CPython intern จำนวนเต็มเล็ก ⇒ แม้ `assertIs` ก็ผ่านทั้งสองแบบ)
⇒ ปักด้วย **`importlib.reload` โดยขยับของที่มันพึ่งพา** (ยัด `{3:…, 2:…}` ให้ hook แล้ว reload ⇒ ยังต้องได้
`(2, 3)` · ตั้ง `SEA_EDGE_SOURCE_SCENE_ID = 777` แล้ว reload ⇒ โมดูลต้องกลายเป็น 777) แล้วคืนสภาพใน
`finally` ⇒ **grep กลไก ไม่ใช่การสะกด** ตาม `NOW.md`

**ชั้นข้อเท็จจริงบนสะพาน (แยกจากชั้นบน ไม่ได้พึ่งกัน)** — รันในโคลน `pf_bridge`:
- `awk -F'\t' '$8=="0x00710440"' external/PF_PROTOCOL_REGISTRY.tsv | wc -l` = **69** (ไฟล์ 520 แถว)
  · แถว `TriggerVital` เอง: `serializer_va=0x006007C0` `handler_va=0x00710440` ⇒ อยู่ใน 69 นั้น
  · `awk -F'\t' '$7=="0x00710440"'` = 19 (คนละคอลัมน์ คนละคำถาม — เขียนไว้กันคนอ่านสลับ)
- `git ls-tree -r --name-only origin/main | grep re234_static_verify` = **0 hit**
- ฝั่ง GT-266: ค่าที่พิมพ์ออกมาเป็นของฉาก 126 บน `550a36d` (ดูข้อ 2 ข)

## 4. nonclaims
- **ผู้เล่นยังไม่เห็นอะไรต่างจากเมื่อวาน** จากงานโค้ดของรอบนี้ — เป็นการจ่ายหนี้คุณภาพบนโมดูลที่
  ยังไม่มีอะไรใน `src/` import (ยืนยันซ้ำรอบนี้: importer เดียวคือไฟล์เทสของมันเอง)
- `HEADLESS_PROOF:` ของ `GT-266` **ไม่ใช่ชั้น client-observable** และไม่ได้อ้างว่าเป็น · ใบยังต้องบูต attended
- ไม่ได้รัน `tests/test_gm_speed_denied_nine_paths.py` — ข้ออ้างเรื่อง `GT-193` คือ "หมุดพวกนี้**มีอยู่**"
  ไม่ใช่ "หมุดพวกนี้เขียววันนี้"
- ไม่ได้แตะ `_CANDIDATES` · ไม่ได้ลงทะเบียนเฟรมใด · ไม่ได้เดาเฟรม · ไม่มี `EnterInstanceVital`
  · ไม่เช็คเลเวล · ไม่แตะ `production_allowed` · ไม่แตะไฟล์คิว · ไม่แตะเขตสายอื่น
- `ISLAND_CONTACT_DISCRIMINATOR` ยัง `None` **โดยตั้งใจ** — `RE-289` ยังไม่มีผล และแม้ผลจะกลับมาเป็นบวก
  ก็ยังต้องมีใบที่สอง (crosswalk ordinal ↔ `0x1FB2` tag `0x0F`) ก่อน ตามที่โมดูลกับใบเขียนไว้ตรงกัน

## 5. TWO_SESSIONS_SAME_SCENE
TWO_SESSIONS_SAME_SCENE: ไม่กระทบ — ไม่มีการเขียน state ใด · `_CANDIDATES` ยังเป็นทะเบียนระดับ process ที่ทั้งสอง id เป็น `None` และไม่มีผู้เขียนฝั่ง production · สอง session ในฉาก 126 ได้คำตอบเดียวกัน (`None`) · relogin ไม่รีเซ็ตอะไรเพราะไม่มีอะไรให้รีเซ็ต

## 6. `pf-adversary`
สั่งต้นรอบตามกติกา (พร้อมเริ่มงาน ไม่ใช่ก่อน commit) บนกิ่งของรอบนี้ทั้งสองรีโป
ผลตอนปิดไฟล์: ดู `ADVERSARY_*` ด้านล่าง
🔴 ข้อ LOW ที่**จ่ายไม่ได้และจะไม่แกล้งจ่าย**: ข้อความในไฟล์รอบเก่า (เลข 32/47 ของ `NO_ORIGINAL_CAPTURE`
สะกดอยู่ใน R318/R322A ไม่ใช่ `RE-234` · "4-tuple" ชี้ผิด branch) — ไฟล์รอบที่ merge แล้วเป็นบันทึกประวัติ
แก้ย้อนหลังไม่ได้ตามกฎบ้าน · บันทึกไว้ตรงนี้แทนเพื่อให้รอบถัดไปไม่ re-derive ของผิด

## 7. NO_FEATURE_WAITING
NO_FEATURE_WAITING: `RE-289` ตั้งเลขแล้วแต่ **ยังไม่มีผลกลับ** ⇒ ไม่มีผล RE ใดถึงสายนี้ที่ต้องแปลงเป็นใบสร้าง+GT ในรอบเดียวกัน · ผลที่ถึงสายนี้รอบนี้คือ `COO-DECISION 0445` (สั่งตอบ K) กับ `LANE-K-NUMBERED-RE-289` (แจ้งเลข) ซึ่งบริโภคครบแล้วพร้อม stub `.CONSUMED.txt`

## 8. รอบหน้าทำอะไร (เรียงลำดับ)
1. **ผล `pf-adversary` ของรอบนี้** ถ้าคืนหลังปลดล็อก = งานแรก (ดูข้อ 6)
2. **ผล `RE-289`** ถ้า RE runner ตอบแล้ว: บริโภคทันที (เจ้าของใบ = สายนี้)
   → ผลบวก: **ห้ามเติม `ISLAND_CONTACT_DISCRIMINATOR` เลย** ออกใบที่สอง (crosswalk ordinal ↔ tag `0x0F`) ก่อน
   → ผลลบ: ปิดทาง `.tgr` ในโมดูลพร้อมเทส
3. **ตามผลของจดหมาย `GT-266`**: ถ้า K วางบรรทัดแล้ว ใบกลับขึ้นรถบัส ⇒ สายนี้มีที่นั่ง attended คืนหนึ่งใบ
   ถ้า K ไม่วาง ⇒ ถามว่าติดตรงไหน
4. 🔴 **คำถามที่ยังไม่มีคำตอบ ค้างมาจากรอบก่อน และรอบนี้ก็ยังตอบไม่ได้**: กลไกที่
   `production_allowed = False` (เช่น `remote_player_hypothesis`) จะพิมพ์โทเคน "ติดอาวุธในฉากเป้าหมาย"
   บนบูตปกติได้อย่างไร ในเมื่อมันถูกปิดอยู่โดยนิยาม — ถ้าไม่มีคำตอบ ใบ attended ของสิ่งที่ยังติดแฟล็ก
   จะติดค้างถาวร ⇒ **รอบหน้าเขียน ASK-COO ใบนี้เป็นงานกระดาษข้อแรก** (รอบนี้ไม่เขียนเพราะเวลาไปอยู่กับ
   งานที่ COO สั่งมาตรง ๆ และงานโค้ด)
5. **promotion**: ข้อ 1 `remote_player_hypothesis` และข้อ 2 `lane_a_choose_npc_scene1` **ยังพลิกไม่ได้**
   ด้วยเหตุผลที่วัดไว้แล้วในรอบ `tsdl0w` (ข้อแรกไม่เคยมีไคลเอนต์เห็นสักไบต์ · ข้อสองปลดแล้ว**เสีย**
   trigger คุยทั่วไป + ร้านค้า P91 = net regression ที่วัดแล้ว) ⇒ **ว่างเพราะรอที่นั่ง attended** ให้ COO นับ
6. **D10/D11/D12** (LOW ค้างจาก adversary ของ `#957`) ยังค้างเหมือนเดิม

## 9. เวลา
เริ่ม 05:51 · เพดาน 75 นาที = **07:06** · ปิดไฟล์นี้ 06:1x
ก้อนเวลาใหญ่สุด = ชุดเต็ม (รันคู่ขนานกับการเขียนจดหมาย) กับ pf-adversary ที่สั่งต้นรอบ

## 10. เกต · ชุดเต็ม · KNOWN_RED_MAIN (พิสูจน์ด้วย control ไม่ใช่คำยืนยัน)
- `python3 tools_bridge/pf_gate_preflight.py --repo <server> --base origin/main` = **PREFLIGHT PASS**
  (รันสองครั้ง: ก่อน commit และบนต้นไม้ที่ commit แล้ว)
- **ชุดเต็มบนต้นไม้สุดท้าย**: `2 failed, 12836 passed, 383 skipped, 31236 subtests passed in 529.58s`
- 🔴 **สองใบที่แดง ไม่ใช่ของสายนี้ และพิสูจน์แล้ว ไม่ได้อ้างลอย ๆ**:
  `tests/test_ui_wire_name_census.py::BuildRowsTests::test_pinned_tier_counts`
  · `tests/test_ui_wire_name_census.py::CommittedArtifactTests::test_committed_artifact_matches_a_fresh_rederive`
  **control**: `git worktree add --detach <tmp> origin/main` + symlink `pf_bridge` ข้าง ๆ
  (เทส census จะ **SKIP** ถ้าไม่มีรีโปพี่น้องอยู่ข้าง ๆ — worktree เปล่าจึงดู "เขียว" หลอก ๆ)
  ⇒ บน `origin/main` เปล่า ได้ **`2 failed, 23 passed`** เทสสองใบเดียวกันเป๊ะ
  ⇒ ตรงกับ `NOW.md` รอบ `0402` "5 แดงบนคลาวด์ ≠ เกตแดง ... ไม่ใช่ของคุณ อย่าถอย"
  · ข้อความจริงที่พิมพ์: `CENSUS DRIFT: reports/PF_UI_WIRE_NAME_CENSUS_20260906.tsv does not match
  a fresh re-derive` (ของ LANE-UI/CS ตาม `COO-DECISION 0445` `db0402-census-pin-161-re-emit-artifact`)
- **`lua_api_message` ×3 (lupa) ไม่ได้แดงในรันนี้** — ต่างจากที่ `NOW.md` เขียนไว้ · ไม่รู้สาเหตุ
  และ **ไม่อ้างว่ารู้** (ไม่ได้ตรวจว่า lupa ติดตั้งอยู่ในอิมเมจนี้หรือเทสถูก skip) บันทึกไว้เฉย ๆ
  เพราะ LANE-UI/Q กำลังถือเรื่องนี้อยู่ (`0540`/`0454`)
- 🔴 `ADVERSARY_PENDING pirate-force-server#993` — สั่ง pf-adversary ต้นรอบตามกติกา
  ผลยังไม่คืนตอนปลดล็อก ⇒ **รอบถัดไปของสาย A สั่ง adversary บนกิ่งนี้เป็นงานแรก** และจ่ายข้อที่คืนมา
  **ยังไม่มีสิทธิ์เขียนว่า "ผ่าน adversary"** และไฟล์นี้ไม่ได้เขียน

SCOREBOARD: COMING | ผู้เล่นยังไม่เห็นอะไรต่างวันนี้ แต่ใบเทสที่ต้องให้เจ้าของเปิดเครื่องขยับจริงสองใบ: GT-266 (วาปเข้าทะเลฉาก 126 สด ๆ ไม่ต้องรีล็อกอิน) ได้บรรทัดหลักฐาน headless ที่ขาดไปจนตกรถบัส โดยรันบนคอมมิต main ปัจจุบันแล้วได้ marker=0 คู่กับ decreed_arrival=17 ตรงตามที่ใบสั่งให้ผู้เทสมองหา ⇒ ใบกลับขึ้นรถบัสได้ · และ GT-193 ถูกยกเลิกโดยเจ้าของใบพร้อมเหตุผลที่วัดเอง ⇒ คืนเวลาเครื่องเจ้าของอีกหนึ่งที่นั่งแทนที่จะเผาไปกับใบที่วัดประตูซึ่งปิดไปแล้ว | pirate-force-server#993 (เปิดแล้ว ไม่ draft · GET ยืนยัน marker แล้ว · 1 commit · 2 files · +326/-31 · **สถานะจริง: รอ gate ไม่ใช่ landed**) · pf_bridge claim #1633 · จดหมาย K สองฉบับ (0603 ยกเลิกสองใบ · 0604 HEADLESS_PROOF ของ GT-266) · adversary A2/A3b/A4/A5/A6/A7/A8/A9 + LOW จ่ายครบเป็นโค้ด · โมดูล 42 passed/72 subtests (จาก 32/61) · มิวแทนต์ 8 ตัวตายครบ (สามตัวเคยรอด) · ชุดเต็ม 2 failed ที่ control พิสูจน์แล้วว่าแดงบน origin/main อยู่ก่อน · preflight PASS

---

## 11. ภาคผนวก — ผล `pf-adversary` คืนหลังปลดล็อก (ไม่ใช่ claim · รอบยังจบตามเดิม)

ผลคืนหลังเติม marker ที่ `#1633` แล้ว ⇒ ตามกฎบ้าน "ผลคืนหลังปลด ⇒ เขียนลงไฟล์รอบ รอบถัดไปหยิบเป็นงานแรก"
🔴 **สายนี้วัดซ้ำเองทุกข้อก่อนรับ** ไม่ได้เชื่อผลเครื่องมือทันที คำสั่งและตัวเลขอยู่ใน body ของ `#993`

### 🔴 D1 (HIGH) — **regression ที่รอบนี้สร้างเอง** · A6/A8 จ่ายผิดทิศ
ข้อ A6/A8 เป็นของจริง (IntEnum 126 ถูกปฏิเสธเป็น scene แต่ IntEnum 3 ผ่านเป็น trigger id)
แต่การรวมสะกดที่ `isinstance(x, int) and not isinstance(x, bool)` **ทำให้ tier 1 หลวมลง** ไม่ใช่แน่นขึ้น
และไปเอาสะกดของ `world_m2_survey_plan` ซึ่ง**ไม่ได้อยู่บนเส้นเรียกนี้** ทั้งที่สองตัวที่อยู่บนเส้นจริง
(`world_sea_edge_crossing.crossing_target` และ `runtime.py:4419`) ใช้ `type(x) is int`

วัดเองทั้งสองต้นไม้:
- **(ก) `candidate_for_trigger_id` raise ที่ `current_scene_id` แล้ว** ⇒ docstring ของมันเอง
  ("Never raises ... EVERY value of either, of every type") **เป็นเท็จ**
  int subclass ที่ `__eq__` โยน `ValueError`: `550a36d` → `None` · กิ่งนี้ → `ValueError`
  · `world_sea_edge_crossing.crossing_target` ตัวเดียวกัน → `None` (ของเขายังถูก)
- **(ข) ฉากที่ไม่ใช่ 126 ผ่าน tier 1 แล้วได้เฟรมจริง** — int subclass ที่ `__eq__` คืน True เสมอ
  + `__hash__` เป็นของ 3: `candidate_for_trigger_id(Sneaky(999), Sneaky(999), registry={3: frame})`
  → **คืนเฟรมสำหรับฉาก 999** · `550a36d` → `None` (tier 1 ปฏิเสธ)
  ⇒ ประโยคใน `_is_a_wire_int` ที่ว่า "มัน**คือ**จำนวนเต็ม ปลายทางแยกไม่ออก" **วัดแล้วว่าเท็จ**:
  `__eq__` ตัดสิน tier 1 กับ 2 และ `__hash__` ตัดสินการ lookup
- **ไม่มีเทสใบไหนในรอบนี้เห็นทั้งสองข้อ** — มิวแทนต์ `int(current_scene_id) != ...` และ
  `int(wire_trigger_id) not in ...` **รอดทั้งคู่** ที่ 42/42 เขียว (และมิวแทนต์นั้นคือ**ตัวแก้**)

⇒ **ถอน `PF-AUTOMERGE: v4` ออกจาก `#993` แล้ว** (GET ยืนยัน) เพื่อไม่ให้ reaper merge regression ขึ้น main
ตามแบบที่ LANE-B ทำกับ `#922` · body ของ `#993` เขียนไว้ว่า **ห้ามคืน marker จนกว่า D1 จะถูกแก้**
🔴 **งานแรกของรอบหน้าคือแก้ D1 แล้วคืน marker ในการ push เดียวกัน** — สะกดเป็น `type(x) is int`
(เก็บการแยกสองเหตุผลของ A6 ไว้ ไม่มีใครค้าน) + ปักด้วย int subclass ที่ override `__eq__`

### 🔴 D2 (HIGH) — **ของเดิม ไม่ใช่ของรอบนี้** · tier 3 เป็น "ชื่อ" ไม่ใช่ "การตรวจ"
`ISLAND_CONTACT_DISCRIMINATOR = ""` **ปลดทั้งสาม tier** และคืนเฟรมจริง — วัดแล้วว่าเป็นแบบนี้
**ทั้งบน `550a36d` และบนกิ่งนี้** ⇒ ไม่ใช่ regression แต่เป็นแผลจริง
`answer_guard_reason(current_scene_id, wire_trigger_id)` **ไม่มีพารามิเตอร์ใดรับหลักฐานการชนเกาะ**
ทั้งที่สิ่งที่ `RE-289` จะวัดคือข้อเท็จจริงเรื่อง**ตำแหน่งของ session**
⇒ รอบแรกที่ได้ discriminator จะเจอทางเลือกระหว่าง "ขยาย signature" กับ "assign ชื่อเฉย ๆ"
และการ assign ชื่อคือ**บรรทัดเดียวที่ผ่านทุกเทสในไฟล์** แล้วเปลี่ยนยามสามชั้นกลับเป็น
id-only classifier ที่ `RE-234` ข้อ (3) ห้ามไว้พอดี
⇒ **signature ต้องโตก่อนที่ข้อเท็จจริงจะมาถึง ไม่ใช่หลัง** · เรื่องนี้เปลี่ยนรูปที่ `COO-DECISION 0405`
รับรองไว้ ⇒ **รอบหน้าเขียน ASK-COO** ไม่ใช่แก้เงียบ ๆ

### ข้อเล็ก (วัดแล้วทุกข้อ · รายละเอียดใน body ของ `#993`)
- **D3** (MED) ลำดับฟิลด์ของ `CandidateFrame` ไม่มีใครปัก — สลับ `va`/`vital_id` แล้วยัง 42 passed
- **D4** (MED) เลขใน docstring ที่**รอบนี้เพิ่งเขียนเอง** ผิด: "of 520 rows" จริงคือ **519** แถวข้อมูล
  (520 นับ header) · และ "all 30 tests" ที่ถูกคือ **32**
- **D5** (LOW-MED) การอ้าง `staged/re234_static_verify.py` ที่ลบออกจากโมดูลแล้ว **ยังอยู่ต้นทาง**
  ที่ `notes_to_chief/20260904_1953_RE-234-RESULT-*.md:9` พร้อม SHA-256 ของไฟล์ที่ git ไม่เคยเห็น
  ⇒ ต้องเขียนจดหมายถึง K/chief ไม่ใช่แก้ docstring
- **D6** (LOW) มิวแทนต์รอดสองตัว: `_CANDIDATES = {2: None, 3: None}` (รูปเดียวกับที่ A9 เพิ่งจ่าย
  ต่ำลงมาหน้าจอเดียว — helper `reimported_with` ของรอบนี้ฆ่าได้ด้วยการเรียกเพิ่มครั้งเดียว)
  · `_table_for(registry) or _CANDIDATES` ใน `registered_count` ⇒ `registered_count(registry={})`
  แอบอ่านทะเบียน production
- **D7** (LOW) A5 จ่ายครึ่งเดียว — มิวแทนต์ tier 1/2 ตายจริง แต่ตายด้วย `assertIn(answer_guard_reason(...))`
  ที่เพิ่มเข้าไป **ไม่ใช่** ด้วย `assertIsNone(candidate_for_trigger_id(...))` ที่เป็นชื่อของเทส
  (ทะเบียน production ว่างอยู่แล้ว) ⇒ ส่ง registry สังเคราะห์ที่มีของ แล้ว assertion แรกจะมีเขี้ยว

### สิ่งที่ adversary **ยืนยันว่าถูก** (ของมีค่า อย่าทิ้ง)
- **A2 ใช้คอลัมน์ถูกแล้ว** (`handler_va` = field 8 → 69 · `serializer_va` = field 7 → 19)
  🔴 และมันเตือนว่า **แผนที่สายนี้ส่งไปให้มันตอนต้นรอบ สะกดคอลัมน์ผิด** (บอกว่า serializer)
  ถ้าเดินตามแผนตัวเอง จะจ่ายบั๊กคอลัมน์ผิดด้วยบั๊กคอลัมน์ผิดอีกที — ที่รอดเพราะไปวัดเองก่อนเขียน
- ข้อสรุป shared stub **แข็งกว่าที่เขียนไว้**: `0x00710440` เป็น `handler_va` ที่พบบ่อยที่สุดในตาราง
  และ 69 แถวนั้นเกือบทั้งหมดคือ **ชุดคำขอ client→server** ⇒ มันคือ default handler ของ vital
  ที่ไคลเอนต์ **ไม่เคยรับ** — ควรเขียนประโยคนี้แทนการนับเปล่า ๆ ในรอบหน้า
- **ธรรมชาติของบั๊กเดิมคือ "สลับคอลัมน์" ไม่ใช่ "สุ่มแถว"** และสองในสี่แถวที่ใบเดิมอ้าง
  (`ChooseNPC`, `ChooseNPCByTableID`) **ถูกอยู่แล้ว** แต่ถูกทิ้งไป — ข้อความใหม่ยังไม่ได้พูดข้อนี้
- **A4: การไม่ย้ายการตรวจคือคำตัดสินที่ถูก** — วัดแล้วว่าถ้าย้ายจะแดง 3 ใบพอดี (`3 failed, 29 passed`)
  ⇒ **ห้ามรื้อฟื้นแผนย้าย**
- มิวแทนต์อีก 27 ตัว **ตายหมด** · ชุดเต็มบนหัวของ `#993`: 12681 passed, 538 skipped, 30554 subtests
- `docs/FUNCTIONAL_COVERAGE.json` **ไม่เอ่ยถึงโมดูลนี้เลย** (0 hit ทุกคำ) ⇒ มองไม่เห็นในบัญชี coverage

### แก้ SCOREBOARD ของรอบนี้ให้ตรงความจริง
บรรทัด `SCOREBOARD:` ข้างบนเขียนว่า COMING โดยนับ `#993` เป็นของที่กำลังจะถึง main
**วันนี้ไม่ใช่แล้ว** — marker ถูกถอน ⇒ `#993` จะไม่ merge จนกว่า D1 จะถูกแก้
สองอย่างที่ยังเป็น COMING จริงคือ **จดหมาย `GT-266` (`HEADLESS_PROOF:`)** กับ **การยกเลิก `GT-193`**
ซึ่งไม่ได้พึ่ง `#993` เลย · งานโค้ดของรอบนี้ = **STUCK ด้วยมือของสายนี้เอง โดยตั้งใจ**
