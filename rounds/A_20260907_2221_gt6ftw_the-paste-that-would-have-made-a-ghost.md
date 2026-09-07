# LANE-A รอบ `gt6ftw` — จุดเสียบที่ใบขอของเราเองสั่งไว้ จะสร้างผีในฉากที่ผู้เล่นเพิ่งออกมา (จ่ายแล้ว)

รหัสรอบ `gt6ftw` · เริ่ม 2026-09-07T22:21+07:00 · claim `pf_bridge#1800`
(ตอนล็อก: `[LANE-A] round ... claim` open = **0 ใบ** · คุมด้วยรายการ open ทั้งหมด 16 ใบ ซึ่งมี `[LANE-K]`/`[LANE-GM]`/`[LANE-DB]` claim สดอยู่ = พิสูจน์ว่า list ทำงานจริง ไม่ใช่คืนว่างเปล่า)
กิ่ง: `pf_bridge/claude/wonderful-goodall-gt6ftw` · `pirate-force-server/claude/nice-ramanujan-gt6ftw`
🔴 **พึ่งกิ่งที่ยังไม่ merge**: ตัดจาก `origin/claude/dreamy-archimedes-q6a8oa` (PR `pirate-force-server#1075`, marker ถูกถอนเองในรอบก่อน) ไม่ได้ตัดจาก main — โมดูลของรอบก่อนยังไม่อยู่บน main (`git merge-base --is-ancestor b558cad origin/main` = ไม่ผ่าน)

## รอบนี้ขยับ NOW/M ข้อไหน
- **`NOW.md` บรรทัด LANE-A ข้อ `2050`** ("แก้ 8 เทส logout ที่ไม่เคยรัน + คอมเมนต์ `:7569` ≤30 นาที 2 รอบ") — **รอบ 1 จาก 2: ข้อ 1 ปิด · ข้อ 2 ปิดครึ่งที่เป็นความจริง เหลือครึ่งที่เป็นลำดับ**
- **หนี้ `pf-adversary` รอบ `q6a8oa` (D1-D10)** — จ่ายครบเก้าข้อในกิ่งใหม่ ตามที่ ADDENDUM ของรอบก่อนสั่งไว้เป็นงานแรก
- **`PANYA 0039` โลกใบเดียว** — ประตูที่จะทำให้ "ผู้เล่นเห็นผู้เล่น" ตอนนี้ลงฉากถูกแล้วบนเส้นล็อกอินทุกเส้น (เดิมลงผิดฉากบนเส้น GM override)
- ไม่ขยับ: **M2** (ไม่ได้แตะรอบนี้ · `RE-303` เพิ่ง `OPEN` ยังไม่มีผลกลับ · `GT-304` ยังตกรถโดยที่ผมไม่แตะโทเคน) · P-2/M4 (ไม่ใช่เขตนี้)

## สิ่งที่ผู้เล่นจะเห็นต่างจากเมื่อวาน — พูดตรง ๆ
**บนจอยังไม่ต่าง และผมไม่อ้างว่าต่าง** — จุดเสียบยังอยู่ในมือ chief
สิ่งที่ต่างคือ: เมื่อวานใบขอของสายนี้ ถ้า chief แปะตามตัวอักษร **ผู้เล่นที่ล็อกอินผ่าน GM login-scene override จะกลายเป็นแถวผีในฉากที่เขาออกมา และมองไม่เห็นเลยในฉากที่เขายืนอยู่จริง**
วันนี้ใบขอชี้จุดที่ถูก และประตูรับ `entry` มาเองเพื่อไม่ให้ตำแหน่งกับฉากหลุดจากกันได้อีก **แม้จุดเสียบจะขยับอีก**

## ของที่ทำ

### 1. หนี้ adversary D1 (HIGH) — ตำแหน่งไหนคือ "ของจริง" สำหรับแถว presence
**คำตัดสินของสาย (ผมเคาะเอง ไม่รอ)**: **`entry.position` ชนะขาด รวมทั้งฉาก**
เหตุผลไม่ใช่รสนิยม: แถว presence ถูกอ่านเพื่อบอก *ผู้เล่นคนอื่น* ว่าใครยืนตรงไหน ⇒ ต้องเป็นจุดที่ไคลเอนต์ของคนนั้น**ถูกส่งไปจริง**
และคอมเมนต์ของ chief เองที่ `runtime.py:9412` เรียก `entry.position` ว่า *"the ONE resolved position"*
- ใหม่: `presence_position_for_login(selected, entry)` → `PresencePosition(scene_id, x, y, z, source)` + `PRESENCE_POSITION_SOURCE_ROW` / `_RESOLVED_ENTRY`
- ใหม่: `register_presence_for_login(selected, entry)` = ประตูของจุดเสียบ (1)
- `register_presence_for_character(..., entry=..., position=...)` — `entry` ตัดสินฉาก · `position=` ทับเฉพาะ x/y/z (จุดเสียบ (2))
- **เทสที่ปักคือการวัดของ adversary ซ้ำ**: แถวบอกฉาก 1 · `resolve_entry` จริงคืนฉาก 2 (และ **relocate** ไปจุด spawn ที่พินไว้ = พิสูจน์ว่าประตูเอาจุดที่ resolve แล้ว ไม่ใช่จุดที่ขอ) ⇒ คนดูในฉาก 2 เห็น `(4242,)` · ฉาก 1 เห็น 0
- **และปักบั๊กไว้เป็นบั๊ก**: `test_without_the_entry_the_same_login_lands_in_the_wrong_scene` — วันที่อาร์กิวเมนต์ `entry` เลิกทำงาน เทสนี้จะชนกับเทสข้างบน

### 2. หนี้ D3 (MEDIUM) — ยามอ่านสองค่า แต่กฎที่ผม cite พูดสามค่า
`legacy_bridge.start_game:103` ใช้ `level is not None and hp_current is not None and hp_max is not None` — **นั่นคือกฎ ไม่ใช่ที่ผมเขียนใหม่**
`hp_pair_for_character` ตอนนี้สะท้อน predicate เดียวกันเป๊ะ: ครบสาม = ใช้ค่าแถว · ไม่มีเลยสักค่า = ค่าคงที่ `player_wire` · **อย่างอื่นปฏิเสธโดยมีชื่อ** (`PRESENCE_REFUSED_LOGIN_VITALS_PARTIAL`)
เทส `test_the_door_and_legacy_bridge_agree_on_every_vitals_shape` เดิน cross-product ทั้ง 8 รูป เทียบกับสิ่งที่สายส่งจริง ไม่ใช่เทียบคำพูด

### 3. หนี้ D2 (HIGH) — เทสกันค่าคงที่ hardcode ที่ **ล้มไม่ได้**
เดิมเทสเกรปหาชื่อค่าคงที่ใน **ซอร์ส** ⇒ เปลี่ยนเป็น `100, 100` ก็ยังเขียว (ชื่อยังอยู่ใน docstring)
ตอนนี้ patch `player_wire.PLAYER_LOGIN_HP_CURRENT/_HP_MAX` เป็น **37/91** แล้วดูว่าประตูขยับตาม — และนั่น**ปิด D8 ไปด้วย** (ค่าคงที่จริงเป็น 100 ทั้งคู่ การสลับ current/max จึงรอดทุกเทสเดิม · มิวแทนต์สลับตอนนี้ตาย)

### 4. หนี้ D5 (MEDIUM) — คำปฏิเสธที่เงียบสนิท
`LANE_A_PRESENCE_REFUSED <reason> scene=<n> character=<id>` — ASCII เสมอ ผ่าน `_ascii_token` (คอนโซลสะพาน cp874)
- เทสยิงคำปฏิเสธ **เจ็ดรูป** แล้วเช็คว่าพิมพ์ทุกรูป · เขียนลงสำเร็จ = **ไม่พิมพ์อะไรเลย**
- ชื่อไทยล้วน + stdout ที่ระเบิด = ทั้งสองรูปไม่ทำให้ล็อกอินตาย (`test_a_broken_stdout_does_not_take_the_login_down`)

### 5. หนี้ D4 / D6 / D9 — ข้อความใบขอที่พูดเกิน (`PLAYER_PRESENCE_WIRING` revision 2)
- ตัดประโยค *"none of these pastes reads a field"* (paste (3) อ่าน `.id`) และ *"the three doors ... do the HP pair read themselves"* (`register_player_presence` ไม่อ่าน HP เลย)
- **D6 พูดออกมาตรง ๆ**: paste (2) ครอบ **ไม่ทั้งหมด** ของการเดิน — `_vital_walk_promote_target_pos` คืน `"v141_reads_this_frame_itself"` ก่อนถึงบรรทัดนั้นสำหรับ TargetPos ธรรมดา ⇒ ครอบเฉพาะเฟรมที่พ่วงคลิกเก็บของ · จะครอบการเดินปกติต้องมีผู้เขียนคนที่สองในเส้นของ v141 = ไฟล์ chief ใบนี้ไม่คิดแทน
- **D9**: `"NEVER RAISES"` → ขอบเขตที่จริง (`model.Character` เป็น frozen dataclass ไม่มีรูปที่ raise · stand-in ที่ `__getattr__` ระเบิดยัง raise ได้ และนั่นคือ caller ที่พัง ไม่ใช่แถวที่เสีย)
- **D7/D10**: ถอดเงื่อนไขย่อยที่ตายแล้วสามตัว (`or type(value) is bool` ×2 · `where is None or`) แล้วปักเทสให้ยามที่เหลือรับน้ำหนัก · เพดาน `PRESENCE_HP_CEILING` ปฏิเสธโดยมีชื่อ + เทสเทียบกับ `world_scene_registry._MAX_HP` (พินไม่ให้ค่าที่ copy มา drift)

### 6. `COO-ORDER 20260907_2050` — **ผมวัดเองก่อนแก้ทั้งสองข้อ ตามที่ COO สั่ง**
**ข้อ 1 (เทส logout 8 ใบ) — ปิดรอบนี้**
วัดเอง: หลังล็อกอินครบใน `_logged_in_state` → `runtime_ack_sent = False` · `transport_socket_closer = None` ⇒ **คำวัดของ adversary UI ถูก**
`TheGuardsRunInTheShapeProductionActuallyHas` รันยามเดิมในรูป production (ล็อกอิน + poll runtime-protocol ที่ v141:3768 ใช้ตั้ง ack + closer ต่อแล้ว)
มิวแทนต์อยู่ **ในใบเดียวกัน**: `_state_class_from_mutated_runtime` อ่านซอร์ส `runtime.py` ถอดยาม `... and self.foundation.selected is None` แล้ว exec เป็นโมดูลของตัวเองใน package จริง (ไม่เขียนทับไฟล์จริง) ⇒ assertion เดิม **แดง**
🔴 **คุมมิวแทนต์เอง**: ลองทำให้การแทนที่เป็น no-op → เทสมิวแทนต์ **fail** ⇒ มันเกรดการกลายพันธุ์จริง ไม่ใช่เกรดอากาศ
`LOGOUT_WIRING_TESTS: production-shaped mutant_red=yes`
`git grep -n "attach_transport_socket_closer" -- tests/test_world_logout_button_notice_wiring.py` → 1 แถว (`state.attach_transport_socket_closer(lambda: self.closed.append(True))`)

**ข้อ 2 (คอมเมนต์ `:7569`) — เลือกทาง (ข) รอบนี้ ทาง (ก) เป็นงานแรกของรอบ 2**
วัดเอง: session รูป production + `logout_acknowledged = True` บนเส้น **flagless** → **`LANE_A_UIA_NOTICE_COMPOSED` พิมพ์ · actions = 0** (เฟรมถูกทิ้งที่ยาม `logout_hypothesis_scenario is None and self.logout_acknowledged`) ⇒ คอมเมนต์เดิม**เท็จ**
- แก้คอมเมนต์ให้ตรงความจริง + เขียน nonclaim ลงไปในนั้น (คอมเมนต์อย่างเดียว **ไม่แตะพฤติกรรม** — `git diff` ของ `runtime.py` รอบนี้เป็นคอมเมนต์ล้วน)
- **ปักการวัดเป็นเทส** `test_the_flagless_post_ack_boot_still_says_composed_and_sends_nothing` — บั๊กที่ปักไว้เป็นบั๊ก **วันที่ทาง (ก) ลง เทสนี้จะแดงและรอบนั้นต้องพลิกมัน** (นั่นคือเหตุผลที่ปัก: คำอ้างจะ stale เงียบ ๆ ไม่ได้ทั้งสองทิศ)
🔵 ทำไมไม่ทำทาง (ก) รอบนี้: มันเป็นการเปลี่ยนลำดับบน dispatch path ⇒ ตามกฎ draft (`NOW.md 1849` / COMMON) PR ทั้งใบต้องเป็น draft และงานหลักของรอบ (หนี้ adversary) จะค้างตามไปด้วย · คำสั่งให้เวลา 2 รอบ ผมใช้รอบที่สอง

## ADVERSARY
สั่ง `pf-adversary` บนกิ่ง `claude/nice-ramanujan-gt6ftw` **ทันทีที่คอมมิตซอร์สแรกลง** พร้อมห้าคำอ้างเป็นเป้า (ทั้งห้าเป็นข้อที่รอบนี้อ้างว่า "จ่ายแล้ว")
สถานะตอนเขียนไฟล์นี้: **ผลยังไม่คืน** ⇒ `ADVERSARY_PENDING pirate-force-server#1082` (กิ่ง `claude/nice-ramanujan-gt6ftw`)
🔴 **ไม่มีที่ไหนในรอบนี้เขียนว่า "ผ่าน adversary"** · รอบถัดไปของสายนี้จ่ายผลก้อนนี้ในกิ่งใหม่เป็นงานแรก
ระหว่างรอ self-review ของผมเอง (ไม่ใช่คำอ้างว่าผ่าน):
- อ่านทุก hunk ใน `git diff --cached` ก่อน commit ทั้งสามครั้ง
- **มิวแทนต์ยามใน `hp_pair_for_character` 11 ตัว (แต่ละ `if` → `if False:`) = ตายทั้ง 11** (0 survivors)
- มิวแทนต์เจาะจงหกตัวสำหรับหกข้อของ adversary (สลับค่าคงที่ · hardcode 100/100 · ทิ้ง `entry` · ฉากมาจากแถวแทน entry · ถอดเสียงปฏิเสธ · ยกเพดานเงียบ ๆ) = **ตายทั้งหก**

## `TWO_SESSIONS_SAME_SCENE:`
ประตูไม่ถือ state ของตัวเอง เขียนลง `world_scene_registry` (สมุดต่อฉาก แชร์ทุก session ในโปรเซส) เหมือนเดิม
สิ่งที่รอบนี้เปลี่ยนคือ **สอง session ที่อยู่ฉากเดียวกันจริง ๆ จะถูกนับว่าอยู่ฉากเดียวกัน** บนเส้น GM override ด้วย — เดิมคนที่ล็อกอินผ่าน override จะไปนั่งอยู่คนละหน้าของสมุด
last-writer-wins ตาม `note_balance` เหมือนเดิม ไม่ได้คิดใหม่

## `NO_FEATURE_WAITING:`
ไม่มีผล RE/GT ใหม่กลับมาถึงสายนี้ในรอบนี้ (`RE-303` เพิ่ง `OPEN` · `GT-304` ยังตกรถ)
จดหมายสามฉบับที่จ่าหน้าถึง LANE-A **บริโภคครบในรอบนี้** พร้อม `.CONSUMED.txt` และสำเนาใน `consumed/`

## วัดเองรอบนี้
- `tests/test_world_remote_player_actor.py`: **65 passed, 41 subtests**
- `tests/test_world_logout_button_notice_wiring.py`: **27 passed**
- ชุดเต็มบนต้นไม้ที่ `git merge origin/main` แล้วเป็นคอมมิตสุดท้ายจริง: **13897 passed, 432 skipped, 0 failed, 37892 subtests passed** ใน 579.91 s (`EXIT=0`) · คอมมิตสุดท้ายจริง `617e1fb`
- `pf_gate_preflight.py --repo pirate-force-server`: **PREFLIGHT PASS**
- non-ascii ในไฟล์ที่แตะ: **0 ไบต์ทั้งสามไฟล์** (`runtime.py` รวมด้วย — ร่างแรกของคอมเมนต์มี emoji 4 ไบต์ จับได้ก่อน commit)
- ไม่ได้เพิ่ม/ลบ/ย้าย skip · ไม่ได้เพิ่มไฟล์เทสใหม่ · ไม่แตะ `app.py` / v141 / `.claude/` / canonical DB · ไม่แตะเขตสายอื่น
- 🔴 **แตะ `runtime.py` จริง แต่เป็นคอมเมนต์ล้วน** ภายใต้ `COO-ORDER 2050` + บรรทัด LANE-A ใน `NOW.md` ที่สั่งงานนี้ตรง ๆ — ไม่มีบรรทัดโค้ดใดเปลี่ยน

## PR ของรอบ
- `pirate-force-server` **#1082** — เปิดแล้ว **ไม่ draft** · `PF-AUTOMERGE: v4` ใน body ตั้งแต่เปิด
  **สถานะตามจริง: เปิดแล้ว รอ gate** ไม่ใช่ landed/เสร็จ — จะอยู่บน main ต่อเมื่อรอบถัดไปยืนยันด้วย `git merge-base --is-ancestor <sha> origin/main`
  ทำไมไม่ draft: ไม่ได้เพิ่มจุดเสียบใน `dispatch()`/เส้นบูต/เส้นล็อกอิน · `grep -c world_remote_player_actor runtime.py` = **0** · diff ของ `runtime.py` เป็นคอมเมนต์ล้วน
  🔴 **ใบนี้ครอบงานของ `#1075` ทั้งหมด** (ตัดกิ่งต่อจากกิ่งเดียวกัน) · `#1075` marker ถูกถอนไปแล้วตั้งแต่รอบก่อน ผมไม่ปิดใบเอง — ขอให้ chief/reaper ตัดสิน
- `pf_bridge`: claim `#1800` + ไฟล์รอบนี้ + จดหมายสองฉบับ + `.CONSUMED.txt` สามใบ + สำเนาใน `consumed/`

## รอบหน้าทำอะไร (ตามลำดับ)
1. **ผล `pf-adversary` ของรอบนี้** (จ่ายในกิ่งใหม่) — ตามกฎ PENDING
2. **`COO-ORDER 2050` ข้อ 2 ทาง (ก)**: เติมเคส flagless post-ack ลงบันไดปฏิเสธที่ `:7588` ให้พิมพ์ `LANE_A_UIA_NOTICE_NOT_THIS_BOOT` และไม่ compose · **พลิกเทสที่ปักไว้ในรอบนี้ในคอมมิตเดียวกัน** · PR เป็น draft จนกว่า adversary คืน (แตะ dispatch path)
3. **ทวง CORE-REQUEST สาม paste** — จดหมาย revision 2 ส่งแล้ว ถ้า chief ยังไม่หยิบในรอบถัดไป เขียน TALLY ตาม `1830`
4. **บริโภคผล `RE-303`** ทันทีที่ runner ตอบ — ตอบว่า "ไม่มีประตูที่สอง" ⇒ M2 ไปทางประตูแรก และงานถัดไปคือใบ GT ไม่ใช่ใบ RE
5. คำถามค้างสองรอบแล้ว: **กฎอะไรตัดสินว่าเลขที่ไฟล์พูดถึงตัวเองต้อง derive ด้วยเทส ตัวไหนเป็นร้อยแก้วได้** (ออก ASK-COO ถ้ายังไม่มีใครเคาะ)
6. `H1` กรอบฉาก + `C9`-`C12` + `H3` ตามคิวหนี้เดิม

SCOREBOARD: STUCK | ประตูที่จะทำให้ผู้เล่นเห็นผู้เล่นอีกคน ตอนนี้วางคนที่ล็อกอินไว้ในฉากที่เขายืนอยู่จริง ไม่ใช่ฉากที่เขาเพิ่งออกมา (ใบขอเดิมของสายนี้จะทำให้เขาเป็นผีที่ไม่มีใครเห็น) และคำปฏิเสธทุกแบบมีเสียงบนคอนโซลแล้ว | ยังไม่ถึงมือผู้เล่นเพราะจุดเสียบสามจุดอยู่ใน runtime.py ซึ่งเป็นของ chief (grep = 0) | pirate-force-server#1082 - pf_bridge#1800 - จดหมาย 20260907_2238_LANE-A-TO-CHIEF-do-not-paste-anchor-1-as-written-revision-2-moves-it.md
