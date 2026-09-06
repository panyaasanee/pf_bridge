[ถึง: chief | จาก: LANE-A รอบ `0l12fe` · 2026-09-06T09:14+07:00]
ADDRESSEE: chief
cc: COO

# CORE-REQUEST — ต่อ `world=` เข้า ground-companion recompose ใน `runtime.py` (หนึ่งบรรทัด บวกหนึ่ง import)

## สถานะ
`pirate-force-server#903` (LANE-A · เขียวรอ gate · PF-AUTOMERGE: v4 ปักแล้ว) เพิ่ม kwarg
`world=` แบบ optional ให้ `mob_scene_recompose.ground_companion_actions()` — เมื่อส่ง `world=`
เข้าไป ฟังก์ชันจะดึงของพื้นที่ยืนอยู่ในทะเบียนโลกที่แชร์ (`mob_ground_persistence.world_ground()`)
มาผสมกับของในเซสชันก่อน compose แทนที่จะเห็นแค่ของที่เซสชันตัวเองฆ่ามาเอง

จุดต่อสายที่ `runtime.py` (บรรทัด ~5409-5426, ของสายคุณ ผมแตะไม่ได้) ยังไม่ส่ง `world=` —
ยังคงพฤติกรรมเดิมทุกประการ (`world=None` = byte-for-byte เหมือนเดิม พิสูจน์แล้วในใบ #903)
ตัวเนื้อ CORE-REQUEST เต็ม (ก๊อปวางได้ตรง ๆ) อยู่ใน
`src/pirateforce_foundation/mob_scene_recompose.py` ค่าคงที่ `WORLD_GROUND_COMPANION_WIRING`

## ทำไมต้องต่อสาย
ตอบ `COO-DECISION 20260905_1152` ข้อ 2(1) — chief เองวัดค่านี้ไว้ในจดหมายสามฉบับ
(`20260905_1446` R354b · `20260905_1542` · `20260905_1812` R356): เซสชันที่สองในฉากเดียวกัน
เห็น `ground frames = 0` เพราะโค้ดที่ merge ไปแล้ว (`#827`/`#828`) อ่านแค่ `mob_loot_cell`
ของเซสชันตัวเอง ไม่อ่านทะเบียนโลกที่แชร์ — ค้างมาตั้งแต่รอบ `r045nx`/R354 · เป็นเกณฑ์ shared-world
ตัวเดียวที่ `PANYA-DECISION 20260905_1140` ข้อ 3 กำหนดไว้ (relogin/เซสชันที่สองเห็นโลกเดิม)

## ก่อนต่อสาย — ต้นทุนที่ยังไม่มีใครวัด (pf-adversary ชี้รอบนี้)
`mob_ground_persistence.world_ground()` เป็น `threading.RLock()` เดียวทั้งโปรเซส (ไม่แยกฉาก)
และ `seed_cell` สแกน/ก๊อปของพื้นทั้งฉาก (สูงสุด `ROWS_PER_SCENE_CAP` แถว) ทุกครั้งที่เรียก — ต่อสาย
ตามที่ขอแล้วมันจะรันบน **ทุกการตีมอน ของทุกผู้เล่น ทุกฉาก** (ไม่ใช่แค่ตอนเข้าฉาก/relogin ซึ่งเป็น
รูปแบบเดียวที่ `seed_cell` เคยถูกวัดมาก่อน) บวกพิมพ์ console หนึ่งบรรทัดต่อครั้ง (`describe_seeded`)
ไม่มีใครวัดว่าต้นทุนนี้ถูกพอไหมที่อัตราการตี (ต่างจากอัตราเข้าฉาก) — ขอให้วัดก่อนหรือทันทีหลังต่อสาย
ไม่ใช่สมมติว่าถูกพอ

## ใครทำอะไรต่อ
- chief: ต่อสาย 1 import + 1 kwarg ตามเนื้อใน `WORLD_GROUND_COMPANION_WIRING` (คง `companion` local
  + `events.append` count ไว้ตามเดิม — เป็นยามจับมิวแทนต์ที่ปักไว้แล้ว ไม่ใช่สไตล์เฉย ๆ) แล้ววัดต้นทุน
  ต่อการตีก่อนขึ้น main จริง หรือรายงานถ้าวัดไม่ได้ในรอบเดียว
- LANE-A: เปิดใบ GT "ฆ่ามอน 1 ตัว ของตก 2 ชิ้น → เซสชันที่สอง/relogin (เซิร์ฟไม่ปิด) เห็นของ 2 ชิ้น
  ที่เดิม" รอบที่ต่อสายเสร็จ (ตอนนี้ยังไม่เปิด เพราะยังไม่มีอะไรให้ผู้เทสเห็นบนจอ — เปิดตอนนี้จะเป็น
  ใบที่บูตแล้วไม่มีทางผ่าน)

SCOREBOARD: COMING | ของพื้นที่คนอื่นฆ่าทิ้งไว้ในฉากเดียวกันจะไม่หายไปเปล่า ๆ อีกต่อไปเมื่อผู้เล่นอีกคน (หรือ relogin) เข้ามาเห็น — แต่ยังไม่ถึงมือผู้เล่นจนกว่า runtime.py จะต่อสาย | pirate-force-server#903 (18/18 tests · full suite 12029 passed/365 skipped/23464 subtests · preflight PASS · pf-adversary reviewed, 1 blocking finding fixed)
