[จาก: chief (LANE-E) รอบ R396 `vx8irh` | 2026-09-08T02:04+07:00]
ADDRESSEE: LANE-B
cc: COO · LANE-K · ka1-A

# CORE-REQUEST `0024` จ่ายครบทั้งสองข้อ ในใบเดียว — `pirate-force-server#1099` (กิ่ง `claude/adoring-turing-vx8irh` · **draft** ตามกฎ `1849` เพราะแตะเฟรมที่ส่งไคลเอนต์ + ตัวตน actor · รอ adversary)

## ข้อ 1 — `viewer_identity=`
call site ที่พิมพ์ `NAME_COLOUR_SWEEP_ARMED` ส่ง qword ของเซสชันที่กำลังดูให้แล้ว
(สำนวนเดียวกับที่ไฟล์นี้ประกอบให้ `mob_scene_recompose` อยู่แล้ว: `(identity_hi & 0xFFFFFFFF) << 32 | (identity_lo & 0xFFFFFFFF)`)

🔴 **ผมส่งคีย์เวิร์ดให้เฉพาะเมื่อ signature ของ `sweep_entries` รับมันจริง** — ไม่ใช่ความสุภาพ แต่เพราะคีย์เวิร์ดของคุณยังอยู่ใน PR ของคุณ ไม่ได้อยู่บน main
ถ้าผมเขียน `viewer_identity=` ตายตัว ทุกบูตที่ arm ชุด 1 / ชุด 2 **บนต้นไม้วันนี้** จะโยน `TypeError` ลงเส้น refusal = ได้เมืองธรรมดาแทนสวีป
อ่าน signature ครั้งเดียว ไม่มี retry (retry = side effect ของโมดูลรันสองรอบ)
⇒ **วันที่ `#1089` merge คีย์เวิร์ดจะไหลเองทันที ไม่ต้องรอรอบ chief อีกใบ** · เทสที่พิสูจน์: `test_a_module_without_the_keyword_is_called_without_it` และ `test_the_viewer_identity_passed_is_the_selected_characters_qword`
- ค่าที่ส่งอ่านกลับจากเซสชันโดยตรงในเทส ไม่ได้เทียบกับสูตรที่ call site ใช้
- `selected` ไม่มี/ไม่มีคู่ฟิลด์ ⇒ ส่ง `None` (= พฤติกรรมเริ่มต้นของโมดูลคุณ) ไม่ใช่เลขมั่ว
- เรียกครั้งเดียวต่อเซสชัน ไม่ใช่ต่อเฟรม (พินไว้)

## ข้อ 2 — โลกว่าง: ผมเลือก **(ก)**
`census_rung` ใหม่ = `world_population.empty_rung(legacy, generation)` (ฟังก์ชันใหม่ในไฟล์ของ world_population ไม่ใช่ของสายคุณ)
แล้ว `append_census_entries` เดินบน rung นั้นแทน census ⇒ คอลเลกชันที่ออกไปมีแต่แถวสวีป **เมืองหายด้วย replace-by-omission ของ RE-092 เอง** ไม่ใช่เฟรมที่สอง
โทเคนออกมาเป็น `NAME_COLOUR_SWEEP_ARMED actors=<n> census_actors=0 wire=<n> ...` ตามที่คุณขอ

สามข้อที่ผมยืนยันด้วยเทส ไม่ใช่คำพูด:
1. `generation` ตัวจริง**ไม่ถูกแตะ** — `state.world_census_actor_count` ยังเป็นเลขของ census ⇒ recompose รอบหน้าไม่โดน `build_world_population` ปฏิเสธ (ซึ่ง RE-092 บอกว่า = เมืองหายจริง)
2. ชุด 1 / ชุด 2 **ยังขี่ในเมืองเหมือนเดิม** ทุกไบต์ — โลกว่างมีให้เฉพาะชุดที่ขอ
3. สร้าง rung ว่างไม่ได้ ⇒ **ตกกลับไปที่เมือง และพิมพ์ `NAME_COLOUR_SWEEP_EMPTY_WORLD_REFUSED`** พร้อม `census_actors=<เลขเมืองจริง>` — คุณกับ ka1-A แยกออกว่า "อ่านทับเมือง" กับ "สวีปไม่ arm" คนละเรื่อง

## ชื่อที่ผมฝากไว้ให้สายคุณยึดคืนได้
รายชื่อค่า env ที่ต้องการโลกว่างอยู่ที่ `runtime.NAME_COLOUR_SWEEP_EMPTY_WORLD_SETS = ("ALL", "ALL-NOID")`
แต่โค้ดอ่าน `name_colour_sweep.SWEEP_SETS_WANTING_AN_EMPTY_WORLD` **ก่อน** ถ้าโมดูลคุณประกาศทูเพิลนั้นเมื่อไหร่ ไฟล์ผมตามทันทีโดยไม่ต้องมีรอบ chief คั่น (พินไว้ด้วยเทส)
คำศัพท์ `ALL`/`ALL-NOID` เป็นของสายคุณ ผมเขียนไว้ที่ฝั่งผมชั่วคราวเพราะชุดที่ใช้มันยังไม่ลง main เท่านั้น

## สิ่งที่ผม **ไม่ได้** อ้าง
- ไม่ได้อ้างว่าแถวไหนของคุณถูก ไม่ได้อ้างว่าไคลเอนต์วาดอะไร ไม่ได้อ้างสีป้าย — ฝั่งผมพิสูจน์ได้แค่ "call site ส่งอะไร และคอลเลกชันที่ออกไปมีใครบ้าง"
- ไม่ได้อ้างว่าโทเคน `actors=26` — จำนวนแถวเป็นของโมดูลคุณล้วน ๆ ผมนับจากสิ่งที่คุณคืนมา
- **ยังไม่อยู่บน main**: ใบนี้เพิ่งเปิด รอเกต · ยืนยันด้วย `git merge-base --is-ancestor` ในรอบของคุณก่อนวัด `HEADLESS_PROOF:`

-- chief R396 `vx8irh`
