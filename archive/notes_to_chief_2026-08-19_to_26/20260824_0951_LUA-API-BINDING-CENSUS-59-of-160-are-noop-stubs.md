# สำมะโน binding ของ Lua API 160 ชื่อ — **59 ชื่อผูกกับ stub ที่ไม่ทำอะไร** · แก้คำแนะนำผิดของผู้ช่วย

**ผู้เขียน:** ผู้ช่วย (cloud · อ่านอิมเมจผ่าน mount แบบเปิดอ่านอย่างเดียว) · **ถึง:** chief (cc) และ Panya
**เวลา:** 2026-08-24 ~09:5x (+07:00) · **ต่อจาก:** `RE-057` (พบว่า `Scene.PlacementOFF` bind เป็น no-op)

---

## 🔴 ① แก้คำแนะนำที่ผู้ช่วยให้ผิดเมื่อ 01:2x

จดหมาย `20260824_0124_GAMEDATA-LUA-API-SPEC-*` เขียนไว้ว่า
> *"ลำดับที่ข้อมูลบอกเองคือ `Player.MobAppear` (3,532) มาก่อนทุกอย่างอย่างขาดลอย"*

**ผิด** — `Player.MobAppear` ผูกกับ stub `0x0045FA00` ซึ่งไม่ทำอะไรเลย
ถ้าเริ่มสร้างเซิร์ฟเวอร์ตามคำแนะนำนั้น จะได้ implement ฟังก์ชันที่ไคลเอนต์ build นี้ไม่เคยเรียกเข้าไปจริง
**ห้ามใช้ `call_count` เพียงอย่างเดียวเป็นลำดับความสำคัญ** ต้องอ่านคู่กับคอลัมน์ `binding_status` ที่เพิ่มให้แล้ว

## ② วิธี (ยกมาจาก RE-057 แล้วขยายให้ครบ 160 ชื่อ)

1. map VA→file offset จาก PE section table จริง (6 sections · `.text` delta `0x400C00` · `.rdata` delta `0x401C00`)
   🔴 ผู้ช่วยพลาดข้อนี้ก่อนหน้าโดยใช้ delta ของ `.text` กับที่อยู่ใน `.rdata` — อ่านได้ขยะ แก้แล้ว
2. หาชื่อเมธอดเป็น ASCII แบบคั่นด้วย NUL ทั้งสองข้างใน image
3. หา `68 <nameVA>` (push imm32) ใน `.text`
4. อ่าน `C7 44 24 xx <imm32>` (`mov [esp+X], delegate`) ในหน้าต่างถัดไป
5. เปิด body ของ delegate — `33 C0 C2 04 00` (`xor eax,eax; ret 4`) = stub ไม่ทำอะไร

**ตัวควบคุม:** `PlacementOFF` → `0x0045FA00` — **ตรงกับผล RE-057 ที่หาด้วยคนละท่า โดยอิสระ**

**การตรวจสอบวิธี:** ระยะจาก `push` ถึง `mov delegate` = **9 ไบต์ ทั้ง 109/109 จุดที่เจอ**
(ถ้าวิธีคว้า delegate ของ registration ข้างเคียงผิด ระยะจะกระจาย ไม่คงที่)
และผลแยกเป็นสองกลุ่มชัด: กลุ่มหนึ่งใช้ **ที่อยู่เดียวกันทั้งหมด** อีกกลุ่ม **ที่อยู่ต่างกันทุกตัว** —
ถ้าเป็นการคว้ามั่ว จะไม่ได้รูปแบบสองขั้วแบบนี้

## ③ ผล

| สถานะ | ชื่อ | จุดเรียกรวม |
|---|---:|---:|
| **`STUB_NOOP`** ผูกกับ `0x0045FA00` | **59** | **5,874** |
| `IMPLEMENTED` ผูกกับฟังก์ชันจริง (ที่อยู่ต่างกันทุกตัว) | 47 | 5,568 |
| `UNRESOLVED` หา binding ไม่ได้ด้วยวิธีนี้ | 51 | 1,204 |
| `AMBIGUOUS` ชื่อซ้ำข้าม namespace ได้ delegate ขัดกัน | 3 | 7 |

คอลัมน์ใหม่ใน `gamedata\PF_GAMEDATA_LUA_API.tsv`:
`binding_status` · `delegate_va` · `delegate_body6` · `registration_va` · `binding_note`

**12 อันดับแรกของฝั่ง stub:** `Player.MobAppear` 3,532 · `Quest.SetFlag` 417 · `Mob.AddBuff` 411 ·
`Player.RemoveItem` 367 · `Scene.PlacementOFF` 173 · `Quest.MobKillCount` 128 · `Scene.PlacementON` 96 ·
`Quest.SetQuestFlag` 90 · `Player.CastSkillAt` 69 · `Player.ShowMessage` 61 · `Quest.ReportDailyQuest` 61 ·
`Quest.CountDownTime` 54

**ตัวอย่างฝั่ง implemented:** `Player.AddItem` `0x00460FF0` · `Quest.RewardItemSelect` `0x00608A90` ·
`Mob.ShowAnimation` `0x00448900` · `Quest.GetQuestFlag` `0x006083C0` · `Player.CheckItemNum` `0x00460B30`

## ④ 🟡 สมมติฐาน — **ยังไม่พิสูจน์ อย่าสร้างอะไรบนนี้**

รูปแบบที่เห็นด้วยตา: ฝั่ง stub เต็มไปด้วยการกระทำที่ **เซิร์ฟเวอร์ต้องเป็นคนตัดสิน**
(`MobAppear` · `SetFlag` · `AddBuff` · `RemoveItem` · `CastSkillAt` · `Teleport` · `Warp` ·
`EnterInstance` / `LeaveInstance` · `OpenStorage` · `SetPVPFaction` · `CallMob` · `StartMove` / `EndMove`)

**ถ้าสมมติฐานนี้จริง รายชื่อ 59 ตัวคือรายการที่มีค่าที่สุดในโปรเจกต์** — มันคือฟังก์ชันที่เซิร์ฟเวอร์ต้นฉบับ
"ต้องมี" โดยโครงสร้าง ไม่ใช่โดยการเดา

🔴 **แต่มีหลักฐานที่ขัดอยู่:** `Player.AddItem` · `AddExp` · `AddCash` · `AddSkillPoint` **เป็น implemented**
ทั้งที่เป็นการกระทำที่เซิร์ฟเวอร์ควรตัดสินเหมือนกัน ⇒ **เส้นแบ่งจริงยังไม่รู้**
อาจเป็น "ส่ง request" vs "ทำเอง" หรืออย่างอื่น — **ต้องเปิด body ของฝั่ง implemented ดูก่อนจึงจะรู้**

## ⑤ ร่างใบที่เหลือ — **RE-059** (เล็กลงมากเพราะสำมะโนทำไปแล้ว)

**objective:** ยืนยันสำมะโนบนสะพาน + ปิดช่องที่วิธี cloud ปิดไม่ได้

1. **ยืนยันซ้ำ** — รันสำมะโนเดียวกันบนสะพานกับอิมเมจที่พิน (sha `9627211412ac…`) เทียบผลรายชื่อ
   ต้องได้ 59 / 47 / 51 / 3 เท่ากัน · **ตัวควบคุมบังคับ: `PlacementOFF` ต้องออกมาเป็น stub**
2. **ปิด `UNRESOLVED` 51 ชื่อ** — 1,204 จุดเรียกที่ยังไม่รู้สถานะ · หาว่าทำไมท่านี้หาไม่เจอ
   (ชื่อไม่ได้อยู่เป็น ASCII แยก? registration คนละรูปแบบ? อยู่ใน namespace table อื่น?)
3. **ปิด `AMBIGUOUS` 3 ชื่อ** — `CheckSoulmate` · `GetGuildRank` และอีกหนึ่ง: ชื่อเดียวถูก register
   หลายจุดด้วย delegate ต่างกัน ⇒ ต้องแยกว่า registration ไหนเป็นของ namespace ไหน
   (สำมะโนนี้ key ด้วย **ชื่อเมธอดล้วน** ไม่ใช่ `Namespace.Method` — นั่นคือข้อจำกัดของมัน)
4. **เปิด body ฝั่ง implemented อย่างน้อย 5 ตัว** (`AddItem` `AddExp` `RewardItemSelect`
   `ShowAnimation` `GetQuestFlag`) ดูว่ามัน "ส่งแพ็กเก็ต" หรือ "ทำงานในเครื่อง"
   ⇒ ข้อนี้ตัดสินสมมติฐาน ④ · **ผลลบมีค่าเท่าผลบวก**

**pass criteria:** ตอบได้ประโยคเดียวว่าเส้นแบ่ง stub/implemented คืออะไร หรือประกาศว่ายังตอบไม่ได้พร้อมเหตุ ·
sha อิมเมจก่อน-หลังตรงกัน · ชั้น client-observable **ว่างเปล่าโดยเจตนา**

## ⑥ 🔴 nonclaims

- สำมะโนนี้ทำจาก **cloud ผ่าน mount** ไม่ได้รันบนสะพาน — จ็อบ 1 ของ RE-059 คือการยืนยัน
- **`STUB_NOOP` แปลว่า "ไคลเอนต์ build นี้ไม่ทำอะไรเมื่อสคริปต์เรียก"** ไม่ได้แปลว่าเซิร์ฟเวอร์ต้นฉบับทำอะไร
  และไม่ได้แปลว่าฟังก์ชันนั้นไร้ความหมาย — เซิร์ฟเวอร์ต้นฉบับปิดไปแล้ว กู้ไม่ได้ตลอดกาล
- **`IMPLEMENTED` ไม่ได้แปลว่าทำสิ่งที่ชื่อบอก** — พิสูจน์แค่ว่า delegate ไม่ใช่ stub
- **51 ชื่อที่ resolve ไม่ได้ = ไม่รู้** ห้ามนับเป็น stub และห้ามนับเป็น implemented
- ตัวเลข `call_count` ยังเป็นความถี่ในซอร์ส **ไม่ใช่ความถี่ตอนรัน**
