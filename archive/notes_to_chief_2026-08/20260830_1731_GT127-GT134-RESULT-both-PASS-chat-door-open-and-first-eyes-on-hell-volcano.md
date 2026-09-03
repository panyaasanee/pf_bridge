# GT-127 + GT-134 RESULT — 🟢 **PASS ทั้งคู่ ในบูตเดียว** · ประตูคำสั่งแชทเปิดจริง (ndjson 8 แถว) · **ตาคู่แรกของโปรเจกต์บนเกาะภูเขาไฟนรก** (81 actor)

ถึง: **สาย GM (GT-127 · ADDRESSEE: LANE-GM)** · **สาย A (GT-134 · ADDRESSEE: LANE-A)** · chief · cc COO, RE
จาก: attended session "กะ1-A" (Panya ขับ UI เอง) · **OBSERVER_CONFIRMED: 2026-08-30T17:1x+07:00**
**เจตนาของรอบ: ปลดสองสายที่ประกาศว่าว่างงาน** — สาย GM ว่างสามรอบติด (เรียกกฎ F เอง 15:18/16:17) · สาย A *"no build waiting on RE-155 and GT-134"* (12:26)

## บูต
BOOT_COMMIT **57490434** = main HEAD ไร้แฟล็ก · grep 6/6 · pytest ผ่าน · code-delta 0 · canonical UNCHANGED · teardown 1374 PASS · ไม่มีวิดีโอ · config GM สองไฟล์เป็นของทิ้ง **ของจริงไม่ถูกแตะ** · jobs 1372/1373/1374/1376

---

## GT-127 = PASS ชั้น wire (ชั้นที่ใบใช้ตัดสิน)

**ndjson `capture/gm_command_log.ndjson` = 8 แถว** = 4 คำสั่งที่รู้จัก × 2 แถว (parse + `outcome` ของ `CORE-REQUEST-GM-032`) ตรงเกณฑ์ "คอมมิตใหม่" ของใบเป๊ะ · ทุกแถว `"executed": false`

| พิมพ์ | stderr | ndjson |
|---|---|---|
| `/lv 30` | `LANE_GM_CHAT_ACTION lv route=action` + `GM_CHAT_NO_BYTES_SENT why=refused_no_wire_path` | 2 แถว ✅ |
| `/warp 2` | `GM_CHAT_STAGED_NEXT_LOGIN scene_id=2` | 2 แถว ✅ |
| `/say ทดสอบ` | `GM_CHAT_NO_BYTES_SENT why=withheld_gm_global_message_vital_version` (เกต `gm/say_wire.py` ปิด) | 2 แถว ✅ |
| ประโยคธรรมดา `สวัสดี` | เงียบ | **0 แถว** ✅ |
| `/notacommand xyz` | `GM_CHAT_COMMAND_REFUSED reason=command_parse_error_GmCommandParseError` | **0 แถว** ✅ |
| `/warp 14` | `GM_CHAT_STAGED_NEXT_LOGIN scene_id=14` | 2 แถว ✅ |

**P3 (บนจอ) ✅** เจ้าของยืนยันว่าไม่มีอะไรเกิดขึ้นบนจอเลย — ตรงคำทำนายของใบ (เลนนี้ต้องมองไม่เห็น)
**P4 (ตัวหักล้าง) ไม่เกิด** — คอนโซลไม่ได้เงียบ ⇒ จุดเรียกต่อสายจริง

### 🎁 ของแถม: คำสั่งปฏิเสธพ่นรายการคำสั่ง GM ทั้งหมดออกมา
```
usage='warp <scene_id> [x y] | npc on|off <mob_id> | item <id> <n> | lv <n> | spawn <mob_id> | say <message>'
```
**มีหกคำสั่ง** · วันนี้ `lv` = `refused_no_wire_path` · `say` = `withheld_..._vital_version` · `warp` = ใช้ได้ (staged)
❓ **ขอสาย GM ตอบในกล่อง:** `npc on|off` · `item` · `spawn` — สามตัวนี้มีสายส่งกลับแล้วหรือยัง และตัวไหนใกล้ใช้ได้ที่สุด (เจ้าของสนใจ `spawn` เป็นพิเศษ)

---

## GT-134 = PASS · **ตาคู่แรกของโปรเจกต์บน `Bg0015`**

```
WORLD_SCENE scene_id=14 seq=0 model=Bg0015 name=Hell_Volcano_Island
  spawn=(-17513.000,18989.000,1894.000) sent_before=NO population=bg0015_roster marker=14
WORLD_CENSUS_BG0015 assembled=81/91 shippable=81 wire=81 bodies=ok pc=14866B
  anchor=(-17513,18989,1894) source=bg0015_full_roster shortfall=identity_unresolved
[G>] WORLD_CENSUS_LANE_SCENE14_INITIAL_81 (14879 bytes)
```
**`sent_before=NO`** = ฉากนี้ไม่เคยถูกส่งมาก่อนเลยในประวัติโปรเจกต์

**จอ (เจ้าของ + ภาพ 2 ใบ):** ป้ายแมพ **Hell Volcanic Island** · spawn ที่ X:-17,513 Y:18,989 มีหอคอยและผลึกลาวา · เดินไปเจอ **Nightmare Claw beast** ×2 และ **Greedy Troll** (HP **260,787** LV 1) · ภูมิประเทศภูเขาไฟเรนเดอร์ครบ

**81 ตัวที่ส่งจริงมีชื่อจริงครบ** เช่น Earth Flame Dragon · Hell King Kong · Lava shakers · Hell Ghoul · Horror butcher Lasa · Baroque · Angelina · Sea Phantom · Big Sword · Carlos

### 🔴 สามช่องว่างที่รอบนี้เปิดออกมา (งานของสาย A)

**① สำมะโนมาหลังผู้เล่นขยับ — ช่องว่าง M1-P ข้อ ① ตัวเดิมเป๊ะ**
เจ้าของ (คำต่อคำ): *"เริ่มมายังไม่มีตัวอะไรเกิด ต้องขยับก่อนแล้วถึงค่อยๆ ไล่กันเกิด"*
คอนโซลยืนยัน: **`TargetPosVital` ที่ L712 · สำมะโนที่ L717** ⇒ สำมะโนตามหลังการขยับ
⇒ **`CORE-REQUEST-026` (arrival census) ที่ GT-121 พิสูจน์แล้วกับ Bg0002 ยังไม่ถูกยกมาใส่ Bg0015** — งานชิ้นเดียว ก๊อปกลไกเดิม

**② `MOB_CENSUS_HOSTILITY scene_id=14 scene=? roster=0 backed=0 override=not_reported`**
ฉาก 14 **ไม่มี combat roster เลย** ⇒ มอนที่นั่นตีไม่ได้ (กำแพงคลาสเดียวกับที่ Bg0002 เพิ่งพังเมื่อวาน — ดู `_sync_combat_scene_state`) · และ `scene=?` แปลว่าชื่อฉากไม่ resolve ในระบบนั้น

**③ `shortfall=identity_unresolved` — 10 ตัวจาก 91 ไม่ถูกส่ง**

**④ ชื่อ Nightmare Claw beast ขึ้นสีเขียว** ⇒ ตระกูล `RE-155` เดิม · **หลักฐานเพิ่มว่าไม่ใช่ปัญหาเฉพาะ Port Royal** เป็นทั้งเอนจิน

---

## nonclaims
1. GT-127 ไม่อ้างว่าคำสั่งใด **ทำงาน** — ทุกแถว `executed: false` ตามที่ใบกำหนด · พิสูจน์แค่ "เซิร์ฟเวอร์อ่านและ parse ได้"
2. GT-127 **P2 คู่ควบคุมบัญชีนอก allowlist ไม่ได้รัน** — เจ้าของไม่มีบัญชีที่สอง (ทำได้ 2 ใน 3 ของ P2)
3. GT-134 ไม่อ้างว่าฉาก 14 เล่นได้ครบ — วัดแค่ "มีสิ่งมีชีวิตขึ้นจอ" · ไม่ได้ตี ไม่ได้คลิก ไม่ได้ตรวจตัวตนทีละตัว
4. **ไม่อ้าง M2 หรือ milestone ใด ๆ** — เห็นเกาะเพราะ GM จองฉากไว้ ไม่ใช่เพราะเส้นทางเดินเรือทำงาน
5. ไม่ตัดสินสาเหตุสีชื่อ (`RE-067`/`RE-155`)

## ต่อไป (เสนอ)
1. **สาย A: ยก arrival census มาใส่ Bg0015** — ช่องว่าง ① ชัดเจนที่สุดและมีกลไกพร้อมอยู่แล้ว · แล้วตามด้วย ② combat roster ของฉาก 14
2. **สาย GM: ปิด GT-127 PASS** + ตอบคำถามคำสั่งสามตัว (`npc`/`item`/`spawn`)
3. **RE-155** ยังเป็นตัวบล็อกสาย A ที่เหลืออยู่ — รอบนี้เพิ่มหลักฐานให้มันอีกฉากหนึ่ง

## หลักฐาน
`capture_gt127_20260830_170453\server_console_live.err.txt` (7 บรรทัด GM chat) · `.out.txt` L593/L712/L717/L809/L810 · `capture\gm_command_log.ndjson` 8 แถว · ภาพเจ้าของ 4 ใบ (เกาะคุก + ภูเขาไฟ) · outbox 1372/1373/1374/1376

— กะ1-A · **ADDRESSEE: LANE-A (ข้อ 1), LANE-GM (ข้อ 2), chief (ปิดหัวใบทั้งสอง)**
