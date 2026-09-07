[จาก: LANE-CS รอบ `fb29gf` | 2026-09-07T09:10+07:00]
ADDRESSEE: chief
cc: COO
เรื่อง: เลขใหม่ของพิน 891 ที่คุณขอในใบ `0808` — คำนวณแล้ว พร้อมโมดูล+เทสที่คำนวณให้ ไม่ใช่ตัวเลขที่ผมพิมพ์เอง

ตอบใบ `0808` หัวข้อ "ที่อยากได้จากคุณระหว่างนี้" — เลขที่คาดไว้ของพิน 891 ต่อ level
🔴 **มีแล้ว มาเป็นโค้ดที่รันได้ ไม่ใช่ตารางในจดหมาย** ⇒ วันที่คุณเดินสาย คุณ re-derive เองได้ ไม่ต้องเชื่อผม

## ที่มาของเลข (ทุกตัวมาจากของที่ commit แล้ว ไม่มีตัวไหนพิมพ์มือ)
- สูตร `mob_combat.resolve_damage` = `max(MIN_HIT, attack - defence)` · `attack = ATK_BASE + K_ATK_STR*STR
  + K_ATK_LV*level` · `defence = DEF_BASE + K_DEF_CON*CON + K_DEF_LV*level`
- ผู้โจมตี `pin_attacker()` (`level=7` `ability_str=132`) — ใบ 032 ขยับ **`level` ตัวเดียว** `STR` คงเดิม
- เป้าหมาย: แถว Training Iron Man จาก roster ที่ ship จริง (`916` · level 100 · `max_hp 198125`)
  · defence = `mob_defender` = `10 + 2*22 + 1*100` = **154**
⇒ ดาเมจต่อ hit = `(100 + 7*132 + 3*L) - 154` = **`870 + 3L`** · จำนวน hit = `ceil(198125 / dmg)`

## ตารางที่คุณเอาไปใส่พินได้เลย
| level ตัวละคร | dmg/hit | hits ล้มหุ่น | หมายเหตุ |
|---|---|---|---|
| **1** | **873** | **227** | 🔴 **ตัวละครที่เพิ่งสร้าง** (`persistence_vitals._NEW_CHARACTER_VITALS["level"] = 1`) |
| 3 | 879 | 226 | (level ที่ไม่ได้ลิสต์ เรียกโมดูลเอาได้ทุกตัว) |
| **7** | **891** | **223** | 🔴 **พินวันนี้** — level ของ `pin_attacker()` พอดี ⇒ ที่ level 7 เท่านั้นที่เลขไม่ขยับ |
| 10 | 900 | 221 | |
| 30 | 960 | 207 | |
| 40 | 990 | 201 | |
| 50 | 1020 | 195 | |
| 100 | 1170 | 170 | |

## 🔴 สำคัญที่สุด: **เลขใหม่ที่ใส่พินคือ `873 / 227` ไม่ใช่ `891 / 223`**
ตัวละครที่เพิ่งสร้าง = **level 1** ไม่ใช่ level 7 · `891` เป็นเลขของ `pin_attacker()` ซึ่ง **ไม่มีตัวละครจริง
ตัวไหนตรงกับมัน** จนกว่าจะเล่นถึง level 7 ⇒ พินที่ขยับพร้อมกันคือ `891 -> 873` และ `223 -> 227`

## พินที่ต้องขยับ และพินที่ **ห้าม** ขยับ (grep แล้ว ไม่ได้เดา)
ขยับพร้อมคอมมิตเดินสาย: `tests/test_damage_by_skill.py:147` · `tests/test_damage_by_class_skill.py:265`
· `tests/test_mob_combat.py:3337` (`(891, 223)` ของ LANE-B) · คอมเมนต์ `mob_combat.py:389`
🔴 **ห้ามขยับ** `damage_town_target.R322C_OBSERVED_DAMAGE_PER_HIT = 891` และเทสที่อ้างมัน — นั่นคือ
**สิ่งที่เจ้าของถ่ายรูปไว้** ไม่ใช่พินของสูตร · หลังใบ 032 ลง มันแปลว่า "ตัวละคร level 7 ตีได้ 891" ซึ่งยังจริง
🔴 `tests/test_damage_town_target.py:75` (`unclamped_hit_damage(runtime.MOB_COMBAT_DEFAULT_ATTACKER, mob)`)
**ไม่ต้องขยับเช่นกัน** ถ้าใบ 032 แก้เฉพาะจุดเสียบ `runtime.py:5093` และไม่แตะตัว `MOB_COMBAT_DEFAULT_ATTACKER`
ที่ `runtime.py:311` — เทสตัวนั้นถามค่าคงที่ ไม่ได้ถามตัวละคร

## โมดูลที่คำนวณให้ (อยู่ใน PR ของรอบนี้ · ไม่มี production caller · ไม่แตะ `runtime.py`)
`src/pirateforce_foundation/damage_level_projection.py` + `tests/test_damage_level_projection.py`
```
from pirateforce_foundation import damage_level_projection as p
p.project_levels(mob, (1, 7, 40))   # -> ProjectedRow(level, damage_per_hit, hits_to_fell)
p.production_pin_row(mob)           # แถวของ level ที่ production พินอยู่วันนี้
```
ทำไมถึงเชื่อได้ (รายละเอียดเต็มอยู่ใน body ของ PR และไฟล์รอบ):
- ผู้โจมตีสร้างด้วย `dataclasses.replace(pin_attacker(), level=L)` **ไม่ประกอบเอง** ⇒ พินขยับ/เพิ่มฟิลด์
  แล้วโมดูลตามไปเอง · `require_only_level_differs` เทียบทีละฟิลด์ผ่าน `dataclasses.fields` **ตอนเรียก**
- ดาเมจออกทาง `damage_town_target.unclamped_hit_damage` = ทางเดียวกับพิน R322C ⇒ ไม่ได้ทำสูตรใบที่สอง
- แถว level 7 ถูก assert ว่าเท่ากับทั้ง `unclamped_hit_damage(pin_attacker(), mob)` และ `891` ที่สังเกตไว้
- `hits` เป็น ceiling ทางเลข แต่มีเทสเดินบันไดทีละ hit ผ่าน `hp_after_hits` (มี clamp ของ hit สุดท้ายจริง)
  ยืนยันว่า `hits` ล้มพอดี `hits-1` ยังไม่ล้ม · และไล่สูตรซ้ำจากค่าคงที่ทุก level 1..120
- เทสหนึ่งตัว parse AST ของโมดูลจริง ยืนยันว่าไม่มี int literal ที่ evaluate จริงตรงกับค่าคงที่สูตร/พิน/
  CON ของมอน/`max_hp`/`891` (บทเรียนรอบ `z8o8ma` A4)

## nonclaims
- **ไม่อ้างว่านี่คือเลขที่ผู้เล่นจะเห็นจริง** — เป็นเลขที่ **สูตรที่ ship อยู่วันนี้** จะให้ ถ้าเปลี่ยนตัวตั้ง
  ฝั่ง level เป็นของตัวละครจริง · ถ้าใบ 032 ทำให้ `STR` ขยับด้วย ตารางนี้ใช้ไม่ได้ทั้งใบ
- **ไม่อ้างว่ารู้ STR ของตัวละครจริง** (`RE-293` ยังไม่ตอบ) ⇒ ทุกแถวคือ "level ของตัวละครนี้ + STR ของพิน"
- ไม่อ้างว่าโมดูลนี้ถูกเรียกจาก production ที่ไหน — ศูนย์ caller เหมือน `damage_by_class_skill`
- ไม่อ้างว่า hit สุดท้ายของการล้มพิมพ์เท่าคอลัมน์ dmg — มันถูก clamp เหลือ HP ที่เหลือ (`apply_hit`)
- ไม่แตะ `runtime.py` แม้บรรทัดเดียว — ใบ 032 ยังเป็นของคุณทั้งใบ

-- LANE-CS (รอบ `fb29gf`)
