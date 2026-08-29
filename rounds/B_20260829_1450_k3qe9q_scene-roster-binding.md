# LANE-B รอบ `k3qe9q` — ฉากที่ผู้เล่นยืนอยู่ เป็นตัวตัดสินว่ามอนตัวไหนตีได้

เปิดรอบ 2026-08-29T14:31+07:00 · เขียน 14:50+07:00
repo: `pirate-force-server` PR #263 · `pf_bridge` PR #413
สาขา: `claude/funny-volta-k3qe9q` · `claude/affectionate-bardeen-k3qe9q`

## ผู้เล่นจะเห็นอะไรต่างจากเมื่อวาน

🔴 **ยังไม่เห็น จนกว่าบรรทัดของ chief จะลง — และรอบนี้ไม่อ้างว่าเห็นแล้ว**

สิ่งที่เปลี่ยนจริงและวัดได้: **กำแพงที่ทำให้ `GT-132` บูตไปก็ได้ `NO-RESULT` เสมอ เหลือครึ่งเดียว**
เมื่อวานสองครึ่งของกำแพงนั้นไม่มีเจ้าของทั้งคู่ วันนี้ครึ่งของสาย B ส่งครบและวัดผลแล้ว
ที่เหลือคือสองบรรทัดในไฟล์ที่ไม่ใช่ของสายนี้ — และมันเป็นบรรทัดที่**วางได้ทันทีโดยไม่เปลี่ยนอะไรเลย**
สำหรับฉากที่เซิร์ฟเวอร์รันอยู่จริงวันนี้ (พิสูจน์เป็นตัวคุม ไม่ใช่คำรับรอง)

## ① ข้อ A ของ ADDENDUM v2 — ชะตา PR รอบก่อน (`0n9inw`)

| repo | PR รอบก่อน | ผล |
|---|---|---|
| `pirate-force-server` | `#260` | ✅ merged `2026-08-29T07:19:03Z` |
| `pf_bridge` | `#410` + `#411` | ✅ merged `07:13:46Z` / `07:17:37Z` |

⇒ งานรอบก่อน (per-drop expiry) อยู่บน main จริง ไม่มีอะไรต้องกู้
ยืนยันจาก API ไม่ใช่จาก `rounds/` — ตามที่ข้อ A สั่งไว้เป๊ะ

## ② ข้อ B — กล่องจดหมาย

**บริโภคหนึ่งใบ:** `FROM_CHIEF_R226_TO_ATTENDED_20260829_1325.md`
เขียนถึงผู้เทส แต่รายงานสถานะใบที่**สาย B เปิดสามใบ** (`GT-146` `GT-142` `GT-132`) จึงบริโภคที่นี่
วาง stub + สำเนาไป `consumed/` ครบ · ไม่ลบต้นฉบับ · ข้อ 3 ของใบนั้นคือที่มาของงานรอบนี้ทั้งรอบ

**ไม่มีใบอื่นที่ถึงสายนี้ค้างอยู่** — ใบ `ASK-COO` ของสายนี้ที่ยังไม่มีคำตอบมีสองใบ
(`20260829_1347` เรื่องอายุของตก · `20260829_0353` เรื่องกฎด่าน 2) ทั้งคู่**ไม่ได้บล็อกรอบนี้**
และตามหลักการ "เขียนคำถาม แล้วเดินต่อ" รอบนี้ก็ไม่ได้รอ

## ③ ที่ ship — ครึ่งของสาย B ที่รอบ `j0u64p` ระบุว่ายังไม่มีเจ้าของ

รอบ `j0u64p` วัดไว้ว่าผู้เล่นที่ยืนใน `Bg0002` **ตีอะไรไม่ติดเลยสักตัว**: `runtime.py` ประกอบ ledger
ด้วย `field_mobs.load_roster()` ไม่มีอาร์กิวเมนต์ ⇒ แถวของ `bg0001` เสมอทุกฉาก ⇒ `strike` ปฏิเสธ
มอนทุกตัวที่ยืนอยู่ตรงหน้าด้วย `target_not_in_ledger` **ก่อนที่ด่านการตายจะถูกถามด้วยซ้ำ**
รอบนั้นขอสามบรรทัด แต่บรรทัดที่ 2 **ไม่มีเจ้าของ** เพราะไม่มีตัวแปลง `scene_id` → ชื่อฉากในรีโป

ตอนนี้มีแล้ว สาย A ลง `world_scene_folder` (ตัวอ่านสาธารณะตัวเดียว · COO-DECISION 0848 ข้อ 3)
⇒ ครึ่งที่ขาดคือของสายนี้ และรอบนี้ส่งครบ:

ที่ `src/pirateforce_foundation/field_mobs.py` และ `mob_combat.py` (ไม่มีแฟล็ก · `production_allowed = True`):

- `field_mobs.scene_for_scene_id(scene_id)` / `roster_for_scene_id(scene_id)`
- `mob_combat.open_ledger_for_scene_id(scene_id)` — ทรงที่ทำให้จุดเรียกเหลือ**บรรทัดเดียว**
- `field_mobs.assert_live_scenes_are_addressable()` / `scene_ids_addressing(scene)` — ยามของ join
- `field_mobs.describe_scene_roster_binding(scene_id)` — G-OBS หนึ่งบรรทัด ASCII
  🔴 **คืนบรรทัด ยังไม่มีใครพิมพ์** (ผู้พิมพ์คือ `runtime.py`)

### สามการตัดสินใจที่เป็นแกน ไม่ใช่รายละเอียด

🔴 **1. เทียบชื่อฉากแบบตรงตัว ไม่ case-fold** — ชื่อโฟลเดอร์ของไคลเอนต์ตัวพิมพ์ไม่สม่ำเสมอจริง ๆ
(ฉาก 1 = `bg0001` · ฉาก 2 = `Bg0002`) และโมดูลตารางของเราถือสองสะกดนั้นตรงตัว
การ case-fold จะเป็น**กฎสะกดใบที่สอง**อยู่ข้างกฎของสาย A และจะกลบเคสที่แพงกว่าเคสที่มันช่วย:
โมดูลตารางใหม่ที่สะกดเพี้ยนจะ "ผ่าน" เงียบ ๆ แทนที่จะถูกจับ ⇒ จับด้วยยามแทน (ข้อ 3)

🔴 **2. ฉากที่ไม่มี roster เปิด ledger ว่าง ไม่ใช่ ledger ของ `bg0001`** — `()` ไม่ใช่ `None`
จึงถึง `open_ledger` ในฐานะ roster ว่างจริง ไม่ใช่ "ใช้ค่าตั้งต้น"
**"เมืองคือที่ที่ไม่มีอะไรให้ตี" ไม่ใช่ "ที่ที่ตีมอน `bg0001` ทะลุพื้นได้"** — และการอ่าน `()` ว่า
"ถอยไปใช้ roster ตั้งต้น" **คือดีเฟกต์ของวันนี้เป๊ะ ๆ** หนึ่งชั้นลงไป จึงเขียนห้ามไว้ใน docstring ทั้งสองตัว

🔴 **3. ยามของ join ที่ล้มเงียบ** — `scene_for_scene_id` คือ join ระหว่างตารางของสองสาย
(`_SCENE_TABLE_MODULES` ของเรา กับทะเบียนฉากของสาย A) และ join แบบนี้**ล้มเงียบในทิศที่แพงที่สุด**:
ฉาก live ที่ไม่มี scene id ไหนชี้ถึง จะคืน `()` ทุกฉาก = มอนหายทั้งฉาก โดยไม่มีอะไร raise ไม่มีอะไรพิมพ์
⇒ `assert_live_scenes_are_addressable()` ทำให้เคสนั้นล้มในสวีตแทนที่จะล้มบนจอผู้เล่น
**และเทสของยามนั้นทำ join พังเองแล้วบังคับให้ปฏิเสธ** เพราะยามที่ไม่เคยมีใครเห็นมันล้ม ไม่ใช่ยาม

## ④ หลักฐานสองชั้น

**ชั้น wire/DB — รันจริง headless มอนตัวเดียวกัน ก่อน/หลัง:**

```
subject : Tornado Eagle identity 0x2033 hp 3857 (scene Bg0002)

BEFORE (ledger ที่ runtime.py เปิดวันนี้ = open_ledger() ไม่มีอาร์กิวเมนต์)
  ledger holds : ['0x2068', '0x206a', '0x206c', '0x206e']
  strike       : REFUSED target_not_in_ledger (identity 0x2033 is not a monster this ledger opened)

AFTER (mob_combat.open_ledger_for_scene_id(2))
  ledger holds : 17 rows, subject present = True
  hit 1        : damage 1024   hp   2833/3857  frames 2
  hit 2        : damage 1024   hp   1809/3857  frames 2
  hit 4        : damage 785    hp      0/3857  frames 1
  ruling_for   : 'PANYA-DECISION 2026-08-27T20:10+07:00 (ADDENDUM 20:18) widen-death-scope-bg0002'
  kill         : frames 2, corpse hold 700 ms

CONTROL ฉาก 17 (โปรเจกต์ไม่ได้ส่ง roster)   ledger 0 rows · strike REFUSED target_not_in_ledger
CONTROL ฉาก 1 เทียบกับวันนี้                open_ledger_for_scene_id(1) == open_ledger() : True
MOB_SCENE_ROSTER scene_id=1 folder=bg0001 live=1 mobs=4
MOB_SCENE_ROSTER scene_id=2 folder=Bg0002 live=1 mobs=17
MOB_SCENE_ROSTER scene_id=14 folder=Bg0015 live=0 mobs=0   (ขุดแล้วแต่ยัง dormant โดยเจตนา)
MOB_SCENE_ROSTER scene_id=17 folder=Bg1001 live=0 mobs=0
MOB_SCENE_ROSTER scene_id=999 folder=? live=0 mobs=0       (ทะเบียนสาย A ไม่ได้ระบุ)
```

บรรทัด `AFTER` คือ **BUILD-005 ทั้งใบ (ตีได้ · เลือดลด · ตายจริง · เป็นศพ) บนมอน `Bg0002`**
วัดที่ชั้น wire ครบ — สิ่งที่ยังขาดคือ**จุดเรียก** ไม่ใช่กลไก

สวีตเต็ม: **4707 ผ่าน · 327 skip · 8780 subtests** (ก่อนรอบนี้ 4650 ผ่าน) ไม่มีอะไรพัง

**ชั้น client-observable — 🔴 ไม่มี และรอบนี้ไม่อ้างว่ามี** ปิดโดย `GT-132` หลังบรรทัดของ chief ลง

## ⑤ pf-adversary

(เติมในข้อ ⑦ ท้ายไฟล์ — เขียนหลังผลจริงออก ไม่ได้เขียนล่วงหน้า)

## ⑥ ที่ขอจาก chief — สองบรรทัด และมันวางได้ทันที

`notes_to_chief/20260829_1445_LANE-B-CORE-REQUEST-scene-roster-binding-two-lines.md`

| # | ที่ | จาก | เป็น |
|---|---|---|---|
| 1 | `runtime.py:1119` | `mob_combat.open_ledger()` | `mob_combat.open_ledger_for_scene_id(<scene id ของ session>)` |
| 2 | `runtime.py:3911` (+1174 / 6486 ถ้าเป็นเส้นเดียวกัน) | `field_mobs.load_roster()` | `field_mobs.roster_for_scene_id(<scene id ของ session>)` |

🔴 **ข้อระวังข้อเดียว ที่รอบนี้วัดปลายทางมาให้แล้ว:** จุดที่อ่าน roster มี**สี่**จุด
(`1119` ledger · `1174` ai register · `3911` dispatch · `6486` census override)
เปลี่ยนบางจุดแล้วเหลือบางจุดเป็น `load_roster()` เปล่า = **census กับ ledger พูดคนละเรื่อง**
ในฉากที่ไม่ใช่ฉาก 1 ซึ่งเป็นทรงเดียวกับ world-wipe ที่ `GT-084` เจอ ⇒ ขอ **ทั้งสี่จุดพร้อมกัน หรือไม่เลย**
ปลายทางทั้งสามตัวรับ roster ว่างได้ ไม่มีตัวไหน raise (วัดแล้ว: `open_register(())` = 0 แถว ·
`full_roster_override(..., ())` = `dict` ว่าง ⇒ falsy ⇒ ข้าม override ⇒ census เดิมยืน)

วันนี้ทั้งกระบวนการ hardcode `population.SCENE_ID = 1` ⇒ **ส่ง `1` เข้าไปก่อนก็ได้ ไม่มีอะไรเปลี่ยน**
(ตัวคุมพิสูจน์แล้วว่าเท่ากันทุกค่า) ⇒ บรรทัดกับ "เลขฉากที่ถูกต้อง" **ไม่ต้องรอกัน**
บรรทัดที่ 3 ของรอบ `j0u64p` (`widened=mob_death.ruling_for(mob)` ~4171) **ยังค้างเหมือนเดิม ไม่ได้ยกเลิก**
