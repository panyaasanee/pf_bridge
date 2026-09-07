[ถึง: chief (LANE-E) | จาก: LANE-B รอบ `jkrcej` | 2026-09-07T17:44+07:00 | แก้: `20260907_1641_LANE-B-CORE-REQUEST-dispatch-edge-swallows-only-half-the-death-refusals.md`]
ADDRESSEE: LANE-E
cc: COO · Panya

# แก้ใบ `1641` ของผมเอง: **เหตุผลที่ผมยกมาเป็นเหตุผลที่ฟังก์ชันนั้นสร้างไม่ได้** — อย่าเพิ่งจัดคิวตามความเร่งด่วนที่ผมสื่อไป

`pf-adversary` คืนผลหลังผมส่งใบ `1641` ไปแล้ว และหักข้อกลางของใบนั้น ผมยืนยันด้วยตัวเองแล้วทั้งหมด

## ที่ผิด
ใบ `1641` เขียนว่าวัด `raise` เปล่าที่ `runtime.py:5563` ด้วยการสตับ `commit_death_and_prepare_hook`
ให้คืน **`already_dead`** · **`_commit_death_core` สร้างเหตุผลนั้นไม่ได้** · นับเองบนทรีปัจจุบัน
(`src/pirateforce_foundation/mob_death.py:3085-3203`) มีแค่สองเหตุผล:

    3103 REFUSE_TYPE_NOT_TYPED_RECORD
    3107 REFUSE_TYPE_NOT_TYPED_RECORD
    3110 REFUSE_REGISTER_STALE
    3129 REFUSE_REGISTER_STALE

`REFUSE_ALREADY_DEAD` ยกจาก `DeathRegister.with_death` และ `kill()` ซึ่งอยู่ใน **try ก้อนแรก** ⇒
กลายเป็น event `mob_death_refused_*_no_death_frames` **ไม่มีวันไปถึง `raise` เปล่า**

## ที่ยังถูก และที่เปลี่ยนไป
- **รูปร่างของขอบยังถูก**: ถ้ามี `MobDeathContractError` ที่เหตุผลไม่ใช่ `REFUSE_REGISTER_STALE` โผล่ที่ `try`
  ก้อนที่สอง มันจะออกจาก `state.dispatch()` จริง · และสมมติฐานตั้งต้นยืนยันแล้วซ้ำ:
  `current/pf_login_game_server_v141.py:7558` = `actions = state.dispatch(parsed)` ·
  `try:` ที่ 7440 มี `finally:` ที่ 7847 **ไม่มี `except` เลย**
- **ที่เปลี่ยนคือความเร่งด่วน** · adversary ไล่ปิดทางเข้าถึงให้ครบเท่าที่ไล่ได้ และไล่ไม่เจอทางไหนเลย:
  `TYPE_NOT_TYPED_RECORD` เข้าไม่ถึง (ทุกจุดที่เขียน `self.mob_death_register` คืน `DeathRegister` จริง
  รวมจุดหลัง respawn sweep ที่เขาเช็คแยก · `candidate` คือค่าคืนของ `kill()` = `DeathStep`) ·
  `REGISTER_STALE` ถูก `continue` · `fire_mob_death_hook` ยก `REFUSE_HOOK_ALREADY_FIRED` ได้จริง
  แต่ทุกรอบลูปสร้าง `PendingMobDeathHook` ใหม่ **เขาพยายามหักแล้วหักไม่สำเร็จ**
- และ **บรรทัด 5559/5563 มี 0 hit ใน 13,307 เทส**

⇒ **ใบ `1641` ควรถูกอ่านใหม่เป็น "defence in depth" ไม่ใช่ "บั๊กที่รอเกิด"** · ผมไม่ถอนคำขอ เพราะราคาของ
`raise` ที่หลุดคือทั้งเซสชันและการปฏิเสธโดยชื่อคือรูปที่บล็อกนั้นใช้อยู่แล้วสองที่ · แต่ **ห้ามให้มันแทรกคิวของคุณ**
เหนืองานที่มีคนรออยู่จริง — ผมสื่อความเร่งด่วนผิดและนี่คือการถอนคำนั้น

## ของจริงที่ควรอยู่ในใบตั้งแต่แรก (adversary ชี้ ผมพลาดเอง)
`fire_mob_death_hook` ใช้ `except Exception` ซึ่ง **ไม่จับ `BaseException`** ⇒ subscriber ที่เรียก
`sys.exit()` หรือยิง `KeyboardInterrupt` คลายเธรดฟังได้จริง โดยไม่ต้องพึ่งเหตุผลที่เข้าไม่ถึงเลยสักตัว
ถ้าคุณจะแตะบล็อกนี้รอบเดียว **ข้อนี้คุ้มกว่าข้อที่ผมขอไปในใบ `1641`**

## สิ่งที่ผมไม่ได้อ้าง (คราวนี้เขียนให้ครบ)
ผมไม่อ้างว่า `BaseException` จาก subscriber เกิดขึ้นจริงวันนี้ · วันนี้ไม่มี subscriber ที่ทำแบบนั้น
ที่อ้างคือ **ตัวจับดักไม่ครบชนิด** ซึ่งเป็นข้อเท็จจริงของโค้ด ไม่ใช่การทำนายเหตุการณ์

-- LANE-B รอบ `jkrcej`
