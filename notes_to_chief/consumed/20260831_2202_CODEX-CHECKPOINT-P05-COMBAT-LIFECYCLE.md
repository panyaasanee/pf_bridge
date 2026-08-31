[ถึง: Claude/chief เพื่อ review · cc: Panya | จาก: OpenAI Codex · 2026-08-31 22:02 +07:00 · corrected_at: 2026-08-31 22:22 +07:00]

# CODEX CHECKPOINT P0-5 — combat/death/animation client lifecycle

**สถานะ:** `CHECKPOINT / PROVISIONAL / HOLD FOR PANYA` — ส่งให้ตรวจอ่านได้ แต่ยังไม่ใช่ ingest, commit, release หรือคำสั่งแก้ ServerProject

ก่อนแก้คำตรวจรับรอบนี้ snapshot guard พบสำเนารายงานก่อนแก้ที่เหมือนกันทุกไบต์อยู่แล้ว จึงไม่คัดลอกซ้ำตามกฎ: `audit_history\Pirate_Force_Codex_Audit_Recommendations.105cc7692579_20260831_1520.byka1B.md` (85,344 bytes; SHA-256 `bbc7ec61cd957535541fd52b63b5d497f23113cd4fa7754c8ace35409eb57658`) รายงานสะสมปัจจุบันมีตราประทับ 4 บรรทัดกับ §0 เพิ่ม/แก้/ถอนครบ

## ผลที่ปิดได้แบบ bounded

- generation: `105cc7692579f0795cd6f3d127790d09a861373b7bec74d487891404162e6113`
- generator SHA-256: `c947274837c233fca722d436a67b207e49a47bf9b240a18a0c5295068dbd1b16`
- artifacts 44 ไฟล์; ผู้ปฏิบัติงานสังเกต local tooling สำเร็จสองรอบได้ generation ID เดิม แต่ไม่มี immutable transcript แยกสองรอบ จึงไม่ใช้จำนวนรอบเป็นหลักฐาน deterministic; independent postpublish reader/hash/size/key/source verification ผ่าน
- `PF_COMBAT_LIFECYCLE.tsv`: 34 แถว = IMAGE 26 + DATA 8; semantic exact 27 / role-only 5 / unknown 2; evidence unique 27 / canonical 2 / explicit reuse 5
- ปิดได้ว่า valid `ActionVital+0x30` ผ่าน behavior lookup ก่อนสร้าง `CActorTask_UseBehavior`; lethal actor-entry dead sync ต้องมี identity เดิมใน actor map ก่อน; `CHitResult` resolve target และอ่าน signed i32 ที่ hit element `+0x08` แต่ gameplay noun/formula ยังไม่ทราบ และไม่มี direct E8 edge ไป pinned HP/death entry points; inbound registry/vtable-bound `TargetVital` slot เป็น no-op
- นี่คือ client partial order เท่านั้น ไม่ใช่ลำดับ original server แบบ end-to-end

## งานที่ยังเปิด

- lifecycle open 8 แถว (`CL-DATA-008`, `CL-IMG-005/009/010/011/022/025/026`): cadence ฝั่ง DATA/IMAGE, hit-reaction label, original flag policy 2 แถว, relative target-panel/name/HP refresh order, CHitResult↔HP arrival order และ original acknowledgement/equipment-dependent behavior selection. Exact original-server death hold เป็น nonclaim นอก census 8 แถวที่ผูกกับขอบเขต `CL-IMG-018` ไม่ใช่ unresolved แถวที่เก้า
- `PF_ATTR_UNRESOLVED.tsv`: 976 = active claims 464 + standalone conflict work 512
- field table เดิมยัง 490 แถว; semantic `UNKNOWN` 42 และ scope `UNKNOWN` 210 ไม่เปลี่ยนจาก P0-4 (`PF_ATTR_FIELD_SEMANTICS.tsv` hash เดิม)
- conflicts 1,285; OPEN 640; `OPEN_SERVER_CODE_SEMANTIC_CONFLICT` 5 = name/guild เดิม 3 + combat lifecycle ใหม่ 2
- probe requests 0; quarantine 0

## สองข้อขัดแย้งใหม่กับ current server code

1. cited `runtime.py:4109-4218` + `mob_combat.py:1633-1680` รับ parsed target-bearing ActionVital โดยไม่มี post-parse `+0x30` check เทียบ visible behavior/action state (`conflict_key=4d48dc31…`). ข้ออ้างจำกัดเฉพาะ cited path ไม่ใช่คำตัดสินว่า production parser ทั้งระบบผิด
2. `mob_combat.py:323,1004,1060` ส่ง CHitResult flags `0x0001`; known IMAGE reaction lane ต้องมี bit 0+bit 3 ติดและ bit 4 ดับ (`conflict_key=bb8832a5…`). **ไม่พิสูจน์** ว่า `0x0009` คือ original-server policy

ไม่มีข้ออ้างว่า “ขาด ActionVital ack” และรอบนี้ไม่ได้แก้ server/workflow/คิวเทส

## การแยกชั้นหลักฐาน

- **[ORIGINAL EVIDENCE: IMAGE/DATA แยกแถว]** lifecycle TSV มีเพียง IMAGE หรือ DATA หนึ่งชั้นต่อแถว; ไม่มี CAPTURE/replacement/owner testimony ปะลงในแถว
- **[CAPTURE EVIDENCE]** census แยกต่างหาก: 2,621 decoded frames เป็น GameClient→local-emulator ทั้งหมด; eligible original-server→client = 0 จึงตอบ original inbound combat orderไม่ได้ และไม่ใช่หลักฐานว่า packet ไม่มีจริง
- **[CLIENT-OBSERVED RESULT]** GT-025 พบว่า DYING_LATCH อย่างเดียวทำให้ flat pose ได้ จึงห้ามเรียกท่านอนว่า `_F_DIE_000`; GT084-R2 วัด 5 double-clicks → 5 ActionVital/5 hits, damage+target flinch, ไม่มี performer attack animation, DYING 20 → hold ~700 ms → DEAD 0, corpse ค้าง ~75 s และไม่มี target panel—เป็น replacement result ไม่ใช่ original policy
- **[ORIGINAL EVIDENCE: IMAGE]** RE-161 ปิด bounded client task chain ว่า actor-entry dead path ไปถึง dead-task creation/queue สำหรับ existing actor. **[RECONSTRUCTED POLICY]** current replacement DEAD full census ใช้เส้นนี้ แต่ task-queue/model-readiness gate ที่หน่วง poseยังไม่ทราบ
- **[RECONSTRUCTED POLICY]** RE-163 ตัดสินเฉพาะ telemetry ของ sender ปัจจุบันว่า `late_ms` เป็น sender-schedule/diagnostic overrun ไม่ใช่ network/client-arrival timestamp

## Hash/size ที่ตรวจหลัง publish

| ไฟล์ | bytes | SHA-256 |
|---|---:|---|
| `PF_ATTR_GENERATION_MANIFEST.json` / internal manifest | 7,622 | `28f2a3f0f7383bf75492c09ac6875d6706faaaa9a0f844fee2ad3a5a0358aaa3` |
| `pf_rederive_attr_semantics.py` | 1,321,270 | `c947274837c233fca722d436a67b207e49a47bf9b240a18a0c5295068dbd1b16` |
| `PF_COMBAT_LIFECYCLE.tsv` | 41,063 | `305b7bdc12e9b638e3c3f37f996af8bb0e2d1877241aaf171885b8fae106b658` |
| `PF_COMBAT_LIFECYCLE.md` | 2,423 | `32d20f8fc8ed66e64644efd55fe1de34c5a0d32cadc0c84aa01c1d5d1f3feacb` |
| `PF_ATTR_UNRESOLVED.tsv` | 2,354,005 | `ab3c84d2d85501e37469d6cbffcbfb181b297e1d4e7024bdd55b72954021f902` |
| `PF_ATTR_CONFLICTS.tsv` | 3,530,362 | `429b4fbd61819c3e964f0e05c10645365adedc4f19a84bbf777fdafb0bcc0578` |
| `PF_ATTR_FIELD_SEMANTICS.tsv` | 1,339,980 | `1418b7559f5b05feef585490e76d33e8f72cd82c1ff854941d7faf37878c7f2f` |

Attempt แรกของ revision ก่อนแก้หยุด fail-closed ก่อน publish ที่ `semantic_report_scope_or_delta_census_mismatch`; authoritative generation เดิมไม่ถูกเปลี่ยน จากนั้นผู้ปฏิบัติงานสังเกต publish/rerun สำเร็จ แต่ไม่มี immutable transcript แยก จึงไม่ใช้จำนวนรอบเป็นหลักฐาน deterministic

## จุดอ่าน

- manifest authoritative: `C:\Users\Panya\Desktop\Pirate Force\pf_bridge\external\PF_ATTR_GENERATION_MANIFEST.json`
- generation directory: `C:\Users\Panya\Desktop\Pirate Force\pf_bridge\external\.pf_attr_generations\105cc7692579f0795cd6f3d127790d09a861373b7bec74d487891404162e6113`
- cumulative audit ที่อัปเดตไฟล์เดิม: `C:\Users\Panya\Desktop\Pirate Force\Pirate_Force_Codex_Audit_Recommendations_CHECKPOINT_20260831.md`

**Delivery nonclaim:** P0-4 checkpoint เดิมยังเป็นประวัติคนละรอบ; ไฟล์นี้คือ checkpoint P0-5 เพียงใบเดียว ไม่ได้ duplicate ตาราง/รายงานหลัก และยัง `HOLD FOR PANYA`
