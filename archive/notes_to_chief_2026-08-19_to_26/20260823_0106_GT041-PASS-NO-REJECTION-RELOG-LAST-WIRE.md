ถึง: chief + Panya

# GT-041 MOVE-AUTHORITY-002 — PASS แบบ no-rejection: การเดินธรรมดาไม่ชน gate; relog กลับจุดล่าสุดที่ client เคยส่งขึ้นสาย

เวลา: 2026-08-23 00:32–01:01 (+07:00) · ผู้เทส: Codex ATTENDED (LOCAL)

## คำตัดสินที่เสนอ

**[PASS] แบบ no-rejection สำหรับ claim ของใบ:** การเดินธรรมดาด้วย `W/A/S/D`, เลี้ยวกล้อง `Q/E` และกระโดด `W+space` ห้าครั้ง ส่ง `TargetPosVital` 122 เฟรม โดยไม่มีเฟรมใดเกินงบที่ ship มา และตำแหน่งในเฟรมสุดท้ายตรงกับแถว DB T4–T7 ทุกค่าพอดี จึงไม่พบหลักฐานว่า gate ปฏิเสธ position report ใดในรอบนี้

ค่า HUD หลังจากเฟรมสุดท้ายยังขยับต่อจากราว `(-4467,-3224)` ไปที่ A3/A4 `(-2472,-2327)` ห่างราว 2187.65 หน่วย แต่ **ไม่มี TargetPosVital หลัง 00:50:59.422** ดังนั้นความแตกต่างนี้คือตำแหน่ง local ที่ไม่เคยส่งขึ้นสาย ไม่ใช่ position ที่ส่งแล้วถูก server ปฏิเสธ

บูต B กลับเข้ามาที่ B0 `(-4467,-3224)` ซึ่งตรงกับ T6/last wire (ต่างจากค่าจริงเพียง 0.57 หน่วยจากการปัด HUD) ไม่ตรง A4. นี่ยืนยัน persistence ของเฟรมล่าสุดที่มาถึง server แต่ไม่ใช่หลักฐาน live correction/rejection

## Client-observable

- A0 หลังเข้าฉาก: HUD `(-8553,-2579)`; T0/T1 `(-8553.947,-2579.689)`
- A1 หลัง W ค้าง 20 วินาที: HUD `(-9083,-1889)`; T2 `(-9141.920,-1900.079)` ห่าง 59.95 หน่วย (สอดคล้องกับ cadence ประมาณ 2 วินาที)
- A2 หลังเดินข้ามฉาก: HUD `(-4128,-1670)`; T3 `(-4128.128,-1670.206)` ห่าง 0.24 หน่วย
- A3/A4: HUD `(-2472,-2327)`; T4/T5/T6 `(-4467.042,-3224.569)` ห่าง 2187.65 หน่วย แต่ HUD จุดนี้ไม่มีใน raw wire
- B0/B1 หลัง relog: HUD `(-4467,-3224)` คงที่ 30 วินาที = T6/last wire ไม่ใช่ A4
- ระหว่างสังเกตสดไม่พบ rubber-band/การดึงกลับแบบคงอยู่หรือเห็นชัด; เกมยอมให้ client เดินต่อเข้าน้ำ/ทะลุ geometry ได้
- มีวิดีโอต่อเนื่อง 13:30 นาทีครอบช่วงเดิน. ยังไม่ได้ทบทวนทุกเฟรมของวิดีโอ จึง **ไม่ claim ว่า transient ต่ำกว่า 1 วินาทีไม่เคยเกิด**; สิ่งที่ไม่ถูกจับ/ทบทวน = non-observed ไม่ใช่ absent

## Wire / gate re-derivation

- raw boot A มี `TargetPosVital 0x2A90` 122 เฟรม; boot B ยืนนิ่งมี 0 เฟรม
- ถอด x/y/z/heading ได้ครบ 122/122 และ timestamp จับคู่ได้ 122/122; moving=1 จำนวน 118, moving=0 จำนวน 4, derived=0 ทั้งหมด
- ค่าสูงสุดจากรายงานติดกัน: planar step 847.192 (งบ 2000), speed 411.858/s (เพดาน 1500/s), `|dz|` 186 (งบ 400), min elapsed 1.103s — over-budget 0/122
- เฟรมสุดท้าย 00:50:59.422 = `(-4467.04150390625,-3224.56884765625,0,5.7715911865234375)`; DB `updated_at=2026-08-22T17:50:59.437000+00:00` และ x/y/z/heading ตรงกันทุกค่า
- ไม่มี TargetPos หลังเวลานั้น; จึงไม่มีช่วงที่ `updated_at` ค้างทั้งที่มี report ใหม่เข้ามา
- console boot A/B มี `[G>]` ปกติ 9/7 บรรทัดตามลำดับ login/start/teleport/runtime/population; ไม่มี corrective frame ของ lane นี้
- `ErrorData`, 28317, `compose_refused`, `already_sent`, `refused`, traceback = 0; stderr ทั้งสองบูต 0 bytes; console ทั้งคู่ลง `[FOUNDATION] stopped` ครบ

## DB T0–T7

| T | x | y | z | updated_at (UTC) | selected sessions | max lease | open |
|---|---:|---:|---:|---|---:|---:|---:|
| T0 | -8553.947 | -2579.689 | 186 | 2026-08-18T10:38:40.374998 | 7 | 8 | 0 |
| T1 | -8553.947 | -2579.689 | 186 | same | 8 | 9 | 1 |
| T2 | -9141.920 | -1900.079 | 186 | 2026-08-22T17:43:12.559417 | 8 | 9 | 1 |
| T3 | -4128.128 | -1670.206 | 0 | 2026-08-22T17:47:03.256916 | 8 | 9 | 1 |
| T4 | -4467.042 | -3224.569 | 0 | 2026-08-22T17:50:59.437000 | 8 | 9 | 1 |
| T5 | -4467.042 | -3224.569 | 0 | same | 8 | 9 | 1 |
| T6 | -4467.042 | -3224.569 | 0 | same | 8 | 9 | 0 |
| T7 | -4467.042 | -3224.569 | 0 | same | 9 | 10 | 0 |

sessions selected +2, max lease +2, open กลับ 0; integrity=`ok`, FK=0. Snapshot ledger SHA256 `D76979A80D791A78237432AAE6414D5387E0D8AD229385B94C4875CFEEF89A11`.

## Exact boot / DB integrity

- resolver job 992 ได้ green commit `b665d9276bcd05ac256132372310fb64d26b163f`, tree `39edf49dd73a5307343eec1dc251f8a7067c21e1`; main HEAD `cf817305327783c4187224c79df3150ced426ae3` tree เดียวกัน, dirty=0
- exact boot root `C:\Users\Panya\Desktop\Pirate Force\pf_bridge\boot_trees\gt041_20260823_003521`
- scenario `scenarios\move_authority_hypothesis_speed_gate.json`
- run DB ไฟล์เดียวทั้งสองบูต: `Pirate Force ServerProject\state\run_gt041_20260823_003521.sqlite3`, SHA256 `5B838B570AF91A98EC1B1D31CA90A39D93DE2A35F06242E8BBE901B396DD5CAB`
- backup `pf_bridge\backup\pirateforce_before_GT-041_20260823_003521.sqlite3`, SHA256 `6BFCEDD5593D316A27A6C300206A9A3BEEC5E65631835308E02289B5FE498FC7`
- missing-DB preflight ตาย exit 2 ด้วยข้อความ exact `--move-authority-hypothesis-scenario requires an explicit existing --db`
- canonical ก่อน/หลังไม่เปลี่ยน: `6BFCEDD5593D316A27A6C300206A9A3BEEC5E65631835308E02289B5FE498FC7`

## Raw / console evidence + SHA256

- boot A raw `capture_v141\GAME_20260823_003622_355362_61678.txt` — `2F7201A9AFC771EDAF665CAE288469829BAA81268B9656312DEDB2E7D337DC35`
- boot B raw `capture_v141\GAME_20260823_005641_969098_57339.txt` — `F276E4A7F377288E74B56AA852777BC4FA052B040ECF13B6A43E1521F9174ED8`
- live summary `capture_v141\GAME_LIVE.txt` — `484663EBC9451FBFB0F1FB2326B620382B87A90D4CF7D8CCC313920FAAF94EAD`
- boot A console out — `20B36247BB23201005393622586E5728DCECEDABFA89D23D00FF01E696DC94DF`; err empty SHA `E3B0C44298FC1C149AFBF4C8996FB92427AE41E4649B934CA495991B7852B855`
- boot B console out — `B297FD3C2937DD96E93463F39725CCB243238A5433B3E3487F9C62BD08ACE785`; err empty SHA เดียวกัน

## Client evidence + SHA256

- A0 `GT041_A0_20260823_0036.jpg` — `4EC3DA8EAFBF84BE3DCDED7C3E49EB325D8B02E9074A48682AFDBE63DA214644`
- A1 หลัง W20s `GT041_A1_after_W20s_20260823_0043.jpg` — `01EB8657FCA35AD38CA014B92B904246C4F55DBD379DCF215C26F6FCAC46B164`
- A2 `GT041_A2_after_traverse_20260823_0047.jpg` — `0189E8239F0C65CEDF8EE534822657E72643174A08A95C904BA1BADB1DBD2D10`
- A3 `GT041_A3_after_5_jumps_20260823_0051.jpg` — `A5E09BA7C82158C761AC5D1A7F66CE359EE10664D742B2517BD0FD92B746FC62`
- A4 `GT041_A4_final_before_exit_20260823_0052.jpg` — `615F204CAABACD15D69839999771D5E3AE5119DC8D13D49F95072A11E4131C47`
- B0 `GT041_B0_relog_20260823_0057.jpg` — `BCBD6CE7EC4ED6A07F3AD2193DCADFEF152236AC3E18C2E56F15A74B8DABDEC4`
- B1 30s `GT041_B1_still30s_20260823_0058.jpg` — `D7F42D6AFC182E95366FC62C24C71DC55FCE0042F5460719058553110691DA8C`
- ไฟล์ `GT041_A1_20260823_0040.jpg` — `BEE9D557023C18292B420FAC5F02619E47CEA45F1806C5F01128F15D5232921F` เป็น failed tap experiment ก่อน W20s ไม่ใช่ A1 บังคับ; เก็บไว้และเปิดเผยเป็น deviation
- วิดีโอ `C:\Users\Panya\Videos\Captures\Pirate Force 1.41.01132 2569-08-23 00-39-49.mp4`, 767,934,348 bytes, 13:30 — SHA256 `372F5980BB3E6214629167E9C8B16CE6AAC646825389D9C2C55600889F8489DB`

## Jobs / deviations

- jobs 992 preflight; 993 boot A; 994/995 helpers; 996 หยุดก่อส่ง input เพราะ foreground guard ไม่ผ่าน; 997 retry ผ่าน; 998 traversal ผ่าน
- 999 parser หยุดก่อ input เพราะ PowerShell interpolation; 1000 corrected return+jump ผ่าน; 1001 T5; 1002 teardown A; 1003 T6; 1004 boot B; 1005 helper
- 1006 teardown B ปฏิเสธแบบ safe ก่อ signal เพราะ info เก่ามี stamp A; 1007 เขียน info receipt B ใหม่โดยไม่ลบ/แก้ของเก่า; 1008 teardown retry ผ่าน; 1009 T7 ผ่าน
- ทั้ง 996/999/1006 ไม่มี input/signal ที่หลุดไปถึงเกม/server; เป็น safe pre-action failures

## Procedural limitations / nonclaims

- ท่า W+space ทำครบห้าครั้ง แต่ฉากเข้าน้ำ/ทะลุ geometry และไม่สามารถยืนยันได้ว่าพื้นผิวนั้นคือทางลาด/บันไดตามขั้นตอน; จึงไม่ claim collision, terrain, ground Z หรือ vertical-budget coverage ของบันได
- ไม่ claim ว่า report ระหว่างทั้ง 122 เคยปรากฏเป็นแถว DB ให้เห็นทีละค่า เพราะ T0–T7 เป็น coarse snapshots; สิ่งที่พิสูจน์ได้คือไม่มี over-budget และ last report = final DB โดยไม่มี sustained log/DB freeze
- ไม่ claim ว่า A4→B0 snapback เกิดจาก authority rejection; A4 ไม่เคยอยู่บนสาย
- budget/gate/scenario เป็นดีไซน์ของเรา ไม่ใช่ policy ของ server ต้นฉบับ

## Teardown

inbox ว่าง · listeners 10188/10189 = 0 · GameClient = 0 · open sessions = 0 · integrity ok/FK 0 · console A/B stopped · canonical unchanged. เลขจ็อบผู้เทสถัดไป = **1010**.
