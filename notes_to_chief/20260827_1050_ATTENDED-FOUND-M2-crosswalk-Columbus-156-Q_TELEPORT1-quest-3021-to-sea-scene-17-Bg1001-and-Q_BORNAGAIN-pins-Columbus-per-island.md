[ถึง: **chief** (M2 20:00) · **สาย A** · RE runner · cc COO · Panya | จาก: เซสชัน attended กะ1 | 2026-08-27 10:50 (+07:00) | ต่อจาก 1040 §2 — ตรวจแล้วได้ field จริง]

# FOUND — crosswalk ของเส้นทาง M2 อยู่ในตารางเควส: **Columbus 156 → `Q_TELEPORT1` quest 3021 → ปลายทาง scene 17 (`Bg1001` "Ship in the Sea")** · และ `Q_BORNAGAIN` ปักว่า Columbus ตัวไหนเป็นของเกาะไหน (Prison Exile = **360** ไม่ใช่ 36)

ทั้งหมดอ่านจาก `gamedata/tables/` ตรง ๆ (ไม่มีการอนุมาน) — grep ซ้ำได้ทุกบรรทัด

## ① Columbus ทุกตัวถือเควสสองชนิด (`MOBS.s_QUEST_BEGIN/END` → `QUESTDATA_TH__QUEST`)

| Columbus `n_ID` | `Q_TELEPORT1` (n_TYPE 20) | `n_VARI` → **scene ปลายทาง** | ข้อความเควส (`QUESTTEXT`) | `Q_BORNAGAIN` → `n_VARI_1` = **ฉากบ้าน** |
|---:|---|---|---|---|
| **156** (Port Royal) | **3021** | `111, 17` → **17 = `Bg1001` 海上一艘船 "Ship in the Sea"** | "มุ่งหน้าไป Atlantic Ocean：Rising Sun Sea" | 3205 → **1** Port Royal ✓ |
| 360 | 3022 | `111, 18` → 18 `Bg1002` | Rising Sun Sea | 3206 → **2 Prison Exile** |
| 36 | 3023 | `19` → `Bg1003` | Rising Sun Sea | 3207 → **3 Spice Paradise** |
| 67 | 3024 | `20` → `Bg1004` | Dark Fog Sea | 3208 → (ตรวจต่อ) |
| 105 | 3025 | `21` → `Bg1005` | Dark Fog Sea | 3209 |
| 196 | 3026 | `39` → `Bg1023` "Sea Desert Island" | Outer space Ocean：Taboo Sea | 3210 |
| 362 | 3027 | `40` → `Bg1024` | — | 3211 |

- scene 17–23 = `Bg1001..Bg1007` ชื่อจีน "海上一/二/三艘船" (เรือ 1/2/3 ลำกลางทะเล) `n_SCENE_TYPE 4` = ฉากทะเลที่ RE-096 พูดถึง (`VEHICLE` row ของ Bg1001..1007) — **นี่คือ "แมพทะเล" ในคำเจ้าของ 16:00 เมื่อวาน** ที่ตัวละครกลายเป็นเรือ
- `Q_BORNAGAIN` = เควส "เกิดใหม่/กลับบ้าน" ที่ n_VARI_1 คือฉากบ้านของ Columbus ตัวนั้น ⇒ **field จริงที่บอกว่า Columbus ตัวไหนอยู่เกาะไหน**: 156 → Port Royal (ตรงคำเจ้าของ) · **360 → Prison Exile** · 36 → Spice ⇒ แก้ 1040 §2: ขอบบล็อก 36–66 = Spice ตามเดิม (ไม่ต้องเลื่อน) และ Columbus ของเกาะคุกคือ 360 (ตัวเพิ่มทีหลัง ไม่อยู่ในบล็อก 1–35)
- `111` ตัวแรกใน n_VARI ของ 3021/3022 น่าจะเป็นเงื่อนไข (quest 111 เป็นเควส `Q_CON_NEW` ฉาก 1 ที่ Columbus 156 ถือเอง) — **สมมติฐาน** ให้ RE/สาย A ดู lua `Q_TELEPORT1` ว่า VARI_1 คืออะไรจริง
- 156 ยังถือ `Q_ENTER_INSTANCE6` 7062/7063 (n_VARI `7060, 1026, 2600001, 1, 2`) = ทางเข้า instance — ไม่เกี่ยว M2 แต่จดไว้

## ② ผลต่อ M2 (กำหนด 20:00 วันนี้ — 0310 ③ / 0915 ①.1)

สเปคต่อสายที่วัดได้ครบแล้ว ไม่ต้องรอ RE อีก:
1. ผู้เล่นคุย **Columbus 156** ที่ index 1 (owner-confirmed) → ไคลเอนต์ส่ง `NPCConversation`/`QuestOperate op1` ด้วย quest id แบบไดนามิก (RE-094) — quest ที่ต้องเสนอ/ตอบคือ **3021** (`Q_TELEPORT1`, lua `_F_FLEX_000`/`_F_TALK_000`)
2. เซิร์ฟเวอร์ตอบด้วย transfer ไป **scene 17 (`Bg1001`)** ผ่านเส้นทาง scene entry เดิม (world_scene_entry/scene_load) · ตัวละครในฉากนี้เป็นเรือ (RE-085: actor เดิมสลับ vehicle module · RE-096: VEHICLE row ยังเลือกไม่ได้ = ข้อจำกัดที่ต้องแจ้งในใบ attended)
3. เทียบท่าเกาะ = RE-086 (client เช็คระยะ 500 → `EnterInstance`) · รายงานกัปตัน = RE-087 · ปลายทางเกาะ = scene 2/3/… ตามท่าที่เลือก
⇒ **ใบ attended M2 ควรเขียนเกณฑ์ชั้นจอเป็น: คุย Columbus (ที่ index 1) → มีตัวเลือก "มุ่งหน้าไป Atlantic Ocean：Rising Sun Sea" → หน้าโหลด → minimap ขึ้น "Ship in the Sea" → ตัวละครเป็นเรือ**

## ③ ของแถมสำหรับ scene 17 (`Bg1001`)

`Bg1001.npc`: 6 definitions (ชุด 1,2,2,4,5,6 — เลข 2 ซ้ำสองครั้ง) · 8 placements · รูปแบบเดียวกับ Bg1002–1007 ⇒ ชุดในฉากเรือน่าจะเป็น "ตำแหน่งเรือ/ท่า" ไม่ใช่ NPC — **สมมติฐาน** ให้สาย A ดูประกอบ RE-096/RE-100

— เซสชัน attended กะ1 · ไม่แตะโค้ด
