[ถึง: chief (LANE-E) | จาก: LANE-B รอบ `jkrcej` | 2026-09-07T16:41+07:00]
ADDRESSEE: LANE-E
cc: COO · Panya

# ขอบรรทัดเดียวที่ขอบ dispatch: `raise` ที่เหลืออยู่ในบล็อกฆ่ามอน **คลายสแต็กออกจาก `state.dispatch()` จริง** (วัดแล้ว)

## บล็อกที่พูดถึงมีจริง ยกมาจากทรีปัจจุบัน

`src/pirateforce_foundation/runtime.py` บรรทัด **5558-5563** ใน `_dispatch_mob_combat`
(กิ่งที่มอนในโรสเตอร์ทุกตัวตายผ่าน · หลังคำสั่ง `commit_death_and_prepare_hook`):

    except mob_death.MobDeathContractError as error:
        if error.reason == mob_death.REFUSE_REGISTER_STALE:
            # Same per-session caveat as the ledger retry
            # above: unreachable today, kept for the contract.
            continue
        raise

🔴 **โทเคนว่าบล็อกนี้มีจริงบนทรีที่วัด** (`origin/main` = `fade2d5` · กิ่งรอบนี้ `cef9875`
ซึ่งไม่แตะ `runtime.py` แม้แต่ไบต์เดียว) — คำสั่งเดียว รันซ้ำได้:

    $ grep -n "REFUSE_REGISTER_STALE:" -A 4 src/pirateforce_foundation/runtime.py
    5559:                            if error.reason == mob_death.REFUSE_REGISTER_STALE:
    5560-                                # Same per-session caveat as the ledger retry
    5561-                                # above: unreachable today, kept for the contract.
    5562-                                continue
    5563-                            raise

`raise` เปล่าบรรทัดสุดท้ายนั้นคือสิ่งที่ขอ

## วัดอะไร และวัดยังไง (ไม่ใช่การอ่านโค้ด)

รอบ `jkrcej` ขับ dispatch จริงบนบูตไร้แฟล็กในฉาก `Bg0002` (ฮาร์เนสเดียวกับ
`tests/test_mob_combat_dispatch_bg0002_kill.py`) แล้ววัดสองทางในบล็อกเดียวกัน:

1. **คำปฏิเสธ `target_outside_the_sanctioned_scope`** (มอนที่ไม่มีใบไหนอนุญาตให้ฆ่า)
   ⇒ **ไม่คลาย** · dispatch คืนค่าปกติ · ได้ `MOB_COMBAT_ANNOUNCE` ไม่มี death/loot ·
   session จด `mob_death_refused_target_outside_the_sanctioned_scope_no_death_frames`
   ⇒ ผู้เล่นเห็น "ตีแล้วไม่ตาย" ตามที่ COO สั่งไว้ · ปักด้วย
   `tests/test_mob_death_refusal_does_not_unwind_dispatch.py` แล้วในรอบนี้

2. **คำปฏิเสธจากขั้น commit ที่เหตุผลไม่ใช่ `REFUSE_REGISTER_STALE`**
   (บังคับด้วยการสตับ `commit_death_and_prepare_hook` ให้คืน `already_dead`)
   ⇒ 🔴 **คลายออกจาก `state.dispatch()` จริง**:

       COMMIT_PATH_UNWOUND_DISPATCH yes exc=MobDeathContractError reason=already_dead

   และ `src/pirateforce_foundation/gm/login_scene_consume.py:243` เขียนไว้เองว่า
   `current/pf_login_game_server_v141.py` **ไม่มี except ครอบ `state.dispatch`**
   ⇒ ปลายทางของ `raise` นี้คือเธรดฟังตาย = **โลกเงียบ** ไม่ใช่ "มอนไม่ตาย"

### วัดซ้ำยังไง (ผมลบสคริปต์ชั่วคราวทิ้งแล้ว ไม่ได้ commit — นี่คือสูตร ไม่ใช่การอ้าง)
บนฮาร์เนสของ `tests/test_mob_death_refusal_does_not_unwind_dispatch.py` (รอบนี้เพิ่ม) เปลี่ยนแค่บรรทัดเดียว:
แทนที่จะถอดใบอนุญาตออกจาก `WIDENING_RULINGS` ให้ patch `mob_death.commit_death_and_prepare_hook`
เป็นฟังก์ชันที่ `raise mob_death.MobDeathContractError(mob_death.REFUSE_ALREADY_DEAD, "...")`
แล้วขับ `_action_vital_pc(target)` ใบเดิม · ข้อยกเว้นจะออกจาก `state.dispatch()` ทันที
(ระวัง: `MobDeathContractError.__init__` ปฏิเสธเหตุผลที่ไม่ได้ลงทะเบียนด้วย `AssertionError`
ต้องใช้ค่าคงที่ `REFUSE_*` จริง ไม่ใช่สตริงมั่ว — ผมพลาดข้อนี้ครั้งแรกและมันทำให้ผลอ่านผิดไปหนึ่งรอบ)

## สิ่งที่ผม **ไม่ได้** อ้าง

- **ไม่อ้างว่าวันนี้มีเส้นทางจริงที่ทำให้ `commit_death_and_prepare_hook` คืนเหตุผลนั้น** ·
  คอมเมนต์ในไฟล์ของคุณเขียนว่า "unreachable today" และผมยังยืนยันไม่ได้ทั้งสองทาง ·
  ที่ผมวัดคือ **รูปร่างของขอบ** ไม่ใช่ความถี่ของมัน — ถ้าเหตุผลนั้นเกิดขึ้นวันไหน ราคาคือทั้ง session
- ไม่อ้างว่าประตูอื่นที่ไปถึงการฆ่า (`diag_multi_object_wiring.death_dispatch`,
  `mob_respawn`, `mob_death_persistence`, `scene_door_walk`) ปลอดภัยหรือไม่ปลอดภัย — รอบนี้ขับประตูเดียว

## ที่ขอ (บรรทัดเดียว เขตคุณ ผมไม่แตะ `runtime.py`)

เปลี่ยน `raise` เปล่าให้เป็นการปฏิเสธโดยชื่อแบบเดียวกับพี่น้องของมันในบล็อกเดียวกัน:

    self.events.append(
        f"mob_death_commit_refused_{error.reason}_no_death_frames"
    )
    break

เหตุผลว่าทำไมนี่คือรูปที่ถูก ไม่ใช่การกลบข้อผิดพลาด:
- บล็อกเดียวกันนี้ **มีสองที่แล้ว** ที่ปฏิเสธโดยชื่อแทนที่จะโยนต่อ
  (`diag_multi_object_commit_refused_*` และ `mob_death_refused_*_no_death_frames`)
  ⇒ ที่ขอคือความสม่ำเสมอ ไม่ใช่นโยบายใหม่
- เหตุผลไม่หาย มันขึ้น event list ที่คนอ่านคอนโซลเห็น
- ต้นทุนของการเดาผิดไม่เท่ากันสองฝั่ง: กลืนแล้วเห็น "มอนไม่ตาย" = บั๊กที่รายงานได้ ·
  ไม่กลืนแล้วเธรดตาย = ผู้เล่นรายงานว่า "เกมค้าง" ซึ่งชี้กลับมาที่นี่ไม่ได้เลย

ถ้าคุณเห็นว่าเหตุผลบางตัวควรดังกว่านั้นจริง ๆ ผมรับได้ — ขอแค่ว่า **อย่าให้มันออกจาก `dispatch`**
(log ดัง · ปิด session อย่างมีระเบียบ · อะไรก็ได้ที่ไม่ใช่ปล่อยให้เธรดฟังตายเงียบ)

## เทสที่ปักครึ่งที่ตอบแล้ว

`tests/test_mob_death_refusal_does_not_unwind_dispatch.py` (รอบนี้ · เขต B)
ลบ `except mob_death.MobDeathContractError` ที่จุดฆ่าโรสเตอร์ออก ⇒ **4 ใน 5 ใบแดง** ·
ใบคุม (การฆ่าปกติยังตายจริงและได้ของตก) ยังเขียว ⇒ ไฟล์นี้ผ่านด้วย dispatcher ที่เลิกฆ่าอะไรเลยไม่ได้
ครึ่งที่ยังไม่ปักคือครึ่งของคุณ และผมไม่เขียนเทสปักไฟล์ที่ผมไม่ได้เป็นเจ้าของ

-- LANE-B รอบ `jkrcej`
