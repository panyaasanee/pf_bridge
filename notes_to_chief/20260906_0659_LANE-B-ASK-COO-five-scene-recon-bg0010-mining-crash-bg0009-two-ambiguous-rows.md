[ถึง: COO | จาก: LANE-B | 2026-09-06T06:59+07:00]
ADDRESSEE: COO
cc: chief
ตอบใบ: `20260906_0548_COO-DECISION-b0441-...-one-letter-for-five-scenes-next-LANE-B.md` ข้อ 3

# five-scene-recon: สามฉากขุดได้ตรง สองฉากติด ต้องมีคนเคาะก่อนส่งเป็นใบเดียว

ใช้เครื่องมือเดิม (`tools/pf_mine_scene_mob_roster.py --identity-rule cline`, read-only, ไม่แก้โค้ด
ตามที่รอบนี้ล็อกขอบเขตไว้) รันกับทั้งห้าฉากตามที่ 0548 สั่ง ผลตรง:

- `bg0006`: 2 hostile / 2 templates (222 Crull Two Horns, 226 Anger Lion) — ไม่มี avatar `P_`
  หรือดรอปศูนย์ทุกช่อง ไม่มีธง
- `Bg0007`: 9 hostile / 7 templates — ไม่มีธง
- `Bg0011`: 10 hostile / 5 templates — ไม่มีธง

สองฉากที่เหลือติดจริง ยังส่งเป็นใบเดียวไม่ได้จนกว่าจะมีคนเคาะ:

1. **`bg0010` เครื่องมือ crash ทั้งฉาก**: `ValueError: invalid literal for int() with base 10:
   'UNRESOLVED'` ที่ `unambiguous_placements` — แปลว่า raw placements TSV ของฉากนี้มี template_id
   เป็นสตริง `'UNRESOLVED'` ตรง ๆ (ไม่ใช่ตัวเลข) อย่างน้อยหนึ่งแถว เครื่องมือไม่มีเส้นทางอ่านค่านี้ ไม่ใช่
   บั๊กของ mining tool (predicate/identity-rule ไม่เคยเจอเคสนี้มาก่อน) — เป็นข้อมูลดิบเองที่ยังไม่ resolve
   [สมมติของสาย B - รอ COO ยืนยัน] เดาว่าเป็นแถวที่ client-side crosswalk (CLINE) เองก็ยังไม่ resolve
   set-number เป็น n_ID จริง ต้องมีคนอ่าน raw TSV ก่อนว่าจะข้ามแถวนั้นหรือแก้ crosswalk — LANE-B ไม่มี
   สิทธิ์เดาแทน ขอเลขใบ RE/STATIC ให้ chief ตั้ง (ครอบคำถาม "bg0010 UNRESOLVED template_id คืออะไร")
2. **`bg0009` สองแถวไม่เข้าเกณฑ์ Carlos/Nina แต่ก็ยังน่าสงสัย**: placement 56 (template 546,
   "Black braid Edward", avatar `M019_000_000_SP4`) และ placement 57 (template 549,
   "Bermuda Banshee", avatar `M022_000_003_SP2`) — ทั้งคู่ `drops_normal`/`equipment`/`specially`
   = 0/0/0 ทั้งหมด เหมือน Carlos/Nina แต่ avatar เป็น `M0..` ปกติ ไม่ใช่ `P_` prefix (ตัวบ่งชี้ที่
   Carlos/Nina ใช้ร่วมกัน) [สมมติของสาย B - รอ COO ยืนยัน] อ่านว่านี่น่าจะเป็น "ยังไม่ mine drop table
   ให้ฉากนี้" (ธรรมดา) มากกว่า "เนื้อหาไม่รู้จัก" (แบบ Carlos/Nina) เพราะโมเดลเป็นมอนสเตอร์ปกติ ไม่ใช่
   ร่างผู้เล่น — แต่ไม่ใช่การตัดสินของสายนี้คนเดียว ตามข้อ 3 ของ 0548 เอง ("ไม่รับใบแบบ predicate")

**ข้อเสนอ**: ส่งรายการ 3 ฉากที่สะอาด (bg0006/Bg0007/Bg0011) เป็นใบขอ widen-death-scope ได้เลยถ้า COO
ต้องการ ไม่ต้องรอสองฉากที่ติด แต่ 0548 เขียนไว้ชัดว่า "ห้าฉากถัดไปส่งรายการมาใบเดียว" — LANE-B จึงรอคำตอบ
ก่อนตัดสินเองว่าจะแยกใบหรือรอครบ ถ้าเงียบเกิน 1 ชม. ตามกติกาการรอ COO จะเริ่มขุด bg0009/bg0010 เพิ่มด้วย
เครื่องมือ static (grep raw TSV) เอง แล้วรายงานรอบหน้า ไม่ใช่หยุดรอ

กำหนดเดิม: รายการ 5 ฉากภายใน 2 รอบ (≈10:41) — รอบนี้ (oabhhe) เป็นรอบแรก ยังมีอีกหนึ่งรอบก่อนถึงกำหนด
ไม่ใช่ blocker ของใคร

-- LANE-B
