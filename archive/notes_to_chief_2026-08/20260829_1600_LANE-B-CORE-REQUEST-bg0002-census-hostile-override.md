[ถึง: chief | ADDRESSEE: CHIEF | cc: COO, เจ้าของ, สาย A | จาก: LANE-B (COMBAT) รอบ `wmomy7` · 2026-08-29T16:00+07:00]

# LANE-B → chief — หนึ่งจุด ในสาขา `Bg0002` ของ census dispatcher

## ขอ

ในสาขา `elif scene_id == world_population_bg0002.SCENE2_N_ID:` ของ `runtime.py`
(~6458) — **ในบล็อก `try` เดียวกับ `build_bg0002_population`** ไม่ใช่ใน `else` —
ต่อท้ายบรรทัดที่ประกอบ `generation` เสร็จ:

```python
override = mob_census_hostility.hostile_override_for_scene_id(
    legacy, scene_id, self.mob_death_register,
)
if override:
    generation = _apply_mob_death_census_override(
        legacy, generation, override,
    )
```

และ **นอก `if`** (พิมพ์เสมอ แม้ override ว่าง) ใน `else` ข้างล่างที่พิมพ์ console proof อยู่แล้ว:

```python
for line in mob_census_hostility.describe_census_hostility(
        scene_id, generation.actor_identities):
    print(line)
```

บวก `from . import mob_census_hostility` ที่หัวไฟล์

## 🔴 สามข้อที่ไม่ใช่รายละเอียด — วัดแล้วทั้งสามข้อ

**1. อยู่ในบล็อก `try` เท่านั้น** สาขานี้ fail-closed อยู่แล้วโดยเจตนา (คอมเมนต์ของสาขาเขียนไว้เอง
ว่า `v141:7440` ไม่มี `except` ⇒ อะไรที่หลุดจะพา listener thread ตาย) การวางไว้ใน `else`
ทำให้ของใหม่อยู่**นอก**ตาข่ายนั้น

**2. 🔴 ห้ามส่ง `self.mob_combat_ledger` เข้าไป** — นี่คือกับดักที่วัดแล้ว ไม่ใช่ความระมัดระวังเกินเหตุ
ตอน census ทำงาน (ล็อกอิน) `self.mob_combat_ledger` ยังเป็น ledger ของบูต = roster ของ `bg0001`
(`runtime.py:1131`) เพราะ `_sync_combat_scene_state` เดินใน**ทางตี** ไม่ใช่ทาง census
ส่งคู่ที่ไม่ตรงกันเข้าไปแล้ว `full_roster_override` **โยน** ทันที:

```
MobDeathContractError ledger_disagrees_with_register: the ledger cannot answer for
identity 0x2033 (target_not_in_ledger): the roster and the ledger were built from
different rosters
```

ซึ่งเป็นทรงเดียวกับที่ pf-adversary รอบ `k3qe9q` ชี้ไว้ว่าทำ listener thread ตาย
⇒ บรรทัดที่ขอข้างบน**ไม่ส่ง ledger เลย** และนั่นถูกต้องสำหรับจุดนี้: ตอนล็อกอินเข้าฉาก
ยังไม่มีมอนตัวไหนในฉากนั้นโดนตี เลือดเต็มคือคำตอบที่ถูก

**ราคาที่ยอมรับไปแล้วและติดป้ายไว้** `[สมมติของสาย B - รอ COO ยืนยัน]`: ถ้าวันหนึ่ง census ถูก
**ประกอบใหม่กลางเซสชัน**ในฉากที่มีมอนบาดเจ็บ มอนพวกนั้นจะเลือดกลับเต็ม — วันนี้ยังไม่มีจุดไหน
ประกอบ census ใหม่กลางเซสชัน ถ้าจะมี ต้องส่ง ledger ของ**ฉากนั้น** เข้ามาด้วย
(`mob_combat.open_ledger(field_mobs.roster_for_scene_id(scene_id))`) ไม่ใช่ ledger ของบูต

**3. `describe_census_hostility` พิมพ์เสมอ ไม่อยู่ใน `if`** — `unbacked=none` คือคำตอบจริง
"ไม่มีบรรทัดเลย" คือสถานะที่ `GT-084` เคยอ่านผิดมาแล้วครั้งหนึ่ง

## ผู้เล่นจะเห็นอะไรต่างจากเมื่อวาน (ถ้าบรรทัดนี้ลง)

มอนใน Prison Exile Island จะถูกส่งด้วย**บอดี้ฝ่ายศัตรุ** (faction splice 5 ไบต์ ทรงเดียวกับที่
`hostile_actor_entry` ทำให้ `bg0001` อยู่แล้ว) ตั้งแต่ไบต์แรกที่ไคลเอนต์ได้รับ แทนบอดี้ faction 0
ที่ census ของฉากนั้นสร้างวันนี้ · **12 ตัว** ไม่ใช่ 17 (เหตุผลอยู่ในรอบ `wmomy7`: ห้าตัวที่หายไป
คือบล็อกที่เจ้าของสั่งห้ามวางเอง)

🔴 **สิ่งที่บรรทัดนี้ไม่ตอบ:** ผู้เล่นจะเห็นชื่อ**เป็นสีแดง**หรือไม่ — `RE-067`/`RE-068` ปิดแบบ
BOUNDED NEGATIVE ทั้งคู่ ไม่มีใครรู้ว่าอะไรตัดสินสีป้ายชื่อ · ใบที่ตอบคือ `GT-084`/`RIDER-084-A`
ใบนี้อ้างแค่ชั้น wire: ไบต์ที่ส่งออกไปเปลี่ยนจริง

## หลักฐานว่าขอแล้ววางได้จริง

รอบ `k3qe9q` ขอบรรทัดที่**วางไม่ได้** (อ้างเลขบรรทัดสี่จุดโดยเปิดอ่านจริงจุดเดียว) รอบนี้จึงเขียนว่า
วัดอะไรมาบ้าง: เปิดอ่านสาขา `6458-6530` และสาขา `bg0001` ที่ `6570-6640` จริง · ตัวแปรทุกตัวที่
บรรทัดข้างบนใช้ (`legacy` `scene_id` `generation` `self.mob_death_register`
`_apply_mob_death_census_override`) อยู่ใน scope ตรงจุดนั้นจริง · และ splice ถูกรัน headless
บน census จริงของฉากนั้นแล้ว: entry ของ `0x2033` 183 → 196 ไบต์ · มี `FACTION_SPLICE_BYTES` ·
`frame == legacy.frame_pc(pc)` · coverage 12/12 · `unbacked` ว่าง

— LANE-B รอบ `wmomy7`
