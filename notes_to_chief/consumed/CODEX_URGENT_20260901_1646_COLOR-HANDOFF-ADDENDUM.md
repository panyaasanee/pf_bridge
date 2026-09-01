[ถึง: chief, LANE-GM, COO, Panya | จาก: Codex static RE | 2026-09-01 16:46 +07:00]

# Addendum — P0-2 relation/style mechanism และ bounded wire/control handoff

ใบนี้ **เพิ่มต่อโดยไม่แก้ทับ** `CODEX_URGENT_20260901_1627_COLOR-RELATION-CORRECTION.md`
และมีอำนาจเหนือถ้อยคำใดในใบนั้นที่อาจอ่านเป็น causal closure.

## คำตัดสินที่แก้ให้ตรงชั้นหลักฐาน

- `[MEASURED][IMAGE]` FACTION loader/comparator, relation fallback และ edge เข้า selector/controller
  เป็นกลไกเส้นเดียวกัน ไม่ใช่ renderer ตัวที่สอง.
- `[MEASURED][DATA]` FACTION row 1 มี target 6; palette แยกชั้นให้ Style56 เป็น
  `(255,62,255,255)`.
- `[COMPOSITION][IMAGE+DATA]` `(local=1,target=6)` + execution ถึง FACTION fallback +
  signed-positive identity + selector/controller gates เป็น **คำอธิบายแบบมีเงื่อนไขที่เพียงพอ**
  ให้ request Style56 เท่านั้น. มัน **ไม่ใช่สาเหตุที่วัดแล้วของ SCENE-005** เพราะรอบนั้นไม่ได้ trace
  earlier exits, fallback result, requested ID หรือ applied ID.
- `[OPEN][RUNTIME]` causal explanation ของ SCENE-005 จะปิดได้เมื่อ trace actor ตัวเดียวกันครบ
  relation branch/result -> requested ID -> controller applied ID -> UILabel style -> pixels.
- `[MEASURED][IMAGE][BOUNDED][OPEN]` ไม่พบ direct style wire ในขอบเขต literal-immediate,
  direct-E8 sinks และ typed paths ที่ audit นี้ แต่ whole-program direct/dynamic/embedded/custom/alias
  question ยัง `OPEN`; ห้ามแปลเป็น global negative.

## Artifact identity

1. `pf_bridge/external/PF_MONSTER_COLOR_MECHANISM_JOIN.tsv`
   - 13,134 B · SHA-256 `dfaf5f31380c3ce6a0cfffd6b8778e1a28154b6438f5f404067b402c3d324190`
   - 8 rows = IMAGE 6 / DATA 2
   - pair generation `40bee0ae06ec8fd710b768b25e029b775cd7eb157f8e75f3047900ff81e14ccc`
2. `pf_bridge/external/PF_MONSTER_COLOR_MECHANISM_JOIN.md`
   - 8,372 B · SHA-256 `2b4125f6387f82f3d8af173136ac018c354eefba22bfcd0af2e1a2314d84534d`
3. `pf_bridge/external/pf_rederive_monster_color_mechanism_join.py`
   - 67,594 B · SHA-256 `14aaee83970f58ca5774e32c3bf561e6cfce97b15a5e81de5110564bb0699b28`
4. `pf_bridge/external/PF_MONSTER_COLOR_WIRE_CONTROL.tsv`
   - 27,191 B · SHA-256 `8fbffa366c495e323a9c87dc443316b1b2352a534b2bd47a97c2766361cae70d`
   - 15 rows = IMAGE 15; final direct-style-wire conclusion=`OPEN`
   - pair generation `6e2041061bc42b44934fd309059eb4177b136714d30e2b5eec5a5c8061d80cc7`
5. `pf_bridge/external/PF_MONSTER_COLOR_WIRE_CONTROL.md`
   - 6,473 B · SHA-256 `b596e71d41cb3efcf9e84b74eea5affedc174429baf8e81a8846e61930738849`
6. `pf_bridge/external/pf_rederive_monster_color_wire_control.py`
   - 71,641 B · SHA-256 `bee56a4a2073a8152651ba083ffa725af46838a4115c9b4149c6b159956dc1ad`

Canonical downstream authority ยังคงเป็น `PF_MONSTER_COLOR_GATE.tsv` 66 rows = IMAGE 58 / DATA 8;
สองชุดใหม่มี claim ownership แคบกว่าและอ้าง prior keys แทนการคัดแถวมานับซ้ำ.

## Verification / delivery boundary

- Root รัน `--check` ของ color gate, mechanism join และ wire/control ผ่านทั้งหมด.
- IMAGE ก่อน/หลังยัง 14,759,424 B และ SHA-256
  `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`.
- Main Attr generation ยัง `b96e420c290201ce60babec398fd2389ea36db2f2f30ce552d9d680f481f3fae`;
  field/status/scope/UNKNOWN delta = 0.
- Artifacts อยู่ `pf_bridge/external` นอก canonical ServerProject Git worktree และไม่ได้ถูก track
  ใน worktree นั้น. Claude บนเครื่องเดียวกันอ่านได้; clone/เครื่องอื่นต้องใช้ owner-approved
  packaging/ingest ตาม `PF_CRITICAL_ARTIFACT_AUTHORITY.json`.
- ไม่มี raw proprietary bytes ถูกคัดลงผลลัพธ์.

## ผลต่อการตัดสินใจ

ห้าม faction-only fix, ห้าม hardcode direct style field และห้ามเรียก P0-2 ว่าปิดบนจอ. สิ่งที่พร้อมคือ
bounded upstream experiment ภายใต้ session+scene+generation identity invariants และ stop rules
62/ส้ม -> 61/แดง -> 63/เทา. การลงมือยังผ่าน chief/COO ตามคิวปกติ; ใบนี้ไม่ใช่คำสั่งแก้ระบบ.

