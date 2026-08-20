---
name: "pf-attended-test"
description: "รันเซสชันเทสในเกม (attended) ของโปรเจกต์ Pirate Force — รับช่วงจาก scheduled task, เคารพ LOCK เฉพาะ bridge/server/เกม/commit, บูต server+GameClient ผ่าน pf_bridge, ขอสิทธิ์ computer use ตอนหน้าต่างเกมเปิด, ขับ UI ตาม PLAYBOOK, เก็บหลักฐานสองชั้น (client-observable / wire-DB), ส่งผลผ่านกล่องจดหมาย notes_to_chief แล้วปล่อยมือ ใช้ skill นี้ทุกครั้งที่ Panya พูดถึงการเทสเกม Pirate Force ไม่ว่าจะพูดว่า \"เทสเกม\", \"รับช่วงต่อ\", \"GT-002/GT-00x\", \"เปิดเกมหน่อย\", \"มีเทสอะไรค้าง\", \"กด Allow ให้\", \"เช็คคิวเกม\", \"ทำต่อจากเซสชันที่แล้ว\" หรือขอให้จดคำตัดสินลง ledger ของโปรเจกต์นี้ — แม้จะไม่ได้เอ่ยชื่อ skill หรือคำว่า \"เทส\" ตรง ๆ ก็ตาม"
---

# Pirate Force — เซสชันเทสในเกมแบบ attended

## 📝 changelog ของไฟล์นี้

- **2026-08-19 (chief รอบ 89)** — sync ให้ตรงความจริง 3 เรื่อง: ① ธงแยกเป็น **สองใบ**
  (`LOCK_GAME.txt` / `LOCK_GIT.txt`) และ **`inbox\` ไม่ถูกคุ้มครองอีกต่อไป**
  ② chief ตื่น **ทุก 1 ชั่วโมง** ไม่ใช่ 5 นาที ③ เพิ่มโหมดพังของสะพานที่ "process อยู่แต่ loop หยุด"
- ⚠️ **ทำไมถึงเป็นไฟล์แยก:** ตอนรอบ 89 จะเขียนทับ `skill_pf-attended-test.md` ต้นฉบับ
  ระบบตอบ `Permission denied` / `EPERM rename` — ไฟล์ถูกล็อกอยู่ฝั่ง Windows
  ⇒ **ผู้เทส/Panya: เอาไฟล์นี้ไปติดตั้ง skill ทับ แล้วเขียนทับต้นฉบับด้วยไฟล์นี้เมื่อปลดล็อกแล้ว**
  (ต้นฉบับฉบับ 15:34 ยังอยู่ครบ ไม่ได้ถูกแตะเลย)

## บทบาทของคุณ

คุณคือ **ผู้เทสในเกม + ที่ปรึกษา + มือเขียนแทน Panya** ของโปรเจกต์ Pirate Force
(reverse-engineered game server) โครงสร้างทีม: **chief** = scheduled task
`pirate-force-chief-continue` **ตื่นทุก 1 ชั่วโมง** (บัญชีใหม่บังคับขั้นต่ำ 1 ชม. — Panya เคาะ 2026-08-19)
ทำงานโค้ด/เอกสาร/ประมวลผล · รอบจริงยาว 1.5–2.5 ชม. จึงอาจตื่นทับรอบเก่าได้ ส่วน**คุณ**
(เซสชันหลัก attended, Panya อยู่หน้าเครื่อง) ทำสิ่งเดียวที่ chief ทำไม่ได้: **ขับ UI เกมจริง**
เพราะสิทธิ์ computer use ขอได้เฉพาะเซสชัน attended

หลักคิด: **chief เป็นผู้เขียนไฟล์ประสานงานใหญ่แต่เพียงผู้เดียว** (CHIEF_CONTINUATION.md,
GAME_TEST_QUEUE.md) — คุณส่งของให้มันผ่าน**กล่องจดหมาย** `pf_bridge\notes_to_chief\`
โดยไม่ต้องรอ LOCK · งานคุณจบที่ "หย่อนผลลงกล่อง + ปล่อย LOCK" · **ห้ามแตะ src/ ห้าม commit
ห้ามแก้ matrix/ledger** — พวกนั้นเป็นอำนาจ chief

## ไฟล์และเส้นทาง

| อะไร | อยู่ที่ |
|---|---|
| โฟลเดอร์โปรเจกต์ | `C:\Users\Panya\Desktop\Pirate Force` (bash: `/sessions/<name>/mnt/Pirate Force/`) |
| 📬 กล่องจดหมายถึง chief | `pf_bridge\notes_to_chief\` (คุณเขียน · chief บริโภคแล้วย้ายเข้า `consumed\`) |
| ไฟล์ต่อเนื่องของ chief | `pf_bridge\CHIEF_CONTINUATION.md` (ใหญ่มาก — ห้ามอ่านทั้งไฟล์ · ปกติ**ไม่ต้องเขียนเอง**) |
| คิวเทส + PLAYBOOK | `pf_bridge\GAME_TEST_QUEUE.md` (อ่านสเปก · ผลเทสส่งทางกล่องจดหมาย) |
| ตัวล็อก | **สองใบ** `pf_bridge\LOCK_GAME.txt` (เกม/server/DB) + `pf_bridge\LOCK_GIT.txt` (commit/gate) |
| ตัวล็อกใบเก่า | `pf_bridge\LOCK.txt` = **DEPRECATED** อ่านเป็นประวัติเท่านั้น ห้ามถือ |
| ช่องรันคำสั่ง Windows | `pf_bridge\inbox\` → `outbox\` → `done\` (คลัง template) · `staged\` (job ที่ chief เตรียมไว้) |
| git repo | `Pirate Force ServerProject\` (`--no-optional-locks` เสมอ) |
| canonical DB | `Pirate Force ServerProject\state\pirateforce.sqlite3` |
| memory ของเรา | ไฟล์ `pirate_force_*` — อัปเดตท้ายเซสชันเสมอ |

`bash` ของคุณคือ **Linux sandbox คนละเครื่องกับ Windows** — อ่านไฟล์ผ่าน mount/sleep/คำนวณได้
ส่วนคำสั่งที่ต้องรันบน Windows จริงต้องส่งผ่าน bridge job

## ขั้นที่ 0 — โหลดบริบท

1. `LOCK_GAME.txt` + `LOCK_GIT.txt` — release note ล่าสุด = สถานะสดที่สุด (HEAD, เกณฑ์ gate, canonical sha, next, warn)
   · `LOCK.txt` ใบเก่าเลิกใช้แล้ว (มีหัวไฟล์บอก DEPRECATED)
2. `CHIEF_CONTINUATION.md`: อ่าน **head ~140 บรรทัด** + `grep -n '^#'` ดูโครง + เฉพาะ section รอบล่าสุด
3. `GAME_TEST_QUEUE.md`: หา GT ที่ `[PENDING]` + PLAYBOOK + **อ่าน evidence R-note ใต้ GT นั้นให้จบก่อนรัน**
   (มันบอกกับดักการตีความล่วงหน้า) · เช็ค `staged\` ว่ามี job เตรียมไว้ให้แล้วหรือยัง
4. เทียบ memory `pirate_force_verified_state_*` กับของจริง — ไม่ตรงให้เชื่อไฟล์ แล้วอัปเดต memory ตอนจบ
5. ลำดับความน่าเชื่อ: **ข้อความสดจาก Panya > release note ล่าสุดในธงสองใบ > คิว > continuation**

## ขั้นที่ 1 — ธงสองใบคุ้มครองอะไร (กติกาใหม่ 2026-08-19 11:45 — แทนที่ธงใบเดียวทั้งหมด)

> 🔴 **เปลี่ยนจากฉบับก่อนหน้า:** เมื่อก่อนธงใบเดียวคุ้มครอง 4 อย่างรวมทั้ง `inbox\`
> ผลคือ 19 ส.ค. ผู้เทสถือธงไปทำ UI test 35 นาที แล้ว chief commit ไม่ได้ทั้งที่ไม่ได้ชนกันจริง
> Panya จึงสั่งแยกเป็นสองใบ **และปลด `inbox\` ออกจากการคุ้มครองทั้งหมด**

**`LOCK_GAME.txt` (ของคุณเป็นหลัก) คุ้มครอง:**
① พอร์ต server 10188/10189 + process ของ server ② หน้าต่างเกม GameClient
③ canonical DB + สำเนา run copy ④ scenario ที่ server บูตด้วย

**`LOCK_GIT.txt` (ของ chief เป็นหลัก · ปกติคุณไม่ต้องแตะเลย) คุ้มครอง:**
① `git commit` / gate run ② git index/staging ③ การแก้ `.gitignore`/manifest/coverage

- 🟢 **การวางจ็อบลง `inbox\` ไม่ต้องถือธงใดทั้งสิ้น** — สะพานเป็นเลนเดียวเรียงคิวให้เองอยู่แล้ว
  ⇒ chief วางจ็อบ gate/commit ระหว่างคุณเทสอยู่ได้ **อย่าตกใจถ้าเห็นจ็อบ 1xx โผล่มาคั่น**
  (แต่ตั้งแต่ 2026-08-20 จ็อบของคุณขึ้นต้นด้วย `0` จะแซงมันได้ ถ้ามันยังไม่เริ่มรัน — ดูหัวข้อเลขจ็อบ)
- **ไม่ต้องถือธงสำหรับ:** อ่านไฟล์ · วิเคราะห์ · เขียนลงกล่องจดหมาย · เขียน memory ·
  คุยกับ Panya — **ห้าม poll รอธงเพื่อจะเขียน markdown** (เปลืองโทเคนเปล่า ๆ ใช้กล่องจดหมาย)
- **ต้องถือ `LOCK_GAME.txt` ก่อน:** บูต server · เปิดเกม · แตะ DB/สำเนา
- **เลขจ็อบกันชน:** chief = **1xx** · คุณ = **9xx** (เคยเลือกเลข 142 ชนกันมาแล้ว)
- 🔴🔴 **คิวสะพานเรียงตาม *ชื่อไฟล์* (`Sort-Object Name`) ไม่ใช่เวลาที่วางจ็อบ**
  ⇒ **ขณะคุณถือธง `LOCK_GAME.txt` ให้ตั้งชื่อจ็อบเป็น `0` + เลขเดิม** เช่น `0940_gt027_teardown.ps1`
  เพราะ `'0' < '1'` ⇒ **แซงจ็อบ `1xx` ของ chief ที่ยังรอในคิวเสมอ** (ตัวนับเดินต่อชุดเดิม ห้ามรีเซ็ต)
  ขณะ**ไม่ได้**ถือธง ใช้ `9xx` เหมือนเดิม
  ⚠️ แซงได้เฉพาะจ็อบที่ **ยังไม่เริ่มรัน** — ถ้า chief เริ่ม gate+pytest ไปแล้วต้องรอจนจบ (เคยรอ ~14 นาที)
  ✅ ปลอดภัยกับ `TEMPLATE_teardown_generic` — มัน glob `*_client_info_*.txt` ตัวใหม่สุด ไม่ผูกเลขจ็อบ
- **ตอนจับ:** เขียน `HELD` + holder = "เซสชันหลัก ATTENDED" + plan + บรรทัดบอกรอบ scheduled ว่าห้ามแตะ bridge
- **ตอนปล่อย:** `RELEASED` + `done:` / `head:` (**canonical DB sha ถ้าเปลี่ยน ต้องประกาศตัวหนา**) /
  `next:` / `warn:` — chief อ่านตรงนี้เป็นหลัก
- **เกณฑ์ตัดสินว่า holder ตาย:** อายุ ≥20 นาที **และ** ไม่มีสัญญาณชีพใน ~20 นาที — สัญญาณชีพ =
  ไฟล์ใหม่ใน `outbox\` **หรือ** `git status` worktree ขยับ **หรือ** ไฟล์ธงใบนั้นถูกแตะ
  · 💓 ระหว่างถือธงให้แตะ/อัปเดต `HEARTBEAT:` ในไฟล์ธงอย่างน้อยทุก ~5 นาที
  🔴 **ครบทั้งสามอย่างนิ่งถึง takeover ได้** (เคย takeover ผิดมาแล้ว: รอบ 76 ให้ลูกมือทำงาน 43 นาที
  เขียนผลลง worktree ไม่ใช่ outbox → ดูเผิน ๆ เหมือนตาย)
- ระหว่างคุณถือ LOCK ทำเทส **chief ยังทำงาน static/ลูกมือของมันต่อได้** (นโยบายอนุญาตแล้ว) —
  มันแค่ห้ามแตะ bridge/server/DB/commit · อย่าแปลกใจถ้าเห็น worktree ขยับระหว่างคุณเทส

## ขั้นที่ 2 — bridge jobs

วาง `.ps1` (**ASCII ล้วน**) ใน `inbox\` → bridge รันตามลำดับชื่อ → `outbox\` → ย้ายไป `done\`

1. **เปิด GameClient จาก job = บล็อก bridge จนหน้าต่างเกมปิด** → ลำดับที่ถูก: วาง boot job →
   รอ log โผล่ใน outbox (ตัว .ps1 จะค้างใน inbox ตลอดช่วงเกมเปิด — ปกติ) → **แล้วค่อยวาง teardown
   ต่อคิว** → teardown รันเองทันทีที่เกมปิด
2. **อย่าเขียน job ใหม่จากศูนย์** — ใช้ `staged\` ที่ chief เตรียมไว้ หรือ copy จาก `done\`
   (boot มาตรฐาน: ตระกูล `072_gt001_boot` · teardown: `073` · boot ที่มีธง scenario: `080/087/090/097`
   — บูตตรงด้วย Start-Process 'py' เพราะ `run_foundation_visible.ps1` ไม่รับธงเพิ่ม)
3. **🔴 sha gate ใน staged job ล้าสมัยได้เสมอ** — canonical sha เปลี่ยนทุกครั้งที่มี session ใหม่/migration
   → เช็คค่าใน LOCK ล่าสุดก่อนรัน ถ้าไม่ตรงให้ `sed -i` แก้ค่าใน staged job แล้วค่อยวาง (เจอมาแล้ว 2 รอบ)
4. **info file: ห้ามใส่ path ที่มี space แบบ k=v คั่น space** — parse ขาด (บั๊กซ้ำ 069, 081)
5. teardown: parse `-split '\s+'` → **PID guard ด้วย ProcessName + StartTime** ก่อนยิงสัญญาณ →
   Ctrl+C ผ่าน `pf_stop_visible_server.py` → นับ markers (`stopped ×1`, traceback 0, stderr 0B,
   listeners 0) → อ่าน DB AFTER → **อย่า fail บน sha ที่คาดว่าเปลี่ยน**
6. job อ่าน DB ต้องใช้ URI `mode=ro` · ถ้า job อ่านพัง ผู้เทสอ่านซ้ำเองได้: copy .sqlite3 ไป /tmp แล้วเปิด read-only
7. **inbox มี job ค้างของรอบอื่น = ห้ามวางทับ** · bridge เงียบนาน = อาจเข้าโหมด Select (QuickEdit) →
   บอก Panya กด Enter/ESC ในหน้าต่าง console (มี watchdog สตาร์ทใหม่เองทุก ≤5 นาทีแล้ว)
   🔴 **โหมดพังที่เจอจริง 2026-08-19 16:51 (รอบ 89):** process สะพาน **ยังอยู่** แต่ **loop หยุด**
   — จ็อบรันเสร็จ เขียน outbox แล้ว แต่ไฟล์ไม่ถูกย้ายไป `done\` และไม่หยิบจ็อบถัดไปอีกเลย 40 นาที
   (คอนโซลที่เปิดแบบเห็นหน้าต่าง ถ้าคลิกโดนจะเข้าโหมด Select แล้วบล็อกที่ `Write-Host`)
   **เช็คเร็วสุด:** ไฟล์ค้างใน `inbox\` + `bridge_loop_state.txt` เก่า = ค้างแน่นอน
   **แก้:** คลิกหน้าต่าง PF BRIDGE กด ESC · หรือปิดทิ้งให้ watchdog เปิดตัว hidden ใหม่

## ขั้นที่ 3 — สิทธิ์เกม

- เช็ค `list_granted_applications` ก่อน — **สิทธิ์ติดเซสชันแชท**: ถ้าเซสชันนี้เคยได้แล้ว ไม่ต้องขอใหม่
  แม้เกมจะถูกปิด/เปิดหลายรอบ
- `request_access(["GameClient.local.bin"])` ได้ผลเฉพาะ **(ก) เซสชัน attended** + **(ข) ขณะหน้าต่าง
  'Pirate Force' เปิดอยู่** → dialog ขึ้นจริง Panya กด Allow ได้ tier full ทั้งเซสชัน
- ขอตอนเกมไม่เปิด → `notInstalled` เงียบ ๆ ไม่มี dialog · **scheduled run ขอไม่ได้เลยทุกกรณี**
  และ UI "เพิ่มแอปใน task settings" **ไม่มีจริง** (เช็คแล้ว) → อย่าเสนอทางนั้นอีก

## ขั้นที่ 4 — ขับ UI

- 🔴 **ก่อนขับ UI: ลากหน้าต่างเกมไปฝั่งซ้ายของจอเสมอ** — หน้าต่างแอป Claude อยู่ขวาจอและ
  **มองไม่เห็นใน screenshot ของคุณ** (ซ่อนตัวตอน capture แต่โผล่ตอนคลิกจริง) มันบังปุ่มเกมได้เงียบ ๆ
  คลิกผ่าน gate ปกติแต่ไปโดนหน้าต่าง Claude ไม่มี error (เคยทำให้สรุปผิดว่า "client ไม่รับ X")
  · ลากด้วย `left_click_drag` ที่ title bar — **จุดปล่อยห้ามตกบน desktop icons/taskbar**
  · ห้ามสรุปว่า "client ไม่ตอบสนอง" จนกว่าจะย้ายหน้าต่างแล้วเทสซ้ำ
- ใช้ `computer_batch` รวม action ที่คาดผลได้ + จบด้วย screenshot · `zoom` อ่านปุ่ม/ข้อความเล็ก
  ก่อนตัดสินใจ — **อย่ากดปุ่มที่อ่านไม่ออก**
- หน้าเลือกเซิร์ฟเวอร์: คลิกชื่อ server + channel ก่อน แล้วกดปุ่ม "เข้า" ซ้ายล่าง ·
  **หน้าต่างเกมขยับ/เปลี่ยนขนาดได้ ยึดภาพล่าสุดเสมอ**
- dialog PVP → ปุ่มซ้าย = ยืนยัน
- หน้าเลือกตัวละคร: **ปุ่มกลาง**จาก 5 ปุ่มแถวล่าง = เข้าเกม · ปุ่ม 2 จากซ้าย = สร้างตัวละคร ·
  ⚠️ **ปุ่มแรกซ้ายสุด = ลบตัวละคร** (โน้ตเก่าที่ว่าปุ่ม 2 คือลบ = ผิด — ยืนยันด้วย zoom แล้ว GT-010)
- เกณฑ์ "เข้าแมพแล้ว": HP bar + minimap + ชื่อแมพมุมขวาบน + chat `[ระบบ] : Pirate Force local
  server online` + **จดพิกัด X,Y มุมจอทุกครั้ง** (ได้หลักฐาน persistence ฟรี)
- แชท: **คลิกช่อง input ใหม่ทุกครั้งก่อนพิมพ์** (focus หลุดหลังกด Enter) · zoom ยืนยันข้อความ
  อยู่ในช่องก่อน Enter · จดเวลากด Enter ไว้เทียบ timestamp ฝั่ง server
- delete flow (GT-010): ปุ่มลบ → dialog ใช่/ไม่ (ไม่มีช่องพิมพ์ชื่อ) → **dialog รหัสผ่านขั้นสอง
  พร้อมคีย์บอร์ดสุ่มบนจอ** (พิมพ์ด้วยคีย์บอร์ดจริงได้)
- คลิกขวาในเกม = หมุนกล้อง · เดิน = คลิกพื้นซ้าย
- ออกเกม: **ทางหลักคือ X มุมขวาบน** (ในแมพ → dialog ยืนยัน ปุ่มซ้าย · ที่หน้า char select →
  ปิดทันทีไม่มี dialog) · ปุ่ม logout ในเกมใช้ได้**เฉพาะเมื่อเป็นเป้าของเทสนั้น**และ server บูต
  ด้วยธง logout scenario — ไม่มีธง = client freeze ต้อง End task · **X ใช้ได้เสมอแม้หลังกด logout**
- client ค้าง/เงียบ: อ่าน GAME_LIVE/console ก่อน **อย่าคลิกวนซ้ำ** · ถ้าต้องรอคนปิดเกม บันทึกสถานะ
  ลง LOCK แล้วรอได้ — job ใน inbox รันเองเมื่อ bridge ปลดบล็อก

## ขั้นที่ 5 — วินัยหลักฐาน

- แยกสองชั้นเสมอ: **client-observable** (ตาเห็น) กับ **wire/DB** — ห้ามใช้ชั้นหนึ่งอ้าง claim ของอีกชั้น
- SQL มาตรฐาน (คอลัมน์จริง): นับ session `WHERE selected_character_id IS NOT NULL` (ห้าม `count(*)` เปล่า)
  + จด `max(lease_generation)` ก่อน/หลัง · ตำแหน่ง `characters c JOIN character_positions p ON
  p.character_id = c.id` · กระเป๋าอยู่ใน `character_backpack_items` (baseline `[1@0,2@1,4@3]`) ·
  **`sessions.id` เป็น hex — เอาแถวล่าสุดต้อง order by `opened_at`**
- เฟรมที่ไม่รู้จัก: lookup `pf_bridge\VITAL_REGISTRY_FROM_CLIENT_BINARY_*.tsv` ก่อน · เก็บ hex +
  timestamp + path ให้ chief decode — **ห้ามตั้งชื่อ semantic เอง** · grep ASCII = 0 ไม่ได้แปลว่า
  ไม่มีเฟรม (ข้อความบนสายเป็น UTF-16)
- ทุกผลต้องมี **nonclaims** · **ผลลบ = ผลที่มีค่า** บันทึกเต็ม · แยก "สังเกตการณ์" ออกจาก "พิสูจน์เหตุ"
- ตัวเลข mention ใน console มี baseline ไม่ใช่ศูนย์ — อย่าใช้ "mentions > 0" เป็นหลักฐานพฤติกรรม

## ขั้นที่ 6 — ส่งผล (ผ่านกล่องจดหมาย ไม่ต้องรอ LOCK)

1. เขียนไฟล์เดียวลง `pf_bridge\notes_to_chief\<YYYYMMDD_HHMM>_gt-results.md` ประกอบด้วย:
   - GT ไหนบ้าง + สถานะที่ควรเป็น (`[PASS]`/`[FAIL]`/`[DONE]`) + วันเวลา + HEAD ที่เทส
   - `result:` block เต็มของแต่ละตัว **แยกชั้น client-observable / wire-DB** + jobs ที่ใช้ +
     backup path + sha เก่า→ใหม่ + **nonclaims**
   - บทเรียน/บั๊กเครื่องมือที่เจอ (chief จะได้ซ่อม template)
2. **ไม่ต้องแก้ GAME_TEST_QUEUE.md หรือ CHIEF_CONTINUATION.md เอง** — chief ยกไปแปะให้เอง
   (ถ้าจำเป็นต้องแก้จริงและถือ LOCK อยู่แล้ว ให้ Read ส่วนนั้นใหม่ก่อน Edit เสมอ อย่า Write ทับทั้งไฟล์)
3. อัปเดต memory (HEAD, sha, ผล GT, บทเรียนใหม่)
4. ปล่อย LOCK พร้อม done/head/next/warn — ตรวจก่อนปล่อย: inbox ว่าง · listeners 0 · GameClient 0
5. **อย่าประมวลผลเทสเป็น report/commit เอง** — วงจรคือ: ผลในกล่อง → chief ประมวล → commit

## บทมือเขียนแทน (เมื่อ Panya เคาะคำตัดสิน)

1. ดึงตัวเลือกจริงจากไฟล์มาสรุปให้ Panya แบบภาษาคน + เสนอ default ที่ chief เอนไว้ แล้วถามผ่าน
   **AskUserQuestion** · **ถ้าการ์ดไม่ขึ้นหรือ Panya ตอบเป็นข้อความ ให้ใช้คำตอบนั้นทันที อย่ารอการ์ด**
2. เขียนคำตอบลง **กล่องจดหมาย** (ไม่ต้องรอ LOCK) — บล็อกต้องมี: เวลาที่ตอบ (บอกว่าเป็นเวลาประมาณ),
   ช่องทาง, ผู้เขียน (มือเขียนแทน), เนื้อหาคำตัดสิน + เหตุผลของ Panya (สำคัญ — chief ใช้ตีความงานต่อ)
3. ทำไมต้องละเอียด: chief เคยปฏิเสธบล็อกคำตัดสินเพราะ timestamp ไม่สอดคล้อง mtime — provenance ชัด
   = คำตัดสินมีผลทันที ไม่เสียรอบ
4. สิ่งที่ Panya "รับปากจะทำเอง" ยังไม่นับว่าทำแล้ว — จดเป็น "ยังไม่ยืนยัน"
5. ถ้าคำตัดสินเปลี่ยน**นโยบายทีม**: แก้ที่ prompt ของ scheduled task เป็นหลัก
   (`update_scheduled_task`) แล้วสำเนาลงกล่องจดหมาย — prompt คือตัวบังคับจริง ·
   **การแก้ prompt ที่มาจากความคิดคุณเอง ต้องเสนอ diff ให้ Panya ดูก่อนเสมอ**

## โหมด dry-run

ถ้าขอ "วางแผนอย่างเดียว" / "อ่านอย่างเดียว" / "dry run": ทำขั้นที่ 0 เต็ม + รายงานสถานะจริง
(LOCK, GT ค้าง, HEAD, sha) + ลำดับที่จะทำ — **ห้ามเขียนไฟล์ ห้ามวาง job ห้าม request_access
ห้ามแตะเกม** ทั้งสิ้น

## เช็คลิสต์ก่อนจบทุกเซสชัน

- [ ] ผลเทส (รวม nonclaims) อยู่ในกล่องจดหมายครบทุก GT ที่แตะ
- [ ] canonical DB sha ใหม่ (ถ้าเปลี่ยน) ประกาศใน `LOCK_GAME.txt` + กล่องจดหมาย + อัปเดต `CANON_SHA.txt`
- [ ] inbox ว่าง · listeners 0 · GameClient process 0
- [ ] ธงที่ถืออยู่ (`LOCK_GAME.txt` / `LOCK_GIT.txt`) = RELEASED พร้อม done/head/next/warn
- [ ] memory อัปเดต
- [ ] บอก Panya สั้น ๆ: ผลอะไร ค้างอะไร ใครต้องทำอะไรต่อ
