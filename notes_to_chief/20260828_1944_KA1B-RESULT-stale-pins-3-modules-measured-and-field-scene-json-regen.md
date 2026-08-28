[ถึง: chief สาย E · cc Panya, COO, สาย A/B | จาก: ผู้ช่วยเซสชัน attended "กะ1-B" (บัญชี [กะ3]) | 2026-08-28T19:44+07:00]

# RESULT — วัด stale pins ครบ 3 โมดูลบนเครื่องจริง · ยืนยันตัวเลข R213 ตรงทุกตัว · และ **regenerate `FIELD_SCENE_CANDIDATES.json` ให้แล้ว (22 -> 24)**

งานตามที่ใบส่งกะ `HANDOVER_to_ka3` ฝากไว้ ("refresh stale pins 3 โมดูล") · สั่งโดย Panya 2026-08-28 ~19:3x +07:00

## T0 — เงื่อนไขการวัด (สำคัญต่อการอ่านผล)
- repo `Pirate Force ServerProject` HEAD ปัจจุบัน = branch `local/a-smoke-20260828-r2` · `main` local = `origin/main` = **`336857cd`** (fetch ล่าสุด 17:24)
  ⇒ **PR `pirate-force-server#197` ยังไม่ merge เข้า clone นี้** ตัวเลขข้างล่างคือสภาพ *ก่อน* งานซ่อมของ R213
- client image `GameClient/GameClient.local.bin`
- 🔴 **รันด้วย `python3` = 3.10.12 ใน Linux VM ของ device bridge ไม่ใช่ `py -3` 3.14 บน Windows**
  ⇒ **นี่ไม่ใช่ผล GT-125** GT-125 ยังต้องรันบน Windows เหมือนเดิม · ใบนี้เป็น "วัดว่าพินค้างจริงไหม" ไม่ใช่ "รัน gate"
- ไม่แตะ `src/` · ไม่ commit · ไม่รัน git · ไม่แตะเกม/เซิร์ฟเวอร์/canonical DB · ไม่จับ `LOCK_GAME`

## ① `tools/pf_runtimeres_actor_entry_static.py` — **แดง 4 พิน · ตัวเลขตรงกับ R213 ทุกตัว**
`exit 1` · `152 guards, 4 failures` · ค่าที่วัดได้จริง (ดึงจาก global ของสคริปต์โดยตรง ไม่ได้อ่านจากข้อความ):

| ตัวนับ | พินในโค้ด | วัดได้จริงวันนี้ |
|---|---|---|
| `SRC_ACTOR_ENTRY_SITES` | 13 | **15** |
| `SRC_ACTOR_STREAM_SITES` | 16 | **23** |
| `SRC_ACTOR_ENTRY_MODULES` | 12 | **14** |
| `SRC_VITAL_STREAM_SITES` | 21 | **25** |

สองโมดูลที่เกินจากรายชื่อพิน: `world_population_bg0002.py`, `mob_diag_multi_object.py`
⇒ **ยืนยันคำวัดของ R213 (15/23/14/25 vs 13/16/12/21) อย่างอิสระบนเครื่องจริง** — งานซ่อมใน `#197` ตรงเป้า ไม่ต้องแก้เพิ่ม

## ② `tools/pf_hp_death_respawn_static.py` — **แดง 2 พิน · เป็นข้อความ ไม่ใช่โค้ด ตรงตาม R213**
`exit 1` · `191 guards, 2 failures`
```
FAIL NEGATIVE: none of the 3 death/revive wire ids appears in v141 or src/  (1 hits)
FAIL NEGATIVE: no Relive/Revive/Respawn encoder or dispatch in v141 or src/ (9 hits)
```
จำนวน hit **1 กับ 9 ตรงเป๊ะ** กับที่ R213 รายงาน ⇒ วิธีนับใหม่ใน `#197` (นับจาก code token) แก้ตรงจุด
🔴 ย้ำตาม R213: **ไม่มี encoder/dispatch คืนชีพเพิ่มขึ้นในเซิร์ฟเวอร์เลย** ช่องว่างเดิมยังเป็นช่องว่างเดิม

## ③ `tests/test_pf_scan_field_scene_candidates.py` — **ใบเดียวที่ต้องทำหน้าเครื่อง · ทำให้แล้ว**
รัน:
```
python3 -B tools/pf_scan_field_scene_candidates.py --gamedata ../pf_bridge/gamedata --out <new>
-> exit 0 : "wrote ... (24 candidates, 268 scenes scanned)"
```
ไฟล์ผลอยู่ที่ **`pf_bridge\staged\FIELD_SCENE_CANDIDATES_regen_20260828.json`**
sha256 `f2152c267126bcf02524a6dd5846ce846ecc2411b5d44d6c42d45bf28353e166` · 10,515 bytes

diff เทียบกับ `docs/FIELD_SCENE_CANDIDATES.json` ที่ commit ไว้ (9,956 bytes):
- `candidate_count` **22 -> 24** · `scenes_scanned` **265 -> 268**
- ผู้สมัครใหม่ 2 ราย:
  - **`Bg0009` scene_n_id 9 "Death City Sea"** — hostile 5 · unambiguous 41
  - **`Bg0003` scene_n_id 3 "Spice Paradise Island"** — hostile 4 · unambiguous 53
- `no_placement_file` เดิมมีสมาชิก -> ตอนนี้ **ว่าง** (สามฉากที่เคยไม่มีไฟล์ placement มีแล้ว หนึ่งในนั้นชื่อ `FilmScene`)
- ประโยค `has_outdoor_air_companion` อัปเดตเอง 185/265 -> 185/268

🔴 **ผมไม่ได้เขียนทับ `docs/FIELD_SCENE_CANDIDATES.json` และไม่ได้ commit** — วางไว้ใน `staged\` ให้ chief ยกเข้า PR
(เขตเขียนของ `docs/` เป็นของสาย/chief ไม่ใช่ของผู้เทส)

## ④ สรุปว่าใครต้องทำอะไรต่อ
1. **chief**: merge `#197` (ปิด ① กับ ②) แล้วยก JSON จาก `staged\` เข้า PR อีกใบเพื่อปิด ③
2. **GT-125** ยังต้องรันจริงบน Windows `py -3 -m pytest -q` หลัง `#197` merge — ใบนี้แทนไม่ได้
3. 🔴 **อ่านใบ `20260828_1940_KA1B-OPS-CORRECTION-*` ก่อน**: `pf_bridge` push ไม่ออกตั้งแต่ ~15:2x เพราะ HEAD ค้างบน branch local
   ⇒ ใบนี้กับไฟล์ใน `staged\` **จะยังไม่ถึงคลาวด์** จนกว่าจะแก้

## ⑤ nonclaims
- ไม่อ้างว่าเครื่องมือทั้งสามจะ exit 0 หลัง `#197` merge — ยังไม่ได้รันบน tree ที่มี `#197`
- ไม่อ้างว่าผลจาก python 3.10 บน Linux VM เท่ากับผลจาก py 3.14 บน Windows โดยเฉพาะตัวสแกนใหม่ที่ R213 บอกว่าทำงานต่างกันบน 3.12+
- ไม่อ้างว่า `Bg0009`/`Bg0003` เข้าถึงได้ในเกม — ใบนี้เป็นสำมะโนจากตารางข้อมูลล้วน ไม่ใช่ผลบนจอ
- ไม่อ้างว่า `docs/FIELD_SCENE_CANDIDATES.json` ตัวที่ commit อยู่ "ผิด" — มันแค่เก่ากว่า gamedata ชุดปัจจุบัน
- ไม่แตะ `src/` ไม่ commit ไม่รัน git ไม่แตะเกม/DB/คิว

— กะ1-B
