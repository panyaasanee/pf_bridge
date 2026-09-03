[ถึง: chief cloud · LANE-B · COO | จาก: RE runner local · 2026-08-28T04:14+07:00]

# RE-117 RESULT — PASS/DONE · NPCAttr ใช้ BasicAttr level/MP bits ชุดเดียวกับ PC จริง

- ใบ: `RE-117 NPCATTR-LEVEL-MP-BIT-001 [STATIC-ON-BRIDGE]`
- START ใบ: `2026-08-28T04:12:37.448+07:00`; ยืนยันไม่มี result letter เดิมและ queue/orders ไม่ขยับหลังปิด RE-118
- วิธี: static/read-only เท่านั้น · ไม่เปิดเกม/server · ไม่จับ `LOCK_GAME` · ไม่แตะ canonical DB/source/queue/git
- verdict: คำตอบเป็น **มีทั้ง level และ MP**. `NPCAttr::Serialize` ที่ `0x00466EB0` เรียก common `BasicAttr::Serialize` `0x004656F0` ก่อน derived mask ทุกครั้ง. ใน base เดียวกัน bit `0x0002 -> +0x5E u16 tag 0x12`, bit `0x0010 -> +0x4C u32 tag 0x14`, bit `0x0020 -> +0x50 u32 tag 0x14`, ครบทั้ง W/R. ดังนั้นไม่ใช่บิต PC-only และไม่ใช่ bounded negative.

## ช่องค้นบังคับ

- **ค้นใน `pf_bridge\external\` แล้ว: เจอ** ใน shared tree 30 ไฟล์ / 29,900,221 ไบต์ fingerprint `399098b4eb5a61ef07fffb5867ce3a8bb5eab0a68f6fb3a39fc452515fc9c61c`: registry ปิด identity ของ `ActorAttr`/`NPCAttr` และ validation ยัง 0 frame. `PF_SERIALIZER_FIELDS.tsv` จัด registry serializer `0x0043BB80` เป็น `EMPTY` argument copier สำหรับทั้งสองชื่อ — **ไม่ใช่** concrete BasicAttr/NPCAttr body ที่ V141 re-derive ไว้; รอบนี้ reconcile ด้วย direct call `0x00466EBF -> 0x004656F0` จากอิมเมจจริง. ไม่เจอ semantic level/MP row ใน external.
- **ค้น gamedata แล้ว: เจอ** ใน shared tree 1,109 ไฟล์ / 15,319,585 ไบต์ fingerprint `cf7d8e93bd798bc425ce346bdf8b2bbdc0a52b1632d89bd980580ae384660d8a`: `MOBS.n_LEVEL_MIN/n_LEVEL_MAX` ที่ columns 9/10 และ `STANDARD_MOB.n_HPMAX`; **ไม่เจอ MP/MAX_MP column** ใน `MOBS` หรือ `STANDARD_MOB`. นี่ให้ provenance ของค่า level แต่ไม่ให้สิทธิ์เดาค่า MP.

## T0 — SHA control

- image SHA-256 `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`, ImageBase `0x00400000`
- V141 source `current/pf_login_game_server_v141.py` SHA `2eb05ed2fdbdd5ee3d91f7fbb8c1d16a4c7a02a843bc97169b16a389e4ea4c22`
- owner decision/probe semantics SHA `6dae5083...b9ce`; prior RE-077 verifier SHA `6f93302d...588f`

## T1 — NPCAttr เรียก BasicAttr จริง

- concrete NPCAttr serializer `[0x00466EB0,0x0046702D)` SHA `da9a2c2a30f4d131d0d3018a9daaa1b4a97bdd2b41145ff6d607a3baa29253ff`
- prologue `0x00466EBB..0x00466EC3`: push mode/stream แล้ว `call 0x004656F0`; หลังจากนั้นจึงแตะ derived byte mask ที่ object `+0xBC`
- ดังนั้น object `this` เดียวกันผ่าน common BasicAttr serializerก่อน NPC-only fields `+0x78/+0x7A/+0x7C/...`; field offsetsด้านล่างเป็น resident field ของ NPCAttr object ด้วย ไม่ใช่การเทียบชื่อ class จาก registry.

## T2/T3 — mask, offset, tag, width

common BasicAttr serializer `[0x004656F0,0x00465986)` SHA `4a8e1b0c95ec929c08bfe944f7f6bfc82d6c64b8b5154f1cbbfb387b5df5ef25`, 252 instructions / 662 bytes / gap 0:

| semantic จาก owner probe | mask bit | object offset | tag / width | W branch | R branch |
|---|---:|---:|---|---:|---:|
| level | `0x0002` | `+0x5E` | `0x12` / 2 bytes | `0x00465736..4A` | `0x00465870..84` |
| MP current | `0x0010` | `+0x4C` | `0x14` / 4 bytes | `0x00465772..86` | `0x004658AC..C0` |
| MP max | `0x0020` | `+0x50` | `0x14` / 4 bytes | `0x00465786..9A` | `0x004658C0..D4` |

positive control ที่อยู่ติดกัน: HP current/max ใช้ bit `0x0004/0x0008`, offsets `+0x44/+0x48`, tag `0x14`, width 4 ที่ `0x0046574A..72`. ตาราง semantics ของ Panya (`20260828_0125...`) ระบุ `+0x5E=level` และ `+0x4C/+0x50=MP cur/max` จาก client-observable PC probe; ใบนี้เพิ่มหลักฐาน static ว่า **NPCAttr วิ่งผ่าน base fields ชุดเดียวกันจริง**.

## T4 — current builder gap

`make_npc_attr` ใน V141 มี base mask `0x0004|0x0008|0x0100|0x0200` และ optional `0x0001/0x0040`; ยังไม่มี parameters/emit ของ `0x0002/0x0010/0x0020`. นี่คือ builder gap จริง ไม่ใช่ wire-format absence.

ค่าที่ build ได้ทันที:
- level: ใช้ `FieldMob.level`/MOBS level provenance ที่สาย B มีอยู่แล้ว แล้ว emit `u16tag(0x12, level)` หลัง basic name ตามลำดับ mask
- MP cur/max: surface/tag/offset พิสูจน์แล้ว แต่ gamedata ชุดที่ค้นไม่มี MP source สำหรับมอน/NPC; expose parameters ได้แต่ **ห้ามประดิษฐ์ค่าหรือ join จาก STANDARD_STATUS ของ PC** จนสาย B เลือก value provenance แยกต่างหาก

## verifier / reproducibility

- `pf_bridge\staged\re117_npcattr_level_mp_static.py` SHA-256 `ba1a76c8bb8515f2b8261099574d7a01d25390b9d8ca6ac0e0270d8b8b8a57e5`
- รัน `python -B` อิสระ 2 ครั้ง: PASS `20/20` ทั้งคู่, exit `0/0`
- probe `pf_bridge\staged\re117_disasm_probe.py` SHA `7e8319ac404685b2846c12b0a2833520083f3f89d75284055d925337d6aee11f`
- source inputs image/V141/external/gamedata/queue/AGENTS/NEW_ORDERS ไม่ขยับระหว่างใบ

## nonclaims

1. ไม่อ้างว่า NPC/มอนต้องแสดง level/MP บนจอเหมือน PC; ใบนี้พิสูจน์ wire surface/common serializer ไม่ใช่ UI consumer.
2. ไม่อ้างว่า owner probe ผิดหรือย้าย semantic ด้วยชื่อ offsetอย่างเดียว; semantic มาจาก owner probe ส่วน applicability มาจาก direct NPCAttr→BasicAttr call.
3. ไม่อ้างค่า MP ที่ถูกของ NPC/มอน; gamedata ที่ค้นไม่มีแหล่งนั้น จึงห้ามเดา `0/0`, `0/1` หรือยืม PC formula.
4. ไม่อ้างว่าทุกรุ่น client ใช้ layout นี้; พิสูจน์อิมเมจ v141 SHA ที่พินเท่านั้น.
5. ไม่มีหลักฐาน client-observable ใหม่ในใบ static นี้; ไม่ใช้ผล static แทนการเห็น HUD/target panel.

## BUILD_IMPACT

**BUILD_IMPACT:** สาย B เพิ่ม optional `level/current_mp/max_mp` และ mask `0x0002/0x0010/0x0020` ใน `legacy.make_npc_attr`; wire `level` จาก `FieldMob.level` ได้ทันทีสำหรับรอบ `GT-084`, ส่วน MP ให้คง omit จนมี value provenance แยก — ห้ามถือว่า wire surface ที่พิสูจน์แล้วเท่ากับค่าที่เดาได้.

BUILD_IMPACT_NONE: 0/1

สถานะที่ chief ควรกรอก: `RE-117 PASS/DONE — NPCATTR INHERITS BASIC LEVEL/MP BITS`.
