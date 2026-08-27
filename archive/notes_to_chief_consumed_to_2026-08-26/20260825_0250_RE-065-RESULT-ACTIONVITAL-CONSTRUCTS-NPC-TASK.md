[ถึง: chief cloud (cc) และ Panya · จาก: RE runner LOCAL]

# RE-065 RESULT — PASS/DONE · ActionVital สร้าง UseBehavior task ให้ projected CNetNPC ได้ในทาง static

- เวลา: `2026-08-25T02:50:37+07:00`
- ใบ: `RE-065 ACTORTASK-USEBEHAVIOR-CTOR-WALK-001`
- หมวด: `STATIC-ON-BRIDGE` · ไม่เปิดเกม/เซิร์ฟเวอร์ · ไม่จับ `LOCK_GAME` · ไม่แตะ DB ใด
- ตัวตรวจรันซ้ำ: `pf_bridge\staged\re065_static_verify.py` · exit 0 · ASCII output · recursive CFG decode errors 0 ทุก span

## คำตอบ objective ประโยคเดียว

**YES — `ActionVital` ขาเข้าจากเซิร์ฟเวอร์สร้าง `CActorTask_UseBehavior` task ให้ projected `CNetNPC` ได้: handler `0x007516C0` resolve actor จาก handle ผ่าน call sites `0x007516EF -> 0x00402A20` และ `0x007516F6 -> 0x00446170`, lookup BEHAVIOR ที่ `0x007517B0 -> 0x00702A10`, แล้วเรียก ctor `0x00751809 -> 0x0047AB30`; type gate ที่ผ่านคือ `CActorBaseClient` token `0x0102CE88` ที่ `0x0047AC0A` (verifier actor hierarchy 111 guards ยืนยัน `CNetNPC` actor_type 4 เป็นลูกใต้ root นี้) และ task ถูก commit เป็น vtable `0x00F0EF10` + flags `8` ที่ `0x0047AB96/0x0047ABEA` ก่อน gate `[actor+0x14]` ซึ่งถ้าตกจะข้ามแค่ optional model wiring แล้วคืน task ที่ `0x0047AE91`.**

## ช่องบังคับก่อนถอด

- **ค้นใน `pf_bridge\external\` แล้ว: เจอ** `ActionVital` (`handler_va=0x007516C0`, serializer span `[0x0074E6A0,0x0074E7DB)`, sha `ff1183...e4d`) และ carrier ที่ใบอ้าง (`CHitResult` handler `0x00750770`, `CKnockdownVital` handler `0x00750700`) ใน `PF_PROTOCOL_REGISTRY.tsv`/`PF_SERIALIZER_FIELDS.tsv`; **ไม่เจอ**ชื่อ `CActorTask_UseBehavior`, `CActorTask_PlayActionEvent`, `CActorTask_Dead` หรือ task-vtable ในชุด external — ตรงกับขอบเขตว่าตารางนี้ครอบ vital ไม่ครอบ task.
- **ค้น gamedata แล้ว: เจอ** `CONSTDATA_TH__BEHAVIOR.tsv` 2,279 แถว × 30 คอลัมน์ (`n_ID`, `s_ANIMATION`, `s_HIT_KEYFRAME`, `s_HITBACK`, ฯลฯ) และมี token `_F_DIE_000`; **ไม่เจอ**ชื่อ task สามตัว, carrier vital, VA, ctor หรือ mapping control-flow. จึงไม่ใช้เลข/ชื่อในตาราง join เข้ากับ ctor และไม่ใช้ gamedata พิสูจน์เส้น code.

พบคำตอบเก่าใน `FACTPACK_R100_DOORB_ATTACK_TASK_CTORS_STATIC.md` ก่อนเริ่มถอด จึงเปลี่ยนจาก “ไปถอดใหม่” เป็น “verify image sha + re-derive byte-exact + ใช้” ตามกฎ. ผล verify พบ correction หนึ่งข้อสำคัญด้านล่าง.

## จ็อบ 1 — control gate PASS

`CActorTask_Dead` เดินซ้ำได้ตรงคำตอบที่รู้แล้ว:

- ctor `0x00472810`, span `[0x00472810,0x00472834)`, file off `0x00071C10`, len 36, sha `54877d3101b779ba1b83e283cbe94f8db9799905fc7a1157a1ada2e3f249c0a7`
- vtable `0x00F0F048` เขียนที่ `0x0047281D`; kind `0x80000005` เขียนที่ `0x00472827`
- UTF-16 token `_F_DIE_000` ที่ `0x00F0F060`; direct caller census = `0x004439E9` จุดเดียว
- recursive CFG: 11 instructions / 36 bytes / gap 0 / errors 0

## จ็อบ 2 — ctor / vtable / custom RTTI

### CActorTask_UseBehavior

- TD `0x0101CEB8`, name `.?AVCActorTask_UseBehavior@@` ที่ `0x0101CEC0`; TD dword ref จุดเดียว `0x00BD1236`
- GetType `0x00471DC0 -> token 0x0102ED50`; vtable slot 0 ของ `0x00F0EF10` ชี้ GetType นี้
- ctor `0x0047AB30`; vtable `0x00F0EF10`; `[task+0x10] = 8` (ไม่ใช่ `0x800000XX`)
- E8/E9 census ของ ctor = 10 จุด: `0x0042514F, 0x0042B815, 0x0042C0C4, 0x0044D1FC, 0x0044D5C4, 0x00453D82, 0x0047B989, 0x0047BA83, 0x00751809, 0x00751AA1`; dword refs ไป ctor = 0

### CActorTask_PlayActionEvent

- TD `0x0101CFB8`, name `.?AVCActorTask_PlayActionEvent@@` ที่ `0x0101CFC0`; TD dword ref จุดเดียว `0x00BD13F6`
- GetType `0x00471F50 -> token 0x0102ECFC`; vtable `0x00F0EF28`
- **ctor มีจริงที่ `0x00471EB0`**: เรียก base ctor `0x00485D40` ที่ `0x00471EDD`, ติดตั้ง vtable ที่ `0x00471EEE`, คืน `this` ที่ `0x00471F32`, `ret 0x14` ที่ `0x00471F44`; ไม่มี kind `0x800000XX`
- direct callers = `0x00448A91, 0x0047C7B6, 0x004BA9EF, 0x004C12DC, 0x0061A645`; dword refs ไป ctor = 0
- **correction ต่อ R100 factpack:** ข้อความเดิม “ctor NOT FOUND / ฟังก์ชัน ~0x471E90 เป็น dtor” ผิด. `0x471E90..0x471EAC` เป็น tail ของ method อื่น; ctor byte-exact คือ `[0x00471EB0,0x00471F47)`. ขอ chief ลง erratum แทนการแก้ไฟล์เก่า.

## จ็อบ 3–4 — verdict ต่อ carrier และ actor gate

- **ActionVital — REACHES:** handler `0x007516C0` resolve performer/target actor จาก qword handle, lookup BEHAVIOR, alloc 0x78 bytes, push `EDI` (resolved actor) ที่ `0x00751806`, call UseBehavior ctor ที่ `0x00751809`. เส้น default ไม่มี CMyActor-only gate; branch `0xEA80` แยกต่างหากมี CMyActor check แต่ไม่ใช่ default construct path.
- **CHitResult — bounded direct negative:** handler `0x00750770` lookup BEHAVIOR ที่ `0x0075082A` แล้วเข้า reaction factory `0x0048D870` ที่ `0x00750A59`; recursive CFG/call-target set ที่วัดไม่เรียก ctor สองตัวโดยตรง. ผลนี้ชี้ path visual reaction เท่านั้น ไม่ใช่คำอ้างว่าไม่มี indirect path ใดในโลก.
- **CKnockdownVital — concrete task UNRESOLVED static:** handler `0x00750700` เรียก builder ผ่าน virtual slot `+0x0C` ที่ `0x0075075F`, แล้ว queue ผลให้ actor ผ่าน `0x004843F0` ที่ `0x00750764`; concrete path `0x0047CAD0 -> 0x0048D270` ติด builder vtable runtime จึงห้ามตั้งชื่อว่า UseBehavior/PlayActionEvent จาก static. ตัวใบยังปิด YES ได้จาก ActionVital โดยไม่เดาเส้นนี้.
- gate ใน UseBehavior ctor: `0x0047AC0A` ตรวจ `CActorBaseClient`; `pf_actor_type_dispatch_static.py` รันกับ image เดียวกัน exit 0, 111 guards, class hierarchy edges 6, actor_type 4 = `CNetNPC`. Gate `[actor+0x14] != 0` ที่ `0x0047AC2B` คุม optional render/animation sub-component แต่ vtable/flags ถูกเขียนก่อนและ bail `0x0047AE91` คืน task.

## Span manifest — ทุกฟังก์ชันที่พึ่ง

ทุกแถว recursive CFG gap 0 / decode errors 0:

```text
HANDLE_KEY          [0x00402A20,0x00402A87) off 0x00001E20 len 103  sha 5823a612986173266ba33447188d218b81c3267341ad708020bba0873fc07022
ACTOR_RESOLVE       [0x00446170,0x004461E6) off 0x00045570 len 118  sha 9aca8f9a7b933faf54502943e8474362617f3c703cb82750990ba7a9488960e7
BEHAVIOR_LOOKUP     [0x00702A10,0x00702A85) off 0x00301E10 len 117  sha a53915973c5f2faab5cb6924759bffee8fd168e81f52cc88970a5866c379006f
POOL_ALLOC          [0x00442D50,0x00442DEF) off 0x00042150 len 159  sha 07b201ca726c122341c4e5af84c98366677b4d6d7533258ce93adcd1083faa59
TYPE_ISA            [0x0088F2B0,0x0088F2D1) off 0x0048E6B0 len 33   sha 00076eb0d61b7763ba58709f657437f455e6c6a2e3da83b3005bef0b847a61e9
ACTOR_QUEUE         [0x004843F0,0x0048441A) off 0x000837F0 len 42   sha e674af915c24df36ad33d7a500a8622de7d91aa7e2de00fb6bc95f1f649530af
ACTORTASK_BASE_CTOR [0x00485D40,0x00485D5B) off 0x00085140 len 27   sha aa2d5ea6cdcf94694d8ac4028e04c071d2408c4c0b858aa3278b6e5566daa262
BEHAVIOR_SINGLETON  [0x004162A0,0x00416307) off 0x000156A0 len 103  sha 59917e70cd5626505a4ed76bd90e8906242464679585c1278be44e6c27baad17
DEAD_CTOR           [0x00472810,0x00472834) off 0x00071C10 len 36   sha 54877d3101b779ba1b83e283cbe94f8db9799905fc7a1157a1ada2e3f249c0a7
USEBEHAVIOR_DTOR    [0x00471D20,0x00471DB2) off 0x00071120 len 146  sha 458fcd5fc1788ce6da749f3d2c6cd0e9839eaa221b878afdddfe0d0fda2dae11
USEBEHAVIOR_GETTYPE [0x00471DC0,0x00471DC6) off 0x000711C0 len 6    sha 2cf3eba98088345f2e3a19e6175b0c8b903db0e45aa3e4b273dabd1b6e7dc603
PLAYACTION_CTOR     [0x00471EB0,0x00471F47) off 0x000712B0 len 151  sha 287e34b64289595550a4a21d6564e91528d51b165c1ca6ad168063193f3aba93
PLAYACTION_GETTYPE  [0x00471F50,0x00471F56) off 0x00071350 len 6    sha 7e3709066b4ca04320755cc1da9baa728fae39f77ddc4f951f08a4f1d178252f
USEBEHAVIOR_CTOR    [0x0047AB30,0x0047AEA9) off 0x00079F30 len 889  sha 44a01825f20d9cba889196679f9a735047774ae1035af49e650389399228ceee
ACTION_HANDLER      [0x007516C0,0x007519EE) off 0x00350AC0 len 814  sha 489bf8110dd35163936e81e6fafc9cd01ae8f76fb24da8af61466199ce96caae
CHITRESULT_HANDLER  [0x00750770,0x00750EBE) off 0x0034FB70 len 1870 sha 9f215538edce8905ed227af46ee5f39bdd4fa06d65e1bc46d5689f814fae88be
CKNOCKDOWN_HANDLER  [0x00750700,0x00750770) off 0x0034FB00 len 112  sha 78b329a0cbec925560f3b678e23fd8f161b35af58adabdf992f02f93805c6178
CKNOCKDOWN_MANAGER  [0x0047CAD0,0x0047CB65) off 0x0007BED0 len 149  sha a78e241e803a8ec9cbbe624f4a48ed7b374ee86f37f7217825248760ece1c05e
BEHAVIOR_BUILDER    [0x0048D270,0x0048D865) off 0x0008C670 len 1525 sha bf02b291afeb1bfa72842aa04723849f9b8f0d2eabc30f8a33cc0ab7130dd11a
HIT_REACTION_FACTORY[0x0048D870,0x0048DB91) off 0x0008CC70 len 801  sha aaea210f5b08f21249e563cacb0af8055dd5d2bba133a2157a500b689cade736
ACTION_SERIALIZER   [0x0074E6A0,0x0074E7DB) off 0x0034DAA0 len 315  sha ff1183bc0258879dd2fe87d3e976ca7a911ed999c6da977e514fa1e9177a4e4d
```

## SHA ก่อน/หลัง

- `GameClient.local.bin` size 14,759,424: ก่อน = หลัง = `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`
- `external/00_SEARCH_HERE_FIRST.md` `6f6c...a459`; `PF_PROTOCOL_REGISTRY.tsv` `27da...fb4d`; `PF_SERIALIZER_FIELDS.tsv` `9928...c123`; `PF_FIELD_VALIDATION.tsv` `080a...1c3` — ก่อน/หลังตรงกัน
- `gamedata/00_SEARCH_HERE_FIRST.md` `f19d...2153`; index `a9ab...b5bc`; columns `6f1a...4d89`; BEHAVIOR TSV `79ee...bf4e` — ก่อน/หลังตรงกัน
- R100 factpack `5b99...cb79`; class census `fd08...becd`; R98 draft `408c...0435` — ก่อน/หลังตรงกัน
- actor hierarchy verifier `b588...5408` และไฟล์ source 4 ตัวที่มัน cross-check (`2eb0...4c22`, `df7b...d52f`, `3953...6d1b`, `669c...3276`) — ก่อน/หลังตรงกัน
- `re065_static_verify.py` `8c70...3e61` — รันซ้ำแล้ว hash ไม่ขยับ
- operational inputs `AGENTS.md`, `CLIENT_RE_QUEUE.md`, จดหมาย R157 — ก่อน/หลังตรงกัน; ไม่แก้คิวหรือไฟล์ของ chief

## ชั้นหลักฐาน

- **static/wire structural:** PASS — image byte-exact + recursive CFG + call/ref census
- **client-observable:** ว่างเปล่าโดยเจตนา — ไม่เปิดเกม ไม่มีภาพ/วิดีโอ และห้ามอ่านผลนี้ว่า NPC โจมตีบนจอแล้ว

## Nonclaims

- YES ฝั่ง static แปลเพียง “มีเส้นทางสร้าง task ใน image” ไม่พิสูจน์ว่า lookup `0x00702A10` คืนแถว BEHAVIOR จริงใน runtime; SCENE-013 null prior ยังคงเป็นความเสี่ยงแยก.
- ไม่พิสูจน์ว่า server ต้นฉบับเคยส่ง ActionVital/behavior-id แบบใด; server เดิมปิดและกู้ไม่ได้.
- ไม่ตั้ง semantics ให้ฟิลด์ `+0x20/+0x24/+0x28/+0x2C/+0x30/+0x34/+0x38/+0x3C/+0x48`; รายงานเพียง offset/code ที่อ่าน.
- ไม่พิสูจน์ `CKnockdownVital` ว่าสร้าง concrete task ตัวไหน; virtual builder ทำให้ส่วนนั้นยัง unresolved static.
- ไม่ compose เฟรม ไม่แก้ encoder ไม่เปิด HYP/ใบใหม่ ไม่แตะ `CAIStateCombatProxy`.
- `INTENT_ATTACK_UNDELIVERABLE` ไม่ควรถูกเลื่อนเป็น runtime-deliverable จากผลนี้ลำพัง; ขั้นต่อยังต้องมีแถว BEHAVIOR ที่ runtime resolve ได้ + attended observation ตามใบที่ chief/Panya เปิดเอง.

## สภาพจบรอบ

- เกม/เซิร์ฟเวอร์ไม่ถูกเปิด · `LOCK_GAME` ไม่ถูกจับ · canonical DB ไม่ถูกอ่านหรือแตะ
- เพิ่มเฉพาะ verifier ใน `pf_bridge\staged\` และจดหมายฉบับนี้; ไม่แก้/ลบ/เปลี่ยนชื่อไฟล์เดิม
- ขอ chief ปิด `RE-065` เป็น **PASS/DONE (YES)** และลง erratum เรื่อง ctor `CActorTask_PlayActionEvent` ในรอบถัดไป
