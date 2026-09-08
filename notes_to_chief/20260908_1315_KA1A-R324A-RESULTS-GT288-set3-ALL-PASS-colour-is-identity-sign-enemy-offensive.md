# R324A RESULTS (ka1-A attended · Panya ที่คีย์บอร์ด 12:39–13:05) — **GT-288 ชุด 3 (สวีป ALL) PASS: P-2 ตอบครบทั้งกฎ** · สีชื่อ = เครื่องหมาย identity → ความสัมพันธ์ฝ่าย → `n_OFFESIVE` · เหลือง/ส้ม/แดง ขึ้นจอครั้งแรกในโปรเจกต์

ADDRESSEE: LANE-K (พับผล + พลิกใบ) · cc: LANE-B (เจ้าของใบ/ผู้บริโภคผล) · LANE-GM (เกตสี `gm/name_color_gate.py`) · COO · chief · Panya
ส่งทาง: สะพาน (เครื่องเจ้าของเปิด)
OBSERVER_CONFIRMED: 2026-09-08T12:45–13:05+07:00 (Panya: ภาพหน้าจอ 5 ใบ + คำบรรยายทีละป้าย · ยืนยันคำต่อคำ "M-IDNEG = แดง · M-IDNEG-T31 = ส้ม" และ "N-HP0 คือเขียว พร้อมหลอดเลือดหมดหลอด และเป็นตัวเดียวที่ล้มลง" และ "ฉันไม่เห็น N-ID0 · ทั้งจอเห็นวาดทั้งหมด 23 ตัว")

## บูต
- BOOT_COMMIT `bb5f5db8` (resolver หัวเขียวล่าสุด · `#1098` และ **`#1099` อยู่ในนี้แล้ว**) · worktree HEAD `76e68b03` clean · ทรีไร้ธง · env เดียว `PF_NAME_COLOUR_SWEEP=ALL` · run DB `state/run_gt288_20260908_123815.sqlite3` ตัดจาก canonical · capture `GameClient/capture_r324a_20260908_123815/` · jobs 1585 บูต / 1586 teardown / 1587 release
- RECHECK บนทรีบูตก่อนบูต (กฎ `0159`): `merge-base --is-ancestor 84bf0787` ผ่าน · pytest ROUND PASS · `tools/pf_name_colour_sweep_headless.py` → `set=ALL actors=22 entries=22` + `NAME_COLOUR_SWEEP_HEADLESS PASS`
- **ชั้น wire ตอนบูตจริง: `NAME_COLOUR_SWEEP_ARMED actors=24 census_actors=0 wire=24 pc=4376 frame=4389`** · `[G>] WORLD_CENSUS_INITIAL_108_SWEEP_24` ×1 + `REAPPLY` ×1 · ไม่มี collection ใบที่สอง
  - **24 ไม่ใช่ 22 เพราะ `#1099` ของ chief ลง main ก่อนบูต** (viewer identity ⇒ `N-LNKP` + `N-IDNEG-LNKP` ประกอบได้ · `census_actors=0` ⇒ **โลกว่าง ตามคำสั่งเจ้าของ `2350` ครบ**) — ตอนเจ้าของสั่ง "บูตเลยไม่ต้องรอ #1099" ทั้ง ka1-A และเธอเข้าใจว่าจะได้ 22 ป้ายพร้อม NPC เมือง แต่ resolver หยิบหัวที่มี `#1099` ให้เอง จึงได้ครบโดยไม่ต้องบูตซ้ำ
- canonical sha **ไม่เปลี่ยน** `4FF37060…A548454` (guard ตรวจก่อน/หลัง) · ปิดสะอาด `FINAL listeners=0 clients=0` · ตัวละคร **Arena01 (Gladiator LV1 ในบูตนี้)** ไม่ได้สร้างตัวใหม่ (deviation)

## ผลทีละป้าย (ชั้นจอ = คำ/ภาพเจ้าของ · เรียงตามลำดับที่โมดูลประกอบ)
| # | ป้าย | identity | ฝ่าย/ฟิลด์ที่ต่าง | **สีที่เห็น** | ตรงคำทำนาย |
|---|---|---|---|---|---|
| 1 | N-BASE | บวก | ควบคุม | เขียว | ✔ |
| 2 | M-BASE | บวก | faction 6 (ศัตรู) | ชมพู | ✔ |
| 3 | N-LVL | บวก | level 100 | เขียว | ✔ |
| 4 | N-HP | บวก | HP 198125 | เขียว | ✔ |
| 5 | N-SPD | บวก | speed 150 | เขียว | ✔ |
| 6 | N-TPL | บวก | template 916 | เขียว | ✔ |
| 7 | N-PRE | บวก | preset M016 | เขียว | ✔ |
| 8 | **N-ID0** | **0** | — | **ไม่ถูกวาดเลย ไม่มีป้าย** | ผลใหม่ |
| 9 | **N-IDNEG** | **−1** | NPC template 1 | **เหลือง** | ✔ |
| 10 | **M-IDNEG** | **−2** | มอน 916 · faction 6 | **แดง** | ✔ (ทำนายว่า "ส้ม/แดง") |
| 11 | **M-IDNEG-T31** | **−5** | มอน 31 · faction 6 | **ส้ม** | ✔ |
| 12 | **N-IDNEG-T916** | **−6** | NPC + template 916 | **เหลือง** | ✔ |
| 13 | N-LNKP | บวก | linked = ผู้ดู | เขียว | ✔ |
| 14–19 | N-ENM0 / N-ENM1 / N-ENM2 / N-ENM6 / N-ENM12 / N-ENMFF | บวก | `n_ENEMY` = 0/1/2/6/12/0xFFFFFFFF | **เขียวทั้งหมด** | ✔ (ผลลบที่มีค่า) |
| 20 | M-ENM1 | บวก | มอน body + n_ENEMY 1 | ชมพู | ✔ |
| 21 | **N-HP0** | บวก | HP ปัจจุบัน 0 | **เขียว + หลอดเลือดหมด + ล้มลง (ตัวเดียวที่ล้ม)** | ผลใหม่ |
| 22 | **N-IDNEG-LNKP** | **−3** | linked = ผู้ดู | **เหลือง** | ✔ |
| 23 | **N-IDNEG-ENM1** | **−4** | n_ENEMY 1 | **เหลือง** | ✔ |
| 24 | M-T001 | บวก | มอน body template 1 | ชมพู | ✔ |
- เจ้าของนับตัวที่วาดบนจอได้ **23 จาก 24** — ตัวที่หายคือ `N-ID0` ตัวเดียว

## กฎที่อ่านได้ (ka1-A · B/GM ตีความต่อ)
**สีชื่อของ client ตัดสินตามลำดับสามชั้น:**
1. **เครื่องหมายของ identity 64 บิต** (ตรง `RE-222` Q1 เป๊ะ): บวก → **สูตรผู้เล่น** (เขียว = ไม่ใช่ศัตรู · ชมพู = faction อยู่ใน `s_ENEMY` ของผู้เล่น) · **ไม่มีฟิลด์ใดใน body พาออกจากสูตรนี้ได้เลย** — level · HP · speed · template · visual preset · `n_ENEMY` ทุกค่า · linked identity · HP 0 → เขียว/ชมพูหมด
2. **identity ≤ 0 → สูตร NPC/มอน** · ในสูตรนี้ **ความสัมพันธ์ฝ่าย** ตัดสินก่อน: ไม่ใช่ศัตรู → **เหลือง** (N-IDNEG · N-IDNEG-T916 · N-IDNEG-ENM1 · N-IDNEG-LNKP ทั้งสี่ตัว) · เป็นศัตรู → ส้ม/แดง
3. **ในกลุ่มศัตรู `n_OFFESIVE` ตัดสินเฉด**: M-IDNEG (template 916 · `n_AI_WANDER=21` → `n_OFFESIVE=1`) = **แดง** · M-IDNEG-T31 (template 31 · `n_AI_WANDER=16` → `n_OFFESIVE=0`) = **ส้ม** ⇒ **ยืนยันบนจอว่า `0x0045C160` = `IsOffensive()` ที่ RE runner ถอดไว้ (จดหมาย 8 ก.ย. 00:35) เป็นตัวเลือกเฉดจริง** — สองป้ายนี้ต่างกัน **ฟิลด์เดียว** คือ template_id
4. **identity = 0 ⇒ ไม่วาดเลย** — ห้ามใช้ 0 เป็น actor identity ใน production (ตรงกับ `RE-222` Q1 ที่จัดศูนย์อยู่ฝั่ง "ไม่เป็นบวก" แต่ Q3 ไม่ได้ระบุว่า registry จะทิ้ง)
5. `N-HP0`: HP ปัจจุบัน 0 บน identity บวก → **ท่าศพขึ้นจริงและหลอดเลือดว่าง แต่สีไม่เปลี่ยน** ⇒ death predicate (เกต 2 ของ RE-222) อยู่ในสาย non-positive เท่านั้น ไม่ใช่ตัวทำให้เทา ในสายผู้เล่น

## สถานะที่เสนอ
- **`GT-288` → PASS** (ทั้งสามชุดปิด: ชุด 1 faction · ชุด 2 actor_type/skin · ชุด 3 ALL) · **`RE-155` ตอบครบทั้ง NPC (เหลือง) และมอน (ส้ม/แดง) ในคราวเดียว** ตามที่เจ้าของสั่งไว้ `2142` 6 ก.ย.
- **P-2 / M3 ชั้นสอง = ตอบแล้ว** — เหลือ "งานสร้าง" ไม่ใช่ "งานหาคำตอบ"
- BUILD_PROPOSED: production actor identity sign | LANE-B | ส่ง NPC/มอนทุกตัวด้วย identity 64 บิต **ไม่เป็นบวก** (ห้าม 0) แล้วให้ความสัมพันธ์ฝ่ายกับ `n_OFFESIVE` ทำงานตามตาราง; token: บูตปกติไม่มี env → NPC เมืองเหลือง · มอนสนาม 27–35 ส้ม · มอน `n_OFFESIVE=1` แดง · ผู้เล่นเขียว/ชมพูเหมือนเดิม
- BUILD_PROPOSED: identity allocator | LANE-B | ตัวจ่าย identity ของ census ต้องกันค่า 0 และแยกช่วง "ผู้เล่น = บวก / NPC-มอน = ลบ" พร้อมเทสที่ปักค่า; token: เทสบน main + ไม่มี actor หายจากจอ
- BUILD_PROPOSED: retire NameColorGateUnmeasured | LANE-GM | เกตที่ปฏิเสธเพราะ "ยังไม่วัด" มีผลวัดแล้ว — ปลดตามผลใบนี้ (อ้าง `RE-222` Q1/Q2 + R324A); token: `gm/name_color_gate.py` ไม่มีการปฏิเสธด้วยเหตุ unmeasured และเทสเดิมยังเขียว
- **หมายเหตุถึง `RE-222` Q2**: ผลนี้ **ไม่ขัด** คำตอบ "typed_CNetNPC เป็นการทดสอบชนิดออบเจ็กต์ เปลี่ยน identity อย่างเดียวไปไม่ถึงหาง typed" — เพราะสีที่ได้ (เหลือง/ส้ม/แดง) มาจากสาขาก่อนหน้าหางนั้น ไม่ใช่จากหาง typed

## nonclaims (ห้ามตัดออกตอนพับ)
- **ไม่ได้คลิก ไม่ได้ตี ไม่ได้ Tab หุ่นตัวใด** (ใบห้าม) ⇒ ไม่มีข้อมูลว่าตัวเหลือง/ส้ม/แดงตีได้หรือไม่ · ไม่ทราบว่าสีเปลี่ยนหลัง aggro ไหม · ไม่ได้วัด "เทา" (ยังไม่มีแถวมอน identity ลบ + ตาย ในชุดนี้ — `M-IDNEG-DEAD` ที่ ka1-A เสนอใน 2325 ไม่ได้ถูกประกอบ)
- ไม่อ้างว่า `n_OFFESIVE` เป็น "ตัวเดียว" ที่แยกส้ม/แดง — วัดได้ว่าสองป้ายที่ต่างกันที่ template ให้คนละเฉด และ RE ระบุ predicate นี้ · ฟิลด์อื่นที่ผูกกับ template (`n_RANK` เป็นบิตมาสก์ · AI_COMBAT) ยังไม่ถูกแยกออกจากกันด้วยการทดลอง
- `N-ID0` "ไม่ถูกวาด" = เจ้าของไม่เห็นบนจอและนับได้ 23/24 · ยังไม่ได้พิสูจน์ว่า client ทิ้งตอน register หรือวาดแล้วมองไม่เห็น (ต้องดู client-side · ผลลบชั้นจอ)
- แถว `+0x1A0` (ค่าฝ่ายที่ RE-310 ภาคผนวก 2 บอกว่าส่งจากสายได้) **ไม่ได้อยู่ในบูตนี้** — ใบ `1140` ยังค้างที่ B · ความสัมพันธ์ฝ่ายในบูตนี้มาจาก faction splice เดิม
- ตัวละคร Arena01 ไม่ใช่ตัวใหม่ · เจ้าของไม่ได้เดินสำรวจนอกลาน · ไม่ได้วัดว่ามี NPC เมืองโผล่หรือไม่ (โลกว่างจาก `census_actors=0` เป็นชั้น wire)

RESULT: GT-288 PASS R324A 2026-09-08 13:05 (set 3 ALL, 24 boards, census_actors=0 · colour = identity sign, then enemy relation, then n_OFFESIVE · yellow for non-positive non-enemy, orange for enemy with n_OFFESIVE=0, red for enemy with n_OFFESIVE=1 · identity 0 not drawn · HP 0 on a positive identity gives the corpse pose but keeps the player colour · no body field, no n_ENEMY value and no linked identity moves a positive identity out of the player formula)
RESULT: RE-155 ANSWERED R324A 2026-09-08 13:05 (both halves in one boot: NPC yellow and mob orange/red · the owner's colour table is reachable with the fields we already send)
SCOREBOARD: COMING | รู้แล้วว่าจะทำให้ NPC เหลืองและมอนส้ม/แดงต้องส่งอะไร — เหลือแค่เปลี่ยนตัวจ่าย identity ของ census ให้ NPC/มอนเป็นค่าไม่เป็นบวก แล้วผู้เล่นจะเห็นสีถูกทั้งเมืองและสนาม | 20260908_1315_KA1A-R324A-RESULTS-*
