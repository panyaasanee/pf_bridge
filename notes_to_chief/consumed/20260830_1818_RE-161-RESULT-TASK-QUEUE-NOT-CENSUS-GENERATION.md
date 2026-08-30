[ถึง: chief (ผู้รับผล RE) · cc: LANE-B, COO, Panya | จาก: Codex RE runner · 2026-08-30T18:18+07:00]

# RE-161 RESULT — current DEAD census เพียงพอ; pose รอ task queue/model gate ไม่ได้รอ census generation

**สถานะที่เสนอ: DONE (static bounded negative, jobs 1-3 ครบ)**

- ROUND START: `2026-08-30T18:00:25.384+07:00`
- TICKET START: `2026-08-30T18:07+07:00`
- ticket block SHA-256: `8fec7cbb632db6f1f39f683376e9b6952a3fe172054095b7ea3d5553eb368a9d`
- queue SHA-256: `be99f1c5a2529545d9db2a7cf1e22c4f6c5830d19033e591f2e327eb5ecc4465`
- pinned image: `GameClient.local.bin` SHA-256
  `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`

## คำตอบสั้น

ไม่พบกลไก `census generation`/sequence ที่บังคับให้ corpse pose รอคิลถัดไป และ actor-entry payload ที่ตรวจไว้ไม่มี
generation field ให้ task รับไปด้วยเลย สำหรับ actor identity ที่มีอยู่แล้ว **current `MOB_DEATH_DEAD` full recomposed census
เพียงพอ** ให้เส้นทาง inbound เข้า death sync, สร้าง `CActorTask_Dead` ที่ `0x472810` และนำ task เข้าคิว

pose `_F_DIE_000` ผูกกับ lifecycle ของ `CActorTask_Dead`:

- task start slot `+0x08 = 0x4765C0` เล่น pose เมื่อ actor/model/type พร้อมและ model bit `0x40` ผ่าน
- task update slot `+0x0C = 0x472850` ตรวจ IsDead + one-shot latch `[task+0x20]` + model bit แล้วเล่น/retry pose
- ระหว่างการ push task กับการเรียก start มี task-manager queue ที่ทำให้ task ใหม่รอได้ถ้ามี current task/queue/update อยู่

ดังนั้น observation ว่า “เห็นล้มตอนคิลถัดไป” ยังเป็น **runtime correlation** ไม่ใช่ static proof ว่า next recompose เป็น
ตัวปลด generation gate. Static ระบุจุดหน่วงที่เป็นไปได้ได้ถึง task queue/model readiness แต่ไม่มีค่า runtime เพื่อชี้ว่า
gate ใดเกิดขึ้นจริงในเซสชันนั้น

## แก้ premise ของ packet sequence

ใน artifact ฝั่ง server ปัจจุบัน `MOB_DEATH_DYING` และ `MOB_DEATH_DEAD` **ต่างก็เป็น full recomposed census frame**
ของ kill เดียวกัน ไม่ใช่ “small DEAD packet แล้วมี recompose ใบที่สามตามมา” ดังนั้น current DEAD census คือ actor-entry
update ปัจจุบันอยู่แล้ว; DYING ของคิลถัดไปเป็นเพียง actor-entry packet ถัดไป ไม่ใช่ generation bump ที่พบใน wire schema

capture เดิม `GameClient/capture_pexile_20260830_151429/server_console_live.out.txt` SHA-256
`a2544e736dc7ba6f8ab132d30d270c13acca71e6f61a4c615643dc8c17fa17bb` ยืนยัน server-side compose/order
DYING → DEAD แบบ 97/97 entries ที่ L7580-7588, L14905-14913, L22675-22683 และ L28538-28546; หลักฐานนี้
ไม่ถูกใช้แทน client-observable pose timing

## exact static chain และ skip/defer gates

เส้นทางสำหรับ actor identity ที่หาเจอแล้ว:

1. inbound actor-entry `0x5E4060..0x5E41CD` → identity reconcile `0x446F30`
2. existing actor path ใช้ actor `+0x20` → death sync `0x4437C0..0x443A9A`
3. `0x443990` ตรวจ IsDead; false = ไม่สร้าง task
4. `0x44399B..0x4439C1` ตรวจ current task `[actor+0x30]` ด้วย RTTI descriptor
   `CActorTask_Dead` (`0x102ED98`); ถ้าเป็น dead task อยู่แล้ว = ข้าม duplicate constructor แต่ไม่ได้รอ generation
5. `0x4439C7` allocate → `0x4439E9` เรียก ctor `0x472810` → `0x4439FC` push ผ่าน `0x4843C0`
6. `0x4843C0` route task เข้า actor task-manager lane ผ่าน `0x4A0C90`; มันไม่ได้เล่น pose เอง
7. ถ้า manager idle, `0x4A0D6E` เรียก update `0x4A0B50` ด้วย dt=0 → promote/start `0x4A09C0` →
   `0x4A0A50` เรียก task vtable `+0x08` แบบ synchronous; ถ้า manager กำลัง update/มี current task/queue อยู่
   task ใหม่รอใน local task queue
8. start `0x4765C0`: actor/model/type gates → model bit `[actor+0x70]&0x40` → pose call ที่ `0x47670F` →
   latch `[task+0x20]=1` ที่ `0x476718`
9. update `0x472850`: actor/model/type/IsDead → one-shot latch → model bit → pose call ที่ `0x4728AF` →
   latch ที่ `0x4728B8`; ถ้า model bit ยังไม่พร้อม latch ยังเป็น 0 จึง retry ใน task update รอบหลังได้โดยไม่ต้องมี census ใหม่

first-spawn/not-found path ใช้ actor `+0x10` และข้าม death sync ใน packet นั้น นี่คือกฎ spawn-before-update ที่เคย pin ไว้
ไม่ใช่ generation rule: ต้องมี actor identity อยู่ก่อนจึงจะใช้ existing-actor death-sync path ได้

## bounded disassembly evidence

recursive disassembly ปัจจุบันบน pinned image ครบตาม span ต่อไปนี้:

- inbound `0x5E4060..0x5E41CD`: 365/365 B, SHA-256
  `85ff71ffceff5345f94facc9b7fa1c39c8efd2e429248d112cdba578d3df944e`
- death sync `0x4437C0..0x443A9A`: 730/730 B, SHA-256
  `85d294b84843e0bd46256e0257cf5d51be0415081739d82b0b4c254975ee9592`
- ctor `0x472810..0x472834`: 36/36 B, SHA-256
  `54877d3101b779ba1b83e283cbe94f8db9799905fc7a1157a1ada2e3f249c0a7`
- queue add `0x4A0C90..0x4A0D78`: 232/232 B, SHA-256
  `24b4ae5879bec87d31b0b836486646378be01684b0a22c754db0331d25127f6a`
- promote/start `0x4A09C0..0x4A0A98`: 216/216 B, SHA-256
  `90047f3e8afae6e07826afdaaeb6b390b7e078f07ae5d61063b3c87baaee3638`
- queue update `0x4A0B50..0x4A0C5C`: 268/268 B, SHA-256
  `b40a715681350369522dfabdbce85ef8fef622b8f924cb25933edba735652c87`
- dead start `0x4765C0..0x476763`: 419/419 B, SHA-256
  `e771b911d0ba2019364b3cda8e6a7ba5c54e2a0a21cf3ae6d0cba1b4f8ed7658`
- dead update `0x472850..0x4728F3`: 163/163 B, SHA-256
  `e04385a8cd54b800add22c4c8c5cc751b4243e19d208d684acdb8af2b6350999`
- raw positive call span `0x4843C0..0x4843EA`: SHA-256
  `72a328e5a239691f2441ea0a78f7d63cbc06b941b7322ec22d43bbd3d57c8cd8`

ผลลบเรื่อง generation ไม่อาศัย linear disassembly เพียงอย่างเดียว: มันประกอบจาก wire-schema artifact, exact inbound/apply/task
CFG, ctor argument ที่มีเพียง actor pointer, queue CFG และ prior proofs ที่ verify SHA แล้ว

## prior answers ที่ verify แล้ว

- `20260825_2121_RE-071-RESULT-STATIC-CONTRADICTION-PINNED.md` SHA-256
  `4accc563c58fd202512f556b3485d6bc54d73f439c9996c7f67fa6022ef7aca6`
- `20260827_1711_RE-107-RESULT-DEATH-BRANCH-MODEL-GATE-BOUNDED.md` SHA-256
  `6f82383c5a2210a108b739d72f3bea5ad649edb3467e0fd07f393e574cc455b3`
- `staged/re107_mob_death_static.py` SHA-256
  `2a4fb50a3691c43b562ec239c86e0754a6776345778ed0c45c1e262924731394`;
  รัน read-only ซ้ำกับ image ปัจจุบัน = `RESULT=PASS failures=0`
- `PF_RUNTIMERES_ACTOR_ENTRY001_STATIC_20260819.md` SHA-256
  `bc2806cc3fd340c1101284062cd85d266b017c364342ba8a5db18578d4bcb03a`:
  actor-entry subobject = mask bit `0x02` + u16 count + polymorphic entries ไม่มี generation/sequence field;
  not-found = spawn, existing identity = update/death sync
- ต้นทาง observation `20260830_1554_GT143-GT132-GT149-RESULT-*.md` SHA-256
  `042462792ee7477ccd22ba45964d53fd3b54b21d598772c2d6b32850dd5c1d1e` ระบุ “next recompose” เป็น
  hypothesis และไม่อ้างสาเหตุ

## job checkpoints

1. **DONE — external/gamedata first:**
   - `pf_bridge/external/`: 131 files / 37,176,794 B / manifest
     `b905e9b13f3c0c87fc4d4d457f637cbbcd31426e4e4ec76d4889fe15e680971c`; exact/raw-byte search
     `CActorTask_Dead|472810|MOB_LOOT_DROP|late_ms|hold_ms|MOB_DEATH|recompose|generation` = **ไม่พบ**
   - `pf_bridge/gamedata/`: 1,109 files / 15,319,585 B / manifest
     `9ba992357c2e6a7edbd366b996a801d3b354930babf695f35b615251bce3a3ab`; search ชุดเดียวกัน = **ไม่พบ**
   - ขอบเขตผลลบ: corpus สองโฟลเดอร์ ณ manifest ข้างบนเท่านั้น
2. **DONE — ctor/call/skip chain:** pin ตั้งแต่ inbound existing-actor path ถึง ctor/push ครบ พร้อมแยก first-spawn,
   not-dead และ duplicate-task gates
3. **DONE — activation/defer/generation question:** พบ local task-queue/model-ready deferral; ไม่พบ census generation field/gate
   ใน wire-to-task chain ที่ปิดครบ

นี่เป็น **method ceiling แบบปิด objective ได้**: ไม่ควรรัน RE-161 ซ้ำจนกว่า chief จะเปลี่ยน objective อย่างมีสาระหรือมี
runtime instrumentation ใหม่ที่แยก queue/model state ได้

## nonclaims

1. ไม่อ้างว่า corpse บนจอในคิลถัดไปคือ target identity เดิม เพราะไม่มี client-observable crosswalk field ผูกจอกับ actor id
2. ไม่อ้างว่า task queue, model bit, first-spawn หรือ duplicate-task gate ใดเป็นสาเหตุจริงของ one-kill lag; static ไม่มีค่ารันไทม์
3. ไม่อ้างว่า client เรียก `_F_DIE_000` สำเร็จใน capture นี้; capture เป็น server-side compose/order evidence
4. ไม่อ้างว่า packet ถัดไปไม่มีอิทธิพลใดเลยต่อ scheduling/update; อ้างเพียงว่าไม่พบ generation contract และ current DEAD
   census เพียงพอต่อการสร้าง/queue task สำหรับ existing actor
5. ไม่อ้างพฤติกรรม original server และไม่จับคู่ actor/corpse เพราะตัวเลข id เท่ากันโดยไม่มี crosswalk

## BUILD_IMPACT

`BUILD_IMPACT_NONE (client task lifecycle; no source/build change)`: ผลนี้ไม่รองรับการเพิ่ม census generation, duplicate
recompose หรือ reorder frame. ถ้าจะพิสูจน์สาเหตุ runtime ให้เปิด attended/observe-only objective แยก โดยเก็บอย่างน้อย
`0x4439FC`, `0x4843C0`, `0x4A0C90`, `0x4A0A50`, `0x4766FE`/`0x47289E`, current task/queue และ model bit
พร้อม client-observable identity crosswalk; ห้ามใช้ wire/DB แทนภาพจอ

## input SHA-256

- `src/pirateforce_foundation/runtime.py`:
  `7a3a958ca16b404a480bf04d43a5340f87c155bc79305385fdd6cf12a48185ca`
- `src/pirateforce_foundation/mob_death.py`:
  `3bc97f227a04dfb3f7f848dbc6a8bf2af36160c35b4bb233a8ff234eca7dcd6a`
- `current/pf_login_game_server_v141.py`:
  `2eb05ed2fdbdd5ee3d91f7fbb8c1d16a4c7a02a843bc97169b16a389e4ea4c22`
- capture console:
  `a2544e736dc7ba6f8ab132d30d270c13acca71e6f61a4c615643dc8c17fa17bb`

