# PF GM plug-in gate — bounded IMAGE + DATA checkpoint

## คำตอบสั้น

- **[ORIGINAL EVIDENCE: IMAGE]** เมื่อ fallback allocation 4 ไบต์สำเร็จ `application+0x7C8` เป็น object ที่ไม่ใช่ NULL และผ่าน pointer gate ของปุ่มได้; ถ้า allocation ล้มเหลว loader เก็บ NULL (`GM-IMG-002`).
- **[ORIGINAL EVIDENCE: IMAGE]** เมื่อคลิก client เรียก vtable slot `+0x04`; fallback slot นี้คืน `NULL` แล้ว dispatcher หยุดก่อนสร้างหน้าต่าง (`GM-IMG-003`, `GM-IMG-006`, `GM-IMG-007`).
- **[ORIGINAL EVIDENCE: IMAGE]** direct executable-section census ปิด 15 member refs (read 10 / write 5) และ pinned direct routes มี call slot `+0x00` 1 จุดกับ `+0x04` 4 จุด. **[MANUAL_HASH_ANCHORED]** การจำแนกบริบทของ slices ที่ pin ไว้พบ copied-alias store/return 0 จุด; นี่ไม่ใช่ symbolic dataflow proof และขอบเขต split-address/pointer arithmetic กับ alias ภายใน external callee ยังเปิด (`GM-IMG-011`, `GM-IMG-015`).
- **[ORIGINAL EVIDENCE: IMAGE]** direct slot `+0x04` return slicesครบ 4 จุด: ส่งเป็น dispatcher argument 2 จุด, empty-predicate argument 1 จุด และ inline UTF-16 compare 1 จุด; immediate alias store/return/deallocator เป็น 0/0/0. การจำแนก consumer เป็น **[MANUAL_HASH_ANCHORED]** และไม่ปิด retention ภายใน downstream calleeหรือ original ownership (`GM-IMG-017`).
- **[ORIGINAL EVIDENCE: IMAGE]** fallback vtable มี cell ที่ `+0x08`: รับ stack-passed destination pointer ของ MSVCP90 `std::basic_string<wchar_t>` (อาจเป็น hidden sret), default-construct เป็นสตริงว่าง, คืน pointer เดิม และ `ret 4`; pointer เป้าหมายมีเพียง cell นี้, ไม่มี direct `E8/E9` rel32 branch และ direct `application+0x7C8` routes ที่ pin ไว้ไม่เรียกช่องนี้. หลัง 12-byte cell region ที่ `+0x0C` เป็น UTF-16 `%s%s` ซึ่งมี exact raw PUSH-imm32 patterns 33 จุด จึงปิด concrete byte adjacency แต่ไม่อ้าง instruction execution, source-level vtable length หรือว่า DLL เดิมไม่มี private method อื่น (`GM-IMG-014`, `GM-IMG-016`).
- **[ORIGINAL EVIDENCE: IMAGE]** resolver ใช้ค่าคืน slot `+0x04` เป็น **GUI model basename** เพื่อประกอบ `.\Data\GUI\Model\<key>.model`; literal `GMUI_BASIC` ที่ EXE อ้างตรงเพียงจุดเดียวถูกใช้เป็น child/tab lookupหลัง panel ถูกสร้างแล้ว แต่ข้อเท็จจริงนี้ไม่บอกค่าคืนของ DLL เดิม (`GM-IMG-009`, `GM-IMG-013`).
- **[ORIGINAL EVIDENCE: DATA]** `GMUI.project` ประกาศ model `GMUI_1`; `GMUI_1.model` มี root `GMUI_1` และ child `GMUI_BASIC` (`GM-DATA-001`, `GM-DATA-002`).
- **[RECONSTRUCTED POLICY — PROPOSED, NOT EXECUTED]** candidate สำหรับ compatibility กับ DATA ที่มีอยู่คือ slot `+0x04` คืน pointer ไปยัง writable process-lifetime UTF-16 buffer ที่บรรจุ `GMUI_1`; corpus ไม่มี `GMUI_BASIC.model`. นี่ไม่ห้ามว่า DLL เดิมอาจเคยคืนข้อความอื่นหรือแม้แต่ `GMUI_BASIC` ผ่านกลไกที่ไม่มีอยู่ในหลักฐานปัจจุบัน และยังไม่อ้างว่าเคยเห็นค่าคืน, constness, mutability หรือ lifetime ของ DLL เดิม.

**[UNPINNED OPERATIONAL INVENTORY — NOT IMAGE/DATA EVIDENCE]** ใบสั่งงานระบุว่า inventory ปัจจุบันไม่พบ `GameMaster.dll`; generator นี้ไม่ได้ enumerate หรือ hash inventory ดังกล่าว จึงอาจ stale และต้องตรวจซ้ำใน runtime lane. หาก inventory นั้นยังจริง อาการ “เห็นปุ่มแต่คลิกไม่เปิด” จึงเพียงสอดคล้องกับเส้น fallback ที่ allocation สำเร็จ; artifact นี้ไม่ยก inventory หรือ screen observation เป็น IMAGE/DATA fact.

## คำแก้จาก checkpoint ก่อน

- **ถอน:** `GMUI_BASIC` ใน artifact รุ่นก่อนเคยถูกเสนอจาก literal xref เป็น candidate น้ำหนักสูงของค่าคืน slot `+0x04`; xref นั้นพิสูจน์เพียง child/tab lookup จึงไม่ใช่หลักฐานของค่าคืน DLL.
- **แก้:** `GMUI_BASIC` คือ ID ของ tab/control ภายใน panel. DATA ปัจจุบันผูก panel นี้กับ model `GMUI_1` และไม่มี `GMUI_BASIC.model`; `GMUI_1` จึงเป็น compatible proposal ไม่ใช่ measured original return.
- **เพิ่ม:** direct executable-section member-reference census, direct producer/consumer closure, direct slot `+0x04` return-lifetime slices, ABI ของ slot `+0x00` และ fallback slot `+0x08`, byte boundary หลัง slot `+0x08`, GUI-model resolver และ recursive DATA model census 534 ไฟล์/0 subdirectory.

## สัญญา ABI ที่ IMAGE บังคับเท่าที่พิสูจน์แล้ว

| ขอบเขต | ข้อเท็จจริง |
|---|---|
| loader | `LoadLibraryW(L"GameMaster.dll")` → `GetProcAddress("CreateGameMaster")` → เรียก export แบบไม่มี argument ชัดแจ้ง → เก็บ pointer ที่ `application+0x7C8` |
| directly proven slots | pinned direct routes มี slot `+0x00` 1 จุดและ slot `+0x04` 4 จุด; manual contextual reading ของ direct 15-reference set พบ copied-alias store/return 0 จุด แต่ split-address/external-alias ยังไม่ปิด |
| slot `+0x00` | `ECX=this`, stack output pointers 2 ตัว, callee `ret 8`, EAX คืน pointer แรก; fallback เขียน dword แรกเป็น `-1` และ init subobject `+4`; semantic ของ outputs ยัง UNKNOWN |
| slot `+0x04` | `ECX=this`, ไม่มี explicit argument, plain `ret`, EAX เป็น pointer ไปยังข้อความ UTF-16 แบบ NUL-terminatedที่ direct callers อ่านทันที; IMAGE ไม่พิสูจน์ constness, mutability หรือ lifetime. Direct caller slicesไม่ store/return/free ค่านี้และ factoryเรียก getterซ้ำสำหรับ empty-checkกับ exact compare แต่ downstream retention/original ownershipยังเปิด |
| fallback slot `+0x08` | stack destination pointer 1 ตัว (explicit หรือ hidden sret ยังแยกไม่ได้), `ret 4`; default-construct MSVCP90 `std::basic_string<wchar_t>` แล้วคืน pointer เดิม; direct pinned routes ไม่เรียกช่องนี้; หลัง 12-byte region เริ่ม referenced UTF-16 `%s%s` และ raw PUSH pattern census=33, แต่ execution/split-address/external-alias reachability ยังเปิด |
| เงื่อนไขผ่าน dispatcher | pointer ต้องไม่เป็น NULL และข้อความต้องไม่ว่าง |
| เงื่อนไขผ่าน GM factory | GUI model basename จาก slot `+0x04` ต้องเท่ากับ requested key แบบ UTF-16 exact comparison |
| compatible DATA binding — PROPOSED | คืน pointer ไปยัง writable process-lifetime UTF-16 buffer ที่บรรจุ `GMUI_1` → resolver โหลด `Data\GUI\Model\GMUI_1.model` → panel ภายในมี `GMUI_BASIC`; ไม่ใช่ค่าดั้งเดิมหรือ lifetime ที่วัดแล้ว |
| object ที่ factory สร้าง | ขนาด `0xEC`, constructor `0x0059D740`, vtable `0x00F46258` |
| cleanup | application ใช้ imported `MSVCR90 operator delete(void*)` กับ pointer โดยตรง แล้ว `FreeLibrary`; ไม่มี virtual-destructor call ในช่วงที่พิสูจน์ |

## สัญญาส่งต่อสำหรับทีม — ยังไม่ใช่ผล runtime

- **[ORIGINAL EVIDENCE: IMAGE]** client ใช้ `GetProcAddress` ด้วย ASCII `CreateGameMaster` แบบ exact. **[RECONSTRUCTED POLICY — PROPOSED]** DLL ต้องเป็น 32-bit และควรบังคับ export table ด้วยไฟล์ `.def` ให้มีชื่อ `CreateGameMaster` ตรงตัว ไม่ใช่ `_CreateGameMaster` หรือ `CreateGameMaster@0`.
- **[RECONSTRUCTED POLICY — PROPOSED]** object ที่ factory คืนต้องจัดสรรด้วย allocator ที่เข้ากันได้กับ imported `MSVCR90.dll` scalar delete ของ client. ทางที่แคบและปลอดภัยที่สุดคือ build x86 ด้วย Visual Studio 2008 `/MD` หรือเรียก imported MSVCR90 `operator new` (`??2@YAPAXI@Z`) โดยตรง; ห้ามสมมติว่า `new` จาก modern UCRT/default heap ใช้ข้ามมาลบด้วย MSVCR90 ได้. จึงห้ามคืน static/global objectด้วย.
- **[RECONSTRUCTED POLICY — PROPOSED]** สอง slot ที่ direct routes บังคับคือ `+0x00` และ `+0x04`: slot `+0x00` ใช้ fallback behavior ที่พิสูจน์แล้วได้; slot `+0x04` ควรคืน pointer ไปยัง writable process-lifetime UTF-16 buffer ที่บรรจุ `GMUI_1`. นี่เป็น hardened policy เพราะ IMAGE ปิดเพียง immediate reads และยังไม่ปิด downstream mutability/retention; ไม่ใช่หลักฐานว่า DLL เดิมคืน literal หรือใช้ lifetime แบบใด. เพื่อ harden ต่อ split-address/external-alias route ที่ยังไม่ปิด ควรมี three-cell fallback-compatible prefix รวม `+0x08` และทำ exact fallback behavior ด้วย แต่ห้ามอ้างว่าช่องนี้จำเป็นต่อการเปิดหน้าต่างหรือว่า DLL เดิมไม่มี private method เพิ่ม.
- **[RECONSTRUCTED POLICY — PROPOSED]** object ไม่ควรพึ่ง destructor เพื่อ cleanup เพราะ application ไม่เรียก virtual destructor/release ก่อน delete.
- **[CLIENT-OBSERVED RESULT REQUIRED]** acceptance ยังต้องเห็นปุ่ม → คลิก → หน้าต่าง `GMUI_1` เปิดและเข้าถึง tab `GMUI_BASIC` ได้ รวมทั้งปิดเกม/cleanup โดยไม่ crash ใน runtime ที่ทีมได้รับอนุญาต.
- **[RECONSTRUCTED POLICY — PROPOSED]** ห้าม patch `0x009F17E0` โดยตรง เพราะตารางนี้พิสูจน์เพียงว่าเป็น fallback getter ของ vtable นี้ ไม่ได้พิสูจน์ว่า function body เป็น private ต่อ GM.

## ขอบเขตที่ยังเปิด

- ไม่รู้ implementation/source ของ DLL เดิม และไม่เห็นค่าคืน runtime เดิม.
- output objects ของ slot `+0x00` ยังไม่มี semantic name; compatible fallback behavior ปิด ABI ได้แต่ไม่ขยายความหมาย.
- semantic name และ split-address/external-alias reachability ของ fallback slot `+0x08` ยัง UNKNOWN แม้ ABI/body และ concrete three-cell-region/string adjacency จะปิดแล้ว.
- direct member-reference census มี 15 direct refs; no-alias เป็น manual hash-anchored contextual reading ไม่ใช่ symbolic proof และยังไม่ปิด pointer-arithmetic/split-address. runtime clean-shutdown test เป็น guard สำหรับ ABI surface ที่อาจยังไม่เห็น.
- direct slot `+0x04` return-use census ปิดเฉพาะ immediate caller slices; ไม่ใช่ symbolic proof ว่า dispatcher/lookup/factory calleeไม่ retain/transform pointer.
- ยังไม่พิสูจน์ runtime window creation หรือ clean shutdown; artifact นี้เป็น implementation contract สำหรับทีม ไม่ใช่คำกล่าวว่าสำเร็จบนจอแล้ว.

## Provenance และ nonclaims

- ทุกแถวใน `PF_GM_PLUGIN_GATE.tsv` มี source เดียว: IMAGE 17 แถว / DATA 2 แถว; ไม่มีแถวใดผสมสองชั้น.
- ไม่ได้รัน GameClient, server, DLL, dump หรือ capture.
- ไม่ได้คัดลอก raw image bytes ลง output; รายงานเฉพาะ VA, file offset, โครงสร้าง, constant และ SHA-256.
- **[DELIVERY BLOCKER — OUTSIDE THIS GENERATOR'S AUTHORITY]** ไฟล์ local-only ชุดนี้รวม pair marker อาจยังไม่ repository-visible; การ allowlist/track/package เป็นคำตัดสินของ chief/owner และ generator นี้ไม่ตรวจหรือแก้ Git. นี่เป็น delivery blocker ไม่ใช่ IMAGE/DATA fact.
- ตารางมี 19 แถว, gate_id ไม่ซ้ำ 19/19, evidence_key ไม่ซ้ำ 19/19.
- Exact ordered gate-ID set ถูก pin เป็น `GM-IMG-001..017` ตามด้วย `GM-DATA-001..002`; pair marker `PF_GM_PLUGIN_GATE.pair.json` ผูก SHA-256 ของ TSV/MD กับ row/source counts และถูก publish เป็นไฟล์สุดท้าย.
- Generator PASS scope: `pinned_image_data_spans_direct_slot4_return_slices_exact_gate_id_set_atomic_pair_integrity;manual_context_is_hash_anchored_not_symbolic_dataflow`. ตัวตรวจผูก structured census กับค่าทั้งใน TSV/MD และรัน mutation guards; semantic class ของ guard/delete/write-role/no-alias/slot4-return-consumer ยังคงเป็น manual hash-anchored interpretation ไม่ใช่ symbolic dataflow.
- TSV SHA-256: `a5f3fdeb6a830b06e3eb9dceff85fc762459ca3e4f9e7ada152937ef1c898509`
- IMAGE SHA-256: `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`
- `GMUI.project` SHA-256: `392f17ba4aba1342ed1e0ec8133e1f2f074b94081fa1ee41bf718021746c0632`
- `GMUI_1.model` SHA-256: `ffd7e5d1c44ffe36b5bacc2857aa049ae6cbea69e11f62541bd0632162bbc69f`

## Evidence keys

- `GM-DATA-001`: `b8f7e81876dbde3085e0a6605312e4b93dec6b41270785a014079bc32f61a734`
- `GM-DATA-002`: `143ffd702668e79d983fc1bfe26a970d56cbecea44c168c24e11750440ac5dfe`
- `GM-IMG-001`: `54b20420b6bb3451ad02aadaeede46c362d2044ef52f38f1e5702d309160839c`
- `GM-IMG-002`: `6a9db33f3670aa555d047bb52fc48027b6dbe6887bfff3aaab1c55cf20921100`
- `GM-IMG-003`: `fc6027136ed157ec2c348a42947c5aca3430d79011649ae4f68798d8244daa39`
- `GM-IMG-004`: `7b96f2b5e29400dd00d17eeaed07ada580288f30ec547c5727ba862a86c3dcb5`
- `GM-IMG-005`: `ac28f4951bc179f5ce87755a46069b0b6066653e004338b8419f126ee8564326`
- `GM-IMG-006`: `5b7b6a6379bbbddfa0edbb2fd0a651a81d031f0e586b65fe741b27fbde2bdd01`
- `GM-IMG-007`: `d21092f9703112f7c4c3a20a6c262df0a996bec8beaf7dd871bd30db2b2affe9`
- `GM-IMG-008`: `676e6d0d05509e31a103dc240c64bce373e50b723f88db740ca2fba162c7b22c`
- `GM-IMG-009`: `33a61fa8475653bc9e38b2a8262214e2ad1d741ac9d8a31ec5cbf1fd7062feac`
- `GM-IMG-010`: `e6ba821d230acbfdd0e2e7bdd610068cf1089355ae62579c0dae69847f2d5ea8`
- `GM-IMG-011`: `6c5f592e5b6836748b445cb117b539cd426f3f88a4a14cdd1af6a34f2ce21ad3`
- `GM-IMG-012`: `6a7981610716270aca8ab01f0ffbbd880304481d474d904338ac2dac816e184f`
- `GM-IMG-013`: `492ee1b1cf41b2bef326d875ada6c1920a4c22fb170b9e17f18fe10f906aeb52`
- `GM-IMG-014`: `2b322cea6085ca76e8e586d18ff088b2eb045c099be9df0ec1b37a5f2c008e25`
- `GM-IMG-015`: `e49ddc4c2d8952df3bdd18b454febf413964dc9974983025425387cf1c8cc162`
- `GM-IMG-016`: `45dd7e8fe68a70dbcf673f8de666c7a73f882a9e71a7a3a8ef684e4068ed95be`
- `GM-IMG-017`: `01a79a9139cbd0791f147c7dd99512eead4af9d716ee0ba2a3fcb7bdcf5e3add`
