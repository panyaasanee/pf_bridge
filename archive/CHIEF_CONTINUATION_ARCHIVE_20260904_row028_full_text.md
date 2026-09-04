# CHIEF_CONTINUATION.md CORE-REQUEST registry row 028, full text (wired, closed)

Moved verbatim by chief round ub8svt (2026-09-04) to keep
CHIEF_CONTINUATION.md under the 30 KB ceiling. Row 028 was already fully
wired and verified merged before this move -- nothing about its status
changes, only where the full wording lives.

- 028 CORE-REQUEST-GM-047 (สาย GM รอบ `bxkxfc` · P0 · `COO-DECISION 20260901_0741`) — cross-scene GM warp label ไม่เคยเรียก resync ตำแหน่ง (`runtime.py:5304` เดิมเช็คเฉพาะ `WARP_ACTION_LABEL`) เสี่ยง DB position เพี้ยนถ้ารัน `GT-182` ก่อนแก้ · แก้รอบ `ts0deo`: เช็คสมาชิกสามป้าย (`WARP_ACTION_LABEL`/`WARP_CROSS_SCENE_TELEPORT_ACTION_LABEL`/`WARP_CROSS_SCENE_NO_COORDS_TELEPORT_ACTION_LABEL`) ที่ `runtime.py:5304` + เทสถดถอยใหม่ที่พิสูจน์ผ่าน dispatch จริง (ยืนยันเทสล้มบนโค้ดเดิม 1!=2, ผ่านบนโค้ดใหม่) · **ต่อแล้ว (wired) — ยืนยันรอบ `69r41m` (R283)**: `pf_bridge#680` merged `2026-09-01T01:19:23Z`, `pirate-force-server#452` merged `01:27:10Z`, ทั้งคู่ยืนยันด้วย `pull_request_read get` (ไม่ใช่ `list_pull_requests`'s `merged` field ซึ่งอ่านผิดเป็น false — tool quirk เดิม) + อ่านโค้ดตรงจาก `origin/main:runtime.py:5304` เห็น `_GM_WARP_LABELS` สามป้ายจริง · ปลด `GT-182` จาก `BLOCKED-PENDING-GM047-FIX` เป็น `BLOCKED-ON-ATTENDED [NEEDS-ATTENDED-CAPTURE]` แล้วรอบนี้
