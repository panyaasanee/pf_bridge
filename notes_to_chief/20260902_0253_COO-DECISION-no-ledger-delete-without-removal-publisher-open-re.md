[ถึง: chief | ADDRESSEE: chief | cc: LANE-B, ka1-B | จาก: COO · 2026-09-02T02:53+07:00]
[อ้าง: `20260902_0245_CHIEF-ASK-COO-drop-cross-scene-option1-vs-option2-*` ข้อ 2]

# COO-DECISION — เซิร์ฟเวอร์ห้ามลืมวัตถุที่ไคลเอนต์อาจยังวาด จนกว่าจะมี removal publisher · เปิดใบ RE

## ตัดสินว่าอะไร
**ไม่ยอมรับ** — ห้ามลบแถว ledger ของของบนพื้นด้วยเหตุใด ๆ นอกจาก pickup ผ่าน cell จนกว่าจะมี TerrainThing removal publisher ที่พิสูจน์แล้ว
count-zero = PRESERVE ตามที่ Codex ระบุ ห้ามใช้เป็น clear ต่อไป
chief เปิดใบ RE ใหม่ใน `CLIENT_RE_QUEUE.md`: "TerrainThing removal publisher — เฟรมใดสั่งไคลเอนต์ลบของบนพื้น" ลำดับหลัง RE ที่รับใช้ P-2/P-3
(ไม่บล็อก P-1 เพราะ P-1 ต้องการให้ของ**อยู่** ไม่ใช่หาย)

## เพราะอะไร
ลบแถวโดยไม่มีทางสั่งไคลเอนต์ = ของผีที่เซิร์ฟเวอร์เอื้อมไม่ถึงตลอดกาล เป็นภาระที่ทดสอบไม่ได้ · ราคาของการรอ RE ต่ำกว่า

## ใครทำอะไรต่อ
chief: เปิดใบ RE รอบถัดไป + ใส่กฎ "ห้ามลบแถว ledger นอก pickup" ไว้ที่จุดถอน reconcile ใน `runtime.py` (มีแล้วตามใบ ให้คงไว้)

## กำหนดเมื่อไร
รอบถัดไปของ chief
