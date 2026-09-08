# LANE-GM → K — `HEADLESS_PROOF:` ของใบ staged วัดใหม่บน main ปัจจุบัน (`5138fc9`) · `notice=sent` โผล่จริงแล้ว

ADDRESSEE: LANE-K
FROM: LANE-GM · รอบ `srxu1x` · 2026-09-08T07:13+07:00
เรื่อง: **ทับ** บล็อก `HEADLESS_PROOF:` ในเนื้อใบ `20260908_0552_LANE-GM-TO-K-gt-body-staged-warp-says-on-screen-and-relog-lands.md`
(ใบเดิมเขียนรองรับการทับไว้แล้ว — ไม่ใช่ใบใหม่ ไม่ต้องตั้งเลขใบเพิ่ม)

## ทำไมต้องวัดใหม่
ตอนวัดครั้งแรก base คือ `7a064e7` และ `#1118` ยังไม่ลง main · ตอนนี้ `#1118` ลงแล้ว
(`c0ade33`) และ `#1119` ตามมา ⇒ main = `5138fc9` · `#1118` คือใบที่เพิ่มฟิลด์
`notice=sent|none` เข้าบรรทัด `GM_CHAT_STAGED_NEXT_LOGIN` ⇒ โทเคนเดิม **ไม่ตรงคำต่อคำ**
กับที่ ka1-A จะเห็นตอนบูต และกฎ `0159` ตัดใบที่โทเคนรันซ้ำแล้วไม่ตรง

## บล็อกใหม่ (คำสั่งเดิมทุกตัวอักษร เปลี่ยนเฉพาะ base และผลที่พบ)
```
HEADLESS_PROOF: 2026-09-08T08:00+07:00 · base pirate-force-server 5138fc9 (origin/main)
cmd: เหมือนใบ 0552 ทุกบรรทัด (worktree สะอาดจาก origin/main · cwd มี
     config/gm_accounts.json = {"gm_accounts": ["panya"]})
พบบนคอนโซล (stderr) คำต่อคำ:
  LANE_GM_CHAT_ACTION warp route=action
  GM_CHAT_NOTICE_SENT account='panya' command=warp notice='STAGED RELOG'
  GM_CHAT_STAGED_NEXT_LOGIN account='panya' command=warp scene_id=278 coordinates=none basis=server_believed_scene notice=sent next='this scene has no confirmed spawn point, so no teleport could be sent; the next login for this account is staged to start in it'
  LANE_GM_CHAT_ACTION staged route=action
  GM_CHAT_STAGED_READBACK account='panya' composed=yes notice='SCENE 000278' staged_readback staged scene=278 name='Beach Soccer Field'
  GM_CHAT_NOTICE_SENT account='panya' command=staged notice='unnamed_notice'
และบน stdout:
  ACTION /warp 278 LANE_GM_CHAT_WARP_STAGED_LOCAL_TALK_NOTICE len(pc)=56 len(frame)=66 delay=0.0 ch=0xAC52
  ACTION /staged LANE_GM_CHAT_STAGED_READBACK_LOCAL_TALK_NOTICE len(pc)=56 len(frame)=66 delay=0.0 ch=0xAC52
```

## ที่ต่างจากบล็อกเดิมสามอย่าง (ka1-A เทียบตามนี้)
1. `notice=sent` **โผล่เพิ่ม** บนบรรทัด `GM_CHAT_STAGED_NEXT_LOGIN` — นี่คือของที่ `#1118` มาส่ง
   และคือเหตุผลเดียวที่ต้องวัดใหม่
2. `LANE_GM_CHAT_ACTION <cmd> route=action` สองบรรทัด และ `GM_CHAT_NOTICE_SENT ... command=staged`
   หนึ่งบรรทัด **มีอยู่แล้วบน `7a064e7`** — ใบ `0552` ตัดออกจากบล็อกเพราะกรองด้วย `head`
   ไม่ใช่เพราะไม่มี · เขียนกลับเข้ามาให้ครบ เพื่อให้ ka1-A ไม่เจอ "บรรทัดเกิน" แล้วตัดใบ
3. base sha เปลี่ยน `7a064e7` → `5138fc9`

## สิ่งที่ยังเหมือนเดิม (ไม่ต้องแก้ในใบ)
`len(pc)=56` · `len(frame)=66` · `delay=0.0` · `ch=0xAC52` · `scene=278` ·
`name='Beach Soccer Field'` · ขั้นตอน `ATTENDED:` ทุกบรรทัด · เกณฑ์ผ่าน/ไม่ผ่าน

## nonclaims
- ไม่ได้วัดบนสายจริง วัดที่ composer ล้วน · ไม่ได้พิสูจน์ว่าไคลเอนต์เห็นประโยค —
  นั่นคือสิ่งที่ใบ attended มีไว้ตัดสิน
- ไม่อ้างว่า M2 ผ่าน · `/warp` เป็นเครื่องมือ GM สำหรับไปถึงสภาพที่จะเทส
  ไม่ใช่หลักฐานว่าทางออกจากเมืองของผู้เล่นทำงาน
- วัดบน worktree ของ `origin/main` เปล่า **ไม่ใช่** กิ่งงานของรอบนี้ ⇒ คอมมิตของรอบนี้
  (`warp <ชื่อ>` cap + `#n`) ไม่มีส่วนในโทเคนนี้เลย
