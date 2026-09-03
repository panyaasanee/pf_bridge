[ถึง: chief cloud (cc), Claude และ Panya · จาก: OpenAI Codex static RE]

# Checkpoint 12:51 — GM / monster color / ground drop รอบสาม

บันทึกเวลา `2026-09-01T12:51:43+07:00`; heartbeat ล่าสุดที่อ่านได้คือ `2026-09-01T12:40:02+07:00  pf_git_sync woke and finished a round, HEAD e339864`.

## ขอบเขตและการไม่สร้างผลซ้ำ

- ตรวจค้น deliverables เดิมก่อนทำและขยายไฟล์ canonical สามชุดเดิมเท่านั้น ไม่สร้างตารางคู่ขนานหรือ duplicate output; `PF_GROUND_DROP_TRANSPORT.*` ไม่ถูกแตะ.
- Codex อ่าน ServerProject เพื่อ audit/cross-check ได้และได้ทำจริง แต่ไม่ได้แก้ ServerProject, ไม่รัน tests/server/client, ไม่แตะ Git/workflow/queue/lease และไม่แก้ frozen V141.
- เขียนเฉพาะ `pf_bridge\external`, note ใหม่นี้ และรายงานสะสมที่ root `Pirate Force`; ไม่คัดลอก raw bytes จาก dump/capture.

## ผลที่ปิดเพิ่มและตรวจซ้ำแล้ว

1. **GM plugin gate:** 16 rows = IMAGE 14 / DATA 2. Slot `+0x08` ปิด exact ABI แบบ `PROVEN_EXACT_ABI_NO_PINNED_ROUTE`: default-construct stack-passed MSVCP90 wstring destination, EAXคืน pointerเดิม, `ret 4`; ไม่พบ pinned direct E8/E9 หรือ application virtual-call route. Slot8เป็น optional hardening ไม่ใช่ proven open-window gate. TSV `06e6e650916708721d2a286738b51578be982f5d270891e9ad9ab373ff80c5e8`; MD `a8e5959a0322ec54251aaba6f4ca1ab9632164a132f5c8a77c24666d9677a1eb`; generator `c677a41830c20a9ece8e01b72c00e35c54d80c5cd08dbb45292de159487b34c8`.
2. **Monster color gate:** 61 rows = IMAGE 53 / DATA 8. `MCG-IMG-046..053` ปิด static readiness bit `0x40`, `+0x258/+0x260`, distance, registry removal, LABEL_NAME FontStyleID/style apply และ indirect render submission. แปดแถวท้ายเป็น `PROVEN_EXACT_MANUAL_HASH_ANCHORED`; checkerพิสูจน์ integrity ของ pinned inputs/spans/rows/output ไม่ใช่ symbolic derivationของ semantics. TSV `85fc315cd734637069c039c256cb061567cbcdb04adc8bedabc1cea6fa315b72`; MD `51234ccd51a93570b8e220fb641bfcbf3383b29d5f14ebee808d20eebc4fc9d6`; marker `c8ea32f3d6575b76c8389d01f7ee92281b389f2a1dd99b7c5771084eddc77082`; generator `2d2adbfdfbef18d2cbe3a8ecab64d50c924db082846e1558616ac66969a9221f`.
3. **Ground-drop lifetime/resolver:** 26 rows = IMAGE 21 / DATA 2 / CAPTURE 3. ปิด installer callsite/setter write, `.nif` extension dataflowไป `.ni_`, packaged-first/loose fallback, `$pcz`/LZMA-shaped decode และ first qualifying parsed NiNode. ไม่อ้าง runtime callback reachability/order/overwrite และ non-null NiNodeไม่ใช่ geometry/pixels. TSV `c364de49000a1a95d5bea8867665d28c47e352ae5a4bc1a99871b9391614fefd`; MD `89c816f4aea8bb016767db46d0c570b678151e27d7556e8cdf6a769b4031ddc9`; generator `09a75f1f8565d060cb4598eb6d7b74c125d5dcb766ad7e7bcb6215c2e899b070`.

ทั้งสาม re-deriver `--check` PASS หลัง publish; imageคง 14,759,424 B / SHA-256 `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`. Adversarial re-review ของ GM, color และ drop ผ่านทั้งหมดหลังแก้ขอบเขต overclaim.

## ข้อความ ServerProject ที่ขอให้ Claude แก้ในรอบเขียนถัดไป

1. `tools/pf_mine_scene_drop_tables.py:43-44` — “column explains nothing about drawing” กว้างเกินไป: `n_DROPMODEL_TYPE` เลือก NIF pathโดยตรง แต่ยังไม่เพียงพอให้เห็น geometry.
2. `docs/FUNCTIONAL_COVERAGE.json:911` — ประโยค “nothing ... reads the +0x14 dword” เป็นประวัติล้าสมัย; static reader/model selectorปิดแล้ว ควร append correctionไม่ลบประวัติ.
3. `src/pirateforce_foundation/mob_loot.py:546`, `scenarios/combat_loot_001.json:44`, `tests/test_mob_loot.py:1764` — ข้อความ “63 IDS” ต้อง re-deriveและแยก production emit universe ออกจาก externally specified 43-ID audit set; ห้ามเปลี่ยน 63→43แบบเดา.
4. `src/pirateforce_foundation/gm/bt_gm_probe.py:28` — factory `0x007280D0` ไม่ได้พิสูจน์ว่า “constructs GMUI_BASIC”; หลักฐานปัจจุบันชี้ panel/model object และ `GMUI_BASIC` เป็น child/tab lookup.

Codexไม่ได้แก้สี่จุดนี้เพราะ Claudeถือ active write lease. Read-only source pinsล่าสุด: `runtime.py` 470,668 B / `609f273c66a2c58ffa3d95b502e43b98d092e2dd768dcbb8008a8eff2732bae3`; `mob_death.py` 152,904 B / `7c0daee1e1532b18c2e2bdeb83fbc4bb65d91394c716409e599369f9f87f614e`; frozen V141 `2eb05ed2fdbdd5ee3d91f7fbb8c1d16a4c7a02a843bc97169b16a389e4ea4c22`.

## สถานะ Attr และสิ่งที่ยังต้องวัด

- Main generationไม่เปลี่ยน: `b96e420c290201ce60babec398fd2389ea36db2f2f30ce552d9d680f481f3fae`; 490 field rows; semantic `UNKNOWN 42` (8.57%); scope `UNKNOWN 210`; field-status delta `0`.
- GMยังต้องมี owner-authorized x86 buildและ attended panel→tab→clean shutdown.
- Colorยังต้องวัด live gate satisfaction, style registry 56–63, actor/reference positions, membership timing, renderer/culling/device และ framebuffer pixelsของ actorเดียวกัน.
- Drop discriminatorถัดไปคือ ณ actual resource request slot `0x01027B8C` เท่ากับ callback `0x00B02300` หรือไม่; จากนั้นวัด actual branch/decode/parser/NiNode descendants/geometry, pickup/expiry/persistence.

## ส่งมอบ

- รายงาน canonical: `C:\Users\Panya\Desktop\Pirate Force\Pirate_Force_Codex_Audit_Recommendations_CHECKPOINT_20260831.md` — 133,306 B, SHA-256 `4a4ea4f4dba837968acdca390dfc6ccca53b192efdb0419f9918794f90fcefb7`.
- Snapshotก่อนแก้รอบนี้: `C:\Users\Panya\Desktop\Pirate Force\audit_history\Pirate_Force_Codex_Audit_Recommendations.b96e420c2902_20260901_1243.md` — 128,628 B, SHA-256 `71feb919ddc1dcc14912097fc6955fcc30d7180f6d04031bf5bde82915b26d57`.

สถานะ: checkpoint ส่งให้ทีมอ่านได้; goal static RE ยัง active และไม่ได้ประกาศว่าจบงานทั้งหมด.
