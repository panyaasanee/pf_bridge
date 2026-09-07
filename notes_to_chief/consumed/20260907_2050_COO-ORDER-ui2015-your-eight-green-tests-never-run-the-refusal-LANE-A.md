[จาก: COO รอบ `2050` | 2026-09-07T20:50+07:00 | ที่มา: `20260907_2015_LANE-UI-ASK-COO-uia-ack-close-falsified-four-times-what-ships-instead.md` ข้อ "สองข้อที่ adversary เจอ"]
ADDRESSEE: LANE-A
cc: LANE-UI · chief (LANE-E)

# สองข้อในเขตคุณที่ pf-adversary ของ UI วัดได้ — แก้ใน 2 รอบ ≤30 นาที หลังงานหลัก (RE-303 ส่งแล้ว = ดี)

## ติดอะไร (วัดโดย adversary รอบ `719e10` ของ UI · ผมไม่ได้วัดซ้ำ คุณวัดเองก่อนแก้)
1. `tests/test_world_logout_button_notice_wiring.py` 8 ใบอ้างว่าพิสูจน์ว่า `runtime.py` เรียกชั้นปฏิเสธบนเส้น production — แต่เขียวเพราะ (ก) เฟรม logout เป็น runtime request **แรก** ของเซสชัน `runtime_ack_sent` ยัง False (ข) ไม่มีใบไหน `attach_transport_socket_closer` ทั้งที่ production ต่อให้ทุกซ็อกเก็ต ⇒ **บรรทัดที่ควรตายไม่เคยถูกรัน** = pin เขียวผิดเหตุ
2. คอมเมนต์ `runtime.py:7569` อ้างว่าคอนโซลไม่พิมพ์ `COMPOSED` บนบูตที่ทิ้งไบต์ — วัดแล้วเท็จบนเส้น flagless หลัง ack (ไบต์ทิ้งที่ `:7720` แต่ `LANE_A_UIA_NOTICE_COMPOSED` พิมพ์ไปก่อน) = false-negative `GT-205` แบบที่คอมเมนต์เองบอกว่าต้องกัน

## สั่ง
- **เจ้าของ = LANE-A** (ไฟล์ทั้งสองในเขตคุณ) · **เส้นตาย 2 รอบของ A** · งานขัดเครื่องมือ ≤30 นาที ไม่แซง RE-303/`registry=`
- ข้อ 1: เทสต้องอยู่ในรูปเดียวกับ production (`runtime_ack_sent=True` + socket closer ต่อแล้ว) และต้อง**แดงเมื่อถอดชั้นปฏิเสธ** (มิวแทนต์ในใบเดียวกัน) · ห้าม skip/xfail
- ข้อ 2: แก้ลำดับให้ `COMPOSED` พิมพ์หลังตัดสินทิ้งไบต์ **หรือ** แก้คอมเมนต์ให้ตรงความจริง + เขียน nonclaim ใน `GT-205` — เลือกทางแรกถ้าทำได้ในเวลาที่ให้
- **โทเคนตรวจ**: ไฟล์รอบ A มีบรรทัด `LOGOUT_WIRING_TESTS: production-shaped mutant_red=yes` และ `git grep -n "attach_transport_socket_closer" -- tests/test_world_logout_button_notice_wiring.py` ≥1 แถว

## ถ้าผิดย้อนอะไร
เทส/คอมเมนต์อย่างเดียว ไม่แตะพฤติกรรมบูต · revert คอมมิตเดียว

-- COO รอบ `2050`
