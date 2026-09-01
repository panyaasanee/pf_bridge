[ถึง: chief, LANE-GM, LANE-B · cc: Panya, COO · จาก: OpenAI Codex · 2026-09-01 14:39 +07:00]

# CODEX CHECKPOINT — GM / monster color / ground drop รอบที่ 5

สถานะ: `LOCAL-AUTHORITATIVE / RELEASED FOR TEAM READING / NOT COMMITTED`

## ทำอะไรไป

1. ปิด RE-191 ระดับ conditional static: palette 61/62/63และ parser/apply routeมีหลักฐานครบแบบแยก IMAGE/DATA; ส่งผลเฉพาะกิจใน `20260901_1439_CODEX-RE191-RESULT-FONTSTYLE63-RGBA.md`
2. ขยาย GM เป็น 19 rows; ปิด immediate slot4-return uses, เพิ่ม exact gate-ID/pair integrity และแก้ proposalจาก read-only literalเป็น writable process-lifetime buffer
3. ขยาย drop DATA structure: reachable mesh 34/34มี material/texturing/external DDS refs; ไม่ยกเป็น runtime bind/pixels
4. ตรวจโค้ด ServerProjectที่ Claudeเปลี่ยนแบบ read-only: `mob_combat.py`/`mob_loot.py` pin driftเป็นการขยับ/เพิ่ม accessorที่ไม่เปลี่ยน relevant producer/lifetime contracts; refreshเฉพาะ external pinsพร้อม guard
5. ส่ง urgent warningว่า `GT-188` pass wordingอนุญาต label-only false green; Codexไม่แก้ queueเอง
6. ทำ adversarial review → corrective re-review → read-only `--check` ของทั้งสามสาย exit 0; ไม่มี lock/stageค้าง; IMAGE hashไม่เปลี่ยน

## สถานะจำนวน

- Main Attr field/status/scope: เปลี่ยน `0` แถว; semantic `UNKNOWN 42`, scope `UNKNOWN 210` คงเดิม
- GM: `18 -> 19` rows = IMAGE `16 -> 17`, DATA 2
- Color: `64 -> 66` rows = IMAGE `56 -> 58`, DATA 8
- Drop: คง 29 rows = IMAGE 23 / DATA 3 / CAPTURE 3; DATA-003 semantic coverageเพิ่มโดยไม่เพิ่มแถว

## Conflict ที่กระทบการต่อสายจริง (เรียงตามผลกระทบ)

1. `GT-188` ยังอาจ PASSด้วย label/ฝุ่นโดยไม่มี item model; ต้องให้ non-text modelที่ STEP-Aเป็น preconditionและตาม objectเดียวถึง STEP-C
2. Foundation positive actor identitiesยังเข้ากลุ่มที่พา selectorไปชมพู; ห้ามแก้ spawnจุดเดียว ต้องมี W↔P seamและครบ 19 writers/references
3. Style 62/61/63 ปิด paletteแล้ว แต่ live trigger/tree/gates/pixelsยังไม่ปิด; อย่าเขียนว่า “สีแก้แล้ว”ก่อน STEP-A/B/C
4. GM `GMUI_1` เป็น compatible DATA binding ไม่ใช่ original DLL return; slot4 mutability/retentionยังต้อง runtime validate
5. GM objectถูก client scalar-deleteด้วย MSVCR90; allocation/CRTผิดทำ clean shutdown crash
6. PRESERVE heartbeatรักษาได้เฉพาะ client entryที่มีแล้ว; มันสร้าง modelที่ไม่เคยถูกวาดไม่ได้
7. Serialized DDS refsไม่พิสูจน์ DDS existence/open/decode/bind/sampleหรือ framebuffer pixels
8. Standalone artifactsยัง Git-ignored; Claudeบนเครื่องเดียวกันอ่านได้ แต่ cloneอื่นไม่ได้จน ownerอนุมัติ packaging/allowlist

## ไฟล์ผล

- GM TSV 27,050 B `a5f3fdeb6a830b06e3eb9dceff85fc762459ca3e4f9e7ada152937ef1c898509`; MD 17,377 B `e64e3868736c57ac4abff8a3d5e1f68b4be9d4edbaaebc7d5dd807d9d775e4ae`; pair 777 B `38b3bf4b64a7be30e5a10c73c7253061f5fd46f390e323c9abf940c9fd0b8b92`; generator 113,012 B `dee0ad09a4cd2d74b6369768ea2bef8fc0091a7c7567200a510b56cd738e9f0e`
- Color TSV 110,234 B `8d236351d827a39a74fe9b5e1b9ac694f5f51af5328fcedc1d9f207720bcbaa0`; MD 40,103 B `1550827abd80711236f6345f34af481108a0469cb4feea10aa54c71ed2591165`; pair 529 B `83666a082354444dec686afe54266fc6f6fd23545ba7e5e6216b3bab0f49eb09`; generator 202,548 B `70762a525dabe1f0f50538106e7de130887197680927385d840009db9f6509dd`
- Drop TSV 61,979 B `b1703a7f31c42ddebf9702d12a7942577407fc320a9c2ad8411a08f3f017e710`; MD 20,164 B `87b98759287cf3b452c721f1e216c3614204b87fac322406b8fb8d8941ae7de2`; generator 167,749 B `6ea406b6821e7e36a809e4ccb50860412924dafe05f76ce2c6d729cd8e3cd818`
- Canonical report: `Pirate_Force_Codex_Audit_Recommendations_CHECKPOINT_20260831.md`; pre-edit snapshot: `audit_history\Pirate_Force_Codex_Audit_Recommendations.b96e420c2902_20260901_1434.md`

## สิ่งที่ Claude ทำต่อได้ทันที

- GM: สร้าง x86 DLLตาม exact ABIบนเครื่องมี toolchain แล้ว attended panel/tab/clean-shutdown test
- Color: implement central W↔P projectionอย่างครบ seam แล้ว instrument actorเดียวกันให้เห็น applied 62→61→63และ pixels
- Drop: แก้เกณฑ์ GT-188ก่อน boot; ถ้า STEP-Aไม่มี model ให้ localize callback→DDS bind→scene→rendererแทนการทดสอบ lifetimeของสิ่งที่ไม่มี

Codexไม่ได้แก้ ServerProject/Git/queue/workflow/leaseและไม่ได้รัน client/server/tests.
