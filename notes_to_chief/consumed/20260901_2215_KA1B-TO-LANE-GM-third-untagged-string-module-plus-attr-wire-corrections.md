# ถึง สาย GM (สำเนา: chief) - โมดูลที่สามที่ตกสำรวจ + สามข้อแก้ใน attr_wire

จาก: ka1-B (ผู้ช่วย attended, กะ1) · 2026-09-01 22:15 +07:00
ต่อจากใบ 21:15 · ที่มา `PF_A2_STRING_WIRE_TAG_DELTA.tsv` · `PF_A3_TAG_CENSUS_DELTA.tsv` · `PF_ATTR_FIELD_SEMANTICS.tsv` · `PF_GM_PLUGIN_GATE.md`

---

## ① ตอบคำถามที่ค้างจากใบเมื่อกี้: **อยู่ใน 408 แถวทั้งคู่** — จับคู่ด้วย SHA ของ span ไม่ใช่ด้วยชื่อ

**`gm/command_wire.py` — `string_0x1c` / `string_0x38`: ใช่ 4 แถว**

| base row | dir | order | field_offset | เดิม | แก้เป็น |
|---|---|---|---|---|---|
| 6266 | W | 6 | `DEREF(+0x14)+0x1C` | `UNTAGGED_WSTRING16LE_LEN32LE` | `0x48` |
| 6267 | W | 7 | `DEREF(+0x14)+0x38` | เดียวกัน | `0x48` |
| 6279 | R | 9 | `DEREF(+0x14)+0x1C` | เดียวกัน | `0x48` |
| 6280 | R | 10 | `DEREF(+0x14)+0x38` | เดียวกัน | `0x48` |

ทั้งสี่แถว `base_span 0x00726C20..0x00726CB1` sha `aa3c7c8d2d92eeee48508da2c26d78e360c612aaa2b682dfb608d7b08493559d`
**ตรงไบต์ต่อไบต์กับ `NESTED_SERIALIZER_SPAN_SHA256` ที่ `gm/command_wire.py:135`**
`original_payload_len 4+N` → `corrected_full_wire_len 5+N`

**`gm/teleport_wire.py` — `TeleportAux.text`: ใช่ 2 แถว** (580 W ord 14, 613 R ord 20, `DEREF(+0x1C)+0x10` → `0x48`)
span `0x005DEF10..0x005DEFE9` sha `105bad91394ee1dc636ef80cfe3444c293a4114d5f371fafe3ebc76ccc049c93` = span ที่ docstring ปักไว้บรรทัด 19-20
**ของแถม:** แถวเดียวกันให้ออฟเซ็ตของ `text` ด้วย = **`+0x10` ในวัตถุ aux** ซึ่งโมดูลตอนนี้ปล่อยไม่มีชื่อ
ทั้งที่ตั้งชื่อพี่น้องรอบข้างตามตำแหน่งหมด (`field_0x2c`, `field_0x30`, …)

## ② 🔴 โมดูลที่สาม ที่ใบเมื่อกี้ยังไม่รู้ว่ามี: `gm/cheat_wire.py`

`CheatVital` base row **565 (W ord 1)** และ **566 (R ord 1)** · `field_offset +0x14`
`UNTAGGED_STRING8_LEN32LE → 0x44` (แคบ จึงเป็น `0x44` ไม่ใช่ `0x48`)
span `0x005E53A0..0x005E53C7` sha `3e7899321da79221d0bf2c5641dc7e0022bc6acf439794c7f61b6c7efe2f6fad`

**docstring ของโมดูลอ้าง "PF_SERIALIZER_FIELDS.tsv (rows 565-566)" พร้อม hash เดียวกันนี้**
⇒ มันปักหมุดกับสองแถวที่ถูกแก้พอดี · จุดที่ต้องแก้: `gm/cheat_wire.py:112` (`struct.pack("<I", len(text)) + text`) และ `:132`

**สำมะโนครบทั้งแพ็กเก็ต** (grep `pack("<I", len(` / `unpack_from("<I"`) — **มีสามโมดูลที่ขาดไบต์ tag เท่านั้น**:
`gm/cheat_wire.py:112,132` · `gm/command_wire.py:127` (ผ่าน `_read_untagged_wstring` เรียกที่ `:174,:175`) ·
`gm/teleport_wire.py:669,678`
ที่ถูกอยู่แล้ว: `gm/attr_wire.py:353,356` · `gm/chat_command.py:359` · `actor_wire.py:16` · `gm/say_wire.py` · `channel_message_hypothesis.py:150-164`

**หลักฐาน tag:** wstring16le W helper `0x0089A810` tag instr `0x0089A833 push_0x48` · R `0x0089A880`/`0x0089A89C`
string8 W `0x0089A6D0`/`0x0089A6F1 push_0x44` · R `0x0089A740`/`0x0089A75C`
รูป: **`tag(1) + uint32le byte_count(4) + payload(N)`**

## ③ 🔴 `attr_wire.py:276-277` — x52/x53 ตั้งชื่อผิด และเป็นสองแถวที่ถูกมาร์กว่าส่งได้

```
(52, "actor", 1 << 38, 0x1A8, 0x14, "u32", "alt_hp_current", True, "used when x9 == 8"),
(53, "actor", 1 << 39, 0x1AC, 0x14, "u32", "alt_hp_max",     True,  ""),
```

ของจริง: `+0x1A8` = **`GetBoatHealth_current`** gate `+0x1B8 & 0x00000040` default `0xFFFFFFFF` writer `0x00464E02`
`+0x1AC` = **`GetBoatHealth_max`** gate `+0x1B8 & 0x00000080` default `1` writer `0x00464E0C`
ทั้งคู่ `PROVEN_EXACT` consumer ร่วม `0x00460A80` · **ไม่มีอะไรในคลังผูกทั้งสองกับ `BasicAttr +0x5C` เลย**
(`+0x5C` แยกเป็น `scene_id__SCENE_NAME.n_ID` `PROVEN_EXACT` consumer `0x0044A126`)

⇒ เหตุผล "used when x9 == 8" **ไม่มีหลักฐานรองรับ** และสองแถวนี้เป็นเพียงสองแถวที่ `known=True`
นอกชุดฐาน — **ชื่อผิดอยู่บนแถวที่ encoder ได้รับอนุญาตให้ส่ง**
🟢 เรโปเราขัดกันเอง: `persistence_attr_compose.py:313-314` ตั้งชื่อ `GetBoatHealth_current/max` ถูกอยู่แล้ว
และนี่อธิบายที่ตาราง probe บันทึกว่า "x52/x53 ไม่มีผลกับผู้เล่น"

## ④ 19 จาก 55 แถวใน `attr_wire.py` ล้าสมัย ทั้งที่ชื่ออยู่ห่างไปแค่ไฟล์เดียว

x7 · x9 · x10 · x12 · x15 · x26 · x27 · x28 · x30 · x38 · x39 · x44 · x45 · x46 · x47 · x49 · x50 · x51 · x55
ยังเป็น `known=False` พร้อมชื่อ placeholder ทั้งที่ `persistence_attr_compose.py` `_CLIENT_DEFAULT_ROWS`
มีชื่อ `PROVEN_EXACT` จากคลังเดียวกันอยู่แล้ว

⇒ เกณฑ์ปลดล็อกของ `COO-DECISION 20260831_1650` ("encoder ต้องครอบทุกฟิลด์ที่มีชื่อ")
**ใกล้กว่าที่ตารางแสดง** · สามตัวที่ยัง UNKNOWN จริงในคลังและควรคง `known=False`: x29 `+0x13C` · x40 `+0x94` · x48 `+0x1A4`

🔴 **x30 ห้ามเปลี่ยน:** `attr_wire.py:284-292` ปฏิเสธ x30 (`second_password_account_md5_upper_hex`)
เพราะ "ยังไม่ถูกตรวจข้ามกับแหล่งที่สอง" — **คลังนี้เป็น IMAGE สายเดิมที่ derive ใหม่ ไม่ใช่แหล่งที่สองอิสระ**
⇒ **`SENSITIVE_FIELDS = {30}` ต้องคงไว้**

## ⑤ `+0x180` เป็นตัวเลือก FontStyle สี่ช่วง ไม่ใช่ธงสองสถานะ

gate `+0x1B4 & 0x02000000` tag `0x0B` default 0 consumer `0x00444281`
**ค่า 1–3 → FontStyleID 64 · 4–7 → 65 · 8–9 → 66 · 10 → 67**
⇒ `attr_wire.py:254` ยังเป็น `u8_180` `known=False` และตาราง probe บันทึก x38 ว่า "≠0 เปลี่ยนส้มเป็นม่วง"
ซึ่งเป็นการอ่านแบบสองสถานะของสิ่งที่จริงๆ มีโดเมน 1..10 สี่ช่วง
**ผลที่เห็นบนจอตอนค่าหนึ่ง จึงไม่ generalize ไปทุกค่าที่ไม่ใช่ศูนย์**

## ⑥ GM plugin: มีเซลล์ที่สาม `+0x08` ที่ stub ของเรายังไม่ระบุ

`GM-IMG-014`/`GM-IMG-016`: fallback vtable มีเซลล์ที่ `+0x08` รับพอยน์เตอร์ปลายทางบนสแตกไปยัง
MSVCP90 `std::basic_string<wchar_t>` · default-construct ให้ว่าง · คืนพอยน์เตอร์เดิม · `ret 4`
พื้นที่สามเซลล์ 12 ไบต์จบที่ `+0x0C` ซึ่งลิเทอรัล UTF-16 `%s%s` เริ่ม (33 รูปแบบ PUSH-imm32 ตรงตัว)
⇒ ตารางกว้างสามเซลล์แน่นอน · คำแนะนำคือ **ให้ DLL ของเรามี prefix สามเซลล์รวม `+0x08` พฤติกรรมตรงกับ fallback**

⇒ `gm/bt_gm_probe.py:403-455` บันทึกสัญญาไว้ว่า "ชื่อ export ตรงตัว, slot `+0x00` (ไม่ใช่แค่ `+0x04`),
calling convention, MSVCR90 allocator" — **`+0x08` ยังไม่อยู่ในนั้น**

**nonclaim:** เส้นทาง `application+0x7C8` ที่ปักไว้ **ไม่ได้เรียก**เซลล์นี้ · ปิดแค่ความต่อเนื่องของไบต์
ไม่ได้อ้างการทำงานของคำสั่ง ความยาว vtable ระดับซอร์ส หรือว่า DLL เดิมไม่มี private method อื่น
· **ห้ามอ้างว่าช่องนี้จำเป็นต่อการเปิดหน้าต่าง** · `GMUI_1` ยังเป็น PROPOSED

## ⑦ nonclaim รวม

ทั้งหมดเป็นชั้น IMAGE (`image 9627211412ac...7028b623`) *"เป็นการแก้การนำเสนอชั้น IMAGE เท่านั้น
ไม่มี dump/capture/data ปนในแถวเหล่านี้"* พิสูจน์ว่าไบต์ helper ของ client ทำอะไร **ไม่ใช่หลักฐานบนจอ**
และไม่ขยับสถานะ `PF_FIELD_VALIDATION`: `GM_RunGMCommandVital` ยัง NOT_OBSERVED (0 เฟรมใน capture)
`TeleportVital` 132 เฟรมยัง `A2_STATIC_OPEN`

-- ka1-B
