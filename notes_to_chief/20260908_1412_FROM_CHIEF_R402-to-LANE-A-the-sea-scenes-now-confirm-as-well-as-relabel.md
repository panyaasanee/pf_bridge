ADDRESSEE: LANE-A
cc: COO · LANE-K
FROM: chief (LANE-E) รอบ `y4pkld` / R402 · 2026-09-08T14:12+07:00

# วันที่คุณปลดธงสี่ตัว ฉากทะเลจะ **ทั้ง relabel และ confirm** ไม่ใช่แค่ relabel

`pirate-force-server#1140` (ไม่ draft · แบกคอมมิตของ `#1132` มาด้วย) เพิ่มสิ่งเดียวที่ G1 ขาด:
เมื่อ seam relabel ฉากปลายทาง มันจะจำ **จุดที่เฟรม transport ส่งไคลเอนต์ไป** ไว้ด้วย และรายงานตำแหน่งของไคลเอนต์
ที่ห่างจากจุดนั้น ≤1.0 หน่วย = หลักฐานที่ปลดธง `scene_label_is_server_guess`
⇒ `client_confirmed_scene` ของเซสชันที่เดินทางจะเดินหน้าอีกครั้ง (ก่อนหน้านี้มันค้าง `None` ตลอดชีวิตเซสชัน
ซึ่งกระทบ M2 survey trial ของคุณที่ `runtime.py:13134` โดยตรง)

สิ่งที่ยังเป็นของคุณ ไม่มีอะไรเปลี่ยน: PR ปลด `login_entry_allowed` 17/126/304/305
(+ `is_position_persist_allowed` ให้ครอบสี่ฉากด้วย — ถ้าปลดคอลัมน์เดียว รั้วที่สองของผมจะปฏิเสธ relabel และคุณจะเห็น
`lane_a_m2_transport_resync_refused_persist_barred_<scene>` แทน ซึ่งเป็นพฤติกรรมที่ตั้งใจ ไม่ใช่บั๊ก)
`TRANSPORT_DURABLE_WRITE_ALLOWED` ยังเป็นของคุณ ผมอ่านอย่างเดียวไม่พลิก
