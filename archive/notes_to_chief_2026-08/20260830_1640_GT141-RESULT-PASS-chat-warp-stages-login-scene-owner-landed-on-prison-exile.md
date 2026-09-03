# GT-141 RESULT — 🟢 **PASS ทั้งสองชั้น** · `/warp 2` ในกล่องแชทธรรมดา จองฉากล็อกอินได้จริง เจ้าของล็อกอินใหม่แล้วโผล่ที่เกาะคุก · ตัวหักล้างทั้งสองปฏิเสธถูกต้อง

ถึง: **สาย GM (เจ้าของใบ · ADDRESSEE: LANE-GM)** · chief · cc COO, สาย A/B, RE
จาก: attended session "กะ1-A" (Panya ขับ UI เอง) · **OBSERVER_CONFIRMED: 2026-08-30T16:3x+07:00**

## บูต
BOOT_COMMIT **7d6f7fc** = main HEAD (เขียวของตัวเอง) ไร้แฟล็ก · grep 6/6 · **pytest 107 passed + 14 subtests** · code-delta 0 · **canonical UNCHANGED** · ไม่มีวิดีโอ (ใบไม่บังคับ หลักฐาน = คอนโซล + ภาพ) · jobs 1368/1365/1370/1366

**config สองไฟล์เป็นของทิ้งทั้งคู่ ของจริงไม่ถูกแตะเลย** — `PF_GM_ACCOUNTS_CONFIG` = `{"gm_accounts":["localtest"]}` · `PF_GM_LOGIN_SCENE_CONFIG` เริ่มที่ `{"gm_login_scene": {}}` แล้วปล่อยให้ `/warp` เขียนเอง (ใช้ได้เพราะ `resolve_gm_login_scene_config_path` บังคับให้ writer/reader ใช้ไฟล์เดียวกัน) ⇒ ขั้นเก็บกวาดของใบเหลือแค่ลบไฟล์ทิ้ง ไม่ต้องแก้ `config/` จริง

## 🔴 ด่าน 2 ของใบล้าสมัย 2 ใน 5 — แก้แล้ว (ใบล้าสมัยใบที่ 4 ในสี่วัน)
| grep ในใบ | ผล | ของจริง |
|---|---|---|
| `get_login_scene_override` in runtime.py | **0** | ถูกแทนด้วย `consume_login_scene_override` (**4 hits**) ตอน GM-033 single-use ลง |
| `def login_entry_is_pinned` in **login_scene_stage.py** | **0** | อยู่ที่ **`login_scene_admission.py:197`** (1 hit) แล้ว re-export ที่ `login_scene_stage.py:356` |

⇒ ทำตามใบตรง ๆ = **"ห้ามบูต"** ปลอม ทั้งที่ด่านกันล็อกเอาต์มีอยู่ครบ · **ขอให้สาย GM แก้ด่าน 2 ในใบ** และเพิ่มบรรทัด `RECHECK:` ที่เป็นคำสั่งวัดได้จริง

## ผล

### P1 [wire] ✅ ทันทีที่พิมพ์ `/warp 2` (stderr)
```
LANE_GM_CHAT_ACTION warp route=action
GM_CHAT_STAGED_NEXT_LOGIN account='localtest' command=warp scene_id=2 coordinates=none
  next='log out and log back in to land there; nothing was sent to the client now'
```
ไฟล์ config หลังจากนั้น: `{"gm_login_scene": {"localtest": 2}}` ⇒ **สองในสามส่วนของ P1 ยืนยันตรง ๆ** (แถว ndjson ไม่ได้ตรวจในรอบนี้ — nonclaim 2)

### P2 [จอ ระหว่างล็อกอินเดิม] ✅ ไม่มีอะไรเกิดขึ้น ตรงคำทำนาย

### P3 [หัวใจของใบ] ✅ **ผ่าน**
ล็อกเอาต์ (ปิดด้วย X) → เปิด client ใหม่โดยเซิร์ฟเวอร์ยังรัน → ล็อกอิน
- wire: `WORLD_SCENE scene_id=2 seq=0 model=BG0002 name=Prison_Exile_Island spawn=(26905.000,21185.000,1680.000)`
- **จอ (เจ้าของ):** *"อยู่เกาะคุก เห็น npc"* · ภาพ: ป้ายกลางจอ **Prison Exile Island** · HUD **X:26,905 Y:21,185** = จุด spawn ของฉาก 2 เป๊ะ · เห็น NPC `Navy T...` ชื่อเขียว · **ปุ่ม GM โผล่ที่แถบล่างด้วย** (สถานะ GM ทำงาน)

### P5 [ตัวหักล้าง] ✅ **ปฏิเสธถูกต้องทั้งสอง**
```
GM_CHAT_WARP_REFUSED account='localtest' scene_id=999999 reason=unknown_scene        stageable=(1, 2, 14, 278, 997)
GM_CHAT_WARP_REFUSED account='localtest' scene_id=3      reason=scene_has_no_login_entry stageable=(1, 2, 14, 278, 997)
```
🔴 **ไม่มี `staged_login_scene` จาก `/warp 3`** ⇒ ด่านกันล็อกเอาต์ทำงานจริงบน client จริง เป็นครั้งแรก

### P4 [คู่ควบคุม] ⚪ **NOT RUN** — เจ้าของไม่มีบัญชีที่สอง (ไม่ใช่ FAIL ตามกติกาใบ)

## 🆕 ของแถม: **ฉาก 14 เข้ารายการ stageable แล้ว**
โทเคนพิมพ์ `stageable=(1, 2, 14, 278, 997)` — ต่างจาก `(1, 2, 278, 997)` ที่ใบเขียนไว้ ⇒ สาย A ลงแถวทะเบียนของฉาก 14 แล้ว (ใบเตือนไว้เองว่าถ้าเห็นเลขเพิ่มอย่าคิดว่าใบพัง)
⇒ 🔥 **`/warp 14` น่าจะพาไปเกาะภูเขาไฟนรกได้เลย** = ทางเข้า `GT-134` (BG0015 first eyes) โดยไม่ต้องบูตพิเศษ **ขอให้สาย A/GM ยืนยันแล้วอัปเดต GT-134**

### 🆕 P6 [ของแถม ไม่ได้อยู่ในใบ] ✅ **single-use กินใบทิ้งจริง**
teardown อ่านไฟล์ config หลังจบรอบ: `LOGIN_SCENE_CONFIG_CONTENT={ "gm_login_scene": {} }` — **ว่างเปล่า**
⇒ override ถูกใช้แล้วหายไปเองตอนล็อกอิน ตรงตาม `COO-DECISION 20260829_0441` ข้อ 2 และ `CORE-REQUEST-GM-033`
**นี่เป็นครั้งแรกที่ single-use ถูกยืนยันกับ client จริง** (ก่อนหน้านี้วัดได้แค่ในชุดเทส) · และแปลว่าขั้นเก็บกวาดด้วยมือไม่จำเป็นอีกแล้ว

## nonclaims
1. 🔴 **ไม่ได้แปลว่า warp ทำงาน** — ไม่มีไบต์ออกสาย ตัวละครไม่เคยข้ามฉากขณะออนไลน์ · พิสูจน์แค่ "คำสั่งในแชทจองฉากล็อกอินได้"
2. ไม่ได้ตรวจแถว ndjson ของ P1 (ตรวจเฉพาะ stderr + ไฟล์ config)
3. **ไม่อ้าง M2 หรือ milestone ใด ๆ** — เห็นเกาะเพราะ GM จองฉากไว้ ไม่ใช่เพราะเส้นทางเดินเรือทำงาน
4. P4 ไม่ได้รัน (ไม่มีบัญชีที่สอง)
5. ไม่ได้ยืนยันว่าล็อกอินรอบถัดไปกลับไปฉากเดิม (ไฟล์ว่างแล้ว แต่ไม่ได้ล็อกอินซ้ำเพื่อดู)

## 🔧 สองอย่างที่กะ1-A ซ่อมระหว่างรอบ (ops ไม่ใช่ผลใบ)
1. **`.git` stale lock** — `refs/remotes/origin/main.lock` ค้างจาก 15:00:14 ทำให้ resolver abort `no green boot commit` ซึ่ง**อ่านเหมือนด่านไม่ผ่าน** · ต้นเหตุ: กะ1-A รัน `git fetch` ใส่ repo บน Windows จากฝั่ง Linux VM · job 1367 ลบ lock (สำเนาเก็บไว้) แล้วพิสูจน์ว่า fetch = exit 0, HEAD ไม่ขยับ · **กติกาที่ขอเพิ่ม: ห้ามรัน git กับ repo นี้จากเครื่อง/เมานต์อื่น**
2. **`RELAUNCH_GAME_CLIENT.bat` แฟลชแล้วปิด** อ่านไม่ทัน — เขียนใหม่ให้ (ก) พิมพ์ผลด่านทีละข้อ (ข) รอยืนยันว่า client ขึ้นจริงภายใน 30 วิ (ค) `pause` ทุกเส้นทางออก · ไฟล์เดิม backup ไว้ที่ `pf_bridge\backup\RELAUNCH_GAME_CLIENT.bat.before_ka1a_*`

## หลักฐาน
`GameClient\capture_gt141_20260830_162539\server_console_live.err.txt` (6 บรรทัด P1+P5 ครบ) · `.out.txt` L358/L408 (`WORLD_SCENE scene_id=2`) · ภาพเจ้าของ (Prison Exile Island, X:26,905 Y:21,185) · `backup\gm_login_scene_GT141_20260830_162054.json` · outbox 1368/1365/1369/1370/1366

— กะ1-A · **ADDRESSEE: LANE-GM (ปิดใบ + แก้ด่าน 2), LANE-A (ฉาก 14 stageable -> GT-134), chief (กติกา git)**
