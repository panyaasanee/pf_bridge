[ถึง: chief cloud (cc), Claude และ Panya · จาก: OpenAI Codex static RE]

# Checkpoint 13:31 — GM / monster color / ground drop รอบสี่

บันทึกเวลา `2026-09-01T13:41:37+07:00`. Lease ของ ServerProject ยังเป็น `active` โดย `Claude (Cowork)`; `LOCK_GAME.txt` ล่าสุดที่อ่านเป็น `RELEASED: 2026-09-01T10:30:50+07:00`.

## ขอบเขตและสิทธิ์อ่าน

- คำว่า Codex “ไม่แตะโค้ดเซิร์ฟเวอร์” หมายถึง **ห้ามเขียนและห้ามรัน** ขณะ Claude ถือ lease ไม่ได้หมายถึงห้ามอ่าน. Codex อ่าน ServerProject แบบ read-only เพื่อตรวจเทียบ ชี้ semantic conflict และกัน implementation ผิดหลักฐานได้และได้ทำจริง.
- Codexไม่ได้แก้ ServerProject, ไม่รัน tests/server/client, ไม่แตะ Git/workflow/queue/lease และไม่แก้ frozen V141. ฝั่ง replacement serverเป็นของจำลองและไม่ถูกใช้เป็นหลักฐานของพฤติกรรมเซิร์ฟเวอร์เดิม.
- ตรวจ deliverables เดิมก่อนทำและขยาย canonical artifactsสามชุดเดิมเท่านั้น ไม่สร้างตารางคู่ขนานหรือ duplicate output. เขียนเฉพาะ `pf_bridge\external`, note ใหม่นี้ และ canonical reportที่ root `Pirate Force`; ไม่คัดลอก raw proprietary bytesออกมา.

## ผลที่ปิดเพิ่มและตรวจซ้ำแล้ว

1. **GM plugin gate:** 18 rows = IMAGE 16 / DATA 2. `GM-IMG-015` วัด direct `application+0x7C`: raw displacement 16 จุด, true member refs 15 จุด, unrelated ESP local 1 จุด. True refs = writes 5 / reads 10; readsแยกเป็น guards 4, scalar delete 1, inline virtual calls 5 โดย slot `+0x00` 1 ครั้งและ `+0x04` 4 ครั้ง. ไม่พบ direct contextที่ store/return pointer alias. `GM-IMG-016` ปิด three-pointer regionก่อน UTF-16 `%s%s`; 33 executable refsเป็น `PUSH imm32`. Split-address/pointer arithmeticและ aliasesใน external calleesยังเปิด. TSV `68f66cb06a5b8b5565534d97d86a87d16b1de7a10c4efd40443d869fdfcf9d8b`; MD `e9dc72bea1c14af9fca1895bc09d58c1eb3f1995c165d95db8dd92721dd6e4b7`; generator `8ecf9524c6008b849eeafbfbe9df65515c69d6e53220724444e99e94f0585526`.
2. **Monster color gate:** 64 rows = IMAGE 56 / DATA 8. `MCG-IMG-054` ปิด sole direct startup routesไป outer init/loaderของ `.\Data\GUI\Model\BigFontStyle.fsl`; `MCG-IMG-055` ปิด loader semanticsแบบ manual/hash-anchored: clear tree, parse children, wide `ID`→`_wtoi`, รับ signed ID `>0`, allocate/construct 0x78, insert/resolve/store/populate. DATA ปัจจุบันมี 186 entries, 186 unique ordered IDs `1..186`, จึงรวม 56–63. `MCG-IMG-056` ปิด bounded CNetNPC vslot `+0x38`→requested byte 0→conditional actor `+0x258` store. Outer initไม่ใช้ inner-loader failure result; live parse/tree population, invocation, state noun, applied styleและ pixelsยังเปิด. TSV `9869e5899f6a972e264433701d61eb2d739dcdca0ec275372ad63dbaabc74810`; MD `6f24637aaa307cb85977089d140b5ffd9034f6df4995583a1127d60e913057e5`; marker `5bc950d2fc8beb8fe1be2c22c59db9f8fe659d1f894e73c54bb1735d4a3f0a10`; generator `1feec4a2266f0c59592d430e1d27e51efabdc4b58fef3835ad81cf40e5b6a4c9`.
3. **Ground-drop lifetime/resolver:** 29 rows = IMAGE 23 / DATA 3 / CAPTURE 3. `GDL-IMG-021` ปิด bounded native entry→CRT→app-init→callback setterและ exact direct slot refs; runtime execution/order/dominance/computed writesยังเปิด. `GDL-IMG-022` ปิด `wrapper+0x84`→retain→world registration→recursive NiNode activation. `GDL-DATA-003` decode+parse `.ni_` 13 ชุดแบบ deterministic: compressed 31,158 B, decoded 83,400 B, 441 blocks; root `NiNode` 13/13 และ root graphถึง `NiMesh` 13/13; totals reachable NiNode 25 / NiBillboardNode 4 / NiMesh 34 / NiPSMeshParticleSystem 2. นี่พิสูจน์ packaged geometry ไม่ใช่ actual runtime loadหรือ pixels. TSV `d889460b8d4c1c4f69b1df349f59ac2dae950c6373ee170915e5f5f2fa94e059`; MD `266067b57fae3b5cb742eb7c1565210d31e11cfb7ed3586f9ef5f2fa033ecc32`; generator `2e627fe03aac4b78c15f62bdc430a3c5e12a7159a93be0c97d3232a475279f68`.

ทั้งสาม re-deriver `--check` PASS หลัง publish; imageคง 14,759,424 B / SHA-256 `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`. Adversarial re-reviewของ artifactsและ canonical reportผ่านหลังสร้าง noteนี้; ไม่พบ provenance mixingหรือ current overclaimที่เหลือ.

## ข้อความ ServerProject ที่ขอให้ Claude แก้ในรอบเขียนถัดไป

Codexอ่านพบและยังไม่ได้แก้สี่กลุ่มนี้:

1. `tools/pf_mine_scene_drop_tables.py:43-44` — “column explains nothing about drawing” กว้างเกินไป: `n_DROPMODEL_TYPE` เลือก NIF pathโดยตรง แต่ยังไม่เพียงพอให้เห็น geometry.
2. `docs/FUNCTIONAL_COVERAGE.json:911` — ประโยค “nothing ... reads the +0x14 dword” ล้าสมัย; static reader/model selectorปิดแล้ว ควร append correctionโดยไม่ลบประวัติ.
3. `src/pirateforce_foundation/mob_loot.py:546`, `scenarios/combat_loot_001.json:44`, `tests/test_mob_loot.py:1764` — “63 IDS” ต้อง re-deriveและแยก production emit universe ออกจาก externally specified 43-ID audit set; ห้ามเปลี่ยน 63→43แบบเดา.
4. `src/pirateforce_foundation/gm/bt_gm_probe.py:28` — factory `0x007280D0` ไม่ได้พิสูจน์ว่า “constructs GMUI_BASIC”; หลักฐานชี้ panel/model object และ `GMUI_BASIC` เป็น child/tab lookup.

Read-only source pins: Foundation runtime 51 source files; direct actor-type-4 writers 30 = reachable 19 / excluded 11; `runtime.py` SHA-256 `609f273c66a2c58ffa3d95b502e43b98d092e2dd768dcbb8008a8eff2732bae3`; frozen V141 SHA-256 `2eb05ed2fdbdd5ee3d91f7fbb8c1d16a4c7a02a843bc97169b16a389e4ea4c22`.

## สถานะ Attr และตัวปลดล็อกถัดไป

- Main generationไม่เปลี่ยน: `b96e420c290201ce60babec398fd2389ea36db2f2f30ce552d9d680f481f3fae`; 490 field rows; semantic `UNKNOWN 42` (8.57%); scope `UNKNOWN 210`; field-status delta `0`.
- **GM:** static direct-use boundaryแคบลง แต่ยังต้อง owner-authorized x86 DLLและ attended panel→`GMUI_BASIC`→clean shutdown.
- **Color:** static loader routeและ ID availabilityปิดแล้ว; ตัวปลดล็อกคือ same-process proofว่า loader populate live treeและ lookup IDs 56–63สำเร็จ จากนั้นตาม actorเดียวกันถึง requested/applied styleและ framebuffer pixelsของส้ม/แดง/เทา.
- **Drop:** packaged filesมี geometryแน่; ตัวปลดล็อกคือพิสูจน์ actual callback executionและ rootเดียวกันผ่าน runtime load→scene registration→renderer→pixels แล้วจึงวัด same-key lifetime, pickup, expiryและ persistence.

## ส่งมอบ

- Canonical report: `C:\Users\Panya\Desktop\Pirate Force\Pirate_Force_Codex_Audit_Recommendations_CHECKPOINT_20260831.md` — 138,123 B, SHA-256 `227a184572262e8b5b07ba6cba4347c3a009884a318a443f38ddbe4591836d7f`.
- Snapshotก่อนแก้รอบนี้: `C:\Users\Panya\Desktop\Pirate Force\audit_history\Pirate_Force_Codex_Audit_Recommendations.b96e420c2902_20260901_1316.md` — 133,306 B, SHA-256 `4a4ea4f4dba837968acdca390dfc6ccca53b192efdb0419f9918794f90fcefb7`.

สถานะ: checkpoint ส่งให้ทีมอ่านได้; goal static RE ยัง `active` เพราะ end-state runtimeทั้งสามเรื่องยังไม่พิสูจน์ และไม่ได้ประกาศว่าจบงานทั้งหมด.
