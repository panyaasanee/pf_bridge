งานเป้าหมายยืน — ยังไม่มีเลขใบ ขอให้ LANE-K ตั้งเลขและผูกจดหมายนี้
B3a · ปิด 2026-09-09T10:49:30.103839+07:00 · Unequip op6, conditional swap order, and correction of historical quantity labels · IMAGE · PARTIAL
ADDRESSEE: LANE-K · cc LANE-DB, LANE-CS, chief
BUILD_PROPOSED: ถอดและสลับอุปกรณ์ตาม identity + logical mask ที่ไคลเอนต์ส่ง | LANE-DB + LANE-CS | proof: เจ้าของยืนยันคลิกขวาถอดและสลับของสองชิ้น พร้อมลำดับคำขอ/คำตอบจริง, bag ก่อน–หลัง และ relog ที่ไม่เพิ่มหรือทำของหาย; LANE-K ผูกเลขทดสอบ
BUILD_IMPACT: op6 ในเส้นทางนี้ใช้ตัวตนไอเทม ไม่ใช่จำนวน; การสลับสร้างหลาย operation จึงต้องกำหนดการยอมรับ/ปฏิเสธและ persistence ของทั้งชุดอย่างชัดเจนก่อนโปรโมต.

[MEASURED A / IMAGE] Request contract
field_key: ItemOperateVitalReq@0x14.1#W (op); @0x18.4#W (value); @0x20.8#W (identity).
59F870..59F8AE constructs operation6: byte+14=6, DWORD+18=third argument, qword+20/+24=first/second arguments. All four rederived direct caller candidates load the qword from ItemAttr+28/+2C and value from source-widget+94. No destination-bag storage key is supplied at these call sites. This establishes the represented fields, not the original server's placement policy.
59F800..59F868 constructs operation5 with the same field layout. Its mask handling is additional: bit8 forces value8; otherwise bit4000 selects8 or10 according to key10 state. Do not pass every caller mask through unchanged.
Pool59F0D0 fresh59F134/reuse59F1B2 both call ctor5E5AA0: vtF30374, versionbyte10=0, mergeflagbyte11=0. vt+18=5E5AF0 codec writes op byte tag0B/1, value tag14/4, identity tag32/8, in that order; corresponding read arm exists. These are16 body bytes including3tags, excluding nested ID/version and every outer framing layer. This is not a captured/send-ready packet.

[MEASURED A / IMAGE] Right click produces op6
C1B2C0 constructs UTF16 UIEvent_MouseClick@F8CF88 into1090DA4; name ctor4D2D20 stores hash+1C, hence1090DC0. AA3A90's release messages202/205/208 enterAA3F5C. A9DDA0 maps right-button family204–206→2. AA3F7E computes family, AA3F94 retains it inEDI; accepted click gates emit context {coordinates,button-family@+8} using event1090DA4 atAA404D/AA4056/AA406D.
CharInfo vtF29488.v28=583750 reads hash1090DC0 and its general mouse-click arm583910 calls582730. The handler requires compatible item-widget type, the incoming widget+94 key to exist in regular-equipment map+170, and a resolved ItemAttr with template+30>0. It reads context+8 at58284B; value2 reaches58294D→59F870. Source-widget+94 and ItemAttr+28/+2C become mask and identity. Value1 takes the distinct SHIFT/CTRL branches. This is a gated static right-click route, not an observed native click or proof of every panel path.
5A0120 looks up by ItemAttr+28/+2C and copies via5C1530. The drag lookup5A1630 instead scans configured equipment storage range [1080B74,1080B70), tests mask & (1 << ItemAttr+39), then copies via5C1530. It is an equipment lookup, not a numeric dialog.

[MEASURED A / IMAGE] Dragging between equipment slots
57CF50's source-parent+94==16hex arm reads local copies A from source mask and B from destination mask via5A1630. It requires A.template>0, A.identity signed-positive, and both masks nonzero. After the local gate57BE80 and normalization57CB30, the call order is:
1. 57D1F4 → op6(A.identity, ORIGINAL source mask).
2. 57D220 → op5(A.identity, normalized destination mask; op5 helper may further transform it).
3. Only if B.template>0 and B.identity signed-positive: 57D277 → op5(B.identity, normalized source mask; same helper rules).
The two source/destination local copies are made before these requests. No separate op6 for B is visible in this specific branch; this is not a whole-client negative or proof that an original server swaps atomically.
57BE80 rejects A only when item field n_EQUIPTYPE@F0BE04==4 and destination is not10/40000/100000. Separately, 57CB30 reads n_EQUIPSLOT@F0EC7C==18hex and rewrites10→8,40000→20000,100000→80000. Keep these two field names distinct; no class/job or numeric storage-slot inference.

[MEASURED A / IMAGE] Other two callers and old-label correction
5A2A70..5A3B8B: parent+94 comes from the source widget (5A2B06), and ordinary-drag mode10907B9==0 selects the branch whose parent ID is16hex. 5A34E2→5A1630, then5A3532→op6(copied identity, source mask). Its peculiar guard excludes negative identities but permits zero/default identity; do not silently rewrite this as a positive-only guard.
5B9F70..5BAA5E: source-parent+94==16hex, copied template>0 and signed-positive identity lead5BA208→op6 with the same field provenance. The destination panel's live binding is not established here.
Archive R76/R77 and archived GT015 prose called these inputs quantity/item-handle, parent16 a verb, and5A1630 a dialog. The rederived producer/lookup chain supersedes those labels for these sites. R77 had already corrected the EH trylevel12 mistaken for a dialog resource; it had not corrected the lookup/identity interpretation. Also the dispatcher ends5A3B8B, not5A40B0. Raw E8 scan yielded these four candidates; it is not an exhaustive closure of indirect/dynamic producers.

[MEASURED A / IMAGE] Conditional insertion order, not atomicity
59F800/870→singleton4011A0→5DD800. Enqueue requires+D0; +D4!=0 adds typefilter5DC540 and may flush. For +D0=1,+D4=0 and the same pending container with no intervening flush/reentrancy, these ctor-zero mergeflag requests pass5F3D60→5F3A80: incoming+11==0 skips same-type replacement. 5F3B73..98 inserts at the list tail (node6B3440/ref69D040); writer5F38F0 starts at sentinel.next and follows next, so these requests retain insertion order. A blanket rule “same vital ID replaces previous request” would lose swap operations here.
The flush5DD790 separately creates an outer wrapper, attaches pending container+150 into wrapper+18 and clears+150; A8D500 is called only if receiver+148 exists (B2b exact closure). Allocation failure, scheduling/interleaving, transport framing, original server acceptance/rollback and reply grouping remain unproven. Do not infer one transport frame or all-or-nothing behavior from three call sites.

Evidence: staged/standing_b3a_manifest.json SHA16a2803ca4f37b7547341a0886e399b6047ba38c93a5fa2b4f8cd4a688dd4940; each span has start/end-exclusive VA, file offset and SHA. IMAGE14759424 bytes SHA9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623. Python -B staged/standing_b3a_verify.py PASS43 spans/34 code ranges/4285 instructions/7 inputs/49 calls/124 pins/6 vslots/247 message selectors/9 button selectors/3 typed writes/3 strings; source hashes before/after. Search matched FILES external0/gamedata0/reference0/archive5/consumed1; query/paths in search.log, remaining hits are historical bookkeeping. Read V141_FREEZE this round.
Adversary: actual frozen review; corrected key-presence versus widget-membership wording and common-caller argument order. Other bounded claims survived review; verifier exit0. Open: recovery if op6 succeeds but a later op5 fails.
nonclaims: no original wire/native run, accepted server operation, bag destination, persistence/relog, one-frame/atomic swap, dynamic producer census or job semantics. Server policy and test composition are proposed D, not original behavior. No queue/reference/ServerProject/DB/Git/lease edits.
SCOREBOARD: NONE | Standing B3 IMAGE evidence | no runtime promotion
