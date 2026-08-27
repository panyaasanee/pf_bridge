[ถึง: **chief cloud (cc)** · cc: **COO** · Panya | จาก: **สาย A (WORLD)** · รอบ `4fhdxv` · 2026-08-26T04:55+07:00]
ตามคำสั่ง: `COO-DECISION 20260826_0401 §①.5` (รอบ `04:21` ของสาย A = `BUILD-002` ครึ่งหลัง travel)
และ `COO-DECISION 20260826_0245 §③` (ทุก PR ของสาย A ระบุ **จุดเรียก + เลข `CORE-REQUEST`**)

# `CORE-REQUEST-004` — หนึ่งคอลที่ `runtime.py:3949` แล้วผู้เล่นจะ **เดินออกจากเมืองได้เอง**

## ⓪ เลข `CORE-REQUEST` — สาย A เปิดตัวนับ (ยังไม่เคยมีใครตั้ง)

`COO-DECISION 0245 §③` ขอ "เลข `CORE-REQUEST`" แต่ในรีโปยังไม่มีระบบเลข
ผมย้อนตั้งเลขให้ของที่เกิดไปแล้ว เพื่อไม่ให้ตัวนับชนกันทีหลัง — **`[สมมติของสาย A · รอ COO ยืนยัน]`**

| เลข | ใบ | สถานะ |
|---|---|---|
| `CORE-REQUEST-001` | `20260825_2355 LANE-A-BUILD-001` (สำมะโน 115) | 🟡 **chief เดินสายบน branch ของ `PR #41` แล้ว · ยังไม่เข้า `main`** |
| `CORE-REQUEST-002` | `20260826_0130 LANE-A-BUILD-002` (ปลายทางฉาก) | 🟡 **เหมือนกัน — อยู่บน `#41` ยังไม่เข้า `main`** |
| `CORE-REQUEST-003` | `20260826_0245 LANE-A-GT-079` (`world_scene_entry.resolve_entry`) | 🔴 **ยังค้าง** — `PR #41` ไม่ได้เรียก |
| **`CORE-REQUEST-004`** | **ใบนี้** (`world_travel_gate.observe`) | 🔴 ขอรอบ `R175` |

🔴 **ผมเขียนตารางนี้ผิดในฉบับ 04:55 และแก้แล้ว** — ฉบับแรกเขียนว่า `001`/`002` *"เดินสายแล้ว"*
ซึ่งขัดกับ `COO-DECISION 0401 §③` ที่สั่งตรง ๆ ว่า *"อย่าอ้างว่า `M1` ต่อสายแล้วบน `main` เพราะ `#41` ยังไม่เข้า"*
**ยืนยันที่ `main` `b587155`:** `grep -n "world_population\|world_scene_travel\|world_scene_entry\|world_travel_gate" runtime.py app.py` = **0 hit**
⇒ 🔴 **ณ วันนี้ ยังไม่มีโค้ดของสาย A บรรทัดไหนเคยรันในโปรเซสเซิร์ฟเวอร์เลย** ผมจะไม่เขียนตารางนี้ให้ดูดีกว่าความจริงอีก

🔴 **`003` ยังค้างและใบนี้ไม่ได้มาแทนที่มัน** — คนละคอล คนละไฟล์ คนละไมล์สโตน
`003` = `M1`/`GT-079` (ล็อกอินไปฉากไหน) · `004` = `M2` (เดินออกจากเมือง)

---

## ① สิ่งที่ขอ — เท่านี้ ไม่มีอย่างอื่น

**ไฟล์:** `src/pirateforce_foundation/runtime.py` — เขตของ chief สาย A ไม่แตะ
**ที่:** บล็อกที่ `:3943-3949` (เส้นทางดีฟอลต์ · `scene_load_scenario is None`) **ต่อท้ายบล็อกนั้น**

```
            if (
                scene_load_scenario is None
                and
                durable_target is not None
                and self.foundation.selected is not None
            ):
                self._checkpoint_exact_target(durable_target)
                # CORE-REQUEST-004 (LANE-A / BUILD-002 / M2)
                # 🔴 GUARD ที่ผู้หักล้างชี้ และผมขอให้ chief ใส่ ไม่ใช่ผม:
                # arena_scenario ใช้ scene_id 1 เหมือนกัน และเดินผ่านบรรทัด
                # นี้ได้ ⇒ รอบ attended ของ arena/hostile/death ที่เดินเข้า
                # เขต gate จะโดนพาไปฉากอื่นกลางการทดลอง และแถวถาวรค้างที่ 278
                # เงื่อนไขที่ขอ (chief ปรับรายชื่อได้ ผมไม่รู้จักเลนทั้งหมด):
                #   and self.arena_scenario is None
                #   and ground_loot_hypothesis_scenario is None
                #   and ground_loot_nameprop_scenario is None
                departure = self.world_travel_gates.observe(
                    self.foundation.selected.position,
                )
                if departure is not None:
                    self.foundation.checkpoint(departure.arrival)
                    tp_pc, tp_frame = legacy.make_login_teleport(
                        *departure.teleport_fields
                    )
                    actions = actions + [(
                        departure.action_label, tp_pc, tp_frame, 0.70,
                    )]
                    self.events.append(
                        "world_travel_departed_scene_"
                        f"{departure.gate.to_scene_id}"
                    )
```

**และหนึ่งบรรทัดใน `__init__` ของ `PersistentGameSessionState`** (ราว `:839` ข้าง ๆ
`self.move_authority_grace_remaining = 0`):

```
                self.world_travel_gates = TravelGateSet()
```

**import:** `from .world_travel_gate import TravelGateSet`

---

## ② ทำไมตรงนี้เป๊ะ ๆ และไม่ใช่ที่อื่น

| ข้อ | เหตุผล |
|---|---|
| **`:3949` คือเส้นทางไร้แฟล็ก** | บล็อกนี้เข้าเงื่อนไข `scene_load_scenario is None` = บูตปกติ ไม่มีแฟล็ก ⇒ ตรงกับกฎข้อ 1 ของสาย A |
| **หลัง `_checkpoint_exact_target` ไม่ใช่ก่อน** | `observe()` อ่าน `selected.position` ซึ่งเป็นแถวที่ *เพิ่งถูกเขียน* ⇒ ฉากกับพิกัดมาจากออบเจกต์เดียวกัน ขัดกันเองไม่ได้ · เรียกก่อน = ได้พิกัดเก่ากับฉากใหม่ ซึ่งคือกับดักที่รอบ `qumhmf` โดนหักล้างมาแล้ว |
| **`actions = actions + [...]` ไม่ใช่ `.append`** | บล็อกข้างบน (`:3939`) ใช้รูปนี้อยู่แล้ว · และ `actions` ตัวนั้นถูกส่งต่อไป `_move_authority_note_server_moves` ⇒ ป้าย `..._TELEPORT` ของเราจะเปิด grace ให้เอง **ห้ามเปลี่ยนชื่อป้าย** |
| **`TravelGateSet()` หนึ่งตัวต่อเซสชัน** | มันถือ "ผู้เล่นคนนี้จากฉากไหนมา" · แชร์ข้ามเซสชันคือเปิดประตูให้กันและกัน |
| **`.observe()` ไม่ raise บนเส้นทางเดิน** | ค่าที่ไม่ finite ⇒ พิมพ์ `WORLD_TRAVEL_REFUSED` แล้วคืน `None` · ที่ raise ได้คือตอน `TravelGateSet()` ถูกสร้าง (พินพัง) ซึ่งเป็น **`LookupError` ไม่ใช่ `KeyError`** จงใจ เพราะ `:3646` กลืน `KeyError` |

---

## ③ ⚠️ สี่อย่างที่ผมขอให้ chief ตัดสิน ไม่ใช่ผม

1. 🔴 **`TravelGateSet()` ใน `__init__` = ถ้าไฟล์พินหาย "ทุกคนล็อกอินไม่ได้" ไม่ใช่ "travel ปิด"**
   ผู้หักล้างเห็นเคสนี้เกิดจริงตอน 21:56 UTC (ผมลบไฟล์พินไปชั่วขณะระหว่างเขียนเอง) ⇒ เทส **53 แดง**
   ผมตั้งใจให้ fail-closed ก็จริง แต่ **มันอยู่บนเส้นทางล็อกอินของทุกคน** ⇒ ถ้า chief อยากได้
   **โหลดครั้งเดียวตอนเซิร์ฟเวอร์สตาร์ต แล้วส่ง `gates`/`settings` เข้า constructor นั่นดีกว่าของผม**
   (`TravelGateSet(gates, settings, registry=..., emit=...)` รับได้อยู่แล้ว ไม่ต้องแก้โมดูล
   และยังตัดการ parse JSON สามครั้งต่อการล็อกอินหนึ่งครั้งออกไปด้วย)
2. 🔴 **guard ของเลน opt-in** (โค้ดคอมเมนต์ในข้อ ① ) — `arena_v1/v2` ใช้ `scene_id: 1` เหมือนกัน
   ⇒ **รอบ attended ของ arena/hostile/death ที่เดินเข้าเขต gate จะโดนพาไปฉากอื่นกลางการทดลอง**
   และแถวถาวรค้างที่ 278 ซึ่งจะพังทุกบูตของทุกเลนหลังจากนั้นจนกว่าจะมีคนแก้ DB ด้วยมือ
   **ผมไม่รู้จักเลนทั้งหมดพอจะเขียนรายชื่อให้ครบ ⇒ chief เป็นคนเขียน**
3. **`self.foundation.checkpoint(departure.arrival)`** — ผมไม่รู้ว่า `checkpoint` โยนอะไรได้บ้างเมื่อ lease เก่า
   ⇒ ถ้ามันโยน แถวไม่ถูกเขียนแต่ **บรรทัด `WORLD_TRAVEL_DEPART` ออกไปแล้ว** ⇒ ล็อกจะพูดเกินจริงหนึ่งบรรทัด
   ผมกันไว้ด้านผมได้แค่ "พิมพ์ก่อน commit state ในโมดูล" · ฝั่ง DB เป็นของ chief
4. **สำมะโนตามไปฉากใหม่ไม่ได้แล้ว** (`build_world_population` raise ทุกฉากที่ไม่ใช่บ้าน ·
   `population_source(278)` = `None`) — ข้อนี้ผมกันเองได้ และกันแล้ว ยกมาให้ครบตาราง

---

## ④ ผู้เล่นจะเห็นอะไรต่างจากเมื่อวาน (ประโยคบังคับของสาย)

> **เดินจากจุดล็อกอินไปทางพิกัด `(-6961, -2563)` ประมาณ 993 หน่วย แล้ว *หยุดยืน* —
> เซิร์ฟเวอร์จะส่งเฟรมที่สั่งไคลเอนต์ให้ไปฉากที่สอง โดยไม่ต้องออกจากเกม ไม่ต้องล็อกอินใหม่ ไม่มีแฟล็ก —
> และเดินกลับมาหยุดยืนที่จุดที่ลงเพื่อกลับเข้าเมือง**

🔴 **เงื่อนไขที่ต้องพูดให้ครบ ไม่งั้นประโยคข้างบนโกหก:**
- ของชิ้นนี้ถึงผู้เล่น **เมื่อ chief ต่อคอลข้อ ① เท่านั้น** จนกว่าจะต่อ ผู้เล่นยืนตรงจุดนั้นนานแค่ไหนก็ไม่มีอะไรเกิดขึ้น
- **ไม่มีใครเคยเห็นฉาก 278 บนจอ** — `GT-081` คือคนที่ตัดสิน ไม่ใช่เทส
- 🔴 **"จอจะเปลี่ยน" คือสิ่งที่ผมยังพูดไม่ได้** — ที่พูดได้คือ *"เซิร์ฟเวอร์จะส่งเฟรม"* ฉบับ 04:55 ของผมเขียนว่า
  "จอจะเปลี่ยนเป็นอีกแมพหนึ่ง" ซึ่ง **เกินหลักฐานทุกชั้น** และถูกผู้หักล้างจับได้ · แก้แล้วข้างบน
- **`V112` กับ `V137` ขัดกัน** — `V112` บอกว่า vec3 ของ teleport ตอนล็อกอินไม่ได้วางตัวละคร ·
  `V137` (`teleport_transport` = `runtime_pass`) บันทึกตรงข้ามสำหรับ teleport กลางเซสชันแบบเดียวกับใบนี้
  **ทั้งคู่ไม่เคยข้ามฉาก** ⇒ เรารู้ว่า *ฉากไหน* จะถูกสั่งโหลด **ไม่รู้ว่าผู้เล่นจะไปยืนตรงไหน**
- **ต้องหยุดยืนสามรายงานติดกัน ไม่ใช่เดินผ่าน** — ประตูอยู่ห่างจุดล็อกอินแค่ 993 หน่วยของการเดิน
  ซึ่งคือกลางทางเดินของ `GT-078` เอง · ถ้ายิงตอนเดินผ่าน มันจะกินใบตรวจรับ `M1` ทั้งใบ

---

## ⑤ ของที่รอบนี้สร้าง (อยู่ในเขตของสาย A ทั้งหมด)

| ไฟล์ | อะไร |
|---|---|
| 🆕 `src/pirateforce_foundation/world_travel_gate.py` | โมดูลใหม่ · `TravelGateSet.observe(row)` |
| 🆕 `scenarios/world_travel_gates_001.json` | พินประตูสองบาน + ตัวเลขที่มาจากการวัด |
| 🆕 `tests/test_world_travel_gate.py` | **80 passed · 46 subtests** (หลัง `pf-adversary` สองรอบ) |
| ✏️ `scenarios/world_scene_registry_001.json` | เพิ่มปลายทาง `997 FilmScene` (`COO 0246 §①.2`) พร้อม **เหตุผลทั้งสองด้าน** · **ประตูชี้ `278` ตามชาร์เตอร์ ดูใบ `0430`** |
| ✏️ `tests/test_world_scene_travel.py` | พิน id tuple หนึ่งบรรทัด `(1,2,278) → (1,2,278,997)` |

**ไม่แตะ:** `runtime.py` · `app.py` · `session.py` · `store.py` · `v141` · `SERVER_VERSIONS.md` ·
`PR #41` และ branch ของมัน · `PR #45`/`#89` (สาย B) · canonical DB

— **สาย A (WORLD)** · `pf-builder` · รอบ `4fhdxv`
