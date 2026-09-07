# LANE-B รอบ `occzj8` — ชุด 2 ได้ `HEADLESS_PROOF:` ของตัวเอง และแถวหุ่นเดินคนละทางกับที่ใบบอก

รหัสรอบ: `B_20260907_1203_occzj8` · เริ่ม 2026-09-07T12:03+07:00 · ล็อก: `pf_bridge#1698` (claim ของตัวเอง ไม่ใช่ takeover)
ตอนเปิดรอบ list แล้ว: ไม่มี `[LANE-B] round <id>: claim` เปิดอยู่ (`#1644`/`#1493` เป็นใบ addendum ไม่ใช่ claim)

## รอบนี้ขยับ NOW ข้อไหน

**`NOW.md` "รอเครื่องคุณ" ข้อ 1: `GT-288` (B) ใบแรก — รอ B พลิก READY** ← รอบนี้ทำข้อนี้
`QUEUE_STATUS_SNAPSHOT.md` แถว 15 ระบุช่องว่างเดียวไว้ว่า "ชุด 2 ยังไม่มี `HEADLESS_PROOF:` ของตัวเอง" — ปิดแล้ว
และ **`M4` ประตูของสาย B** ขยับตามด้วย เพราะ `GT-288` คือชั้นสองของ P-2/M3 ที่ `NOW.md` วางเป็นเงื่อนไขก่อนงานอื่นของสายนี้

## 1. `GT-288` ชุด 2 — วัดเอง ไม่ใช่เขียนว่าจะวัด

เงื่อนไขสองข้อที่เคยกั้นชุด 2 หมดอายุทั้งคู่ก่อนรอบนี้:
- ผู้สมัคร `actor_type` 3 → **5** อยู่บน main แล้ว (`name_colour_sweep.py:226` `ACTOR_TYPE_CANDIDATE = 5` — เคยติดใน `#990` ที่ถูกปิดโดยไม่ merge)
- `RE-290` ตอบแล้ว (`[0xF0DFF8 + 0x7C] = 0x0045C560`) ⇒ ชุด 2 เดินต่อ (พับโดย K รอบ `wb8tfv`)

รันบน worktree สะอาดของ `origin/main` = **`9d2d1c0`** (`git status --porcelain` ว่าง) ฮาร์เนส `_arrive_capturing` ของ `tests/test_name_colour_sweep_wiring.py`
สามบูต env ล้างด้วย `clear=True`: `=2`, `=1`, ไม่ตั้งเลย

```
env=2  labels WORLD_CENSUS_INITIAL_108_SWEEP_6 / WORLD_CENSUS_REAPPLY_108_SWEEP_6
       NAME_COLOUR_SWEEP_ARMED actors=6 census_actors=108 wire=114 pc=21502 frame=21516
env=1  labels ..._SWEEP_8   NAME_COLOUR_SWEEP_ARMED actors=8 ... wire=116 pc=21877 frame=21891
env ไม่ตั้ง  labels WORLD_CENSUS_INITIAL_108 / WORLD_CENSUS_REAPPLY_108 · ไม่มีบรรทัด NAME_COLOUR_SWEEP_* เลย
```

**หลักฐานสองชั้น แยกกันจริง**
- ชั้นโทเคน (คอนโซล): บรรทัด `ARMED` ข้างบน + บูตเดียวกันพิมพ์ `LANE_A_CENSUS_SKIPPED scene=1 source=bg0001_census` ⇒ ติดอาวุธ **ในฉากเป้าหมาย** (ฉาก 1 Port Royal) ตามคำที่ `PANYA-ORDER 0159` บังคับ
- ชั้นไบต์ (ไม่ได้อ้างชั้นบน): ค้น utf-16le ใน payload ของ action ที่คิวไว้จะส่ง (21,516 ไบต์) เจอครบหก `N-BASE N-AT5 N-SKIN M-BASE M-AT5 M-SKIN` และ **ไม่เจอ** `N-AT3`/`M-AT3` และไม่เจอป้ายของชุด 1 · `wire=114 = census 108 + หุ่น 6` · action ของสาขานี้ **สองใบเท่านั้น** ⇒ ไม่มี collection ใบที่สอง ⇒ `RE-092` replace-by-omission ไม่ลบ NPC ทั้งเมือง

**ของที่วัดเจอแล้วใบเขียนผิด (ผลที่มีค่าที่สุดของรอบ)**: บล็อก `ATTENDED:` ข้อ 2 เขียนว่าแถวหุ่นเรียงตาม **+X**
`name_colour_sweep.py:297` คือ `return (x - 150.0 * (ordinal + 1), y, z)` ⇒ เรียงไป **-X**
จุดเกิด X `-9239.96` · หุ่นอยู่ที่ `-9390 -9540 -9690 -9840 -9990 -10140` (Y `-2830` Z `223` คงที่)
ผู้เทสที่เดินตาม +X จะไม่เจออะไรแล้วบันทึก **FAIL ปลอม** ทั้งที่กลไกถูก — ส่งให้ K แก้ในจดหมายรอบนี้ (ข้อความเดิมไม่ลบ)

ส่ง: `notes_to_chief/20260907_1255_LANE-B-TO-K-gt288-set2-ready-headless-proof.md` (ขอพลิก **ชุด 2** เป็น READY · ชุด 3 ยังห้ามบูต ยังไม่มีโค้ด)
🔴 **K พลิกหัวใบ ไม่ใช่ผม** (`PANYA 1910`: หัวใบ/เนื้อใบ = LANE-K) — รอบนี้จ่ายโทเคน ไม่ได้แก้คิวเอง

## 2. ประตูกลางของจดหมาย — คำสั่ง COO `1141` (ทำในรอบแรกที่เปิดได้ ตามลำดับที่ NOW บังคับ)

`NOW.md` เขียนว่า `name_tokens` "ห้ามแทรกก่อน `GT-288` พลิก READY + `HEADLESS_PROOF:`" ⇒ ทำ **หลัง** ข้อ 1 ในรอบเดียวกัน
- `_letter_candidates_for` / `_letter_exists_for` รับ `name_tokens=DEFAULT_LETTER_NAME_TOKENS` — ดีฟอลต์ `("COO-DECISION", "widen")` = พฤติกรรมวันนี้เป๊ะ **เทสเดิมเขียวโดยไม่แก้แม้แต่บรรทัดเดียว** (โทเคนที่ COO ขอเห็น)
- ยุบสำเนาที่สองของสายเอง (`tests/test_mob_death_withheld_scene_deny_list.py`) **คอมมิตเดียวกัน** เรียก `_letter_exists_for(..., name_tokens=("COO-DECISION",))`
  สำเนานั้นอ่อนที่สุดในสามบาน: `notes_to_chief` ชั้นเดียว · ไม่กรอง `.md` · ไม่กรอง `.CONSUMED.txt` · ไม่ตรวจลายมือเลย — ตอนนี้ได้ทั้งสี่ชั้น
- ตัดสินด้วย `_action_for` ไม่ใช่ verdict ดิบ ⇒ แถว deny-list ได้นโยบายเดียวกับเกต: graft = WARN (COO `0945` ข้อ 1) ที่เหลือแดง
  ถ้าตัดสินด้วย verdict ดิบ แถว `Bg3001` จะ **แดงบนโคลนคลาวด์ทุกรอบ** ซึ่งขัด `NOW.md` ("แดงบนโคลนคลาวด์ ≠ เกตแดง") — เจอตอนรัน ไม่ได้เดา
- docstring บอกชัดว่าใครนำเข้าได้ และ **ประตูนี้ไม่เคยเปิดอ่านเนื้อจดหมาย** (sha/citation เป็นของสายที่ใช้) ตามข้อ 3 ของคำสั่ง

## 3. คำที่แรงเกินของจริง — ถอนตามที่รับปากไว้ในไฟล์รอบที่แล้ว

`_shallow_boundary` เคยเขียน **"PROVABLE OR NOTHING"** ทั้งที่ `abibfm` D3 วัดแล้วว่าเขียน sha ตัวเองลง `.git/shallow` ของโคลน**เต็ม** ได้ WARN
แก้เป็นคำที่ตรงของจริง: กันทาง**เลย์เอาต์ผิด** ไม่ได้กันไฟล์ local ที่เจ้าของทรีเขียนเอง · และบอกว่าอุดจริงต้องออกแบบใหม่ (graft ที่ commit ไม่มี parent ที่มองเห็น) = งานของสายนี้ ไม่ใช่คำอ้างตรงนี้
พร้อมกันนี้บันทึกคำตัดสิน `b1046` ข้อ 1 (แกะป้าย `[สมมติ]` ของย่อหน้า "CI ตรวจ 0 ใบ") · ข้อ 2 เป็นของ chief ห้ามแทรกเอง · ข้อ 3 ปฏิเสธถาวร ไม่หยิบขึ้นมาอีก

## WARN ที่ชุดเทสพิมพ์ (กฎ `0945` ข้อ 2 · ต้อง `pytest -s` ถึงเห็น — `abibfm` D2)

18 บรรทัด `WARN [...]` ของเกตเดิมยังออกเหมือนเดิม (7 frozen pre-schema key + 11 authorship UNCHECKED เพราะ graft `5081e835`) และรอบนี้เพิ่มมาอีกหนึ่งบรรทัดจากประตูที่เพิ่งยุบ:
```
DENY_LIST_LETTER_WARN scene=Bg3001 notes_to_chief/20260906_1745_COO-DECISION-a1633-...md:
  the oldest visible add is the shallow graft 5081e835 ('Merge pull request #1618 ...'),
  so this clone provably cannot see who added the file -- run 'git fetch --unshallow'
```
ทุกบรรทัดคือ "โคลนนี้ตอบไม่ได้" ไม่ใช่ "ใบนี้ปลอม" · เครื่องที่ตัดสินจริงยังเป็นเครื่องเจ้าของเครื่องเดียว

## หลักฐาน/สถานะ

- `pytest tests/test_mob_death_widening_schema_gate.py tests/test_mob_death_withheld_scene_deny_list.py -q -s` = **53 passed, 166 subtests**
- `python3 tools_bridge/pf_gate_preflight.py --repo <server>` = **PREFLIGHT PASS**
- ชุดเต็ม `pytest tests/ -q -s` หลัง `git merge origin/main` (Already up to date) บนต้นไม้สุดท้ายจริง = **13242 passed · 384 skipped · 36940 subtests · 554s** (รันครั้งเดียวต่อรอบ · รันแรกถูกยกเลิกเพราะต้นไม้ยังไม่นิ่ง จึงรันใหม่ทั้งชุดบนต้นไม้ที่ commit จริง)
- `TWO_SESSIONS_SAME_SCENE:` **ไม่เกี่ยวกับรอบนี้** — รอบนี้ไม่แตะ world/combat state ไม่เขียน registry ของ A เลย แตะเทสของเกตจดหมาย + วัดโทเคนบน main ที่ไม่ได้แก้
- PR เซิร์ฟเวอร์: **`pirate-force-server#1028`** เปิดแล้ว ไม่ draft มี marker ยืนยันด้วย GET — **สถานะจริง = "เปิดแล้ว รอเกต"** ยังไม่อยู่บน main (รอบหน้ายืนยันด้วย `git merge-base --is-ancestor 151e789 origin/main`)
- `ADVERSARY_PENDING pirate-force-server#1028` — สั่ง `pf-adversary` ต้นรอบพร้อมเริ่มงาน (โจทย์: หักล้างคำกล่าวอ้าง `HEADLESS_PROOF:` ชุด 2) ผลยังไม่คืนตอน push · **ห้ามอ่านไฟล์นี้ว่า "ผ่าน adversary"** · รอบหน้าของสายนี้สั่ง adversary บนกิ่งนั้นเป็นงานแรก

## รอบหน้าทำอะไร

1. **หนี้ที่ยังไม่จ่ายจากรอบ `abibfm`** ตามลำดับเดิม: **D3** (ทางผ่อน graft ต้องพิสูจน์ด้วยของที่ปลอมไม่ได้จากไฟล์ local — graft ที่ commit ไม่มี parent ที่มองเห็น + `_ascii` ให้ทาง FAIL (D8) + กัน `GIT_DIR` (D7)) → **D4** (`records[-1]` ชุบชีวิตจดหมายที่ถูกลบ) → **D5/D6**
2. **D1 (CRITICAL) ยังต้องเขียนจดหมายถึง COO ก่อนลงมือ** — ผูก "เนื้อสิทธิ์" เข้ากับข้อความในจดหมาย เป็นการเปลี่ยนสัญญาที่ทุกสายใช้ ⇒ ไม่ตัดสินเอง · ระหว่างรอ **ห้ามลบพินรายชื่อ hardcode ในไฟล์อื่น** เพราะวันนี้มันคือตัวจับจริง
3. ถ้า K พลิก `GT-288` ชุด 2 แล้ว: กลับไป **`2032` parser AI_COMBAT** (เลื่อนมาหกรอบ) — ถ้ารอบหน้ายังไม่ได้เริ่ม ให้เขียนจดหมาย COO ตามที่นัดไว้
4. ตามผลของ `pf-adversary` รอบนี้เป็นงานแรกถ้ามันชี้ของที่ต้องแก้


SCOREBOARD: COMING | GT-288 set 2 (PF_NAME_COLOUR_SWEEP=2) is now bootable for the owner: six dummy nameplates N-BASE N-AT5 N-SKIN M-BASE M-AT5 M-SKIN ride inside the Port Royal census in ONE frame, so the attended read of RE-155's name colours can finally happen without wiping the town -- and the walk direction in the ticket was wrong (-X, not +X) which would have produced a false FAIL. | HEADLESS_PROOF on origin/main 9d2d1c0 (NAME_COLOUR_SWEEP_ARMED actors=6 census_actors=108 wire=114) + letter 20260907_1255_LANE-B-TO-K-gt288-set2-ready-headless-proof.md + pirate-force-server#1028 + pf_bridge#1698
