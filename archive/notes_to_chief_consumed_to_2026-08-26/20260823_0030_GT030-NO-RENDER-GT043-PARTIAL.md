ถึง: chief + Panya

# GT-030 rerun — actor_type 2 ไม่เรนเดอร์ที่จุด B/A หลัง MOVE · GT-043 สังเกตไม่พบ world object หาย แต่หลักฐานยังไม่ครบเต็มใบ

เวลา: 2026-08-23 00:09–00:25 (+07:00) · ผู้เทส: Codex ATTENDED (LOCAL)

## คำตัดสินที่เสนอ

### GT-030 REMOTE-PLAYER-VIS-001 — ผล substantive = **CLIENT NO-RENDER ใต้ mask ชุดนี้**

wire ส่ง sweep ครบ 5 เฟรมและไม่มี despawn จนกว่าจะตัด connection ตามดีไซน์ของใบ จากนั้นผู้เทสเดินไปตรวจตำแหน่งที่ไม่ซ้อน NPC โดยตรง:

- B `ProbePlayer02` คาดที่ X `-8989.957`, Y `-2780.045`; ผู้เล่นยืนที่ HUD X `-8972`, Y `-2808` (ห่างประมาณ 33 หน่วย), กวาด Q รอบจุด 4 มุม — ไม่เห็นโมเดลคน/ตัวใส/กล่อง/ป้ายอื่นนอกจาก Arena01
- A หลัง MOVE คาดที่ X `-8839.957`, Y `-2780.045`; ผู้เล่นยืนที่ HUD X `-8892`, Y `-2786` (ห่างประมาณ 52 หน่วย), ภาพระยะประชิด + Tab ซ้ำ 4 ครั้ง — ไม่เห็นโมเดลและไม่มี target panel ขึ้น
- ชื่อ `ProbeControl03` ไม่ปรากฏทั้งป้ายและพาเนล; เกณฑ์หยุดไม่ถูกยิง

เพราะ A/B ไม่มี despawn และตรวจหลัง sweep ครบที่พิกัดจริงระยะประชิด ผลนี้ตอบข้อ (ข) ได้ว่า **B และ A-หลัง-MOVE ไม่เรนเดอร์ด้วย mask/เฟรมชุดนี้** ไม่ใช่แค่ “ระบุตัวไม่ได้” แบบรอบ #12. ตามคำสั่งในใบ **อย่ารัน GT-030 รอบสามเพื่อไล่ target panel**; chief ควรส่งต่อ static selection/render-mask path หากต้องการแตกสาเหตุ

อย่างไรก็ดี ภาพบังคับ before/after ทุก cadence ไม่ครบตามฟอร์ม: screenshot ใบแรกหลัง trigger ที่อ่านได้อยู่ที่ +3.487 วินาที และไฟล์ baseline/+0 ไม่ถูกเก็บคงอยู่ใน capture root แม้ผู้เทสเห็นสด จึงห้ามใช้ผลนี้ claim เรื่อง visual transient ต่ำกว่า 3.487 วินาที หรือรูปร่าง A ตอน stack กับ Navy Transfer. ข้อสรุป no-render ยึดจาก persistent A/B หลังจบชุดเท่านั้น

### GT-043 POP-SURVIVAL-001 — **PARTIAL / NO-RESULT เต็มใบ**

- ก่อน trigger ผู้เทสเห็นและคลิก `Navy Transfer`; wire event ยืนยัน target `0x2001`, placement P0, ชื่อ `Navy Transfer` เวลา 00:12:32.770
- หลังเฟรม count-1 bit `0x02` ทั้งชุด วัตถุโลก/เรือขนาดใหญ่จุดเดิมยังอยู่ในภาพ +75.721s, +88.397s และหลังเดินยืนยัน P2; ไม่พบการหายทันทีใน landmark เดียวที่ติดตาม
- แต่ใบนี้บังคับ NPC/วัตถุหลายตัว + P0/P0a/P0r และ P1/P1a/P1r มุมเดิมครบ ไฟล์ P0 ไม่คงอยู่และติดตามได้ชัดเพียง landmark เดียว ดังนั้น **ห้ามปิด GT-043 เป็น “ไม่มีประชากรหายทั้งฉาก”**. ข้อที่พูดได้มีเพียง “ไม่สังเกตเห็น Navy/world ship landmark ที่ติดตามหาย”
- ถ้าจะปิดใบตามเกณฑ์เต็ม ต้องพ่วง GT-043 ใหม่กับเลน bit `0x02` อื่นและเก็บ P0/P1 หลายตัวให้ครบ; รอบนี้เป็นหลักฐาน partial เท่านั้น

## Exact boot

- jobs 988 preflight / 989 boot / 990 console-title neutralizer / 991 teardown
- boot commit `b665d9276bcd05ac256132372310fb64d26b163f`
- tree `39edf49dd73a5307343eec1dc251f8a7067c21e1`
- exact archive tree `pf_bridge\boot_trees\gt030_20260823_000922`; main HEAD `cf817305327783c4187224c79df3150ced426ae3` ไม่ถูก checkout/แก้และ worktree clean
- scenario `scenarios\remote_player_hypothesis_visibility_probe.json`
- run DB `Pirate Force ServerProject\state\run_gt030_20260823_000922.sqlite3`
- capture root `GameClient\capture_gt030_20260823_000922`

## Wire / DB

- session start 00:10:07.399; chat `PFCHATPROBE1` 12 ASCII ถึง wire เวลา 00:13:53.332 หนึ่งครั้ง
- outbound ครบตามลำดับ: `SPAWN_BARE` 181 B (`late=0.4 ms`) → `SPAWN_AVATAR` 288 B (`1.2 ms`) → `MOVE_A_1` 72 B (`0.5 ms`) → `MOVE_A_2` 77 B (`0.6 ms`) → `NEGATIVE_CONTROL` 218 B (`1.2 ms`)
- cadence 15 วินาที; negative-control อยู่ราว 00:14:53. ไม่มี `compose_refused`, `already_sent`, `ErrorData=28317`, traceback หรือ stderr
- raw GAME `C:\Users\Panya\Desktop\Pirate Force\GameClient\capture_gt030_20260823_000922\capture_v141\GAME_20260823_001007_389467_52560.txt` — SHA256 `6F064A885A8F0AE9057E865638B83A253A691B5214C0682E89F7FB6C82F7CDFA`
- console `C:\Users\Panya\Desktop\Pirate Force\GameClient\capture_gt030_20260823_000922\server_console_live.out.txt` — SHA256 `27D1972F626D4E9DC285AB1FA9D2C2BFA08FC2722BD228631CC6A84D96A3904E`
- event log `capture_v141\GAME_EVENTS_LIVE.txt` — SHA256 `1885012DA0B7A1279FD6CF2F83F8D0089F158644A3F9F0B27BF2D07E9CF9096B`
- run DB หลังรอบ SHA256 `D076BEC22DACA40EEE2093F66C1DD3D9B565A64E33176EDFAA772659BFF00E40`; sessions with character=8, open=0, max lease_generation=9, integrity=`ok`, FK=0
- canonical ก่อน/หลังและ backup ตรงกัน `6BFCEDD5593D316A27A6C300206A9A3BEEC5E65631835308E02289B5FE498FC7`

## Client evidence + SHA256

Key frames:

- `GT030_final_negative_control_sideB_75721ms_20260823_0018.jpg` — `836BADA0EE2879FE6DC0FAE1EF68EF7D2B41C3D2038C275BB182D9AC771FBAAD`
- `GT043_P1_sideA_after_all_88397ms_20260823_0018.jpg` — `4462A85C815D6AF26D0FB087C63584AC7FA2B8071164B6173ECE23EC428EE107`
- `GT043_P2_walk_closer_after_all_20260823_0019.jpg` — `650A6FDC28E33B058F5C631C3C09027AB6CBBB2F51D0186FDD064F6AA6D7CE6D`
- `GT030_walk_exact_B_check_20260823_0022.jpg` — `2DB5151ADA5ECE44E250DDED8D65CDE2D7CAE0FA1032E7600B6A10C36D27E239`
- `GT030_A_exact_persist_20260823_0025.jpg` — `9D3E1A37FA3DA81462B32BA19DCBE03E85F537E32A728B8F5903128BE39D0788`

ภาพอื่นใน capture root:

- `GT030_A_Tab_1_20260823_0025.jpg` — `85FC286FD2A78A26F7102A94121E7E6F3C73BF75431168CCF262FB998934C006`
- `GT030_A_Tab_2_20260823_0025.jpg` — `7D94C7180F3F6AC22B05175BC81940827A1D2CF05DE5327F705B4E0D32A160A8`
- `GT030_A_Tab_3_20260823_0025.jpg` — `27D48E997A90EC13285E49028CD08ED2186B59F8C157C19D2EC98296AC450C77`
- `GT030_A_Tab_4_20260823_0025.jpg` — `74F0FABFA19551F92507D9EE51689DF25F9A94F3C7FECF8BC8EA6147836E5E9E`
- `GT030_at_A_close_20260823_0024.jpg` — `859DDA1AB3DF0C3A40FF73915B785CA4A5F309D8F8DFE38FDE090C25D24429ED`
- `GT030_at_B_360_1_20260823_0022.jpg` — `61AC8A8074AB0196D7F7EEE430C4231BE62FF3F4DCC0585C0DA00616E4C23F35`
- `GT030_at_B_360_2_20260823_0022.jpg` — `A4634AD9D60D1C5C37ED0F521EBB181D4CB53E9A5B29B39C8DA3AF3BC1D66410`
- `GT030_at_B_360_3_20260823_0022.jpg` — `573CE5DB6741A32D096404EF07DABE95A0A26FA4C7B32B1FB86778F631498B42`
- `GT030_at_B_360_4_20260823_0022.jpg` — `5E57E80C089D616174064EA5ECDD71286BC1BB95625C4499ABE78CE438DB10AC`
- `GT030_exact_A_final_check_20260823_0024.jpg` — `F9576E7A9110C4F49FC26F612A4801939B71051EFCFD01F9E0472A13B1FD44B2`
- `GT030_exit_dialog_20260823_0029.jpg` — `1105129831F7EF031E7A51C3C68C7BAF1C6F6A2A866A4623090E37F1F3FBB8A2`
- `GT030_near_A_final_check_20260823_0024.jpg` — `74381408D67070DE6051A7FF189374B641FF7A6FE12BD979CD5298610DA84E0C`
- `GT030_near_B_persist_check_20260823_0020.jpg` — `34D734E2CE4271B89E6F3D0B359EC75D361344ED572766AB91A75EFBACCFEDDF`
- `GT030_persist_360_Q500_1_20260823_0021.jpg` — `B95246F80AAA0BC9C583278A9B23E69D275BFF7E7298CBEB99D3A30F62B7F6DC`
- `GT030_persist_360_Q500_2_20260823_0021.jpg` — `C201550F16DB279CD7B016327327221CEEDD742AFF6BEF2B40A23143A7AEDE42`
- `GT030_persist_360_Q500_3_20260823_0021.jpg` — `2195AF9E7B0DD0584F025EDDD1EF746EE19BE780901DE8CF4D3438BD2660D607`
- `GT030_persist_360_Q500_4_20260823_0021.jpg` — `74F8A21B9728BD8125999894B3EF86EC583AAD79B4A0CDDAF45E31CB34BDC192`
- `GT030_P_tab_before_20260823_0019.jpg` — `084AB57888F8BF818B2D6D5A02CB500960D6789DBA5F97B64C9D3CF68C4C5BF5`
- `GT030_P_tab_after_20260823_0019.jpg` — `1595987A8A33D46BA317C984EB84A2474F040379357EAEB3EF53228C320C3D88`
- `GT030_walk_exact_A_after_move_check_20260823_0023.jpg` — `DC3F43A55440EEE3C169A0CA5B9B3C0159D35A1799C05A87217ED87A4AE37A98`
- `GT030_zoomfar_persist_check_20260823_0020.jpg` — `A392D5C03A9F95E52FD388E95B53D94EB0E88008B89C82275973700C851BC56B`
- `GT030_zoomout_persist_check_20260823_0020.jpg` — `3B08E6271B9C3025B71A5B3129F88720ED4422E06F536B97064D140FD1436711`
- `GT043_P1a_Navy_select_after_20260823_0028.jpg` — `934EF5771AEC1385D6CF947A750EA20B4CA64B538C439D127EE25014182459FB`
- `GT043_P1a_Navy_target_after_all_20260823_0026.jpg` — `181494873A3C3915103553F4B9B4583E6701E19BE6E301B982C9310B46DB06F3`

## Teardown

- GameClient=0, listeners 10188/10189=0, server/console stopped, inbox empty
- capture root ถูกต้องและมี 35 files; actual console ลงท้าย stopped marker=1, traceback=0, stderr 0 bytes
- receipt `pf_bridge\outbox\991_gt030_teardown.utf8.txt` — SHA256 `DD9590ECA7FF3E07A572FC6F2281F8E79DF9374880543AACB2D0BB7D95E3935F`
- canonical unchanged; main worktree clean

## Nonclaims

- เฟรม/สูตร/faction/mask เป็นดีไซน์ของเรา ไม่ใช่ของเซิร์ฟเวอร์ต้นฉบับ ซึ่งกู้ไม่ได้ตลอดกาล
- ไม่ claim ว่า mask bit ไหนจำเป็นต่อ render และไม่ claim ว่า click/Tab bind กับ actor_type 2 ได้
- ไม่ claim ว่า nameplate ลอยหัวต้องมี; ผล no-render ยึดจากไม่พบโมเดลที่ B/A ระยะประชิด ไม่ใช่จากชื่อ
- ไม่ claim visual transient ต่ำกว่า 3.487 วินาทีว่าไม่เกิด; การไม่ติดภาพ = unobserved ไม่ใช่ absent
- GT-043 ไม่ใช่ combat/aggro/persistence และรอบนี้ไม่พิสูจน์ประชากรทั้งฉากหรือสาเหตุระดับ `[mgr+0x24]`
