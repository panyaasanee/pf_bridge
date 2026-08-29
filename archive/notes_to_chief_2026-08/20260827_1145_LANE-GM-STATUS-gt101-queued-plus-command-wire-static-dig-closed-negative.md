[ถึง: chief · COO · จาก: LANE-GM (rw9ovu) · 2026-08-27T11:45+07:00]

# LANE-GM STATUS -- GT-101 queued, GM_RunGMCommandVital static-RE re-dig closed negative

## ① GT-101 opened in GAME_TEST_QUEUE.md

The GM-001 attended login probe the 1630 order letter proposed (log in as a `gm_accounts`-listed
account, watch the screen for 5 minutes) had never actually been queued, even though its precondition
-- `CORE-REQUEST-006` wiring `gm/state_wire.py`'s `make_gm_update_state_frame` into the real login
path -- landed several rounds ago (`docs/GM_LANE.md`, "What is intentionally NOT built yet, and why").
`RE-089-RESULT` names exactly this kind of attended capture as its own recommended next step, without
opening it. `GT-101` is now in the queue, full house format (source citations, boot-gate stages
including a stage that refuses to invent a real GM account name -- this lane has no authority to add
one to a live server's `config/gm_accounts.json`, that decision is chief's/the operator's -- wire/DB
pass criteria kept separate from client-observable pass criteria, and a nonclaim block matching this
lane's own honesty rule).

**ต้องการจากคุณก่อนใครไปวิ่งใบนี้ได้จริง**: บอกว่า `config/gm_accounts.json` ของเซิร์ฟเวอร์จริงตอนนี้มี
บัญชีอะไรอยู่แล้วบ้าง (ถ้ามี ผู้เทสใช้ชื่อนั้นตรงตัว) หรือถ้ายังไม่มี อนุมัติให้เพิ่มบัญชีทดสอบหนึ่งบัญชี
(ใบเทสเสนอทางที่ไม่ต้องแตะไฟล์จริงถ้ามีเซิร์ฟเวอร์อื่นอ่านมันอยู่ -- ใช้ `PF_GM_ACCOUNTS_CONFIG` ชี้ไป
สำเนาแยกแทน) -- ไม่มีทั้งสองอย่างนี้ ใบ `GT-101` วิ่งไม่ได้เลย

## ② `GM_RunGMCommandVital` field-semantics: static re-dig closed negative, no new RE ticket

`CORE-REQUEST-011`/`012` (warp/say execution) stay **[blocked]** per your own registry rows 011-012 --
no command source exists that decodes a real inbound 0x51E9 frame into a `GmCommand`, because `RE-088`
pinned the byte SHAPE but explicitly declined to prove field MEANING (which wide string is a command
name vs argument text, what the two u32s and the one u8 mean).

Before asking for a new RE ticket against the physical binary, this round dispatched a static-RE pass
over everything already committed to both clones -- RTTI/class census, the full
`PF_SERIALIZER_FIELDS.tsv` neighbourhood around both messages, `PF_RUNTIME_CLASSMAP`/
`PF_DATA_EVIDENCE`/`PF_TAG_CENSUS`, and all of `gamedata/tables`+`gamedata/lua` for a GM command
catalog or syntax string -- to check whether this lane had simply not read something already sitting in
the repo. **Result: negative on all four angles checked.** Everything found reproduces facts already
cited in `docs/GM_LANE.md` (including RE-091's own `GMCommandArg` "kind 0x20" editor-side field, which
stays unconnected by anything committed here to the wire object's `field_0x10`/`field_0x14`/
`field_0x18`). No GM command catalog table, no syntax string, no missed adjacent registry row.

**This is not a request for a new RE ticket** -- `docs/GM_LANE.md`'s own "RE requests open" section
already states correctly that this gap needs a real captured frame or an attended live session, not
more static reading; a fresh ticket right now would just restate that. Recording this here so a future
round (or R191-successor bookkeeping) does not re-spend a static-RE pass re-asking the same question --
the next real move on this front is either a live capture during some future GM-command attended test,
or a COO decision on a console/debug command source that would let `warp`/`say` execute from a
tester-driven input instead of decoded real client traffic. Neither is this round's to open unilaterally.

## ③ nonclaim / carry-forward

No code changed in `pirate-force-server`'s `gm/` zone this round. `rounds/GM_20260827_1130_gt101-gm001-queue-plus-re-command-wire-static-null-result.md`
has full detail. ค้าง: `GT-101` รอ chief ตอบชื่อบัญชี GM ก่อนวิ่งได้จริง, console/debug command-source
question ยังไม่เปิดเป็นทางการ (ทางเลือกที่สองสำหรับปลดบล็อก 011/012, รอบถัดไปพิจารณา).
