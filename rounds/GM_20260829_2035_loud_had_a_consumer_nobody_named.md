[LANE-GM · รอบ `npo898` · 2026-08-29T20:35+07:00]

# รอบ `npo898` — "ดัง" ที่ไม่มีใครถามว่าดังถึงใคร กลายเป็นความเงียบที่สุดที่สายนี้ผลิตได้

## ล็อกและชะตาของรอบก่อน (ขั้น A ของ ADDENDUM v2)

- `../pf_bridge/VITAL_REGISTRY_FROM_CLIENT_BINARY_20260817.tsv` **มีจริง** (ยืนยันเป็นขั้นแรกของรอบ)
- ต้นรอบ **ไม่มี** PR `[LANE-GM]` ค้างทั้งสอง repo
  (ที่เห็นและ **ไม่แตะ**: `[LANE-E]` `#277`/`#437` · `[LANE-B]` `#275`/`#434`)
  ⇒ ยึดล็อกด้วย draft ก่อนทำงาน: เซิร์ฟเวอร์ **PR #278** · สะพาน **PR #438**
- **ชะตารอบก่อน `6vhfgh`:** เซิร์ฟเวอร์ `#274` และสะพาน `#433` — วัดด้วย `git merge-base --is-ancestor`
  บน `origin/main` ที่ fetch สดทั้งสอง repo ⇒ **อยู่บน main ทั้งคู่** ไม่มีอะไรต้อง cherry-pick กู้
- ป้ายเวลา (ข้อ C): `TZ=Asia/Bangkok date` = 20:13 ตอนต้นรอบ · heartbeat ล่าสุด 20:02 ⇒ ห่าง **11 นาที** ผ่านเกณฑ์

## กล่องจดหมาย (ขั้น B) — บริโภคหนึ่งใบ และมันคืองานทั้งรอบ

**`20260829_1924_CHIEF-REPLY-GM-037-wired-merged-plus-two-findings-back.md`**
ตอบใบ `CORE-REQUEST-GM-037` ที่สายนี้เปิดเอง · ไม่มีสตับ ⇒ ของสายนี้
อ่าน · ใช้ผล · สตับ · สำเนาไป `consumed/` ครบ

(ใบที่ยังไม่มีสตับใบอื่นในกล่อง — `RE-150-RESULT`, `RE-152-RESULT`, `COO-DECISION` 1941 สองใบ,
`KA3A-*`, `LANE-A-*`, `LANE-B-*` — ตอบใบของสายอื่นทั้งหมด **ไม่แตะ**
· `CORE-REQUEST-GM-038` ของสายนี้ยังไม่มีคำตอบจาก chief ⇒ ยังค้าง ไม่มีอะไรให้บริโภค)

## 🔴 ข้อเท็จจริงที่กลับหัวรอบนี้: failure mode ที่สายนี้ **ขอเอง** ไม่ได้ดัง มันเงียบที่สุด

ใบ `CORE-REQUEST-GM-037` ห้าม `getattr` default: ผลลัพธ์ที่เสียฟิลด์ `cause` **ต้อง raise** ไม่ใช่
พิมพ์คำ placeholder · chief ต่อสายตามนั้นเป๊ะ · pf-adversary (รอบ `nbulzb`) แล้ววัดปลายอีกข้างของ raise
และ chief ส่งกลับมาให้สายนี้ตัดสิน

| วัดได้ | วัดที่ไหน (สายนี้ **วัดซ้ำเอง** ไม่ได้เชื่อใบ) |
|---|---|
| การอ่าน `override_result.cause` อยู่ **ใน** `except (ValueError, OSError, TypeError)` แต่ **นอก** print guard | `runtime.py:5611` และบล็อกรอบ ๆ |
| `AttributeError` เปล่าไม่อยู่ในเน็ตไหนเลย | ทูเพิลเดียวกัน |
| การหลุดคลาย **game listener thread ทั้งตัว** | `current/pf_login_game_server_v141.py` `game_listener`: `except Exception` ตัวเดียวในลูปครอบแค่ decompress/parse (`:7456`) ส่วน `state.dispatch(parsed)` (`:7558`) ไม่มี except อื่นนอกจาก socket |
| โปรเซสยังรับพอร์ต **login** ต่อ | thread ตัวนั้นเป็น daemon และ main thread ไม่ตายไปด้วย |

⇒ อาการที่ผู้เทสได้: ต่อติด แล้วไม่เข้าเกม ตลอดไป · คอนโซลเงียบ · supervisor เห็นโปรเซสแข็งแรง
นั่นคือ **ความเงียบที่สุดที่สายนี้ผลิตได้ โดยสวมคำว่า "ดัง"**

## สิ่งที่ลงจริงรอบนี้ (เขตสายนี้ล้วน · ไม่แตะไฟล์ของ chief แม้บรรทัดเดียว)

| โมดูล | อะไรเปลี่ยน |
|---|---|
| `gm/login_scene_consume.py` | `ConsumeResultMisuse(AttributeError, TypeError)` · `__setattr__`/`__delattr__` โยนคลาสนี้แทน `AttributeError` เปล่า · `__getattr__` ใหม่ครอบสล็อตที่ไม่เคยถูกเซ็ต · print โทเคน `GM_CONSUME_RESULT_LOST_FIELD field=<name> effect=override_refused_login_at_own_row` (มีการ์ด · เฉพาะชื่อใน `__slots__`) · แก้เลขนับ "seven call sites" ที่เท็จ |
| `tests/test_gm_consume_result_lost_field_is_survivable.py` | ใหม่ 14 เทส: สองฐานคือสองมิวแทนต์คนละตัว · ฟิลด์ที่หายตกในเน็ตของ runtime · `hasattr`/`getattr(default)` ยังทำงาน · เส้นทางปกติไม่ถูกดัก · print ไม่สแปม ไม่รั่วค่า และ stdout ที่ตายแล้วไม่เปลี่ยนชนิด error |
| `tests/test_gm_login_scene_consume_cause_wiring_in_runtime.py` | เทส end-to-end ใหม่: ผลลัพธ์ **ของจริง** ที่เสีย `cause` ⇒ `dispatch` **ไม่ raise** · ไม่มีบรรทัด placeholder · แถวเหตุการณ์ `gm_login_scene_override_lookup_failed_ConsumeResultMisuse` · ตัวละครยืนที่แถวของตัวเอง |
| `docs/GM_LANE.md` | ส่วน Round `npo898` · และข้อ 2 ของ chief: ขีดฆ่า "seven" ไม่ใช่แก้เป็น "eight" |

**ทำไมไม่ต้องขอ `runtime.py` เลย:** ฐาน `TypeError` พาความล้มเหลวเข้าเน็ตที่ chief **มีอยู่แล้ว**
ฐาน `AttributeError` ทำให้ `hasattr` / `getattr(x, n, default)` / `copy.deepcopy` (ที่หา `__deepcopy__`
**บนอินสแตนซ์**) ไม่เปลี่ยนพฤติกรรม — คือรีเกรสชัน D8-R เดิมที่จะเปิดใหม่ถ้าเผลอถอดฐานนี้ทิ้ง

**และมันพิมพ์** เพราะถ้าไม่พิมพ์ รอบนี้จะ **เงียบกว่าเดิม**: ของเดิมอย่างน้อยยังมี traceback ลง stderr
ผ่าน thread excepthook ระหว่างทางไปฆ่า thread · แถวเหตุการณ์อย่างเดียวไม่มีใครอ่านตอนตีสาม

**สิ่งที่ไม่เปลี่ยน เพราะมันคือสัญญา ไม่ใช่รัศมีความเสียหาย:** การอ่าน attribute ยังอยู่นอก print guard
· ไม่มี `getattr` default ที่จุดเรียก · ไม่มีการพิมพ์ placeholder `cause=` ให้ฟิลด์ที่หาย

## ข้อ 2 ของ chief: "เจ็ดคำ นับได้แปด"

แก้โดย **ขีดฆ่าเลข ไม่ใช่แก้เป็นแปด** (D6 รอบ `6vhfgh`: แปดจะเท็จในรอบที่เพิ่มกิ่งที่เก้า)
สามจุด: หัวข้อใน `docs/GM_LANE.md` · docstring ของ `tests/test_gm_login_scene_consume_cause.py`
· **เลขที่สามที่ chief ยังไม่เห็น** คือคอมเมนต์ `"at seven call sites"` ใน `gm/login_scene_consume.py`
"เจ็ด" อีกสองแห่งพูดถึงฉบับร่างแรกที่ถูกทิ้งซึ่งมีเจ็ดโทเคนจริง ⇒ **ถูกต้อง ไม่แก้**

## หลักฐาน

- **เขียว(local pytest ทั้งชุด บน main+diff นี้): 5011 passed · 327 skipped · 8860 subtests** (126 วินาที)
- มิวแทนต์ที่ **วัดว่าฆ่าได้จริง** รอบนี้ (ไม่ใช่คำอ้าง):
  1. `ConsumeResultMisuse` เหลือฐานเดียว (`AttributeError`) → 5 เทสแดง รวมทั้ง end-to-end ที่ raise หลุด `dispatch`
  2. ลบ `__getattr__` → 3 เทสแดง
  3. inline การอ่าน `cause` เข้า print guard ของ `runtime.py` → 2 เทสแดง
     (วัดโดยแก้ไฟล์ของ chief **ชั่วคราวในเช็คเอาต์ แล้วคืนค่า** ยืนยันด้วย `git status` ว่าไม่เหลือรอย)
- `git add` ทีละไฟล์ตลอดรอบ (COO-DECISION 20260829_1444 ข้อ 1)
- ชั้นที่สอง (client-observable) **ยังไม่มี** และรอบนี้ไม่แกล้งว่ามี

## pf-adversary

<!-- ADVERSARY -->

## nonclaim (ต้องอ่านคู่กับทุกบรรทัดข้างบน)

ไม่มีอะไรในรอบนี้เห็นได้จากหน้าจอเกม · ไม่มีอะไรให้สถานะ GM กับใคร · ไม่กว้างชุดฉากแม้ฉากเดียว
· เส้นทางที่เทสขับทั้งหมดเป็น **รีเกรสชันในรีโป** ไม่ใช่สถานการณ์จริง (ที่ HEAD `ConsumeResult`
ที่ไม่มี `cause` สร้างไม่ได้: constructor บังคับ + `__slots__`)
· **รอบนี้ไม่ได้ใช้ GM ข้ามขั้นอะไรเลย** เพราะไม่มีใบเทสที่ใช้ GM ในรอบนี้
· GM คือเครื่องมือไปถึงสภาพที่จะเทส ไม่ใช่หลักฐานว่าฟีเจอร์ทำงาน
· ไม่แตะ M2 · ไม่แตะ `CORE-REQUEST-GM-038` ซึ่งยังค้างรอ chief

## ผู้เทสจะทำอะไรได้ที่เมื่อวานทำไม่ได้

**คนเฝ้าคอนโซล / คนดูแลเซิร์ฟเวอร์:** วันที่มีรีเกรสชันทำให้ผลลัพธ์ consume เสียฟิลด์ไป
เมื่อวานได้ **พอร์ตเกมตายถาวรใต้โปรเซสที่ดูมีชีวิต** (พอร์ต login ยังรับ) คอนโซลไม่มีอะไร
supervisor ไม่รีสตาร์ท ต้องเดาเองว่าทำไมไคลเอนต์ต่อติดแล้วไม่เข้าเกม
วันนี้ได้ **บรรทัดชื่อจริงบนคอนโซล** `GM_CONSUME_RESULT_LOST_FIELD field=cause` + แถวเหตุการณ์
`gm_login_scene_override_lookup_failed_ConsumeResultMisuse` ที่ grep ได้ และ **เซิร์ฟเวอร์ยังรับคนอื่นต่อ**
— ล็อกอินนั้นเสียแค่ปลายทาง GM ที่วางไว้ ตัวละครยืนที่แถวของตัวเอง

🔴 **ผู้เทสหน้าจอเกม: ไม่ได้อะไรใหม่รอบนี้** และรอบนี้จะไม่แกล้งบอกว่าได้
