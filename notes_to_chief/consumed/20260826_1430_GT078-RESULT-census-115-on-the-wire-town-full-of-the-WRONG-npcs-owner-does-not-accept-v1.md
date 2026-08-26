[ถึง: **chief / สาย E (PLATFORM)** · **สาย A (WORLD)** · **COO** · cc: สาย B · Panya | จาก: **มือเขียนแทน Panya (เซสชัน attended [กะ1])** · เขียน 2026-08-26T14:30+07:00 · รอบเทส 12:55–13:37 +07:00]

# `GT-078` M1-V1-ACCEPTANCE — ผล: **ชั้น wire ผ่านครบ (115/115 ออกสาย · ไม่มีแฟล็ก · 37 นาทีไม่หลุด) · เจ้าของเห็น NPC เต็มเมืองจริง — แต่เจ้าของ *ไม่รับ* เป็น `v1` เพราะ NPC ที่โผล่ "ไม่ใช่ตัวที่ควรอยู่ตรงนั้น" ทุกตัว**

`OBSERVER_CONFIRMED: 2026-08-26T14:10+07:00` (เจ้าของนั่งหน้าจอเองตลอดรอบ · เธอขับตัวละครเองตั้งแต่ 13:25 · คำยืนยันและคำตัดสินของเธอมาเป็นข้อความยาวหนึ่งฉบับ ~14:10 คัดคำต่อคำไว้ในข้อ ⑥)

---

## ① เช็คลิสต์ปลดบล็อก 5 ข้อ + `BOOT_COMMIT`

| ข้อ | ผล |
|---|---|
| 1 การต่อสายอยู่บน `main` | ✅ `PR #56` (rebuild ของ #41) merge 12:28 · `main` = `d84118ae` มี `world_census_enabled` |
| 2 resolver | รอบแรก 12:43 **ปฏิเสธทุก candidate** (merge commit บน main ไม่มี verdict ของตัวเอง · PR head ทุกใบ tree ต่างจาก main ใน runnable code) ⇒ สั่ง `workflow_dispatch` gate บน `main` → เขียว run 32935255793 → รอบสอง 12:54 **`BOOT_COMMIT: d84118ae98041550ead7b8b327e29354eb16dd21`** (mainline · verdict ของตัวเอง) · `CODE_DELTA_vs_main = 0` |
| 3 ห้า grep (job 1192 · `outbox\1192_gt078_hold_and_resolve.utf8.txt`) | บรรทัด1 `world_census_enabled = (` … `not active_lanes and second_password_mode == "required"` runtime.py:770-772 **GO** · บรรทัด2 `build_world_population` runtime.py:4129 **GO** · บรรทัด3 `WORLD_CENSUS_INITIAL_` runtime.py:4179 **GO** · บรรทัด4 `--world-census-actors` app.py:132 (หนึ่งบรรทัด · type=int default=None) **GO** · บรรทัด5 `V134_P0_P30_P91_ISOLATED` v141 **4 บรรทัด** (4296/4302/6087/6088) **GO** |
| 4 ที่อ่าน `composed` | ✅ บรรทัด `WORLD_CENSUS …` + ป้าย `[G>]` ทั้งสองใบ (ข้อ ③) |
| 5 เจ้าของนั่งเอง | ✅ Panya |

🔴 **เรื่องที่ใบเทสเขียนไว้ผิดและต้องแก้:** ใบ `GT-078` บรรทัด "client: `-SecondPasswordMode bypass` (ท่ามาตรฐาน)" **ขัดกับกฎกักกันของ R173** (`runtime.py:771` — สำมะโนเปิดเฉพาะเมื่อ `second_password_mode == "required"`) ⇒ รอบนี้บูต **ไม่ใส่** `--second-password-mode` เลย · ผลข้างเคียงที่วัดได้: ไม่มีหน้ารหัสผ่านขั้นสองโผล่ตอนล็อกอิน (เจ้าของบอกว่ามันโผล่เฉพาะตอนลบตัวละครและเปิดกระเป๋า Hotkey I) · 🔴 **`PLAY_PIRATE_FORCE.bat` / `9001_play_boot.ps1` ใส่ `bypass` อยู่ ⇒ โหมดเล่นของเจ้าของตอนนี้ได้เมือง 3 ตัว** — chief ต้องตัดสินว่าจะแก้ launcher หรือแก้กฎกักกัน

## ② `CommandLine` ของโปรเซสเซิร์ฟเวอร์ (ทั้งบรรทัด · job 1193)
```
"C:\Windows\py.exe" -3 -u -m pirateforce_foundation.app --db "C:\Users\Panya\Desktop\Pirate Force\Pirate Force ServerProject\state\run_gt078_20260826_125511.sqlite3" --capture-root "C:\Users\Panya\Desktop\Pirate Force\GameClient\capture_gt078_20260826_125511"
```
ไม่มี `-scenario` · ไม่มี `--export-events` · ไม่มี `--second-password-mode` · ไม่มี `--world-census-actors` · console ไม่มี label เลนหัววัด (`HYP_`/`ARENA_`/`SCENE_`) แม้บรรทัดเดียว ⇒ **กฎข้อ 1 ผ่าน**

## ③ สี่เลข — แยกกัน ห้ามยุบรวม
| เลข | ค่า | ที่มา |
|---|---|---|
| **`composed`** | **115** | `WORLD_CENSUS assembled=115/115 wire=115 bodies=ok pc=17928B frame=17942B anchor=(-9110.456,-2611.582,186.000) reapply_ms=3000 source=full_census shortfall=none` (console:1394) |
| **`sent`** | **115 × 2 เฟรม** | `GAME_LIVE.txt`: `13:15:11.923 SENT label=WORLD_CENSUS_INITIAL_115 frame_bytes=17942` · `13:15:14.923 SENT label=WORLD_CENSUS_REAPPLY_115 frame_bytes=17942 delay=3.00` · ป้าย `[G>] WORLD_CENSUS_INITIAL_115 (17942 bytes; late=0.8 ms)` / `[G>] WORLD_CENSUS_REAPPLY_115 (17942 bytes; late=0.8 ms)` · **ไม่มี `V134_*_ISOLATED_*` ทั้งบูต** |
| **`seen_max_frame`** | **6** | `GT078_CENTER_FULLRES_20260826_132851.png` — หุ่นเกราะส้ม 1 · สัตว์ปีก-ใบไม้ 3 · ดอกไม้ชมพู 1 · (ป้าย "…d Sailor" ตัวอยู่นอกเฟรม ไม่นับ) · เจ้าของนับด้วยตาแล้วบอก "เห็นหลายตัว สอดคล้องกับทุกจุดตำแหน่งบน minimap" |
| **`seen_tour_total`** | **≈ 18 (±2)** | นับตัวที่ *เห็นร่าง* แยกตามรูปร่าง+ตำแหน่ง ตัดซ้ำด้วยตำแหน่งบนจอ/มินิแมพ: ท่าเรือ 4 (ชุดขาว-ฟ้า · หุ่น Warden · โจรสาวผมส้ม · ทหารข้างรถเข็นแดง) · ใจกลางเมืองจากภาพของผม 5 (เกราะส้ม · สัตว์ปีก-ใบไม้ ×3 · ดอกไม้ชมพู) · จากสกรีนช็อตเจ้าของ 9 (ชุดม่วง · หมวกแดง · Unemployed Sailor · สัตว์ดอกไม้แดง · ตัวเล็ก Mystery Prisoner · ตัวที่น้ำพุ · ตัวส้มขวา · ตัวเล็ก Old Prisoner · Apprentice Witch) · ±2 เพราะ "ดอกไม้ชมพู" กับ "สัตว์ดอกไม้แดง" อาจเป็นตัวเดียวกันคนละมุม และตัวที่น้ำพุอาจซ้ำ |

**ชั้น wire ยังพิสูจน์ไม่ได้ว่ามีอะไรขึ้นจอ · ชั้นจอยังบอกไม่ได้ว่าเซิร์ฟเวอร์ส่งกี่ตัว** — ทั้งสองข้อคงไว้ตามนิยามใบ

## ④ ตารางต่อจุด + `G-FRAME`

`T0 = 2026-08-26T13:02:50+07:00` (±5 วิ — เฟรมที่ HP bar + minimap + "Port Royal" + แชต online ครบ ในสกรีนช็อตของผม · `GAME_EVENTS`: TeleportVital 13:02:19.66 · **วิดีโอเป็นกรรมการ chief ปรับ T0 ได้จากไฟล์ .mkv**)

| จุด | HUD X/Y | เวลา (+07) · `t` | นับได้ | ไฟล์ |
|---|---|---|---|---|
| **S0** จุดเกิด | -8,553 / -2,579 | 13:04:26 · +96.7 | **0** (เจ้าของกวาดกล้อง 4 ทิศเอง · "S0 เสร็จ เห็น 0 ตัว") — **สำมะโนยังไม่ถูกส่ง** เพราะยังไม่มี TargetPos | `GT078_S0_FULLRES_20260826_130421.png` |
| **S1** ฝั่ง Navy Transfer | -9,194 / -2,616 | 13:16:11 · +799 | 1 ข้างตัว (ชุดขาว-ฟ้า) ทันทีที่สำมะโนถึง | `GT078_S1_FULLRES_20260826_131609.png` |
| **S1b** หันไปทางสถานี | -9,444 / -2,950 | 13:20:33 · +1060 | 4 (Warden หุ่นใหญ่ **นอนราบกับพื้น** · ชุดขาว-ฟ้า · โจรสาวผมส้ม · ทหารข้างรถเข็น) + ป้าย "Marine Transport Station" | `GT078_S1b_FULLRES_20260826_132030.png` |
| ⛔ ตกน้ำ | -9,764 / -2,614 → -9,762 / -1,817 | 13:22–13:25 | — (ดูข้อ ⑩) | (ในวิดีโอ) |
| **S-CENTER** ใจกลางเมือง (เจ้าของพาไป) | **11,865 / 6,147** | 13:28:52 · +1561 | **6** | `GT078_CENTER_FULLRES_20260826_132851.png` |
| ภาพเจ้าของ ×4 (ในเกม F-key) | 11,865 / 6,147 (หมุนกล้อง) | 13:33:02 / :10 / :39 / :58 · +1812 / +1820 / +1849 / +1868 | 4–5 ต่อเฟรม + ป้ายชื่อ 8 ป้าย | `GameClient\Data\ScreenShot\20260826_1333{02,10,39,58}.png` |
| **POST** ก่อนออก | 11,865 / 6,147 | 13:36:09 · +1996 | 3 | `GT078_POST_FULLRES_20260826_133606.png` |

```
FRAME: GT078_S0_FULLRES_20260826_130421.png      t=+96.7   จาก T0=2026-08-26T13:02:50+07:00  dist=unmeasured ถึง (ไม่มี NPC ในเฟรม)
FRAME: GT078_S1_FULLRES_20260826_131609.png      t=+799.0  จาก T0=2026-08-26T13:02:50+07:00  dist=unmeasured ถึง NPC ชุดขาว-ฟ้าข้างตัว
FRAME: GT078_S1b_FULLRES_20260826_132030.png     t=+1060.0 จาก T0=2026-08-26T13:02:50+07:00  dist=unmeasured ถึง Warden / Marine Transport Station
FRAME: GT078_CENTER_FULLRES_20260826_132851.png  t=+1561.0 จาก T0=2026-08-26T13:02:50+07:00  dist=unmeasured ถึง กลุ่ม NPC 6 ตัวรอบลาน
FRAME: 20260826_133302.png (ในเกม)               t=+1812.0 จาก T0=2026-08-26T13:02:50+07:00  dist=unmeasured ถึง Unemployed Sailor / สัตว์ดอกไม้แดง
FRAME: 20260826_133339.png (ในเกม)               t=+1849.0 จาก T0=2026-08-26T13:02:50+07:00  dist=unmeasured ถึง Old Prisoner / Apprentice Witch
FRAME: GT078_POST_FULLRES_20260826_133606.png    t=+1996.0 จาก T0=2026-08-26T13:02:50+07:00  dist=unmeasured ถึง Apprentice Witch
UNMEASURED_DIST: 7/7
```
🔴 `UNMEASURED_DIST` เกินครึ่ง ⇒ **ตามกฎ G-FRAME chief ไม่บริโภคใบนี้เป็นผล "ปิดใบ" จากเฟรม** — และไม่จำเป็น เพราะคำตัดสินของใบนี้มาจากเจ้าของโดยตรง (ข้อ ⑥) ไม่ได้มาจากการอ่านเฟรม · ระยะวัดไม่ได้เพราะ HUD ไม่แสดงพิกัดของ NPC และรอบนี้ไม่มี `--export-events`

## ⑤ กฎข้อ 2 (สะสม) ทีละบรรทัด
- ล็อกอิน **ผ่าน** (12:56 LoginVerify → ACK) · หน้าเลือกตัวละคร **ผ่าน** (12:59:09 StartGame) · เดิน `W/A/S/D` + หัน `Q/E` **ผ่าน** (105 TargetPosVital) · **อยู่ในแมพ 13:02:50 → 13:36:33 = 33 นาที 43 วิ ไม่หลุด ไม่ค้าง ผ่าน** (session แถวเดียว opened 12:59:09.535 closed 13:36:33.554 +07 · ไม่มี reconnect · ไม่มี GAME connection ที่สอง)
- **NO-CRASH** — เจ้าของหมุนกล้องด้วยคลิกขวาลากตลอดรอบ กล้องหมุนตาม (ผมใช้ Q/E ซึ่งไม่นับเป็นตัวเช็ค)
- คลิก NPC: มี `TargetVital actor_id=0x0000000010010001` ที่ 13:33:27 แล้ว clear 1.5 วิถัดมา (`GAME_EVENTS` seq 3-4) — เจ้าของคลิกตัวหนึ่งเพื่อดู heading · **ไม่มีเฟรมสำมะโนถูกส่งซ้ำ** (`[G>]` รวมทั้งไฟล์ยังเป็น 9) ⇒ ข้อกังวล R173 ⑦-4 "คลิกละ 17.9 KB" **ไม่เกิดในรอบนี้** [วัดแล้ว · เคสเดียว]

## ⑥ ประโยคของเจ้าของ — คัดคำต่อคำ (ข้อความ ~14:10 +07)
> "จากการทดสอบรอบนี้ ฉันเห็น npc เกิดขึ้นมาในเมืองหลายตัว สอดคล้องกับทุกจุดตำแหน่งบน minimap ซึ่งเข้าใจบรรยากาศเดิมของเซิฟเวอร์ดั่งเดิมมาก แต่มีหลายจุดที่มันยังไม่ใช่"
>
> "อย่างแรก npc ที่เกิดจริง บางตัวมีชื่อ บางตัวไม่มี ซึ่งตัวที่มีชื่อ ก็ไม่ใช่ชื่อจริงๆ ของมันด้วย แต่เป็น Title ของมัน เช่น สาวโจรผมทองชุดดำ Marine Transport Station คือชื่อที่ขึ้นอยู่ตอนนี้ของ npc ตัวนึงแถวท่าเรือ (ชื่อเป็นสีฟ้าด้วย) แต่จริงๆ แล้วชื่อของมันจริงๆ ที่ไม่ขึ้นในนี้ คือ "Columbus" ควรขึ้นเป็นชื่อสีเหลือง และมีคำว่า Marine Transport Station เป็นสีฟ้าขึ้นอยู่เหนือชื่อสีเหลืองของมันอีกทีนึง และตำแหน่งของมันจริงๆ อยู่จะอยู่แทนที่ Navy Transfer ในตอนนี้"
>
> "เรื่องที่สำคัญที่สุดอันดับ 1 คือ npc ทุกตัว (ขอย้ำว่าทุกตัว) ไม่ใช่ npc ที่ควรอยู่ในเมืองนี้ หรือในตำแหน่งนั้น จริงๆตามการอ้างอิงจากเซิฟเวอร์ดั่งเดิม ตำแหน่งจุดเกิดของ npc แต่ละตัวตอนนี้ถูกต้องหมด แต่ตัวตัวที่เกิดจริงๆ "ไม่ใช่เลย""
>
> "npc ดอกไม้สีแดง ที่จริงควรจะเป็น npc ชื่อ Sase และ title คือ Guild Assistant ในขณะเดียวกัน npc Unemployed Sailor ในตอนนี้ก็ควรจะเป็น npc ชื่อ Hields และ title คือ Guild Administrator หากอ้างอิงค์จาก capture จาก server ต้นฉบับจริง จะเห็นว่าตำแหน่งหน่ะถูกต้อง แต่ npc หน่ะ "ไม่ใช่เลย""
>
> "server จริงๆจะไม่มี npc (หรือ monster) ปรากฏขึ้นมาในเมืองเยอะขนาดตอนนี้ จำนวนอาจใกล้ๆเคียง แต่ไม่เยอะขนาดตอนนี้ ฉันว่าเป็นเพราะว่า ในสถานะ server จริงๆ ปกติ npc ,monster บางส่วนใน map นี้ บางตัวอาจจะถูก hidden ไว้เฉพาะในสถานะที่ตัวละครนั่นๆ มี quest หรือภาระกิจที่ค้างหรือกำลังดำเนินการไว้อยู่ npc ก็จะ hide / unhide ให้ตรงกับสถานะปัจจุบันของเรา และแน่นอนจะมีกลุ่มที่เป็น npc มาตรฐาน ที่ไม่เกี่ยวข้องกับเควส และมีไว้ใช้เปิดฟังชั่นสำคัญแช่ง ตลาด ร้านค้า ตีบวกอุปกรณ์ เข้าดันเจี้ยน เข้า guild map พวกนี้ก็ควรจะอยู่ค้างในเมืองอยู่แล้วตลอด"
>
> "npc ใน map ในเซฟิเวอร์เดิม บางตัวสามารถเดินวนๆ ได้ แต่ npc ที่เซิฟเวอร์เราตอนนี้ ไม่มีตัวไหนเดินวนๆออกมาเลย (หายใจได้ทุกตัวยังปกติ ยังไม่เจอตัวไหนเป็นท่า T pose และเวลาคลิกที่ตัว npc ก็ heading หันหนามาทางเรา ถูกต้องแล้ว) แต่ยังขาดการเดินไปมาในระยะของมันอยู่"
>
> "ครั้งหน้าฉันตั้งความหวังว่าจะมาให้เทสใหม่ก็ต่อเมื่อ npc เป็นตัวที่ถูกต้องแล้ว (อย่างน้อย Unemployed Sailor ตอนนี้ก็ควรจะเป็น Hields - Guild Administrator แล้ว) ไปจัดการซะ"

**ประโยคกฎข้อ 4 ("ผู้เล่นทำอะไรได้ที่เวอร์ชันก่อนทำไม่ได้") — เจ้าของยังไม่ได้ให้ประโยคนี้** และไม่ได้พูดว่า "เมืองมีชีวิตแล้ว" · เธอพูดว่า "เข้าใจบรรยากาศเดิม…มาก แต่…ยังไม่ใช่"
📎 เจ้าของอ้างถึง "capture จากเซิร์ฟเวอร์เดิมจุดเดียวกัน" (Sase / Hields) — **ผมยังไม่ได้รับไฟล์ภาพนั้น** ขอให้เจ้าของวางลง `evidence_screens\` หรือส่งมาในแชต แล้วผมจะเติม path+sha ลงใบนี้ (จนกว่าจะมี ให้ถือว่าเป็นคำให้การของเจ้าของ [stated] ไม่ใช่ [วัดแล้ว])

## ⑦ คำตัดสิน — แถวไหน
- ชั้น (1): **ผ่านครบ** · ชั้น (2): `seen` ≫ 3 หลายจุดหลายทิศ · กฎข้อ 2 ผ่านครบ · ≥10 นาที ⇒ ตามตาราง = **V2 SHIPPED-WITH-CAP** (`seen_max_frame 6` < `sent 115` · ห้ามเรียกว่าเพดานไคลเอนต์)
- 🔴 **แต่ V2 บอกว่า "PASS ของ M1 ได้ (เจ้าของตัดสิน)" — และเจ้าของตัดสินว่า *ไม่รับ*** ⇒ **`M1 เมืองมีชีวิต` ยังไม่ถึงตามเจ้าของ · `v1` ไม่ประกาศ · ห้ามเขียนบล็อก v1 ลง `SERVER_VERSIONS.md`**
- เหตุที่ไม่ใช่ V3/V4: เมืองไม่ได้ "เหมือนเดิม" และไม่มี regression — ปัญหาคือ **ความถูกต้องของ identity ของ actor ต่อ placement** ซึ่งใบ GT-078 ไม่ได้วัด (nonclaim ⑪ ของใบ) และเจ้าของยกมาเป็นเกณฑ์รับ
- **ผลนี้ตกใครแทน:** ตาราง placement 115 ตัว (`bg0001`) ส่ง "actor ที่ถูกวาง ณ จุดนั้นในตารางของเรา" ซึ่งเจ้าของยืนยันว่า **ตำแหน่งถูก ตัวผิดทุกตัว** ⇒ เป็นเรื่อง **การแมป placement → identity/name/title** (สาย A + RE) ไม่ใช่ wiring ของสาย E

## ⑧ PLAYBOOK ข้อ 13 — สีป้าย (อ่านจาก full-res / ภาพในเกมของเจ้าของ · `evidence_layer=eye`)
| ภาพ | ป้าย | สี |
|---|---|---|
| S1b | ชื่อตัวเอง `Arena01` (เหนือหัว) | ส้ม-เหลือง |
| S1b | `Marine Transport Station` (บนตัวชุดดำผมทอง) | ฟ้า |
| S1b | `Warden` (บนหุ่นใหญ่ที่นอนราบ) | ขาว-ฟ้าอ่อน |
| S1b / CENTER | NPC ชุดขาว-ฟ้า · โจรสาวผมส้ม · ทหาร · เกราะส้ม · สัตว์ปีก-ใบไม้ ×3 · ดอกไม้ชมพู | **ไม่มีป้าย** (เขียนออกมาตามกฎ) |
| CENTER | `…d Sailor` (ตัวนอกเฟรม) | ฟ้า |
| 133302 | `Gold Shark Leader` · `Naval Con…` · `…ive Traders` · `Bomber` · `Unemployed Sailor` | ฟ้า ทั้งหมด |
| 133310 | `Mystery Prisoner` · `Bomber` | ฟ้า |
| 133339 / POST | `Old Prisoner` · `Apprentice Witch` | ฟ้า |
| ทุกภาพ | ชื่อไอเทมบนพื้น · ชื่อผู้เล่นอื่น · ป้ายสีเหลือง | **ไม่มี** |
อ่านไม่ออก/ถูกบัง: 2 ป้าย (`Naval Con…`, `…ive Traders` ถูกตัดขอบ) · 🔴 **ไม่พบป้ายสีเหลืองแม้แต่ป้ายเดียวทั้งรอบ** — เจ้าของบอกว่าเซิร์ฟเวอร์เดิม NPC มี **ชื่อสีเหลือง + title สีฟ้าอยู่เหนือชื่อ** สองบรรทัด · ของเรามีบรรทัดเดียวสีฟ้า (ซึ่งเจ้าของระบุว่าคือ title ไม่ใช่ชื่อ) · **จดสีอย่างเดียว ไม่สรุปสาเหตุ (`RE-067`)**

**ค่าสำหรับ `REAL_SERVER_DIVERGENCE.tsv` (chief เติมเอง · ห้ามผมแก้ไฟล์):** หนึ่งแถวต่อป้ายข้างบน · `evidence_layer=eye` · `open_ticket=RE-067` · `blocks_promotion=no` · `divergence`: (a) NPC label = title only, blue, no yellow name line · (b) identity at placement differs from original (Columbus/Marine Transport Station expected at Navy Transfer spot · Hields/Guild Administrator expected where Unemployed Sailor stands · Sase/Guild Assistant expected where red flower creature stands) · (c) no NPC wanders · (d) more visible actors than the original at the same time (owner: quest-gated hide/unhide + standard function NPCs)

## ⑨ census `[G>]` ทั้งไฟล์ (9 บรรทัด)
```
LOGIN_VERIFY_ACK_ONCE (55) · FOUNDATION_CHARACTER_LIST_ONCE (265) · FOUNDATION_SELECTED_START_GAME (418) · V113_TELEPORT_SCENE1_STABLE_ZERO_TARGET_ONCE (73) · RUNTIME_RES_ACK_FIRST_REQ (24) · V99_SHOW_MESSAGE_LOCAL_SERVER_ONLINE (102) · V100_MUSIC_CONTROL_CURRENT_SCENE (39) · WORLD_CENSUS_INITIAL_115 (17942) · WORLD_CENSUS_REAPPLY_115 (17942)
```
`ErrorData=28317` = **0** · traceback **0** · stderr **0 B** · TargetPosVital ขาเข้า 105 · `GAME_EVENTS_LIVE`: TeleportVital 13:02:19 · ActionVital 13:25:41 · TargetVital 13:33:27 (+clear)

## ⑩ ข้อสังเกตฟรี + สิ่งที่ผมทำผิด
1. 🔴 **มือเขียนแทนพาตัวละครตกน้ำ 13:22** (หัน Q/E แล้วเดิน W ที่ขอบท่า) — อยู่ในน้ำใต้กำแพงท่า (-9,764/-2,614 → -9,762/-1,817) ปีนกลับไม่ได้ ~3 นาที · เจ้าของรับคีย์บอร์ดไปพาขึ้นบกและไปใจกลางเมืองเอง · **ผิดกฎ "ห้ามลงน้ำ" ของใบ** · ข้อมูลฟรีสำหรับ `RE-073`: ตัวละครลอยที่ระดับน้ำ HP ไม่ลด เซิร์ฟเวอร์รับ TargetPos ต่อ ไม่มี event ผิดปกติ
2. 🔴 **คำสั่งเจ้าของ (บันทึกเป็นกฎ):** *"ไปเทสต์ใจกลางเมือง … คราวหน้าอย่ามาเทสต์แถวนี้อีก"* — ท่าเรือแคบ ของบังกล้อง ตกน้ำง่าย ⇒ **จุดมาตรฐานรอบหน้า `S-CENTER = X 11,865 · Y 6,147`** · PLAYBOOK ของใบ attended ทุกใบต้องย้าย S0/ทัวร์มาที่นี่ (ขอ chief/pf-queue-author แก้ P0/P1 ในใบที่ยังไม่รัน)
3. `Warden` (หุ่นใหญ่หน้าสถานี) **เรนเดอร์นอนราบกับพื้น** ขณะที่ตัวอื่นยืนปกติ — จดไว้ ไม่สรุป (อาจเป็น heading/orientation ของแถวนั้น · D4 ของ R173 พินเฉพาะ sha ไม่ได้พินท่า)
4. หลังก้าวแรก 13:15 NPC ชุดขาว-ฟ้าโผล่ **ข้างตัวทันที** และมินิแมพเต็มไปด้วยจุด — เจ้าของยืนยัน "สอดคล้องกับทุกจุดตำแหน่งบน minimap"
5. สำมะโนถูกยิงช้า (T0+742 วิ) เพราะเจ้าของกวาดกล้องอย่างเดียว 12 นาทีโดยไม่ก้าว — ตรงกับกับดักที่ใบเตือน ("เงียบจนกว่าจะขยับตัว") **ไม่ใช่ความผิดปกติ**
6. เจ้าของกด F-key ถ่ายภาพในเกม 4 ใบ (ไม่ใช่การพิมพ์ตัวอักษร) และ ActionVital 1 ใบที่ 13:25:41 — ไม่มีผลข้างเคียงที่วัดได้

## ⑪ วิดีโอ + ⑫ ไฟล์/sha256
`evidence_video\1193_gt078_FULLROUND_20260826_125514.mkv` · 1920×1080 · 30 fps · duration 2524.133 s · **nb_read_frames 24,941 เทียบ 75,724 ที่คาดจาก duration×fps ⇒ "หาย" 50,783 เฟรม** (ตัวเลขตามสูตรใบ · น่าจะเป็น VFR/ตัดเฟรมซ้ำของ recorder — nonclaim ไม่ได้พิสูจน์ · chief เทียบกับรอบก่อน ๆ ได้) · start=2026-08-26T12:55:15.001 (ห้ามใช้เป็นสมอเวลา)
```
A225791B0EA4ECECF3F5FC1ED3BB11AF4FCCFF39E4B7D1FC3C259249EB9FC2ED  381336611  pf_bridge\evidence_video\1193_gt078_FULLROUND_20260826_125514.mkv
817BF6019218165E6B434BBCAB080CE06987126BF69A0B6F3020F43257D5482E  2541802  pf_bridge\evidence_screens\GT078_S0_FULLRES_20260826_130421.png
AF1B58D42A6F97F17CB3096A77C23CFBC6A74A21547B952CD21B857E03D2BFE2  2043169  pf_bridge\evidence_screens\GT078_S1_FULLRES_20260826_131609.png
16474F7C5E98347935785C6E50FBA20BF7C0D4EC7CDC3F126B753BE180ED2A26  2626572  pf_bridge\evidence_screens\GT078_S1b_FULLRES_20260826_132030.png
D8C8CA7C7EE9A32D04B1B2C40ACFF0C510F4227E61FBFB331428329B56C344F2  2168082  pf_bridge\evidence_screens\GT078_CENTER_FULLRES_20260826_132851.png
7E73CD562EB5E91FF1A2506EE26FC91882F5B9640AF5466B22019B1DD91DB2DC  2621332  pf_bridge\evidence_screens\GT078_POST_FULLRES_20260826_133606.png
F9D9B295939F95A4A9998C4B9D79BCB14113F23E87A29312FA1E3307D3EB16A2  1656986  GameClient\Data\ScreenShot\20260826_133302.png
8784ACCDCBFB319E7CB367BF4DC7C876660A0E18F973FF9FA47F15CF58DD4FBB  1660752  GameClient\Data\ScreenShot\20260826_133310.png
3A71AE019B88A4D698E92F0E934257D40618A3A986DB4B5D6886E3396CAFBE90  1791242  GameClient\Data\ScreenShot\20260826_133339.png
C7C299B6C72146BF7C711AD35D9BF627BF9EA028C93EFD3F795104443B7228EF  1778518  GameClient\Data\ScreenShot\20260826_133358.png
028102E990EFD9F72A2A501F3B3FDFB962D252929F28DA8F7168702D8F507D95  399713  GameClient\capture_gt078_20260826_125511\server_console_live.out.txt
E3B0C44298FC1C149AFBF4C8996FB92427AE41E4649B934CA495991B7852B855  0  ...\server_console_live.err.txt
92C13F5E6AAAFB309FCCC057BD7CA577483E0EAE7C3C7D77A3F350957F1F1951  254531  ...\capture_v141\GAME_LIVE.txt
106EA6187D06AFC91CDA4E45F2AA010A0CABB8A05EEF324BF0F157EA37197B9F  1647  ...\capture_v141\GAME_EVENTS_LIVE.txt
B4C4CC0136968AC76FDFC5CBBE584A6A73101F8B7920A360A34D2259CBAFBFC6  2284973  ...\capture_v141\GAME_20260826_125909_581038_59390.txt
E12D3C67FBD64BD004ED3CA4E1DE31231ECEC3BD4EAC002CFEB5234970CF8FE2  2326  ...\capture_v141\LOGIN_20260826_125601_119705_55873.txt
D3F813C08955992CA80AA33B3CA2CE5AE3E603761C772BA72C3175979002BF7F  86016  Pirate Force ServerProject\state\run_gt078_20260826_125511.sqlite3  (เก็บไว้ให้ chief re-derive)
4FF37060D3A2E876A41A479A348E062557D6C2FA2FF355548FAF81830A548454  86016  pf_bridge\backup\pirateforce_before_GT-078_20260826_125511.sqlite3
```

## ⑬ เวลา / DB / teardown
boot stamp 12:55:11 · server up 12:55:34 · client window 12:55:35 · login 12:56 · StartGame 12:59:09 · T0 13:02:50 · census 13:15:11.9 · ตกน้ำ 13:22 · S-CENTER 13:28 · ออกเกม 13:36:33 · teardown 13:36:56–13:37:38 **exit 0** (TEMPLATE_teardown_generic: BEFORE listeners 2 → AFTER 0 · ctrl-c helper exit 0 · stopped ×1 · ready ×2 · traceback 0)
`run_gt078_20260826_125511.sqlite3`: `integrity_check ok` · fk 0 · sessions(selected) **11 → 12** (+1 ตามเกณฑ์) · `max(lease_generation)` **12 → 13** · แถวใหม่ `fafa5eb8…` opened 05:59:09.535Z closed 06:36:33.554Z
canonical `state\pirateforce.sqlite3` sha256 **ก่อน = หลัง = `4FF37060D3A2E876A41A479A348E062557D6C2FA2FF355548FAF81830A548454`** = `CANON_SHA.txt` · ไม่ถูกเปิดตลอดรอบ · `LOCK_GAME` ปล่อยโดย job 1196 หลังใบนี้

## ⑭ `BUILD_IMPACT`
```
BUILD_IMPACT: ไม่มี v1 — ชั้นที่ "พัง" ไม่ใช่ composed/sent/seen (115/115/6) แต่คือ "identity ของ actor ต่อ placement" ซึ่งใบนี้ไม่ได้วัดและเจ้าของใช้เป็นเกณฑ์รับ
              -> cc ห้ามเขียนบล็อก v1 · seen_max_frame=6 ใช้เป็นเลขตั้งต้นงบประชากรได้ตามใบ
              -> งานใหม่ที่เจ้าของสั่ง ("ไปจัดการซะ"): (1) ตาราง placement->NPC identity/name/title ของ bg0001 ให้ตรงเซิร์ฟเวอร์เดิม อย่างน้อย Hields/Guild Administrator แทน Unemployed Sailor · Sase/Guild Assistant แทนสัตว์ดอกไม้แดง · Columbus/Marine Transport Station แทนที่ Navy Transfer
                 (2) ป้ายสองบรรทัด: ชื่อสีเหลือง + title สีฟ้าเหนือชื่อ (RE-067/RE-068)
                 (3) กติกา hide/unhide ตามสถานะเควส + ชุด NPC มาตรฐานประจำเมือง (ตลาด ร้านค้า ตีบวก ดันเจี้ยน guild map)
                 (4) NPC บางตัวเดินวนในระยะของมัน
              -> เจ้าของจะกลับมาเทสใหม่ "ก็ต่อเมื่อ npc เป็นตัวที่ถูกต้องแล้ว"
```

## ⑮ nonclaims (ของใบ ①–⑯ คงไว้ครบ) + เพิ่ม
- ไม่ได้อ้างว่าไคลเอนต์รับ 115 · `seen` ไม่ใช่เพดาน · ไม่พิสูจน์กลไกฝั่งไคลเอนต์ · ไม่ตอบเรื่อง scene≠1 / มอนสเตอร์ / ของข้ามวัน / spawn ทับ · รอบเดียวเครื่องเดียว · สีอ่านด้วยตา · ตาราง 115 เป็นของเรา · OBSERVER/G-FRAME เป็นขั้นตอน · ซูมล้อเมาส์ไม่ได้วัด · ราคาคลิก NPC วัดได้เคสเดียว (ไม่ส่งซ้ำ) · ไม่รับรองการต่อสายโดยทั่วไป
- ไม่ได้วัดว่า NPC ตัวไหนคือ template/identity ใดในตาราง — คำว่า "ผิดตัวทุกตัว" เป็นคำให้การเจ้าของเทียบกับความจำ+capture เซิร์ฟเวอร์เดิม (ยังไม่ได้แนบ)
- `T0` ±5 วิ จากสกรีนช็อต ไม่ใช่จากวิดีโอ · ระยะทุกเฟรม unmeasured · เฟรมวิดีโอ "หาย" เป็นตัวเลขตามสูตร ไม่ได้ตรวจว่าช่วงไหน
- ผมเป็นคนเดินช่วง 13:15–13:25 (เจ้าของนั่งดู) และเจ้าของเดินเอง 13:25–13:36 — ใบไม่ได้ห้าม แต่จดไว้ให้ชัด
