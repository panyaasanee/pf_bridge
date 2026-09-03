[ถึง: chief · จาก: Codex RE runner · 2026-08-30T09:57+07:00]

# RE-154 RESULT — DONE · ตัวตอบ ChooseNPC อ่าน membership จริง; ข้ออ้างว่า `population_indices=None` แล้วยังเข้ากิ่งนี้ขัดกับ source ปัจจุบัน

## ขอบเขตและ input pin

- START: `2026-08-30T09:49:08.386+07:00` · static only · ไม่เปิดเกม/เซิร์ฟเวอร์/DB และไม่รัน test
- คิวเปลี่ยนระหว่างรอบ จึงอ่านใบเต็มใหม่หลัง mtime `2026-08-30T09:56:04.680+07:00`: queue SHA-256 `75b3344883f9df1c4ee1edb96f5a528cc372a2d39bcc31b717ede6eceaa80efe`; RE-154 section SHA-256 `d3a4105b403cdb21e136248e3c1136ddd1b04b9b56d92e31baf7f8701235e1a5`
- source-search manifest (frozen v141 + `src/pirateforce_foundation/**/*.py`): 120 files / 4,407,840 bytes / `42031f7d675c51d83ab06b41407ab6455627fcd8709071762ba5d362aac61edf`
- key files: v141 `2eb05ed2...ea4c22`; runtime `bcda2688...e4bcd`; scene gate `c1b07cd8...0a6b1`; world face `91676e12...17341`; scene-14 responder `86a02027...909a`

## คำตัดสินสั้น

Premise ในหัวใบถูกหักครึ่งหนึ่ง: กิ่ง `ChooseNPC` ของ v141 **อ่าน `population_indices` เป็นเกตจริงสองชั้น** และไม่ได้ตอบเมื่อมันเป็น `None` ตาม source ที่ pin อยู่ตอนนี้ แต่กิ่งนี้ **ไม่อ่าน scene** และเมื่อ membership เป็น non-`None` มันสร้างเฟรมจากตาราง Port Royal แบบ hard-coded ดังนั้น stale/wrong-scene membership ยังทำให้ตอบคนผิดหรือ crash ได้

สอง label ที่ใบยกมา (`V98_NPC_FACE_PLAYER_POSITION_HEADING_P0` และ `V112_TEST_HARNESS_FACE_PLAYER_P91`) ออกมาจากกิ่งนี้เท่านั้น ใน source SHA ข้างบน การได้ label เหล่านั้นพร้อมสถานะ `population_indices=None` เป็นไปไม่ได้: เงื่อนไข line 4397 จะปฏิเสธก่อนเข้าลูป ต้องกลับไปตรวจ revision/state ของสคริปต์ D2; ห้ามใช้ผลนั้นสรุปว่าตัวตอบไม่อ่าน field

## 1) v141 ตัดสิน ChooseNPC อย่างไร

1. `current/pf_login_game_server_v141.py:4395-4399` รับเฉพาะ outer ที่ `nested_id` เป็น `TARGET_VITAL` หรือ `CHOOSE_NPC`, ต้องมี `self.population_indices is not None`, และต้องยังไม่อยู่กิ่ง destination marker1
2. `:4400-4408` parse เฉพาะ `ChooseNPC` records ที่ฝังอยู่จริง แล้ว dedupe identity; bare `TargetVital` ที่ไม่มี ChooseNPC ให้ list ว่างและไม่ตอบ actor
3. `:4409-4410` แปลง `idx = actor_identity - 0x2001` และตอบต่อเมื่อ `idx in self.population_indices`
4. ไม่มี scene check ในกิ่งนี้ และ `make_v98_conversation_face_state` ที่ `:1078-1106` สร้าง actor ทั้งชุดจาก `PORT_ROYAL_UNAMBIGUOUS_PLACEMENTS`; `:1093-1095` ใช้ `by_idx[idx]` แบบ hard lookup ทุก member
5. ตาราง Port Royal อยู่ `:1323-1439`, มี 115 แถวแบบ sparse ช่วง index `0..148` จึงให้ band ที่ *เป็นไปได้* `0x2001..0x2095` แต่ set ที่ตอบจริงคือ `{0x2001 + idx | idx อยู่ใน population_indices และมีแถว Port Royal}` ไม่ใช่ทั้งช่วง
6. special cases หลัง membership ผ่าน:
   - index 30 / `0x201F`: `:4411-4415` ไม่ตอบ NPC
   - index 91 / `0x205C`: `:4433-4447` ส่ง face + `TradeZoom store5` ครั้งเดียว
   - index 0 / `0x2001`: `:4448-4468` ส่ง face + q3020 conversation ครั้งเดียว
   - index อื่น: `:4470-4478` ส่ง face + empty/default conversation
   - identity นอก current membership: `:4479-4482` ignore

ผลสำคัญ: `population_indices` เป็นหลักฐาน server-side ว่าเคย queue census ไม่ใช่หลักฐาน client-observable ว่าจอรับ/วาดจริง และไม่มี scene stamp อยู่ใน field นี้เอง หาก membership ของ scene อื่นถูกยัดเข้าไป กิ่ง `:1093-1094` จะอ่านตาราง Port Royal; index ที่ไม่มีแถวทำ `KeyError`, index ที่ชนกันให้คน Port Royal ผิดฉาก

## 2) สำมะโนเส้นตอบอื่น

| เส้นทาง | membership/scene gate | ผล |
|---|---|---|
| bare `TargetVital` | v141 `:3788-3815` parse/เก็บ target; P30 arm ต้องมี index 30 ใน membership (`:3808-3809`) | ไม่มี actor reply; embedded ChooseNPC เท่านั้นที่ไปกิ่ง `:4395` |
| idle `ActionVital EA60` | builder อยู่ `:2139-2183` | ไม่มี production call site; `npc_idle_action_sent` ถูก reset แต่ไม่เคย set true จึงไม่มี active idle responder |
| shop open จาก P91 | ผ่าน ChooseNPC membership ก่อน (`:4409-4410`, `:4433-4447`) | ไม่ตอบ actor ที่ไม่อยู่ membership ในกิ่งนี้ |
| `TradeCmdVital` cart/final buy | `:4128-4201` ตรวจแต่ wire fields, counters และ cash; **ไม่ตรวจ scene, membership, `shop_store5_open_sent`, หรือ actor** | ช่องโหว่ sink จริง: forged/desynced client ขอ cart ack ได้จาก initial state และไป cash update ได้หลัง sequence แม้ไม่เคยได้รับ P91/store |
| q3020/default conversation | `:4448-4478` อยู่หลังกิ่ง ChooseNPC membership | ไม่มีกิ่ง conversation actor-ungated ใน v141 |
| destination P86 conversation | `:4483-4525` ต้อง marker1 membership exact + armed sequence + one-shot state | gated แยกต่างหาก |
| Columbus q3021/3205 modular responder | `runtime.py:4786-4810` ต้อง placement index 1 อยู่ใน `population_indices` ก่อน parse/compose | gated |
| scene-14 responder ที่เตรียมไว้ | `lane_a_choose_npc_scene14.py:120` ยัง `production_allowed=False`; `:165-171` ตรวจ membership และ selected idx; runtime ไม่มี call site | ยังไม่ออก production wire |
| default mob combat `ActionVital` | `runtime.py:4054-4095` resolve จาก selected-scene roster แต่ไม่ตรวจ client-announced census membership; `:4188-4193` เริ่มส่ง `MOB_COMBAT_ANNOUNCE` | ช่องโหว่ actor-target sink อีกจุด: valid forged ActionVital อาจตอบ field mob ที่อยู่ใน roster แต่ไม่เคยประกาศให้ client |
| opt-in scene action ack | `runtime.py:6476-6504` ต้อง `scene_remote_spawned` และ prior hostile TargetVital capture | ไม่ใช่ unannounced path ตาม state machine นี้ |

## external / gamedata ก่อนอ่าน source

- `pf_bridge/external`: สแกน 125 files / 36,886,598 bytes ครั้งเดียว; manifest `f5c1d036...ef6440`. พบ `ChooseNPC`/`TargetVital` ใน 8 registry/validation files (เช่น `PF_PROTOCOL_REGISTRY.tsv`, `PF_SERIALIZER_FIELDS.tsv`) ซึ่งยืนยัน class/field/capture direction เท่านั้น; ไม่พบ `population_indices`, `0x2001`, `0x205C` หรือ server membership gate ใน hit ชุดนี้
- `pf_bridge/gamedata`: สแกน 1,109 files / 15,319,585 bytes ครั้งเดียว; manifest `ae16237d...ac54d`; ไม่พบ exact terms `ChooseNPC`, `TargetVital`, `population_indices`, `0x2001`, `0x205C` หรือสอง output label จึงไม่มี data crosswalk เพิ่มเติมสำหรับ admission

## เกตที่ถูกต้อง / BUILD_IMPACT

`current/pf_login_game_server_v141.py` ต้องคง immutable. จุดแก้ของ ChooseNPC cross-scene คือ `src/pirateforce_foundation/runtime.py` **ก่อน** `actions = super().dispatch(parsed)` (`runtime.py:6657`): สำหรับ `TARGET_VITAL/CHOOSE_NPC` ให้เลือก responder ตาม current scene, ตรวจ production-allowed + scene-stamped announced membership, แล้วไม่ปล่อย frozen Port-Royal responderอ่าน membership ของฉากอื่น. Seam ถูกเตรียมไว้แล้วที่ `lane_hooks.__init__.py:482-486`; module scene 14 ระบุ contract นี้ตรง ๆ ที่ `lane_a_choose_npc_scene14.py:51-60`

ต้องแยก sink gate เพิ่ม ไม่ควรเหมารวมว่าแก้ ChooseNPC แล้วจบ:

- TradeCmd: require active store session/latch ที่ผูก scene + actor ที่ประกาศจริงก่อน cart/final-buy reply; `shop_store5_open_sent` อย่างเดียวเป็นขั้นต่ำแต่ยังไม่ scene-stamped
- Mob combat: require target อยู่ใน census membership ที่ส่งให้ session/scene นั้นจริง ไม่ใช่เพียงอยู่ใน static roster

ใบนี้ไม่แก้โค้ดตาม objective จึง `BUILD_IMPACT=ANALYSIS_ONLY`; ไม่มี build/test/runtime/commit

## nonclaims

1. static proof เท่านั้น ไม่ใช่ runtime/capture/client-observable proof และไม่อ้างว่าผู้เล่นปกติส่ง forged request
2. ไม่อ้างว่า R236 เป็น regression; source ปัจจุบันแสดงว่าการ restore สี่ fields ที่ `runtime.py:6697-6702` ปิด stale-latch แบบที่ docstring อธิบาย แต่ไม่ได้ re-run D2
3. ไม่อ้างว่า `population_indices` พิสูจน์การ render บนจอ; มันเป็น server-side queued-membership latch
4. ไม่จับคู่ identity เพราะเลขเท่ากันข้ามฉาก; band `0x2001..0x2095` เป็น arithmetic ของ sparse Port-Royal placement index เท่านั้น
5. ไม่แก้ v141/runtime/source/gamedata/external/queue และไม่แตะ game/server/DB/git

