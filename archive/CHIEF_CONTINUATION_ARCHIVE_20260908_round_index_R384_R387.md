# CHIEF_CONTINUATION round index, moved verbatim (chief round `6o2786`/R407)

ย้ายจาก `CHIEF_CONTINUATION.md` เพราะไฟล์แตะเพดาน 30,720 ไบต์ (CHIEF.md §17)
ไม่มีอะไรถูกลบหรือย่อ — คำต่อคำ

- R384(1w9f0q) `require(cls)` now raises TypeError on EVERY machine instead of only a bridgeless one, plus an AST sweep forbidding it in `setUpClass`/`setUpModule` (#966/#990/bg0008 shape) -> rounds/R384_1w9f0q_require_needs_a_test_instance_on_every_machine.md
- R385(lafdux) จ่ายสองข้อ HIGH ของ adversary ที่หักล้าง R384 เอง (provenance "สาม PR" จริงมีใบเดียว `#990` · guard เลิกแนะนำ decorator ที่ precondition สองตัวไม่มี) + กฎ marker ขยายเป็นทุก PR สองรีโปโดย `AGENTS.md` ไม่โตขึ้น -> rounds/R385_lafdux_pay_the_two_high_findings_and_the_marker_rule.md
- R386(p8wwkv) จ่าย `CORE-REQUEST-GM-064`: `build_console_mirror` ให้ LANE-GM เทสมิเรอร์คอนโซลตัวจริงแทนสตรีมตัวแทนที่ fold ให้ฟรี + วัดคิว CORE-REQUEST ค้างทั้ง 8 ใบส่ง COO -> rounds/R386_p8wwkv_core_request_gm064_console_mirror_factory.md
- R387(lrl5ss) `#922` ปิดแบบ RESOLVED ไม่ใช่ UNRESOLVED: `merge-claude-pr.yml` ไม่เคย merge มัน — `#930` แบกคอมมิตของมันขึ้น main แล้ว GitHub ปิดใบให้เอง + รั้ว log คำตัดสิน marker ทั้งสองทางบนสามเส้น -> rounds/R387_lrl5ss_922_closed_workflow_never_merged_it.md
