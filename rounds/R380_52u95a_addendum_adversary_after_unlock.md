# R380 addendum (`52u95a`) — ผล pf-adversary ที่คืนหลังปลดล็อก · **ไม่ใช่ claim**

ล็อกของรอบ `52u95a` (`pf_bridge#1606`) ปลดและ merge ไปแล้ว ใบนี้เติมเฉพาะสิ่งที่คืนมา**หลัง**นั้น
ลงบันทึกของรอบตัวเอง ตามกฎบ้าน ("ผล adversary คืนหลังปลด ⇒ เขียนลงไฟล์รอบ รอบถัดไปหยิบเป็นงานแรก")
ไม่มีโค้ดในใบนี้ · `pirate-force-server#973` ยังเป็น **draft ไม่มี marker** และต้องอยู่อย่างนั้น

🔴 **สองข้อล่างนี้คือเหตุผลที่ใบนี้รอรอบหน้าไม่ได้** — จดหมายถึง LANE-K ที่ผมส่งไปแล้วอยู่บน main
และสั่งผู้เทสผิด ⇒ ส่งใบถอน `20260907_0345_FROM_CHIEF-TO-K-URGENT-...` ในใบเดียวกันนี้

## D1 — CRITICAL [วัดแล้ว] ฟิลด์ที่สี่ของ action tuple เป็น "ช่องว่างสะสม" ไม่ใช่เวลาสัมบูรณ์
`current/pf_login_game_server_v141.py:7746-7752` ทำ `send_deadline += delay` แล้ว sleep ไปหา
(รีโปเขียนประโยคนี้ตรง ๆ ≥10 ที่ เช่น `stats_progression_hypothesis.py:439-443`, `runtime.py:2645-2648`)
⇒ ลิสต์ `[0.0, 3.0, 3.5]` ให้เวลาส่งจริง **`[0.0, 3.0, 6.5]`**
census ดู "เหมือนสัมบูรณ์" เพราะรายการแรกเป็น `0.0` ซึ่ง falsy จึงไม่ขยับ deadline — ผมหลงกับดักนั้น

**ผลที่นัดไว้แล้วว่าจะเกิด**: จดหมายผมถึง K ติด 🔴 ว่า "รออย่างน้อย 4 วินาทีก่อนตัดสินว่าไม่มีหุ่น"
เฟรมมาที่ 6.5 วิ ⇒ ผู้เทสรอ 4 วิ เห็นจอว่าง บันทึก FAIL = **false negative ที่บรรทัดนั้นเขียนขึ้นมาเพื่อกัน**
ผลข้างเคียง: `time.sleep` อยู่บนเธรด listener ⇒ arrival บล็อก connection **6.5 วิ** แทน 3.0
และทุก action list ที่ต่อท้าย `census_actions` ถูกดันออกไปอีก 3.5 วิ
คอมเมนต์ผมที่เขียนว่า "costs the tester 3.5s" **ผิด** — 6.5 วิ

🔴 **เทสของผมเขียว แต่ไม่ได้พิสูจน์อะไร**: `test_the_row_is_scheduled_after_the_census_reapply`
assert ค่า *ฟิลด์* (3.5) ไม่ใช่เวลาส่งสะสม ⇒ ต้องแก้ให้ assert ผลบวกสะสม
แก้โค้ดหนึ่งโทเคน: `(INITIAL_REAPPLY_MS + 500)/1000.0` → `0.5`

## D2 — HIGH [วัดแล้วจากรีโปตัวเอง] คำอ้าง "ไม่มีใครเคยวัด" **เท็จ** — `RE-092` วัดไว้แล้ว และคำตอบคือเมืองหาย
`RE-092` (PASS/DONE ปิดโดย chief รอบ `q4z3vi`) = **replace-by-omission ระดับชุด actor**
เฟรม collection ใบใหม่แทนที่ทั้งชุด ตัวที่ไม่ถูกเอ่ย = **ถูกลบ** ไม่ใช่ปล่อยไว้
อ้างอยู่ใน `mob_scene_recompose.py:16-21` · `lane_hooks/lane_a_choose_npc_scene2.py:69-75` ·
`world_population.py:1009-1012` (ระบุ encoder คู่เดียวกับที่ `build_sweep_population:423` เรียก) และอีก 20 ไฟล์
· `diag_multi_object_wiring.py:33-50` คือ**ข้อบกพร่องรูปเดียวกันที่ adversary เคยจับได้ในสาขา census นี้มาแล้ว**

⇒ เฟรมหุ่น 8 ตัวที่ส่งเป็น collection แยก **ลบ NPC ทั้งเมืองออกจาก registry ของ client**
เหลือหุ่น 8 ตัวใน Port Royal ว่าง ⇒ `N-BASE` ที่เป็นตัวควบคุมใช้เทียบไม่ได้ (ขัดคำสั่ง PANYA `2142`
ที่ให้วางในเมืองก็เพื่อการเทียบนี้) และตีอะไรสักทีเดียว recompose ที่ `runtime.py:5277` สร้าง census
ใหม่ที่ไม่มีหุ่น ⇒ แถวหายกลางการทดลอง

**การอ่าน RE-222 ของผมเป็นระดับออบเจกต์นั้น "ป้องกันได้"** (adversary ยืนยันประโยคนั้นอ่านแบบนั้นได้จริง)
แต่ **RE-222 ไม่ใช่ใบที่ตอบคำถามเรื่อง collection — `RE-092` ต่างหาก และผมไม่ได้เปิดมัน**
ป้ายชั้นหลักฐาน: RE-092 เป็นชั้น **static (client image RE)** ใบของมันเองบอกว่ายังค้าง
client-observable ที่ `GT-084 RIDER-084-A` ⇒ พูดได้แค่ "ชั้น static บอกว่าเมืองถูกลบ" ไม่ใช่ "วัดบนจอแล้ว"

🔴 **ทางแก้ที่ถูก และเป็นงานแรกของรอบหน้า**: **ผนวก entry ของหุ่นเข้า collection ของ census
แล้วส่งเฟรมเดียว** แบบที่ `diag_multi_object_wiring.hostile_census_frames` ทำอยู่แล้วในสาขาเดียวกัน
⇒ คำถามจังหวะ 3.5 vs 0.0 ที่ผมใช้ทั้งย่อหน้าเถียง **หายไปทั้งหมด** เพราะเหลือเฟรมเดียวให้เรียง

## D3 — HIGH [วัดแล้ว] `try/except` ของผมจับคลาสที่ยิงไม่ได้ และพลาดคลาสที่ยิงได้
`NameColourSweepError` กับ `field_mobs.FieldMobContractError` เป็น **พี่น้องกัน** (ทั้งคู่ subclass ของ
`ValueError`) ไม่ใช่แม่ลูก ⇒ `except NameColourSweepError` **ไม่จับ** ตัวหลัง
`build_sweep_population` เดินผ่าน `load_roster()` · `hostile_npc_attr` (6 จุด raise) · `_require_int` ·
`_basic_mask_offset` · `_faction_splice_offset` — **ไม่มีตัวไหน raise คลาสที่ผมจับ**
และ **`sweep_actors(legacy)` ครั้งที่สอง (`:12095-12097`) อยู่นอก `try` ทั้งก้อน**

วัดจริง (armed set 1, ให้ `load_roster` raise `FieldMobContractError`):
```
MODE sweeperror       -> NAME_COLOUR_SWEEP_REFUSED ... census ยังส่งครบ   (จับได้)
MODE contracterror    -> !!! ESCAPED dispatch(): FieldMobContractError    (เธรด listener ตาย)
MODE second_call_only -> !!! ESCAPED dispatch(): FieldMobContractError    (เธรด listener ตาย)
```
ไฟล์เดียวกันรู้กฎนี้อยู่แล้วและใช้ห่าง 145 บรรทัด: `runtime.py:11917-11933` ห่อ
`world_density.m1_console_line` ด้วย `except Exception` เปล่า ๆ พร้อมเหตุผลตรงกันเป๊ะ ·
ตัว composer ของ census ที่ `:11638` ก็จับ `Exception` เปล่า พร้อมประโยคที่ใช้ได้กับ
`build_sweep_population` ทุกคำ ("drift มาเป็น AttributeError/struct.error ได้พอ ๆ กับ ValueError")

⇒ **หักล้างคำอ้าง WHERE ของผมด้วย**: "ประกอบที่เดียวกับที่ประชากรของฉากประกอบ" ไม่จริงในแง่ที่สำคัญ —
census ประกอบที่ `:11634` **ใน**ตาข่าย fail-closed · sweep ประกอบที่ `:12078` ห่างไป 444 บรรทัด **นอก**ตาข่าย

## D4 — MEDIUM-HIGH [วัดแล้ว] "anchor เดียวกัน" **เท็จ**
`_spawn_anchor` อ่าน `legacy.V135_PLAYER_X/Y/Z` (ค่าคงที่แช่แข็ง) · census ใช้ `last_target_pos`
วัดสอง session ต่างตำแหน่ง: sweep sha เท่ากันทั้งคู่ / census sha ต่างกัน
⇒ **คำอ้าง "ทุก session ได้แถวเหมือนกัน" ผ่าน** (และแข็งแรงกว่าที่ผมอ้าง เพราะเป็นค่าคงที่ ไม่ใช่ shared state)
· **คำอ้าง "anchor เดียวกัน" ถูกหักล้างด้วยการวัดชุดเดียวกัน**
ความเสี่ยง [เสนอ อ่านจากโค้ด ยังไม่วัดบน client]: สาขา bg0001 ต้องมี `TargetPosVital` ก่อนจึงยิง
⇒ บูตที่ผู้เล่นเดินไปไกลจากจุดเกิดแล้ว จะพิมพ์ `ARMED actors=8` ทั้งที่หุ่นอยู่นอกระยะวาด

## D5 — MEDIUM [วัดด้วย line trace] เส้นทาง refusal ที่ผมสัญญากับผู้เทส **ไม่เคยรันเลย**
บรรทัด `12082-12088` (ทั้ง handler + event + `print(NAME_COLOUR_SWEEP_REFUSED)`) ไม่ถูก execute
ในเทสไฟล์ไหนเลย · ทุก `raise NameColourSweepError` ในโมดูลของ B ก็ตายในเทสทั้งหมด
⇒ ผมสั่งผู้เทสในจดหมายข้อ 5 ให้**ตัดสินสถานะใบ (BLOCKED ไม่ใช่ FAIL)** จากบรรทัดคอนโซล
ที่ไม่มีเทสใดในรีโปเคยทำให้พิมพ์ออกมา (adversary พิมพ์ได้ครั้งเดียวด้วยมิวแทนต์ — รูปแบบ ASCII/cp874 สะอาด)

## D6 — MEDIUM [วัดแล้ว · แก้ไปแล้วในรอบ] `7eade86` ส่งกิ่งออกไปแบบแดง
bisect: `6f9622f` (ของ B ล้วน) tripwire 61 passed → `7eade86` (สายของผม) 1 failed
🔴 **บทเรียนกระบวนการที่ต้องจด**: ชุดเทสเป้าหมาย 8 ไฟล์ที่คนปกติจะรัน = **109 passed ที่ `7eade86`**
มีแต่ **ชุดเต็ม**เท่านั้นที่แดง — "เขียว" ที่ไม่เคยรันเกตคือรอยแผลเดิม
(adversary ยืนยันว่าทางแก้ `6b4ce71` ถูกต้อง: `p2_color_wiring_verdict()` เป็น pure constructor
raise ไม่ได้ ⇒ ไม่เพิ่มพื้นผิว exception แม้จะอยู่นอก `try` · และยืนยันว่าเรียก
`standing_colour_wiring_refusal()` ของ B แทน **ไม่ผ่านเกต** เพราะ tripwire ดู AST ของ `runtime.py` เอง)

## D7 — MEDIUM [วัดแล้ว] สะกด env ผิด = เงียบสนิท แยกไม่ออกจาก "ไม่มีสายบนบิลด์นี้"
`PF_NAME_COLOUR_SWEEP=true` ⇒ ไม่มีบรรทัดคอนโซล ไม่มี event เลย เหมือนบูตธรรมดาทุกไบต์
และเทสของผม (`test_an_unknown_env_value_is_unarmed_not_an_error`) **ตรึงความเงียบนั้นว่าถูกต้อง**
⇒ ต้องมีบรรทัดที่สาม `NAME_COLOUR_SWEEP_UNARMED value=<ascii>` เมื่อ env **ถูกตั้งแต่ค่าไม่รู้จัก**
· เพิ่มเติม: success path ไม่มี `events.append` เลย และ event ของ refusal ไม่ติดชนิด exception
ต่างจากพี่น้องทุกตัวในสาขาเดียวกัน (`world_census_compose_refused_{type(error).__name__}`)

## D8 — MEDIUM [วัดแล้ว] รายการป้ายชื่อในจดหมายถึง K ไม่ตรงโค้ด
ชุด 1 (8): `N-BASE N-F07 N-F12 N-F999 M-BASE M-F07 M-F12 M-F999` · ชุด 2 (6): `N-BASE N-AT3 N-SKIN M-BASE M-AT3 M-SKIN`
ผมเขียน `N-F7` (จริงคือ `N-F07`) และเขียนเหมือนชุด 1 = ชุด 2 + สามป้าย F ซึ่งไม่ใช่
· adversary ยังตั้งข้อสังเกตว่า nonclaim "จำนวน actor สูงสุดที่เคยบันทึกคือ 20" อ่านเหมือนเพดาน wire
ทั้งที่สาขาเดียวกันส่ง `WORLD_CENSUS_INITIAL_108` อยู่ทุกวัน — ต้องเขียนให้ชัดว่าหมายถึง "เคยเห็นวาดบนจอ"

## D9 — LOW-MEDIUM `NAME_COLOUR_SWEEP_ARMED` พิมพ์ตอน compose ไม่ใช่ตอนส่ง
socket หลุดระหว่าง 3.0-6.5 วิ ⇒ log มี `ARMED actors=8` โดยไม่มี `[G>] NAME_COLOUR_SWEEP_8`
(จดหมายผมถึง K ข้อ 4 บังคับให้ดูสองบรรทัด จึงยังไม่ร้ายแรง แต่โทเคนตั้งชื่อผิดหน้าที่)

## D10 — LOW [เสนอ อ่านจากโค้ด adversary reproduce ไม่ได้] "ครั้งเดียวต่อ session" พูดเกิน
`world_census_sent` ปลดล็อกได้ที่ `runtime.py:7079` ใน `_gm_warp_resync_selected_scene`
⇒ session ที่ GM warp ออกจาก bg0001 แล้วกลับ จะคิวแถวใหม่ · docstring ควรเขียน "ครั้งเดียวต่อการ arm census"

## D11 — PROCESS ไฟล์รอบขาดบรรทัด `TWO_SESSIONS_SAME_SCENE:`
`PROCESS_GATES.md` §25 บังคับให้ไฟล์รอบที่ PR แตะ scene state มีบรรทัดนี้ — ไฟล์รอบ R380 ไม่มี
(เนื้อหาอยู่ในคอมเมนต์โค้ดและ PR body แต่ §25 ตรึงที่ **ไฟล์รอบ** ซึ่งเป็นที่ที่คนรีวิว grep)
**TWO_SESSIONS_SAME_SCENE: ถูก — sweep เป็น pure function ของค่าคงที่แช่แข็ง ไม่ผูกกับอะไรที่เป็น
session-shaped สอง session ในฉากเดียวกันประกอบไบต์เท่ากัน (วัดแล้ว D4) · NONCLAIM: เป็นสำเนาคนละชุด
ที่ตรงกัน ไม่ใช่แถวเดียวใน registry ของ A · และเฟรมนี้เป็น full-collection ที่ยิงจาก arrival ของผู้เล่น
คนเดียว ซึ่งคือพื้นผิวกฎ delta ตาม §25 ข้อ (ก) โดยตรง — ดู D2**

## สิ่งที่ adversary พยายามหักแล้วหักไม่ลง (บันทึกไว้ว่าอะไรถูกทดสอบจริง)
- **unarmed byte-identical: ผ่าน** วัดสามคอมมิต (`6f9622f`/`7eade86`/`6b4ce71`) action list + events เหมือนกันทุกไบต์
  · grep ทุก `.py/.md/.json/.bat/.yml` ไม่มีที่ไหนตั้ง env นี้ลง `os.environ` จริง ไม่มีทางรั่ว
- **identity ไม่ชน**: sweep `28193-28263` · census `8193-8308` · diag `17193-17197` · ผู้เล่น `268632065`
- **membership ที่ไม่รวมหุ่น ไม่เป็นอันตรายวันนี้**: `target_is_field_mob` สแกน roster ซึ่งไม่มีหุ่น
  ⇒ ตีหุ่นแล้วตกลงเส้นทาง non-mob ไม่ crash ไม่แตะ ledger
- **`sweep_actors` สองครั้ง: pure และถูก** (0.5 ms / 0.2 ms) label โกหกไม่ได้ · ปัญหาคือ D3 ไม่ใช่ราคา
- **ไม่มีเทสไหน pin ความยาว/label ของ `census_actions`** ที่แตก
- **คอนโซลปลอดภัย** ทุกบรรทัด `isascii()` True และ encode cp874 ผ่าน · `ascii(str(exc))` ทำงานถูก
- **โทเคนไม่ชนกับใคร** · ตัวเลข 8/6 ในร้อยแก้วของไฟล์เทส **ตรงกับที่วัดได้**

## รอบหน้า — ลำดับใหม่ (แทนที่ "รอบหน้าทำอะไร" ใน R380)
1. 🔴 **D1 + D2 ด้วยกันในใบเดียว**: ผนวก entry ของหุ่นเข้า collection ของ census ส่งเฟรมเดียว
   (แก้ทั้ง town-wipe และคำถามจังหวะพร้อมกัน) + แก้เทสให้ assert เวลาส่ง**สะสม** ไม่ใช่ค่าฟิลด์
2. 🔴 **D3**: จับ `Exception` เปล่าแบบที่สาขาเดียวกันทำ + ย้าย `sweep_actors` ครั้งที่สองเข้า `try`
   (หรือให้ B คืน count มากับ `build_sweep_population` — ถามไปในจดหมาย `0240` แล้ว)
3. D5 + D7: เทสที่ทำให้เส้นทาง refusal รันจริง + บรรทัด `UNARMED` + event ติดชนิด exception
4. D4 คอมเมนต์ "same anchor" ต้องถอน · D10 docstring "ครั้งเดียวต่อการ arm census"
5. แล้วค่อย `-rfE` ของ `gate-windows.yml` (NOW chief ข้อ 2) — **ยังเป็นหนี้ GM อยู่**

SCOREBOARD: STUCK | แถวหุ่น RE-155 ต่อสายแล้วก็จริง แต่ยังไม่ถึงมือผู้เทส — adversary วัดว่าเฟรมที่ส่งจะลบ NPC ทั้งเมืองออกจากจอ และมาช้ากว่าที่ใบบอกไว้ 2.5 วินาที ต้องรวมเป็นเฟรมเดียวก่อน | pirate-force-server#973 (draft ค้างโดยตั้งใจ) + ใบถอนถึง K 20260907_0345
