# LANE-A round eepcv6 (เริ่ม 2026-09-06T19:21+07:00) — ขั้นที่ 4 ของรายการปลดแฟล็ก scene 1 + ขุด static ที่เปลี่ยนทิศ M2

## รอบนี้ขยับ NOW/M ข้อไหน

**ขยับ M2 ในทางที่ไม่ใช่โค้ด และมันคือของชิ้นสำคัญที่สุดของรอบ**: NOW.md วาง M2 เป็นที่ที่โปรเจกต์อยู่ และผล `GT-233` v3 เพิ่งกลับมา NEGATIVE เป็นครั้งที่สาม ใบผล R322A ชี้ว่าทางที่เหลือคือทาง (ก) ของ R318 §2.3 ("เซิร์ฟเดิมตอบเฟรม 0x1FB2") และว่า Panya เคาะแล้วในใบ PANYA-ORDER `1910` — รอบนี้ขุด static แล้วพบว่า **ทางนั้นถูก RE-234 ของเราเองปิดไปตั้งแต่ 5 ก.ย.** (handler ที่รับคำตอบของ TriggerVital เป็นสตับว่างที่ใช้ร่วมกับอีกสี่คลาส) รายละเอียดและสิ่งที่ขอ COO เคาะอยู่ในจดหมาย `20260906_1939_LANE-A-R322A-CONSUMED-*`

**ไม่ขยับ M3/P-2** และ **ไม่ขยับ M2 ฝั่งโค้ด** — ไม่มี PR ที่แตะเส้นทาง M2 ในรอบนี้ เพราะ opcode ที่จะตอบยังไม่มีใครรู้ (ข้อ "ติดอะไร" ข้างล่าง)

**ขยับรายการก่อนพลิกแฟล็กของ scene 1 จนหมดฝั่งสาย**: ขั้นที่ 4 คือขั้นสุดท้ายในรายการนั้นที่ยังเป็นของสาย A ล้วน ⇒ หลัง `#943` **ไม่มีขั้นไหนในรายการรอสายนี้อีกแล้ว** ที่เหลือคือสี่บรรทัดของ chief สามกลุ่ม กับใบ attended ของขั้นที่ 3

## ที่ทำ

`pirate-force-server` (กิ่ง `claude/nifty-euler-eepcv6` · PR **#943** เปิดแล้ว ไม่ draft มี marker)

**ขั้นที่ 4 (enumerate v141 behaviour ที่ขี่เฟรม `TARGET_VITAL` ในฉาก 1)** — responder branch รันแทน `super().dispatch(parsed)` ⇒ กลืนทั้งเฟรม ไม่ใช่แค่ลูป ChooseNPC
- `FROZEN_TARGET_VITAL_BEHAVIOURS` = **แปดแถว** เดินตามลำดับซอร์สของ v141 ลงบล็อกเดียวที่เฟรมพวกนี้เข้า (`v141:3680`) แต่ละแถวมี file:line ที่มันถูกอ่านมา และคำตัดสินหนึ่งใน UNREACHABLE / DISARMED / STAND_ASIDE / ACCEPTED_GAP · **อ่านจากไฟล์ frozen ไม่ใช่จาก capture**
- UNREACHABLE พิสูจน์จริงไม่ใช่อ้าง: v136 docking prompt ต้องการ `raw_pc == V136_EMPTY_RUNTIME_REQ_PC` ซึ่งเป็น PC 12 ไบต์ `vital_count 0` และ `nested_id None` (`v141:5642-5645`) — เฟรมที่ nested id เป็น TARGET_VITAL มี nested id ⇒ เท่ากันไม่ได้
- สองแถวเป็น STAND_ASIDE และ `respond()` ปฏิเสธเอง (คีย์เวิร์ดสามสถานะทั้งคู่ ทางเดียว ทำได้แค่ปฏิเสธ):
  - `runtime_ack_sent=False` — เฟรม runtime request แรกของ connection พ่วง RuntimeRes ack ที่ตรงกับ constructor (`v141:3768`) + welcome message + scene music · `runtime.py` เองเกตทางของตัวเองสิบกว่าจุดบนแฟล็กเดียวกันนี้
  - `exact_frozen_marker1_ready_pc=True` — `V138_MARKER1_READY_PC` **เป็นเฟรม TARGET_VITAL เอง** (`v141:5874-5882` assert ไว้ตรง ๆ) ⇒ มันเข้า branch นี้ และจะพา V140 marker1 population send หายไปด้วย
- **ทั้งคู่ inert**: ไม่มีใครส่งคีย์เวิร์ดวันนี้ ทั้งคู่ default `None` และ `None` แปลว่า "ไม่เคยบอก" ไม่ใช่ "ล้มเหลว" ⇒ พฤติกรรมเหมือนก่อนคอมมิตนี้ทุกไบต์สำหรับทุก call site ที่มีอยู่
- บรรทัดที่ปลดล็อกมันเป็นของ chief เขียนไว้ verbatim ใน `FROZEN_TARGET_VITAL_BEHAVIOUR_WIRING` **พร้อมเงื่อนไข**: ต้องลงคู่กับ decline fallback ที่ `WORLD_CENSUS_IDENTITY_RESOLVED_WIRING` ขออยู่แล้ว — ลำพังคีย์เวิร์ดอย่างเดียว decline ที่ตอบศูนย์ไบต์บน runtime request แรกจะกลืน ack ที่ client รออยู่ **แย่กว่า**การกลืนที่ guard นี้กันเสียอีก · ลงได้ข้างเดียว = อย่าลงเลย
- **สองแถวค้างเป็น ACCEPTED_GAP และถูกตั้งชื่อไว้ว่าเป็นเหตุผลที่แฟล็กยังปิด ไม่ใช่เหตุผลให้เปิด**: `v129_post_action1_request_observed` (bookkeeping ไม่คิวเฟรม) และ `v126_action_target_arm` ที่ pf-adversary `hd6tac` วัดไว้ — อันหลังไม่เสียหายใน Port Royal เพราะ `exact_p30_target` ต้องการรูป arena-harness ที่ actor จริงของฉาก 1 ไม่มี ซึ่งเป็นเรื่อง**บังเอิญ** ⇒ ใบ attended ของขั้นที่ 3 ต้องคลิกโดยมีอาวุธผูกอยู่

**อัปเดตหัวรายการปลดแฟล็ก**: ขีดฆ่าขั้นที่ 4 และแก้ประโยค "Steps 4, 6 and 7 are still lane A's own and still undone" ซึ่งหยุดเป็นความจริงไปแล้วสองรอบ (6/7 เสร็จรอบ `vxfepr`)

## ขุด static (ตัวแทน pf-adversary รอบนี้)

สั่ง **pf-static-re** ต้นรอบพร้อมเริ่มงาน (ไม่ได้สั่ง pf-adversary — งบ agent ไปลงตัวนี้แทน ดู "หลักฐาน") หกคำถามเรื่อง M2: ใครเปิดหน้ารายงานกัปตัน · ตระกูล `NavigationEx_*` · ตารางทริกเกอร์ฉาก 126 · Lua · เฟรมเปิด UI ทั่วไป · ของที่เซิร์ฟเรามีอยู่แล้ว
ผลเต็มและ nonclaims อยู่ในจดหมาย `20260906_1939_LANE-A-R322A-CONSUMED-*` สรุปสามข้อ:
1. 🔴 **ทาง (ก) ตายแล้ว** — RE-234 (DONE/MIXED ปิดรอบ `2mnd7b`) วัดว่า handler คำตอบของ TriggerVital = `[0x00710440,0x00710445)` = `mov al,1; ret 4` · ยืนยันซ้ำจาก `PF_PROTOCOL_REGISTRY.tsv:98` + ตัวคุมสี่คลาสที่ใช้ VA เดียวกัน ⇒ เป็นสตับใช้ร่วม รูปที่รอดคือ "ตอบด้วย opcode อื่น ยังไม่รู้ตัวไหน" = ที่ที่ RE-265 ค้างอยู่
2. 🎯 **ประตูที่ถูกที่สุดที่ยังไม่เปิดคือ `Bg3001.tgr`** — RE-273 (วันนี้ 13:40) พิสูจน์แล้วว่า `.tgr` คือตาราง trigger id → ชื่อ → lua (3,942 เรคอร์ด ordinal ผิด 0) **และมี parser พร้อมแล้ว** (`staged/re273_tgr_parse.py`) แต่ **ไม่มี artifact จาก .tgr ถูก commit เลยสักไฟล์** · หนึ่งรอบบนเครื่อง Panya = ได้ตารางฉาก 126 ทั้งตาราง ไม่ต้อง disassemble ไม่ต้องบูตเกม
3. 🔴 **เกตเลเวล**: `CONSTDATA_TH__SAILING_RESULT.tsv` วางเกาะ `n_VARI_1=2` (Prison Exile) ไว้ช่วงเลเวล **50-60** ⇒ ตัวละครเทสต่ำกว่า 50 อาจอยู่นอกเงื่อนไขที่ shipped มา ไม่ว่าเซิร์ฟส่งอะไร — ขอให้เป็นเกตของใบ GT ถัดไป ไม่ใช่ช่องให้จด

ผลลบที่บันทึกไว้เต็ม (Lua ไม่มีทางนี้ · `OpenCloseUI` opcode ยังไม่ established · ทิศทาง W/R อ่านจากตาราง TSV ไม่ได้) อยู่ในจดหมาย

## หลักฐาน

- `python3 -m pytest tests/test_lane_a_choose_npc_scene1.py` → **70 passed, 132 subtests passed**
- ชุดเต็มหลัง `git merge origin/main` (sha `88c5c3a` · main ขยับรับ `#939` ของรอบ `vxfepr` ระหว่างรอบนี้ · แก้ conflict โดยเก็บทั้งสองฝั่ง ไม่ทิ้งของใคร) → **12452 passed, 373 skipped, 0 failed** (445 s)
- `tools_bridge/pf_gate_preflight.py --repo <server>` → **PREFLIGHT PASS**
- ไม่มี skip เพิ่ม/ลบ/ย้าย · ไม่มีไฟล์เทสใหม่ (เติมคลาสในไฟล์เดิม)

**`ADVERSARY_NOT_COMMANDED` `pirate-force-server#943` / กิ่ง `claude/nifty-euler-eepcv6`** — รอบนี้ **ไม่ได้สั่ง pf-adversary** งบ agent ไปลงที่ pf-static-re เพื่อขุดทาง M2 แทน · บันทึกตามจริง ไม่ใช่ `ADVERSARY_UNAVAILABLE` (tool มีให้เรียก) และไม่ใช่ `ADVERSARY_PENDING` (ไม่มีอะไรค้างอยู่) · **รอบถัดไปของสาย A สั่ง pf-adversary บนกิ่งนี้เป็นงานแรก**
self-review แทน: อ่านทุก hunk ใน `git diff --cached` ก่อน commit ทุกครั้ง · รันไฟล์เทสที่แตะทุกครั้งที่แก้ · และปะ **มิวแทนต์สองตัวลงไฟล์จริง** ยืนยันว่าแดง แล้วคืนไฟล์และรันเขียวอีกครั้ง:
- `if not runtime_ack_sent` แทน `is False` → 22 failed
- `is not False` แทน `is True` บน guard ของ marker → 23 failed

**ชั้นหลักฐานสองชั้นแยกกัน · nonclaims**: รอบนี้มี **ชั้นเดียว** คือ wire/dispatch shape ระดับ unit (ไม่มีเซิร์ฟจริง ไม่มีซ็อกเก็ต) — **ไม่มีชั้น client-observable และไม่อ้างว่ามี** · `production_allowed` ยังเป็น `False` ไม่มีไบต์ใดถึงไคลเอนต์จากทางนี้ · การขุด static ทั้งหมดอ่านจาก TSV/จดหมายที่ commit แล้ว **ไม่ได้อ่านไบนารีไคลเอนต์** (ไม่มีในโคลนคลาวด์) ⇒ VA/span/sha ทุกตัวเป็นการคัดมา ไม่ใช่การ verify

**TWO_SESSIONS_SAME_SCENE:** ไม่แตะ — guard ทั้งสองเป็นฟังก์ชันบริสุทธิ์ของสถานะ frozen ต่อ connection ไม่อ่าน/เขียน world registry ที่แชร์ข้าม session

**NO_FEATURE_WAITING:** ผล `GT-233` ที่บริโภครอบนี้เป็น NEGATIVE และสิ่งที่มันปลดล็อกคือ**การรู้ว่าทางไหนตาย** ไม่ใช่ฟีเจอร์ที่รอสร้าง — ใบสร้างที่ควรตามมาต้องรอ opcode ซึ่งข้อ 1 ข้างบนบอกว่ายังไม่มีใครรู้ ⇒ สิ่งที่ออกแทนคือคำขอใบ RE (`Bg3001.tgr`) ในจดหมายถึง COO

## จดหมาย

- บริโภค `notes_to_chief/20260906_1909_KA1A-R322A-RESULTS-GT233-v3-NEGATIVE-1byte-vs-R318-GT281-wire-PASS.md` (GT-233 เป็นใบสาย A) · stub `.CONSUMED.txt` + สำเนาใน `notes_to_chief/consumed/` ลงกิ่งนี้ · `NOT-FOLDED:` — K พับใบผลเอง
- ออก `notes_to_chief/20260906_1939_LANE-A-R322A-CONSUMED-re234-refutes-0x1FB2-reply-bg3001-tgr-is-the-door.md` (ADDRESSEE: COO · cc chief/K/ka1-A) ขอ COO เคาะสามข้อ · มีสองข้อแก้ตัวเลขถึง K ("trigger 36" ไม่เคยอยู่ในชุดที่วัดได้ · `SCENE_NAME_TIP` 330 ไม่ใช่ 331)
- ไม่ออกใบ GT ใหม่: `production_allowed` ของฉาก 1 ยังปิด (ใบที่บูตแล้วไม่เห็นอะไรต่างคือใบที่กินเวลาเครื่อง Panya ฟรี) และใบ M2 ใบถัดไปควรเป็นใบ RE ของ `Bg3001.tgr` ซึ่งขอเลขจาก K ไปแล้วในจดหมาย

## ติดอะไร / ใครปลด

1. **M2 ติดจริง และติดที่ opcode** — ทาง (ก) ตาย (RE-234) · ทางที่รอดต้องรู้ว่า opcode ไหนเป็นตัวเปิดหน้ารายงาน · สาย A **ห้ามเดา opcode** ⇒ ปลดโดย: ใบ RE ของ `Bg3001.tgr` (ขอ K ตั้งเลข ขอ COO เคาะ) หรือใบ RE ของ `TriggerResult`
2. **PANYA-ORDER `1910` อ่านไม่ได้** — ไม่อยู่บน `origin/main` เพราะสะพานฝั่งเครื่อง Panya ค้าง (`SYNC_STUCK_20260906_1856.md` `behind: 4, ahead: 0` cherry-pick ค้าง) ⇒ ปลดที่เครื่องเท่านั้น ตามข้อ 1 ของ "รอ Panya ติ๊ก" ใน NOW.md
3. รายการปลดแฟล็ก scene 1: เหลือสี่บรรทัดของ chief สามกลุ่ม (`0137` · `VENDOR_AND_MISSION_LATCH_WIRING` · `WORLD_CENSUS_IDENTITY_RESOLVED_WIRING` + `FROZEN_TARGET_VITAL_BEHAVIOUR_WIRING`) แล้วจึงถึงใบ attended ของขั้นที่ 3

## รอบหน้าทำอะไร

1. **สั่ง pf-adversary บนกิ่ง `claude/nifty-euler-eepcv6` เป็นงานแรก** (รอบนี้ไม่ได้สั่ง — บันทึกไว้แล้ว)
2. ถ้า COO ตอบข้อ 2 ของจดหมาย: ส่งเนื้อใบ RE `Bg3001.tgr` ให้ K ผ่าน `*-TO-K-gt-body-*` · ถ้ายังไม่ตอบ ส่งเนื้อใบไปเลยแล้วให้ K ถือไว้ (ระเบียบ "เขียนคำถาม แล้วเดินต่อ")
3. ถ้า `0137` ขึ้น main: อ่านเทสทั้งไฟล์ด้วย pf-adversary อีกครั้งตามเงื่อนไขท้ายไฟล์ แล้วค่อยพิจารณาพลิกแฟล็ก — ยังไม่ใช่รอบนั้นจนกว่าใบ attended ขั้นที่ 3 จะมี
4. promotion ข้อ 1 (`remote_player_hypothesis.py` `#1476`) ยังรอ GT ไม่ใช่งานให้บูตเอง

SCOREBOARD: COMING | ยังไม่มีอะไรใหม่บนจอ (แฟล็ก scene 1 ปิดเหมือนเดิม) — ที่ขยับคือ (ก) รายการก่อนพลิกแฟล็กฉาก 1 ไม่เหลือขั้นไหนรอสาย A อีกแล้ว คลิกที่มาถึงก่อนเซิร์ฟตอบ ack แรกหรือมาในเฟรม marker-ready จะไม่ถูกกลืนอีกต่อไป และ (ข) M2 รู้แล้วว่าทางที่ใบสั่งให้เดินตายไปตั้งแต่เมื่อวาน พร้อมประตูถัดไปที่ถูกกว่าบูต attended | pirate-force-server#943 (open, marker, รอ gate) · pf_bridge round eepcv6 · จดหมาย 20260906_1939_LANE-A-R322A-CONSUMED-*
