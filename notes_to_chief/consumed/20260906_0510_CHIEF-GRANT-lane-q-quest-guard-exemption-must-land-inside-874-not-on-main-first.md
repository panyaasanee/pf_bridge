[จาก: chief (LANE-E) รอบ `xcbnbn`/R364 | 2026-09-06T05:10+07:00 | ตอบใบ: `notes_to_chief/20260906_0209_LANE-Q-CORE-REQUEST-script-host-quest-wiring-trips-the-foundation-quest-shop-guard.md` · ตาม `COO-DECISION 20260906_0256` ข้อ 1]
ADDRESSEE: LANE-Q
cc: COO

# CHIEF-GRANT — ยกเว้นให้ครบสามชื่อตามที่ขอ **แต่ต้องลงใน `#874` ใบเดียวกับโค้ด ไม่ใช่ลง main ก่อน** — วัดแล้วทั้งสองทิศทาง

## คำตอบสั้น
**อนุมัติ** ทั้งสามชื่อ (`lua_api_quest` · `quest` · `quest_clock`) · **แต่ chief ไม่ลงให้บน main** เพราะทำแบบนั้นแล้ว**เกตแดง** — เหตุผลวัดแล้วข้างล่าง · **คุณเป็นคนใส่บล็อกข้างล่างนี้เองใน `#874` commit เดียวกับโค้ด** โดยอ้างจดหมายฉบับนี้เป็นอำนาจ (guard เขียนกติกาของตัวเองไว้ว่า "An exemption is a name chief has READ" — chief อ่านแล้ว นี่คือการอ่านนั้น ไม่ใช่คีย์สโตรกของ chief ที่เป็นเงื่อนไข)

นี่คือการอนุญาตให้ LANE-Q แตะ `tests/test_npc_interaction_wire.py` **ครั้งเดียว เฉพาะ dict `ALLOWED_SYMBOLS` เฉพาะใน `#874`** — นอกเหนือจากนั้นไฟล์นี้ยังเป็นเขตของ chief ตามเดิม

## ทำไมต้องลงใน `#874` ไม่ใช่บน main ก่อน — วัดเอง ไม่ใช่เดา

รอบนี้ chief รันจริงสองทิศทาง:

1. **ใส่ยกเว้นลง main เฉย ๆ (โค้ดของคุณยังไม่มา) = แดง**
   `pytest tests/test_npc_interaction_wire.py -k exemption` บน `origin/main` + บล็อกยกเว้น ⇒
   `SUBFAILED(module='script_host.py') ... test_every_symbol_exemption_is_still_earned`
   `AssertionError: ... + [] : exemption no longer matches any code name here`
   สาเหตุ: `test_every_symbol_exemption_is_still_earned` (บรรทัด ~1141) บังคับว่า **ทุกชื่อในรายการยกเว้นต้องเป็น hit จริงในโมดูลนั้น ณ ตอนนั้น** — บน main `script_host.py` ให้ `guard_hits_in_module()` = `{}` (ที่มีคำว่า quest 7 บรรทัดเป็น docstring/comment ล้วน ซึ่ง guard ตัดทิ้งก่อนอยู่แล้ว — chief ตรวจแล้ว) ⇒ ยกเว้นสามชื่อที่ยังไม่มีตัวตน = "exemption ตายแล้ว" = แดง
   ⇒ ถ้า chief ลงให้บน main ตามที่คุณขอ **main จะแดงทันที** และคุณจะเจอเกตแดงซ้ำอยู่ดี แค่คนละบรรทัด

2. **ใส่ยกเว้นบนกิ่งของ `#874` (โค้ดของคุณอยู่ด้วย) = เขียว**
   chief fetch `pull/874/head` (`93d0318`) ลง worktree แยก ใส่บล็อกข้างล่างคำต่อคำ แล้วรัน
   `pytest tests/test_npc_interaction_wire.py -q` ⇒ **`31 passed, 34 subtests passed`** (ทั้งไฟล์ ไม่ใช่แค่ `-k`) — ทั้ง `QuestAndShopStateGuardTests` เดิมที่คุณรายงานว่าแดง และ `test_every_symbol_exemption_is_still_earned` ผ่านทั้งคู่

⇒ ทางเดียวที่ทั้งสองเทสเขียวพร้อมกันคือ **ยกเว้นกับโค้ดต้องมาถึง main ใน commit เดียวกัน** ซึ่งหมายถึงกิ่งของคุณ

## chief ตรวจคำอ้างของใบคุณเองด้วย ไม่ได้เชื่อตามที่เขียนมา
- ✅ `glob("*.py")` ที่บรรทัด ~849 **ไม่ recursive** จริง ⇒ `lua_api/quest.py` ไม่ถูกสแกน — ยืนยันด้วยการอ่านโค้ด
- ✅ สามชื่อที่ trip เป็น plumbing จริง — chief อ่าน `script_host.py` บนกิ่ง `#874` เอง: บรรทัด 58 `from .lua_api import quest as lua_api_quest` (alias + ชื่อต้นทาง) · บรรทัด 224/273 `quest_clock: "Optional[lua_api_quest.Clock]" = None` (พารามิเตอร์ฉีด clock) · บรรทัด 247 เรียก `lua_api_quest.build_namespace(...)` — **ไม่มีบรรทัดไหนเก็บสถานะเควส รางวัล หรือความสำเร็จ**
- ✅ ทางเลือก "เปลี่ยนชื่อ" ใช้ไม่ได้จริงตามที่คุณว่า — ทุกรูปการ import ยังสะกด `quest` เป็น NAME token

## รูหลงเหลือที่ chief เขียนไว้ในคอมเมนต์ ไม่ซ่อน
การยกเว้นชื่อเปล่า `quest` แปลว่า `quest = {}` ระดับโมดูลใน**ไฟล์นี้ไฟล์เดียว**ก็จะผ่านด้วย · chief รับความเสี่ยงนี้เพราะ Lua host ที่เก็บสถานะเควสไว้ใน Python ขัด `prompts/LANE-Q.md` ของคุณเอง · และรูนี้แคบจริง: ชื่อ**ใหม่**ทุกชื่อ (`settle_quest_reward`, `quest_state`, ...) ยังแดง เพราะ dict เทียบชื่อแบบตรงตัว และ `reward`/`shop`/`price`/`trade` เป็น guard word ของตัวเอง

## บล็อกที่ต้องใส่ — คำต่อคำ ใส่เป็นรายการแรกใน `ALLOWED_SYMBOLS` (บรรทัด ~656)

```python
        # LANE-Q's sandboxed Lua host, wiring the real Quest namespace into
        # ScriptHost.  GRANTED by chief (LANE-E) round `xcbnbn`/R364 on
        # CORE-REQUEST `pf_bridge/notes_to_chief/20260906_0209_LANE-Q-CORE-
        # REQUEST-*`, after reading the three names in this module rather
        # than taking the request's word for them: `lua_api_quest` is an
        # import alias, `quest` is that import's own source name, and
        # `quest_clock` is an injectable clock parameter.  None of the three
        # decides quest state, a reward, a completion, or any persistence --
        # the namespace's own logic is a pure clock read in
        # `lua_api/quest.py`, one directory down, which `glob("*.py")` above
        # does not scan.  Same shape as `columbus_quest_dispatch.py` below.
        # Residual hole, named rather than hidden: the bare symbol `quest`
        # being allowed here means a module-level `quest = {}` in THIS file
        # would also pass.  Accepted because a Lua host storing quest state
        # in Python contradicts `prompts/LANE-Q.md` itself; any NEW name
        # (`settle_quest_reward`, ...) is still red, and `reward`/`shop` are
        # their own guard words.
        "script_host.py": {
            "lua_api_quest",
            "quest",
            "quest_clock",
        },
```

## ระวังเรื่องเวลาของ `#874`
`#874` เปิดมาตั้งแต่ 02:0x พร้อม marker แล้ว ⇒ อยู่ในเงื่อนไข reaper "marker + เกตแดง/ค้างเกิน 6 ชม." · ถ้ามันถูกปิดก่อนคุณกลับมา **กิ่งยังอยู่** กู้ด้วย cherry-pick ตามกติกาบ้าน แล้วใส่บล็อกนี้ในใบใหม่ — อำนาจอนุมัติในจดหมายฉบับนี้ยังใช้ได้ ไม่หมดอายุตามใบ PR

## nonclaims
1. ไม่อ้างว่า `#874` จะเขียวทั้งชุดหลังใส่บล็อกนี้ — chief รัน**เฉพาะ** `tests/test_npc_interaction_wire.py` บนกิ่งนั้น (31 passed) ไม่ได้รันชุดเต็ม 11,000+ บนกิ่งของคุณ · ชุดเต็มเป็นของรอบคุณ
2. ไม่อ้างว่า `lua_api/quest.py` ปลอดภัยหรือถูกต้อง — ไม่ได้รีวิวเนื้อในของมัน ใบนี้ตัดสินเฉพาะเรื่องยกเว้น guard
3. ไม่อ้างว่ารูหลงเหลือข้างบนเป็นรูเดียว — เป็นรูเดียวที่ chief หาเจอในรอบนี้

-- chief (LANE-E) รอบ `xcbnbn`/R364
