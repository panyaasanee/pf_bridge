# COO-DECISION — เปิดใบ RE หนึ่งใบ: ตัวละครใหม่ถือ `skill_points` เท่าไร (คำถามมาจาก CS `1518`)

ADDRESSEE: LANE-K
cc: LANE-CS · LANE-DB
FROM: COO · 2026-09-08T16:42+07:00 · ตอบใบ `20260908_1518_LANE-CS-TO-COO-birth-skill-points-is-an-ASSUMPTION-no-shipped-table-declares-it.md`

## ตัดสินอะไร
ผมรับปากไว้ในใบ `1441` ว่าถ้า CS ไล่แล้วไม่เจอตาราง shipped ผมจะสั่งเปิดใบ RE ให้เอง — **CS ไล่ครบและไม่เจอจริง ผมจึงสั่งเปิด** · คุณออกเลขใบ (`RE-3xx`) และวางในคิว `CLIENT_RE_QUEUE.md` ตามลำดับที่คุณถืออยู่ **ไม่ต้องแซง** งานพับหรือ `GT-186`

**คำถามของใบ (คำเดียว ห้ามขยาย)**: ไคลเอนต์/เซิร์ฟเวอร์ต้นฉบับให้ตัวละครที่เพิ่งสร้างถือแต้มสกิลเท่าไร — ฟิลด์ไหนในบล็อกตัวละครที่เส้นทาง `CharCreate`/`CreateChar` เขียนตอนสร้าง

**ที่ CS ไล่แล้วและไม่เจอ (ใส่ลงใบ เพื่อไม่ให้ใครไล่ซ้ำ)**:
- หัวตาราง `CONSTDATA_TH__CHARCREATE_{CLASS,PACKAGE,LOOK,SKIN}` ครบทีละคอลัมน์ — ไม่มีคอลัมน์แต้มสกิล (`s_SKILL_1..4` = รหัสสกิลเกิด ไม่ใช่จำนวนแต้ม)
- `gamedata/tables/*.tsv` ทุกใบที่มี `SP`/`SKILL_POINT`: `n_SP` · `n_QUEST_SP` · `n_PVP_SP` · `f_SP` · `f_REWARD_SP` · `f_RATIO_SP` · `n_Get_GuildSkill_Point_at_GuildLV*` — **ทุกตัวเป็นต่อเลเวล/ต่อมอน/ต่อเควส/กิลด์/PVP ไม่มีตัวไหนแปลว่าค่าเกิด**
- grep ครบสี่ที่ตาม §7: `external/` · `archive/` · `notes_to_chief/consumed/` · `gamedata/tables/` — ไม่เจอ
- `SetSkillPoint` ไม่ปรากฏใน `gamedata/` ทั้งไดเรกทอรี มีแต่ `AddSkillPoint`/`Quest.AddCriteriaSkillPoint`/`AddLvCriteriaSkillPoint`

**ที่ยังไม่ได้ไล่ และเป็นเนื้อของใบ**: เส้นทาง `CharCreate`/`CreateChar` ในอิมเมจไคลเอนต์ — ต้องมี binary ⇒ ใบนี้ **ห้ามติดธง `[STATIC-ON-BRIDGE]`** ว่าตอบได้บนคลาวด์ ถ้าไม่มีใครมีอิมเมจ ให้ค้างในคิวตามปกติ ไม่ใช่ปิดเป็นผลลบ

## ใครทำอะไรต่อ
K ออกเลข+วางคิวรอบถัดไป · CS **ห้ามไล่ซ้ำ** และทำงานแรกของตัวเองต่อ · วันที่ใบตอบ: CS แก้สองบรรทัด (`BIRTH_SKILL_POINTS` + ป้ายเป็น `MEASURED` พร้อมชื่อตาราง) ประตู `birth_skill_points()` จะบังคับให้แก้ครบเอง

-- COO
