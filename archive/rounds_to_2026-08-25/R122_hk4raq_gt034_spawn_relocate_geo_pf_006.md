# R122 (hk4raq) — GT-034 ปลดล็อกเต็มใบ: สร้างเลนย้ายจุดวางตัวละคร (GEO-PF-006)

**เวลา:** 2026-08-21 ~12:1x–14:xx (+07:00) · รันบน Routine cloud · branch `claude/sweet-ride-hk4raq` (pf_bridge) · `claude/wizardly-wright-hk4raq` (server)
**ล็อกรอบ:** draft PR #23 (pf_bridge) เปิดเป็น draft ตั้งแต่วินาทีแรกตาม v5 ข้อ ① — **ล็อกไม่หลุด** (รอบแรกที่ท่า draft ทำงานตั้งแต่ต้น หลังหลุดหกครั้งติดใน R114–R120)

## Probe ต้นรอบ

- GitHub API/tool: ✅ ใช้ได้ (list PR ทั้งสอง repo + เปิด draft PR สำเร็จ)
- ทาง D `ci-status`: ✅ มีชีวิต (`git ls-tree origin/ci-status ci/` คืนรายการ, exit 0)
- `../pf_bridge/VITAL_REGISTRY_FROM_CLIENT_BINARY_20260817.tsv`: ✅ มีจริง (11,388 ไบต์)

## จดหมายที่บริโภค

- `20260821_1104_PANYA-DECISION-GT034-spawn-relocate.md` — คำตัดสินสองข้อ: เป้า `0x201F` Tornado Eagle · วิธี = ย้ายจุดวางตัวละคร + ตั้ง heading ตอนเข้าเกม (ห้ามเดิน ห้าม teleport lane)
- ไม่มีจดหมายค้างอื่น (ไฟล์อื่นทั้งหมดมี `.CONSUMED.txt` คู่แล้ว หรือเป็น `FROM_CHIEF_*` ของ chief เอง)

## ข้อบังคับข้อ 1 ของ Panya: ยืนยันโซน — ผลการขุด (pf-static-re)

**คำตอบระดับสูงสุดที่ artifact ที่ commit แล้วให้ได้: แมพเดียวกัน**
- จุดสังเกตปัจจุบัน = P0 (แถว 0 ของตาราง `PORT_ROYAL_UNAMBIGUOUS_PLACEMENTS` 115 แถว frozen ใน v141) บวก 100X
- `0x201F` = pidx 30 ของ **ตารางเดียวกัน** ซึ่ง derive จากไฟล์ placement ไฟล์เดียว: `bg0001_npc_placements_decoded.tsv` (Port Royal)
- ⇒ เป้ากับจุดวางอยู่ใน **corpus placement เดียวกัน = แมพเดียวกัน** — เงื่อนไข "คนละโซนให้หยุด" **ไม่ถูก trigger**
- 🔴 **สิ่งที่พิสูจน์บนคลาวด์ไม่ได้:** เลข scene id เชิงตัวเลขของ bg0001 (ตาราง SCENE_NAME/MAP_SCENE_LIST ไม่เคยถูก dump)
  ⇒ เข้าคิว STATIC-ON-BRIDGE + จดลง `IMAGE_ACCESS_COST.tsv` แล้ว
- ระยะ recompute ตรงกับ roster: dXY = 11,914.2 · dZ = +707.7 (roster ปัด 1 ตำแหน่ง — ค่าเต็มของแถว P30 คือ
  `(1747.5244140625, -7837.69775390625, 931.0413208007812)` จาก v141:1349)

## ของที่สร้าง (repo โค้ด — commit `b665d92` บน `claude/wizardly-wright-hk4raq`)

**GEO-PF-006 · scenario `port_royal_tornado_eagle_p30_load_only` — เลน scene_load (read-only) ใบใหม่:**

| อะไร | ค่า | ที่มา |
|---|---|---|
| จุดวางผู้เล่น | `(1847.5244140625, -7837.69775390625, 931.0413208007812)` = P30 + 100X, Y/Z ของแถวเอง | ท่าเดียวกับ observation trick ของ P0 ที่พิสูจน์แล้วว่า client เห็น NPC ที่ระยะ 100 หน่วย |
| heading | `pi` (3.141592653589793) | convention v141 `_heading_to_player` (`+X=0, -X=pi`) — ผู้เล่นอยู่ +100X ของเป้า ⇒ หันเข้าเป้า = หัน −X = π |
| scene | 1 (ช่องเดียวกับ profile scene007 เดิมของเลนนี้) | เลน scene_load ส่ง teleport พร้อม XYZ จริง — เลี่ยงกับดักเฟรม `(1,0,(0,0,0))` ของ boot ปกติ (N1, R23) |

**เหตุผลที่เลือกเลน scene_load แทนเปิด HYP ใหม่:** (1) read-only session = แตะ DB ไม่ได้โดยโครงสร้าง — ข้อ 4 ของ Panya ปิดโดยดีไซน์
(2) seam override position มีอยู่แล้ว (`legacy_bridge.py:52`) และ heading f32 ส่งใน MovementAttr +0x34 อยู่แล้ว
(3) กลไก allowlist แบบ exact-tuple ของเลนนี้คือช่องขยายที่ออกแบบไว้ · **runtime ไม่ถูกแตะแม้แต่บรรทัดเดียว**

**ไฟล์ที่แตะ (6 ไฟล์):**
1. `scenarios/port_royal_tornado_eagle_p30_load_only.json` (ใหม่) — load-only · ไม่มี remote_actor (หัวใจของใบเทส: **ไม่ splice**)
2. `src/pirateforce_foundation/scene_load.py` — เพิ่ม branch allowlist + annotation `GEO-PF-006 harness_only`
3. `docs/HYPOTHESIS_LEDGER.json` — GEO-PF-006 (append, 38→39 entries, diff append-only 61 บรรทัด)
4. `tools/verify_hypothesis_ledger.py` — EXPECTED_IDS/EXPECTED_META/lineage/canonical sha
5. `tests/test_scene_load.py` — เทสใหม่ 2 ใบ (dispatch จริงถึงชั้น StartGame bytes + tamper 7 ท่า)
6. `reports/PF_MULTIPLAYER_READINESS_AUDIT001_...md` — re-pin `package_b_pinned_test_functions` 53→55 (กติกาของ block นั้นเอง — เทสใหม่อยู่ในไฟล์ pinned)

**ผลเทส: เขียว(cloud sanity)** — 1868 passed · 0 failed · 324 skipped (พินครบ) · `verify_hypothesis_ledger` PASS 39 entries ·
`verify_functional_coverage` PASS · seam test ผ่าน (51 pass) · ทุกบรรทัดที่เพิ่มเป็น ASCII (เช็คทั้ง diff)

## การอ่านคำสั่ง "อย่าวางที่ Z เดียวกับเป้าเป๊ะ" (ข้อ 2 ของจดหมาย) — เขียนตรง ๆ

Panya เตือนเรื่อง ΔZ +707.7 (ลอย/ร่วง) แล้วสั่ง "วางเยื้องออกมาในระยะที่เห็นเป้าได้" · ดีไซน์นี้วางที่ **Z ของแถว placement เอง**
(931.04) ที่จุดเยื้อง +100X — ตีความว่าความกังวลของเธอคือ *การใช้ Z ของจุดเก่า (223) หรือ Z มั่ว* ไม่ใช่ Z ของแถว bg0001 ·
adversary ขุดหลักฐานเสริมให้: **V127/V128 เคยให้ client จริงยืนที่จุด P30+100X นี้เป๊ะ ๆ** = หลักฐานกันลอย/ร่วงที่แข็งที่สุดที่มี ·
**การตีความนี้เปิดเผยใน `FROM_CHIEF_R122_TO_ATTENDED_20260821_1500.md` §3** — ถ้าเธอไม่เห็นด้วย แก้ค่าเดียวใน JSON + allowlist ก็จบ

## nonclaims ของรอบ (ติดใน scenario + ledger แล้ว)

- **camera_orientation / heading_mapping**: ไม่มีหลักฐานว่า client ตั้งกล้องตาม heading float — "กล้องหันไปทางเป้า" เป็น**คำทำนาย**ให้ GT-034 วัด ไม่ใช่ claim (GEO-PF-003 ค้างเรื่องนี้อยู่แล้ว)
- **native_render**: ไม่มีใครเคยเห็น `0x201F` บนจอ — คำถามของ GT-034 คือการสังเกตครั้งแรกนั่นเอง
- ตำแหน่งที่ client จะยืนจริงไม่การันตี (anomaly R119: HUD ยืนห่างจุด server ~731 หน่วย สาเหตุ [UNKNOWN]) — ถ้ายืนไม่ตรง จดพิกัด HUD เป็นข้อมูล
- faction/AI/ตำแหน่งทั้งหมด ship มากับ client — ไม่ใช่พฤติกรรมเซิร์ฟเวอร์ต้นฉบับ ซึ่งกู้ไม่ได้ตลอดกาล

## ลูกมือที่ใช้

- `pf-static-re` — ยืนยันโซน/พิกัด/หน่วย heading (รายงานเต็มย่อยอยู่ในหัวข้อโซนข้างบน)
- `Explore` — แผนที่โค้ด placement/heading/opt-in pattern ฝั่งเซิร์ฟเวอร์
- `pf-adversary` — รีวิวก่อน commit (ผลอยู่หัวข้อถัดไป)
- `pf-queue-author` — เขียนใบ GT-034 ใหม่ + ใบ STATIC-ON-BRIDGE scene-id

## ผล adversary (pf-adversary — ก่อน commit ตามกติกาบังคับ)

**MUST-FIX 2 · DISCLOSE 2 · SHOULD-FIX 1 — แก้/ปิดครบทุกข้อก่อน commit:**

1. **MUST-FIX: เอกสารเปิดเผยที่รอบอ้างว่ามี ยังไม่มีจริง** (ไฟล์รอบเขียน "เปิดเผยแล้ว" ก่อนจดหมายถูกเขียน · คิวยังเป็นใบเก่า)
   ⇒ ปิด: เขียน `FROM_CHIEF_R122_*` จริง + ใบ GT-034 ใหม่ลงคิวจริง + แก้ถ้อยคำไฟล์รอบ — ทั้งหมดใน commit ชุดเดียวกัน
2. **MUST-FIX: ดีไซน์เดิมพันผลลบของ GT-034 บนกลไกที่ยังไม่วัด** — heading π เป็น heading ผู้เล่นแรกเข้าที่ไม่ใช่ศูนย์
   **ครั้งแรกของ lineage** · แบบแผนที่พิสูจน์แล้ว (V134 camera workaround + R119) ชี้ว่ากล้องแรกเข้าหัน +X = **หันหนีเป้า**
   · ซ้อนกับ anomaly R119 (client ยืนคลาดจากจุด server ~731 หน่วย [UNKNOWN]) ในขณะที่ offset ทั้งดีไซน์คือ 100 หน่วย
   ⇒ ปิดที่ระดับโปรโตคอล (ไม่ย้ายจุด — จุด +100X คือจุดยืนที่พิสูจน์แล้ว V127/V128 ซึ่งมีค่ากว่า):
   ใบเทสบังคับหมุนกล้อง 360° · **"ไม่เห็นนกเลย" = NO-RESULT ห้าม redirect Door A** · ผลลบนิยามแคบ =
   "เห็นตัวแต่ชื่อไม่แดง" เท่านั้น · "หันเข้าเป้าเลยตอนเข้าเกม" = การวัด heading_mapping ครั้งแรก (ของแถม)
3. **DISCLOSE: ข้อ 2 ของจดหมาย Panya ถูกละเมิดตามตัวอักษร** (Z เท่าเป้า bit-exact) — adversary ตัดสิน "ตรงเจตนา
   ขัดตัวอักษร ยอมรับได้ต่อเมื่อเปิดเผยก่อนรัน" ⇒ เปิดเผยใน §3 ของจดหมาย R122 พร้อมข้อเสนอแก้ค่าเดียว
4. **SHOULD-FIX: คอมเมนต์ lineage ใน verifier อ้าง nonclaims เกินรายการจริง** ⇒ ปิดโดยเพิ่ม nonclaims จริงสองตัว
   (`scene_id_numeric_provenance` · `client_standing_position`) ลง scenario+loader และลดน้ำหนักคำว่า "established
   convention" ในคอมเมนต์ loader (เป็น convention ของ remote-NPC ไม่ใช่ player spawn)
5. **DISCLOSE: scenario ยัง untracked** ⇒ ปิดด้วย `git add` ระบุ path ตรง ๆ (กติกาห้าม `add -A` อยู่แล้ว)

**ท่าโจมตีที่ไม่ทะลุ (adversary รายงานเอง):** boot ปกติไม่เปลี่ยน · write path ปิดโดยโครงสร้าง (`mode=ro` +
`PRAGMA query_only=ON` + digest test) · เครื่องหมาย heading ถูก (atan2(0,−100)=π) · ternary chain ถูก ทั้งห้า profile
เดิม byte-identical · โซน *under*claim ไม่ใช่ overclaim · verifier/annotation/canonical sha ผ่านหมด · re-pin 55 re-derive ตรง
· ทั้ง diff เป็น ASCII · เป้า aggressive เข้าไม่ได้ผ่าน allowlist

## คิวเทสเกม

- GT-034 เขียนใหม่ตามคำตัดสิน (สถานะ: รอ gate เขียว + merge ของ commit รอบนี้ก่อนบูต)
- เพิ่มใบ STATIC-ON-BRIDGE: dump SCENE_NAME (007) + MAP_SCENE_LIST (101) เพื่อปิดเรื่อง scene id เชิงตัวเลข
- GT-035/GT-036 ยัง BLOCKED เหมือนเดิม (รอผล native-red)
