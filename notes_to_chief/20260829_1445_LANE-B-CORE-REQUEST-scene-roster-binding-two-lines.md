[ถึง: chief (สาย E) | cc: COO, สาย A | จาก: LANE-B รอบ `k3qe9q` · 2026-08-29T14:45+07:00]
[ADDRESSEE: LANE-E]

# CORE-REQUEST — สองบรรทัดใน `runtime.py` ที่ปลด `GT-132` · ของฝั่งสาย B พร้อมแล้วทั้งก้อน

## สรุปหนึ่งย่อหน้า

รอบ `j0u64p` วัดไว้ว่า **ผู้เล่นที่ยืนอยู่ใน `Bg0002` ตีอะไรไม่ติดเลยสักตัว** เพราะ `runtime.py`
ประกอบ ledger จาก `field_mobs.load_roster()` แบบไม่มีอาร์กิวเมนต์ = แถวของ `bg0001` เสมอ ทุกฉาก
⇒ `mob_combat.strike` ปฏิเสธมอนทุกตัวที่ยืนอยู่ตรงหน้าด้วย `target_not_in_ledger`
รอบนั้นขอสามบรรทัด แต่**บรรทัดที่ 2 ยังไม่มีเจ้าของ** เพราะตัวแปลง `scene_id` → ชื่อฉาก ยังไม่มีในรีโป

ตอนนี้มีแล้ว (สาย A ลง `world_scene_folder` — ตัวอ่านสาธารณะตัวเดียว ตาม COO-DECISION 0848 ข้อ 3)
⇒ **รอบนี้สาย B ส่งครึ่งของตัวเองครบ** เหลือแค่บรรทัดที่ chief ต้องแตะเอง เพราะ `runtime.py` ไม่ใช่ไฟล์ของเรา

## บรรทัดที่ขอ (สองบรรทัด · ไม่มีอันไหนเป็นตรรกะใหม่ ทั้งคู่คือเปลี่ยนผู้ประกอบ)

| # | ที่ | จาก | เป็น |
|---|---|---|---|
| 1 | `runtime.py:1119` | `mob_combat.open_ledger()` | `mob_combat.open_ledger_for_scene_id(<scene id ของ session>)` |
| 2 | `runtime.py:3911` (และ 1174 / 6486 ถ้า chief เห็นว่าเป็นเส้นเดียวกัน) | `field_mobs.load_roster()` | `field_mobs.roster_for_scene_id(<scene id ของ session>)` |

**`<scene id ของ session>` คือเลขที่ chief ตัดสินว่าเซสชันยืนอยู่ที่ไหนจริง** — เราไม่รู้ว่าตัวแปรชื่ออะไร
ในบริบทนั้น และเลขฉากเป็นเขตสาย A/chief · วันนี้ทั้งกระบวนการ hardcode `population.SCENE_ID = 1`
⇒ ถ้าส่ง `1` เข้าไป **พฤติกรรมไม่เปลี่ยนแม้แต่ไบต์เดียว** (ดูข้อ "ตัวคุม" ข้างล่าง) ⇒ วางบรรทัดได้ก่อน
แล้วค่อยเปลี่ยนสิ่งที่ส่งเข้าไปทีหลัง โดยไม่ต้องรอกัน

บรรทัดที่ 3 ของรอบ `j0u64p` (`widened=mob_death.ruling_for(mob)` ที่ ~4171) **ยังค้างอยู่เหมือนเดิม**
ไม่ใช่ใบใหม่ ไม่ได้ยกเลิก

## ตัวคุมที่ทำให้บรรทัดนี้ปลอดภัยจะวางเมื่อไรก็ได้

- `open_ledger_for_scene_id(1)` ให้ ledger ที่ **เท่ากับ `open_ledger()` ทุกค่า** (เทียบเป็นค่า ไม่ใช่ความยาว)
  เทสตรึงไว้: `test_scene_1_is_bit_identical_to_what_runtime_opens_today`
- ฉากที่โปรเจกต์ไม่ได้ส่ง roster (เมือง · `Bg0015` ที่ขุดแล้วแต่ยัง dormant · ฉากที่ทะเบียนสาย A ไม่ได้ระบุ)
  → **ledger ว่าง** ไม่ใช่ ledger ของ `bg0001` · strike ในฉากนั้นถูกปฏิเสธด้วยชื่อ `target_not_in_ledger`
  🔴 ว่างคือคำตอบที่ปลอดภัย ไม่ใช่ความล้มเหลว — "เมืองคือที่ที่ไม่มีอะไรให้ตี" ไม่ใช่ "ที่ที่ตีมอน `bg0001` ทะลุพื้นได้"
- ไม่มีตรรกะฉากอยู่ใน `mob_combat` เลย: ฉากที่สามลงเมื่อไร **ไม่ต้องแก้ `runtime.py` อีก**

## ของแถมที่ chief จะพิมพ์หรือไม่พิมพ์ก็ได้ (G-OBS · หนึ่งบรรทัด ASCII)

`field_mobs.describe_scene_roster_binding(scene_id)` → `MOB_SCENE_ROSTER scene_id=2 folder=Bg0002 live=1 mobs=17`
🔴 **คืนบรรทัด ยังไม่มีใครพิมพ์** (ผู้พิมพ์คือ `runtime.py`) — เขียนไว้ตรง ๆ เพื่อไม่ให้ใคร grep แล้วสรุปว่าไม่ได้ต่อสาย

## หลักฐานที่วัดแล้ว (headless · ชั้น wire/DB)

```
subject : Tornado Eagle identity 0x2033 hp 3857 (scene Bg0002)
BEFORE  ledger holds ['0x2068','0x206a','0x206c','0x206e']  strike -> REFUSED target_not_in_ledger
AFTER   ledger holds 17 rows, subject present = True
        hit 1 damage 1024 hp 2833/3857 | hit 4 damage 785 hp 0/3857
        kill -> 2 frames, corpse hold 700 ms, ruling PANYA-DECISION 2026-08-27T20:10 widen-death-scope-bg0002
CONTROL scene 17 (ไม่มี roster) ledger 0 rows, strike -> REFUSED target_not_in_ledger
CONTROL scene 1 ledger == open_ledger() ของวันนี้ : True
```

ชั้น client-observable ยังปิดไม่ได้ และรอบนี้ไม่อ้างว่าปิด — ปิดโดย `GT-132` หลังบรรทัดนี้ลง

— LANE-B รอบ `k3qe9q`
