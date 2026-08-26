[ถึง: COO · chief · สาย A · สาย B · RE runner (local) | จาก: attended (กะ1) แทนเจ้าของ · 2026-08-26T16:30+07:00]

# PANYA-ORDER — เปิดเลนพิเศษ "Lane GM" + ผลสำรวจต้นทางที่ attended ทำให้แล้ว (static บนสะพาน 16:05-16:25)

## ① คำสั่งเจ้าของ (verbatim 16:1x+07:00)
> "เปิดเลนพิเศษขึ้นมา ชื่อ Lane GM ฉันต้องการให้ค้นหาอะไรก็ตามที่เกี่ยวกับ GM / developer functions จาก client เช่น แมพ GM คำสั่ง GM วิธีทำให้ตัวเป็น GM ความสามารถของ GM ไอเท็ม GM และอะไรก็ตามที่เกี่ยวข้อง เพื่อที่จะนำข้อมูลหรือฟังก์ชัน GM เหล่านี้มาใช้ให้เกิดประโยชน์ในการทดสอบเกมต่อไป"

เจตนา: เครื่องมือ GM = ตัวคูณของทรัพยากรที่แพงที่สุดในโปรเจกต์ (เวลาเจ้าของนั่งเทส) — วาร์ปไปฉากที่ต้องเทสได้เลย, เปิด/ปิด NPC, ให้ไอเท็ม/เลเวล, spawn มอนสเตอร์ โดยไม่ต้องเดินเกมจริงทุกครั้ง

## ② ผลสำรวจ (ค้น external/ + gamedata/ + strings ของ GameClient.bin ตามกฎ "ค้นก่อนถอด")
**ค้นใน pf_bridge\external\ แล้ว: เจอ** · **ค้น gamedata แล้ว: เจอ** — GM ไม่ใช่ของซ่อน client มี transport ครบอยู่แล้ว:

| vital id | ชื่อ (VITAL_REGISTRY 20260817) | ทิศ (จาก handler VA) | ที่รู้แล้วใน external/ |
|---|---|---|---|
| 0x51E9 | `GM_RunGMCommandVital` | client→server (handler = 0x00A106C0 ตัว default ไม่มี handler ฝั่ง client) | serializer 0x00729E10 · **ยังไม่มีแถวใน PF_SERIALIZER_FIELDS** ⇒ ต้องถอด |
| 0x8C77 | `GM_RunGMCommandResultVital` | server→client (handler 0x00729F00 = GMModule_Client) | serializer 0x00729790 · ยังไม่มีแถว field |
| 0x5A19 | `GM_UpdateGMStateVital` | server→client (handler 0x00729F00) | **layout รู้แล้ว**: 0x0B@+0x14 (1B) · 0x0B@+0x15 (1B) · 0x14@+0x18 (4B) — span 0x00729720-0x00729785 sha 03b18673… |
| 0x8D30 | `GM_ForbidToTalkResultVital` | server→client | มีแถว field ใน SERIALIZER_FIELDS |
| 0x9F2C | `Channel_GMGlobalMessageVital` | server→client (ประกาศ GM ทั้งเซิร์ฟเวอร์) | RUNTIME_CLASSMAP |
| 0x162E | `CheatVital` | ทั้งสองทิศ | **layout รู้แล้ว**: string8 len32LE ตัวเดียว @+0x14 |
| 0x6CEC | `Activity_CheatCodeVital` | ทั้งสองทิศ | layout รู้แล้ว: u32 + wstring16 ×5 (โค้ดกิจกรรม ไม่ใช่ GM) |
| 0x2DEF | `CWebGMVital_GSGC` | — (`CWebGMModule` = GM tool ผ่านเว็บ) | RUNTIME_CLASSMAP |
| — | `TeleportVital` / `ForcePos` / `CWarpResult` / `TeleportCheckVital` | registry มี serializer/handler VA ครบ | field layout ยังไม่มี ⇒ ต้องถอด (ใช้ร่วมกับเส้นทางเดินทางจริงของใบ 1600 ด้วย) |

สตริงใน client ที่ยืนยันบริบท: `GMModule_Client` · `GMCommandArg` (RTTI) · `.\Data\CP\bmmsg\bm_gm.tga` (ไอคอน GM ในบอลลูนแชท) · `RewardGMToolEventHandler` · **ไม่พบสตริงคำสั่ง GM แบบ `/xxx` เลย** ⇒ ข้อสรุปเบื้องต้น (ยังไม่พิสูจน์): client ส่งข้อความคำสั่งดิบไปให้เซิร์ฟเวอร์ตีความ — คลังคำสั่ง GM อยู่ฝั่งเซิร์ฟเวอร์เดิมที่หายไป **เราต้องนิยามคำสั่งเองในเซิร์ฟเวอร์ของเรา** client เป็นแค่ท่อ + สถานะ + จอแสดงผล

ข้อมูลเกม (gamedata/ ที่ commit แล้ว — cloud อ่านได้ตรง ๆ):
- `TEXTDATA_TH__SCENE_NAME_TIP.tsv` มีคอลัมน์ **`s_GM_SCENE_NAME`** 331 ฉาก = "แมพ GM" ที่เจ้าของถาม (ชื่อฉากแบบที่ GM เห็น + เลข scene id ในวงเล็บ เช่น "เรือในทะเล 1(17)" · Port Royal=1 · Prison Exile Island=2 · Spice Paradise Island=3 · Slave Market Island=4 · Ship in the Sea=17-23 · Ship in the Sky=24-30) — **ตารางนี้ตอบเรื่อง scene id ของทะเล/เกาะให้ใบ 1600 ได้ทันทีด้วย**
- `CONSTDATA_TH__MOBS.n_GM_SWITCH` = 1 อยู่ 7 แถว (855 傑克 · 871 探員考森 · 882 麥哲倫 · 897 傳說中的商人 · 902 王威利 · 8180/8181 水燈) = NPC กิจกรรมที่ GM เปิด/ปิด
- `QUESTDATA_TH__QUEST.n_GM_SWITCH` = 1 อยู่ 39 เควส = เควสกิจกรรมที่ GM เปิด/ปิด
- `TEXTDATA_TH__GMTOOL.tsv` 97 แถว = ประเภท log ของ GM tool (ดรอปมอนสเตอร์, ซื้อขาย, ตีบวก…) — ไว้ทำ item-flow log ทีหลัง ไม่ใช่รอบแรก
- Lua API ฝั่ง client มี `Player.AddItem/AddExp/AddCash` IMPLEMENTED แต่ `Player.Teleport/Warp/TeleportWithVehicle` เป็น STUB_NOOP บน client — การวาร์ปเป็นเรื่องของเซิร์ฟเวอร์ผ่าน wire ล้วน

## ③ นิยามเลนที่เสนอ (ขอ COO ออก CHARTER-03)
- ชื่อ/ล็อก: **[LANE-GM]** · routine `PF Lane GM · TOOLS (cloud)` cron `11 * * * *` (ช่อง :11 ว่าง ไม่ชนใคร) — prompt v1 อยู่ `staged\PROMPT_PF_Lane_GM_v1.txt` รอเจ้าของวาง
- เขตเขียน: `src/pirateforce_foundation/gm/` · `scenarios/gm_*.json` · `tests/test_gm_*.py` · `rounds/GM_*.md` · จดหมาย — wiring เข้า runtime.py/app.py ผ่าน CORE-REQUEST ถึง chief เหมือนสาย A/B
- 🔴 กฎความปลอดภัย: สถานะ GM ให้ได้เฉพาะบัญชีที่ตั้งไว้ฝั่งเซิร์ฟเวอร์ (config/DB `gm_accounts`) · ค่าเริ่มต้น = ไม่มีใครเป็น GM · client ขอเป็น GM เองไม่ได้ · `production_allowed=true` ได้เพราะไม่ต้องใช้ flag แต่ผู้เล่นทั่วไปต้องไม่เห็นอะไรต่าง
- 🔴 กฎความซื่อสัตย์: **GM เป็นเครื่องมือไปถึงสภาพที่จะเทส ไม่ใช่หลักฐานว่าฟีเจอร์ทำงาน** — วาร์ปด้วย GM ไปเกาะแล้วเห็นเกาะ ≠ M2 ผ่าน · ทุกใบเทสที่ใช้ GM ต้องมีบรรทัด nonclaim ระบุว่าใช้ GM ข้ามขั้นไหน
- ลำดับงาน: **GM-001** ส่ง `GM_UpdateGMStateVital` ตอน login ให้บัญชี gm_accounts (layout รู้แล้ว — สร้างได้วันนี้) → attended probe 5 นาที: จอเปลี่ยนอะไร (ไอคอน bm_gm · UI · prefix แชท) · **GM-002** จับ capture ว่า client ส่ง 0x51E9 เมื่อไร/รูปแบบไหนตอนอยู่ในสถานะ GM (attended พิมพ์ในแชท) → ได้ layout จากของจริง · **GM-003** คำสั่ง v1 ฝั่งเซิร์ฟเวอร์: `warp <scene_id> [x y]` · `npc on|off <mob_id>` (n_GM_SWITCH) · `item <id> <n>` · `lv <n>` · `spawn <mob_id>` · `say <ข้อความ>` (0x9F2C) · **GM-004** ตาราง scene id/ชื่อ GM 331 ฉากเป็น `gm/scene_catalog.py` (pin sha ตารางตามธรรมเนียม)

## ④ ใบ RE ที่ขอให้ chief ออกเลข RE-0xx ให้ RE runner บนสะพาน (static ต้องเปิด image — cloud ทำไม่ได้)
1. layout ของ `GM_RunGMCommandVital` serializer 0x00729E10 (W) + `GM_RunGMCommandResultVital` 0x00729790 (R) — เทียบวิธีเดียวกับที่ Codex ทำกับ CheatVital
2. `GM_UpdateGMStateVital` handler 0x00729F00: ไบต์ไหนคือ is_gm · ค่า u32 คืออะไร (gm level?) · เมื่อ on แล้ว client เปลี่ยนอะไร (xref `bm_gm.tga`, GMModule_Client)
3. `TeleportVital` 0x005EB470 / `ForcePos` 0x005E4250 / `CWarpResult` — field layout (ใช้ทั้ง GM warp และเส้นทางเดินทางจริง)
4. แชทเข้า → ไปที่ 0x51E9 เมื่อใด (prefix? สถานะ GM?) — xref id global 0x01088F8C

## ⑤ ขอ chief
- v6.2 (เมื่อเจ้าของออก): เพิ่มแถว `สาย GM TOOLS [LANE-GM] :11` ในตาราง §0 และนับ CORE-REQUEST ของสาย GM ใน §17 ต่อจาก A/B — **ยังไม่ต้องแก้ prompt ตอนนี้** เจ้าของสั่งรอดู v6.1 ก่อน · ระหว่างนี้ PR [LANE-GM] ไม่ใช่ล็อกของใคร ห้ามแตะ เหมือน A/B

## ⑥ สิ่งที่ attended จะทำต่อ
- รอเจ้าของตัดสินว่าจะสร้าง routine เดี๋ยวนี้หรือรอ v6.1 นิ่งก่อน · ถ้าสร้างแล้ว รอบแรก :11 จะเห็นใบนี้ + prompt
- GM-001 probe attended: รอ chief/COO บอกว่า build ที่มี GM state ขึ้น main แล้ว ค่อยเปิดเกม (ไม่เปิดก่อน)
