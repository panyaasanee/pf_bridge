ถึง: chief (cloud) / LANE-B

# RE-109 RESULT — DONE / BOUNDED-NEGATIVE: actor-name color driver remains behind unlabelled virtual/resource consumers

เวลาเริ่มใบ: `2026-08-27T18:00:48.278+07:00`  
เวลาปิดผล: `2026-08-27T18:15+07:00`  
โหมด: static only; ไม่เปิดเกม ไม่จับ `LOCK_GAME` ไม่แตะ canonical DB/source/queue

## คำตอบสั้น

ยังทำ byte/field map ของสีขาว/เขียว/เหลือง-น้ำเงิน/ส้ม/แดงเข้ม/เทา/ชมพูไม่ได้จาก static image นี้โดยไม่เดา จึงปิดตามเกณฑ์ bounded negative ของใบ

สิ่งที่ pin เพิ่มจาก RE-067/068 คือ path ของ **ตัวเรา** กับ **มอน** ไม่ใช่ path เดียวกันตั้งแต่ชั้น class/nameboard:

- `actor_type=3` สร้าง `CMyActor` และ vtable `+0x7C` สร้าง `NameBoardPlayer` (`0x456580`; update complete CFG `[0x005BD320,0x005BD8DB)`).
- `actor_type=4` สร้าง `CNetNPC` และ vtable `+0x7C` สร้าง `NameBoardNPC` (`0x45C560`; update complete CFG `[0x005BD8E0,0x005BDF20)`).

ดังนั้น “ตัวเราเป็นส้ม” กับ “มอน neutral เป็นส้ม” **ห้ามสรุปว่าเป็น field เดียวกัน** จาก RGB ที่เห็นเท่ากัน ทั้งสอง observation เข้าคนละ board class และ concrete update คนละ body. ใน body ที่ถอดครบทั้งสองฝั่งไม่พบ direct call ไป `FONT_COLOR` loader `0x5491B0` หรือ relationship comparator `0x4A1D50`; consumer ที่เหลือเป็น virtual/resource state ซึ่งยังไม่มี receiver/property crosswalk.

## T0 — controls และ inputs

- `GameClient/GameClient.local.bin`: size `14,759,424`, SHA-256 `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`.
- `CLIENT_RE_QUEUE.md`: SHA-256 `bbcf4942c2a15a8498d00fb92afa9874b2ab795c55bc68b194bc775303b0ea51`.
- `NEW_ORDERS.txt`: SHA-256 `8129a95e3a4c4f61a48b71fd593413ec9087883be703334407177edb3a70aab3`.
- `AGENTS.md`: SHA-256 `8b7fab9e409ffbcbda5accbb22016a4ed6cea5c134e11d107a25fbe41e6ed6e3`.
- owner reference `20260827_1635_PANYA-REFERENCE-original-server-combat-loop-colors-death-loot-vs-ours.md`: SHA-256 `d3b79bbc63c22c865a6b2f04317ed9ef48ebddd2a2d8f0af7271f36571410b32`.
- LANE-B status `20260827_1734_LANE-B-STATUS-panya-reference-consumed-re107-re108-closed-re109-110-111-opened.md`: SHA-256 `58a8562a323fefc005e6536746c58292740b177036fefcf72f05cbe5b96b8b9f`.
- prior controls: `re067_static_verify.py` SHA `838c70ef...56026e2`; `re068_static_verify.py` SHA `b17b5411...e1edbd`; RE-068 rerun ผ่าน `46/46` และภายใน rerun RE-067/UI controls ครบ.
- verifier ใบนี้: `staged/re109_actor_name_color_static.py`, SHA-256 `961c5a79b8613de2c6568cb05a39ed6625a6b719f1c64e940d527d742ea8674c`; ผล `43/43`, `failed=0`.

ชุดค้นร่วมทำครั้งเดียวและ reuse:

- `external/**`: 28 files, 28,965,991 bytes, manifest fingerprint `07fdbbdc0b760f728f9266cb1f0a2b6c80f84cc014e497a33b994652b3dc8d89`.
- `gamedata/**`: 1,109 files, 15,319,585 bytes, manifest fingerprint `4c81ba5efc202d426d667b1abef961e2c8c0ec6c8b2075a0a8773f2213de4d8e`.

## T1 — xref ตัวเลือกสี

ขอบเขต complete recursive CFG ที่ pin ใหม่/ยืนยันซ้ำ ทุก span ด้านล่าง `SPAN_GAP_BYTES=0`, `DECODE_ERRORS=0`:

- Player: allocator `0x456580`, bind `0x5BE080`, update `0x5BD320` (`485` instructions, span SHA `204704c5...aa6a8`).
- NPC: update `0x5BD8E0` (`503` instructions, span SHA `e5a09bce...23c2c`) และ concrete callees `0x5BC580`, `0x5BB560`, `0x5BB6B0`, `0x5BB7F0`, `0x5AA5E0`, `0x5BAE30`.
- Relationship comparator `0x4A1D50` (`84` instructions, span SHA `cbc9d0ab...cac5`) มี direct rel32 caller เดียว `0x43C5E0` ใน complete body `0x43C380`; caller นี้อยู่นอก Player/NPC board updates ที่ตรวจ.
- `0x5BAC20` เป็น HP-bar texture toggle ที่อ้างเพียง `Bar_Hp_Mob.tga`/`Bar_Hp_Npc.tga`; ไม่ใช่ `LABEL_NAME` color selector.
- `NameBoardNPC` vtable 15 slots ถูก census/pin ครบ; concrete update/callees ที่ตรวจไม่มี direct call ไป relationship comparator หรือ `FONT_COLOR` loader.

สิ่งนี้ **ไม่ใช่** คำกล่าวว่า virtual consumer ไม่มีทางเลือกสี; เป็นขอบเขต negative ที่บอกว่าตัวเลือกไม่ปรากฏเป็น direct field→color edge ใน bodies ที่ถอดครบ และ static ยัง resolve receiver/property ของ virtual calls ต่อไปไม่ได้.

## Mandatory search — external

ค้น `external/**` ทั้งชุด textual (`.tsv/.md/.txt`) หลังอ่าน `00_SEARCH_HERE_FIRST.md`:

- เจอ structural rows ของ `CreateActorVital`, `BasicAttr`, `NPCAttr`; schema ของ `CreateActorVital` ยังมี scalar `u8` หลายตัว แต่ไม่มีชื่อ semantic ว่าเป็น name-color/relation selector.
- ไม่พบ semantic row สำหรับ `NameColor|name_color|DrawName|NameLabel|HeadName|TitleColor|FontColor|NameBoard` ในขอบเขตนี้.
- `ActorRelationshipData` ยังไม่มี serializer/getter/crosswalk ที่ใช้ผูก wire byte เข้ากับ board property.

ผลลบนี้จำกัดที่ external snapshot/fingerprint ข้างต้น ไม่ได้ claim ว่า client ไม่มี path ดังกล่าว.

## Mandatory search — gamedata

ค้น `gamedata/**` หลังอ่าน `00_SEARCH_HERE_FIRST.md`:

- เจอ `CONSTDATA_TH__FONT_COLOR.tsv`: 57 rows, columns `n_ID/f_RED/f_GREEN/f_BLUE`.
- เจอ `CONSTDATA_TH__FACTION.tsv`: 38 rows, columns `n_ID/s_ENEMY`.
- เจอ `MOBS.n_SKIN_COLOR` ที่ `PF_GAMEDATA_COLUMNS.tsv` row `MOBS/24`.
- ไม่พบ Lua crosswalk ที่ผูก `FONT_COLOR`, faction หรือ `n_SKIN_COLOR` เข้ากับ actor `LABEL_NAME`.

สามอย่างนี้เป็นตาราง/field แยกกัน ไม่มี foreign-key/consumer field ที่พิสูจน์การ join; ห้ามจับคู่เพราะเลข ID เท่ากัน. `field_mobs.py` SHA `58bd7757...31638e` ระบุชัดว่า faction `player=1`, `mob=6` เป็น **OUR DESIGN**, ไม่ใช่ original-client color semantics.

## T2 — map ตาม observation ที่ยืนยันได้

| สี/สถานะที่ owner เห็น | path ที่ static pin ได้ | byte/field map |
|---|---|---|
| ขาว — ตัวเองเดิม | `CMyActor → NameBoardPlayer` | UNKNOWN |
| เขียว — ผู้เล่นอื่นเดิม | player-family → `NameBoardPlayer` | UNKNOWN |
| เหลือง/น้ำเงิน — NPC เดิม | `CNetNPC → NameBoardNPC` | UNKNOWN |
| ส้ม — มอนยังไม่ aggro เดิม | `CNetNPC → NameBoardNPC` | UNKNOWN |
| ส้ม — Arena01 ของเรา | `CMyActor → NameBoardPlayer` | UNKNOWN; คนละ board class กับแถวก่อน |
| แดงเข้ม — มอน aggro เดิม | `CNetNPC → NameBoardNPC`; relation/faction เป็น candidate เท่านั้น | UNKNOWN |
| เทา — มอนตายเดิม | `CNetNPC → NameBoardNPC`; death state มี path อื่นที่ RE-107 pin | UNKNOWN ที่ color sink |
| ชมพู/magenta — มอนของเรา | `CNetNPC → NameBoardNPC` | UNKNOWN; ไม่มี provenance ผูกกับค่าที่เราส่ง |

จึงตอบ objective 2 ได้เพียงว่า static ปัจจุบันพิสูจน์ว่า **คนละ class/path ก่อนถึง unresolved consumer**; ยังพิสูจน์ไม่ได้ว่า downstream ใช้ field เดียวกันหรือคนละ field และห้ามเติมคำตอบจากสีที่เหมือนกัน.

## T3 — attended capture ที่แคบที่สุด

แยกสอง experiment ห้ามรวม self กับ NPC:

1. **NPC A/B:** identity, `actor_type=4`, name, preset, XYZ, HP/death state และทุก attr byte คงเดิม; เปลี่ยน relation/faction scalar ที่มี serializer crosswalk เพียงหนึ่ง field/หนึ่งค่าในแต่ละ run. เก็บ screenshot client-observable กับ exact frame/decoded wire แยกหลักฐาน. เริ่ม control neutral แล้ว mutant เดียว; ไม่ sweep หลาย byte พร้อมกัน.
2. **Player A/B:** identity, `actor_type=3`, START_GAME/selected-actor body และ faction คงเดิม; เก็บ control สีส้มปัจจุบัน แล้วเปลี่ยน scalar ใน `CreateActorVital` ทีละตัวได้ **หลัง** pin offset/serializer ของ scalar นั้น. ห้ามเอาผล NPC มาเป็น crosswalk ของ Player เพราะ board class ต่างกัน.

ถ้าไม่มี control สีขาวที่ wire-known ให้ทำ passive capture ของ control ก่อน ไม่เดาค่า “white”. เกณฑ์รับหนึ่ง mapping คือเปลี่ยน field เดียวแล้วสีเปลี่ยนซ้ำได้ โดย frame diff ยืนยันว่า byte อื่นไม่เปลี่ยน.

## Nonclaims / method ceiling

1. ไม่ claim ว่า RE-067 ผิด: ใช้ผล RE-067/068 เป็น controls; RE-109 มีหลักฐาน owner ใหม่และเพิ่ม Player path จึงไม่ใช่ rerun method เดิมล้วน ๆ.
2. ไม่ claim ว่า faction ทำให้ตัวเราเป็นส้ม หรือทำให้มอนเป็นแดงเข้ม.
3. ไม่ claim ว่า `actor_type` เลือกสี; static พิสูจน์เพียงว่าเลือก class/nameboard ต่างกัน.
4. ไม่ claim ว่า RGB เหมือนกันหมายถึง property ID/field เดียวกัน.
5. ไม่ claim ว่า `FONT_COLOR`/`FACTION`/`MOBS.n_SKIN_COLOR` join กันจากเลข ID.
6. ผล negative จำกัดที่ pinned image, external/gamedata snapshots และ complete CFG bodies ที่ระบุ; virtual UI-manager/widget consumer ยัง unresolved.
7. นี่เป็น **method ceiling**: ห้าม rerun RE-109 ด้วย static direct-call/linear-xref แบบเดิมจน chief มี symbol/UI receiver map, wire crosswalk ใหม่ หรือ attended A/B capture.

BUILD_IMPACT: ตอนนี้ไม่มี client/server color fix ที่ provenance รองรับ; ห้าม hard-code สีจาก `actor_type`, faction `1/6`, `FONT_COLOR` ID หรือ `MOBS.n_SKIN_COLOR`. งาน build ต้องรอ attended one-field A/B crosswalk แยก Player/NPC ก่อน.
