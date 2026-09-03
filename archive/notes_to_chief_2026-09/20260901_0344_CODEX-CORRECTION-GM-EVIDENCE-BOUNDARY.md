[ถึง: chief · LANE-GM · COO | จาก: Codex static RE | 2026-09-01T03:44:14+07:00]

# CODEX CORRECTION 3 — ขอบเขตหลักฐาน GM และ artifact รุ่นที่มีผล

บันทึกนี้แทนที่คำแนะนำเชิง semantic และ hashes ใน `20260901_0254_CODEX-CORRECTION-GM-PLUGIN-ROOT-CAUSE.md` กับ `20260901_0321_CODEX-CORRECTION-GM-MODEL-KEY-GMUI-1.md`; ห้ามแก้สองไฟล์เก่าย้อนหลัง.

## สิ่งที่ถอน

- ถอนประโยคเชิงเด็ดขาดว่า IMAGE พิสูจน์ `GMUI_BASIC` “ไม่ใช่” ค่าที่ DLL เดิมคืน. IMAGE พิสูจน์ได้เพียงว่า literal xref จุดเดียวใน EXE ถูกใช้เป็น child/tab lookup หลัง panel ถูกสร้าง; มันไม่เห็นค่าคืน runtime ของ DLL ที่หาย.
- ถอน hashes รุ่น 03:21: TSV `14581a25…`, MD `b9e28552…`, script `a6532825…`; ทั้งสามไม่ใช่รุ่นปัจจุบัน.
- แก้คำว่า fallback non-NULL เสมอ: fallback non-NULL เฉพาะเมื่อ allocation 4 ไบต์สำเร็จ; branch allocation-failure เก็บ NULL.
- แก้คำว่า complete interface census: ที่ปิดได้คือ direct executable-section member-reference census; copied alias/split-address dataflow ยังเป็น nonclaim.

## สิ่งที่ยืน

**[ORIGINAL EVIDENCE: IMAGE]** loader ใช้ `GameMaster.dll` / `CreateGameMaster`; direct refs `application+0x7C8` มี 15 จุด (read 10 / write 5), `.text` มี raw displacement 16 จุดรวม stack-local ที่ไม่เกี่ยวข้องหนึ่งจุด และ `.code` มีศูนย์. Pinned direct calls คือ slot `+0x00` 1 ครั้ง กับ slot `+0x04` 4 ครั้ง. Slot `+0x04` ถูก consumer ใช้เป็น GUI model basename เพื่อประกอบ `.\Data\GUI\Model\<key>.model`.

**[ORIGINAL EVIDENCE: DATA]** corpus 534 `.model` / 0 subdirectory ไม่มี `GMUI_BASIC.model` ทุก case variant; `GMUI.project` ประกาศ `GMUI_1` และ `GMUI_1.model` มี root `GMUI_1` กับ child `GMUI_BASIC`.

ดังนั้น `L"GMUI_1"` เป็น **[RECONSTRUCTED POLICY — PROPOSED compatible binding]** ที่แข็งแรงสำหรับ DATA ปัจจุบัน ไม่ใช่ original DLL return ที่วัดแล้ว. Acceptance ยังต้องเปิด panel `GMUI_1`, เข้าถึง tab `GMUI_BASIC` และ shutdown สะอาดใน lane runtime ที่ได้รับอนุญาต.

## Artifact รุ่นที่มีผลหลัง adversarial review

- `external/pf_rederive_gm_plugin_gate.py`: 54,640 ไบต์, SHA-256 `c991e68db9a5105b0e9532688d702dcbf447215114a0774d7d35080b837c1100`.
- `external/PF_GM_PLUGIN_GATE.tsv`: 17,569 ไบต์, 15 แถว = IMAGE 13 / DATA 2, SHA-256 `790cb0f2e4f4dc9277226cb569ebaadca2e2eaf11ba59d87a8919e612f5cbffd`.
- `external/PF_GM_PLUGIN_GATE.md`: 10,877 ไบต์, SHA-256 `a3018a03778633ea1ee8e44038c9ecac93ff562f17453d57157da79468fe5d27`.
- write และ `--check` ผ่าน; exclusive lock, atomic replace และ final pair check กัน concurrent-writer false PASS. IMAGE/Data hashesไม่เปลี่ยน.

## Delivery blocker ที่ต้องรู้

สามไฟล์ใต้ `pf_bridge/external` เป็น local-only และถูก ignore ตาม workspace policy. Clone อื่นจะเห็นจดหมายนี้แต่ยังไม่มี artifact จนกว่า chief/owner จะอนุมัติ packaging/allowlist; Codex ไม่แตะ Git ตามคำสั่ง. จึงให้ Claude อ่านผลจากเครื่องนี้/path จริงก่อน และอย่าอ้างว่าไฟล์ถูก ingest ใน repository แล้ว.
