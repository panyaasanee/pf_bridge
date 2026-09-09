งานเป้าหมายยืน — ยังไม่มีเลขใบ ขอให้ LANE-K ตั้งเลขและผูกจดหมายนี้
ADDRESSEE: GT-272 equipment owner / LANE-B / CORE / LANE-K / chief / Panya · Codex static RE
B1n · ปิด 2026-09-09T13:04:29.354352+07:00 · IMAGE A / DATA A / proposed integration D · NEWPROGRESS: RH203's configured buff and hitrate scaling

[MEASURED] Answer: EQUIPMENT_BASE row203 (full item2200203) has n_ID_BUFF15211, whose BUFF row declares ADD_HITRATE(0.025). The effect multiplies a STANDARD_BUFF value. With STANDARD_BUFF1.f_HITRATE100, a zero aggregate becomes2.5 internal units. A concrete item-data consumer computes this into temporary aggregates. That path does not prove that equipping the sword automatically updates the actor's CBuffAttr. B1e supplies a separate CBuffVital trial seam.

ค้นชุดส่งมอบแล้ว: เจอ prior B1e BUFF loader/parser/lookup/apply proof, B1h item-table key proof, B1d hitrate getter/UI binding; selected IMAGE span hashes verified. Focused n_ID_BUFF/s_VARYDATA search found no prior answer for this consumer. Search paths/lines recorded; no global absence claim.
ค้น gamedata แล้ว: เจอ EQUIPMENT_BASE, BUFF, STANDARD_BUFF and STACK. Original PCZ re-parsed for these four complete table ranges, then five selected rows compared with TSV values. Coverage checked first; both equipment rows remain in_progress.

[MEASURED][DATA A] Selected inputs; each row's decoded range/hash in manifest:
| table | row | selected values |
|---|---|---|
|EQUIPMENT_BASE (code22)|201|n_ID_BUFF0; s_VARYDATA empty; SWORD/model3/map2/type1|
|EQUIPMENT_BASE (code22)|203|n_ID_BUFF15211; s_VARYDATA71; SWORD/model4/map2/type1|
|BUFF (code51)|15211|n_STACK999; n_BUFF_TYPE0; f_DURATION0; constant ADD_HITRATE(0.025)|
|STANDARD_BUFF (code46)|1|f_HITRATE100.0|
|STACK (code56)|999|n_POSITIVE0; n_MAX_STACK999; n_STACK_PROPERTIES0|
BUFF15211 conditional/FXS/animation strings are empty. Zero n_ID_BUFF does not prove absence of other stats. s_VARYDATA71 remains opaque. Primary lookup uses row15211; do not prefix it with table code51.
Raw PCZ SHA496b5c7b5a7f4c1ab5e343937ca7278b3db5b4501250caa7da47f22dc2c9c3f8; decoded8443000bytes SHA496dfb2ef2cf517482a7b426c9dd5edf0278564fe11195b96f36df90607f0d2d.
BUFF15211 row range[2104372,2104464), SHAc0b9cb2e0ac39d935f48f368b2ca0cae453d3e30d720f5f713861ece1a57e8f5.

[MEASURED][IMAGE A] Numeric item-consumer route, bounded:
-5B0F90..5B14C6 accepts full ItemID. Its quotient selects table via890FC0;46B3E0 extracts remainder and890E70 selects row. Thus2200203 resolves code22/row203 under the proven registration.
-5B1379 supplies UTF16 n_ID_BUFF(F0C964) and default0 to891FD0. This helper reads the named type0 integer column, otherwise returns its supplied default. Nonzero result goes through5B139D to5B0750, with category33; zero bypasses this branch. Category33 is a local call argument, not a newly identified wire opcode.
-5B0750 supplies primary ID and a sum of its third/fourth scalar arguments to5B04D0 at5B0787. The upstream caller also uses global10224E4 in one scalar calculation. The proper scalar values from a live item instance are not closed here; do not choose a secondary key solely from n_CONDITION_LV/n_ITEMLV.
-5B04D0..5B0539 initializes TWO stack-local aggregates through64EF80 and passes their addresses to64A810, using manager getter424990. Getter returns10317C0; ctor64A650 calls loader655A40. This is not asserted to be B1e's runtime manager instance.
-64A810 resolves primary via4A1C70, secondary via652CF0; missing either returnsfalse. Secondary0 returnsnull; values above manager44 are clamped to that stored maximum. With primary/secondary and first output nonnull, it dispatches primary+BC constant effect.v0 into the output; the second output covers a separate effect vector. These outputs are the stack buffers from this caller, not actor248. Line-building remains PROVEN_ROLE_ONLY; no exact tooltip row claimed.

[MEASURED][IMAGE A] ADD_HITRATE producer and consumer:
-655A40 loader attaches the parsed s_CONSTANT_BUFF list as established in B1e. Parser653B90 recognizes ADD_HITRATE at6545A4/AD, requests numeric argument1 through4319B0 at6545E2, stores float descriptor10 at6545F5 and installs vtableF37020 at6545F8.4319B0 uses imported _wtof and narrows the result tofloat32. Invalid/missing parser arguments are not a valid fixture.
- STANDARD_BUFF f_HITRATE(F14D14) is read through891F30 at656272 and, on successful typed read, stored at compiled secondary64 at656282.
- F37020.v0=650D30: reads secondary64, multiplies by descriptor10 in double, adds destination64, narrows tofloat32, snaps results within inclusive +/-float32(1e-5) tozero, then stores destination64. v4=650D80 performs subtraction with the same snap. This is aggregate arithmetic, not server hit-probability authority.
- B1e runtime application uses CBuffAttr+C0 as aggregate base, so this field becomes CBuffAttr124. FightAttr getter4687F0 explicitly reads its CBuff input124 at468821 and adds it to its other terms, with a minimum-zero clamp. The temporary caller above does not establish that live update.
- WIDGET-SLOT reused/rehashed: Char_Info2 LABEL_HIT, handler11C, UILabel at model-local(160,45); binder name/lookup/store exact.57ED6B calls4687F0, formats through %.2f%s at57ED80, then widget.v128 at57EDB2. Suffix/global state and pixels are not measured. Do not label2.5 as2.5% probability merely from this calculation.

[PROPOSED][D] Arithmetic control: aggregate0, secondary100.0 and parsed multiplier0.025 ->float322.5; subtracting the same contribution returns0 after the near-zero snap. A hypothetical base value1 instead of100 yields approximately0.025. Offline arithmetic only; this does not mean STANDARD_BUFF row1 has value1.
BUILD_PROPOSED: Extend the RH2200201->2200203 appearance fixture with a separate CBuffVital trial using primary15211 and secondary1 only after config/bucket/identity gates are established; reserve one source/serial and remove using that exact key, compare CBuff124 plus LABEL_HIT before/add/remove, preserve unrelated stats | GT-272 equipment owner / LANE-B, LANE-K to bind | exact frames+input identities+aggregate/HIT observations with return to baseline; no success inferred from model replacement
BUILD_IMPACT: This adds a sword-linked buff candidate to B1e's earlier trial options. The original server's equip-to-buff emission, legal secondary choice, duration/stack policy and duplicate behavior remain unproven. Do not append buffs on every repeated equip or promote this proposal into accepted gameplay.
nonclaims: No native/client/server execution, authoritative equip/unequip transaction, automatic stat application from ItemOperateVitalRes, all stat producers, actual hit chance/damage, tooltip pixels/row, s_VARYDATA semantics, persistence/reconnect or runtime promotion. No queue/lease/ServerProject/reference/asset/Git writes.

Evidence: IMAGE14759424bytes SHA9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623. Exact spans/file offsets/SHA and16 source hashes: staged/standing_b1n_manifest.json.
item_stat_consumer: VA005B0F90..005B14C6, file1B0390, 1334bytes, SHAc1207a107b3aa5677194429bbf3349f3843a21aca918652e7789639aca88832b.
Manifest SHA847569d7854230b5a30b5bcc5ebf6ad43bbab0d7ac099effd99405c356683a31; verifier standing_b1n_verify.py SHAbc58ec89240bcd8d60a80957f2e86ff6f44bba80407bd9bd67fe9485418661de; log SHA35e345fd5b05e18ad406eb6e61f5cf4818bec3c5967d05303bb26a4d6abbb34c. PASS35spans/27ranges/7354ins/16sources/722calls/191pins/57independent anchors/4raw tables/5rows/2vslots/1UI binding/1import/5arithmetic controls. Inputs checked before/after.
ADVERSARY: a6f_review found no material defect; verifier exit0. Argument/output order and finite arithmetic rechecked. Original secondary-key/equip transaction remains open.
SCOREBOARD: NONE | Standing B1 IMAGE evidence | no runtime promotion
