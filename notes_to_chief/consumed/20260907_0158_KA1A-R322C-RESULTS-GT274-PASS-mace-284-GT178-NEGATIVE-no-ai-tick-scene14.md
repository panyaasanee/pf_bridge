# R322C RESULTS (ka1-A attended · Panya ที่คีย์บอร์ด 01:29–01:51) — GT-274 PASS · GT-178 NEGATIVE-MEASURED (ฉาก 14 ไม่มี AI tick · โจมตีกลับส่งไม่ได้)

ADDRESSEE: LANE-K (พับผล) · cc: COO · LANE-B · LANE-A · chief
ส่งทาง: สะพาน (เครื่องเจ้าของเปิด)
OBSERVER_CONFIRMED: 2026-09-07T01:48+07:00 (Panya: "ใช่ เป็นท่าเอากระบองทุบ" + ภาพ · "ไม่เห็นมอนมันจะทำอะไรเลย" + ภาพ Glaucoma)

## บูต
- BOOT_COMMIT `88759b48` (main ณ ตอนบูต `f51ca624` · code_delta 2 · resolver เลือกหัวเขียวล่าสุด) · ไร้ธง ไร้ env · pytest ในต้นไม้ 313 passed 8 skipped · gate GT-274 `d52cae3` อยู่ในคอมมิต ✓
- run DB `state/run_gt274_20260907_012915.sqlite3` (ต่อจาก run_gt281 ของ R322B) · canonical sha **ไม่เปลี่ยน** `4FF37060…A548454` · capture `GameClient/capture_r322c_20260907_012915/` (hex windows 117 hits) · jobs 1556/1557/1558/1559 · ปิดสะอาด · ตัวละครใหม่ Paladin อยู่เฉพาะใน run DB

## GT-274 PRODUCTION-ATTACK-POSE-BY-CLASS — **PASS ทั้งสองชั้น**
- ครึ่งแรก (R322B 00:5x): Gladiator (Arena01) ตี Fighting Fish → จอ: ฟันดาบ · wire: `POSE_PRODUCTION class=1 equip_type=1 base=2 behavior=280`
- ครึ่งหลัง (R322C): สร้างตัวใหม่ **Paladin หน้าตา #1** → ตี Training Iron Man (916) ในเมือง 4 ครั้ง → จอ: **ฟาดกระบอง** (เจ้าของยืนยัน + ภาพ ดาเมจ 891 บนจอ) · wire: `POSE_PRODUCTION class=2 equip_type=2 base=3 behavior=284` ×4 · `damage announced -891, applied 891` HP 192779→189215/198125 ตรงจอ
- ขั้น 3 ของใบ (สวมอาวุธแล้วตีซ้ำ) ไม่ได้ทำ — GT-272 ยังไม่ผ่าน (RE-280) · `TWO_SESSIONS_SAME_SCENE:` ไม่ได้วัด (ผู้เล่นคนเดียว)

## GT-178 BG0015-HOSTILE-TWELVE-AGGRO — **NEGATIVE-MEASURED พร้อมสาเหตุ**
- ก่อนบูต (บล็อกในใบ รันจากต้นไม้บูต): `SHIPPED` 11 แถว = Glaucoma(343)×7 · Phosphor Fascinator(345) · Crimson Sharp Teeth(348) · Arbiter Bells(350) · Lava shakers(353) · Horror butcher Lasa(355) — ทุกตัว LV105 HP 228,055 · `WITHHELD 87 924 Carlos`
- `/warp 14` (Hell Volcanic Island) → wire: `MOB_CENSUS_HOSTILITY scene_id=14 scene=Bg0015 roster=11 backed=11 unbacked=none refused=0 withheld=1` · จอ: Glaucoma ชื่อชมพู เจ้าของเดินเข้าประชิด
- **มอนไม่ทำอะไรเลย** (ไม่หัน ไม่วิ่ง ไม่ตี HP เจ้าของ 100/100) — สาเหตุจากคอนโซล:
  1. **ไม่มี AI tick ในฉาก 14**: ทั้งเซสชันมีบรรทัด `MOB_AI_TICK_LIVE scene=1 mobs=4` บรรทัดเดียว (หุ่นซ้อมเมือง) ไม่มี `MOB_AI_TICK_LIVE scene=14` — ตาม docstring `runtime.py:_sync_combat_scene_at_edge` (COO 3 ก.ย. 19:43): tick ถูกเกตให้เดินเฉพาะเมื่อ register ตรงฉากที่ยืน แต่**การสร้าง register ใหม่ตอนมาถึงทำไว้แค่ฉาก 1/2** ฉาก 14 ที่มี roster 11 ตัวไม่มีใครต่อสาย ⇒ "ปลอดภัยแต่ไม่มีสมอง"
  2. แม้ในฉาก 1 ที่ tick เดิน: `LANE_B_MOB_AI_TICK actor=0x206E idle->aggro intent=attack_undeliverable` (ตอนเจ้าของตีหุ่น) = มอนเข้าสถานะโกรธแล้วแต่**ส่งการโจมตีกลับหาผู้เล่นไม่ได้** (เส้นทางมอน→ผู้เล่นยังไม่ต่อ)
- **นี่คือผลลบที่ควรได้จาก headless ไม่ใช่เวลาเจ้าของ**: บล็อก ATTENDED ของใบเติมเมื่อ 6 ก.ย. ตาม R364 ข้อ 2 โดยไม่รัน headless ดูว่า tick วิ่งในฉาก 14 ไหม · ka1-A ก็ตรวจก่อนบูตแค่ roster ไม่ตรวจ tick — เจ้าของถามเอง "ทำไมคนส่งใบไม่ดูก่อน" → PANYA-ORDER `HEADLESS_PROOF` (ใบแยก 0159)

## สถานะที่เสนอ
- GT-274 → PASS (ขั้น 3 รอ GT-272)
- GT-178 → NEGATIVE-MEASURED · ใบสร้างของ B (M4) 2 ข้อ: (ก) ทุกฉากที่มี roster สร้าง `MobAiRegister` ของตัวเองตอนผู้เล่นมาถึงและ tick เดิน — พิสูจน์ headless ด้วย `MOB_AI_TICK_LIVE scene=14 mobs=11` ก่อนเรียกเจ้าของ (ข) ต่อสายมอนตีผู้เล่น (`attack_undeliverable` → deliver) · เมื่อ (ก)+(ข) ขึ้น main ค่อยเปิด GT-178 รอบ 2 พร้อม HEADLESS_PROOF

## nonclaims
- ไม่อ้างว่ารู้ว่าเกตของ 3 ก.ย. ควรถูกถอด (มันกันบั๊กจริง: tick ด้วยรายชื่อฉากเก่า) — ที่ขาดคือครึ่งหลัง · ไม่ได้วัด aggro radius/`n_OFFESIVE` ของ Glaucoma เพราะ tick ไม่เดิน · ไม่อ้างว่า Paladin เกิดมามีค่าถูกทุกอย่าง (R307 เคยพบ class/HP ผิดตอนสร้าง — วันนี้ class=2 ถูก)

RESULT: GT-274 PASS R322C 2026-09-07 01:36 (Paladin mace pose · POSE_PRODUCTION class=2 behavior=284 · Gladiator half class=1 behavior=280 in R322B)
RESULT: GT-178 NEGATIVE-MEASURED R322C 2026-09-07 01:48 (roster=11 backed=11 but no MOB_AI_TICK_LIVE for scene 14 · attack_undeliverable · mobs never react)
SCOREBOARD: DONE | ผู้เล่นอาชีพต่างกันออกท่าโจมตีต่างกันจริง (ดาบ/กระบอง) · มอนสนามยังยืนเฉยไม่ตีกลับ (M4 ยังไม่เริ่ม) | 20260907_0158_KA1A-R322C-RESULTS-*
