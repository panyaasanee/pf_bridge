[ถึง: chief · cc: COO, เจ้าของ | จาก: LANE-A (สาย A · WORLD) รอบ `qoj8ei` · 2026-08-31T11:36+07:00]
[ตอบใบ: `CLIENT_RE_QUEUE.md` RE-167 CENSUS-FRAME-INTERMITTENT-ABORT-001]

# RE-167 RESULT (wire/DB layer only) -- ไม่พบ buffer/timeout ฝั่งเซิร์ฟเวอร์ที่อธิบาย 10053 ได้ ปิดชั้นนี้เป็น bounded-negative พร้อมข้อเสนอ

## สถานะ

**ชั้น wire/DB: ตอบครบ ข้อ 1-4, ผลลบ (bounded-negative)** -- ไม่มีจุดในซอร์สที่ commit แล้วอธิบาย
`ConnectionAbortedError 10053` แบบเจาะจงได้ **ชั้น client-observable: ยังไม่เปิด GT ใหม่** (ยังไม่มีโค้ดแก้ให้เทส)

## ข้อ 1 -- ฝั่งเซิร์ฟเวอร์มี buffer/timeout ที่ทำให้ send abort เป็นบางครั้งไหม

ไม่พบ จุดส่งจริงมีจุดเดียวคือ `current/pf_login_game_server_v141.py:7746-7755`:
- `c.settimeout(600)` ตั้งไว้ที่ `:7406` (connection-level, 10 นาที) -- กว้างเกินกว่าจะอธิบาย abort บนเพย์โหลด
  ~20KB เดียว
- แต่ละ action ส่งด้วย synchronous `c.sendall(out_frame)` ใต้ `send_lock` (`:7753-7755`) ไม่มี chunking,
  ไม่มี retry, ไม่มี custom timeout ต่อ-send
- เมื่อ `sendall()` โยน `(ConnectionResetError, ConnectionAbortedError, BrokenPipeError, OSError)`
  โค้ด**แค่พิมพ์ `[G!] send failed` แล้ว `break`** (`:7754-7757`) -- ออกจาก loop ทันที ไม่ retry ไม่ raise ต่อ
- ผลข้างเคียงที่ยังไม่มีใครพูดถึงมาก่อน: `break` (ไม่ใช่ `continue`) แปลว่าถ้า `WORLD_CENSUS_INITIAL` เอง
  abort, `WORLD_CENSUS_REAPPLY` (คิวถัดไปในลิสต์เดียวกัน) **ก็ไม่ถูกส่งด้วย** -- ตรงกับหลักฐานที่ผู้เทสรายงาน
  (ครั้งที่ขาด: ขาดตั้งแต่ INITIAL, ครั้งถัดมา: ผ่านทั้ง INITIAL และ REAPPLY -- ไม่มีเคสที่ INITIAL ผ่านแต่
  REAPPLY ขาด ซึ่งตรงกับ break-not-continue ทุกจุด)

**สรุปข้อ 1**: ไม่มี buffer/timeout ฝั่งเซิร์ฟเวอร์ที่ยาวหรือแคบผิดปกติ การ abort ไม่ใช่ผลจาก server-side
schedule -- `settimeout(600)` กว้างเกินกว่าจะเป็นสาเหตุ และไม่มี logic อื่นที่หน่วง/บล็อกก่อน `sendall()`

## ข้อ 2 -- ฝั่งไคลเอนต์อ่านเฟรมเป็นก้อนเดียวหรือแบ่งอ่าน

**Bounded-negative ตามที่ใบสั่งงานอนุญาต**: ไม่มี client image/disassembly ใหม่ในรอบนี้ ตอบจากฝั่งเซิร์ฟเวอร์
ไม่ได้ -- เซิร์ฟเวอร์ไม่รู้ว่าไคลเอนต์อ่านเฟรมยังไง มันแค่ `sendall()` ก้อนเดียว TCP เป็น byte stream ไม่มี
framing ฝั่ง socket ที่ระดับนี้ ต้องมีคนอ่าน client disassembly ถึงจะตอบได้จริง

## ข้อ 3 -- ควร chunk เฟรมสำมะโนใหญ่ไหม, threshold เท่าไร

**เสนอได้จาก static analysis แต่ implement ไม่ได้ในเขตของสายนี้**: ถ้าจะ chunk ต้องแก้ที่จุดเดียว
(`current/pf_login_game_server_v141.py:7753`, `c.sendall(out_frame)`) -- ไฟล์นี้คือ "V141 legacy
characterization source" ที่ AGENTS.md (บรรทัด 130) และเกตคอมมิตบังคับว่าต้อง**สะอาด (byte-identical) ทุกรอบ**
(`git diff --stat` ว่างเป็นเงื่อนไขผ่านเกต) -- ไม่ใช่แค่ไฟล์ของ chief แบบ `runtime.py`/`app.py` แต่เป็นไฟล์ที่
ทั้งโปรเจกต์ตกลงกันไว้ว่าห้ามแก้เลยไม่ว่าใคร **นี่คือประเด็นโครงสร้างที่ต้องส่งต่อ ไม่ใช่แค่ CORE-REQUEST ปกติ**
(ดูหัวข้อ CORE-REQUEST ด้านล่าง) ถ้าจะ chunk โดยไม่แตะไฟล์แช่แข็ง ทางเดียวที่เห็นคือหน่วง/แบ่ง payload
**ก่อน**ถึง v141 (เช่น ให้ `runtime.py`'s census_actions ส่งเป็นหลายเฟรมเล็กแทนเฟรมใหญ่เฟรมเดียว) -- แต่นั่น
เปลี่ยน wire ที่ `world_population.py` ประกอบ ซึ่งกระทบ V141 self-test's regression ceiling ด้วย (AGENTS.md
"Regression ceilings to preserve") ไม่ใช่การตัดสินใจที่ทำเงียบ ๆ ได้จากรอบเดียว

## ข้อ 4 -- ผลลบเป็นคำตอบได้ไหม

**ใช่ นี่คือคำตอบของรอบนี้**: ไม่มี server-side race/buffer/timeout ที่ static analysis หาเจอ ลักษณะอาการ
(เฟรมขนาดเท่ากัน บางครั้งผ่านบางครั้งขาด) สอดคล้องกับสาเหตุนอกซอร์สที่ commit แล้ว (เช่น ฝั่งไคลเอนต์/OS/
เครือข่าย/แอนตี้ไวรัสบน Windows ที่รีเซ็ตการเชื่อมต่อ) มากกว่าบั๊กที่กำหนดได้ในโค้ดที่มีอยู่วันนี้

## ข้อห้ามที่ยืนยันว่าไม่ได้ทำ

ไม่ได้ลดจำนวน actor ไม่ได้แตะ `runtime.py`/`app.py`/`current/pf_login_game_server_v141.py`
(`git diff --stat` ว่างทั้งสามไฟล์ ยืนยันด้วย SHA-256 ด้านล่าง) ไม่ได้อ้างว่าอ่าน log ครั้งเดียวแล้วสรุปสาเหตุ
แท้จริง (G1) -- อ่านซอร์สโดยตรง ไม่ใช่ log

## CORE-REQUEST (ถึง chief, ไม่ใช่คำขอแก้ตรง ๆ)

ไม่มี "ขอแก้บรรทัดนี้" เพราะไม่มีบรรทัดในเขตของสายนี้ที่ควรแก้ -- **มีคำถามเชิงโครงสร้างที่ต้องให้ chief/COO
ตัดสิน**: ถ้าอนาคตต้องการ chunking จริง จะทำได้ก็ต่อเมื่อ (ก) แก้ v141 frozen source ซึ่งขัดกับกติกา "ต้องสะอาด"
ที่มีอยู่ก่อนงานนี้ หรือ (ข) เปลี่ยนรูปเฟรมที่ `world_population.py` ประกอบให้เล็กลงเป็นหลายก้อน ซึ่งอาจกระทบ
regression ceiling ที่ AGENTS.md ปักไว้ ทั้งสองทางไม่ใช่การตัดสินใจของรอบเดียว ไม่ใช่ของ LANE-A คนเดียว --
ส่งเป็นคำถามเชิงนโยบาย ไม่ใช่โค้ด ยกให้รอบถัดไปหรือ COO ตัดสินว่าจะเปิดทางไหน

## ยังไม่ได้พิสูจน์

ชั้น client-observable ทั้งหมด -- ยังไม่มี fix ให้เทส จึงยังไม่เปิด GT ใหม่ (ตาม pass criteria ของใบนี้: สาย A
เปิดใบเมื่อมีของให้เทส)

## input SHA-256 (ยืนยันไฟล์แช่แข็งไม่ถูกแตะ)

- `current/pf_login_game_server_v141.py`: `2eb05ed2fdbdd5ee3d91f7fbb8c1d16a4c7a02a843bc97169b16a389e4ea4c22`
- `src/pirateforce_foundation/runtime.py`: `a4719484830f300ce11e73bd989c9db9a69e55666aea7fb27dfdcdc84d7d8eae`

## links

`notes_to_chief/20260831_1036_GT106R2-RESULT-PASS-client-renders-the-destination-scene-mid-session-plus-two-new-findings.md`

-- LANE-A (WORLD) รอบ `qoj8ei`
