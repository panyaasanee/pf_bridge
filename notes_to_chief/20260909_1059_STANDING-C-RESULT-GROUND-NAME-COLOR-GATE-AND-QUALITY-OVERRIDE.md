งานเป้าหมายยืน — ยังไม่มีเลขใบ ขอให้ LANE-K ตั้งเลขและผูกจดหมายนี้
C1a · ปิด 2026-09-09T10:59:45.602086+07:00 · Ground-item name color: wire gate/seed, local quality, and create/update asymmetry · IMAGE + DATA · PARTIAL
ADDRESSEE: LANE-K · cc LANE-B, LANE-GM, chief
BUILD_PROPOSED: สีป้ายของตกตามคุณภาพ พร้อมคงสีหลังรีเฟรช | LANE-B + LANE-GM | proof: เจ้าของยืนยันป้าย NameBoard_ITEM ของไอเทมเดิมจากการสร้างใหม่และอัปเดตซ้ำ; ผูก key/item id/gate/seed/เฟรมจริง และทดสอบสามแขนท้ายจดหมาย
BUILD_IMPACT: ตัวเลือกสีมาจากทั้งสายและตารางในเครื่อง; แค่ส่งไอเทมต่างคุณภาพยังไม่ทำให้ชื่อแยกสีเมื่อ gate ปิด. อย่าแปลง wire seed เป็นคุณภาพไอเทมที่บันทึกถาวรโดยอัตโนมัติ.

[MEASURED A / IMAGE] Exact label and field ownership
DropThingGameObj ctor5F49C0 stores item-nameboard at+80, creates it via5BBC40 (vtF2CDC0), calls v14=5BE2F0. That initializer requests NameBoard_ITEM@F2CFF8, finds LABEL_ITEM_NAME@F1C7F4, type-checks UILabel and stores it at nameboard+30. DATA NameBoard_ITEM.model has exactly one UILabel, second child in Controls, ID LABEL_ITEM_NAME, default FontStyleID55.
5BACF0 receives the selected integer, calls this label.v13C. UILabel vtF8AA28.v13C=AA37D0 stores label+90, looks up registry style viaA9F590 and calls v144=AA6EF0; that apply routine passes style+30..3C to vD8=6D0F40. This closes the specific item-label FontStyleID route.
field_key: TerrainThing@0x14.4#W (item data key), TerrainThing@0x1B.1#W (name-style gate), TerrainThing@0x1A.1#W (signed-at-consumer style seed). All are scoped to this class. UIFontStyle@0x30.16#R is the RGBA color consumed by this UILabel.

[MEASURED A / IMAGE] Wire shape and defaults
TerrainThing codec5F85B0: per element key+10 tag14/u32 and mask+28 tag0B/u8. Mask02 carries item key+14 tag14/u32; mask08 carries gate+1B tag05/u8; mask10 carries XYZ; mask20 carries seed+1A tag08/u8. Order is item key, optional mask04/+18, gate, XYZ, seed. In a record carrying item/XYZ/gate/seed, mask3A includes those fields; with the existing +18 field retained it is3E. These are field masks, not outer opcodes.
Fresh AND reused pool5F82C0 initialize gate=0 and seed=1 (5F832C/35 and5F83C6/CD). Thus a freshly decoded record omitting the gate retains0. Do not assume the previous packet's gate survives omission. Existing reconciler calls5F4C00 at6AFDE9; new-key branch calls5F41E0 at6B01A0. 

[MEASURED A / IMAGE] Creation differs from later update
At create5F41E0, seed is sign-extended at5F433E and saved locally. After model/nameboard prerequisites succeed,5F47FE tests gate:

- gate0: request FontStyleID52 (34hex).
- gate nonzero AND signed seed1..6: request table[seed], exactly93..98 fromF30EC8.
- gate nonzero with any other signed seed: skip this style setter. The DATA model begins with55; “no setter” does not guarantee untouched pixels.
The create color branch uses the wire seed; it does not perform the update branch's n_QUALITY replacement.
At update5F4C00, after label/world and item-row prerequisites succeed,5F4D04 tests gate:

- gate0: request52.
- gate nonzero but signed seed<=0: request52, without the n_QUALITY query.
- positive seed: query local n_QUALITY@F0C190 via5F4D2D. A present value>0 replaces the seed. Missing/nonpositive quality leaves the seed. The resulting value1..6 maps93..98; otherwise request52.
Raw seeds128..255 are negative here. A positive seed7 can become a valid color after a table override even though create skipped its setter. A table value7 overrides a valid seed but then falls back52. Do not treat absent/zero quality the same as positive out-of-range quality.

[MEASURED A / DATA + conditional IMAGE apply] Palette
BigFontStyle.fsl entries consumed through the style registry:

| selector/result | FontStyleID | RGBA | data color |
|---|---:|---|---|
| gate0/fallback |52|(244,61,57,255)|warm red |
| seed/quality1 |93|(255,255,255,255)|white |
|2|94|(0,236,0,255)|green |
|3|95|(81,168,255,255)|blue |
|4|96|(179,102,255,255)|purple |
|5|97|(255,128,64,255)|orange |
|6|98|(255,255,0,255)|yellow |
93 has no explicit FontColor attribute: loaderA9F860 creates a fresh style with ctorA9D6B0 initializing all four color floats to1.0; parserA9DAE0 retains them when FontColor is absent. Style55 also omits FontColor. Explicit components pass through53F7B0/53F5E0, division by255 and clamp[0,1]. Block40867A..4086EB requests .\Data\GUI\Model\BigFontStyle.fsl into global manager1090708. Actual loader success, later registry changes, style-cache equality, rendering and pixels remain runtime conditions.
Local n_QUALITY is NOT_WIRE in this path; the wire item key chooses the row. DATA censuses (full distributions in manifest): ITEM_MISC1646 rows; EQUIPMENT_BASE974; ITEM_CONSUMABLES1260. These are not observed drops or original quality-roll probabilities.

[CODE observation / bounded] Current composer connection
Read-only mob_loot.py: _element_via_tags uses mask12; _element_via_tags_with_model_type uses mask16. Both omit name gate08 and seed20; their code therefore does not ask this color path to use item quality. This is compatible with one fixed style across different item rows. It does NOT establish which function/frame produced the owner's observed orange labels; style52's exact RGB is reported above rather than silently calling it97/orange. Source SHA is pinned, no server code or runtime changed.

[PROPOSED D] Three-way same-item test
Use one verified item row with n_QUALITY2 and a visible model, holding item/key/position/model-type constant. On a fresh creation in each separate run: A gate0 seed2 predicts52; B gate1 seed2 predicts94; C gate1 seed5 predicts97 on create and94 after an update of the same key. Record both phases; a native frame may skip visible intermediate colors. Preserve the full ground-key set required by the existing collection contract. Do not isolate one key by omitting other live drops. Stop and retain exact evidence if model/label is absent, item row differs, keys disappear, or a reply changes unrelated state. No run performed here; this composition and arithmetic are ours, not the original server's policy.

Evidence: staged/standing_c1a_manifest.json SHA1f0c12692d80c6c98698f05754a25c768f1e8770318750612e6b7ce2b930fcf6; spans pin start/end-exclusive VA, file offset and SHA; IMAGE14759424 bytes SHA9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623. Python -B staged/standing_c1a_verify.py PASS32 spans/20 ranges/2642 instructions/10 inputs/21 calls/82 pins/5 slots/4 codec tag/width checks/8 font rows/1 label/3 DATA censuses/5120 bounded branch evaluations/12 counterexamples. Source hashes before/after.
Focused search matched FILES external5/gamedata8/reference17/archive99/consumed16; query/paths in search_focused.log. Initial scope0/0/0/24/9 in search.log. Reused GDL render/codec facts and MCG font parse/apply, newly joined to this item label and create/update branches. Read EVIDENCE_GATES this round.
Adversary: actual frozen review found no substantive defect; verifier exit0. Branch evaluations verify reconstruction, not native execution. Open: whether a rendered frame exposes the create color before update override.
nonclaims: no native test/pixels, original item-quality distribution, exact causal diagnosis of all-orange footage, automatic inventory rarity/persistence, sender authorization or complete rendering-state census. No queue/reference/ServerProject/DB/Git/lease edits.
SCOREBOARD: NONE | Standing C IMAGE+DATA evidence | no runtime promotion
