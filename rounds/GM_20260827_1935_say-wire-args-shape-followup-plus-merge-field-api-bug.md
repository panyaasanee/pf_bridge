# รอบ a54s3e -- LANE-GM: ปิดช่อง args-shape ที่ค้างของ `gm/say_wire.py` + พบบั๊ก API สำคัญข้ามสาย (2026-08-27 19:3x +07:00)

## บริบท

รอบ nzt815 (warp-executor args-shape follow-up) ปิดช่องของ `gm/warp_executor.py` แล้วบันทึกไว้ใน
`docs/GM_LANE.md` ว่า `gm/say_wire.py` มีช่องเดียวกันสองข้ออยู่ (catch แคบเกินไป + ไม่มี guard กัน
`str`/`bytes` scalar) แต่ไม่ได้แก้เพราะไม่ได้แตะไฟล์นั้นในรอบนั้น -- ติดป้ายไว้เป็นค้างสำหรับรอบถัดไป
รอบนี้ทำตามนั้น

## ต้นรอบ: ตรวจล็อกตาม ADDENDUM v6.2 ข้อ A

ไม่มี PR `[LANE-GM]` เปิดค้างทั้งสอง repo ตอนต้นรอบ -- เปิด draft PR ยึดล็อกตามขั้นตอน
(`pf_bridge#198`, `pirate-force-server#117`)

ตรวจ PR ปิดล่าสุดของสายนี้ทั้งสอง repo ด้วย **`pull_request_read` (method `get`)** ไม่ใช่
`list_pull_requests`: `pf_bridge#192` และ `pirate-force-server#114` ทั้งคู่ `merged: true` -- งานรอบก่อนอยู่บน
main แล้ว ไปต่อได้ ไม่ต้อง cherry-pick กู้อะไร

**หมายเหตุสำคัญ**: เหตุผลที่ระบุว่าใช้ tool ไหนตรวจ ดูหัวข้อ "พบบั๊ก" ด้านล่าง -- ถ้าใช้ `list_pull_requests`
แทน จะได้คำตอบผิด (ดูรายละเอียด)

## ทำอะไรไปบ้าง (pirate-force-server, `pirate-force-server#117`) -- สองรอบย่อยในรอบเดียว

**ผ่านที่ 1**: `gm/say_wire.py`'s `len(args)`/`args[0]` guard เปลี่ยน catch จาก
`TypeError`/`(TypeError, KeyError, IndexError)` เจาะจง เป็น `except Exception` กว้าง ๆ ทั้งสองจุด
และเพิ่ม `isinstance(args, (str, bytes))` ปฏิเสธตั้งแต่ต้น -- แก้แบบเดียวกับที่ `warp_executor.py`
ทำในรอบก่อน (blacklist pattern เดิม) commit แล้ว push เข้า PR

**pf-adversary ตรวจ (รอบที่ 1)** เจอช่องจริง ไม่ใช่แค่ทฤษฎี: dict ที่ key เป็นเลขจำนวนเต็ม
(เช่น `{0: "hello"}`) คือ "mapping" ตามที่ `docs/GM_LANE.md` เรียกไว้เป็นหนึ่งในสามรูปทรงต้องห้ามอยู่แล้ว
แต่ `len(d)` และ `d[0]` ผ่านปกติทั้งคู่ ไม่โยน exception เลย -- ทั้ง guard `str`/`bytes` และ `except Exception`
ทั้งสองจุดจึงไม่ทำงาน สร้างเฟรมจริงออกมาจาก dict ที่ไม่ใช่รูปทรงที่ตั้งใจรับ ช่องเดียวกันนี้มีอยู่ใน
`warp_executor.py` เองด้วย (`{0: 1, 1: 2, 2: 3}`) พร้อมพบว่า docstring ที่เขียนไว้ระบุที่มาของการแก้ผิด
(อ้างว่า "รอบ warp-executor follow-up" เป็นคนแก้ `say_wire.py` ทั้งที่ `docs/GM_LANE.md` ของรอบนั้นเองบันทึก
ชัดว่าไม่ได้แตะไฟล์นี้)

**ผ่านที่ 2 (แก้จริง)**: เปลี่ยนจาก blacklist เป็น allowlist -- `GmCommand.args` ประกาศชนิดเป็น
`tuple[str, ...]` ใน `gm/commands.py` อยู่แล้ว (รูปทรงที่ถูกต้องมีแบบเดียว) ทั้งสองโมดูลจึงตรวจ
`isinstance(args, tuple)` ตรง ๆ ก่อนแตะ `len()`/index ใด ๆ เลย ปิดช่องทั้งหมดในทีเดียว (dict ทุก key type,
`str`/`bytes`, `bytearray`, `memoryview`, `list`, object แปลก ๆ) แทนที่จะไล่แก้ทีละรูปทรงที่ adversary เจอ
แก้ทั้ง `say_wire.py` และ `warp_executor.py` พร้อมกัน (อยู่ในเขตเขียนของสายนี้ทั้งคู่) แก้ docstring ที่ระบุที่มาผิดด้วย

**pf-adversary ตรวจซ้ำ (รอบที่ 2)** เจตนาหาว่า allowlist เองพังไหม -- ตรวจ subclass ของ `tuple`/namedtuple
ที่โกหกพฤติกรรมตัวเอง, ตรวจว่า `len()`/index ที่ไม่มี try/except ครอบแล้วจะโยนอะไรหลุดออกมาไหมสำหรับ tuple
จริง (รวม tuple ว่าง), ตรวจ docstring ทั้งสองไฟล์ให้ตรงกับ git history จริง -- ไม่พบช่องเพิ่มเติม

เทสใหม่ต่อยอด `SayWireArgsShapeFollowUpTests`/`WarpExecutorArgsShapeTests`: dict คีย์ตัวเลข, `list`,
`bytearray` (คู่กันทั้งสองไฟล์) และปรับ `docs/GM_LANE.md` ให้เล่าประวัติทั้งสองผ่านจริง ไม่ใช่แค่ผ่านแรก

ไม่มีการเปลี่ยนพฤติกรรมบน happy path -- `args` ที่เป็น tuple จริงตามจำนวน/ชนิดที่ถูกต้องให้เฟรมเหมือนเดิมทุกไบต์
`say`/`warp` ยังไม่ทำงานจริงหลังรอบนี้: โมดูลเหล่านี้คืนแค่ bytes ให้ caller ไม่ส่งอะไรเอง และไม่มีบัญชีใดได้อะไร
ที่ไม่เคยได้มาก่อน (`CORE-REQUEST-011`/`CORE-REQUEST-012` ยังไม่ต่อสาย `runtime.py`)

## ค้นแล้ว: ไม่เจอ (ไม่เกี่ยวข้องรอบนี้)

รอบนี้ไม่พึ่งข้อมูลจาก client เลย -- แก้บั๊กเชิงตรรกะล้วนบนโค้ดที่มี wire layout พิสูจน์แล้ว กฎ "ค้นก่อนถอด"
ไม่มีผลกับรอบนี้

## เทส

`tests/test_gm_say_wire.py`: 21/21 · `tests/test_gm_warp_executor.py`: 20/20 · `test_gm_*.py` ทั้งชุด: 185/185
(179 เดิม + 6 ใหม่ นับผ่านที่ 2 เท่านั้น เพราะเทส 4 ข้อของผ่านที่ 1 ยังอยู่ครบ ไม่ถูกลบ)

## พบบั๊ก: `list_pull_requests` (GitHub MCP tool) รายงาน `merged` ผิดเสมอ -- กระทบ ADDENDUM v6.2 ข้อ A ทุกสาย

ต้นรอบนี้ตรวจ PR ปิดล่าสุดของทุกสาย (ไม่ใช่แค่ของตัวเอง) ด้วย `list_pull_requests(state=closed)` ก่อน
เพื่อความเร็ว -- ผลลัพธ์ทุกแถวในทั้งสอง repo (`pf_bridge` 20 รายการ, `pirate-force-server` 20 รายการ ย้อนหลัง)
รายงาน `"merged": false` **หมดทุกใบ** รวมถึงใบที่มี commit log ยืนยันชัดเจนว่า merge จริงแล้ว
(`git log` เห็น `Merge pull request #196 ...` เป็นต้น)

ตรวจซ้ำด้วย `pull_request_read(method="get")` กับสองใบเดียวกัน (`pf_bridge#192`, `pirate-force-server#114`)
-> ได้ `"merged": true` ถูกต้อง พร้อม `merged_by`/`merged_at` ครบ

สรุป: **`list_pull_requests` ไม่ใช่แหล่งความจริงสำหรับฟิลด์ `merged`** (น่าจะเป็นข้อจำกัดของ GitHub REST list
endpoint เองที่ไม่คืนฟิลด์นี้ครบ ไม่ใช่บั๊กของโค้ดสายนี้) -- ต้องใช้ `pull_request_read` แบบ `get` ทีละใบเท่านั้น

**นี่กระทบ ADDENDUM v6.2 ข้อ A โดยตรง**: ข้อ A สั่งให้ทุกสาย (A/B/E/GM) ตรวจ "PR ล่าสุดของสายคุณ ... state=closed
... merged=true/false" ต้นทุกรอบ ถ้าสายไหนเรียก `list_pull_requests` ตามสัญชาตญาณ (เร็วกว่า, list หลายใบทีเดียว)
จะเห็น `merged=false` เสมอ **ทุกรอบ ทุกสาย ตลอดไป** แม้ PR จะ merge จริงแล้วก็ตาม แล้วจะตีความว่า "งานรอบก่อนหายจาก
main" ทั้งที่ไม่จริง -> เริ่ม cherry-pick commit ที่ merge อยู่บน main แล้วซ้ำเข้าไปในรอบใหม่ -- สร้าง duplicate
commit / conflict / ความสับสนข้ามทุกสายพร้อมกัน ตรงข้ามกับเป้าหมายที่ v6.2 ตั้งใจแก้ (self-lock) เลย

รอบนี้เลี่ยงได้เพราะตรวจด้วย `get` ตั้งแต่ต้น (ดูหัวข้อ "ต้นรอบ" ด้านบน) แต่ไม่รู้ว่าสาย A/B/E รอบถัดไปจะเรียก
tool ไหน -- นี่ไม่ใช่เรื่องที่ GM lane แก้ได้เอง (ข้อความของ ADDENDUM เป็นของ chief/COO ไม่ใช่เขตเขียนของสายนี้)
เขียนใบ ASK-COO แยกต่างหาก

nonclaim: การพบนี้เป็นเรื่อง tooling/process ล้วน ไม่เกี่ยวกับ GM gameplay หรือ wire ใด ๆ ไม่อ้างว่าฟีเจอร์
GM ทำงานอะไรเพิ่มขึ้น

ผู้เทสจะทำอะไรได้ที่เมื่อวานทำไม่ได้: ไม่มี -- รอบนี้เป็นการแก้ความทนทานของโค้ดภายในเขตเขียนของสายเอง
(ไม่มีจุดเรียกจริงจากไคลเอนต์) บวกการพบบั๊ก tooling ที่ไม่ใช่ gameplay

## แก้ไขเพิ่ม (ผ่านที่ 3 ของ pf-adversary): คำยืนยันของผ่านที่ 2 ผิด

หลังบันทึกด้านบนแล้ว ส่ง `pf-adversary` ตรวจ allowlist (`isinstance(args, tuple)`) อีกรอบเพื่อยืนยันก่อนปิดรอบ --
**ผลผ่านที่ 2 ที่เขียนไว้ว่า "ไม่พบช่องเพิ่มเติม" นั้นผิด** ผ่านที่ 3 พิสูจน์สดได้ภายในไม่ถึงนาที: tuple subclass
ที่ override `__len__`/`__getitem__` ให้โยน exception อื่น (เช่น `RuntimeError`, `KeyError`) ผ่าน
`isinstance(args, tuple)` ได้ปกติ และ `GmCommand` (frozen dataclass เปล่า ไม่มี validation ใน `__post_init__`)
ไม่มีอะไรกันไม่ให้ caller สร้างแบบนี้ได้ -- ตรงกับ threat model "ไม่ว่าจะมาจากไหน" ที่ docstring ประกาศไว้เอง

แก้จริง: เปลี่ยนจาก `isinstance(args, tuple)` เป็น `type(args) is tuple` -- ปฏิเสธ subclass ทุกชนิด
tuple ตัวจริง (ไม่ใช่ subclass) ไม่มีทางโยน exception จาก `len()`/index ได้เลย จึงไม่มี dunder ให้โกหกอีกต่อไป
เพิ่มเทส 2 ข้อต่อไฟล์ (lying `__len__`, lying `__getitem__`) `docs/GM_LANE.md` บันทึกการแก้คำยืนยันผิดของผ่านที่ 2
ไว้ตรง ๆ ไม่ลบทิ้ง ตามกติกา "ห้ามลบประวัติเดิม"

เทสรอบสุดท้าย: `tests/test_gm_say_wire.py` 23/23 · `tests/test_gm_warp_executor.py` 22/22 · `test_gm_*.py` 189/189
