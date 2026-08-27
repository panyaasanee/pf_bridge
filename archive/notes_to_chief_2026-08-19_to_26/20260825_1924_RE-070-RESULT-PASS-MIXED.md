[ถึง: chief cloud (cc) และ Panya · จาก: RE runner LOCAL]

# RE-070 RESULT — DONE / PASS-MIXED: object คือ UI `SystemSetting_LogoutConfirm`; MODE ไม่ใช่เซตปิด; `+0x24` เป็นทั้ง display และ gate

**เวลา:** 2026-08-25T19:24:13+07:00  
**ใบ:** `RE-070 ORCHESTRATOR-TRANSITION-GATE-001` · `STATIC-ON-BRIDGE`  
**สถานะเสนอ:** `DONE / PASS-MIXED` — objective ทั้งสามข้อมีคำตอบแบบ static; มี erratum ต่อ R100 และ bounded nonclaim เรื่อง alias นอก vtable graph  
**รอบนี้:** ไม่เปิดเกม · ไม่บูต server/client · ไม่จับ `LOCK_GAME` · ไม่แตะ canonical DB · ไม่แก้ source/queue · ไม่ทำ git operation

## สรุปคำตอบสามข้อ

1. **writer ของ `[object+0x28]` ในกราฟ class ครบมีสองจุด:**
   - `0x7197D0`: ล้างเป็นศูนย์ใน UI-init method (vtable slot `+0x18`, entry `0x719780`)
   - `0x7199EA`: คัดลอก `event_record+0x2C` เข้า `object+0x28` ใน handler ของ event ชื่อ UTF-16 `initial` (vtable slot `+0x30`, entry `0x719990`)
   writer ของ `+0x24` อยู่คู่กันที่ `0x7197CD` (clear) และ `0x7199E4` (`event_record+0x30 -> object+0x24`) · census recursive CFG ของ **31 slots ทั้ง vtable** พบ writer สี่จุดนี้เท่านั้น ไม่มี writer จาก inbound handler หรือ tick ในกราฟที่วัด
2. **`+0x28` ไม่ได้ถือค่าแค่ `{1,4}`:** handler รับ dword ใด ๆ จาก record; โค้ดทำ `dec; cmp 3; ja default` แล้ว jump-table สำหรับค่าเดิม `1..4` · ค่านอกช่วงไป default ได้ จึงพิสูจน์ว่า `{1,4}` ไม่ใช่เซตปิด
3. **`+0x24` เป็นทั้ง display และ gate:** คำนวณ `delta = [object+0x24] - [app+0x7BC]`
   - entry `0x719990` ใช้ delta ในแขนงแสดงผล (แขนง MODE 1/4) และส่ง delta เข้า UI object
   - entry `0x719620` เปรียบเทียบ `delta` กับค่าคงที่ `3`; ถ้า `delta <= 3` และ `[object+0x18] != NULL` จะเรียก virtual `[vtable+0xF4](false)` ของ sub-object นั้น
   ⇒ มัน **ไม่ใช่ display-only** · threshold ที่วัดได้คือ `3` · writer/gate ไม่อ่าน `GetTickCount` / `timeGetTime` / QPC โดยตรง

## 🔴 Erratum ต่อฐาน R100

- `0x719AB0` และ `0x719B90` **ไม่ใช่หัวฟังก์ชันสองตัว**: ไม่มี direct rel32 caller และไม่มี pointer-table reference ทั้งคู่; ทั้งสองเป็น basic block ภายในฟังก์ชันเดียวที่เริ่ม `0x719990`
- ขอบเขตจริง: `[0x00719990,0x00719C11)` · file offset `0x00318D90` · len `641` · instructions `176` · CFG errors `0` · gap `19` · indirect jumps `1` (jump-table MODE) · SHA-256 `a55288cb6a345d5c12d4d558dc7b13185f44bbc4cb6a2ac12188dbe1608e7576`
- vtable `0xF45030` resolve ชื่อจาก factory ในอิมเมจได้ตรง ๆ เป็น UTF-16 **`SystemSetting_LogoutConfirm`**: factory `0x721700` เปรียบเทียบชื่อที่ `0xF2FDAC`, allocate `0x2C` ไบต์ แล้วติดตั้ง `0xF45030` ที่ `0x721878`
- เพราะฉะนั้นคำเรียก *session/connection orchestrator* ใน R100 เป็นการตีความกว้างเกินหลักฐานชื่อ class; ของจริงที่พินได้คือ **UI logout-confirm handler ที่ถือ sub-object connection และมี transition logic**
- `[vtable+0xF4]` ที่ `0x719BD0/0x719BE7` เป็น slot ของ sub-object `[object+0x1C]/[object+0x18]` ตาม correction ของ R166 — ไม่ใช่ slot ของ vtable `0xF45030`

## MODE branch map — รายงาน behavior ไม่ตั้งชื่อ semantic

| ค่า `+0x28` | branch ที่วัดได้ |
|---|---|
| `1` | resource id default `0x2C4`; เข้า elapsed-display; `[+0x1C]` close arg = true |
| `2` | resource id `0x59D`; ไม่เข้า elapsed-display; `[+0x1C]` close arg = false; มี UI branch เฉพาะ mode 2 |
| `3` | resource id `0x59C`; ไม่เข้า elapsed-display; `[+0x1C]` close arg = false |
| `4` | resource id `0x59E`; เข้า elapsed-display; `[+0x1C]` close arg = true; และ `[+0x18]` close arg = false |
| ค่าอื่นทั้งหมด | ไป default resource id `0x2C4`; ไม่เข้า elapsed-display; `[+0x1C]` close arg = false |

🔴 ตารางนี้ **ไม่ใช่ mapping `1=exit` / `4=char-select`** — ใบนี้ไม่มีหลักฐานพอให้ตั้งชื่อสองค่านั้น

## Call-site census และชนิด path

- `0x719990`: ไม่มี direct rel32 caller; pointer เดียวคือ vtable `0xF45030 +0x30` (`0xF45060`) ⇒ **UI event/config path**; ตรวจ record string `initial` ก่อนคัดลอก `+0x30/+0x2C`
- `0x719780`: vtable slot `+0x18`; clear `+0x24/+0x28` ⇒ **UI lifecycle/init path**
- `0x719620`: vtable slot `+0x2C`; อ่าน/ใช้ค่าแต่ไม่เขียน ⇒ **tick/update consumer path**
- `0x719C80`: vtable slot `+0x28`; dispatch ตาม identity ของ sub-object; ไม่เขียน `+0x24/+0x28`
- `0x719C30`: direct rel32 caller **หนึ่งจุด** `0x719CC1` ภายใน `0x719C80`; เมื่อ gate ของ `[object+0x18]` ผ่าน มันสร้าง/ส่ง `LogoutVital` subcode `0x0A` แล้ว clear app flag · ไม่ใช่ writer ของ MODE/timer
- T6 ไม่ต้องเปิด: UI binding ถูก resolve จาก factory สำเร็จแล้ว และ T1–T4 ไม่ตัน

## `+0x24` กับแหล่งเวลา

- writer ที่พินได้คัดลอกจาก `event_record+0x30` ไม่ได้เรียก OS clock
- reference ที่นำมาลบคือ `[app+0x7BC]`; จุดเขียนที่ผูกกับ app โดยตรงและพินซ้ำได้คือ app ctor `0x40AC22` (zero), `GSCN_RunTimeProtocolRes` `0x5E40F7`, `SelectActorVital` `0x5EFC7A`
- มี literal-displacement candidate เพิ่มที่ `0x9C9349` (`movss [esi+0x7BC], xmm1` หลัง `xorps xmm1,xmm1`) ซึ่งเป็น zero-reset; **ยังไม่ได้พิสูจน์ว่า `esi` alias app singleton** จึงไม่ใช้มันตั้งความหมาย
- class init มี `GetTickCount` ที่ `0x7198CC` จริง แต่ผลถูก `and 1; inc` ใช้เลือกค่า 1/2 ในการประกอบ UI string และ **ไม่มี dataflow เข้า `+0x24/+0x28`** · writer/gate graph ไม่มี reference ของ `GetTickCount`, `timeGetTime`, QPC
- จึงสรุปได้เฉพาะ operation: `+0x24` เป็นค่าจาก event record ที่ถูกเทียบกับ app/protocol reference และมี gate `<=3`; **ไม่ตั้งชื่อว่า wall clock / deadline / timestamp**

## Rider: `ReturnSelectServerVital 0x709E` สองเฟรม

ผลนี้ปิดความขัดกันได้โดยแยก direction:

- `PF_FIELD_VALIDATION.tsv`: `ReturnSelectServerVital W = observed 2 / parsed 2 / files 2 / VALIDATED`; แต่ `R = observed 0 / NOT_OBSERVED`
- ไฟล์ 1: `GameClient/capture_demo_fullloop_20260817_035212/capture_v141/GAME_20260817_035430_388049_52451.txt` · SHA-256 `2a43616bac2370cd68297ff533c9ef0c84498d1ea35e6d81957af81391efa3ab` · block ordinal 6
- ไฟล์ 2: `GameClient/capture_gt011_20260818_170121/capture_v141/GAME_20260818_170347_645157_52155.txt` · SHA-256 `b79b22f9c69519a7baf560470af2e2248985ed648c8d3a2c7c1bf81053d53ee3` · block ordinal 7
- ทั้งสองเป็น `DECOMPRESSED` / direction **W**, outer `GSCN_LoginProtocol 0x453A`, derived mask มี bit `0x02`, nested count `1`, nested wrapper id **`0x709E`** ตรงทั้งคู่
- ⇒ ไม่ใช่ schema collision ที่ชั้น message id/wrapper: มี nested id `0x709E` จริงและ registry 519-name ไม่มี collision · แต่ผลนี้ไม่ได้ re-interpret ค่า payload
- ⇒ ไม่ขัดกับ nonclaim ว่า **client ยังไม่เคยรับ 0x709E ขา R**; ขณะเดียวกันมันหักล้างถ้อยคำกว้างใน `logout_hypothesis.py` ที่ว่า **`0x709E has no client producer`** — อย่างน้อย client/capture path เคยผลิตขา W สองครั้งแล้ว
- ขอให้ chief แก้ถ้อยคำ source/ledger เป็น: **พบ outbound W producer สองเฟรม; inbound R ยังไม่พบ; ความหมาย/non-zero provenance ของ payload ยังไม่ได้วัดใน rider นี้** · รอบนี้ RE runner ไม่แก้ source เองและไม่เปิดใบใหม่

## Mandatory searches สองที่

- **ค้นใน `pf_bridge\external\` แล้ว:** เจอ `LogoutVital`/`ReturnSelectServerVital` ใน protocol registry, serializer fields และ field validation; เจอ rider W=2/R=0 ตามข้างบน · **ไม่เจอ** orchestrator VA (`f45030/719ab0/719b90/719c30/719c80/719bd0/719bef/f45058`) ในห้าตาราง `PF_PROTOCOL_REGISTRY`, `PF_SERIALIZER_FIELDS`, `PF_FIELD_VALIDATION`, `PF_PROTOCOL_PRIORITY`, `PF_RUNTIME_CLASSMAP` (0 hit)
- **ค้น `gamedata` แล้ว:** `rg -i` ทั้ง `gamedata/**/*.tsv` และ `*.md` ด้วย VA/class/message ชุดเดียวกัน (`f45030`, methods, `ReturnSelectServerVital`, `LogoutVital`, `orchestrator`) = **0 hit** · ขอบเขตคือ 188-table dump + indices/docs ที่มีอยู่; ไม่ใช่คำอ้างว่าไม่มีในไฟล์ข้อมูลชนิดอื่นนอกชุดนี้

## Spans / SHA-256 / recursive CFG

| entry | span | file offset | len | instructions | CFG errors | gap | indirect | SHA-256 | บทบาท |
|---|---|---:|---:|---:|---:|---:|---:|---|---|
| `0x00446F30` | `[0x00446F30,0x004470DE)` | `0x00046330` | 430 | 154 | 0 | 0 | 0 | `9c1157d3109c27c41783d6eed630a6eb46511ef6789a4e121306944ec1271d7d` | positive control GT-040 |
| `0x00719620` | `[0x00719620,0x00719672)` | `0x00318A20` | 82 | 27 | 0 | 0 | 0 | `b11ba6a3189e85e449606502b17e086cd141190c939765a4b2d68e10039af158` | delta threshold gate / update |
| `0x00719680` | `[0x00719680,0x00719771)` | `0x00318A80` | 241 | 98 | 0 | 0 | 0 | `638ac40b75b5dd7750fc4e1ad0fc61ea5e88a5284d6a02729fadb879586bf0f4` | vtable slot `+0x60` binding helper |
| `0x00719780` | `[0x00719780,0x0071998F)` | `0x00318B80` | 527 | 151 | 0 | 0 | 0 | `b0a95a08119a7035f42b5839a5a06914b9e35badf945603a81ec3fd829183606` | UI init / clear writers |
| `0x00719990` | `[0x00719990,0x00719C11)` | `0x00318D90` | 641 | 176 | 0 | 19 | 1 | `a55288cb6a345d5c12d4d558dc7b13185f44bbc4cb6a2ac12188dbe1608e7576` | event writer + MODE switch; gap 19 = four jump-table case stubs |
| `0x00719C30` | `[0x00719C30,0x00719C7B)` | `0x00319030` | 75 | 20 | 0 | 0 | 0 | `e6dc4a7c5d73dbe5bed6d4d0e7864650b54eeb26057195c2af707c5cebd720df` | sub-object-gated `LogoutVital 0x0A` send path |
| `0x00719C80` | `[0x00719C80,0x00719CCB)` | `0x00319080` | 75 | 29 | 0 | 0 | 0 | `1bb77a4b9f635028268474394a733dde90944ac5f246f87c23f4f5462564a02d` | event dispatch |
| `0x00721700` | `[0x00721700,0x0072197E)` | `0x00320B00` | 638 | 201 | 0 | 0 | 0 | `8864d161cfd431acbec4d90b10c0db2f2b9f5a7a4e88b3bf50f01f90b6cc4d3e` | name factory → class/vtable |
| `0x009C8FF0` | `[0x009C8FF0,0x009C9567)` | `0x005C83F0` | 1399 | 257 | 0 | 0 | 0 | `a6294f8ccefb585cb972b49b3e812387773bf84219f655b9ee3c293284dd0f2f` | literal `+0x7BC` zero-reset candidate (alias unproved) |

vtable `0xF45030`: 31 slots ถึง `+0x78`, zero sentinel ที่ `0xF450AC`; SHA-256 ของ pointer bytes `[0xF45030,0xF450AC)` = `64146715dc527dd2508f96a88e6a5960162ccf201a51ceabd90e7b785c4cbd97`

## T0 / reproducibility / read-only

- image size `14,759,424 B`; SHA-256 ก่อน/หลัง `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`
- 256-byte guards ผ่านทั้งห้า: `0x00318E00=3cba6128…`, `0x00318F00=64802a0f…`, `0x00319000=79064c48…`, `0x00B43400=023ab4a4…`, `0x00B43500=ae0490a8…`
- positive control `0x446F30` SHA ตรง GT-040
- verifier: `staged/re070_static_verify.py` SHA-256 `e27f1c14271c151eac6954b8ac0f7927623b8a3983c304dde1dce2b06465b7c1` (ณตอนรันสุดท้าย) · **104/104 guards, failed 0**
- probe: `staged/re070_static_probe.py` SHA-256 `43c5403bc6c8f9d4539f4d4e149d6f6b3026f73e96069b82bedf63be499f1fd4`
- verifier พิน SHA ก่อนอ่านและเทียบหลังจบของ image, CFG helper, external/gamedata indices+tables ที่ใช้, R100 factpack, GT-040 control note, validator+inventory, source `logout_hypothesis.py`, และ capture สองไฟล์; **ทุกไฟล์ตรงก่อน/หลัง**
- วิธี negative: recursive CFG + complete 31-slot vtable walk + rel32/dword census + exact wrapper parse; **ไม่ใช้ linear disassembler เป็นหลักฐานของผลลบ**

## Nonclaims

1. ไม่พิสูจน์ mapping semantic ของ MODE (โดยเฉพาะห้ามเขียน `1=exit` / `4=char-select`)
2. ไม่พิสูจน์ว่า value นอก `1..4` เกิดจริงที่ runtime; พิสูจน์ว่าโค้ดยอมรับและมี default branch
3. writer census ครบภายใน factory + vtable 31-slot graph; **ไม่ exclude pointer alias จากโค้ดนอกกราฟทั้งโปรแกรม**
4. ไม่ตั้งชื่อ `+0x24` ว่า timestamp/deadline/wall clock; พิสูจน์เฉพาะ copy, subtraction, display และ threshold gate
5. literal `[esi+0x7BC]` ที่ `0x9C9349` เป็น zero-reset จริง แต่ยังไม่พิสูจน์ว่า `esi` คือ app singleton
6. rider พิสูจน์ W wrapper/id สองเฟรมและ R=0 ใน corpus ที่แช่แข็ง; ไม่พิสูจน์ความหมาย field values และไม่พิสูจน์เซิร์ฟเวอร์ต้นฉบับ
7. ผลนี้เป็น static/wire ชั้นเดียว ไม่มี client-observable claim
8. ไม่ออกแบบ variant D, ไม่เปิดใบใหม่, ไม่บอกว่า server ของเราควรตอบอะไร — chief/Panya เป็นผู้ตัดสินงานถัดไป

**ไฟล์ที่ RE runner เขียนในรอบนี้:** `staged/re070_static_probe.py`, `staged/re070_static_verify.py`, และจดหมายฉบับนี้เท่านั้น
