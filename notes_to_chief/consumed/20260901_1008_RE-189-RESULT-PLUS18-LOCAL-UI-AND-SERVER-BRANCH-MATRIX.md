[ถึง: LANE-A (ผู้เปิดใบ) · chief · สาย C · COO · cc Panya | จาก: RE runner local · 2026-09-01T10:08:16.082+07:00]

# RE-189 RESULT — DONE / PASS-MIXED · `+0x18` มาจาก local UI; server build matrix ปิดครบหกกิ่ง

- ใบ: `RE-189 LOGOUT-TRANSITION-ORCHESTRATOR-WRITER-OF-PLUS18-001 [STATIC-ON-BRIDGE]`
- START: `2026-09-01T09:50:35.997+07:00`
- วิธี: static/read-only; ไม่เปิดเกม/เซิร์ฟเวอร์, ไม่จับ `LOCK_GAME`, ไม่แตะ DB/source/queue/external/gamedata/git
- 11-file input manifest SHA-256 `8ff5d8109ad87ea26992250fdca2f755e946c828ef7e505cbc84c9601bcf8f4e`; client image SHA `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`.

## Job 1 — writer ของ `[SystemSetting_LogoutConfirm+0x18]`

**คำตอบ:** writer เดียวใน complete bounded class graph คือ local UI binding ไม่ใช่ inbound/network response.

- vtable `0xF45030` slot `+0x60` -> method `0x719680`.
- method นี้ resolve local UI children ตามชื่อ: `TIME_LOGOUT -> +0x14`, `BUTTON_CANCEL -> +0x18`, `BUTTON_LOGOUT -> +0x1C`, `LABEL_TIP -> +0x20`.
- จุดเขียนคือ `0x7196F8`, bytes `89 46 18`, `mov [esi+0x18],eax`; ค่า `eax` มาจากการ lookup UTF-16 `BUTTON_CANCEL` ผ่าน local UI tree (`0xAA1750`) แล้ว type-chain check (`0xAB73C0` / `0x88F2B0`).
- lifecycle/init `0x719780` เรียก slot `+0x60` ก่อน clear `+0x24/+0x28`; gate `0x719620` อ่าน `+0x18` เท่านั้น. event method `0x719990` ก็อ่าน `+0x18` และเขียนเพียง `+0x24/+0x28`.
- census ครบ vtable 31 slots / 24 unique methods: เมื่อไม่นับ stack operand มี object-relative `+0x18` writer เพียง `0x7196F8`; ไม่พบ inbound message copy/writer ใน graph นี้.

pins:

- writer method `[0x719680,0x719771)`, 241 B, CFG errors/gaps/indirect `0/0/0`, SHA `638ac40b75b5dd7750fc4e1ad0fc61ea5e88a5284d6a02729fadb879586bf0f4`
- writer/source slice `[0x7196B8,0x7196FB)`, SHA `9c2c52a4da6945370934d388ccb12011cd8dc6b1dc99fa11247b2796a032dcb0`
- init `[0x719780,0x71998F)`, SHA `b0a95a08119a7035f42b5839a5a06914b9e35badf945603a81ec3fd829183606`
- gate `[0x719620,0x719672)`, SHA `b11ba6a3189e85e449606502b17e086cd141190c939765a4b2d68e10039af158`
- vtable `[0xF45030,0xF450AC)`, SHA `64146715dc527dd2508f96a88e6a5960162ccf201a51ceabd90e7b785c4cbd97`

**ผลเชิงกลไก:** ไม่มี server response ใดเขียน `+0x18` โดยตรงผ่านกลไกนี้. ประตูจะพร้อมได้เมื่อ local logout-confirm UI ถูก instantiate/bind จนมี `BUTTON_CANCEL`; การออกแบบ body/timer/frame ใหม่ไม่สามารถแทนเงื่อนไข UI นี้ได้. แต่ server traffic อาจกระตุ้น UI ทางอ้อมผ่านกลไกนอก graph ได้ — ใบนี้ไม่อ้าง whole-program impossibility.

**Job 1: CLOSED / BOUNDED-POSITIVE.** method ceiling คือ complete factory+vtable graph; ไม่ exclude pointer-alias store นอก graph ทั้งโปรแกรม.

## Job 2 — server architecture matrix สำหรับหกกิ่งของ GT-033

ตรวจ server `main` HEAD `8346ee8060cc3316c7275d7fa2927e781c4432ae`; แยกชั้น server/wire จาก client-observable.

1. **redirect / hand-back:** `PARTIAL / GAP`. GAME ส่ง ordered frames และ close ได้; LOGIN listener ยังรับ connection ได้ แต่ไม่มี GAME↔LOGIN correlation หรือ genuine hand-back primitive. LOGIN connection เดิมเป็น one-shot (`sent_select`) จึงใช้ซ้ำไม่ได้โดยตรง; ต้องเพิ่ม lifecycle/plumbing หรือให้ client reconnect ใหม่พร้อม protocol ที่มีหลักฐาน.
2. **timer 0/2s/10s/ไม่ปิด:** `BUILDABLE`. profile มี `close_delay_ms` / `post_ack_action`; runtime inject timer และมี no-close profile แล้ว. ค่าใหม่ต้องเพิ่ม allowlisted profile/source เท่านั้น.
3. **กลับลำดับ/ส่งซ้ำ:** `BUILDABLE`. dispatch คืน ordered action list; listener ส่งตามลำดับบน locked TCP stream. reverse/duplicate ต้องเพิ่ม profile/branch เท่านั้น.
4. **0x709E fields ไม่เป็นศูนย์:** `MECHANICALLY BUILDABLE, EVIDENCE-BLOCKED`. encoder รับ body ได้ แต่ current helper/allowlist pin 16-byte zero body; ไม่มี measured producer/field semantics ให้เลือกค่า จึงยังห้ามสร้าง variant.
5. **ปิด LOGIN connection แยก:** `TARGETED-CLOSE GAP`. LOGIN 10188 และ GAME 10189 แยกจริง; source ไม่ได้ proactive-close LOGIN หลัง SelectServerRes — มันอยู่ recv loop จน peer EOF/reset/600s timeout. logout state ถือ closer ของ accepted GAME socket เท่านั้น. managed shutdown มีเพียง undifferentiated all-socket bulk close ตอนหยุดทั้ง server; ไม่มี targeted LOGIN handle/correlation. ต้องเพิ่ม LOGIN registry keyed to handoff/session + targeted close/reset. ไม่อ้างว่า client peer คง LOGIN เปิดอยู่หลัง handoff — static server codeตอบไม่ได้.
6. **ส่งตอน logout dialog เปิด:** `BUILDABLE AS TIMING VARIANT`. server รู้ exact full-form GetWorldInfoVital ที่สัมพันธ์กับ dialog-open และตอนนี้จงใจ no-reply; profile ใหม่สามารถส่ง `0x709E` ณ จุดนั้นก่อน LogoutVital ได้. server ไม่สามารถยืนยัน client UI state; ต้องวัด attended.

สรุป: **กิ่ง 2,3,6 สร้างได้ด้วย architecture เดิม; 4 ส่งไบต์ได้แต่ขาดหลักฐาน; 1 ขาด hand-back lifecycle; 5 ขาด targeted cross-listener control/correlation.** Current A/B มีอำนาจปิด GAME เท่านั้น.

source pins: `runtime.py` SHA `f18670d847df8305da31879f3419c7675edd62018e6618f73ef769ce4da96f35`; `session.py` `0af55dd17a04fed89f8be2a6b8f6444c39b00756bb379c200cc9fa105f082035`; `logout_hypothesis.py` `b57b8cc6a37e36831e49a30a2255052a2e0729f55575b74adf5f94152a8409f9`; current v141 wrapper read-only SHA `2eb05ed2...`; branch source archive SHA `47b04df92272a86b8d05a40766a1815dab6f9302eb18ffdcabe8316d9a29c8bf`.

**Job 2: CLOSED.**

## mandatory search / BUILD_IMPACT

- **ค้น `pf_bridge\external\` แล้ว:** reused full-tree manifest 2,443 files / 758,848,182 bytes / SHA `7c6647ebf4738b168e168f4d44776dc2409ff78845194061d3a9f4f225af5b21`; exact `SystemSetting_LogoutConfirm|0x719620|0xF45030|BUTTON_CANCEL|object+0x18` = ไม่พบ. protocol/serializer artifacts ไม่มี writer binding นี้.
- **ค้น `pf_bridge\gamedata\` แล้ว:** reused full-tree manifest 1,109 files / 15,319,585 bytes / SHA `f06b5d02854f10e50222c8326b6e7038d7a49a4ffdff142e9c5f2cceecf4dead`; exact terms เดียวกัน = ไม่พบ. คำตอบมาจาก image/class graph กับ server source ไม่ใช่ gamedata.

**BUILD_IMPACT:** LANE-A/สาย C สร้างต่อได้เฉพาะกิ่ง **2,3,6** โดยยังต้องวัด client-observable; กิ่ง 4 รอ field evidence; กิ่ง 1/5 ต้อง CORE-REQUEST plumbing ใหม่. อย่าสร้าง response เพื่อหวังเขียน `+0x18`; ถ้าจะทดสอบ gate ต้อง target ช่วงที่ local dialog binding ยังอยู่.

`BUILD_IMPACT_NONE: 0/1`

## nonclaims

1. ไม่ claim whole-program ว่าไม่มี pointer alias ภายนอก class graph เขียน `+0x18`.
2. ไม่ claim ว่า response ไม่มีทางกระตุ้นการสร้าง UI ทางอ้อม; พิสูจน์เฉพาะว่า field นี้ไม่ได้มาจาก inbound payload writer ใน graph ที่วัด.
3. ไม่ตั้งชื่อ MODE `1/4` ว่า exit/char-select.
4. ไม่ claim client เห็น FIN หรือคง LOGIN socket เปิดหลัง handoff; source server กับ client-observable เป็นคนละชั้น.
5. ไม่ claim nonzero 0x709E values จากความสามารถ serializer; byte-capable ไม่เท่ากับ semantic evidence.
6. ผลลบจำกัดที่ exact searches + complete bounded factory/vtable graph; ไม่ใช้ linear disassembler เป็นหลักฐานผลลบ.
7. ไม่มีเกม/server boot, capture ใหม่, DB/source/queue/external/gamedata/git mutation.
