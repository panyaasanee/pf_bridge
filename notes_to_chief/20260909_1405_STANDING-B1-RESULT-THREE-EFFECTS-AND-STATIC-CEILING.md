งานเป้าหมายยืน — ยังไม่มีเลขใบ ขอให้ LANE-K ตั้งเลขและผูกจดหมายนี้
ADDRESSEE: GT-272 equipment owner / LANE-B / LANE-DB / LANE-CS / CORE / LANE-K / chief / Panya · Codex static RE
B1q · IMAGE A / prior capture A within its recorded scope / composition D · 2026-09-09 · BOUNDED ANSWER + STATIC CEILING

[MEASURED] คำตอบ B1: ผลสามอย่างใช้คนละ state object/consumer แต่สามารถอยู่ใน `GSCN_RunTimeProtocolRes 0x6E9D` envelope เดียวกันได้. `ItemOperateVitalRes 0x4C13` อัปเดต bag/UI; actor collection ที่มี `AvatarAttr 0x16A0` อัปเดตภาพบนตัว; `CBuffVital 0x15E0` อัปเดต buff aggregate/stat. Static image ไม่พิสูจน์ว่า original server รวมสามส่วนนี้ใน frame เดียวหรือส่งหลาย frame และไม่มี authentic op=5 response ใน corpus ปัจจุบัน.

ค้นชุดส่งมอบแล้ว: B1a–B1p มีเส้นทางแยกครบ; RE-059 มี 0x4C13 จริง 5 เฟรม แต่ผู้เขียนเดิมจำกัดชัดว่าไม่พิสูจน์ producer/original-server policy และทุก ItemAttr มี `+0x39=0xFF`, จึงไม่ใช่ equip response. รัน extractor เดิมซ้ำได้ 5 frames/4 files ตรง inventory; R321 มี op=5 request สามครั้งแต่ v141 ตั้งใจไม่ตอบ จึงให้ negative ของ emulator เท่านั้น ไม่ใช่ original response.

[MEASURED][IMAGE A] ส่วน (ก) bag/UI:
- `ItemOperateVitalRes` vtable `0x00F30668` ผูก codec `0x005EDA20` และ handler `0x005EF5E0`; nominal ID `0x4C13`. Success shape ที่ client reader รองรับคือ version2, status/R4=0, bag-present=1, child เป็น plain `ItemBagAttr`, แล้ว affected tail.
- Handler `0x005EF5E0..0x005EF61A` ส่ง child/list/status เข้า app+0x590 `0x005A8A00` แล้วส่ง child/listเข้า app+0x4E0 `0x005C6D20`; ไม่มี actor identity หรือ CBuff record ใน handler body.
- สำหรับช่องมือขวาหลัก B1a/b พิสูจน์ widget `ITEM_RH_ONE` mask8 จึง `ItemAttr+0x39=N=3`; storage key `ItemAttr+0x34` ต้องเป็น record ที่มีจริงในช่วง regular `[200,230)`. Static ยังไม่พิสูจน์ allocation/replace policy ว่าต้องเลือก key ใด จึงห้าม hardcode `200+N`.
- RE-059 known answer แรกยืนยัน message layer 54 bytes ของ 0x4C13 version2/plain bag และ ItemAttr ทั่วไป แต่ `+0x39=0xFF`; มันพิสูจน์ grammar ไม่พิสูจน์ equip success.

[MEASURED][IMAGE A] ส่วน (ข) world appearance:
- RuntimeRes base codec `0x005F4070` รองรับ nested-vital collection; derived codec `0x005E3EE0` รองรับ actor collection. Handler `0x005E4060` reconcile actor collection ก่อน dispatch nested vitals จึงสองส่วนสามารถ co-pack ใน outer `0x6E9D` เดียว แต่ completion ของ model/resource อาจเกิดภายหลัง.
- Actor entry ต้องใช้ identity เดิมและ `AvatarAttr 0x16A0`; RH อยู่ `AvatarAttr+0x54`, mask bit `0x400`. Apply chain ไป actor+0x34C, dirty flag และ hand-resource loader ถูกพิสูจน์ใน B1c/g–l. Partial preservation ต้องมี cache basis; actor list omission อาจลบ actor อื่น จึงไม่ส่ง singleton roster โดยเดา.

[MEASURED][IMAGE A] ส่วน (ค) stats:
- `ItemOperateVitalRes` ไม่มี CBuff payload และ handler ไม่มี target-actor stat path. `CBuffVital 0x15E0` มี codec `0x00657390` และ handlerแยก `0x0064AD40` ที่ resolve target identity แล้วแก้ aggregate.
- B1n/o พบ item2200203 -> BUFF15211/ADD_HITRATE และสูตร secondary จาก property7/n_ITEMLV + property4*2; B1p ปิด wire ของ key4/7 แล้ว. อย่างไรก็ดี original equip-to-CBuff producer, secondary ที่ server เดิมเลือก, duration/serial/duplicate policy ยังไม่มีหลักฐาน จึงยังเป็น runtime control D ไม่ใช่คำตอบ original item-stat policy.

[MEASURED] ขอบเขต same/separate:
- คนละ payload/class และคนละ consumer แน่นอน.
- `AvatarAttr actor collection + ItemOperateVitalRes nested vital` อยู่ outer RuntimeRes เดียวกันได้แน่นอนจาก codec.
- nested collection รองรับหลาย vital จึงบรรจุ CBuffVital ร่วมได้ในเชิงโครงสร้าง; original ordering/co-packing/recipient policy ยัง UNKNOWN. การใช้ outer packet เดียวไม่ทำให้สาม operation กลายเป็น atomic transaction.

หลักฐาน IMAGE `[start,end)`:
- ItemOperate codec VA `0x005EDA20..0x005EDC31`, file `0x001ECE20`, SHA `b5f6a1586a810c0a98ceb7c925a0d4afa10cff41db661eb0947b8918f3a11d54`.
- ItemOperate handler VA `0x005EF5E0..0x005EF61A`, file `0x001EE9E0`, SHA `436b856fc41eb2d1f90b103bddaba29b621e21df99633c0f181a609224a9ff1d`.
- Runtime base codec VA `0x005F4070..0x005F4110`, file `0x001F3470`, SHA `27a079028e76685564ac37c0ff27c38996837970fe347e6be54474cf8c19c60a`.
- Runtime derived codec VA `0x005E3EE0..0x005E404E`, file `0x001E32E0`, SHA `ea5a21f39f095780b3f83fec2d465f3fe435f6b0ffc04a1e67107ffad489ea60`.
- Runtime handler order VA `0x005E4060..0x005E40E3`, file `0x001E3460`, SHA `500fcfdc89dcbe85d2d5dd1b14bed8f1f3fa63ab01cb90b534318ff775ce5251`.
- AvatarAttr codec VA `0x00464560..0x00464952`, file `0x00063960`, SHA `d9f565631b1e5afd35ceead1e230a8ecb38b55ffb007da587e0ce605e18a0b88`.
- CBuffVital codec VA `0x00657390..0x00657579`, file `0x00256790`, SHA `b1892118b8092ae450d78910b43ec01a7074d0967970b1661464ec0cce685373`.
All derive from `GameClient.local.bin` 14,759,424 bytes SHA256 `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`.

[BLOCKER / stop rule] Static B1 has reached its evidence ceiling. A stronger claim needs one of: (1) original-server equip session showing request op5 plus all server responses through stable post-equip state, or (2) attended GT-272 running the bounded composition and separately observing equipment widget, RH actor model, and stat source/aggregate. Another image-only round cannot prove original co-packing, storage-key allocation policy, or equip-to-CBuff emission. Per master anti-drowning rule, move to the next standing topic instead of repeating B1.

BUILD_PROPOSED: Run one staged GT-272 sequence with owner-only 0x4C13 bag update (`+0x34` chosen from actual free regular record, `+0x39=3`), appearance-preserving AvatarAttr RH update for the same identity, and a separately labelled CBuff control; record exact outer frames and three independent observations, then repeat after reconnect | GT-272 owner / LANE-B with CORE; LANE-K to bind | `GT272_UI_SLOT_PASS`, `GT272_RH_MODEL_PASS`, `GT272_STAT_SOURCE_PASS`, reconnect token; absence/failure recorded per component

nonclaims: no authentic original op5 response; no original storage-key allocator; no original same-frame/atomic policy; no original equip-to-CBuff producer or sword-stat values; no proof that a structurally accepted packet produces pixels; no native/server/client run this round; no persistence/reconnect/runtime promotion; no queue/lease/workflow/reference/ServerProject/Git mutation.
Artifacts: `pf_bridge/staged/standing_b1q_verify.py`, `standing_b1q_re059_recheck.log`. Stdlib verifier pins seven IMAGE spans and vtable binding, reproduces RE-059 known answer 1, and rejects a tag mutation.
SCOREBOARD: NONE | Standing B1 bounded static answer | runtime/original policy open
