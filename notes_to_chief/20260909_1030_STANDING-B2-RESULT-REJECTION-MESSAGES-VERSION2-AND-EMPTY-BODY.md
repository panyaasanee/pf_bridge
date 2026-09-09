งานเป้าหมายยืน — ยังไม่มีเลขใบ ขอให้ LANE-K ตั้งเลขและผูกจดหมายนี้
B2a · ปิด 2026-09-09T10:30:28.557449+07:00 · ItemOperateVitalRes rejection messages / empty reply body · IMAGE+DATA · PARTIAL
ADDRESSEE: LANE-K · cc LANE-DB, LANE-CS, chief
BUILD_PROPOSED: คำตอบปฏิเสธการสวมใส่พร้อมเหตุผล โดยคงข้อมูลกระเป๋าเดิม | LANE-DB + LANE-CS | proof: owner ทดลองของผิดเงื่อนไข เห็นข้อความที่ตรง MESSAGE และของยังอยู่ช่องเดิม; ระบุ reply/capture/DB ก่อน–หลัง

BUILD_IMPACT: ต่อครึ่ง reply ที่ยังเปิดของ RE-305 / GT-272: ให้ผู้เล่นทราบเหตุผลที่ใส่ไม่ได้; proof และผู้รับผิดชอบตาม BUILD_PROPOSED ข้างบน.

[MEASURED A / IMAGE] ตรวจ raw status ครบ 256 ค่า
ItemOperateVitalRes nominal 0x4C13, vt F30668.v18=5EDA20, v1C=5EF5E0. Handler อ่าน byte+30 → 5A8A00(global app+590); status0 ไป success bag path 5A8AA1. Nonzero: 5A8A63 sign-extend, decrement, unsigned compare20; selector 21 bytes@5A9A88 → jump table@5A9A78:
• raw 1,3,4,5,6,7,8 → MESSAGE 33.
• raw 15 → MESSAGE 3.
• raw 21 → MESSAGE 327.
• raw 2,9–14,16–20,22–255 → epilogue 5A9A4C; ไม่มี message call ใน branch นี้. raw128–255 เป็น signed negative และหลุด unsigned bound. ไม่เรียกว่า “reply ไม่มีผลทุกระบบ”.
ทุก nonzero branch ข้าม success bag application ใน 5A8A00; ไม่ได้ย้อน transaction ฝั่ง server.

[MEASURED A / IMAGE + DATA] เหตุผลและปลายทางข้อความ
5A8A97→5CBC00: table UTF16 MESSAGE@F0FB74, fields n_TYPE@F0C760, n_NOTIFY_TYPE@F2D51C, s_MESSAGE@F0FB60; table และ presence ของทั้งสามฟิลด์ต้องมี. 5CBCDC→5C9FE0(string,0x100000,n_TYPE,n_NOTIFY_TYPE).
TEXTDATA_TH__MESSAGE.tsv 907 rows (hashในmanifest):
• ID33 type35 notify0: “ไม่ตรงตามเงื่อนไข ไม่สามารถใช้ได้!”
• ID3 type35 notify0: “ช่องว่างในกระเป๋าไม่เพียงพอหรือจำนวนไอเทมดังกล่าวมีถึงจำนวนจำกัดแล้ว！”
• ID327 type2 notify0: “สถานะในปัจจุบันไม่สามารถดำเนินการได้!”
35=0x23: bit1 routes SystemMessage→Main_Chat, bit2→Main_MESSAGEBOX, bit0x20 invokes ASCII UI_Fail through 401270→A2B990. type2 routes Main_MESSAGEBOX only among these branches. Window lookup/creation must succeed; UI rendering/audio playback not observed. No per-status distinction proving level/class/wrong-kind: statuses1,3–8 share generic text; original server reason enum remains unknown.

[MEASURED A / IMAGE] Reject still calls second helper
5EF60E ALWAYS→5C6D20(global app+4E0,&bag14,&vector18), without status argument. bag==null → 5C6D34 jumps directly to return5C6E5C. Nonnull bag: first map28..40 iterates ItemAttr template30 + identity28/2C→5C5D70; second map48..60 identities→5C6280. Second map is inside bag, not the separate reply vector. 5C5D70 prefix contains writes matched by template: node+2C=1 and identity+18/+1C (5C5E8C/AE/B1). Thus a nonzero status does not globally suppress supplied bag effects. Exact manager semantics/remaining nested callees not promoted here.

[MEASURED A / IMAGE] Version and fresh/reused object guards
F30668.v14=5ED480→5EC730; both fresh5EC794 and reused5EC812 call ctor5EBED0. ctor clears bag14, vector ctorB13AE0 clears begin/end24/28, sets byte10=2 at5EBF3E. v10=5EBF70 reads nominal registered ID1082018. Prototype allocation/ctor→5F3DF0 visible at5EE4D2..5EE501; callback execution/config readiness is not a runtime result.
5EDA20 writes and reads status08/1, bag-present0B/1, then vector-count08/1. Absent bag leaves freshly cleared14 null; count0 adds no vector record. Nested decoder5F3E20 uses factory and compares wire version with object10 (mismatch E0000031). IMPORTANT: nested ItemReply version2; outer RuntimeRes version4 (B1f); neither is version0.

[PROPOSED D] Minimal rejection, reconstructed codec BODY only
`0b02 120100 12134c 0b02 0801 0b00 0800 0b00` =18 bytes for raw status1. Offsets0 base-mask,2 nested-count,5 nested-id,8 nested-version,10 status,12 absent-bag,14 empty-vector,16 derived-mask. All tags are real bytes. Change status VALUE byte11 to15 or21 for those message families. No fabricated identity or item payload needed in this subset. Empty derived mask skips the actor-collection reconcile call on a fresh outer object; outer handler can do other work.
Shape/tag/version proof A; choice status1 for a server validation failure and the 18-byte composition D. Excludes outer opcode/version/length/compression/encryption. This is not a captured original frame, not a send-ready transport frame, and not a native acceptance pass.

Drag restoration remains OPEN: RE305 letter e88013ca… says items returned without any server reply, but its observation/time limitations and evidence grade remain as published. This round did not re-audit captures or observe the screen. Static rejection consumer above has no proven drag-restoration contract. Next B2b traces drag release/cancel and item presentation separately; do not make error reply wait/rollback assumptions from the word “reject”.

Rerun: Python -B staged/standing_b2a_verify.py. PASS 33 spans/22 code ranges/7 input hashes/27 calls/41 pins/5 vslots/6 typed widths/256 statuses/3 DATA rows/18-byte golden/255 body roundtrips/26 scoped negatives. Tests only exercise offline reconstruction; malformed subset rejection is not the full native protocol parser.
Manifest staged/standing_b2a_manifest.json SHA 18fd2e1fb3ad80f8c0b6a52f8532a47c26eec55a9cf0eac5029ff7cd8942c781. It pins each VA start/end-exclusive, file offset, span SHA, exact input SHA, DATA rows and body. IMAGE SHA 9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623 (14,759,424 bytes), checked before/after.
Search five domains: matched FILES external15 / gamedata0 / reference14 / archive27 / consumed3, query and paths in standing_b2a_search.log. DATA0 only means that initial query missed; targeted MESSAGE read supplied rows above. Queue has no eligible work; standing B2 advanced under owner continuous-work order.
Independent adversary /root/a6f_review: no material defect after independent switch, message arguments/strings, fresh+reuse state, bag side effects and nested framing checks; actual verifier exit0. Drag-vs-reply discrimination remains open.
nonclaims: no new runtime/client/server, pixels, persistence, original server policy, transport, successful equipment, global side-effect absence, or proven drag bounce. สูตร/การเลือก policy ของ payload นี้เป็นดีไซน์ของเรา ไม่ใช่เซิร์ฟเวอร์ต้นฉบับ. ไม่แก้ queue/reference/ServerProject/DB/Git/lease.
SCOREBOARD: NONE | Standing B2 IMAGE evidence | no runtime promotion
