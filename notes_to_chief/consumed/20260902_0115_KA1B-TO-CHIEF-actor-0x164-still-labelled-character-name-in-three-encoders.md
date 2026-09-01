# ถึง chief (แจกต่อ: สายที่ถือ stats/damage/player wire) - `ActorAttr +0x164` ยังถูกเรียกว่าชื่อตัวละครในสามที่

จาก: ka1-B (ผู้ช่วย attended, กะ1) · 2026-09-02 01:15 +07:00
ที่มา `PF_ATTR_CONFLICTS.tsv` — สามแถวสถานะ **`OPEN_SERVER_CODE_SEMANTIC_CONFLICT`** ชี้จุดเดียวกัน

---

## ① ข้อขัดแย้ง

> frozen (`NON_EVIDENCE_SERVER_CODE`): *"optional stats-progression encoder labels `ActorAttr +0x164` as `character_name`"*
> rederived (`PF_ATTR_FIELD_SEMANTICS.tsv`, IMAGE): *"`ActorAttr +0x164` feeds `NameBoard_Player` `LABEL_GUILD` child `+0x5C`;
> ข้อความชื่อตัวละครคือ `BasicAttr +0x28`"*

และ `PF_ATTR_FOR_SERVER.md` เผยแพร่ `+0x164` เป็น **`NameBoard_Player_LABEL_GUILD_text`** พร้อม `server_safe = YES`

แต่ encoder ของเราในสามที่ (stats-progression, damage/HP-link, player-wire helper) **ยังเรียกมันว่า `character_name`**
⇒ สามแถวนี้ยังเป็น OPEN ไม่มีใครปิด

## ② ทำไมเรื่องนี้ควรสะดุดหูเป็นพิเศษ

**นี่คือบั๊กเดียวกับที่เราปิดไปแล้วเมื่อ 28 ส.ค.** — CORE-REQUEST-027 ย้ายชื่อตัวละครไป `BasicAttr +0x28`
หลังผลจากเลน probe และใบหลักฐาน `20260828_0955_KA1B-EVIDENCE-nameboard-3-lines-*`
ที่พิสูจน์ว่าป้ายเหนือหัวมีสามบรรทัดจากสามช่อง (บน = กิลด์ `+0x164` · กลาง = ฉายา · ล่าง = ชื่อจริง `+0x28`)

⇒ **ตัวที่ต่อสายจริงแก้แล้ว แต่ป้ายชื่อผิดยังค้างอยู่ในโมดูลข้างเคียงอีกสามตัว**
นี่คือรูปแบบที่อันตราย: ความเข้าใจถูกต้องแล้ว แต่ชื่อเก่ายังอยู่ในโค้ด
**คนที่มาอ่านทีหลังจะเชื่อชื่อ ไม่ใช่เชื่อใบหลักฐาน**

## ③ ขอให้ทำ

เปลี่ยนชื่อให้ตรง (`+0x164` → guild-label text) **ไม่ต้องแก้พฤติกรรม** ถ้าไม่มีใครส่งค่าลงช่องนั้นอยู่แล้ว
และตรวจว่ามี encoder ตัวไหน**ส่งชื่อตัวละครลง `+0x164` จริงหรือเปล่า** — ถ้ามี นั่นคือของเก่าที่หลุดรอด
CORE-REQUEST-027 มา และจะทำให้ชื่อไปโผล่บรรทัดกิลด์อีก

## ④ nonclaim

ชั้น IMAGE ล้วน · เป็นเรื่องของ `NameBoard_Player` เท่านั้น **ไม่ได้พูดถึงคลาส actor อื่น**
· `server_safe = YES` เป็นการประเมินของ Codex ว่าปลอดภัยจะส่ง **ไม่ใช่ข้ออ้างว่าเซิร์ฟเวอร์เดิมเคยส่ง**
· ผมไม่ได้เปิดสามไฟล์นั้นเองมาไล่ทีละบรรทัด ผู้ตรวจรายงานว่าอยู่ในกลุ่ม stats-progression /
damage-HP-link / player-wire helper **ให้สายที่ถือยืนยันตำแหน่งจริงก่อนแก้**

-- ka1-B
