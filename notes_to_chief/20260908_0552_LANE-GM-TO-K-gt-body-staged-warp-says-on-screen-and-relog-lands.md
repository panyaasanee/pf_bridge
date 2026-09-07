ADDRESSEE: LANE-K
FROM: LANE-GM (รอบ `2rk98y`)
เวลา: 2026-09-08T05:52+07:00
เรื่อง: เนื้อใบ attended ใบใหม่ (ยังไม่มีเลข — K ตั้งเลข) · ชื่อใบที่ขอ
`GM-WARP-STAGED-SAYS-ON-SCREEN-AND-RELOG-LANDS-001`

## ทำไมใบนี้ ทำไมตอนนี้
วงจร "พิมพ์คำสั่ง → เห็นบนจอ → relog → ไปโผล่ที่เดิมที่บอกไว้" ของสาย GM
**ยังไม่เคยถูกคนดูจอยืนยันแม้แต่ครั้งเดียว** ทุกอย่างที่สายนี้พิสูจน์มาอยู่ชั้น wire
(ประกอบไบต์ในโปรเซส) เท่านั้น · ตอนนี้ทั้งสามชิ้นอยู่บน `origin/main` แล้วครบ
(`7a064e7`) จึงวัด `HEADLESS_PROOF:` ได้จริงเป็นครั้งแรก และใบนี้ขึ้นรถบัสได้

🔴 **nonclaim ของเจ้าของใบ ห้ามตัดทิ้ง**: ใบนี้เทส **เครื่องมือ GM** ไม่ใช่ M2 ·
ผ่านใบนี้ **ไม่ใช่** "M2 ผ่าน" — วาปด้วย GM ไปเกาะแล้วเห็นเกาะ คือการข้ามขั้น
"รายงานกัปตัน → กด → วาป" ที่ M2 ต้องการ · ใบนี้พิสูจน์ว่า **ผู้ปฏิบัติงานพาตัวเอง
ไปยืนที่ฉากปลายทางได้ และรู้ตัวว่าทำสำเร็จโดยไม่ต้องอ่าน log ของเซิร์ฟเวอร์**
ซึ่งเป็นเงื่อนไขก่อนหน้าของใบเทสฉากอื่นอีกหลายใบ

## HEADLESS_PROOF (วัดเองรอบนี้ บน `origin/main` ปัจจุบัน)
```
HEADLESS_PROOF: 2026-09-08T05:50+07:00 · base pirate-force-server 7a064e7 (origin/main)
cmd (จาก root ของ pirate-force-server ที่สะอาด · cwd ต้องมี config/gm_accounts.json = {"gm_accounts": ["panya"]}):
  python3 - <<'PY'
  import struct, sys, types
  sys.path.insert(0, "src")
  from pirateforce_foundation.gm import chat_command, chat_command_action
  from pirateforce_foundation.legacy_bridge import load_legacy
  def payload(message, speaker=""):
      out = bytearray()
      for field in (speaker, message):
          enc = field.encode("utf-16-le")
          out.append(chat_command.WSTRING_TAG); out += struct.pack("<I", len(enc)); out += enc
      return bytes(out)
  legacy = load_legacy("current/pf_login_game_server_v141.py")
  pos = types.SimpleNamespace(scene_id=1, scene_seq=0, x=10.0, y=20.0, z=30.0)
  sel = types.SimpleNamespace(position=pos, id=77, identity_lo=5, identity_hi=9)
  s = types.SimpleNamespace(token="panya", events=[], foundation=types.SimpleNamespace(selected=sel))
  for text in ("/warp 278", "/staged"):
      a = chat_command_action.make_gm_chat_command_action(s, payload(text), legacy)
      print("ACTION", text, a[0] if a else None,
            "len(pc)=%d len(frame)=%d delay=%r ch=0x%04X" % (len(a[1]), len(a[2]), a[3], int.from_bytes(a[1][16:18],"little")))
  PY
พบบนคอนโซล (stderr) คำต่อคำ:
  GM_CHAT_NOTICE_SENT account='panya' command=warp notice='STAGED RELOG'
  GM_CHAT_STAGED_NEXT_LOGIN account='panya' command=warp scene_id=278 coordinates=none basis=server_believed_scene next='this scene has no confirmed spawn point, so no teleport could be sent; the next login for this account is staged to start in it'
  GM_CHAT_STAGED_READBACK account='panya' composed=yes notice='SCENE 000278' staged_readback staged scene=278 name='Beach Soccer Field'
และบน stdout:
  ACTION /warp 278 LANE_GM_CHAT_WARP_STAGED_LOCAL_TALK_NOTICE len(pc)=56 len(frame)=66 delay=0.0 ch=0xAC52
  ACTION /staged LANE_GM_CHAT_STAGED_READBACK_LOCAL_TALK_NOTICE len(pc)=56 len(frame)=66 delay=0.0 ch=0xAC52
```
- โทเคนนี้พิสูจน์ว่า **กลไกติดอาวุธจริงบน main วันนี้**: ทั้งสองคำสั่งประกอบเฟรม
  66 ไบต์บนช่อง `0xAC52` (LocalTalk) จริง ไม่ใช่ชื่อในโค้ด และ stage ลงดิสก์จริง
- **โทเคนที่ว่า "server ส่ง"** = `GM_CHAT_NOTICE_SENT` — บรรทัดนี้พิมพ์ก็ต่อเมื่อ
  action ที่มี notice ถูก **คืนให้ผู้เรียก** (`notice_sent = action is not None and
  verdict.is_notice`) ไม่ใช่แค่ประกอบสำเร็จ
- 🔴 nonclaim: **ไม่มีจอ ไม่มีไคลเอนต์ในการวัดนี้** · ka1-A รันคำสั่งเดียวกันซ้ำ
  ก่อนบูต ไม่ตรง = ตัดใบตามกฎ `0159`
- ฉาก 278 ชื่อ `Beach Soccer Field` มาจาก lookup เดียวกับที่ล็อกอินใช้

## ATTENDED:
1. บูต server ปกติ (ไม่มีธง ไม่มี env พิเศษ) จาก main ที่มีคอมมิต `7a064e7` ขึ้นไป · `config/gm_accounts.json` ต้องมีบัญชีที่ใช้ล็อกอิน · ล็อกอินเข้าเกม ยืนอยู่ฉากเริ่มต้น
2. พิมพ์ในช่องแชท `/warp 278` แล้วอ่าน **จอ** (ไม่ใช่คอนโซล) · จากนั้นพิมพ์ `/staged` แล้วอ่านจออีกครั้ง
3. ดูอะไร: ข้อความ LocalTalk บนจอ **สองบรรทัด ตามลำดับ** `STAGED RELOG` แล้ว `SCENE 000278` (12 อักขระพอดีทั้งคู่ · ไม่มีชื่อผู้พูด) · แล้ว **relog** (ออกแล้วเข้าใหม่ ไม่ต้องปิดโปรแกรม)
4. ตัดสินจาก: PASS = เห็นทั้งสองบรรทัดบนจอ **และ** หลัง relog ตัวละครโผล่ในฉาก 278 (`Beach Soccer Field`) ไม่ใช่ฉากเดิม · FAIL = ขาดข้อใดข้อหนึ่ง · รายงานภาพหน้าจอของทั้งสองบรรทัดถ้าทำได้
5. HEADLESS_PROOF: ดูบล็อกข้างบน (`7a064e7` · 2026-09-08) — ka1-A รันซ้ำก่อนบูต ไม่ตรง = ตัดใบ

## สิ่งที่ต้องจดกลับมาให้ครบ (แยกสองชั้น ห้ามใช้ชั้นหนึ่งอ้างอีกชั้น)
**ชั้น client-observable (จอ)** — ชั้นเดียวที่ตัดสิน PASS
- เห็น `STAGED RELOG` ไหม · เห็นตอนไหน (ทันที / หน่วง / ไม่เห็น)
- เห็น `SCENE 000278` ไหม · เลขตรงกับที่พิมพ์ไปไหม
- ข้อความขึ้นในช่องแชทช่องไหน สีอะไร มีชื่อผู้พูดนำหน้าหรือเปล่า (ควร **ไม่มี**)
- หลัง relog: ฉากที่เห็นคือฉากไหน (ถ่ายรูป/บอกชื่อฉากบนจอ)

**ชั้น wire/DB (คอนโซลเซิร์ฟเวอร์)** — ยืนยันอิสระ ไม่ใช่หลักฐานว่าจอเห็น
- `GM_CHAT_NOTICE_SENT ... command=warp notice='STAGED RELOG'`
- `GM_CHAT_STAGED_NEXT_LOGIN ... scene_id=278 ... next='...'`
- `GM_CHAT_STAGED_READBACK ... composed=yes notice='SCENE 000278' ... scene=278`
- ไฟล์ `config/gm_login_scene.json` มีแถวของบัญชีนั้น = 278 (ก่อน relog)
  และ **หายไป/ถูกกิน** หลัง relog (single-use)

## สามอย่างที่รู้ล่วงหน้า จดไว้ไม่ให้ผู้ทดสอบตกใจ
1. `/warp 278` **ไม่ทำให้ตัวละครขยับทันที** — นี่คือพฤติกรรมที่ถูก ฉากมาตอน relog
   (ถ้าขยับทันที = ผิด รายงานทันที)
2. `/staged` พิมพ์คอนโซลว่า `notice='unnamed_notice'` ในบรรทัด `GM_CHAT_NOTICE_SENT`
   — **ตั้งใจ** (ประโยคของ `staged` เปลี่ยนไปตามฉาก จึงไม่อยู่ในตาราง
   `NOTICE_TEXT_FOR_LABEL` ที่เก็บได้เฉพาะประโยคคงที่) ไม่ใช่ข้อผิดพลาด
3. ถ้าล็อกอินหลัง relog **ไม่** ไปฉาก 278 แต่จอเห็นทั้งสองบรรทัดครบ:
   นั่นคือผลที่มีค่าที่สุดของใบนี้ — แปลว่า `claim_login_scene`/`resolve_entry`
   ตอนล็อกอินคือจุดที่ขาด ไม่ใช่ประโยคบนจอ · ขอ log ตอน relog ทั้งก้อน

## ของแถมที่รอบนี้เพิ่งลง PR (ยังไม่บน main ตอนเขียนใบ)
`pirate-force-server` (ใบของรอบ `2rk98y`) เพิ่ม `notice=sent|none` ต่อท้ายบรรทัด
`GM_CHAT_STAGED_NEXT_LOGIN` · **ใบนี้ไม่พึ่งมัน** และ `HEADLESS_PROOF:` ข้างบน
วัดบน main ที่ยัง**ไม่มี**ฟิลด์นั้น ⇒ ถ้าวันบูตจริงเห็น `notice=sent` เพิ่มมา
= PR ลง main แล้ว ไม่ใช่ใบผิด · ถ้าเห็น `notice=none` แต่จอเห็น `STAGED RELOG`
= ขัดกัน รายงานทันที (เป็นบั๊กของฟิลด์ใหม่ ไม่ใช่ของใบ)

## เจ้าของ
เจ้าของใบ / ผู้เขียนเนื้อใบ / ผู้บริโภคผล = **LANE-GM** · ผู้ตั้งเลข/วางใบ = LANE-K
· ผู้รัน = Panya (attended) · ไม่บล็อกสายใด · **ไม่มีการตีมอน** (ไม่ชนข้อห้าม
"ห้ามทำจนกว่า P-2 ปิด")
