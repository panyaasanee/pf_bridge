ถึง chief — ผล RE-157 UNANNOUNCED-ACTOR-SINK-GATES-TRADECMD-AND-MOBCOMBAT-001 (STATIC-ON-BRIDGE)

# RE-157 — DONE / PASS (static guard-point audit)

TICKET START: `2026-08-30T11:10:47.928+07:00`  
โหมด: static/read-only เท่านั้น; ไม่เปิดเกม ไม่บูต server/client ไม่ใช้ capture และไม่แก้ source

## คำตอบสั้น

ยืนยันช่องโหว่เชิง state ทั้งสองจุดจาก current committed source:

1. **TradeCmd**: guard ต้องอยู่ก่อน frozen v141 สร้าง cart/final-buy reply และต้องอ่าน **active store-session stamp** ที่ผูก `(scene_id, announced actor identity, census/session generation)` ไม่ใช่ boolean `shop_store5_open_sent` อย่างเดียว
2. **Mob combat**: guard ต้องอยู่หลัง target resolve เป็น field mob แต่ก่อน cadence/ledger mutation โดย require target อยู่ใน **exact actor-identity membership ที่ census ของ session+scene นั้นส่งจริง** ไม่ใช่เพียง static roster และไม่ใช่เทียบ placement index เพราะเลขเท่ากัน

สอง guard เป็นคนละ state machine; ห้ามใช้ ChooseNPC guard ของ RE-154 แทน

## Job 1 — TradeCmd guard: DONE

### สิ่งที่ current source ทำ

- state มีเพียง `shop_store5_open_sent: bool` ที่ `current/pf_login_game_server_v141.py:3533-3535`
- store-open ถูก queue เมื่อ exact ChooseNPC identity แปลงเป็น index ที่อยู่ใน `population_indices` และเป็น P91: `:4395-4411`, `:4433-4442`
- แต่ `TradeCmdVital` branch `:4128-4230` เริ่ม decode แล้วสร้างผลตอบโดยไม่อ่าน `shop_store5_open_sent`, current scene, chosen actor หรือ census membership
- cart ACK predicate อยู่ `:4134-4145`, queue reply `:4146-4165`
- final-buy predicate/sequence อยู่ `:4166-4201`
- close command `:4211-4223` เพิ่ม count แต่ไม่ clear `shop_store5_open_sent`; boolean จึงไม่ใช่ “active session” และข้าม scene/census replacement ได้

### จุด guard ที่ควรเพิ่ม

**จุดบังคับ fail-closed:** ก่อนเข้า `cart_add_valid` ที่ v141 `:4134` และก่อน `final_buy_sequence_valid` ที่ `:4173`; ใน runtime wrapper ที่ถือ selected scene จริง จุด interception ที่ปลอดภัยกว่าคือ **ก่อน** `actions = super().dispatch(parsed)` ที่ `src/pirateforce_foundation/runtime.py:6787` เมื่อ `nested_id == legacy.TRADE_CMD_VITAL` เพราะหลังเรียก `super()` frozen branch อาจ queue reply ไปแล้ว

guard ต้อง require record แบบ structured เช่น:

`ActiveStoreSession(scene_id, actor_identity, membership_generation/token)`

โดยมีเงื่อนไขครบ:

- record ถูก stamp เฉพาะตอน store-open frame ถูก queue จริงจาก announced P91 (`v141:4433-4442`)
- `record.scene_id == self.foundation.selected.position.scene_id`
- `record.actor_identity` อยู่ใน exact announced actor-identity set ของ census generation ที่ยัง active
- cart/final-buy sequence อยู่ภายใต้ record เดียวกัน
- clear เมื่อ close command, scene handoff, census replace/refuse หรือ session reset

runtime wrapper สามารถ stamp หลัง `super().dispatch()` เฉพาะเมื่อ action list มี exact store-open label และ source identity ผ่าน ChooseNPC membership แล้ว; แต่ incoming TradeCmd ต้อง validate ก่อนเรียก `super()` เสมอ

**อย่าใช้ `shop_store5_open_sent` เดี่ยว ๆ**: มันพิสูจน์เพียงว่า frame เคยถูก queue ครั้งหนึ่ง ไม่พิสูจน์ว่า store ยัง active, scene ยังเดิม หรือ actor ยังถูกประกาศใน census ที่ client ถืออยู่

## Job 2 — mob-combat guard: DONE

### สิ่งที่ current source ทำ

- `_dispatch_mob_combat` parse ActionVital แล้วดึง `target = field_qword_20`: `runtime.py:4028-4049`
- `_sync_combat_scene_state()` เลือก roster จาก `selected.position.scene_id`: `:4050-4061` (helper `:3966-4005`)
- membership ที่มีอยู่จริงก่อน cadence คือ `target_is_field_mob = any(mob.actor_identity == target for mob in roster)`: `:4093-4095`
- ถ้าเป็นสมาชิก static roster จะเดิน cadence ที่ `:4096-4110` แล้วเข้า `attack_from_observed_action`/ledger ที่ `:4111-4145`
- ไม่มี predicate ว่า actor identity นั้นอยู่ใน census bytes ที่ session นี้ได้รับจริง

### จุด guard ที่ควรเพิ่ม

**จุดบังคับ fail-closed:** หลัง `target_is_field_mob` ที่ `runtime.py:4093-4095` และก่อน cadence branch ที่ `:4096`:

```text
if target_is_field_mob and not announced_membership.admits(
    scene_id=current_selected_scene,
    actor_identity=target,
    active_generation=current_census_generation,
):
    return []
```

ตำแหน่งนี้รักษาพฤติกรรมเดิมของ non-field target (ไม่กิน cadence) และกัน state mutation ทุกชั้น: cadence, combat ledger, HP/bar/death frames

### membership ที่ต้องใช้

ต้องมี per-session record เช่น `AnnouncedActorMembership(scene_id, actor_identities, generation)` ซึ่ง set จาก **actor identities ที่ serialize ลง census จริง** และ update/clear แบบ atomic ที่ทุก successful census/handoff commit

- home census มี `generation.actor_identities` และ commit state แถว `runtime.py:7759-7799`
- bg0002 census มี `generation.actor_identities` แต่ source จงใจ **ไม่ตั้ง** `world_census_indices` (`:7369-7377`) เพราะ index semantics คนละตาราง
- lane census commit/stamp อยู่ `:7548-7610`
- handoff update/clear membership อยู่ `:7076-7105`

ดังนั้น `world_census_indices` เดี่ยว ๆ ใช้เป็น guard กลางไม่ได้: bg0002 ไม่ตั้งมันโดยตั้งใจ และการคำนวณ `target -> index` จากเลขที่ดูเท่ากันโดยไม่มี explicit crosswalk จะผิดกฎ evidence gate. ต้องเก็บ qword actor identities ที่ออก wire จริง

## Mandatory searches (ทำก่อน source audit)

### `pf_bridge/external/`

- ขอบเขต: recursive ทั้ง root, `130 files`, `37,060,029 bytes`
- manifest SHA-256: `3a665f1dce22530eddc177e85699faa22ab9abfaf444182269119345ddea624e`
- เจอ protocol/schema provenance:
  - `PF_PROTOCOL_REGISTRY.tsv:198` = `TradeCmdVital`
  - `PF_PROTOCOL_REGISTRY.tsv:496` = `ActionVital`
  - `PF_FIELD_VALIDATION.tsv:394-395` และ `:990-991`
  - serializer rows `PF_SERIALIZER_FIELDS.tsv:2551-2570` และ `:6543-6568`
- ไม่เจอ active-store latch, scene-stamped announced membership หรือ crosswalk ที่อนุญาตให้แทน runtime session state; external rows พิสูจน์ wire shape เท่านั้น

### `pf_bridge/gamedata/`

- ขอบเขต: recursive ทั้ง root, `1,109 files`, `15,319,585 bytes`
- manifest SHA-256: `9ba992357c2e6a7edbd366b996a801d3b354930babf695f35b615251bce3a3ab`
- exact recursive search ของ `TradeCmdVital|ActionVital|shop_store5_open_sent|population_indices|announced_actor|census membership` = **0 hit**
- gamedata มี roster/placement facts แต่ไม่มีหลักฐานว่า session ใดส่ง actor ใดออก wire; จึงใช้ static roster แทน announced membership ไม่ได้

## Input SHA-256

- `CLIENT_RE_QUEUE.md`: `ec77be09f2e352adbce102936a16be2a2fa09d800aeb5ffd498373c94faeba21`
- `NEW_ORDERS.txt` ณเริ่มใบ: `23baaba70c88c70093392264a6362e3c336e2d1584aca0f31f301f4354ca01d1`
- `AGENTS.md`: `085e33a261abbb9161a2f58b6ff686152d5893ff40dce038bd6e1520ff4465bf`
- `EVIDENCE_GATES.md`: `b39bf6cee61751ace859311dd33e6f8f0dfe260bd97b3ee571719bcc09bb1044`
- `current/pf_login_game_server_v141.py`: `2eb05ed2fdbdd5ee3d91f7fbb8c1d16a4c7a02a843bc97169b16a389e4ea4c22`
- `src/pirateforce_foundation/runtime.py`: `d590585619b13c34910a2a313b501de83ce3763a9e98d117e20092d20fe9d879`

## Nonclaims

1. ไม่อ้างว่าผู้เล่นปกติ trigger ช่องนี้; เป็น forged/desync risk ตาม RE-154
2. ไม่อ้างว่า client แสดงผลหรือยอมรับ replies; ใบนี้ไม่เปิดเกม
3. ไม่อ้างว่า static roster membership เท่ากับ announced membership
4. ไม่จับคู่ actor qword กับ placement index เพราะตัวเลขดูเท่ากัน; guard ต้องได้ explicit identity set จาก census serialization
5. ไม่อ้างว่า `shop_store5_open_sent` คือ active session
6. ไม่อ้างว่า ChooseNPC scene guard ปิด TradeCmd/ActionVital แล้ว; dispatch คนละ branch และ state คนละชุด

## BUILD_IMPACT

`BUILD_IMPACT: ANALYSIS-ONLY / TWO SOURCE GUARDS REQUIRED, NO SOURCE CHANGE IN THIS TICKET.`

- Trade: เพิ่ม runtime-owned active-store session stamp + pre-`super().dispatch` fail-closed guard; clear ทุก close/scene/census transition
- Combat: เพิ่ม scene+generation-stamped exact announced actor-identity membership; gate field-mob target ที่ `runtime.py:4096` ก่อน cadence/ledger

การแก้ควรอยู่ใน owning lane/runtime seam ตาม chief workflow; อย่าแก้ pinned v141 หรือ hard-code actor/index จาก equality

## Closeout input drift

หลังปิด jobs มี background sync เพิ่ม `external/pf_build_v5_manifest.py` เวลา `11:13:35+07:00` (SHA-256 `d70e3fc5f853f6bb3286d5e71a7209f5e150ce3e71674b6a7848658418e8f82e`). ค้นเฉพาะ delta แล้วไม่มี `TradeCmdVital/ActionVital/shop_store5/population_indices/announced_actor/census membership`; guard points ไม่เปลี่ยน. Final external root = `131 files`, `37,138,668 bytes`, manifest `4368a319d5b4a48c4ce6d62ac03a29630598e27b87d5f167e1b397870bf00478`
