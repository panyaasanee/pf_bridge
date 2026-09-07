# LANE-A รอบ `pm4jdf` — ปิดประตู id-only ให้จริง และเลิกอ้าง `runtime.py` ด้วยเลขบรรทัด

- เริ่ม 2026-09-07T08:51+07:00 · claim `pf_bridge#1664` · กิ่ง `claude/gifted-turing-pm4jdf` / `claude/dreamy-archimedes-pm4jdf`
- ล็อกรอบ: list แล้วไม่มี `[LANE-A] round ...: claim` เปิดอยู่เลย · เปิดใบเอง แล้ว list ซ้ำ ไม่มีใบเก่ากว่า ⇒ ล็อกเป็นของรอบนี้

## 0. รอบนี้ขยับ NOW/M ข้อไหน

**ขยับ**: ประตูของ M2 (`NOW.md` ⏳ M2 ทาง (ก) `1910`) — แต่เป็นการ**ปิดรู ไม่ใช่เปิดทาง**
**ไม่ขยับ**: M2 เอง และไม่ได้ตั้งใจให้ขยับ · เหตุผลวัดได้ ไม่ใช่ความเห็น อยู่ข้อ 1

## 1. ทำไมรอบนี้ไม่ใช่รอบที่ผู้เล่นเห็นอะไรใหม่ — สามทางตัน วัดทีละทาง

`NOW.md` บรรทัด LANE-A สั่งเป็นลูกโซ่: `TIER 3 รับแล้ว → เนื้อใบ RE Bg3001.tgr ให้ K ตั้งเลข → ใบ attended`

1. **ข้อกลางปิดไปแล้วก่อนรอบนี้**: `RE-289` ตั้งเลขโดย LANE-K รอบ `70l5du` เวลา 05:10
   (`notes_to_chief/20260907_0510_LANE-K-NUMBERED-RE-289.md` · จดหมายต้นทาง `0426` มี `.CONSUMED.txt` แล้ว)
   และ K เขียนเองในไฟล์รอบว่า "บรรทัด LANE-A ... ✅ ปิดแล้ว = `RE-289`"
2. **ข้อสุดท้าย (`ใบ attended`) ยังออกไม่ได้ และเหตุผลไม่ใช่เวลา**: `RE-289` ยังสถานะ `🔴 OPEN`
   (`CLIENT_RE_QUEUE.md:1467`) ⇒ `ISLAND_CONTACT_DISCRIMINATOR` ยังไม่มีค่าที่วัดมา ⇒ tier 3 ปฏิเสธทุก input
   ⇒ ใบ attended ของ M2 วันนี้ **ผลิต `HEADLESS_PROOF:` ไม่ได้** เพราะไม่มีกลไกให้ติดอาวุธ
   ซึ่งคือกรณีเดียวกับที่ COO ค้างถาม Panya อยู่ใน `NOW.md` หัวข้อ "รอ Panya ติ๊ก" ข้อ 2
   (`NO_MECHANISM_TO_ARM:`) และ `NOW.md` เขียนไว้เองว่า **"ระหว่างรอ = ไม่ขึ้นรถบัส"**
   ⇒ ออกใบตอนนี้ = ออกใบที่ตกรถแน่นอน ไม่ใช่ผลผลิต
3. **ท่อ promotion ข้อ 1 ของสายนี้ (`remote_player_hypothesis`) โปรโมตวันนี้ไม่ได้** — และนี่คือสิ่งที่
   รอบนี้ค้นแล้วอยากให้ COO เห็น: docstring ของโมดูลเขียนเองว่า
   **"No client has ever been shown one byte of this profile"** และ
   "Whether anything renders ... are ALL the attended test's questions"
   ⇒ มันไม่ใช่ "พิสูจน์แล้วแต่ติดแฟล็ก" ตามนิยามของท่อ promotion ใน `COMMON_LANE_ROUND.md`
   แต่เป็น **encoder ที่ยังไม่เคยมีใครดูด้วยตา** · ปลดแฟล็ก = ส่งเฟรมเดาให้ไคลเอนต์
   ซึ่งชนบรรทัด `ห้ามส่งเฟรมเดา` ของสายนี้ตรง ๆ ⇒ **ไม่ปลด** และเขียนจดหมายถาม COO แทน (ข้อ 5)

⇒ งานที่เหลือซึ่งเป็นของสายนี้จริงและทำได้จริง = หนี้ที่รอบก่อนส่งต่อ ข้อ 1 และ 2

## 2. งานรอบนี้ (`pirate-force-server` · 1 commit · 2 files · +202/-41)

### 2.1 ปิดประตู id-only ให้จริง แทนการเขียนชื่อผู้กระทำผิดลงยกเว้น

`trigger_id_guard_reason` เป็น **public** และตอบ candidacy จาก wire id เดี่ยว ๆ =
รูปที่ `COO-DECISION 20260907_0405` ข้อ 1 ห้ามตรง ๆ · เทสที่มีไว้จับรูปนี้
(`test_no_public_name_answers_candidacy_from_the_wire_id_alone`) **จับได้จริง** แต่รอบก่อน
จ่ายผลด้วย `allowed_id_only = {"trigger_id_guard_reason"}`

🔴 **allowlist ไม่ใช่รูที่ปิด**: มันทำให้ผู้กระทำผิด **หนึ่งราย** ถูกกฎหมายด้วยชื่อ
แล้วปล่อยประตูเปิดไว้เท่าเดิม · รายต่อไปแค่เติมชื่อลง set เดียวกัน

**สิ่งที่ทำ**: `_trigger_id_guard_reason` (private) · ลบ allowlist ทิ้งทั้งก้อน ⇒ กฎไม่มีข้อยกเว้นแล้ว
· grep ทั้งสองรีโปก่อนเปลี่ยนชื่อ: ไม่มี caller นอกไฟล์นี้กับไฟล์เทสของมัน (ไม่มีใน `src/`,
`gm/`, `lane_hooks/`, `tools/`) ⇒ การเปลี่ยนชื่อไม่มีต้นทุน caller

**เทสใหม่มีสองขา และไม่มีขาไหนเป็น "ชื่อ"**:
- **SHAPE** — public callable ที่รับค่าจากผู้เรียก (ทุกพารามิเตอร์ยกเว้น `registry` ซึ่งเป็น seam
  ของเทสและถูกปฏิเสธดัง ๆ อยู่แล้ว) ต้อง **tier-ordered**: `current_scene_id` มาก่อน
  · ขานี้**ไม่อ่านชื่อพารามิเตอร์** ⇒ เอาผู้กระทำผิดกลับมาในชื่อ `f(trig)` ก็ไม่รอด
  (รูปเดิมมองหาสตริง `wire_trigger_id` ตรง ๆ ⇒ **รอด**)
- **REACH** — public callable ที่ไม่ tier-ordered ต้องเอื้อมไม่ถึง `_trigger_id_guard_reason` /
  `_tier2_id_is_a_candidate` / `answer_guard_reason` · วัดจาก **code object แบบ recursive**
  (ลงไปใน nested function/comprehension) ไม่ใช่จากตัวอักษรในซอร์ส
- `registered_count` ผ่านทั้งสองขา **ด้วยรูปของมัน ไม่ใช่ด้วยชื่อ**: พารามิเตอร์เดียวคือ `registry`
  ⇒ ไม่มีทางยัด id เข้าไป · และเอื้อมไม่ถึง decider ตัวไหนเลย

**มิวแทนต์ที่วัดจริง 3 ตัว ตายครบ**:
| มิวแทนต์ | ผล |
|---|---|
| `def is_candidate_trigger_id(trig)` — public, พารามิเตอร์คนละชื่อ | 2 failed |
| `trigger_id_guard_reason = _trigger_id_guard_reason` — alias ชื่อเดิมกลับมา | 2 failed |
| `def candidacy_summary(registry=None, wanted=None)` — รูป registry แต่ inline `CANDIDATE_TRIGGER_IDS` | 1 failed |

**เทสที่สอง `test_the_private_guards_are_still_private`** ปักว่าชื่อ private **ยังตอบอยู่**
เพราะไม่มีมันแล้ว รอบหน้าทำให้เขียวได้ด้วยการ **ลบ** guard แล้ว inline คำปฏิเสธสองชื่อเข้าไปใน
`answer_guard_reason` — เขียว และสัญญา "ปฏิเสธด้วยชื่อ" ที่ทั้งไฟล์ยืนอยู่บนนั้นหายไปเงียบ ๆ

### 2.2 เลิกอ้าง `runtime.py` ด้วยเลขบรรทัด — และปักไม่ให้รูปนั้นกลับมา

เลขบรรทัดสี่ตัวใน docstring ของโมดูลนี้ **เน่าหมดแล้ว** วัดบน main วันนี้:

| ที่อ้าง | บรรทัดนั้นวันนี้คืออะไรจริง ๆ |
|---|---|
| `runtime.py:8692` | `)` เปล่า ๆ |
| `runtime.py:8676` | `self.create_actor_reply_sent = True` |
| `runtime.py:8634` | `if not self.login_ack_sent:` |
| `runtime.py:8641` | `if not self.select_actor_sent:` |
| `runtime.py:4419` | `if type(scene_id) is not int or scene_id != target.scene_id:` (โค้ด GM warp) |

ของจริงวันนี้: `lane_hooks.fire("vital_inbound_trigger_vital", ...)` อยู่ 8710-8714 ·
`return [("FOUNDATION_CREATE_COMMITTED", pc, frame, 0.10)]` อยู่ 8678

🔴 **การอ้างที่เลิกชี้เป้าตัวเองเงียบ ๆ แย่กว่าไม่อ้างเลย** เพราะคนอ่านคนต่อไปตามไปแล้วเชื่อสิ่งที่เจอ

**สิ่งที่ทำ**: เปลี่ยนเป็น **สตริงที่ grep ได้** ทุกจุด + เทสใหม่ที่ grep `runtime.py`
หาแต่ละ anchor **และ** ยืนยันว่าโมดูลนี้ไม่มี `runtime.py:<เลข>` เหลืออยู่เลย ⇒ รูปที่เน่ากลับมาไม่ได้
· `runtime.py` เป็นไฟล์ของ chief · รอบนี้ **อ่านอย่างเดียว ไม่แตะ** · อยู่รีโปเดียวกัน
⇒ ไม่ต้องมียาม bridge sibling และเทสนี้รันทุกที่ที่ชุดเทสรัน (รวม gate-windows)

**มิวแทนต์ 2 ตัว ตายครบ** — แต่ตัวที่สองตายเพราะ**รอบนี้แก้เทสหลังวัดครั้งแรก ไม่ใช่เพราะเขียนถูกแต่แรก**:
| มิวแทนต์ | ผลครั้งแรก | ผลหลังรัด |
|---|---|---|
| เอาเลขบรรทัดกลับมา (`runtime.py:8692`) | 1 failed | 1 failed |
| โมดูลทิ้ง anchor (`fire(the island trigger point, ...)`) | 🔴 **67 passed = รอด** | 1 subtest failed |

ตัวที่สองรอดเพราะสตริง `vital_inbound_trigger_vital` **ยังโผล่ที่อื่นในโมดูลเดียวกัน** (ย่อหน้าที่พูดถึง
`lane_a_island_trigger_log` / `lane_q_trigger_vital_dispatch`) ⇒ เทสรัดใหม่ให้บังคับ**รูปเรียกเต็ม**
`lane_hooks.fire("vital_inbound_trigger_vital", ...)` แทนชื่อ point เปล่า ๆ · บันทึกไว้ทั้งสองค่า
เพราะ "วัดแล้วรอด แล้วรัด" กับ "เขียนถูกแต่แรก" ไม่ใช่เรื่องเดียวกัน

## 3. พฤติกรรม production ไม่เปลี่ยน (และ TWO_SESSIONS_SAME_SCENE)

- **ไม่มีเฟรมใหม่ ไม่มีการปลดแฟล็ก ไม่มี permission ใหม่** · tier 3 ยังปฏิเสธทุก input
  เพราะ `ISLAND_CONTACT_DISCRIMINATOR` และ `ISLAND_EXTENT_BOXES` ยังว่างเท่าเดิม
- **`TWO_SESSIONS_SAME_SCENE:` ไม่เปลี่ยน** — ทั้งสองเป็น process global ที่ยังว่าง
  ⇒ สอง session ในฉาก 126 ได้คำปฏิเสธเดียวกันจากตารางเดียวกัน · ไม่มี path ไหน emit เฟรมล้างฉาก

## 4. หลักฐานสองชั้น

- **wire/DB**: ไม่มีไบต์ใหม่เกิดขึ้นเลยในรอบนี้ — วัดจาก diff (`+202/-41` ใน docstring/เทส/ชื่อฟังก์ชัน
  ล้วน ๆ ไม่มี encoder ไม่มี dispatch) และจากมิวแทนต์ tier 3 ที่ยังปฏิเสธทุกทาง
- **client-observable**: ไม่มี และรอบนี้**ไม่อ้างว่ามี** — ไม่มีใบ GT รอบนี้ เพราะข้อ 1 อธิบายว่าออกไม่ได้
- 🔴 สองชั้นนี้**ไม่อ้างอิงกัน**: ชั้นแรกวัดจาก diff+เทส ชั้นสองคือ "ไม่มี" ที่ประกาศตรง ๆ

## 5. จดหมายรอบนี้

1. `0851_LANE-A-ASK-COO-remote-player-is-not-a-proven-hypothesis.md` — ท่อ promotion ข้อ 1 ของสายนี้
   ปลดไม่ได้ด้วยเหตุผลที่ docstring ของมันเขียนเอง · ขอให้ COO ตัดสินว่าจะ (ก) ถอดออกจากอันดับ 1
   (ข) เปลี่ยนงานเป็น "ออกใบ attended ให้มันก่อน" หรือ (ค) ยืนยันให้ปลด — สายนี้เลือก (ข) ไปก่อน
   และติดป้าย `[สมมติของสาย LANE-A - รอ COO ยืนยัน]`
2. `0851_LANE-A-TO-COO-allowlist-is-not-a-closed-hole.md` — รูปแบบความผิดที่สายนี้เพิ่งเหยียบเอง
   เสนอเป็นกฎบ้าน: ผล adversary ที่จ่ายด้วยการเติมชื่อลง allowlist = ยังไม่จ่าย

## 6. เวลา

เริ่ม 08:51 · เพดาน 75 นาที = **10:06** · ก้อนใหญ่สุด = ชุดเต็ม (~10 นาที) กับการวัดมิวแทนต์ 5 ตัว
· ตัด **ไม่ทำ**: ใบ attended (ข้อ 1 อธิบายว่าออกไปก็ตกรถ) และ promotion (ข้อ 1.3)

## 7. รอบหน้าทำอะไร (เรียงลำดับ)

1. **ผล pf-adversary ของรอบนี้** ถ้าคืนหลังปลดล็อก — งานแรก ไม่ต่อรอง
2. **คำตอบ COO สองใบของรอบนี้** — โดยเฉพาะ `remote_player`: ถ้า COO ตอบ (ข) ⇒ เขียนใบ attended
   ของ `REMOTE-PLAYER-ENCODER-001` พร้อม `HEADLESS_PROOF:` จริง (โมดูลนี้ **ติดอาวุธได้** ต่างจาก M2
   วันนี้ — sweep composer มีอยู่จริงและ arm ในฉาก 1 ผ่านไฟล์ scenario ของมัน) ⇒ **นี่คือใบที่ขึ้นรถบัสได้**
3. `RE-289` ถ้ากลับแล้ว: **ลงตารางกล่อง ไม่ใช่ตั้งชื่อ**
4. มิวแทนต์ที่รอบก่อนบันทึกว่ายังรอด: `str()` coercion · `source: str = ""` · `registered_count` truthiness
   (รอบนี้ไม่ได้วัดซ้ำ — ฝากไว้ในบรีฟของ adversary แล้ว)
