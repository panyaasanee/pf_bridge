# STANDING A4 RESULT — M011 descriptor and packaged animation assets

**ADDRESSEE:** Chief / LANE-B combat runtime owner  
**DATE:** 2026-09-09 14:33 +07:00  
**LANE:** static read-only Binary + shipped asset inspection; no client/server run

## Result

ผล A4 รอบ `20260909_1421` ระบุว่า Tornado Eagle row 31 ใช้ model class `M011`, outfit `M011_000_000_SP3` และ BEHAVIOR 3220/3221/3226/3231/3233 เรียก `_F_SENTRY_000`, `_F_FLEX_000`, `_F_ATTACK_000..003`. รอบนี้ปิดช่อง **packaged resource existence** ของชื่อทั้งหก:

- descriptor ที่มากับ client จริงคือ `GameClient/Data/GC/V/m011_000_000_sp3.av_`, packed size 882, SHA-256 `ea513a03c8e0d26b88a779f8b6cfaec24dddc357b2f5b40baeddf427187c8782`;
- ถอด `$pcz`/raw-LZMA ในหน่วยความจำได้ XML `AvatarData` size 9,696, SHA-256 `2bea12aee12d8aceebdbff3919f6c9dba95dc0b943130f21270a201807144e7c`;
- descriptor มี NIF เดียว `./Data/GC/M/M011_000.nif`, มี Action 15 รายการ และมี KfFile ที่ตรงกับชื่อ A4 ทั้งหกทุกตัว;
- packed `.k_` ทั้งหกมีอยู่จริง ถอด `$pcz` ได้ครบ และ decoded payload ทุกตัวเริ่มด้วย `Gamebryo File Format, Version 30.1.0.2`.

## Exact crosswalk and hashes

| BEHAVIOR token | descriptor KfFile | shipped packed file | packed size / SHA-256 | decoded size / SHA-256 |
|---|---|---|---|---|
| `_F_SENTRY_000` | `.\\Data\\GC\\A\\M011_F_SENTRY_000.kf` | `m011_f_sentry_000.k_` | 15,832 / `c85ca81cb6d7d2c107faf97e771b81565446b483552da2b02f87dc6c77c2e7e2` | 33,979 / `bcf6eb5beea1bd3f60d08d092a8d235dfed277348bb3d05f578f8f8115d535be` |
| `_F_FLEX_000` | `.\\Data\\GC\\A\\M011_F_FLEX_000.kf` | `m011_f_flex_000.k_` | 55,958 / `9fd52e1bb4381067ad6ef5df9e52b9b1e5e8841ecae08e9fb211f8703a92db31` | 108,657 / `edcfc151fce7f35234d3386d4f158d72a83fd7a62b7201786e54607519847ec0` |
| `_F_ATTACK_000` | `.\\Data\\GC\\A\\M011_F_ATTACK_000.kf` | `m011_f_attack_000.k_` | 28,054 / `8a6f8c1e169f55244572b68752f3d328d3d8fd02a668606bdea3a7bb3f270107` | 54,014 / `7134b3a28eaa86fdc158998657a6b05a3f0ff53ad09e97eadef3ad655ca156eb` |
| `_F_ATTACK_001` | `.\\Data\\GC\\A\\M011_F_ATTACK_001.kf` | `m011_f_attack_001.k_` | 30,113 / `aed4f335177dee743d9296093a1222278d15dc416aebb4423f620482ae2883b9` | 54,522 / `ace6468ebffef25eb0d939ea4b180f0fcea0e04d58cbb431ff7d6d89c815b7bc` |
| `_F_ATTACK_002` | `.\\Data\\GC\\A\\M011_F_ATTACK_002.kf` | `m011_f_attack_002.k_` | 16,171 / `044934226722f365f353429ca6abfdb581da000163ef0d69620c3467d3683e85` | 32,346 / `91df811f595cbe42dd5ba110a52ecc4e27f332eeb4e405453536ca487d95d005` |
| `_F_ATTACK_003` | `.\\Data\\GC\\A\\M011_F_ATTACK_003.kf` | `m011_f_attack_003.k_` | 37,239 / `4ac4efd391daf57a9137754403822be6af0829c62e0413f20a8762e4089e5714` | 65,106 / `f8e0718aeaffd5c734972de1321322d6a5e16702410fed28aa9267e9e412cbf8` |

ชื่อไฟล์บน disk ใช้ lower-case และเปลี่ยน `.kf` เป็น packed suffix `.k_`; ตารางนี้พิสูจน์การจับคู่ด้วย basename ที่ตรงกันและ content ที่ถอดได้ ไม่ได้อ้างว่าการเปลี่ยน suffix นี้เป็น logic ของ original server.

## Fixed-image parser/resolver pins

Image: `GameClient.local.bin`, size 14,759,424, SHA-256 `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`.

| role | VA span | file span | SHA-256 |
|---|---|---|---|
| Avatar Action parser reads `KfFile` | `0x008835B0..0x008836C5` | `0x004829B0..0x00482AC5` | `79f13de975da32c3ddc887872ebd902b585fe02bcb181a2972bf519b55d87f3f` |
| Kf resolver/cache | `0x008829B0..0x00882B71` | `0x00481DB0..0x00481F71` | `ac19d0de20dc509091b6199779ab486be96f68a22fcb5a5d7b3898d304143d43` |
| action record construction | `0x00888150..0x0088821C` | `0x00487550..0x0048761C` | `2083af25e5f8659aea78e7e44caa9dbeeae5fd53092ecc02d5b31b787a43bb7f` |
| Avatar PartList/ActionList orchestrator | `0x00883AC0..0x00883E6D` | `0x00482EC0..0x0048326D` | `6523971ef7317b96a59f14d92515984ed4a9552684c1a432cbfdcf6626561ba9` |

หลักฐาน IMAGE เดิมและ re-pin รอบนี้ยืนยันว่า parser อ่าน KfFile แล้วส่งเข้า resolver/cache เพื่อสร้าง action record. เมื่อประกอบกับ descriptor เฉพาะ `M011_000_000_SP3` และไฟล์แพ็กจริง จึงไม่มี packaged-file-missing blocker สำหรับหกชื่อใน A4.

## Evidence grade and nonclaims

- **A — exact shipped data/static producer:** descriptor XML, KfFile inventory, packed/decoded hashes, Gamebryo headers และ binary parser/resolver spans ข้างต้น.
- **D — compositional bridge only:** การประกอบ BEHAVIOR token จากผล `20260909_1421` กับ suffix ที่ตรงใน descriptor ทำให้แต่ละ token มี resource candidate แบบ exact และตรวจซ้ำได้.
- **ไม่อ้าง** ว่า client เลือก outfit/action นี้สำเร็จใน runtime, โหลด file handle สำเร็จ, เล่น/เรนเดอร์ clip, ว่าความยาว clip เท่ากับ BEHAVIOR keyframe threshold, หรือว่า original server เลือก selector ใด.
- **ไม่อ้าง** ว่า `.kf -> .k_` เป็น server policy; `.k_` คือ packaged filename ที่ตรวจบน disk เท่านั้น.

## Verification

Stdlib-only verifier: `pf_bridge/staged/standing_a4_assets_verify.py`  
SHA-256: `fb7838af4860afbe37df0f501a758c1945f7df3d87a65c7d22bd562206dbba2b`

Log: `pf_bridge/staged/standing_a4_assets_verify.log`  
SHA-256: `32434e2493c17c85df5d3abbc01794521dcae2973fbf446145f2d8a079f9bfe8`

Result: `PASS image_spans=4 descriptor_actions=15 relevant_assets=6 known_answers=6 traps=2; static assets only; runtime load/render and selector policy unproven`

Verifier pins all source hashes before use, rechecks them after use, has six known-answer mappings, and rejects two altered/missing-crosswalk mutations.

## BUILD_PROPOSED

LANE-B may keep selector `3220` as the first attended Tornado Eagle attack candidate: its `_F_SENTRY_000` and `_F_ATTACK_000` resources are present, descriptor-linked and parseable. Acceptance still requires one runtime cycle correlating selector/performer/target with the visible clip, number event, resident/HUD HP decrease, then a second cycle. Stop/falsify the candidate if the actor callback rejects the token, resolver/cache reports failure, the wrong clip plays, or damage events do not correlate.
