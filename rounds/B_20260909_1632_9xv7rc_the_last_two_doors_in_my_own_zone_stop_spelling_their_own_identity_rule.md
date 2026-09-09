round 9xv7rc
start 2026-09-09T16:32+07:00
claim

# LANE-B round 9xv7rc

HEAD ที่บูต: `pirate-force-server` origin/main `2e28496` · `pf_bridge` origin/main `422f737`
เลขจ็อบ: ไม่ได้ใช้ (ไม่ใช่ใบ attended)
เวลาเทียบ heartbeat: `_BRIDGE_HEARTBEAT.txt` ล่าสุด `2026-09-09T16:20:02+07:00` · เวลาผม `16:32` · ห่าง 12 นาที ไม่ค้าง

## ล็อกรอบ
list `[LANE-B] round *: claim` ที่เปิดอยู่ = **ไม่มี** (ใบ LANE-B ที่เปิดค้างทั้งห้าใบเป็น `addendum` ไม่ใช่ claim)
⇒ เปิด claim เอง `pf_bridge#1999` · ไม่ใช่ takeover

## รอบนี้ทำอะไร (`pirate-force-server#____` · `claude/nice-meitner-9xv7rc` · sha `f828239`)

งานตามลำดับที่ COO เคาะ: `COO-DECISION 20260909_1312` ข้อ 1-3 (= `PANYA-ORDER 20260908_1545` ข้อ 2.1/2.2/2.5)
**"หนึ่งฟังก์ชัน หนึ่งกติกา หนึ่งที่" ก่อนแตะตัวจ่าย** — รอบก่อน (`k1hsp0`) ปิดสตริง wiring ไปแล้ว
รอบนี้ปิดสองประตูสุดท้ายที่ยังเขียนกติกาช่วง identity เอง **ในเขตของผม**

### 1. `mob_aggro.py` — สี่จุดที่เขียน `identity <= 0` เอง → `_require_player_identity`
ฟังก์ชันใหม่เรียก `mob_identity_sign.is_player_identity` จุดที่แก้:
`PlayerObservation.identity` · แถวในตาราง threat · `MobAiState.target_identity` · `apply_damage_threat(attacker_identity)`

**ทั้งสี่จุดเป็นฝั่งผู้เล่นจริง ๆ และยังต้องเป็นบวกต่อไป** — ไม่ได้เปลี่ยนพฤติกรรม
ที่เปลี่ยนคือ **รั้วบอกเองว่ายืนอยู่ฝั่งไหน** เมื่อก่อน `<= 0` สองความหมาย ("ผู้เล่นเท่านั้น" กับ
"ไม่ใช่ actor จริง") สะกดเหมือนกันเป๊ะ วันที่ band พลิกเป็นลบ มันจะแปลตรงข้ามกัน และคนอ่านต้อง
เดาทีละประตู · `.reason` ของทุก refusal คงสตริงเดิมทุกตัว (`REFUSE_IDENTITY_NOT_POSITIVE`,
`REFUSE_STATE_MALFORMED`) เพื่อไม่ให้ caller/เทสที่อ่าน `.reason` เปลี่ยน

### 2. `mob_combat_bg0015_gates.py` — ประตูนี้ถือ identity ของ **มอน** ไม่ใช่ผู้เล่น
`splice_identities_missing_from` รับแถวจาก census ฉาก 14 ของสาย A แล้วปฏิเสธ `identity <= 0`
วันที่ตัวจ่ายพลิก **มันจะทิ้งทุก placement ที่ A ส่งมา แล้วรายงานว่า "ขาดครบสิบสอง"**
— cross-check ที่ตอบว่า census ว่างไม่ว่า census จะมีอะไร แย่กว่าไม่มี cross-check เพราะมัน
อ่านเหมือนผลวัด · เปลี่ยนเป็น `mob_identity_sign.is_targetable_identity`
(คง `type(...) is not int` ไว้เองเพื่อกัน `True` ที่ isinstance มองเป็น 1)

### 3. `tests/test_mob_identity_band_end_to_end.py` (ใหม่) — ข้อ 2.5 ของเจ้าของ "สี่ขาในใบเดียว"
มอนตัวเดียว identity `-16773184` (เอาจากตัวจ่ายจริง `mob_wire_identity(1, 0)` ไม่ได้พิมพ์เลขเอง)

| ขา | ประตู | ผล |
|---|---|---|
| ลงทะเบียนโลก | `world_scene_registry.MobVital` | 🔴 `ValueError: actor identity out of range` (ไฟล์ของ A ห้ามแตะ) |
| จดเลือด | `mob_combat.MobBalance` / `CombatLedger` | ✅ |
| ผูกของดรอป | `mob_loot.GroundDrop` | ✅ |
| เข้าทะเบียนศพ | `mob_death.DeathRegister.with_death` | ✅ |

สามขาที่เปิด **ผ่านด้วยเลขตัวเดียวกัน** (ข้อ 3 "id เดียวตลอดวงจร") — เคส
`test_the_three_open_doors_agree_on_ONE_number`
ขาที่ปิด **ปักตามสภาพจริง ไม่ skip ไม่ xfail** (`2050` ห้ามทั้งสาม) และเขียน "ประโยคที่ต้องกลับด้าน"
ไว้ในตัวเคสเอง + เคส `test_the_four_in_one_is_not_green_yet` ที่ถือรายชื่อประตูที่ยังปิด
⇒ **วันที่ A แก้ `_require_identity` สองเคสนี้จะแดงทันที** และการแก้คือกลับด้านตามที่เขียนไว้
เทสที่แดงตอน blocker ถูก "ถอดออก" คือรูปที่ทำให้ลืม blocker ไม่ได้ นี่คือเหตุผลที่มันไม่ใช่คอมเมนต์

### 4. `mob_identity_sign.py` — docstring อย่างเดียว
"the four agreed" → "the THREE agreed" (หนี้ที่ adversary รอบ `k1hsp0` ชี้ไว้แบบไม่บล็อก
= ข้อ 2 ของ "รอบหน้าทำอะไร" รอบก่อน จ่ายแล้ว)

### 5. หนี้ marker ของสายตัวเอง (`COO-BLOCKER-SWEEP 20260908_2141` ข้อ 2) — **จ่ายครบ 5 ใบ**
ใบ addendum ของ LANE-B ที่เปิดค้างโดยไม่มี marker เลย เก่าสุดตั้งแต่ 6 ก.ย.:
`#1493` · `#1644` · `#1768` · `#1823` · `#1860` — เติม `PF-AUTOMERGE: v4` ให้ครบทั้งห้าใบรอบนี้
พร้อมย่อหน้าอธิบายว่าใครเติมและทำไม · ทุกใบเป็น "หนึ่งไฟล์ ไม่มีโค้ด" ในรีโปสะพานอย่างเดียว
🔴 ข้อความเดิมในสามใบที่เขียนว่า "PR ฝั่งเซิร์ฟเวอร์ใบนั้นไม่มี/ถอด marker" **ยังคงเดิม** —
เป็นคนละใบคนละรีโป marker นี้ไม่ได้คืน marker ให้ `#922`/`#1059`/`#996`/`#1089`/`#1112`

## ขยับ NOW/M ข้อไหน
- **`1545` / `1312` ข้อ 1-2 (กติกาช่วง identity ตัวเดียว)**: รันโทเคนของ COO จริง
  `git grep -n "0xFFFFFFFF\b\|<= 0\|<=0" src/pirateforce_foundation/mob_*.py`
  **ยังเหลือสี่บรรทัด และผมไม่แก้ทั้งสี่ — เขียนเหตุผลไว้ทีละบรรทัดตามข้อ 2.2**
  ("จุดที่แก้ไม่ได้จริงต้องเขียนเหตุผลลงใบ ห้ามเงียบ") ดู "ที่ตั้งใจไม่แตะ"
- **ข้อ 2.5 (เทสสี่ขา)**: เขียว 3/4 · ขาที่ 4 เป็นไฟล์ของ A
- **ข้อ 6 = จ.3 (พลิก `field_mobs.actor_identity`)**: **ยังทำไม่ได้** ตามลำดับที่เคาะ — เขียนจดหมาย
  `20260909_1649_LANE-B-ASK-COO-one-door-left-before-the-allocator-can-flip.md` (ADDRESSEE: COO)
  เสนอสามทาง แล้วเดินต่อด้วยทางที่ 3 (คงลำดับเดิม) ไม่หยุดรอ
- **จ.2 (พลิกทีละฉาก)**: ยังค้าง — `#1181` (ประตูทะเบียน A) **ยัง draft ไม่ merge** ตรวจเองผ่าน API
  ไม่ใช่จาก NOW
- **M3/M4**: ไม่ขยับบนจอรอบนี้ — งานนี้เป็นการถอดกำแพงที่จะทำให้ M3/M4 พังเงียบวันที่ band พลิก

## ที่ตั้งใจไม่แตะ (ไม่ใช่ลืม)
- `world_scene_registry.py:187` `_require_identity` — ของ A · `COO-DECISION 1312` ข้อ 1 สั่งห้ามผมแตะ
- `mob_ai_player_damage.py:249` (`actor <= 0`, เป็น identity ของ **มอน** จริง) — NOW เขียนว่า
  "กำแพงสอง = ของคุณ **หลังประตูลง**" ประตูยังไม่ลง จึงไม่แตะรอบนี้ · **นี่คือกำแพงถัดไปที่ต้องล้ม
  ก่อน จ.3 และมันอยู่ในเขตผมแล้ว** — รอสัญญาณเดียวคือ `#1181` ลง main
- `mob_ai_player_damage.py:285` และ `mob_hit_frame.py:405` (`character_id <= 0`) — **ไม่ใช่
  actor identity**: เป็นเลขตัวละครฝั่งฐานข้อมูล (ใช้เปิด `store` อ่าน vitals) คนละปริภูมิกับเลขบนสาย
  ถ้าลากมาผ่าน `is_player_identity` เท่ากับผูกกุญแจ DB เข้ากับกติกาเครื่องหมายของสาย ซึ่งผิด
  (ชื่อ refusal ของมันบังเอิญชื่อ `REFUSE_IDENTITY_NOT_POSITIVE` เท่านั้น)
- `mob_viewer_link.py:186` (`viewer_identity <= 0`) — **ค่าที่ยังไม่ decode**: คอมเมนต์เหนือ
  `LINKED_IDENTITY_CEILING = (1 << 64) - 1` เขียนเองว่า "an unsigned qword is what the wire
  carries" ⇒ ประตูนี้รับค่าดิบจากสาย ไม่ใช่ค่าที่ผ่าน `decode_wire_identity` แล้ว
  การเอา predicate ฝั่ง **signed** ไปครอบตรงนี้คือความผิดพลาดตัวเดียวกับที่ docstring ของ
  `mob_combat._require_identity` เตือนไว้ (ค่าดิบ `18446744073709551614` ของมอนที่จริง ๆ คือ `-2`)
  ⇒ ประตูนี้ต้อง `decode_wire_identity` ก่อน แล้วค่อยถาม predicate — เป็นงานคนละชิ้น ไม่ยัดรอบนี้
- `gm/teleport_wire.py` · `gm/name_color_gate.py` — ตาราง `1545` วัดแล้วว่าสองแถวนี้ผ่านอยู่แล้ว
  (`0 … 64 บิต`) และเป็นเขตสาย GM
- `lifecycle.py:252` · `action_ack.py:114` · `columbus_quest_dispatch.py` — นอก `mob_*` และเป็น
  กติกาฝั่ง **ผู้เล่น** · `lifecycle.py` เขียนเหตุผลไว้ในตัวแล้วว่าทำไมต้องเป็นบวก (ผู้บริโภค
  identity ผู้เล่นทุกตัววันนี้ต้องการค่าบวก) ไม่ใช่กติกาที่ band ของมอนจะชน

## ADVERSARY
สั่ง `pf-adversary` ระหว่างรอบบนกิ่ง `claude/nice-meitner-9xv7rc`
__ADVERSARY_STATUS__

## เทส
- targeted: `tests/test_mob_aggro.py` + `tests/test_mob_combat_bg0015_gates.py` = **84 passed / 58 subtests**
- ใบใหม่: `tests/test_mob_identity_band_end_to_end.py` = **10 passed**
- ชุดเต็มบนต้นไม้สุดท้าย (หลัง `git merge origin/main` = Already up to date): **15766 passed / 450 skipped / 0 failed / 43470 subtests passed** (1055 s)
- `python3 tools_bridge/pf_gate_preflight.py --repo ../pirate-force-server` = **PREFLIGHT PASS**

## nonclaims
- ไม่ได้แตะ `field_mobs.FieldMob.actor_identity` — ยังเป็น `0x2000 + placement_index + 1`
  (นี่คือจุดเดียวที่ต้องย้อนถ้าไคลเอนต์คลิก actor ค่าลบไม่โดน)
- **ไม่มีหลักฐานชั้นจอ**ว่า identity ไม่เป็นบวกแล้วยังคลิกเลือกเป้าได้/ตีโดน/ตายเป็นศพ/ดรอปได้
  — เจ้าของไม่เคาะใบ attended เรื่องนี้ (`1545` ข้อ 3) จึงไม่ตั้งใบ และไม่อ้างว่ารู้
- ไม่ได้อ้างว่าข้อ 2.5 เขียวครบสี่ขา (3 เขียว 1 ปักตามสภาพจริง)
- ไม่ได้ยืนยันว่า `f828239` อยู่บน main (ยังไม่ merge) — รอบหน้ายืนยันด้วย
  `git merge-base --is-ancestor`
- ไม่ได้ตรวจว่าห้าใบ addendum ที่เติม marker จะผ่านเกตจริง — ส่งมอบให้ reaper แล้วคือจบหน้าที่
- ไม่ได้บริโภคจดหมายที่จ่าหน้าถึง LANE-B ที่ค้างอยู่ **23 ใบ** (ดูหัวข้อถัดไป)

## หนี้ที่ยกให้รอบหน้าอย่างเปิดเผย
🔴 กล่องจดหมาย LANE-B มีใบที่ยังไม่ถูกบริโภค **23 ใบ** (เก่าสุด `20260908_1048`) ส่วนใหญ่เป็น
`STANDING-A*/C/D-RESULT-*` จาก Codex RE ที่เข้ามารัวในวันเดียว บวก `RE-321-RESULT` (8 เส้น `.avt`)
และ `20260909_1533_STANDING-A1-BLOCKER-NO-CANONICAL-REGISTER-RMW` ที่เป็น **BLOCKER**
รอบนี้ไม่แตะเพราะไม่เกี่ยวกับกติกาช่วง identity และ `1846`/`COMMON_LANE_ROUND` ห้ามให้กระดาษ
กินทั้งรอบ — **แต่กองนี้โตเร็วกว่าที่สายจะบริโภคทัน และควรถึงตา COO**

## รอบหน้าทำอะไร
1. **บริโภคกล่องจดหมาย 23 ใบ** เริ่มที่ `1533 STANDING-A1-BLOCKER` (BLOCKER) แล้ว `RE-321`
   (NOW สั่งไว้แล้ว: "re-body `.avt` 8 เส้น → K") — ทำเป็นงานแรก ไม่ให้เกิน 30 นาทีของรอบ
2. เช็ค `#1181` ลง main หรือยัง — **ลงแล้ว ⇒ ล้มกำแพงสอง `mob_ai_player_damage.py:249` ทันที**
   (อยู่ในเขตผม รอแค่สัญญาณ) แล้วต่อ จ.2
3. ถ้า COO ตอบจดหมาย `1649` ว่าให้เร่งประตูของ A ⇒ กลับด้านสองเคสใน
   `test_mob_identity_band_end_to_end.py` พร้อมกันในคอมมิตเดียว แล้วพลิกตัวจ่าย (จ.3)
4. 🔴 `mob_viewer_link.py:186` — ใส่ `decode_wire_identity` ก่อนประตู แล้วค่อยถาม predicate
   (รอบนี้เจอแล้วแต่ไม่ยัดเข้ามา: ค่าดิบ `18446744073709551614` = มอน `-2` จะผ่านประตูนี้ฉลุย
   วันที่ band พลิก) — เป็นเขตผม ทำได้ทันทีไม่ต้องรอใคร
5. ถ้ายังติดทั้งสอง ⇒ root cause ของ `GT-223` (`mob_death_persistence.py` / `mob_drop_presence.py`)
   ซึ่งรอบ `k1hsp0` ชี้ไว้แล้วว่าเป็นต้นตอจริง และเป็น "หาง P-1" ใน NOW

SCOREBOARD: STUCK | ถอดกำแพงสองบานสุดท้ายในเขตตัวเองที่จะทิ้งมอนทั้งฉากเงียบ ๆ วันที่เลขประจำตัวมอนพลิกเป็นค่าลบ — ผู้เล่นยังไม่เห็นอะไรต่างวันนี้ เพราะตัวจ่ายยังไม่พลิก และประตูสุดท้ายที่ขวางอยู่เป็นไฟล์ของสาย A ที่สายนี้ถูกสั่งห้ามแตะ | pirate-force-server#____ - sha f828239 - 84 passed targeted + 10 passed (four-in-one) + 15766 passed/450 skipped/0 failed (full suite) - จดหมาย notes_to_chief/20260909_1649_LANE-B-ASK-COO-one-door-left-before-the-allocator-can-flip.md
