# R120 (deo6qn) — บริโภค GT-032/033/040 · audit จดหมาย GT-040 + erratum E3-E5 · build HYP-PF-031 (variant C ของ GT-033)

**เซสชัน:** deo6qn · branch `claude/confident-wozniak-deo6qn` (pf_bridge) · `claude/busy-bohr-deo6qn` (server)
**เวลา:** 2026-08-21 ~10:00–1x:xx (+07:00) (~03:00–0x:xxZ UTC)
**ล็อก:** PR #19 (non-draft ตาม v5 ①) ถูก workflow merge ทิ้งใน **11 วินาที** (เปิด 03:00:07Z merge 03:00:18Z)
— **ล็อกหลุดครั้งที่หกติดต่อกัน** (R114-lx6eer, R115, R117, R118, R119, R120) ⇒ ยึดคืนด้วย **draft PR #20** ตาม precedent R115/R117
🔴 **ย้ำข้อเสนอเดิมของ R119 อีกเสียง: v5 ข้อ ① ควรสั่ง "เปิด draft PR" ตั้งแต่แรก** — หกรอบติดที่ non-draft claim ตายใน <1 นาที

## probe ต้นรอบ (ตาม v4 ข้อ PROBE)

| ข้อ | ผล |
|---|---|
| gh CLI | ไม่มี (`gh_exit=1`) — เหมือน R112 |
| GitHub API (MCP) | ✅ ใช้ได้ (list PR ทั้งสอง repo สำเร็จ) |
| ทาง D `ci-status` | pf_bridge: **ไม่มี branch** (ปกติ — repo นี้ไม่มี gate) · server: ✅ มีชีวิต 8 ไฟล์ verdict |
| โครงพี่น้อง | ✅ `../pf_bridge/VITAL_REGISTRY_FROM_CLIENT_BINARY_20260817.tsv` มีจริง (11,388 ไบต์) |

## จดหมายที่บริโภค (4 ใบ — สำเนาลง `consumed/` + stub · ต้นฉบับไม่แตะ)

1. `20260821_0900_GT032-PASS-GT033-BLOCKED-input.md`
2. `20260821_0936_GT040-PART-A-RESULTS-from-assistant.md`
3. `20260821_0951_GT040-PART-B-RESULTS-from-assistant.md`
4. `20260821_0956_GT040-PART-C-RESULTS-from-assistant.md`

## งานที่ทำ

### ① GT-032 → ✅ PASS ลงคิวแล้ว + ตอบคำถาม event ที่ผู้เทสถาม (สืบเองในโค้ด)

ผู้เทสถาม: เกณฑ์ในคิวบอกให้ดู event `npc_hostile_hypothesis_player_faction1_start_game_sent`
ใน console ก่อนยิง แต่ grep ทั้งล็อกแล้ว **= 0 ครั้ง** ทั้งที่ผลเป็นบวก — (ก) ชื่อผิด (ข) faction มาทางอื่น (ค) hostility ไม่ต้องพึ่ง faction?

**คำตอบ (วัดจากโค้ด):** เป็น **(ก) ในความหมาย "เกณฑ์ของ chief สังเกตไม่ได้โดยโครงสร้าง"** —
- event ชื่อนั้นมีจริงและถูก append ที่ `runtime.py:1947` แต่ `self.events` เป็น list ในหน่วยความจำ
  **ไม่มีบรรทัดใดใน `src/` พิมพ์มันออก console** — ตัวพิมพ์เดียวคือ `[G>] label (N bytes)` ที่
  `current/pf_login_game_server_v141.py:7762` ซึ่งพิมพ์เฉพาะเฟรมขาออก ⇒ grep ไม่เจอ = ปกติ
- **pairing ครบสองข้างพิสูจน์ทางอ้อมได้แน่น:** dispatch ของ HOSTILE_SPAWN มี guard
  `if not self.npc_hostile_player_faction_start_sent: refuse "..._player_faction_not_applied_no_reply"` (ไม่มีไบต์ออก)
  ⇒ การที่เฟรม HOSTILE_SPAWN ออกไปได้ = faction-1 StartGame ถูกส่งแล้วจริง
- ทางเลือก (ค) ตกไปด้วยหลักฐานเก่า: arena-v2 นับ 1,023 ครั้งว่า NPC faction 6 เดี่ยว ๆ vs ผู้เล่น faction 0 = เป็นกลาง
- เกณฑ์ในคิวถูกแก้แล้วในบล็อกผลของ GT-032 · ข้อค้าง "ขอบแดงมาจาก hostility หรือ Tab" ยกเป็นเกณฑ์แถมรอบใหญ่หน้า (อยู่ใน GT-043 ด้วย)

### ② audit จดหมาย GT-040 สามใบ (ลูกมือ pf-static-re เทียบกับ artifact ที่ commit แล้ว) → erratum E3-E5

ผลใหญ่ที่ไม่มีใครเห็นมาก่อน: **จดหมายท่อน B ไม่ได้หักล้าง CHUNK2-Q2 จริง** —
- gaplist §4.2 ลอกคำ CHUNK2-Q2 มา**ผิดฟังก์ชัน**: CHUNK2-Q2 ชี้ cache-diff `[0x01081A90]+0x154` ที่ `0x5DCB40`
  (สเตจ merge ก่อน bind ใน handler `0x5E4060`) แต่ gaplist เอาไปแปะกับ `0x446F30` (reconcile ที่ `0x5E4085`) — คนละลูก
- ท่อน B สแกนแค่ `0x446F30` แล้วไม่เจอ `0x01081A90` ⇒ หักล้างได้แค่**ถ้อยคำของ gaplist** ไม่ใช่ CHUNK2-Q2
  (ท่อน B ไม่เคยเปิด `0x5DCB40`) · `remote_player_hypothesis.py:60-65` ถือ attribution ที่ถูกอยู่แล้ว ไม่ต้องแก้โค้ด
- ลง **ERRATUM R120 สามข้อ** ใน `FACTPACK_R100_INREPO_LOOT_SPAWN_GAPLIST.md`:
  **E3** แก้ mis-attribution (ความผิดเป็นของ gaplist ไม่ใช่ CHUNK2-Q2 และ supersede คำขอของท่อน B ที่ overreach)
  **E4** บันทึกกลไกจริงของ `0x446F30` = generation stamp + gate bit `0x02` (ของใหม่ — เดิมอยู่ในลิสต์ "explicitly not examined")
  **E5** ประตู 4: serializer `PickupTerrainThing` ถูกปักแล้ว (vtable `0xF3005C` · `0x5E5E30` · handler `0x5EF640` สองทาง)
  — ทั้งหมดติดป้าย "รอ GT-042 re-derive แบบปฏิปักษ์" · ห้าม encoder จนกว่าจะปิด
- ผล audit ที่เหลือ: ตาราง bit→offset, vtable family marker, single-caller `0x5E4085`, registration `0xBEE5E0/E1/E5`
  (สามที่อยู่ในทังก์เดียว ไม่ขัดกัน), id `0x4543` [DERIVED] — **AGREES ทั้งหมด** · หลายรายการเป็น NEW-NO-RECORD (เติมของใหม่)

### ③ GT-033 → 🔴 BLOCKED-INPUT ลงคิวแล้ว + build variant C: HYP-PF-031 LOGOUT-CHAT-PUSH-001

ผู้เทสคลิกรายการ `ออก` ในเมนู HOME ไม่ติด 4 ครั้ง (Return ก็ช่วยไม่ได้ — ไม่ใช่ปุ่ม default)
⇒ client ไม่เคยส่ง LogoutVital ⇒ variant A/B ไม่มีวันได้รัน ⇒ ตามข้อเสนอผู้เทส ("ยิงจากคำสั่งแชต"):
**variant C** = scenario opt-in ใหม่ — trigger ด้วยแชต ascii12 (ท่าเดียวกับ GT-032 ที่ผู้เทสทำได้แน่)
แล้ว server **push** `ReturnSelectServerVital 0x709E` (เฟรม 48 ไบต์แช่แข็ง sha256 pin เดิมของ HYP-PF-028)
**โดยไม่รอ request** — ตอบคำถามว่า transition ต้องการ request pairing ไหมในตัว
· pre-approved ใต้ policy #3/#4 (ปุ่ม gameplay + pattern มาตรฐาน: opt-in · fail closed · ledger · headless proof)
**สถานะ:** [จะเติมเมื่อลูกมือ implement รายงาน]

### ④ คิว + งานแม่บ้าน

- GT-032 ✅ PASS · GT-033 🔴 BLOCKED-INPUT + บล็อก variant C · GT-040 ✅ DONE (ผลยังไม่ re-derive → GT-042)
- ใบใหม่: **GT-042** (re-derive GT-040 A/B/C + decode `0x402A20` ปิด scope `[mgr+0x24]`) · **GT-043**
  (observation แถม: ประชากรรอดไหมหลังเฟรม count-1 bit `0x02` — จาก decode ท่อน B เฟรมพวกนี้ควรกวาดประชากร
  แต่ไม่เคยมีใครรายงาน wipe · yes/no ตัดสินได้ทั้งคู่) — [สถานะ: จะเติมเมื่อ pf-queue-author ส่งร่าง]
- `IMAGE_ACCESS_COST.tsv` +2 แถว (scope `[mgr+0x24]` ต้องอิมเมจ · id จริง `PickupTerrainThing` ต้องอ่านตอนรัน)

## สิ่งที่ไม่ได้พิสูจน์ / nonclaims

- ทุกข้อเท็จจริง GT-040 เป็นชั้น wire/static และ**ยังไม่ผ่าน re-derivation แบบปฏิปักษ์บนอิมเมจ** (GT-042)
- audit ของรอบนี้เทียบ "จดหมาย vs สิ่งที่ commit แล้ว" เท่านั้น — ถ้าทั้งคู่ผิดเหมือนกัน audit จะมองไม่เห็น
- HYP-PF-031 พิสูจน์ได้แค่ headless ชั้น wire — client transition หรือไม่ = คำถามของ GT-033 variant C (attended)
- ไม่ claim ว่า `0x709E` ของเรา = ของเซิร์ฟเวอร์ต้นฉบับ ซึ่งกู้ไม่ได้ตลอดกาล
