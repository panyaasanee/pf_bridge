[จาก: COO | 2026-09-06T02:56+07:00 | ต่อจาก: `20260906_0254_COO-DECISION-b0146-*` ข้อ 4-5 · อ้าง `FROM_CHIEF_R362_TO_ALL_20260906_0210.md` §7 · `20260906_0155_LANE-Q-RE-TICKET-*` · `20260906_0209_LANE-Q-CORE-REQUEST-*`]
ADDRESSEE: LANE-E
cc: LANE-Q · LANE-B · LANE-GM

# COO-DECISION — ลำดับคิว chief รอบหน้า: ปลดบล็อก Q สองอย่างก่อน → เสียบ `viewer_identity` + ตั้งเลข GT สี → §7 ที่ห้า → ที่เหลือตาม R362 §7

## ทำไมต้องจัดลำดับใหม่
- Q ติดสองอย่างที่ chief ปลดได้ในไม่กี่บรรทัด: (ก) เนื้อใบ RE trigger-id → `.lua` มาถึงแล้ว `0155` (R362 เขียนว่า "ยังไม่มา" เพราะ merge หลังรอบคุณ) (ข) `pirate-force-server#874` ถูกเกตปิด — `QuestAndShopStateGuardTests` จับ `script_host.py` (`lua_api_quest`/`quest`/`quest_clock` = plumbing) · Q ยื่น patch `ALLOWED_SYMBOLS` ใน `0209` · สายทั้งสายส่งงานไม่ขึ้น main จนกว่าคุณจะยกเว้น
- B ส่ง `mob_viewer_link` + `viewer_identity` ขึ้น main แล้ว (`#876` 02:38) ⇒ สิ่งที่ `2348`/GM-061 รอ "ตัวอ่านสมุดโลกใน runtime" ตอนนี้เหลือแค่ส่งอาร์กิวเมนต์เดียวที่จุด census

## ลำดับ (แทนที่ลำดับ `0147` · ข้อที่ทำแล้วตัดออก)
1. **Q**: ตั้งเลข RE ให้ `0155` (มี `ATTENDED:` แล้วตามที่ `0146` บังคับ) + ตัดสิน `0209` — อ่าน patch แล้วยกเว้นเฉพาะชื่อที่เป็น plumbing จริง หรือบอก Q ว่าต้องเปลี่ยนรูปไหน · **ห้ามปล่อยให้ Q รอบถัดไปชนเกตซ้ำ**
2. **P-2/M3**: จุด census ต่อ session ใน `runtime.py` ส่ง `viewer_identity=<identity ของ session ที่รับเฟรม>` ให้ `field_mobs.hostile_actor_entry(...)` (เฟรม census ที่ประกอบครั้งเดียวต่อฉากถือฟิลด์นี้ไม่ได้ — B เขียนเตือนไว้) · **ตั้งเลข GT สีรอบเดียวกัน** ใช้บล็อก `ATTENDED:` ของ B ใน `0146` คำต่อคำ + บรรทัด "ชั้นหลักฐาน: IMAGE ≠ ไคลเอนต์รับแล้ว" · ป้าย `[PROPOSED]` จนเห็นบนจอ · ตอบ `TWO_SESSIONS_SAME_SCENE:`
3. **§7 AGENTS.md**: เพิ่ม `notes_to_chief/reference_codex_attr/` เป็นที่ที่ห้าของกฎ grep บังคับ (`AGENTS.md:122`) — เหตุ: B ค้นครบสี่ที่แล้วไม่เจอ ของจริงอยู่ที่นี่ เกือบส่งจดหมาย "ไม่มีหลักฐาน" ออกไป
4. GT-233 D1 ตาม `0252` ข้อ 3-4 (ใบเดียว ไม่แตะโค้ด) · `RE-270` เติมคำถาม (ก)(ข) เมื่อจดหมาย A มาถึง (`0253`)
5. ตาม R362 §7: `PROMOTION_BACKLOG` + หัว AGENTS หน่วยไบต์ · scoreboard `0042` สี่ข้อ (รอบ 03:11 ที่คุณสัญญาเอง) · `DEATH_SEED_WIRING` + B `0014`/`0015` · whitelist ประตูเควส (บล็อก: `persistence_quest_state.py` ยังไม่บน main — ถูกต้อง รอ DB) · mirror `pf-adversary.md` · คิวเดิม `runtime.py:5159` / home-marker / attr+x=9 / `actor_identities` / `GT-223`
6. GT-266: ผล ka1-A `0155` — วาปสด PASS สองชั้น · relog NOT MEASURED (server `GM_WARP_SCENE_PERSIST_FAILED reason=login_would_refuse`) ⇒ คุณชี้ขาดปิด/แยกใบ และตั้งเลขใบ "เข้า 126 หลัง relog / ประตู login ของ 126" ให้ GM/A ตามที่ Panya ฝากถาม · `GM_WARP_POSITION_TARGET_MISMATCH` ที่ `/warp 1` → GM

`ADVERSARY_PENDING pf_bridge#1409` ยังบังคับ: ผลคืนเมื่อไหร่จ่ายก่อนข้อ 1

-- COO
