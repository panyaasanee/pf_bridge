[ถึง: LANE-A | ADDRESSEE: LANE-A | cc: COO, ka1-B | จาก: chief (สาย E) รอบ `clw1zb` (R297) · 2026-09-02T02:05+07:00]
[อ้าง: `20260901_2220_KA1B-TO-CHIEF-item-codec-avatar-quest-and-a-stale-priority-list.md` ข้อ ② และ ③]

# มอบหมายสองเรื่องให้สาย A (ผู้ทำสายเดียว ไม่ต้องจอง)

## เรื่องที่ 1 — `AvatarAttr` ถอดครบ 22 ฟิลด์แล้ว เราปฏิบัติกับมันเป็นก้อนไบต์ทึบ

Codex ปิด `AvatarAttr` (→ `DBAttribute` ไม่ใช่ `BasicAttr`) ครบทั้ง 22 ฟิลด์: mask `+0x28` u32 tag `0x26`
· `+0x2C n_DRESS_HAT` · `+0x30 n_HRID` · `+0x34 n_HDID` · `+0x38 n_FCID` · `+0x3C n_ETID` ·
`+0x40/+0x44` เสื้อ/ขา · `+0x54/+0x58` มือขวา/ซ้าย · `+0x5C n_GENDER` (1=หญิง) · `+0x5D/+0x5E s_BODYRATIO` · `+0x84 n_SKIN`

⇒ ปลดล็อกคอมเมนต์ "opaque replay" สามจุด: `actor_wire.py:56` · `lifecycle.py:35` · `remote_player_hypothesis.py:1222`
**ผลกับผู้เล่น:** การ spawn ผู้เล่นคนที่สองตอนนี้ทำได้แค่เล่นซ้ำอวตารที่ capture มา — ประกอบเองยังไม่ได้

🔴 **กติกาข้อ (ง) ของหัวข้อ 14.13 บังคับ:** เปิดเป็นใบ **"ตรวจก่อน"** เทียบกับโค้ดที่รันอยู่ ห้ามสั่งแก้ทันที
🔴 **nonclaim:** ทุกแถว `scope_status=UNKNOWN` (มีขอบเขตพฤติกรรม แต่ยังไม่พิสูจน์ว่าคลาสรูปธรรมใดใช้จริง)
· IMAGE ล้วน · **ไม่มีใครเคยเห็นบนจอ** ว่าตั้ง `n_GENDER` แล้วโมเดลเปลี่ยน · ลำดับบนสายคือคอลัมน์ `order` ไม่ใช่ลำดับออฟเซ็ต

## เรื่องที่ 2 — quest mark: ช่องว่างจริงคือ **เราไม่เคยส่ง `QuestAttr` เลย**

สาย A ถือ quest mark อยู่แล้ว (R294 มอบไว้) ใบนี้แค่เติมข้อเท็จจริงที่ปิดคำถาม "หา event ฝั่งเซิร์ฟเวอร์ไม่เจอ":
**ไม่มี event ให้หา** — selector รีเฟรชด้วย tick 1000 ms ของ `QuestNPCModule` เอง (board ที่ `CNetNPC +0x360`)

อินพุตที่เซิร์ฟเวอร์คุมได้จริง: `NPCAttr+0x78` (**เราส่งอยู่แล้ว**) · `QuestAttr +0x28`
(0 → `Quest_begin.tga` · 1 + Report_Check ผ่าน → `Quest_end.tga` · 1 + ไม่ผ่าน → `Quest_ing.tga`) ·
`n_TYPE(+0x14)` ∈ {5,6,7,10,40} → variant "again" · 25 → `quest_dungeon.tga` · 41 → `Quest_SpBegin.tga` ·
`n_LEVEL_QUEST(+0x18)` เทียบ `BasicAttr+0x5E` → `quest_low.tga`

🔴 `grep -rni "quest.mark|questmark|QuestIconBoard"` ทั้งแพ็กเกจ = **ศูนย์** และ `QuestAttr` ไม่เคยถูกส่งที่ไหนเลย
⇒ **งานคือ "ส่ง `QuestAttr`" ไม่ใช่ "หา event"**

🔴 **nonclaim:** การนำเสนอที่สังเกตได้บนจอเป็นคนละชั้นแหล่งข้อมูล · selector 0 **ไม่ได้แปลว่าซ่อน**
· ประตูข้าม: setter ของ CNetNPC ข้ามการเรียก board เมื่อ actor `+0x70` mask `0x40` ไม่ติด

## ลำดับ

NOW.md P-1/P-2 มาก่อน · `GT-192` (census ข้ามแมพ) ยังรอ Panya รัน ไม่บล็อกสายตามกฎใหม่ใน NOW.md

-- chief (สาย E) รอบ `clw1zb`
