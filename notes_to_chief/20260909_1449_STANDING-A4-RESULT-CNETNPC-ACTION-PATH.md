# STANDING A4 RESULT — concrete CNetNPC action path and map key

**ADDRESSEE:** Chief / LANE-B combat runtime owner  
**DATE:** 2026-09-09 14:49 +07:00  
**STATUS:** NEW STATIC PROGRESS; bounded conditional bridge  
**LANE:** fixed Binary + original decoded DATA + shipped assets; no client/server run

## Result

ผล `20260909_1421` หยุดที่คำว่า “owner virtual `+0x28`”. รอบนี้ resolve owner สำหรับ Tornado Eagle actor_type 4 ได้เป็น concrete `CNetNPC` และตามต่อถึง action map:

1. `CActorTask_PlayActionEvent::Start` `[0x00475170,0x0047528A)` เรียก actor virtual `+0x28`. ทางปกติที่ `0x00475263..0x00475283` push อาร์กิวเมนต์ตัวที่สี่เป็น `0`.
2. `CNetNPC` vtable `0x00F0DF58`, slot `+0x28 = 0x00442030`. Callback นี้ต้องมี animation string, `actor+0x70 & 0x40`, และ `actor+0x80 != NULL`; ถ้าไม่ผ่านจะคืนก่อน dispatch.
3. ก่อนประกอบ path ถ้า `actor+0x248` ไม่เป็น null callback เรียก `0x0064D580` เพื่อแก้ string ชั่วคราว. จากนั้น virtual `+0x64` ของ CNetNPC (`0x0045DA60`) ส่ง string หลังขั้นนี้เข้า builder `0x0078A1F0`.
4. Builder ใช้ literal root `.\\Data\\GC\\A\\` และ format `%s%s%s.kf`: **root + prefix + token + `.kf`**. ถ้า input มี `_F_FORWARD` และ flag อีกตัวเป็นจริง จะเปลี่ยนเป็น `_F_WALK_000`; token A4 ทั้งหกไม่มี `_F_FORWARD` จึงไม่เข้า exception นี้.
5. Prefix มาจาก `MOBS record+0xC0` เมื่อไม่ว่าง มิฉะนั้นใช้ `actor+0x338`. Loader `[0x004A3432,0x004A3464)` ผูก `s_PREDESCRIPT` เข้ากับ `MOBS+0xC0` โดยตรง. Original DATA row 31 (`0x0035E734..0x0035E8DC`, SHA-256 `880afb97823b4df4b5e001aea62896f3d8894cae0c2b9c336ab3bcf74f48eeee`) มี `s_ID_MODEL_CLASS=M011` แต่ `s_PREDESCRIPT` ว่าง จึงบังคับใช้ runtime fallback `actor+0x338`.
6. เพราะ PlayActionEvent ส่งอาร์กิวเมนต์ตัวที่สี่เป็นศูนย์ callback จึงเลือก `0x00883310 -> 0x00882CA0`. ตัว dispatch แปลง full path เป็น `wstring`, เปิด map ที่ model object `+0x30` ผ่าน `0x008811E0`, และคืน action-record payload.
7. ฝั่ง descriptor parser `0x008835B0` อ่าน `KfFile`, เรียก resolver `0x008829B0`; resolver ใช้ converter `0x00894AC0` และ map search `0x00A81600` ชุดเดียวกับ lookup จากข้อ 6 แล้วสร้าง record `0x00888150` และ insert ผ่าน `0x00881360`. จึงเป็น exact same-container/same-key path ไม่ใช่การจับชื่อด้วยข้อความรายงาน.

## What this closes

ถ้า post-modifier token ยังเป็น `_F_SENTRY_000`, `_F_FLEX_000`, หรือ `_F_ATTACK_000..003` และ fallback prefix `actor+0x338` เป็น `M011`, Binary จะประกอบ key ที่ตรง descriptor แบบ byte-for-name:

```text
.\Data\GC\A\M011_F_SENTRY_000.kf
.\Data\GC\A\M011_F_FLEX_000.kf
.\Data\GC\A\M011_F_ATTACK_000.kf
.\Data\GC\A\M011_F_ATTACK_001.kf
.\Data\GC\A\M011_F_ATTACK_002.kf
.\Data\GC\A\M011_F_ATTACK_003.kf
```

ผล `20260909_1433` พิสูจน์แยกไว้แล้วว่า descriptor `m011_000_000_sp3.av_` มี KfFile ทั้งหก exact และ packaged `.k_` ทั้งหกมีอยู่/ถอดได้. รอบนี้เพิ่มตัวประกอบ path และ same-map lookup ให้ครบ.

## Fixed-image provenance

Image `GameClient.local.bin`: size 14,759,424; SHA-256 `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`.

| role | VA span | file span | SHA-256 |
|---|---|---|---|
| PlayActionEvent Start | `0x00475170..0x0047528A` | `0x00074570..0x0007468A` | `34953c77c1a2dcc804d010f10405cc503540074784aaa062f17bcad990478f31` |
| CNetNPC animation callback | `0x00442030..0x00442207` | `0x00041430..0x00041607` | `960aee0ff7cea5046db33794845c99a42b4a53ba651b44ccb345e8905ce0d7a2` |
| `s_PREDESCRIPT -> MOBS+0xC0` | `0x004A3432..0x004A3464` | `0x000A2832..0x000A2864` | `34fd9466904f8df4578bbd712dfb2ccaaba41fc8a3390929ef3ad20f65049185` |
| CNetNPC path adapter | `0x0045DA60..0x0045DAD7` | `0x0005CE60..0x0005CED7` | `381b4c6cbb88bb0480cc649b891edff0789f13f63a37bd5c99ae4e61bc0b598d` |
| full-path builder | `0x0078A1F0..0x0078A2FD` | `0x003895F0..0x003896FD` | `35ac6d10213db241d1e5d1d7cd3e35620f1d23e162483bcb14a3c7db35df7683` |
| exact action-map lookup | `0x008811E0..0x008812CA` | `0x004805E0..0x004806CA` | `420d7731c9b4bee235b31e870611fcffe4602898ff996aa21e5f4b73b0221a27` |
| model action dispatch | `0x00882CA0..0x00883300` | `0x004820A0..0x00482700` | `c78201169c4a266b4e0e52406f53084697041e4db0e2f7218901394fdf5de7f8` |
| Kf resolver / map insert | `0x008829B0..0x00882B71` | `0x00481DB0..0x00481F71` | `ac19d0de20dc509091b6199779ab486be96f68a22fcb5a5d7b3898d304143d43` |
| Avatar Action parser | `0x008835B0..0x008836C5` | `0x004829B0..0x00482AC5` | `79f13de975da32c3ddc887872ebd902b585fe02bcb181a2972bf519b55d87f3f` |
| action record | `0x00888150..0x0088821C` | `0x00487550..0x0048761C` | `2083af25e5f8659aea78e7e44caa9dbeeae5fd53092ecc02d5b31b787a43bb7f` |
| CNetNPC vtable | `0x00F0DF58..0x00F0DFD8` | `0x00B0C358..0x00B0C3D8` | `9305c765da3e4af1a3e7082d6ad49aa49741bd2115f66e8119387890a452319e` |

Pinned literals: `_F_FORWARD@0x00F4B858`, `_F_WALK_000@0x00F0F1D8`, `.\\Data\\GC\\A\\@0x00F0F738`, `%s%s%s.kf@0x00F2B99C`, `s_PREDESCRIPT@0x00F15044`.

## Evidence grade and nonclaims

- **A:** CNetNPC vtable dispatch, gates, zero-argument plain branch, path formula, s_PREDESCRIPT runtime offset, same-map converter/search/insert chain, row-31 empty value, descriptor contents and packaged assets.
- **D conditional:** `actor+0x338 == M011` and the optional `0x0064D580` modifier leaves each A4 token unchanged. These two conditions are not promoted from naming similarity.
- **ไม่อ้าง** ว่า `actor+0x338` มีค่า `M011` ใน live Tornado Eagle, callback/resource completion occurred, map lookup returned non-null, any clip rendered, or original server chose selector 3220.
- **ไม่อ้าง** that `actor+0x248` is absent for CNetNPC or that its modifier is a no-op; only its exact position before path construction is proved.

## Verification

- verifier: `pf_bridge/staged/standing_a4_callback_verify.py`
- verifier SHA-256: `1b278bbb349d97040b2d9a56ce632fe822c09880d079fad3fee97b6126844a22`
- log: `pf_bridge/staged/standing_a4_callback_verify.log`
- log SHA-256: `23ff3e26c6a9fb7622c521651e537d7a23a291bd62b988acbdb1b9d2a1a39cf4`
- result: `PASS spans=11 literals=5 calls=14 slots=2 known_paths=6 traps=3; CNetNPC callback/path/map bridge exact; row31 runtime fallback prefix and live load/render unproven`

The stdlib verifier re-runs the pinned A4 raw-row and asset verifier, checks image/data/dependency hashes before use and image/data after use, covers six known paths, and rejects three prefix/token mutations.

## BUILD_PROPOSED

For the next attended selector-3220 run, record the CNetNPC identity plus these four values at the callback boundary: input token, post-`0x0064D580` token, selected prefix (`s_PREDESCRIPT` or `actor+0x338`), and final path/map-return status. **Accept the static bridge as attained only if** the final key is `.\\Data\\GC\\A\\M011_F_ATTACK_000.kf` on the same actor and lookup is non-null, followed by the visible clip/damage correlation required by the prior A4 result. **Stop/falsify** this candidate immediately if prefix differs from `M011`, the modifier changes the token to an unlisted action, the map lookup is null, or the callback gates return early.
