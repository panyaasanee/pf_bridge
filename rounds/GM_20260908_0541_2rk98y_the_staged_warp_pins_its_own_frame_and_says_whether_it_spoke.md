# LANE-GM รอบ `2rk98y` — วาปที่ stage ปักเฟรมของตัวเองได้แล้ว และบอกว่ามันพูดหรือเปล่า

- เริ่มรอบ: 2026-09-08T05:41+07:00 (`TZ=Asia/Bangkok date`)
- ล็อกรอบ: `pf_bridge#1863` (`[LANE-GM] round 2rk98y: claim`) — ค้นก่อนเปิด:
  PR หัว `[LANE-GM] ...` ที่ยังเปิดอยู่ใน `pf_bridge` = **0 ใบ**
  (`search_pull_requests` `repo:panyaasanee/pf_bridge is:open is:pr in:title "LANE-GM"`
  = `total_count 0` · control: query เดียวกันด้วย `"LANE-DB"` คืน 4 ใบ ⇒ ตัวค้นทำงาน
  ไม่ใช่ผลศูนย์ปลอม) จึงตัดกิ่งใหม่ **ไม่ใช่ takeover**
- กิ่ง: `claude/brave-galileo-2rk98y` (bridge) · `claude/zealous-hawking-2rk98y` (server)
- นาฬิกา: บรรทัดล่างสุดของ `_BRIDGE_HEARTBEAT.txt` = `05:28:02 +07` ห่างจากเวลาเริ่มรอบ
  **13 นาที** ⇒ สะพานไม่ค้าง ไม่ต้องเทียบหลักฐานอิสระ
- `VITAL_REGISTRY_FROM_CLIENT_BINARY_20260817.tsv` **ยืนยันว่ามีจริง** (11,388 ไบต์)
- อ่านตามลำดับ COMMON: `NOW.md` (รอบ `0442`) → กล่องจดหมาย → ไฟล์รอบล่าสุดของสาย
  (`0w9jhq` + addendum `0512`) → คิวในไฟล์สาย

## รอบนี้ขยับ NOW/M ข้อไหน — ตอบทีละข้อของบรรทัด `LANE-GM`
1. **"`#1837` claim ปิด → คัดลอกไฟล์รอบ `h7bwnl` ลง PR ใหม่"** — **จบไปแล้ว ไม่ใช่งานค้าง**
   ยืนยันบน `origin/main` วันนี้: `2a631dd` + `f591f58` วางไฟล์รอบ `h7bwnl` และจดหมายครบ ⇒
   รอบนี้แค่ **บริโภคใบเตือน** `20260908_0336_SYNC-NOTICE-*` (วาง `.CONSUMED.txt` แล้ว)
   และขอให้ COO ลบบรรทัดนี้ออกจาก `NOW.md` (จดหมาย `0553` ข้อ 1)
2. 🔴 **"งานแรก = วัด `HEADLESS_PROOF:` `staged` บน main ก่อนใบ attended"** — **ปลดล็อกแล้ว
   และจ่ายครบรอบนี้** · รอบก่อนตอบว่า "วัดไม่ได้ เพราะยังไม่อยู่บน main" · วันนี้อยู่แล้ว:
   `git grep -l "staged_readback" origin/main -- src/ tests/` เจอ 5 ไฟล์ และ
   `WARP_STAGED_NOTICE_TEXT = "STAGED RELOG"` อยู่ที่ `gm/say_wire.py:235` บน `origin/main`
   ⇒ **วัดจริงบน worktree สะอาดของ `origin/main` `7a064e7`** (§2) แล้วส่งเนื้อใบ attended ให้ K
3. **"`#1096`/`#1106` draft"** — `#1106` merge เข้า main แล้ว (โค้ดของมันอยู่บน main ตามข้อ 2)
   · `#1096` **ไม่แตะ** ตามเดิม คำถาม "ใครปิด" ยังอยู่กับ COO (ใบ `0300`)
4. **บันได M**: **ไม่ขยับ M2 และไม่อ้างว่าขยับ** — ใบ attended ที่ส่งวันนี้เทส **เครื่องมือ GM**
   ผ่านใบนั้นไม่ใช่ M2 ผ่าน (ข้อ (3) ของนิยามสายในไฟล์พรอมป์ · เขียนเป็น nonclaim ตัวหนา
   ในเนื้อใบเอง ไม่ได้เขียนแค่ที่นี่)
5. **PANYA `1846`**: งานหลักไม่ติดรอบนี้ · โค้ดเซิร์ฟเวอร์ที่ส่งไปคือหนี้ adversary ที่รอบก่อน
   ส่งต่อมาเป็น "งานแรกรอบหน้า" **ตรงตามที่ addendum `0512` สั่งไว้เอง** และหนึ่งในนั้น (D4)
   เป็นบรรทัดที่ผู้ปฏิบัติงานอ่านบนคอนโซลจริง ไม่ใช่เทสล้วน
6. **`0442` จดหมาย ALL-LANES ห้ามวาง `.CONSUMED.txt` ร่วม** — ใบที่รอบนี้บริโภคเป็นใบ
   `ADDRESSEE: LANE-GM` ใบเดียว ไม่ใช่ ALL-LANES ⇒ วาง stub ได้ตามปกติ

## §1 งานหลัก: จ่ายหนี้ `pf-adversary` ของรอบ `0w9jhq` — D1/D2/D3/D4/D5/D6/D7/D8
addendum `0512` เขียนไว้ตรง ๆ ว่า "**ไบต์ที่ชิปไม่ผิด สิ่งที่ขาดคือเทสที่จะเห็นถ้ามันผิด**"
รอบนี้เขียนตาที่มองเห็นนั้น ไม่ได้แก้ไบต์

| ข้อ | มิวแทนต์ที่ **เคยรอด** ทั้งชุด | ราคาถ้ามันหลุดจริง | ตายที่ไหนตอนนี้ |
|---|---|---|---|
| D1 | สลับ `pc`/`frame` ในทูเพิล | v141 เขียน `out_frame` ⇒ ส่ง pc 56 ไบต์แทนแพ็กเก็ต 66 ไบต์ · GM ไม่เห็นอะไร คอนโซลบอกว่าส่งแล้ว | `assert_staged_warp_notice_only` อ่าน `pc[16:18]` + decode + `frame[-len(pc):] == pc` |
| D2 | `delay` `0.0` → `3.0` | v141 `time.sleep` ก่อน `sendall` ⇒ ทุก `/warp` ที่ stage แช่คิวส่งของคอนเนกชันนั้น 3 วินาที | helper เดียวกัน (`assertEqual(delay, 0.0)`) |
| D5 | ประโยค → `WARP DONE!!!` (12 ASCII เหมือนกัน) | คำอ้างว่า "ย้ายแล้ว" จากคำสั่งเดียวในสายที่ **ไม่ย้ายใคร** | helper เดียวกัน ปักสองด้าน: body ที่ decode ได้ **และ** `say_wire.WARP_STAGED_NOTICE_TEXT` |
| D3 | เติมป้ายเข้า `runtime.py` `_GM_WARP_LABELS` | resync เขียน `selected.position.scene_id` เป็นปลายทาง + ติดอาวุธ `gm_warp_position_pending` ⇒ ก้าวเดินธรรมดาก้าวถัดไปถูกนับว่า "วาปถึงแล้ว" | `StagedWarpRuntimeLabelWiringTests` อ่าน `runtime.py` เป็นข้อความ (ท่าของ `OneOfTwoWiringTests`) |
| D4 | `notice=` เป็นค่าคงที่ / ลืมส่ง | คอนโซลตอนประกอบไม่ได้ = ตอนสำเร็จ **ลบหนึ่งบรรทัด** ⇒ ต้องอ่าน "ความว่าง" | ฟิลด์ `notice=sent\|none` จริงบน `GM_CHAT_STAGED_NEXT_LOGIN` + สามเทสใหม่ |
| D7 | docstring "Two of the labels" ทั้งที่มี **หก** | ตัวเลขในร้อยแก้ว drift เงียบมาสี่รอบแล้ว | `NoticeLabelCountTests` อ่าน docstring จริงเทียบจำนวนป้ายจริง |
| D8 | helper ก๊อปสองไฟล์ | ปักแรงที่เดียว อีกที่อ่อนตลอดไป | เหลือ **นิยามเดียว** อีกไฟล์ `import` (ท่าเดียวกับ `test_gm_warp_undo_confirm_window.py`) |
| D6 | คำว่า "answers on screen" | เป็นข้อเท็จจริงชั้น wire ไม่ใช่ชั้นจอ | `docs/GM_LANE.md` มี nonclaim ชั้น **"Nobody has seen `STAGED RELOG` on a screen"** ตรงแบบเดียวกับที่บ้านนี้เขียนไว้แล้วสองที่เรื่อง `SPEED DENIED` |

- **`_print_staged_way_out` รับ `notice` เป็น keyword บังคับ ไม่มีค่าเริ่มต้น** — ต่างจากทุก
  argument อื่นของฟังก์ชันนั้นที่ค่า default **จริงสำหรับ caller ที่ลืม** · ค่าเริ่มต้นของ
  `notice` ไม่มีค่าไหนจริงทั้งสองทาง ⇒ caller ที่ลืมจะพาความเงียบกลับมาโดยการละเว้น
  (ท่าเดียวกับ `legacy` ของ `_stage_action` ที่รอบ `0w9jhq` ตั้งไว้)
- **แหล่งของคำ = `notice_sent` ของ caller ไม่ใช่ `verdict.is_notice`** — `is_notice` แปลว่า
  ประโยคถูก **แนบ** แต่ audit ที่ล้มทิ้งประโยคที่แนบแล้วได้หนึ่งชั้นข้างบน ⇒ สองบรรทัด
  (`GM_CHAT_NOTICE_SENT` กับ `GM_CHAT_STAGED_NEXT_LOGIN`) เถียงกันเองไม่ได้ตามโครงสร้าง

## §2 `HEADLESS_PROOF:` — วัดจริงบน `origin/main` สะอาด (ครั้งแรกของกลไกนี้)
วัดบน **worktree แยกของ `origin/main` `7a064e7`** (ไม่ใช่กิ่งของรอบนี้ · กิ่งนี้เพิ่ม
`notice=` เข้าไปในบรรทัดเดียวกัน จึงวัดบนกิ่งไม่ได้โดยหลักการ)
```
GM_CHAT_NOTICE_SENT account='panya' command=warp notice='STAGED RELOG'
GM_CHAT_STAGED_NEXT_LOGIN account='panya' command=warp scene_id=278 coordinates=none basis=server_believed_scene next='this scene has no confirmed spawn point, so no teleport could be sent; the next login for this account is staged to start in it'
GM_CHAT_STAGED_READBACK account='panya' composed=yes notice='SCENE 000278' staged_readback staged scene=278 name='Beach Soccer Field'
ACTION /warp 278  LANE_GM_CHAT_WARP_STAGED_LOCAL_TALK_NOTICE  len(pc)=56 len(frame)=66 delay=0.0 ch=0xAC52
ACTION /staged    LANE_GM_CHAT_STAGED_READBACK_LOCAL_TALK_NOTICE  len(pc)=56 len(frame)=66 delay=0.0 ch=0xAC52
```
- นี่คือครั้งแรกที่ **ทั้งวงจร** (`/warp` → ประโยค → `/staged` → ชื่อฉากจริง) ถูกเดินจากปลาย
  ถึงปลายบน main โดยไม่ต้องมีกิ่งไหนช่วย · ฉาก 278 = `Beach Soccer Field` จาก lookup
  **เดียวกับที่ล็อกอินใช้**
- คำสั่งเต็ม + nonclaim อยู่ในจดหมาย `20260908_0552_LANE-GM-TO-K-gt-body-*`
- 🔴 **ไม่มีจอ ไม่มีไคลเอนต์ในการวัดนี้** — เป็นหลักฐานชั้น wire ล้วน

## §3 ใบ attended ที่ส่งให้ K วันนี้
`notes_to_chief/20260908_0552_LANE-GM-TO-K-gt-body-staged-warp-says-on-screen-and-relog-lands.md`
ชื่อใบที่ขอ: `GM-WARP-STAGED-SAYS-ON-SCREEN-AND-RELOG-LANDS-001` (เลขใบ = K ตั้ง)
- บล็อก `ATTENDED:` ครบ 5 บรรทัด + `HEADLESS_PROOF:` ในบล็อกนั้น
- **ปิดวงจรที่สายนี้ยังไม่เคยมีใครดูจอยืนยัน**: พิมพ์ → เห็น `STAGED RELOG` → `/staged`
  เห็น `SCENE 000278` → relog → ยืนที่ฉาก 278
- ใบเขียนไว้ล่วงหน้าว่า **ถ้าจอเห็นครบแต่ relog ไม่ไป 278 คือผลที่มีค่าที่สุดของใบ**
  (แปลว่าจุดขาดอยู่ที่ `claim_login_scene`/`resolve_entry` ไม่ใช่ประโยคบนจอ)
- ใบ **ไม่พึ่ง** `notice=` ของ PR รอบนี้ และเขียนไว้ว่าถ้าเห็นฟิลด์นั้น = PR ลง main แล้ว

## §4 หลักฐาน
- มิวแทนต์ **6 ตัว รัน 6 ตาย** (สลับ pc/frame · delay 3.0 · `WARP DONE!!!` ·
  `notice=True` ตายตัว · เติมป้ายเข้า `runtime.py` · docstring กลับเป็น "Two") · control เขียว
- ชุดเต็ม `pytest tests/` บนต้นไม้สุดท้ายจริง: **ดู `SCOREBOARD` ท้ายไฟล์**
- `pf_gate_preflight.py --repo <server>`: ดูท้ายไฟล์
- **ไม่เพิ่มไฟล์เทสใหม่** (ต่อท้ายสองไฟล์ที่มีอยู่) · **ไม่เพิ่ม/ย้าย/ลบ skip** ·
  ไม่แตะ canonical DB · ไม่แตะ `runtime.py`/`app.py`/v141 (อ่านเป็นข้อความอย่างเดียว) ·
  ไม่แตะเขตสาย A/B · ไม่แตะ `tools_bridge/` · ไม่แตะ `.claude/`
- บรรทัดที่ **เพิ่ม** ในดิฟทั้งหมดเป็น ASCII (นับแล้ว: non-ascii added lines = 0)

## nonclaims
- 🔴 **ไม่มีใครเคยเห็น `STAGED RELOG` บนจอ** — รอบนี้ก็ยังไม่เห็น · ทุกคำในไฟล์นี้และใน
  `docs/GM_LANE.md` เป็นชั้น wire จนกว่าใบ attended ข้างบนจะถูกรัน
- **ไม่ได้รันบนเครื่องเจ้าของ ไม่มีจอ ไม่มี client** · `HEADLESS_PROOF:` คือหลักฐานว่า
  **กลไกติดอาวุธบน main** ไม่ใช่ว่าฟีเจอร์ผ่าน
- **ไม่ขยับ M2** · GM คือเครื่องมือไปถึงสภาพที่จะเทส
- **ไม่อ้างว่าจะผ่านเกต Windows** — ไม่มีเครื่อง Windows ที่นี่
- **ไม่อ้างว่าอยู่บน main** สำหรับใบของรอบนี้ — รอบถัดไปยืนยันด้วย
  `git merge-base --is-ancestor <sha> origin/main`
- **ยังไม่ได้จ่ายหนี้ adversary เก่าทั้งหมด**: `D9`(0w9jhq) · `D4`/`D6`/`D9`/`D11`/`D13`
  จาก `osxc85`/`5rxy86`/`6b1o1r` · `qpauwp` D5 · ข้อ 3 ของ `6b1o1r` — ยกไปรอบหน้าตามเดิม

## TWO_SESSIONS_SAME_SCENE (แก้ให้ตรงกว่ารอบก่อน ตาม D9)
รอบ `0w9jhq` เขียนว่า "ไม่กระทบ" ซึ่งจริงสำหรับ **การเขียน** แต่ไม่ครบสำหรับ **ใครได้ยิน**:
`runtime.py:8071-8081` บอกว่าทุกคอนเนกชันของ listener นี้ใช้ตัวตนเดียว (`--token` ของโปรเซส)
⇒ แถวที่ stage เป็นของ **ทุกเซสชันของบัญชีนั้น** แต่ประโยค `STAGED RELOG` เป็น
**ต่อคอนเนกชันที่พิมพ์** · เซสชันที่สองที่ relog จะไปโผล่ฉาก 278 โดยไม่เคยถูกบอก —
นี่เป็นสมบัติของ **stage** ไม่ใช่ของประโยค และไม่ได้เกิดจากรอบนี้ · รอบนี้ไม่เปลี่ยนมัน
แต่ **บันทึกให้ตรง** และ `notice=sent|none` ที่เพิ่มวันนี้อยู่บนคอนโซล (ของทั้งโปรเซส)
จึงเป็นที่แรกที่ผู้ปฏิบัติงานเห็นได้ว่าประโยคออกไปกี่ครั้งเทียบกับ stage กี่ครั้ง ·
ไม่แตะ registry ที่แชร์ ไม่แตะ roster/HP/ศพ/ของตก

## §5 สถานะ PR ตามจริง (ห้ามเขียนว่าเสร็จ/landed)
- **`pirate-force-server`** ใบของรอบนี้ — เปิดแล้ว ไม่ draft · `PF-AUTOMERGE: v4` ในบอดี้
  ตั้งแต่เปิด · **ยังไม่ยืนยันว่าอยู่บน main**
- **`pf_bridge#1863`** — claim ของรอบนี้ เติม marker ตอนจบ = ปลดล็อก
- **`ADVERSARY_PENDING`** — สั่ง `pf-adversary` บนกิ่ง `claude/zealous-hawking-2rk98y`
  ต้นรอบ (เรียก 1 ครั้งจากเพดาน 2) · **ไม่มีประโยคไหนในไฟล์นี้เขียนว่า "ผ่าน adversary"**
  · ผลคืนหลังปลดล็อก = รอบถัดไปหยิบเป็นงานแรก

## รอบหน้าทำอะไร (เรียงแล้ว)
1. 🔴 **ผล `pf-adversary` ของรอบนี้** ถ้าคืนหลังปลดล็อก — จ่ายในรอบเดียวกัน
2. 🔴 **ยืนยัน `git merge-base --is-ancestor`** ว่าใบของรอบนี้ขึ้น main หรือยัง ·
   ถ้าขึ้นแล้ว **วัด `HEADLESS_PROOF:` ซ้ำให้เห็น `notice=sent`** แล้วส่งบรรทัดใหม่ให้ K
   ทับของเดิมในเนื้อใบ (ใบเขียนรองรับไว้แล้ว)
3. **เทสความเท่ากันของกฎ single-use กับ `resolve_entry(via_login=False)`** (ยกจาก `0w9jhq` §2)
4. **หนี้ adversary เก่าที่ยังไม่จ่าย** (ดู nonclaims) — `D9` ของ `0w9jhq` ก่อน
5. **ตอบ K เรื่อง `RE-302`** (ค้างหลายรอบ) + เสนอ chief เรื่อง `docs/FUNCTIONAL_COVERAGE.json`
   ที่ไม่มีแถวของคำสั่ง GM ใหม่เลย
6. **ยังไม่ทำและยังไม่มีใครขอ**: `staged` ของบัญชีอื่น · `warp <ชื่อ> #<n>` (ชื่อซ้ำ)
