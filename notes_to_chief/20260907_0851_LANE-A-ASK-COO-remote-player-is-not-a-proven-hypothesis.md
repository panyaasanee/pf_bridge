ADDRESSEE: COO
FROM: LANE-A (WORLD)
ROUND: pm4jdf (claim pf_bridge#1664)
WHEN: 2026-09-07T08:51+07:00

# ท่อ promotion ข้อ 1 ของสาย A ปลดไม่ได้ ด้วยเหตุผลที่ docstring ของมันเขียนเอง

## ติดอะไร

`NOW.md` หัวข้อ "เมื่อไม่มีงานด่วน — ท่อ promotion" จัดอันดับ
**1 `remote_player_hypothesis` A** และ `COMMON_LANE_ROUND.md` นิยามงานสำรองข้อแรกไว้ว่า
"หยิบ scenario/hypothesis ในเขตตัวเองที่ **พิสูจน์แล้ว** แต่ยัง `production_allowed = false`"

รอบนี้ M2 ตัน (RE-289 ยัง OPEN ⇒ tier 3 ปฏิเสธทุก input ⇒ ใบ attended ผลิต
`HEADLESS_PROOF:` ไม่ได้) จึงลงมาที่ท่อ promotion ตามกติกา แล้วอ่านโมดูลจริง

**สิ่งที่โมดูลเขียนถึงตัวเอง** (`src/pirateforce_foundation/remote_player_hypothesis.py`
หัวข้อ `SCOPE THIS MODULE DOES NOT COVER`):

> No client has ever been shown one byte of this profile. Whether anything
> renders, what it looks like, whether the name board fills, whether frames
> 3/4 move it, and whether the negative control stays nameless are ALL the
> attended test's questions.

และหัวไฟล์:

> THIS IS OUR DESIGN, NOT THE ORIGINAL SERVER'S, WHICH IS UNRECOVERABLE.
> Every value below without a [PROVEN ...] source is a value we chose.

⇒ มันไม่ใช่ "พิสูจน์แล้วแต่ติดแฟล็ก" · มันคือ **encoder ที่ยังไม่เคยมีใครดูด้วยตาสักครั้ง**
ปลดแฟล็ก = ส่งเฟรมที่เราออกแบบเองให้ไคลเอนต์จริงโดยไม่มีใครเคยเห็นผล
ซึ่งชนบรรทัด **`ห้ามส่งเฟรมเดา`** ในบรรทัด LANE-A ของ `NOW.md` ตรง ๆ

`docs/PROMOTION_BACKLOG.md` เองก็เตือนไว้ใน nonclaims ว่า
"ไม่ได้ตรวจว่าแต่ละอันพร้อมโปรโมตจริงวันนี้" — ใบนี้คือการตรวจข้อ 1 แล้วรายงานกลับ

## ทางเลือก

- (ก) ถอด `remote_player_hypothesis` ออกจากอันดับ 1 แล้วเลื่อนตัวอื่นขึ้น
- (ข) เปลี่ยนงานของข้อ 1 จาก "ปลดแฟล็ก" เป็น **"ออกใบ attended ให้มันก่อน"**
- (ค) ยืนยันให้ปลดเลย โดยรับความเสี่ยงว่าไม่มีใครเคยเห็นผลบนจอ

## เลือกอะไรไปแล้ว

**(ข)** · ติดป้าย **[สมมติของสาย LANE-A - รอ COO ยืนยัน]** · รอบนี้ยังไม่ได้เขียนใบ
(หมดงบเวลา) แต่บันทึกเป็นงานลำดับ 2 ของรอบหน้าไว้แล้วในไฟล์รอบ

เหตุผลที่ (ข) ไม่ใช่การถ่วงเวลา: โมดูลนี้ **ติดอาวุธได้จริง** ต่างจาก M2 วันนี้ —
sweep composer มีอยู่และ arm ในฉาก 1 ผ่านไฟล์ scenario ของมัน
⇒ ใบของมัน **ผลิต `HEADLESS_PROOF:` ได้** ตาม `NOW.md` `0159` ⇒ **ขึ้นรถบัสได้**
ต่างจากใบ M2 ที่วันนี้เข้าเงื่อนไข `NO_MECHANISM_TO_ARM:` ที่ท่านยังรอ Panya ตอบอยู่

## ถ้าผิดต้องย้อนอะไร

ไม่มีโค้ดต้องย้อน — รอบนี้ไม่ได้แตะ `remote_player_hypothesis.py` เลยสักบรรทัด
ถ้าท่านตอบ (ค) รอบหน้าปลดแฟล็กได้ทันทีโดยไม่มีอะไรค้าง
ถ้าตอบ (ก) ก็แค่ข้ามไปข้อถัดไปของท่อ

## nonclaims

- ไม่ได้รันเทสของ `remote_player_hypothesis` ในรอบนี้ · อ่าน docstring กับ
  `docs/PROMOTION_BACKLOG.md` เท่านั้น
- ไม่ได้ตรวจข้อ 2 ของท่อ (`lane_a_choose_npc_scene1`) ซ้ำ — backlog ระบุเองว่าเป็น
  net regression ที่วัดแล้ว จึงไม่ใช่ตัวเลือก
- ไม่ได้อ้างว่า encoder ของมันผิด · อ้างแค่ว่า **ยังไม่มีใครดู** ซึ่งเป็นคนละเรื่องกัน
