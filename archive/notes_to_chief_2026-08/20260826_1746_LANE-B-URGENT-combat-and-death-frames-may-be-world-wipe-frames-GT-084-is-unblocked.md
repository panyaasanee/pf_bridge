[ถึง: **chief cloud (cc)** · cc: **COO · RE runner · Panya · attended** | จาก: **สาย B · COMBAT (`pf-builder`)** · รอบ `yjty8a` · 2026-08-26T17:46+07:00]

# `LANE-B-URGENT` — `mob_combat.bar_frames` / `mob_death.death_frames` อาจเป็นเฟรมล้างโลก และ `GT-084` (การโจมตีจริงครั้งแรก) หลุดบล็อกแล้ว

## ⓪ อ่านสองบรรทัดนี้ก่อน

🔴 **ใบนี้ไม่ได้ขอย้อน `#63`** ผมไม่มีอำนาจแตะ `runtime.py` และไม่เสนอให้ทำเอง — ใบนี้ขอ **การตัดสินใจของ chief/COO** ก่อน `GT-084` ถูกยิงจริง
🔴 **ผมไม่ได้แก้อะไรในโค้ดพฤติกรรมเลยรอบนี้** — ดู PR body: มีแค่ docstring + เทสที่ pin รูปทรงเดิม ไม่มีบิตไหนเปลี่ยน

## ① ปัญหา — จุดสองจุดที่ผมเองเขียนไว้ ตอนนี้เชื่อมกันแล้วและไม่มีใครเชื่อมมันก่อนหน้านี้

| ของ | เขียนไว้เมื่อไหร่ | บอกว่าอะไร |
|---|---|---|
| `notes_to_chief/20260826_0910_LANE-A-CORE-REQUEST-the-town-must-not-follow-you-out-of-town.md` §④.bis | 09:10 (cc สาย B ตรง ๆ) | `mob_combat.py:923`/`mob_death.py:852` (ตอนนั้น) ส่ง **nonempty one-entry `make_runtime_remote_actors` generation** — ถ้าเซแมนติกคือ "แทนที่ทั้งชุด" เฟรมนี้จะลบ actor อื่นทุกตัวที่ไม่อยู่ในเฟรมทิ้ง คำถามยังไม่มีคำตอบตอนนั้นเพราะโมดูลยังไม่ถูก wire |
| `notes_to_chief/20260826_1017_RE-082-RESULT-OBJECT-REF-IS-ELEMENT-KEY.md` T4 | 10:17 | พิสูจน์ (static, `PickupTerrainThing` consumer): **nonempty generation = replace-by-omission จริง** (key เก่าที่ไม่อยู่ใน generation ใหม่ถูก erase) · **zero-entry generation = no-op** ไม่ล้าง |
| `pirate-force-server#63` merge | 16:49+07:00 | `field_mobs`/`mob_combat`/`mob_death` wired เข้า `runtime.py` เส้นทางไร้แฟล็กจริง — **ทำให้คำถามของ 09:10 ไม่ใช่สมมติฐานอีกต่อไป** |
| `notes_to_chief/GAME_TEST_QUEUE.md` `GT-084` | เปิดโดย R177 · `[BLOCKED — รอ merge ก่อน]` | ทดสอบ **การโจมตีจริงครั้งแรกที่ไปถึง `mob_combat`/`mob_death` บนบูตไร้แฟล็ก** — เงื่อนไขบล็อกคือ "merge เข้า `main`" ซึ่งเกิดแล้วที่ `#63` ⇒ **ใบนี้พร้อมยิงตอนนี้** แต่หัวใบไม่มีข้อสังเกตให้เช็คว่านักแสดงอื่นบนจอหายไปหรือไม่ |

โค้ดจริงที่ผมตรวจสดรอบนี้ (`main` หลัง `#65` merge, ไม่ใช่ก๊อปเลขบรรทัดเก่า):

```
mob_combat.py:937   pc, frame = legacy.make_runtime_remote_actors([entry])   # bar_frames — ONE entry
mob_death.py:856    pc, frame = legacy.make_runtime_remote_actors([entry])   # death_frames — ONE entry
```

เทียบกับที่ปลอดภัยอยู่แล้วในไฟล์เดียวกัน (ส่ง `entries` หลายตัว ไม่ใช่ตัวเดียว):
```
field_mobs.py:552   pc, frame = legacy.make_runtime_remote_actors(entries)   # full roster
mob_death.py:1349   pc, frame = legacy.make_runtime_remote_actors(entries)   # full roster (corpse_override)
```

## ② สิ่งที่ยังไม่รู้ — และทำไมผมไม่แก้เอง

`RE-082` พิสูจน์เซแมนติกนี้ให้ **`PickupTerrainThing` consumer คนละตัว** เท่านั้น ใบจดหมายของ RE-082 เองเสนอว่ามันน่าจะ generalize มาตอบ `RE-077` `T5` (world/app cleanup ตอนเปลี่ยนฉาก) แต่ `RE-077` `T5` เองปิดเป็น **BOUNDED NEGATIVE** — "ห้ามสรุปว่า remote actor ถูก preserve หรือถูก drop แน่นอน" ยังไม่มีใครรัน static trace กับ consumer ตัวจริงของ `make_runtime_remote_actors` (`GSCN_RunTimeProtocolRes` mask `0x02`, chain `0x5E1C10`/`0x5E01D0` ตามด็อกสตริงของฟังก์ชันเอง)

`GT-035` (PASS, 2026-08-25) พิสูจน์ว่าหลอด HP ของมอนสเตอร์ที่ถูกตีเองอ่านถูกต้อง — **ไม่ได้พิสูจน์ว่านักแสดงอื่นบนจอยังอยู่** เพราะไม่มีใครนับพวกเขาก่อน/หลัง ผมจึงไม่กล้าเขียนโค้ดเปลี่ยนรูปทรงเฟรม (เช่นส่งทั้ง roster แทนตัวเดียว) เพราะ:
- ไม่รู้ว่านั่นคือ fix ที่ถูกจริงไหมโดยไม่มี RE ยืนยัน scope ของ collection
- อาจทำลายพฤติกรรมที่ `GT-035` วัดไว้แล้วจริง (`CombatStep.frames`: "ONE FRAME LONG on a killing blow" เป็นสัญญาที่เทสยึดอยู่)
- การแก้ wire semantics โดยไม่มีหลักฐาน static คือสิ่งที่กฎ "หลักฐานสองชั้น" ห้ามพอดี

## ③ สิ่งที่ทำรอบนี้ (ไม่ใช่ fix — เอกสาร + เทส pin เท่านั้น)

- `mob_combat.py` (`bar_frames`) และ `mob_death.py` (`death_frames`) เพิ่ม docstring ย่อหน้าใหม่อ้างใบนี้ + `#63` + RE-082 ตรง ๆ
- `tests/test_mob_combat.py`/`tests/test_mob_death.py` เพิ่มเทสละหนึ่งตัว pin ว่าเฟรมยังเป็น **หนึ่ง entry พอดี** (ไม่ใช่ roster ไม่ใช่ศูนย์) — ถ้าใครแก้รูปทรงต่อจากนี้โดยไม่ตั้งใจ เทสจะแดง
- ไม่แตะบิตพฤติกรรมสักตัว: `340 passed` ทั้งก่อนและหลัง (`tests/test_mob_*.py`) · ผ่าน `pf-adversary` ก่อน commit

## ④ ขอ chief/COO ตัดสิน

- (ก) **เปิดใบ RE ใหม่** (เลขถัดจาก RE-083 ตามธรรมเนียม chief เป็นคนออกเลข) ให้ RE runner: trace consumer ของ `GSCN_RunTimeProtocolRes` mask `0x02` (`0x5E1C10`/`0x5E01D0` ตามด็อกสตริง `make_runtime_remote_actors`) ว่า nonempty generation ของ collection นี้เป็น replace-by-omission เหมือน `PickupTerrainThing` หรือไม่ — คำถามเดียวกับที่ปิด `GT-084` ให้อ่านผลถูกต้อง
- (ข) **ก่อน `GT-084` ถูกยิง**: เติมข้อสังเกตในหัวใบ `GAME_TEST_QUEUE.md` ให้ผู้เทส **นับ/สังเกต actor อื่นบนจอ (ตัวละครอื่น ถ้ามี) ก่อนโจมตีและหลังแต่ละหมัด** ไม่ใช่จ้องแต่หลอด HP ของ `0x201F` เท่านั้น — นี่เป็นของ `pf-queue-author`/chief ไม่ใช่ของสายนี้ ผมไม่แตะ `GAME_TEST_QUEUE.md` เอง
- (ค) ถ้า chief/COO เห็นว่าความเสี่ยงสูงพอ อาจเลือก **ชะลอ `GT-084`** จนกว่า (ก) ตอบ — เป็นการตัดสินใจของ COO ไม่ใช่ของสายนี้

## ⑤ ถ้าไม่ทำอะไรเลยกับใบนี้

`GT-084` อาจถูกยิงและอ่านผลแค่หลอด HP ของมอนสเตอร์เป้าหมาย — ถ้าเซแมนติก "แทนที่ทั้งชุด" เป็นจริง ผู้เทสจะไม่มีทางรู้ว่านักแสดงอื่นหายไปพร้อมกัน (ไม่มีอะไรบนจอบอก) และผลจะถูกอ่านเป็น PASS ทั้งที่ M4 กำลังส่ง world-wipe ทุกครั้งที่มีหมัดหรือการตาย

## nonclaims

- ไม่ได้อ้างว่า collection นี้ล้างจริง — ยังไม่มี static trace ของ consumer ตัวนี้โดยเฉพาะ
- ไม่ได้อ้างว่า `GT-035` พิสูจน์ว่าปลอดภัย — พิสูจน์เฉพาะหลอด HP ของเป้าหมายเอง
- ไม่ได้แตะ `runtime.py` · `app.py` · `pf_login_game_server_v141.py` · `GAME_TEST_QUEUE.md` · canonical DB

— **สาย B · COMBAT**
