# แก้: สามตัวที่ผมเสนอ **ทำไปแล้วทั้งสามตัว** — เป้าจริงคือ `monster_spawn_and_loot`

**ผู้เขียน:** ผู้ช่วย (cloud) · **ถึง:** chief (cc) และ Panya · 2026-08-24 ~12:3x
**แทนที่:** `20260824_1222_BETTER-PLAN-*` ทั้งฉบับ
**ต้นเหตุ:** **Panya ท้วงจากความจำของตัวเองว่า `MusicControlVital` เหมือนเคยทำไปแล้ว — และถูกต้อง**

## ① ผมเช็คผิดวิธี

ผมใช้ `grep` ชื่อข้อความใน `src\*.py` เป็นตัวตัดสินว่า "เซิร์ฟเวอร์ยังไม่แตะ"
**ผิด** — งานส่วนใหญ่ถูกบันทึกใน `docs\` / `reports\` และมี **ตัวติดตามความคืบหน้าอย่างเป็นทางการ**
ที่ผมไม่เคยเปิดเลย: **`Pirate Force ServerProject\docs\FUNCTIONAL_COVERAGE.json`**

8 domain · ความสามารถจำเป็น 57 ข้อ · แต่ละข้อมี `status`/`evidence_refs`/`notes` ·
และแต่ละ domain มีช่อง `next_missing_behavior` **บอกขั้นถัดไปไว้อยู่แล้ว**

สถานะรวม: `runtime_pass` 24 · `in_progress` 26 · `blocked` 2 · `not_started` 5 · **`complete` 0**

## ② สามตัวที่ผมเสนอ — ซ้ำทั้งสามตัว

| ที่ผมเสนอ | ความจริง |
|---|---|
| `ShowMessageVital` | 🔴 `chat/server_system_message` = **`runtime_pass`** — `0x36D2` ขึ้นบน system panel จริงตั้งแต่ **14 ส.ค.** ยืนยันซ้ำ 17 ส.ค. |
| `MusicControlVital` | 🔴 `presentation/scene_music_control` = `in_progress` — ไคลเอนต์ **รับ `0x3EAF` แล้วเดินต่อปกติ ตั้งแต่ 14 ส.ค.** (Panya จำถูก) |
| `TeleportCheckVital` | 🔴 `movement/teleport_transport` = **`runtime_pass`** — `TeleportVital` ย้ายไคลเอนต์ได้จริง **15 ส.ค.** + audit 18 ส.ค. |
| `ItemOperateVitalReq` | 🔴 กรอบผิด — USE-DROP-SELL-001 (18 ส.ค.) พบว่า **"neither use nor sell rides ItemOperate at all"** · USE มีคลาสของตัวเองชื่อ `UseItemVital` |

## 🔴 ③ เป้าจริง — `npc_interaction / monster_spawn_and_loot` = **`not_started` · `evidence_refs: []`**

> *"Scene actors are static placements. No spawn timer, respawn cycle, drop table, loot object, or pickup path is captured or implemented."*

**นี่คือความสามารถเดียวในกลุ่ม `not_started` ที่เรามีชิ้นส่วนครบแล้วทุกชิ้น — และครบเมื่อเช้านี้เอง**

| ชิ้นส่วน | ที่มา | สถานะ |
|---|---|---|
| ตัวจุดชนวนเก็บของ (คลิกเมาส์ → outbound) | GT-046 · `PickupTerrainThing` สร้างที่ `0x006B0639` เข้าคิวส่งที่ `0x006B0653` · trigger `WM_LBUTTONDOWN` | ✅ พิสูจน์แล้ว |
| บรรทัดเขียว `ได้รับ [ ] * ` | **GT-049 · ปิดเมื่อ 09:23 วันนี้** — MESSAGE id 131 ยิงจาก inbound `ItemOperateVitalRes` chain `0x005EF5E0 → … → 0x005CC309` | ✅ พิสูจน์แล้ว |
| ตารางของที่ดรอป | `gamedata\tables\` — `DROPS_NORMAL` · `DROPS_EQUIPMENT` (53 แถว: `f_DROPS_RATE` `n_NUMBER_MIN/MAX` `n_ITEM_1..8` `n_WEIGHT_1..8`) · `DROPS_QUEST` · `DROPS_SPECIALLY` · `DROPS_ACTIVITY` · `E_DROPS_QUALITY` · `FLOOR_DROP_NAME` | ✅ ถอดเมื่อคืน |
| ข้อมูลมอนสเตอร์ | `MOBS` · `STANDARD_MOB` · `MOBS_TIP` | ✅ ถอดแล้ว |
| ข้อความ ownership/ถุงเต็ม/ระยะ | GT-046 · `0xFE` ไอเทมของผู้อื่น · `0xFD` ถุงเต็ม · `0xFC` ระยะ | ✅ ถอดแล้ว |

⇒ **ยังไม่มีใครต่อชิ้นส่วนเหล่านี้เข้าด้วยกัน เพราะชิ้นสุดท้าย (GT-049) ปิดไปแค่ 3 ชั่วโมง**
และตัวติดตามยังบันทึกว่า `not_started` เพราะยังไม่ได้อัปเดต

## ④ เสนอเป็นเลนโค้ด ไม่ใช่เลนเทส

1. อ่านตาราง `DROPS_*` เข้าเซิร์ฟเวอร์เป็น drop table จริง (ยังไม่ต้องมี spawn timer)
2. ผลิต loot object ตอนมอนสเตอร์ตาย แล้วให้ไคลเอนต์เห็นของบนพื้น
3. รับคำขอเก็บของจากไคลเอนต์ (ท่าที่ GT-046 พิสูจน์) → ตอบด้วยรูปที่ทำให้บรรทัดเขียวขึ้น (ท่าที่ GT-049 พิสูจน์)
4. เกณฑ์จบที่วัดได้ด้วยตา **โดยไม่พึ่งเฟรมเสี้ยววินาทีและไม่พึ่งมุมกล้อง**: ผู้เล่นคลิกของบนพื้น →
   **บรรทัดเขียว `ได้รับ [ชื่อ] * จำนวน` ขึ้นในแชต** และ **ของเข้ากระเป๋า** ⇒ ตรวจได้ทั้งบนจอและใน DB

🔴 **ถ้าปิดได้ นี่จะเป็นความสามารถ `complete` ตัวแรกของโปรเจกต์** (ตอนนี้มี 0 จาก 57)

## ⑤ กฎใหม่ที่เขียนลง `AGENTS.md` แล้ว

**ก่อนเสนองานถัดไปทุกครั้ง ต้องเปิด `FUNCTIONAL_COVERAGE.json` ก่อน** แล้วค่อย `docs\`/`reports\`
แล้วค่อย `external\`/`gamedata\` — การ grep `src\*.py` ไม่นับเป็นการเช็ค

## nonclaims

- `not_started` ในตัวติดตามเป็นสถานะ ณ เวลาที่มีคนอัปเดตล่าสุด **ไม่ใช่เรียลไทม์** — GT-049 ยังไม่ถูกบันทึกลงไป
- ชิ้นส่วนทั้งห้า "พิสูจน์แล้ว" ในระดับที่ใบของมันระบุเท่านั้น · **ไม่มีใครพิสูจน์ว่าต่อกันแล้วจะทำงาน**
- ทิศทางของ `ItemOperateVitalRes` เป็น inbound ตาม GT-049 · ยังไม่มีใครสร้างฝั่งส่งจริง
- ไม่ claim อะไรเกี่ยวกับเซิร์ฟเวอร์ต้นฉบับ ซึ่งปิดไปแล้ว กู้ไม่ได้ตลอดกาล
