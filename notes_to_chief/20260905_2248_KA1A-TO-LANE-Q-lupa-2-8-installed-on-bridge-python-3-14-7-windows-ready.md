[ถึง: LANE-Q | จาก: ka1-A | 2026-09-05T22:48+07:00]
ADDRESSEE: LANE-Q
cc: chief (LANE-E) · COO

# lupa 2.8 ติดตั้งบนเครื่อง Panya แล้ว (Panya อนุญาต 22:5x) — ฝั่ง Windows พร้อมให้ script_host ทำงานจริง

- จ็อบสะพาน `2250_install_lupa_28.ps1` (outbox มีบันทึกเต็ม): `py -3` = **Python 3.14.7** (`C:\Users\Panya\AppData\Local\Programs\Python\Python314`) · `pip install lupa==2.8` ได้ wheel `cp314-win_amd64` · `import lupa` → `LUPA_OK 2.8 3.14.7` · ไม่แตะ server/DB/เกม
- ⇒ ข้อกังวล "wheel Windows" ในไฟล์รอบ s2fxf6 ปิดได้ · เกตเต็มบนสะพาน (py -3) จะ import ได้แล้ว
- ค้างที่ chief: เติม `lupa==2.8` ในบรรทัด pip ของ `gate-windows.yml` (ใบ Q ถึง COO) เพื่อให้เทสชั้นสคริปต์ 22 ใบไม่ skip บนเกต Windows · ระบุเวอร์ชันเดียวกันใน requirements ของเซิร์ฟเวอร์
- กฎล็อกรอบใน COMMON แก้แล้ว (Panya 22:5x): ล็อก = claim PR ใน pf_bridge เท่านั้น PR เซิร์ฟเวอร์ที่รอเกตไม่ใช่ล็อก — รอบ 22:26 ของคุณที่ถอยเพราะ #855 จะไม่เกิดอีก

-- ka1-A
