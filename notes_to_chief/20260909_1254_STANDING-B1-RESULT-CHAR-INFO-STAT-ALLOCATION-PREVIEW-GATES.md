งานเป้าหมายยืน — ยังไม่มีเลขใบ ขอให้ LANE-K ตั้งเลขและผูกจดหมายนี้
ADDRESSEE: GT-272 equipment owner / LANE-B / CORE / LANE-K / chief / Panya · Codex static RE
B1m · ปิด 2026-09-09T12:54:36.145197+07:00 · IMAGE A / original UI DATA A / example D · NEWPROGRESS: distinguish local stat allocation preview from equipment stat observation

Answer: CharInfoEventHandler+1B9 is used by the character-panel stat-allocation controls. In the reviewed refresh path, LABEL_STR/CON/DEX/INT/PER still receive their FightAttr getters directly; pending allocation has separate LABEL_DEPLOY_* controls. However ten derived labels, including LABEL_ATK, add local pending values when1B9!=0. A higher ATK display alone therefore cannot establish that an equipment response changed authoritative stat inputs. This refines B1d's previously untraced preview qualifier.

ค้นชุดส่งมอบแล้ว: เจอ B1d's exact refresh/binder/vtable and prior stat formulas; their selected spans were rehashed. Focused57C190|57D410|57D760|Deploy_OK|ResetDeployPoint|handler+1B9|stat.preview found no additional result in external/server docs and one prior B1d letter in notes. Broad1B9 SHA false positives excluded; focused search recorded. No global absence claim.
ค้น gamedata แล้ว: เจอ Char_Info2 model references. The original GameClient/Data/GUI/Model/Char_Info2.model supplies32 selected controls, each joined to an IMAGE name/lookup/store. No constant table needed for the local control trigger. Coverage checked first; equip_unequip and appearance_and_avatar_binding remain in_progress. Exact search and source hashes are in the manifest.

[MEASURED] 1. WIDGET-SLOT, offsets belong to CharInfoEventHandler; positions are model-local, not screen pixels:
| handler | control | Position | role in this path |
|---|---|---|---|
|84|LABEL_STR|(128,45)|FightAttr STR result|
|98|LABEL_DEPLOY_STR|(180,45)|pending STR allocation display|
|D4|BUTTON_STRUP|(231,52)|increment control|
|254|BUTTON_STRDOWN|(214,52)|decrement control|
|EC|BUTTON_OK|(144,238)|control whose state follows1B9|
|F0|LABEL_ST|(136,205)|remaining points display|
|BC|LABEL_ATK|(175,165)|getter or getter plus pending contribution|
Hex offsets. Binder584150..58573D joins UTF16 names/AA1750/typed stores. Missing or wrong-type controls can be null.

[MEASURED] 2. Entry, NOT_WIRE local control state:
- ctor583120 installs vtableF29488, initializes handler22C..250 tozero. v28=583750 handles controls, v2C=5839E0 refreshes, v30=583BE0 handles string notices. Startup585740 calls reset57D410 at585843 and explicitly zeros1B9 at585947, conditional on reaching those points; don't infer a live instance.
- 58395D..5839BF compares the event's control pointer with D4/D8/DC/E0/E4 and its token with the current value at1090DA0. Matching routes call57C190 at583976/993. The event token is not a measured universal number.
- 57C190 requires local player1032EC4. It sets1B9=1 at57C1A9 BEFORE testing the supplied control and subsequent widget gates. Thus setting the flag is not evidence that allocation completed. With valid STR control and the reviewed widget path,57C25E increments1C8, updates LABEL_DEPLOY_STR, and57C282/288 increment22C/230. The later ST budget check57C8F3/FC follows those mutations; ST0 is not an allocation-budget guarantee. ST decrements at57C902 only when reached.
- The five DOWN controls are registered with57D760 via57A090 (e.g.5855B8/C1). Registration stores owner and method in a callback object;634980 invokes that method with owner and event control. The decrement helper57CE00 rejects a null/zero pending display, then decrements the supplied pending count and first derived accumulator. Do not infer perfect undo of every accumulator from this one helper.

[MEASURED] 3. Display consequence, bounded to refresh57E1D0..57F42A:
- Five primary labels use direct getter calls57E6C8/6EB/70E/731/754, after the independent point/additional-attribute displays and before the next1B9 gate. LABEL_STR is not replaced by the pending STR count in this refresh path.
-1B9!=0 at57E78F routes MC/AC/MATK/ATK through pending contributions. Additional groups are PPT/PAP/MPT/MAP (57E969) and AR/MR (57EDC9). All ten IDs/positions pinned; other paths not excluded.
- ATK example:57E926 calls467E90;57E92B reads signed handler22C,57E933 reads float global1022614,57E950 multiplies,57E954 adds,57E958 truncates,57E95C stores widget220. Getter and pending integers convert to float32 then double before arithmetic; coefficient is read as float32. The pinned IMAGE coefficient is1.0, not a measurement of runtime global state.
- [PROPOSED] D arithmetic control: getter100,pendingSTR1,coefficient1.0 gives ATK101 in preview,100 with flagzero; FightAttr getter can be unchanged. No client ran for this example.

[MEASURED] 4. Clear boundaries:
-57D410 zeros1C8..1D8, clears pending widgets conditionally, and sets1B9=0 at57D752. It does not itself zero22C..250; don't substitute it for every complete cleanup sequence.
- Notice ResetDeployPoint (UTF16F29600) calls57D410 then explicitly zeros all ten DWORDs22C..250 (583C38..6E). Deploy_OK (F2958C) sets1B9zero, calls57D410, then57BE00 on22C clears the same ten DWORDs. String equality is imported MSVCP90 wide-string operator== atIATC3B2D0. These are consumer-side notices, not newly identified network acknowledgments.
- In57D760, after the accepted path increments LABEL_ST, equality with localplayer.ActorAttr+80 at57DD87/8D clears1B9 at57DD95. This relies on the current point display and ActorAttr value; no blanket assertion that every DOWN click resets mode.
field_key: CharInfoEventHandler@0x1B9.1#W and#R = local preview control, NOT_WIRE in these paths. ActorAttr and FightAttr offsets remain separate classes.

[PROPOSED] D — measurement protocol
BUILD_PROPOSED: Add stat-allocation controls to GT-272's observation preconditions: begin from initialized clean panel state, avoid pending allocation while measuring equipment, record LABEL_STR, LABEL_DEPLOY_STR, LABEL_ST and LABEL_ATK before/after alongside the actual stat inputs; when instrumented record1B9 and22C | GT-272 equipment owner / LANE-B, LANE-K to bind | frame/input evidence + exact widget observations with preview state, not ATK-only success
BUILD_IMPACT: This closes a measurement ambiguity for B1(c); it does not provide original-server item bonuses. Existing B1e synthetic CBuff trial remains composition D and must not be called authentic equipment stats.
nonclaims: No native/client/server execution, measured UI event/token, pixels, all1B9 writers, original stat-allocation/equip policy, network Deploy_OK carrier, acceptance/rollback, persistence/reconnect or runtime promotion. No queue/lease/ServerProject/reference/asset/Git mutation.

Evidence: IMAGE14759424bytes SHA9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623. Exact VA/file offset/end/SHA inventory staged/standing_b1m_manifest.json.
plus: VA0057C190..0057C9E2, file17B590, 2130bytes, SHAd87a066697159887b997a06a2389d320e28c282c2e5851aa5b593cfacc8dfc74.
reset: VA0057D410..0057D75E, file17C810, 846bytes, SHA81f0af26327ea530e1641f606d8341f8bb7b586f3a675d6443d1e3fe879447c0.
CharInfo.refresh: VA0057E1D0..0057F42A, file17D5D0, 4698bytes, SHA6bae71588474ad51e16c555a359c0caf16fd5889db915f6e26da982a33eba3f2.
Manifest SHA3d4ba65ce7a3387002fb39db5e1f0f53c7670a608b840f209e9c826b863caa18; verifier standing_b1m_verify.py SHAb2aac1af9582ded58c88fc71d5026bbebb8231e0f3e29dfeda3339d653ca1940; log SHAca0f9fbe46f8e4ea99d560979adf173447651666f3b46c4437703f4e31873f13. PASS56spans/18code ranges/5854instructions/8sources/484calls/524pins/55independent anchors/32UI bindings/5direct primary calls/4vslots/1import/3arithmetic controls. Inputs checked before/after; STATIC ONLY.
ADVERSARY: a6f_review found no material defect; verifier exit0. Added evidence markers and qualified the late ST budget check. Deploy_OK producer remains unclaimed.
SCOREBOARD: NONE | Standing B1 IMAGE evidence | no runtime promotion
