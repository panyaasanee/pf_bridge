# KA1A R321 RESULTS — รอบ "กลุ่ม 3" flagless · **ต้นเหตุมอนเขียว/ตีไม่ได้ = login เข้าฉาก 126 ไม่ส่ง basic_faction** · RE-272 · GM /lv · GT-217 · GT-269 · GT-214/250/252 (ซ้ำ) · GT-220/223/242 BLOCKED
ADDRESSEE: chief
cc: LANE-A (§1 faction · GT-214/250/252) · LANE-GM (§1 ตั๋ว relog 126 · /lv · GT-269 · GameMaster.dll) · LANE-DB (RE-272/GT-272) · LANE-B (§1 = คำตอบ P-2) · COO (§7 คิวล้าสมัย · คำสั่งเจ้าของ 2 ข้อ) · LANE-UI (GT-251/253 สถานะ)
เขียนโดย: ka1-A (attended · Panya อยู่หน้าคีย์บอร์ดตลอด 11:03–12:49 +07:00) · เวลาเขียน 2026-09-06 13:0x +07:00

## บูต (ชั้นเครื่อง)
- job `1539_r321_group3_boot.ps1` → `R321_BOOT=PASS` 11:02:59 · teardown `1541` 12:50:26 `TEARDOWN DONE` · release `1542` 12:51:04
- BOOT_COMMIT `c16dbb467371d8dffb2d4ec35dda8ddbc8f33c7a` (main `20502a58` code_delta=12 — resolver เลือกเขียวล่าสุด) · **ไร้ธง ไร้ env** (`FLAGLESS=confirmed`) · pytest ในต้นไม้ `test_equip_state_static + test_gm_level_command + test_gm_warp_relog_stage` = 65 passed
- canonical sha ก่อน=หลัง `4FF37060D3A2E876A41A479A348E062557D6C2FA2FF355548FAF81830A548454` · run DB `state/run_gt272_20260906_110222.sqlite3` integrity ok
- capture `GameClient/capture_r321_20260906_110222/` — server 1 โปรเซส · **client 6 เซสชัน** (11:03 · 11:17 · 12:03 · 12:19 · 12:21 · 12:35 — relog ด้วย X + job relaunch `1540` ×2 และ Panya เปิดเอง ×2) · raw journal ต่อเซสชัน + `GAME_LIVE.txt` 705 KB + `GAME_EVENTS_LIVE.txt` 51 KB + **`R321_GROUP3_hex_windows.txt` 744 KB (104 หน้าต่าง)** · sha256 ทุกไฟล์ใน `outbox/1541_r321_teardown.out.txt`
- teardown: stopped 1 · traceback 0 · listeners 0 · GameClient 0 · ErrorData 0 ตลอดรอบ
- ⚠️ ปลั๊กอิน `GameMaster.dll` (sha `4a0ecb58…`, จาก `patches/gm_plugin/`) ถูกคัดลอกกลับข้าง client 11:33 และ**คงไว้** — ดู §6 คำสั่งเจ้าของ

## §1 ต้นเหตุ "มอนชื่อเขียว ตีไม่ได้ + หลอดฟ้าเหนือหัว" — วัดจาก 6 เซสชัน (คำตอบของ P-2 ที่ B/GM ตามหา)
**อาการ (client-observable · Panya):** ฉาก 2 มอน Fighting Fish ทั้ง 12 ตัวชื่อ**เขียว** คลิกโจมตีไม่ได้ · ตัวละครมีหลอดสีฟ้าเหนือหัว · อาการ**ติดตามตัวไปทุกฉากที่ warp ต่อ** · แต่บางเซสชันชื่อ**ชมพู**ตีได้ปกติ (เหมือน 5 ก.ย. R316)
**ตารางทดลอง (ตัวแปรเดียวต่อครั้ง):**
| เซสชัน | เข้าเกมยังไง | LV | สีมอนฉาก 2 |
|---|---|---|---|
| 11:17 → `/warp 1` → `/warp 2` (11:51) | login เข้า **126** ผ่านตั๋ว relog | 5 | **เขียว** |
| 12:19 | login เข้าฉาก 2 (บันทึกไว้) | 1 | ชมพู |
| 12:21 | login เข้าฉาก 2 | 5 | ชมพู |
| 12:21 ต่อ: `/warp 1`→`/warp 2` · `/warp 126`→`/warp 2` | (ไม่ relog) | 5 | ชมพู |
| 12:35 → `/warp 2` | login เข้า **126** ผ่านตั๋ว relog | 5 | **เขียว** + หลอดฟ้า |
⇒ ไม่ใช่เลเวล · ไม่ใช่ warp path · **ตัวแปรเดียว = login ลงในฉาก 126**
**wire (เทียบไบต์เฟรม `FOUNDATION_SELECTED_START_GAME` ที่ server ส่งตอน login · เซสชัน 12:21 vs 12:35):**
- login บก (ฉาก 2): 423 B · offset 48 `12 4F 07` = BasicAttr mask **`0x074F`** · มีฟิลด์ `14 01 00 00 00` (u32=1) หลัง scene block = **`basic_faction=1`** (ชื่อตาม `gm/attr_wire.py` แถว x=11 "1 = player side")
- login ทะเล (ฉาก 126): 418 B · `12 4F 03` = mask **`0x034F`** · **ไม่มีฟิลด์ faction** (ต่างกันแค่ 5 ไบต์นี้ + scene id `02`→`7E` + พิกัด spawn) · เฟรมอื่นตอน login เหมือนกันทุกไบต์ · census ฉาก 2 (`WORLD_CENSUS_BG0002_INITIAL_97` 18,151 B) **เหมือนกันทุกไบต์** ทั้ง R316 (5 ก.ย. ชมพู) / R320 / R321 ทุกเซสชัน — NPCAttr ของมอนไม่ได้เปลี่ยน
- ที่มาในโค้ด (ต้นไม้ที่บูต): `world_faction_admission.py` (LANE-A) ส่ง faction ของผู้เล่นเฉพาะฉากที่ registry เปิด + `n_SAVE=1` (1, 2, 14 …) · ฉาก 126 ไม่เข้าเกณฑ์ → `ActorAttr` เปล่า (ไฟล์เขียนไว้เองว่า "every other scene ships the plain ActorAttr") · faction ถูกส่ง**ครั้งเดียวตอน login** — `TeleportVital`/census ตอน warp ไม่ส่งซ้ำ → client ถือ faction 0 ตลอดเซสชัน
**ข้อสรุป:** ผู้เล่นที่ login ลงทะเล (ตั๋ว relog ของ `/warp 126` · GT-217/GT-266 path) กลายเป็น "ไร้ฝ่าย" ถาวรจนกว่าจะ login ใหม่บนบก → มอนทุกฉาก neutral (เขียว) ตีไม่ได้ · ด้านกลับ: `/warp 126` จากบก (มี faction) ทำให้ HP บนทะเลโชว์ `-1/1` (R320+R321 เห็นทั้งสองครั้ง)
**เจ้าของ/ทางแก้ที่เห็น (ไม่สั่ง แค่ชี้):** LANE-A — ส่ง `basic_faction` ทุก login scene หรือส่งซ้ำหลัง teleport ข้ามชนิดฉาก · LANE-GM — ตั๋ว relog 126 ต้องรู้ผลข้างเคียงนี้ · LANE-B — P-2 "สีชื่อมอน" ในบูตปกติ**ไม่มีบั๊กฝั่ง NPCAttr** (ชมพูทุกครั้งที่ login บนบก) แนะนำปิดสมมติฐานฝั่ง composer มอน
**nonclaims:** ไม่ได้ทดสอบ login ลงฉาก 14 (เปิดแล้ว n_SAVE=1) ว่าชมพูไหม · ไม่ได้ยืนยันว่า client ใช้ faction เทียบกับ NPCAttr byte ไหน (แค่ผลบนจอ + ไบต์ที่ต่าง) · หลอดฟ้าเหนือหัวไม่ได้ถอดว่าเป็นอะไร

## §2 RE-272 / GT-272 — สวมอาวุธจากกระเป๋า (คำสั่งเจ้าของ 0156)
- **client-observable:** เปิดหน้าตัวละคร ช่องอุปกรณ์ว่าง · กระเป๋า 3/40 (ดาบ×2 ช่อง 0 · ถัง ช่อง 1 · Create Character Blade ช่อง 3) · ทำ 3 แบบ: (11:05) คลิก+ลาก · (11:09) ดับเบิลคลิก/คลิกขวาหลายครั้ง · (11:11) ลากไปช่องอาวุธอย่างเดียว → **ช่องอุปกรณ์ไม่เปลี่ยนทั้ง 3 ครั้ง** · หลัง relog (11:17) ยังไม่มีอาวุธ
- **wire:** `ItemOperateVitalReq` (0x4BED) 16 B payload `0B 05 14 08000000 32 0400000000000000` = **op=5 · value=8 · identity=0x4 (Blade)** ×3 (11:05:30 · 11:09:07 · 11:11:48) **ไบต์เหมือนกันทุกครั้งไม่ว่าดับเบิลคลิกหรือลาก** · client ส่งครั้งเดียวต่อการกระทำแล้วรอ (กดซ้ำหลายทีได้เฟรมเดียว) · server: `MILESTONE V123_EQUIP_FROM_BAG_REQUEST_CAPTURED_NO_REPLY` ×3 ไม่ตอบ (ตามบิลด์)
- **สถานะที่เสนอ:** RE-272 = **CAPTURED (ครบ 3 ซ้ำ)** ส่งให้ LANE-DB เขียนแขน (ข) · GT-272 = รอ server ตอบ op=5 ก่อนถึงจะวัด persist ได้ (relog วันนี้ = NEGATIVE ตามคาด)

## §3 GM `/lv <n>` (คำสั่งเจ้าของ 0155 · ใบ GT ยังไม่มีเลข)
- `/lv 5` 11:13:09 → แชท `[ทั่วไป] : LV SET RELOG` · err `GM_LV … level -> 5 (row written; next login sends it)` · จอยัง LV 1 (ตั้งใจ) → relog 11:17 → **จอ LV 5** · `LOGIN_VITALS from_row level=5` · `/lv 1` 12:18 → relog → LV 1 · `/lv 5` 12:20 → relog → LV 5 · ทำซ้ำ 3 ครั้งตรงทุกครั้ง
- **สถานะที่เสนอ:** PASS สองชั้น (chief ตั้งเลขใบแล้วปิดจากผลนี้ได้เลย ไม่ต้องบูตอีก)

## §4 GT-217 — ตั๋ว relog เข้า 126
- `/warp 126` (11:14) → err `GM_WARP_SCENE_PERSIST_FAILED scene=126 reason=login_would_refuse` + `GM_WARP_RELOG_ENTRY_STAGED scene=126 single_use=1` → X ออก → login 11:17 → **เกิดกลางทะเล Rising Sun Sea X:3,050 Y:232** · server ส่ง `WORLD_CENSUS_LANE_SCENE126_INITIAL_37` ตอน login · ทำซ้ำได้ (12:35 ก็เข้า 126) · login ครั้งถัดไปหลังไปบก = ฉากบกที่ persist (2)
- **สถานะที่เสนอ:** PASS สองชั้น · **แต่มีผลข้างเคียง §1 (ไร้ faction)** — ใบ GT-217/266 ควรบันทึกไว้ในเกณฑ์

## §5 GT-269 — GMUI 3 แท็บ
- ครั้งแรก (11:2x ทะเล/บก) ปุ่ม GM **เงียบ ไม่มีเฟรม** — เพราะ `GameMaster.dll` ไม่อยู่ข้าง client (rollback ของ GT-207/219 ถอนไว้) · ใบ GT-269 **ขาด P0** ข้อนี้ (ผู้เขียนใบอ้างภาพ 2 ก.ย. ที่ถ่ายตอน DLL ติดอยู่) · คัดลอก DLL กลับ 11:33 → relog → **GMUI เปิด** (12:4x)
- **client-observable (Panya ถ่าย 3 ภาพ · ka1-A อ่านป้าย · Panya ยืนยันคำอ่านทีหลัง):** แท็บ 1 "ฟังก์ชั่นพื้นฐาน" **7 แถว**: ตัวละครซ่อนตัว (ซ่อนตัว/ปรากฏตัว) · ฉากที่นี่ [ช่อง] X Y Z · NPC ที่นี่ · ผู้เล่นที่นี่ · ล็อกผู้เล่น · **[ช่องว่างสูงหนึ่งแถว — ไม่มีวิดเจ็ตที่มองเห็น]** · ฆ่าผู้เล่น · ข้อมูลล่าสุด [ช่องกว้าง] · ปุ่ม "ปฏิบัติ" มุมขวาล่าง · แท็บ 2 "ฟังก์ชั่นเชิงระดับ(?)" **5 แถว**: มอนสเตอร์เกิด · ตี…มอน (อ่านไม่ชัด — Panya ยืนยัน) · แบนสนทนาโดยทั่วไป (แบนทั้งหมด/ปลดแบน · ระยะเวลา นาที · ช่องกว้าง) · แบนสนทนาตัวบุคคล (แบน/ปลด · ชื่อผู้เล่น · สาเหตุ · ระยะเวลา นาที (0=ถาวร)) · ใส่คำสั่ง [ช่องกว้าง] · แท็บ 3 "ฟังก์ชั่นกิจกรรม" **5 แถว**: ไอเทมดรอป [0] + พื้นที่ดรอป [0] · BUFF ฉาก [0] · เปลี่ยนฝ่าย [0] · แชทอิสระ (ปิด/เปิด) · กิจกรรมกอบกู้ [0] + ได้จำนวน [0]
- **wire:** ไม่มีเฟรมออกตอนเปิดหน้าต่าง (ตามใบ) · **สถานะที่เสนอ:** PASS ชั้น client (7/5/5 ตรง census · ช่องว่างหน้า 1 = ไม่มีวิดเจ็ต) · LANE-GM แก้ใบเพิ่ม P0 "ต้องมี GameMaster.dll"

## §6 คำสั่งเจ้าของ (Panya · 6 ก.ย. 11:4x · เขียนแทนโดย ka1-A)
1. **`GameMaster.dll` ติดถาวรข้าง client** (`GameClient/GameMaster.dll` sha `4a0ecb58…` 14,848 B) จนกว่าจะพิสูจน์ว่าต้อง replace ด้วยไฟล์ที่ถูกต้องกว่า · **ห้ามใบไหนสั่ง rollback อีก** (เดิม GT-207/219 สั่งถอนเพื่อเทสตัวตรวจ DLL — เหตุผลนั้นจบแล้ว) · chief ลง AGENTS §7 · teardown template ห้ามลบ
2. ใบที่ต้องแพตช์ฝั่ง client (DLL/ไฟล์) ต้องประกาศใน `ATTENDED:` บรรทัดแรกเป็น P0 — เสนอลง COMMON (ka1-A จะเสนอ diff ให้ Panya เคาะ)

## §7 คิว GT ล้าสมัย — วันนี้เสียเวลาเจ้าของซ้ำ 3 ใบ (ถึง chief + COO)
- R364 ข้อ 2 สั่งเติม `ATTENDED:` ให้ "19 ใบ READY" และ NOW/คิวยังขึ้น READY สำหรับใบที่**ทดสอบเสร็จแล้ว**: GT-200/214/217/220 PASS ใน `R307` (3 ก.ย.) · GT-223 FAIL-as-designed `R309` · GT-250/251/252/245 ใน **`R317` (5 ก.ย. 11:25 — ยังไม่ถูก consume 25 ชม.)** · GT-253 = เนื้อเดียวกับ RE-237 ที่ R320 เก็บแล้ว · GT-255/257/266/230 R320
- วันนี้จึงรัน GT-214/250/252 ซ้ำ (ผลเหมือน R307/R317: GT-214 คลิก P91/P86 → `LANE_A_CHOOSE_NPC_SCENE2_FACE` 12,574 B · GT-250 ป้าย 8 ชื่อคงเดิมหลังเดินไกล+กลับ · GT-252 ตัวเลือก 2 → `QuestOperateVital` quest 3205 server เงียบ รูป Columbus ค้าง) — ใช้เป็น regression ยืนยันได้ แต่ไม่ควรเกิด
- **ต้นเหตุ:** ผลเทสอยู่ในจดหมาย แต่สถานะในไฟล์คิว 2 MB ต้องให้ chief แก้มือ และงานนั้นไม่มีเส้นตาย/ตัววัด → **ขอ chief พับผล R307/R309/R317/R320/R321 ลงคิวในรอบ archive** และ **ขอ COO วัด "จดหมายผลค้างพับ > 6 ชม. = escalation"** · ka1-A จะใส่บรรทัด `RESULT: <GT> <สถานะ> <รอบ> <วันที่>` ท้ายจดหมายผลทุกฉบับต่อจากนี้ให้เครื่องอ่านได้

## §8 ใบที่ BLOCKED / ไม่ได้ทำ
- **GT-220 / GT-242 / GT-223 (ต้องฆ่ามอน):** BLOCKED ในบูตนี้ — ฉาก 2 มอนเขียวตีไม่ได้ (§1) · ตอนที่มอนชมพู (12:19–12:35) Panya ใช้เวลาไล่หาต้นเหตุ §1 ซึ่งคุ้มกว่า · ทำได้ทันทีในบูตหน้าถ้า login บนบก
- **GT-262** (แผงขาย/คลังกิลด์) ตัดออก — เวลาเกิน 1 ชม.
- **GT-200** ไม่ต้องทำ (PASS R307 · วันนี้เห็น Columbus LV 10 / Martin LV 35 / Fighting Fish Sergeant LV 35 เป็น regression เสริม)

## §9 ข้อสังเกตเครื่องมือ
- resolver ถอย 12 commit จาก main (CI ยังไม่ตรวจของใหม่) — ปกติ
- job relaunch `1540` ใช้ซ้ำได้หลายครั้ง (copy เป็น 1540b/1540c) · Panya เปิด client เองได้ตอน server ยังรัน (เซสชัน 12:21/12:35)
- ตัวถอด `GAME_EVENTS_LIVE` ยังไม่ถอด `ItemOperateVitalReq` เป็นชื่อฟิลด์ครบ (แค่ operation/value/identity) พอใช้

## RESULT lines (เครื่องอ่านได้)
RESULT: RE-272 CAPTURED R321 2026-09-06 11:05-11:11
RESULT: GT-272 NEGATIVE-EXPECTED R321 2026-09-06 (server no reply yet)
RESULT: GT-LV(no number) PASS R321 2026-09-06 11:13-12:21
RESULT: GT-217 PASS R321 2026-09-06 11:17 (side effect: no faction, see §1)
RESULT: GT-269 PASS-CLIENT R321 2026-09-06 12:4x (P0 GameMaster.dll added)
RESULT: GT-214 PASS-AGAIN R321 2026-09-06 11:52 (first PASS R307)
RESULT: GT-250 NEGATIVE-AGAIN R321 2026-09-06 11:29 (first R317)
RESULT: GT-252 CAPTURED-AGAIN R321 2026-09-06 11:47 (first R317)
RESULT: GT-220 BLOCKED R321 2026-09-06 (no attackable mob, §1)
RESULT: GT-242 BLOCKED R321 2026-09-06 (same)
RESULT: GT-223 BLOCKED R321 2026-09-06 (same)
RESULT: GT-262 NOT-RUN R321 2026-09-06 (time)

## SCOREBOARD: DONE | ผู้เล่นพิมพ์ /lv 5 แล้ว login ใหม่เป็น LV 5 จริงบนจอ (และ /lv 1 กลับได้) | capture_r321_20260906_110222 · จดหมายนี้ §3

## ภาคผนวก A — เฟรม client→server ที่ไม่ใช่การเดิน/หัวใจ (เวลา +07:00 · payload hex หลัง decompress · จาก GAME_EVENTS_LIVE.txt)
```
---- 2026-09-06T11:03:45.787 SESSION_START peer=127.0.0.1:62223 raw=GAME_20260906_110345_785651
11:04:14.952 f5     TeleportVital              163B  hex=0B020B000B000B000F000012010F0B000B010BFF32000000000000000026FFFFFFFF0B190B000B000501320000000000…
11:05:00.536 f29    CheckSecondPwdVital         44B  hex=0800190000000044200000003544393042463734383644414432384536303436413138334338464444383339
11:05:30.615 f47    ItemOperateVitalReq         16B operation=5 value32_mapped=8 item_identity=0x0000000000000004 hex=0B051408000000320400000000000000
11:09:07.739 f155   ItemOperateVitalReq         16B operation=5 value32_mapped=8 item_identity=0x0000000000000004 hex=0B051408000000320400000000000000
11:11:48.741 f235   ItemOperateVitalReq         16B operation=5 value32_mapped=8 item_identity=0x0000000000000004 hex=0B051408000000320400000000000000
11:13:09.134 f275   UNKNOWN_0xAC52              20B chat='lv 5' hex=4800000000480A0000002F006C00760020003500
11:14:23.159 f313   UNKNOWN_0xAC52              28B chat='warp 126' hex=480000000048120000002F0077006100720070002000310032003600
11:14:28.189 f314   TeleportVital               40B  hex=0B020B000B000B000F000012902A0B002A00A03E452A000068432A0000AC422A000000000B000B00
---- 2026-09-06T11:17:16.774 SESSION_START peer=127.0.0.1:56422 raw=GAME_20260906_111716_772069
11:17:39.364 f11    TeleportVital               47B  hex=0B020B000B000B000F000012938B0B000B0012902A0B002A00A03E452A000068432A0000AC422A1C9540400B000B00
11:18:21.246 f34    CheckSecondPwdVital         44B  hex=0800190000000044200000003544393042463734383644414432384536303436413138334338464444383339
11:23:49.309 f198   UNKNOWN_0xAC52              24B chat='warp 1' hex=4800000000480E0000002F00770061007200700020003100
11:23:59.779 f199   TeleportVital               68B  hex=0B020B000B000B000F000012B41E0B002AB72BBFC32AD45F10C62AB9E030C52A00003A430F7E0012902A0B002AD45F10…
11:47:06.877 f891   TargetVital                 25B placement=P1 data_name='Sebastian' kind=2 hex=320220000000000000080212B60F0B00320220000000000000
11:47:10.903 f894   QuestOperateVital           23B quest_id=3205 hex=12850C0801080014000000003200000000000000000500
11:51:38.198 f1027  TargetVital                 11B target=clear kind=2 hex=3200000000000000000802
11:51:40.315 f1028  GetWorldInfoVital            2B  hex=0B00
11:51:44.220 f1030  UNKNOWN_0xAC52              24B chat='warp 2' hex=4800000000480E0000002F00770061007200700020003200
11:51:50.403 f1031  TeleportVital               40B  hex=0B020B000B000B000F000012902A0B002A0032D2462A0082A5462A0060D5442A000000000B000B00
11:52:28.550 f1052  TargetVital                 25B placement=P91 data_name='Local people' kind=2 hex=325C20000000000000080212B60F0B00325C20000000000000
11:52:30.285 f1053  ChooseNPC                  122B placement=P91 data_name='Local people' hex=325C2000000000000012B41E0B002AA2FF0BC32AC4F17B462A04FD77462A00E01C450F7E0012B41E0B002ADAE258C32A…
11:53:28.788 f1082  TargetVital                 67B placement=P86 data_name='Mori Hiroko' kind=2 hex=325720000000000000080212B60F0B0032572000000000000012B60F0B0032572000000000000012B60F0B0032572000…
---- 2026-09-06T12:03:40.306 SESSION_START peer=127.0.0.1:58649 raw=GAME_20260906_120340_303550
12:03:51.426 f4     TeleportVital               40B  hex=0B020B000B000B000F000012902A0B002A0032D2462A0082A5462A0060D5442AC8FF31400B000B00
12:18:13.408 f435   UNKNOWN_0xAC52              20B chat='lv 1' hex=4800000000480A0000002F006C00760020003100
---- 2026-09-06T12:19:24.931 SESSION_START peer=127.0.0.1:54015 raw=GAME_20260906_121924_929165
12:19:35.458 f4     TeleportVital               47B  hex=0B020B000B000B000F000012938B0B000B0012902A0B002A0032D2462A0082A5462A0060D5442AC8FF31400B000B00
12:20:59.769 f48    UNKNOWN_0xAC52              20B chat='lv 5' hex=4800000000480A0000002F006C00760020003500
---- 2026-09-06T12:21:58.466 SESSION_START peer=127.0.0.1:63629 raw=GAME_20260906_122158_464535
12:22:11.541 f5     TeleportVital               47B  hex=0B020B000B000B000F000012938B0B000B0012902A0B002A9766A4462AE43411462A000015442A423D21400B000B00
12:23:43.415 f52    TargetVital                 11B placement=P60 data_name='Ancient Civilization Alert Weapon' kind=1 hex=323D200000000000000801
12:28:46.677 f202   UNKNOWN_0xAC52              24B chat='warp 1' hex=4800000000480E0000002F00770061007200700020003100
12:28:57.410 f203   TargetVital                 56B target=clear kind=1 hex=320000000000000000080112A2250B040B020B000B000B000F000012902A0B002AD45F10C62AB9E030C52A00003A432A…
12:29:03.912 f208   UNKNOWN_0xAC52              24B chat='warp 2' hex=4800000000480E0000002F00770061007200700020003200
12:29:07.971 f209   TeleportVital               40B  hex=0B020B000B000B000F000012902A0B002A0032D2462A0082A5462A0060D5442A000000000B000B00
12:30:05.281 f240   UNKNOWN_0xAC52              28B chat='warp 126' hex=480000000048120000002F0077006100720070002000310032003600
12:30:09.658 f241   TeleportVital               40B  hex=0B020B000B000B000F000012902A0B002A00A03E452A000068432A0000AC422A000000000B000B00
12:30:17.275 f247   UNKNOWN_0xAC52              24B chat='warp 2' hex=4800000000480E0000002F00770061007200700020003200
12:30:21.818 f248   TeleportVital               40B  hex=0B020B000B000B000F000012902A0B002A0032D2462A0082A5462A0060D5442A000000000B000B00
12:33:22.287 f340   UNKNOWN_0xAC52              28B chat='warp 126' hex=480000000048120000002F0077006100720070002000310032003600
12:33:26.684 f341   TeleportVital               40B  hex=0B020B000B000B000F000012902A0B002A00A03E452A000068432A0000AC422A000000000B000B00
12:34:12.456 f365   UNKNOWN_0xAC52              24B chat='warp 1' hex=4800000000480E0000002F00770061007200700020003100
12:34:23.627 f366   TeleportVital               68B  hex=0B020B000B000B000F000012B41E0B002AB72BBFC32AD45F10C62AB9E030C52A00003A430F020012902A0B002AD45F10…
12:34:30.567 f370   UNKNOWN_0xAC52              28B chat='warp 126' hex=480000000048120000002F0077006100720070002000310032003600
12:34:34.763 f371   TeleportVital               40B  hex=0B020B000B000B000F000012902A0B002A00A03E452A000068432A0000AC422A000000000B000B00
---- 2026-09-06T12:35:38.959 SESSION_START peer=127.0.0.1:56640 raw=GAME_20260906_123538_957409
12:35:47.902 f4     TeleportVital               47B  hex=0B020B000B000B000F000012938B0B000B0012902A0B002A00A03E452A000068432A0000AC422AAA2E2E400B000B00
12:36:05.317 f15    UNKNOWN_0xAC52              24B chat='warp 2' hex=4800000000480E0000002F00770061007200700020003200
12:36:11.338 f16    TeleportVital               40B  hex=0B020B000B000B000F000012902A0B002A0032D2462A0082A5462A0060D5442A000000000B000B00
```
(ตัดออก: TargetPosVital การเดิน 0 เฟรม · ActionVital action_30=EA60/EA61 ระหว่างเดิน/หมุน 57 เฟรม — อยู่ครบใน GAME_LIVE.txt / hex windows)

## ภาคผนวก B — `FOUNDATION_SELECTED_START_GAME` (PC หลัง decompress) login บก vs login ทะเล 126 · ไบต์ 40–180 (ส่วนที่ต่าง) · เต็มเฟรมอยู่ใน raw journal ของเซสชัน 12:21 และ 12:35
```
LAND scene2 LV5 (12:21:5x) len=423
    40: 01 00 01 10 00 00 00 00 12 4F 07 48 0E 00 00 00 41 00 72 00
    60: 65 00 6E 00 61 00 30 00 31 00 12 05 00 14 64 00 00 00 14 64
    80: 00 00 00 2A 00 00 C8 43 12 02 00 32 00 00 00 00 00 00 00 00
   100: 14 01 00 00 00 32 01 08 00 00 00 00 00 00 05 01 19 01 00 00
   120: 00 32 10 27 00 00 00 00 00 00 12 A0 16 0B FF 32 01 00 01 10
   140: 00 00 00 00 26 FF FF FF FF 14 00 00 00 00 14 09 40 11 00 14
   160: F0 EF 10 00 14 1A F0 10 00 14 00 00 00 00 14 7A 18 23 00 14
SEA scene126 LV5 (12:35:4x) len=418
    40: 01 00 01 10 00 00 00 00 12 4F 03 48 0E 00 00 00 41 00 72 00
    60: 65 00 6E 00 61 00 30 00 31 00 12 05 00 14 64 00 00 00 14 64
    80: 00 00 00 2A 00 00 C8 43 12 7E 00 32 00 00 00 00 00 00 00 00
   100: 32 01 08 00 00 00 00 00 00 05 01 19 01 00 00 00 32 10 27 00
   120: 00 00 00 00 00 12 A0 16 0B FF 32 01 00 01 10 00 00 00 00 26
   140: FF FF FF FF 14 00 00 00 00 14 09 40 11 00 14 F0 EF 10 00 14
   160: 1A F0 10 00 14 00 00 00 00 14 7A 18 23 00 14 7B 18 23 00 14
```
- ต่างกัน: offset 50 `07`→`03` (BasicAttr mask 0x074F → 0x034F) · offset 89 scene `02`→`7E` · บก มี `14 01 00 00 00` ที่ offset 100 (u32 basic_faction=1 · ทะเลไม่มี) · offset ~100–125 พิกัด spawn ต่างฉาก · ที่เหลือเหมือนกัน
- census ฉาก 2 `WORLD_CENSUS_BG0002_INITIAL_97` 18,151 B: R316 (5 ก.ย. 10:34) == R320 (6 ก.ย. 00:25) == R321 ทุกเซสชัน — diff = 0 ไบต์

-- จบจดหมาย · ka1-A
