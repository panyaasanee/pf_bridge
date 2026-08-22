ถึง: chief + Panya

# GT-033 LOGOUT-TRANSITION variant C — PUSH 0x709E สำเร็จ แต่ไม่เกิด persistent transition

เวลา: 2026-08-23 00:01–00:06 (+07:00) · ผู้เทส: Codex ATTENDED (LOCAL)

## คำตัดสินที่เสนอ

**variant C = ผลลบที่มีค่า: client ไม่ transition จาก unsolicited `ReturnSelectServerVital 0x709E` เพียงเฟรมเดียวใน runtime-ready state ปกติ**

server รับ chat ASCII 12 ตัว `PFCHATPROBE1` หนึ่งครั้ง และส่ง pinned frame `0x709E` หนึ่งครั้งจริง แต่ client คงอยู่หน้าแมพเดิม ส่ง runtime heartbeat/keepalive ต่อเนื่อง และไม่ relog/reconnect จนผู้เทสกด X ออกเองประมาณ 63 วินาทีหลัง push

- ผลนี้ตอบเฉพาะ variant C ว่า **ไม่มี persistent transition**
- ตาม adversary caveat ห้ามสรุปว่า `0x709E` ไม่ใช่ trigger ทุก state: อาจต้องอยู่ใน state ของ logout dialog/request pairing ก่อน
- ห้ามสรุปข้ามไปว่า connection-teardown คือคำตอบ; variant A/B ยังติด BLOCKED-INPUT เดิม
- ไม่ได้ทดสอบ subcode 01 และไม่ได้ส่ง `LogoutVital`

## Exact boot

- boot commit `7b8002522fedeecf9bcd5ea9d0d4ec5e732e4034`
- verdict `origin/ci-status:ci/7b8002522fedeecf9bcd5ea9d0d4ec5e732e4034.json`: `sha` ตรง, `conclusion=success`, run `32444037989`
- tree `c624c210dd37e79b77c983f3e5fc0376c3fb3b96` ตรงกับ merge `c6146a3`
- materialized exact tree ด้วย `git archive` ที่ `pf_bridge\boot_trees\gt033c_20260823_000146`; main HEAD `cf81730` ไม่ถูก checkout/แก้
- scenario `logout_hypothesis_chat_push_return_select.json`; jobs 986 boot / 987 teardown

## Client-observable

1. เข้าเกมด้วย `Arena01`; map `Port Royal`, HUD HP 100/100, X -8,553 / Y -2,579
2. กด Return เพื่อ focus chat, พิมพ์ `PFCHATPROBE1` ครบ 12 ASCII ตัว และถ่ายภาพก่อนส่ง
3. กด Return ส่งหนึ่งครั้ง; chat input ว่างกลับตามปกติ
4. ภาพหลัง trigger ที่เก็บได้ที่ +4.002, +6.412, +7.325, +8.620 วินาที และภาพยืนยัน ~30 วินาที ยังเป็นหน้าแมพเดิมทั้งหมด ไม่มีหน้า character select/dialog ใหม่/process exit
5. ออกจากเกมเองด้วย X + ปุ่มยืนยันซ้าย; process ไม่ได้ปิดจาก `0x709E`

ข้อจำกัดสำคัญตามคำเตือนของ Panya: screenshot API มี latency ทำให้ภาพหลัง trigger ใบแรกอยู่ที่ +4.002 วินาที จึง **ไม่ claim ว่าไม่มี flash/intermediate visual ที่สั้นกว่า 4 วินาที**; สิ่งที่พิสูจน์จากสายตาคือไม่มี transition ที่คงอยู่ ซึ่งเป็น outcome ที่ pass criterion ต้องการวัด หาก 0x709E ทำให้กลับ character select จริง หน้านั้นควรยังอยู่ให้เห็นในภาพต่อ ๆ มา

ภาพและ SHA256:

- `GT033C_pre_trigger_20260823_0002.jpg` — `D8E8862FA96591F01E2CA952B843E3945AF27679E15ECEFFADC42F67B3154560`
- `GT033C_chat_typed_20260823_0002.jpg` — `36600A1168E7A80A88D8FC3BC55CF12DC9B4D53E3CE54D4D38532EC498A5F26B`
- `GT033C_post_immediate_4002ms_20260823_0002.jpg` — `0225707A57287ECF169314198597944C8CBA809929EE7254C0FBCFD9A93A2802`
- `GT033C_post_plus150_6412ms_20260823_0002.jpg` — `09D77255F9CA22B8D81DAC3521D102221A66B63A68E3C083C7CC39D2A0A9BA0F`
- `GT033C_post_plus500_7325ms_20260823_0002.jpg` — `91C08512D31E9A19ED121FF802C250A18743C29113C70191DC366D5EC1750F7B`
- `GT033C_post_plus1300_8620ms_20260823_0002.jpg` — `3048B2583699518AE5EDF2DD8ECD8585AE613030025B35FE59220EAF42EABC2B`
- `GT033C_still_in_map_30s_20260823_0003.jpg` — `776A526E8A14F3514A84BD4F99F60C178A56AA3362106FF9421EDF236924E296`

## Wire / DB

- `SESSION_START` 00:03:14.395; chat event 00:04:31.000
- inbound frame #43: vital `44114 / 0xAC52`, payloadเป็น UTF-16LE `PFCHATPROBE1`, count=1
- outbound label `HYP_PF_031_LOGOUT_CHAT_PUSH_RETURN_SELECT_SERVER_UNSOLICITED`, `late=0.4 ms`, count=1
- PC 38 bytes SHA256 `A4C8DF4299EA7C3A5EE5554D1D29D7F8C1A2B51031CA210CBEB9AF2AD9D4CA9E` ตรง scenario pin
- full frame 48 bytes SHA256 `08C2A925BD67CD3D0AFA7992F98D472ED8FD22787756521A5DF8CBF174E5CB8E` ตรง scenario pin
- หลัง push client ส่ง runtime req #44 ต่อเนื่องถึง #95; ไม่มี second session/relog และ push count ยัง 1
- `LogoutVital` runtime count=0; `ErrorData=28317` count=0; traceback=0; actual stderr=0 bytes
- run DB เพิ่ม session ตาม writable-flow ปกติ: lease `9`, selected_character_id `1`, opened `2026-08-22T17:03:14.357015+00:00`, closed `2026-08-22T17:05:34.178316+00:00` (00:05:34 +07, ตอนผู้เทสออกเอง); open sessions=0, integrity=ok, FK=0
- canonical และ backup SHA256 คงเดิม `6BFCEDD5593D316A27A6C300206A9A3BEEC5E65631835308E02289B5FE498FC7`; run DB หลังรอบเป็น `09F7BAA56E254BACF09822196E065D8437DD908DAD6EB8C8C9CA6CA0039E37D0` ตาม session write ที่คาด
- raw GAME: `C:\Users\Panya\Desktop\Pirate Force\GameClient\capture_gt033c_20260823_000146\capture_v141\GAME_20260823_000314_384738_51326.txt` (170,898 bytes)
- actual console: `C:\Users\Panya\Desktop\Pirate Force\GameClient\capture_gt033c_20260823_000146\server_console_live.out.txt` (44,372 bytes), ลงท้าย `[FOUNDATION] stopped`

## Teardown/tooling note

- final: GameClient=0, listeners=0, inbox empty, main worktree clean, canonical unchanged
- job 987 เป็นสำเนาตรงของ generic template จึง derive job tag ถูกต้อง แต่ capture collector เลือก `capture_v142` แทน `captureroot` จาก info file เมื่อไม่ได้ส่ง `CaptureFilter`; count/stopped-marker ใน receipt ของ 987 จึงเป็นของ root ผิดและไม่ควรใช้อ้างผลรอบนี้
- raw root ที่ถูกต้องด้านบนถูกตรวจแยก: actual console `[FOUNDATION] stopped`, stderr 0, GAME ปิด 00:05:34, ไม่มี traceback
- ขอเจ้าของ tooling พิจารณาให้ template ใช้ `captureroot` จาก newest info file เป็นค่า default หรือ fail หาก path กับ filter ไม่ตรง

## Nonclaims

- ไม่ claim ว่า response นี้คือของ original server ซึ่งกู้ไม่ได้
- `0x709E` ยังไม่ถูก confirmed เป็น trigger และผลลบนี้แยก “wrong trigger” ออกจาก “right trigger but wrong client state” ไม่ได้
- field values ของ `0x709E` เป็น zero default ไม่มี producer
- ไม่ claim ว่าไม่มี visual flash ต่ำกว่า 4 วินาที; claim เฉพาะไม่มี persistent transition และ connection ยังทำงานต่อ
- one-shot เป็นราย connection; รอบนี้ไม่มี relog และไม่ได้ยิงครั้งที่สอง

