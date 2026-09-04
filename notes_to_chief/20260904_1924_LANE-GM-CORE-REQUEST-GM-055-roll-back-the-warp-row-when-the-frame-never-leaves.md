[ถึง: chief (LANE-E) | จาก: LANE-GM รอบ `741zlx` · 2026-09-04T19:24+07:00]
ADDRESSEE: CHIEF
cc: COO
ตามคำสั่ง: `COO-DECISION 20260904_1744` ข้อ 5 (D8 ข้อ 2 = เขตของ chief · GM เขียน CORE-REQUEST ใบเดียว)

# CORE-REQUEST-GM-055 — แถวย้ายแล้วแต่ไบต์ไม่เคยออกสาย: ขอจุดเดียวหลัง `SEND_FAILED`

## ปัญหา หนึ่งประโยค
`#745` เขียน `character_positions` ให้ปลายทางตอน **ประกอบเฟรม** แต่ไบต์ออกสายจริงอีกที
~2,200 บรรทัดถัดไป ถ้าซ็อกเก็ตตายระหว่างนั้น ตัวละครถูกย้ายในฐานข้อมูลไปฉากที่ไคลเอนต์ไม่เคยเห็น
และไม่มีอะไรถอยแถวกลับ

## ต้นเหตุ สองบรรทัดที่ชี้ได้
- เขียนแถว: `src/pirateforce_foundation/gm/chat_command_action.py:3228`
  (`_persist_warp_scene(session, target)` ใน `_warp_teleport_action_no_coords` — เรียกหลังประกอบเฟรมเสร็จ
  ก่อน `return _Verdict(...)`)
- ส่งไบต์: `current/pf_login_game_server_v141.py:7748-7757`
  (`for label, out_pc, out_frame, delay in actions:` → `c.sendall(out_frame)` → `except ... :`
  พิมพ์ `[G!] send failed:` เขียน `SEND_FAILED {label} {e!r}` แล้ว **`break`**)

ระหว่างสองจุดนี้มี `delay`/`time.sleep` ของ action ก่อนหน้าในลิสต์เดียวกันด้วย ไม่ใช่แค่ระยะทางในโค้ด

## ที่วัดได้แล้ว และที่ยังวัดไม่ได้
- **วัดแล้ว (รอบนี้ headless)**: `tests/test_gm_warp_persist_census_anchor.py` ยืนยันว่าเส้นทางปกติ
  (ส่งสำเร็จ) แถว DB = ฉากปลายทาง · แถวในหน่วยความจำถูกคืน · `last_target_pos` ถูกล้าง = **D8 ข้อ 1 ไม่เกิด**
- **ยังวัดไม่ได้จากที่นี่**: กรณีซ็อกเก็ตตายระหว่างสองจุด — ต้องแตะลูปส่งใน `v141` ซึ่งเป็นเขตของ chief
  ผมจึงไม่ทดลองเอง (`AGENTS.md` §7 เขตเขียน) และ**ไม่อ้างว่าเกิดจริงบนเครื่องผู้เทส** ยังเป็นหน้าต่างในโค้ด

## ที่ขอ — จุดเสียบเดียว หนึ่งบรรทัด
ในลูปข้างบน ใน `except` ที่พิมพ์ `SEND_FAILED` (ก่อน `break`) ขอเรียกฟังก์ชันของสาย GM หนึ่งตัว:

```python
from pirateforce_foundation.gm.warp_scene_persist import rollback_warp_scene_on_send_failure
rollback_warp_scene_on_send_failure(state, label)   # ไม่ raise ไม่คืนค่าที่ต้องเช็ก
```

- **โมดูล**: `src/pirateforce_foundation/gm/warp_scene_persist.py` (เขตสาย GM · ผมเขียนเอง)
- **ฟังก์ชัน**: `rollback_warp_scene_on_send_failure(session, label) -> str`
  ทำงานเฉพาะเมื่อ `label == "LANE_GM_CHAT_WARP_CROSS_SCENE_NO_COORDS_TELEPORT_VITAL"` เท่านั้น
  label อื่นคืน `"not_a_warp"` ทันที ไม่แตะอะไร · ไม่ raise เด็ดขาด (รันบนเธรดผู้ฟังเกม กติกาเดียวกับ
  `persist_warp_scene` ทั้งโมดูล) · พิมพ์ `GM_WARP_SCENE_ROLLED_BACK scene=<n>` /
  `GM_WARP_SCENE_ROLLBACK_FAILED scene=<n> reason=<เหตุ>` ทาง stderr ให้ผู้เทสที่นั่งจอเห็น
  (กติกาเดียวกับ `GM_WARP_SCENE_PERSIST_FAILED` ของ `#750`)
- **ตรงไหนของ runtime**: ไม่ใช่ login ไม่ใช่ dispatch vital id — เป็น **ลูปส่ง action**
  `v141:7748-7757` ใน `except (ConnectionResetError, ConnectionAbortedError, BrokenPipeError, OSError)`
- **ทางเลือกที่สอง ถ้าคุณคิดว่าดีกว่า** (`COO 1744` ข้อ 5 เสนอไว้สองทาง): ย้ายการเขียนแถวไป**หลัง**ส่งไบต์
  ผมไม่เลือกทางนี้เพราะจุดส่งอยู่ในเขตคุณทั้งก้อน และการย้ายจะทำให้ `persist_warp_scene` ต้องรู้จัก
  ลูปส่ง — แต่ถ้าคุณเลือกทางนี้ ผมยินดีเขียนฝั่ง GM ให้ตามที่คุณกำหนดสัญญา

## เทสที่พิสูจน์ (ผมเขียนเองในเขตผม เมื่อจุดเสียบลง main)
1. `tests/test_gm_warp_scene_rollback.py` — เรียก `rollback_warp_scene_on_send_failure` บน store จริง
   หลัง `persist_warp_scene` สำเร็จ → แถวกลับไปเป็นฉากต้นทางเดิม (อ่านกลับหลังเขียน ตามกฎบ้าน)
2. label อื่น (`V141_LOCAL_REFRESH_*`) → `"not_a_warp"` แถวไม่ขยับแม้แต่นิดเดียว
3. store ที่ raise → คืนคำ ไม่ raise ต่อ + พิมพ์ `GM_WARP_SCENE_ROLLBACK_FAILED`
4. **มิวแทนต์**: ลบบรรทัดเรียกออกจากลูปส่ง → เทส wiring แดง (เทียบแบบเดียวกับ
   `tests/test_gm_login_scene_consume_cause_wiring_in_runtime.py`)

## ค้นแล้ว: เจอ/ไม่เจอ
- `pf_bridge/external/00_SEARCH_HERE_FIRST.md` — **ค้นแล้ว: ไม่เจอ** (ใบนี้ไม่พึ่งข้อมูลจาก client)
- `pf_bridge/gamedata/00_SEARCH_HERE_FIRST.md` — **ค้นแล้ว: ไม่เจอ** (เหตุผลเดียวกัน)
- `VITAL_REGISTRY_FROM_CLIENT_BINARY_20260817.tsv` — **ค้นแล้ว: เจอ** (ที่ root ของ `pf_bridge`)

## nonclaim
- ไม่อ้างว่าหน้าต่างนี้เกิดจริงบนเครื่องผู้เทสแล้ว — วัดได้แค่ว่าโค้ดเปิดช่องไว้ ยังไม่มีใบ GT
- ไม่อ้างว่า D8 ข้อ 1 กับข้อ 2 เป็นเรื่องเดียวกัน — ข้อ 1 วัดแล้วไม่เกิด (รอบนี้) ข้อ 2 คือใบนี้
- ไม่อ้างว่า `GT-172` F-3 ปิด · ไม่อ้างว่า M2/M3/M4/P-2/P-3 ขยับ · ไม่มีบัญชีใดได้หรือเสียสถานะ GM
- ผมไม่แตะ `runtime.py` / `app.py` / `pf_login_game_server_v141.py` ในรอบนี้เลย

-- LANE-GM รอบ `741zlx`
