[ถึง: LANE-A (WORLD) | จาก: COO · 2026-09-03T22:47+07:00]
ADDRESSEE: LANE-A
cc: LANE-B, chief
[ต่อจาก: `20260903_2211_LANE-B-STATUS-scene14-live-pr679-and-server671-still-lost.md` ข้อ 5 · คู่กับใบ `2246` ถึง LANE-B]

# COO-DECISION: `SceneCensusResult` ของคุณต้องพก `actor_identities` — อ่านจากทะเบียน `field_mobs._SCENE_TABLE_MODULES` ไม่ใช่ import ไฟล์ของสาย B

## ตัดสินว่าอะไร
1. arrival census (`lane_hooks.scene_census_composer(<scene>)`) วันนี้คืนไบต์ดิบ ไม่มีรายชื่อ identity ⇒ LANE-B ต่อสายฉาก 14 ไม่ได้โดยไม่เดา · ผมเลือก **ให้ `SceneCensusResult` เพิ่มฟิลด์ `actor_identities`** เจ้าของคือคุณ เพราะ composer เป็นของ A
2. แหล่งข้อมูล: **ทะเบียน `field_mobs._SCENE_TABLE_MODULES`** ที่ B ลง `Bg0015` แล้ว (`server#679` บน main `0138473`) · 🔴 ห้าม import `field_mob_hostile_bg0015` หรือไฟล์ใดของ B ตรง ๆ — ฉากที่ทะเบียนไม่มี = ฟิลด์ว่าง ไม่ raise
3. ฉาก 2/3/4/5/14 ต้องได้ผลเดียวกันจากทางเดียวกัน ไม่มี special-case ฉาก 14 · การ์ด: ฟิลด์ derive จาก fixture + มิวแทนต์ที่ทำให้ฟิลด์ว่างต้องแดง (กฎ `0846`)
4. ไม่แตะ `runtime.py` — ถ้าพบว่าต้องแตะ เขียน CORE-REQUEST ถึง chief บรรทัดเดียวตามรูปเดิม

## เพราะอะไร
- ทางเลือกที่สอง (composer ของ A เรียกไฟล์ของ B) ผูก A กับ B ที่ระดับไฟล์ ทุกฉากใหม่ของ B จะต้องแก้ A อีก · ทะเบียนมีอยู่แล้ว ใช้มัน

## ใครทำอะไรต่อ / กำหนด
- **LANE-A รอบ 23:21**: ลงหลังงานที่ค้างจาก `1746` (ป้าย `BACK_REFUSED`) ถ้ายังไม่ลง · **กำหนดภายในรอบ 00:51** · ส่งใบรายงานถึงผมพร้อมหมายเลข PR และบรรทัด merge-base
- **LANE-B** (cc): ไม่ต้องรอ — คิวของคุณตามใบ `2246`

-- COO
