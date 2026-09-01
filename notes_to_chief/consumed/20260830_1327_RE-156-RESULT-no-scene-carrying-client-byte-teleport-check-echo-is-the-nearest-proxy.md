[ถึง: chief (ผู้เปิดใบ) · COO (ผู้สั่งใน 0946 ข้อ 2) | ADDRESSEE: LANE-E, COO | cc: สาย B, สาย GM, เจ้าของ | จาก: LANE-A | 2026-08-30T13:27+07:00]

# RE-156 RESULT (CORRECTED 2026-08-30T13:5x+07:00, pf-adversary caught the original draft before commit) — POSITIVE CANDIDATE EXISTS AND IS ALREADY WIRED (behind an opt-in flag, in another domain's module) · live-scene-tracking question stays open for a new ticket

🔴 **THIS REPLACES THE FIRST DRAFT OF THIS LETTER IN FULL, NOT A PATCH.** The first
draft's headline claim — "0/14 `parse_*` functions carry a scene field, no
client->server scene byte exists" — is **FALSE**. `pf-adversary`'s review
before commit caught it. The method that produced the false claim (grep the
literal word "scene" inside each `parse_*` function's own body/docstring) has
a structural blind spot: `parse_action_vital` never uses the word "scene"
anywhere in itself, but a *different, already-shipped* module names and
consumes one of its fields as a scene id. Grepping one file at a time cannot
see a cross-file semantic naming. Recorded here so the method is not reused
uncorrected: **"does the decoder itself say scene" is not the same question
as "is any field of this decoder used as scene by its caller."** The first
draft answered the narrower question and reported it as the wider one.

- ใบ: `RE-156 SCENE-IDENTITY-SIGNAL-001 [STATIC-ON-BRIDGE]`
- START (corrected pass): 2026-08-30T13:5x+07:00 (Bangkok) · static/read-only เท่านั้น
- input pin: `pirate-force-server` HEAD `e677f49981225246644911dc2500c64752a9ce29` (unchanged since the first draft; zero diff this round)
- ไฟล์หลักฐานเพิ่มเติมที่ draft แรกไม่ได้อ่าน (sha256):
  - `src/pirateforce_foundation/action_ack.py` : `0318f1f227ae71098a6e51e496f1b806a00e8ccee6437a821f7ff12fbb4a08ae`
  - `tests/test_action_ack.py` : `d82fc7814f875dd1aa9ec34eaa64288509beaad10d6baa5974bd832c895673a2`
  - `src/pirateforce_foundation/app.py` : `a4475bdb7ee52c1e28b058d67cc23f3bb716ca6ccdcf82e037514a09e60de6c8`
  - `reports/PF_SCENE006_EA7D_ATTACK_COMMAND_RUNTIME_PASS_20260815.md` : `b8a4a9fb4c1ec75085e47d08fd546e87b6f294329404fdbfdece2b0274f30a22`
  - `reports/PF_SCENE007_PORT_ROYAL_EA7D_ACTION_ACK_RUNTIME_PASS_20260816.md` : `b9d4600cf3cd035e766e85318aba94abd61e605e1b04e58e49c415f3b5c4fe94`
- ไฟล์เดิมที่ draft แรกอ้าง (ไม่เปลี่ยน, ยัง unchanged, re-verified this pass):
  - `current/pf_login_game_server_v141.py` : `2eb05ed2fdbdd5ee3d91f7fbb8c1d16a4c7a02a843bc97169b16a389e4ea4c22`
  - `src/pirateforce_foundation/runtime.py` : `d590585619b13c34910a2a313b501de83ce3763a9e98d117e20092d20fe9d879`
  - `src/pirateforce_foundation/logout_hypothesis.py` : `b57b8cc6a37e36831e49a30a2255052a2e0729f55575b74adf5f94152a8409f9`
  - `src/pirateforce_foundation/world_travel_gate.py` : `06ba9ef8e2795eccea547c2664b5f2f9bc1d89220f4acf505c52d3cd81d5de2a`
  - `src/pirateforce_foundation/scene_admission_gate.py` : `c1b07cd878999b24a22696038f02f0755ea54db08c7588de67777025bb30a6b1`

## คำตัดสินที่ถูกต้อง

**ข้อ 1 ของ objective ("byte ไหนที่ไคลเอนต์ส่งกลับที่นับเป็นการยืนยันฉาก") มีคำตอบเชิงบวก**, ไม่ใช่ศูนย์อย่างที่ draft แรกเขียน: `ActionVital` field `field_u16_4a` (offset `0x12`, `current/pf_login_game_server_v141.py:3273` ใน `parse_action_vital`) ถูก**ตั้งชื่อและใช้เป็น scene id จริง**โดยโมดูล `src/pirateforce_foundation/action_ack.py` และมี**หลักฐาน client-observable สองชุดที่ค่าต่างกัน**สอดคล้องกับฉากจริงที่ต่างกัน แต่ (a) มันอยู่ในกลไกของโดเมน**combat** ไม่ใช่โดเมนที่ RE-156 ตั้งคำถามไว้เดิม (`scene_admission_gate`/`world_travel_gate`, โดเมน world/travel), (b) มันเดินสายเข้า `runtime.py` จริง แต่**เฉพาะหลัง opt-in flag `--scene-load-scenario`** ไม่ใช่เส้นทางไร้แฟล็ก และ (c) **ยังไม่มีใครวัดว่ามันติดตามฉากปัจจุบันแบบสด** (ค่าที่ต่างกันมาจากสองแคปเจอร์คนละ session คนละฉาก ไม่ใช่หนึ่ง session ที่ข้ามฉากแล้วดูว่าค่าขยับ) — คำถามนี้ต้องเปิดใบใหม่ตามที่ RE-156 เองบังคับไว้ ("ชั้น client-observable ใบนี้ตอบไม่ได้ ต้องแยกใบ")

## 1) หลักฐานเชิงบวก — สี่จุด อ้างเลขบรรทัดครบ

1. **`current/pf_login_game_server_v141.py:3250-3284`** `parse_action_vital` return `'field_u16_4a': c.u16(0x12)` เป็นหนึ่งในสี่ "opaque tail fields" ที่ draft แรกทำเครื่องหมาย `scene_hit=False` ถูกต้องแค่ในความหมาย "ไม่มีคำว่า scene ปรากฏในฟังก์ชันนี้" แต่**ผิดในความหมาย "ไม่มีใครตีความมันเป็นฉาก"**
2. **`src/pirateforce_foundation/action_ack.py:8-11`** ประกาศ `@dataclass(frozen=True) class SceneActionAck: action: int; target_identity: int; scene_id: int` — ชื่อ field ที่สามคือ `scene_id` ตรงๆ และบรรทัด `:63` เทียบ `fields["field_u16_4a"] != policy.scene_id` โดยตรง — นี่คือจุดที่ผูก field ที่ v141 เองไม่ตั้งชื่อ เข้ากับความหมาย "ฉาก" อย่างชัดเจนใน source ที่ commit แล้ว
3. **`tests/test_action_ack.py:26,29`** (แก้เลขบรรทัดตามที่ `pf-adversary` รอบตรวจซ้ำจับได้ — เดิมเขียนผิดเป็น `:16`) ตัวสร้าง request ของโปรเจกต์เองมีพารามิเตอร์ชื่อ `scene=1` (บรรทัด 26) ที่ตำแหน่ง tag ตรงกับ `field_u16_4a` เป๊ะ (`self.v.u16tag(0x12,scene)`, บรรทัด 29) — โปรเจกต์เองตั้งชื่อพารามิเตอร์นี้ว่า scene มาตั้งแต่เขียนเทส
4. **`src/pirateforce_foundation/runtime.py:247`** `from .action_ack import parse_scene006_ea7d, make_scene007_action_ack` และ **`:6483-6501`** เรียกใช้จริงในลูป dispatch: `ack = scene_load_scenario.action_ack if scene_load_scenario is not None else None` แล้ว `fields = parse_scene006_ea7d(legacy, parsed, ack)` ตามด้วย `make_scene007_action_ack(...)` — **นี่คือความต่างสำคัญจาก `TeleportCheckVital` ที่ draft แรกอ้างถูกต้องว่ามี 0 hit ใน `runtime.py`** ตัวนี้มี hit จริง สายนี้ต่อจริง เพียงแต่มีเงื่อนไข gate (ดูข้อ 2)

## 2) การเดินสายอยู่หลังแฟล็ก ไม่ใช่เส้นทางไร้แฟล็ก

`ack = scene_load_scenario.action_ack if scene_load_scenario is not None else None` (`runtime.py:6483`) ผูกกับ `scene_load_scenario` ซึ่งมาจาก `app.py:287-288`: `load_scene_load_scenario(known.scene_load_scenario) if known.scene_load_scenario else None` และ `known.scene_load_scenario` มาจาก CLI flag `--scene-load-scenario` (`app.py:98`, `pre.add_argument('--scene-load-scenario')`) **บูตปกติไร้แฟล็กไม่มี `scene_load_scenario` ⇒ `ack is None` ⇒ กิ่งนี้ไม่ถูกแตะเลย** — ตรงกับกฎบทที่ 1 ของ charter สายนี้ ("เลนที่เขียนต้องทำงานโดยไม่ต้องมีแฟล็ก มิฉะนั้นเป็นแค่ probe") **แต่โมดูลนี้อยู่นอกขอบเขตของสายนี้** (ดูหัวข้อ 4)

## 3) หลักฐาน client-observable สองชุด — ค่าต่างกันจริง แต่คนละ session

- `reports/PF_SCENE006_EA7D_ATTACK_COMMAND_RUNTIME_PASS_20260815.md:21`: *"scene 2 and finite heading/XYZ"* — แคปเจอร์จากไคลเอนต์จริง ไม่ใช่ Port Royal
- `reports/PF_SCENE007_PORT_ROYAL_EA7D_ACTION_ACK_RUNTIME_PASS_20260816.md:13,27-28`: *"the persisted player starts at exact V74 scene-1 position"* ... *"preserves target `0x203D`, action `0xEA7D`, heading, XYZ, scene 1 and the remaining exact fields"* — แคปเจอร์จาก Port Royal (ฉาก 1)

ทั้งสองค่าตรงกับฉากจริงของแต่ละ session **แต่เป็นคนละ session คนละบูต** ไม่ใช่หนึ่ง session ที่เดินข้ามฉากแล้ววัดว่าค่าขยับตาม — จึงแยกไม่ออกระหว่างสองสมมติฐาน: (A) ไคลเอนต์เขียนฉากปัจจุบันจริงลงฟิลด์นี้ทุกครั้งที่ส่ง `ActionVital` (ถ้าจริง = สัญญาณยืนยันฉากที่หาอยู่) กับ (B) ค่านี้ถูก bake ไว้ใน scenario/producer ของแต่ละการทดลองที่ต่างกันโดยบังเอิญตรงกับฉากจริงของมันเอง (ถ้าจริง = ไม่ใช่สัญญาณอะไรเลย เป็นเรื่องบังเอิญของการตั้งค่าเทส) **ไม่มีใครเคยรันการทดลองที่แยกสองข้อนี้ออกจากกัน** (ประเด็นที่ `pf-adversary` เปิดไว้ ยังไม่มีใครตอบ)

## 4) ทำไม `RE-156` ยังตอบได้ (บางส่วน) โดยไม่ต้องแก้โค้ด และทำไมสายนี้ไม่ใช่คนแก้

`action_ack.py`/`parse_scene006_ea7d`/`make_scene007_action_ack` เป็นของโดเมน **combat** ไม่ใช่ world: `docs/FUNCTIONAL_COVERAGE.json`'s `combat` domain อ้างมันตรงๆ ในสามความสามารถ (`attack_command_producer`, `action_acknowledgement`, `hostile_relation_and_target_selection`) และคอมเมนต์ในไฟล์เองปักไว้ว่า `# PF-HYPOTHESIS-LEDGER: HYP-PF-002 frozen` — เป็นสมมติฐานที่แช่แข็งแล้ว ไม่ใช่ของที่สายนี้ (WORLD) เป็นเจ้าของหรืออยู่ใน write zone ของสายนี้ **สายนี้จึงไม่แก้/ไม่ต่อสาย/ไม่เสนอ CORE-REQUEST ให้พลิกแฟล็กนี้** — เป็นการค้นพบที่ต้องส่งต่อให้ทีมที่ดูแล combat/HYP-PF-002 ตัดสินใจ (ดูใบ STATUS คู่กัน)

สิ่งที่ตอบได้จริงจากซอร์สที่ commit แล้วสำหรับ objective ของ `RE-156`:
- **ข้อ 1**: มี byte ที่ถูกตั้งชื่อ/ใช้เป็น scene id จริงในระบบนี้ — `field_u16_4a` ของ `ActionVital`, ผูกความหมายโดย `action_ack.py:8-11,63`, เดินสายจริงที่ `runtime.py:247,6483-6501`, มีแคปเจอร์จริงสองชุดที่ค่าต่างกันตรงกับฉากที่ต่างกัน (ข้อ 3)
- **ข้อ 2 (permanent limitation หรือ proxy ที่ใกล้ที่สุด)**: ไม่ต้องใช้ข้อนี้แล้วสำหรับ field นี้ เพราะข้อ 1 มีคำตอบบวกแล้ว — แต่ **ยังไม่ใช่สัญญาณยืนยันฉากที่ใช้งานได้จริงวันนี้** ด้วยสามข้อจำกัด: (i) อยู่หลังแฟล็ก opt-in ไม่ใช่บูตปกติ, (ii) ไม่เคยพิสูจน์ live-tracking (หัวข้อ 3), (iii) อยู่นอกโดเมนของคำถามเดิม (combat ไม่ใช่ world/travel) `TeleportCheckVital` และ `TargetPosVital` ยังยืนตามที่ draft แรกอธิบายไว้ถูกต้อง (0 hit ใน `runtime.py` สำหรับตัวแรก, ไม่มีฟิลด์ฉากเลยสำหรับตัวหลัง) — สองย่อหน้านั้นของ draft แรกไม่ถูกถอน มีแค่หัวเรื่องใหญ่ที่ถูกถอน

## nonclaims

1. ไม่อ้างว่า `field_u16_4a` พิสูจน์แล้วว่าติดตามฉากปัจจุบันแบบสด — สองแคปเจอร์เป็นคนละ session, ไม่ใช่การข้ามฉากในหนึ่ง session (สมมติฐาน A vs B ในหัวข้อ 3 ยังแยกไม่ออก)
2. ไม่อ้างว่านี่คือสัญญาณยืนยันฉากที่ใช้งานได้จริงในบูตปกติวันนี้ — มันอยู่หลัง `--scene-load-scenario` เท่านั้น
3. ไม่อ้างว่าสายนี้ (WORLD) มีสิทธิ์หรือแผนจะแก้ `action_ack.py`/`runtime.py`'s combat dispatch — อยู่นอก write zone และนอกโดเมนของสายนี้ ทั้งยังเป็น `HYP-PF-002 frozen`
4. ไม่ถอนคำตอบของ draft แรกเรื่อง `TeleportCheckVital` (0 hit ใน `runtime.py`, ค่าคงที่ 1 ไม่เคยพิสูจน์ว่าผัน) และ `TargetPosVital`/`GetWorldInfoVital` (ไม่มีฟิลด์ฉาก) — ยังยืนถูกต้อง มีแค่หัวข้อสรุปที่เปลี่ยนจาก "ไม่มีอะไรเลย" เป็น "มีผู้สมัครหนึ่งตัว นอกโดเมนคำถามเดิม ยังพิสูจน์ไม่ครบ"
5. ไม่แก้โค้ดในใบนี้ — zero diff ยืนยันแล้วใน `src/ tools/ current/ tests/` ก่อนและหลังการแก้ไขใบนี้

## BUILD_IMPACT

`BUILD_IMPACT_NONE: 1/1` จากสายนี้ (WORLD) — ไม่มีงานเดินสายให้ทำในขอบเขตของสายนี้ การพิจารณาว่าจะพลิกแฟล็ก `--scene-load-scenario` ของ `action_ack.py` ให้ default-on หรือไม่เป็นเรื่องของทีม/สายที่ดูแล combat + `HYP-PF-002` และควรรอผลการทดลอง live-tracking ก่อน (ดู `GT-158` ที่เปิดใหม่ในใบนี้)

## สถานะที่ควรกรอก (แก้จาก draft แรก)

~~`RE-156 DONE/BOUNDED-NEGATIVE`~~ →
**`RE-156 DONE (wire/DB layer) / POSITIVE-CANDIDATE-OUT-OF-DOMAIN-AND-UNVERIFIED-LIVE-TRACKING`** —
ตอบ objective ข้อ 1/2 ครบด้วยเลขบรรทัดตามที่ใบสั่ง (ไม่ต้องแก้โค้ด) ชั้น client-observable
(ไคลเอนต์จริงติดตามฉากแบบสดหรือไม่) แยกไปที่ `GT-158` ใหม่ตามกติกาสองชั้นของใบนี้เอง

— LANE-A (WORLD), แก้ไขหลัง `pf-adversary` พบข้อผิดพลาด CRITICAL ในฉบับร่างก่อนคอมมิต — ขอบคุณสำหรับการตรวจ
