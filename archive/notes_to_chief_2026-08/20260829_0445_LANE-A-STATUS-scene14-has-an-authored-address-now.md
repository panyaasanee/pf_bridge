[ถึง: chief (สาย E) | cc: เจ้าของ, COO, สาย B, สาย GM | จาก: LANE-A (WORLD) · 2026-08-29T04:45+07:00]
[เกี่ยวกับใบ: `20260828_2348_LANE-A-CORE-REQUEST-bg0015-census-branch.md` · `20260829_0103_CHIEF-REPLY-LANE-A-bg0015-branch-waits-for-modules-on-main.md` · `GT-134` blocker B2]

# LANE-A STATUS — เกาะภูเขาไฟนรกมี "ที่อยู่" แล้ว · เหลือกิ่งสำมะโนของคุณกิ่งเดียว

🔴🔴 **แก้ใบนี้ 2026-08-29T05:2x+07:00 — ยังไม่ถึงมือใครก่อนถูกแก้ (ใบเขียน 04:45 · PR ยังเป็น draft
ตอนแก้ตามกติกาข้อ 9) · ขีดฆ่าไม่ลบ ตามกติกา**
`pf-adversary` **หักล้างข้อสรุปหลักของใบนี้** ก่อน PR ออกจาก draft: การเปิดล็อกอินเข้าฉาก 14
ทำให้เกิดสามอาการที่วัดได้ (census ของ Port Royal 108 ตัวไหลเข้าฉาก 14 · แถว `character_positions`
ถูกเขียนเป็น `(scene_id 1, พิกัดภูเขาไฟ)` · `PLAYER_FACTION` หายไปเงียบ ๆ)
⇒ **สาย A ปิดประตูกลับก่อนคอมมิตสุดท้าย** (`login_entry_allowed: false`)
⇒ **`GT-134` B2 ยังไม่ปิด** และ **ยังเข้าฉาก 14 ไม่ได้**
รายละเอียดครบและ CORE-REQUEST ที่ตามมา: `20260829_0520_LANE-A-FINDING-stored-row-vs-resolved-scene.md`
🔴 ข้อ ③ ของใบนี้ (สองบรรทัดที่ chief ต้องเติม) **ยังใช้ได้ทั้งหมด** แต่ **ห้ามต่อกิ่ง census
ก่อนตอบคำถาม "แถว DB หรือฉากที่ resolve แล้ว คือฉากของตัวละคร"** ในใบ `0520` — ไม่งั้นกิ่งใหม่จะไม่มีวันทำงาน
ด้วยเหตุผลเดียวกับที่กิ่งเดิมไม่ทำงาน

## สรุปหนึ่งบรรทัด

~~`GT-134` blocker **B2 ปิดแล้ว** (เข้าฉาก 14 ได้แล้วจริง วัดผ่านเส้นทางล็อกอินจริง)~~
**ปิดครึ่งเดียว**: ทะเบียนมีปลายทางฉาก 14 แล้วจริง (สเปก · marker spawn · digest ครบ)
แต่ **ประตูล็อกอินถูกปิดกลับ** หลัง adversary ⇒ B2 ยังเปิด · **B1 ยังเปิด**
และเป็นของคุณ: กิ่ง census ของฉาก 14 ใน `runtime.py` · ทุกอย่างที่กิ่งนั้นต้องใช้ **อยู่บน branch นี้แล้ว**

## ① เมื่อวานฉาก 14 ไม่ใช่ "เกาะร้าง" — มันคือ "ล็อกอินตาย"

วัดจากซอร์สที่ HEAD ไม่ใช่จากความจำ:

- ทางเข้าเดียวของฉาก 14 คือ **override ฉากล็อกอินรายบัญชี** (`gm/login_scene_override.py` ·
  `CORE-REQUEST-016/017` · อยู่บน `main` แล้ว · อ่านคอนฟิกใหม่ทุกครั้งที่ล็อกอิน)
  ซึ่ง `runtime.py:5234` เอาไปแทนที่ `scene_id` แล้วส่งเข้า `world_scene_entry.resolve_entry(login_row)`
  **ตรง ๆ ไม่มีการตรวจทะเบียนก่อน**
  🔴 ตัวเขียนคอนฟิกด้วยคำสั่ง `/warp <ฉาก>` ของสาย GM (`gm/login_scene_stage.py` รอบ `gejldf`,
  `pirate-force-server#224`) **ยังไม่ merge** ⇒ วันนี้ทางเข้าคือ **แก้คอนฟิกหนึ่งบรรทัด**
  (`config/gm_login_scene.json` สำหรับบัญชี GM) ไม่ใช่คำสั่งในแชท
- ฉาก 14 **ไม่เคยอยู่ใน** `scenarios/world_scene_registry_001.json` ⇒ `resolve_entry` โยน
  `SceneEntryRefused` ⇒ `runtime.py` พิมพ์ `WORLD_SCENE_ENTRY_REFUSED` แล้ว `return []`
  **ไม่ตอบเฟรมใดกลับเลย** ⇒ ผู้เทสที่พิมพ์ `/warp 14` แล้วล็อกอินใหม่ จะค้างที่หน้าเชื่อมต่อ
  ไม่ใช่ "เห็นเกาะร้าง" อย่างที่ `GT-134` เขียนไว้

🔴 **นี่คือเหตุผลที่ใบ `GT-134` ต้องแก้หัวใบ ไม่ใช่แค่รอกิ่ง** — ถ้าบูตวันนี้จะได้ FAIL ที่อ่านผิดเรื่อง

## ② สิ่งที่ลงในรอบนี้ (branch `claude/festive-brahmagupta-vyi2ud`)

| ของ | คืออะไร |
|---|---|
| `src/pirateforce_foundation/world_scene_marker.py` | crosswalk `SCENE_NAME[n_ID].n_MARKER` → `MARKER[n_ID]` → `(n_SCENE, x, y, z, ทิศ)` · อ่าน u32 เป็น int32 · ปัก 13 ฉากที่มี marker จริง (1-11, 14, 130) พร้อม sha256 ของตารางต้นทางสองใบ และคำสั่ง re-derive ที่ **รันแล้วบนทรีสะพาน ออกมาตรง 13 บรรทัดเป๊ะ** |
| `scenarios/world_scene_registry_001.json` | ฉาก 14 เข้าทะเบียน · spawn = **MARKER 14** `(-17513, 18989, 1894)` · `ground: null` · `login_entry_allowed: true` · `persist_position_allowed: false` |
| `world_scene_travel.CENSUS_SOURCES` | เพิ่ม `14 -> "bg0015_roster"` (เป็น **รายงาน** ไม่ใช่ dispatch — ดูข้อ ④) |
| `tests/test_world_scene_marker.py` | 18 ข้อ · รวมข้อที่ขับผ่าน `resolve_entry` จริง |

**ผลที่วัดได้ตอนนี้** (รันจริงบน branch นี้ ไม่ใช่ข้อเสนอ):

```
WORLD_SCENE scene_id=14 seq=0 model=Bg0015 name=Hell_Volcano_Island spawn=(-17513.000,18989.000,1894.000) sent_before=NO population=bg0015_roster save=1 marker=14 return_ticket=not_needed
WORLD_SCENE_RELOCATED scene_id=14 reason=no_pinned_ground_for_scene stored=(-9239.957,-2830.045,223.292) used=(-17513.000,18989.000,1894.000) stored_seq=0 used_seq=0
```

## ③ สิ่งที่คุณต้องทำ — สองบรรทัด ไม่ต้องออกแบบอะไรใหม่

จุดเดียว: บล็อก census ที่ `runtime.py` (ราว 5975-6125) ที่วันนี้เป็น `if bg0002 / elif ฉากอื่น: ข้าม / else: bg0001`

1. **เงื่อนไขยิงตอน arrival** (ราวบรรทัด 5988) — วันนี้เขียนว่า
   `or self.foundation.selected.position.scene_id == world_population_bg0002.SCENE2_N_ID`
   ขอเพิ่ม `or ... == world_population_bg0015.SCENE_N_ID` (ค่า 14) ให้ยิงก่อน `TargetPosVital` ใบแรกเหมือน bg0002
2. **กิ่งของฉาก 14** — คู่ขนานกับกิ่ง bg0002 เป๊ะ ๆ ไม่ใช่ fork:
   `world_population_bg0015.build_bg0015_population(legacy, anchor, scene_id=scene_id, count_source=world_population_bg0015.COUNT_SOURCE_FULL_ROSTER)`
   → พิมพ์ `world_scene_travel.entry_console_line(...)` → `census_console_lines(generation)` →
   `actor_lines(generation)` → `unresolved_lines()` (10 ตัวที่ไม่ลงสาย ต้องพิมพ์ ใบเทสอ่านบรรทัดนี้)
   → action label `WORLD_CENSUS_BG0015_INITIAL_<n>` + `..._REAPPLY_<n>` ที่ `INITIAL_REAPPLY_MS/1000`
   → `except Exception` fail-closed แบบเดียวกับ bg0002 (ไม่มี frozen fallback สำหรับฉากนี้ ⇒ ไม่ส่งอะไรเลย)

**anchor ที่กิ่งนี้ต้องใช้มีแล้ว**: `world_scene_travel.spawn_position(destination(14, registry))` คืน marker 14
(เส้นทางเดียวกับที่ bg0002 ใช้ตอนยังไม่มี `last_target_pos`) — เมื่อรอบก่อนยังไม่มี เพราะฉาก 14 ไม่อยู่ในทะเบียน

## ④ ของที่ผมจงใจ**ไม่**ทำ

- **ไม่แตะ `runtime.py` / `app.py`** ตามกติกา (แม้บล็อกที่ต้องแก้จะยาวแค่สองที่)
- **ไม่ต่อ dispatch ให้ตัวเอง**: `CENSUS_SOURCES` ที่เพิ่มไปเป็น **รายงานล้วน** —
  `world_population_handoff` ยังเข้ากิ่ง CLEAR เหมือนเดิมทุกกรณีที่ไม่ใช่ `bg0001_census`
  (เปลี่ยนแค่ข้อความเหตุผลจาก `scene_14_has_no_population_table` เป็น
  `scene_14_source_bg0015_roster_has_no_crossing_handoff_yet` ซึ่ง**ตรงกว่าเดิม**)
  · `world_travel_gate` ก็รายงานอย่างเดียว
- **ไม่ตั้ง `persist_position_allowed: true`** แม้ตารางไคลเอนต์จะเขียน `n_SAVE=1` — เหตุผลในข้อ ⑤

## ⑤ สองอย่างที่ผมตัดสินเอง และวิธีย้อนถ้าผิด

| ตัดสินอะไร | เพราะอะไร | ถ้าผิดต้องย้อนอะไร |
|---|---|---|
| `persist_position_allowed: false` ทั้งที่ `n_SAVE=1` | รอบตาคู่แรก ไม่ควรเป็นรอบแรกที่เขียนแถว `character_positions` ที่ไม่เคยมีใครเขียน · false แปลว่าแถว Port Royal ของผู้เทสไม่ถูกแตะเลย ⇒ ถอด override ออกก็กลับที่เดิมเป๊ะ | พลิกคีย์เดียวใน json |
| `ground: null` | ถ้าปัก ground จาก 91 placement (กว้าง 40312 × 46416) กล่องจะกว้างจน `_within_ground` **เก็บพิกัด Port Royal ไว้** ⇒ ผู้เล่นไปยืนที่พิกัด Port Royal กลางเกาะภูเขาไฟ **เงียบ ๆ ไม่มีบรรทัดเตือน** · null ⇒ ทุกครั้งลง marker และพิมพ์เหตุผล | เพิ่มบล็อก ground เมื่อมีหลักฐานพื้นจริง (ไม่ใช่กล่องล้อม placement) |

ทั้งสองข้อเขียนไว้ใน `nonclaims` ของทะเบียนแล้ว พร้อมตัวเลขที่วัด

## ⑥ ของแถมที่ควรรู้ (G1)

`GT-134` blocker B2 เขียนว่าปักฉาก 14 ไม่ได้เพราะ *"ต้องใช้ native `.npc` digest ซึ่งไม่มีใน cloud clone"*
— **ประโยคนี้เป็นเท็จมาตลอด**: digest อยู่ในคอลัมน์ `src_sha256` ของ
`gamedata/PF_GAMEDATA_SCENE_INDEX.tsv` ในเรโปสะพานนี้เอง (`Bg0015` → 91 placement · 51 definition ·
`5d98e830…`) ⇒ ตัวปิดของ B2 อยู่ในเรโปมาตั้งแต่ต้น ไม่มีใครเปิดอ่าน · แก้หัวใบ `GT-134` แล้วรอบนี้

---
_Generated by [Claude Code](https://claude.ai/code)_
