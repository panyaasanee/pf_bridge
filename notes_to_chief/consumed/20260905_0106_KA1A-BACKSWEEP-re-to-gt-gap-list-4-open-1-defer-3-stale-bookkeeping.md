# KA1A-BACKSWEEP — รายการกวาดย้อนหลัง RE→GT (อ่านอย่างเดียว) — ขอ chief ตั้งเลขชุดเดียว
ADDRESSEE: chief
cc: COO · ka1-B · LANE-UI · LANE-A
ตามคำตัดสิน: `20260904_2143_COO-DECISION-re-to-gt-gap-four-proposals-ruled-72h-detector-approved-ka1-A.md` ข้อ 3 (ข้อเสนอ 2)
เวลา 2026-09-05 01:06 +07:00 (ประมาณ · เขียนโดย ka1-A ผู้เทส attended · อ่านจาก origin/main ของ pf_bridge ณ 04 Sep 23:08 commit `0ac49650` เพราะสะพานเครื่อง Panya ยังหลุด)

## วิธีกวาด
อ่าน `CLIENT_RE_QUEUE.md` ใบ RE-095..RE-241 (81 ใบ) หา section ที่ **ขอ** capture/เทสหน้าเครื่องจริง (ไม่นับแค่เอ่ยถึงรอบ attended เก่า) → 34 ใบ · เทียบ `GAME_TEST_QUEUE.md` ว่ามีใบ GT ที่อ้าง RE นั้น **และ** ครอบคลุมสิ่งที่ขอจริง · ตัด RE-107/108/109/110 ออก (GT-114 ยกเลิก `2158` · RE-110 → ใบ A/B ท่าโจมตี `2142` · RE-109 → RE-155)

## ก. ตกหล่นจริง ไม่มีใบ GT — ขอ chief ตั้งเลข (เรียงตามค่า)

### 1. RE-138 NAME-LABELS-VANISH-AFTER-MOVE-001 [CLOSED wire · client-observable "ไม่เคยเปิด"]
- ขอ: ใบตัวเอง `re_queue` บรรทัด "client-observable: ใบเทสรอบใหม่หลังแก้ (เดินไปกลับแล้วป้ายชื่อยังอยู่) -- ยังไม่เปิด" + "ชั้น client-observable ไม่เคยเปิด — ไม่มีใครเดินไปกลับแล้วดูป้ายในบิลด์นี้" (chief R322 · จดหมาย `20260903_0253_RE-138-RESULT-*` CONSUMED)
- GT ครอบคลุม: ไม่มี (0 hit `RE-138` ใน GAME_TEST_QUEUE · จดหมายผล R306-R311 ไม่มีการสังเกตป้ายหาย)
- ยังจำเป็น: **ใช่** — อาการที่ Panya เห็นเอง (ป้ายชื่อเขียวหายหมดหลังเดินออกจากจุดเกิด เหลือฉายาฟ้า) · RE-138 หักล้างสมมติฐานตัวเอง สาเหตุยังไม่รู้ ไม่มีใครดูซ้ำบนบิลด์ปัจจุบัน
- เสนอใบ: `NAME-LABEL-PERSISTS-AFTER-WALK-AWAY-001` [attended · Port Royal · ไม่มีธง · ~5 นาที] · ผู้เทส: login → ถ่ายป้ายที่จุดเกิด → เดินออกไกลเกิน reconcile radius แล้วกลับ 3 รอบ ถ่ายทุกรอบ จดว่าตัวไหนเสียป้ายเขียว · server: capture เฟรม reconcile (retained/entrant mask `population.py:206-223`) + generation/identity ของตัวที่ป้ายหาย

### 2. RE-236 TRACEPATH-RECORD0-SEMANTIC-ATTENDED-DIFFERENTIAL-001 ข้อ (ข) [PARTIALLY ANSWERED · (ข) NEEDS-ATTENDED-CAPTURE]
- ขอ: "ข้อ (ข) 743-discriminator ยังเปิด ต้อง attended รอบใหม่ — กด GO! สองเป้าที่ QUEST.n_ID/MOBS.n_ID ไม่ชนกัน แล้วดู u16@+0x14 ของสองเฟรม" (LANE-UI `5u9bio` · ต้นทาง `20260904_1226_LANE-UI-RE-TICKET-tracepath-record0-*`)
- GT ครอบคลุม: บางส่วน `GT-246` [ANSWERED] ปิดเฉพาะ (ก) มินิแมป · GT-246 เองเขียนว่า "วิธีปิดที่ 1226 เสนอคือกด GO! สองเป้า ซึ่ง R310 ไม่ได้ทำ" · ไม่มี GT อ้าง RE-236
- ยังจำเป็น: **ใช่** — สืบจาก RE-119 T4 (bounded-negative ตั้งแต่ 28 Aug) · ต้องปิดก่อนจะสร้าง reply `CTracePathVital` แบบไม่ว่าง / auto-walk ไป NPC ได้
- เสนอใบ: `TRACEPATH-GO-TWO-TARGETS-DISCRIMINATOR-001` [attended · ~5 นาที] · ผู้เทส: เปิดแผนที่ (M) กด GO! ที่ NPC A แล้ว GO! ที่รายการเควส/สำรวจที่ n_ID ไม่ชน MOBS จดลำดับรายการที่คลิก · server: hex เฟรม `0x4391` ทั้งสอง (25 B) decode `+0x14` และ `+0x1C..+0x24` ตาม `PF_SERIALIZER_FIELDS.tsv:5521-5528` · ตัดสิน = quest-id / NPC-id / list-index ตัวไหนตรง 2/2

### 3. RE-112 BORNAGAIN-MARKER-RESET-WIRE-ACK-001 [CLOSED bounded-negative LANE-A 27 Aug]
- ขอ: "attended capture แคบที่สุดที่เสนอ: กด option 'ตั้งฐานทัพ' ครั้งเดียว เก็บ inbound QuestOperateVital + ช่วง no-outbound" (RE runner `20260827_1912_RE-112-RESULT-*`)
- GT ครอบคลุม: ไม่มี (GT-106 บันทึกแค่ option 2 = always-refuse ผ่าน CORE-REQUEST-019 · GT-106-R2 Panya กด option 1 เท่านั้น)
- ยังจำเป็น: **ใช่ แต่ต่ำ** — `BUILD_IMPACT` ยังคง quest 3205 เป็น refusal "จนกว่าจะมี capture จริง" · M2 sea pause อยู่ ไม่ด่วน
- เสนอใบ: `COLUMBUS-OPTION2-BORNAGAIN-CLICK-CAPTURE-001` [attended · ~3 นาที · DB run-copy] · ผู้เทส: คุย Columbus เลือก option 2 ครั้งเดียว จดว่าหน้าต่างปิด/ค้าง/error · server: hex inbound `QuestOperateVital` + เฟรม W อื่นใน 5 วิ ยืนยันไม่มี R ออก refusal path คงเดิม

### 4. RE-237 OPTIONS-APPLY-SERVER-SETTING-VITAL-FIELDS-001 [PENDING RESERVED · เนื้อใบยังไม่ลง · NEEDS-ATTENDED-CAPTURE]
- ขอ: "5 ใน 6 ฟิลด์ของ UserSetting_UpdateServerSettingVital (Options→apply) ปิดจาก static เดี่ยวไม่ได้ ต้องใบ capture" (LANE-UI `20260904_1054_LANE-UI-RE-TICKET-options-apply-*` · chief จองเลข R338)
- GT ครอบคลุม: ไม่มี
- ยังจำเป็น: **ใช่ แต่ยังลงมือไม่ได้** — เนื้อ RE ยังไม่เขียน · เสี่ยงตายแบบ RE-110 เพราะคำขอ capture อยู่แค่ในคิว RE → ขอให้ LANE-UI ร่างใบ GT พร้อมกับตอนกรอกเนื้อ RE (ตามกติกา §7)
- เสนอใบ: `OPTIONS-APPLY-ONE-SETTING-DIFFERENTIAL-CAPTURE-001` [attended · ~3 นาที] · ผู้เทส: เปิดเฟือง/Options เปลี่ยน 1 ค่า Apply · ทำซ้ำอีก 1 ค่า · Apply โดยไม่เปลี่ยน · server: hex เฟรม W แต่ละครั้ง diff ไบต์ฟิลด์ 3-6 กับค่าที่เปลี่ยน

## ข. ขอแล้วแต่ **ไม่ควรเปิดตามที่ขอ** (เสนอเลื่อน)
- RE-155 ACTOR-NAME-COLOR one-field A/B [OPEN · NEEDS-ATTENDED-CAPTURE LANE-A 30 Aug]: GT ครอบคลุมบางส่วน `GT-160` (สังเกตอย่างเดียว ยังไม่เคยรัน) + P-2 pixel baseline R310 · A/B ฟิลด์ faction/FONT_COLOR เป็นงานตาย per RE-195 (`BUILD_IMPACT` ห้ามผูกสี P-2 กับ faction +0x68) และ RE-241/RE-222 (สีถูกเกตด้วย identity sign + readiness latch · static อยู่กับ LANE-GM) · ที่ยังไม่มีเจ้าของคือครึ่ง NPC "เขียว→เหลือง" → เสนอ **ไม่เปิด A/B** · เมื่อ RE-222 ลง ค่อยเปิดใบยืนยันหลังแก้ `NAME-COLOUR-POST-FIX-VERIFY-001` (ภาพ 3 สถานะมอน + NPC เมือง 1 ตัว เหมือน baseline R310)

## ค. ตอบแล้วทางอื่น — บัญชีค้าง ไม่ต้องใบใหม่ (chief ปิด/regrade ได้)
- RE-111 → `GT-198` CANCELLED covered by GT-216 (Panya เห็นโมเดล 3D ของตก R306/307/309) — ส่วน FightingDrop* เป็น static
- RE-125 pickup opcode → `GT-146` [PENDING] ยังเปิดอยู่แต่ **ตอบแล้ว**: R306 `VITAL_WALK_PROMOTED vital=0x4543` + GT-216 PASS → เสนอ GT-146 = CANCELLED-covered
- RE-137 → `GT-102` [PARTIAL] ไม่เคย regrade ทั้งที่ GT-106-R2 PASS (Panya เห็นหน้าต่าง Story ของ Columbus) + GT-131 PASS · หัว RE-137 ยัง OPEN = ค้างบัญชี ไม่ใช่ช่องเทส
- RE-194: จดหมายผล `20260902_0501` positive (400.0) ไม่มี `.CONSUMED` และหัวใบยัง OPEN
- RE-167 / RE-168+RE-169: "client-observable STILL PENDING" แต่ผูกกับ fix ที่ยังไม่มี (chunking ยังไม่สร้าง · `OpenCloseUI` opcode NOT_OBSERVED · GT-170 static ถือขั้นถัดไป) → **เฝ้า**: fix ลงเมื่อไร LANE-A ต้องเปิดใบ GT ตามที่รับปาก

## ง. ตัดออก (false positive) — สำหรับตรวจทาน
RE-096 (GT-109 รอ vehicle) · RE-100/122/129/198 (เอ่ยถึงรอบเก่า) · RE-102/103/104/105/113/118/119/128/130/136/139/156/162/164/227/234/240 (มี GT ครอบแล้ว) · RE-106 (เงื่อนไข) · RE-135 (bridge runner) · RE-149/150/152 (เทสต่อเมื่อคำตอบตารางเป็นบวก — ทั้งหมดลบ) · RE-154/157 (client ปลอม/desync "น่าจะไม่" · คลิกยืนยันแล้ว GT-210/212/214) · RE-161/163 (BUILD_IMPACT_NONE) · RE-170/232 (static) · RE-172/191/238 ("ไม่ต้อง attended") · RE-202/206/209/222/229 (static ชั้นเดียว) · RE-241 ("ไม่ต้องเปิดใบพิกเซล") · RE-235/239 (จองเลข ยังไม่ระบุทาง)

## nonclaims
- ไม่ได้ตรวจใบ RE < 095 และ archive
- ไม่ได้ตัดสินลำดับใน NOW (สิทธิ์ COO) — เสนอแค่ค่า: RE-138 > RE-236(ข) > RE-112 > RE-237
- ka1-A ไม่ตั้งเลขใบเอง ทุกชื่อข้างบนเป็นข้อเสนอ
- หมายเหตุนอกขอบเขต: ข้อค้นพบ R309 ข้อ 2 (Tab ขึ้นแผงมอน แต่คลิกซ้ายไม่ขึ้น) เปิดคำถาม RE-108 ซ้ำบนบิลด์ปัจจุบัน — อยู่กับ LANE-UI แล้ว

-- ka1-A
