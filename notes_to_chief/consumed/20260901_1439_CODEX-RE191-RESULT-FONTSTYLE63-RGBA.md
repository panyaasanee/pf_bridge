[ถึง: chief, LANE-GM · cc: Panya, COO · จาก: OpenAI Codex static RE · 2026-09-01 14:39 +07:00]

# RE-191 RESULT — FontStyle 63 และเส้น parse/apply

ผล: **PASS ที่ชั้น conditional static + DATA palette; runtime pixels ยังเปิด**

## คำตอบตรงใบ RE-191

Premise ในใบต้องแก้ก่อนใช้: `0x00AA488F` **ไม่ใช่ RGB parser**. มันเป็น branch ของ `UILabel.FontStyleID`:

- present-but-empty หรือ sentinel `0x00F0930C` ข้าม conversion และ dispatch ID `0`
- nonempty/nonsentinel เข้า `0x00894700` → `_wtoi`; IMAGE ไม่พิสูจน์ digit validator ดังนั้นข้อความอย่าง `abc` ก็อาจเข้าและได้ `0`
- fallbackอีกขาใช้ embedded `FontStyle` แล้วเรียก parserตัวเดียวกับ registry

**[ORIGINAL EVIDENCE: IMAGE / MCG-IMG-057..058]**

- full six-section E8+rel32 census พบ direct callsไป `0x00A9DAE0` exactly 2 จุด: registry loader `0x00A9FA11` และ UILabel embedded-style branch `0x00AA490D`
- `0x00A9DAE0` อ่าน `FontColor` เข้า style `+0x30..+0x3C` และ `OutlineEffectColor` เข้า `+0x4C..+0x58`
- `0x0053F5E0` แปลง componentด้วย `_wtoi`, หาร exact `255.0`, clamp `[0,1]`
- `0x00AA6EF0` ส่ง FontColorไป UILabel vslot `+0xD8 -> 0x006D0F40` และ outlineไป `+0x224 -> 0x006D0CF0`

**[ORIGINAL EVIDENCE: DATA — แยกจาก IMAGE]**

| FontStyleID | FontColor RGBA | OutlineEffectColor RGBA | คำบรรยาย |
|---:|---|---|---|
| 61 | `(255,100,100,255)` | `(150,0,0,255)` | แดง/แดงอมชมพู |
| 62 | `(255,159,113,255)` | `(91,30,0,255)` | ส้ม/แซลมอน |
| 63 | `(179,179,179,255)` | `(60,60,60,255)` | เทา |

เมื่อต่อ DATA+IMAGEแบบติดป้าย: style63 normalizeเป็นประมาณ `(0.701960802,0.701960802,0.701960802,1)` และ outline `(0.235294119,0.235294119,0.235294119,1)`.

## เพดานที่ห้ามข้าม

- selectorเดิมผูก conditionally: 62คือ clear/normal lane, 61คือ offensive/bit lane, 63คือ CNetNPC vslot `+0x3C` true laneในขอบเขตที่ pinไว้
- นี่ไม่แปลว่า style63 = death ในทุกบริบท และไม่พิสูจน์ว่า live actorผ่าน gateนั้น
- ยังต้องเห็น live registry node, requested/applied ID และ pixelsของ actorตัวเดียวกันก่อนปิดส้ม→แดง→เทาบนจอ
- อย่า hardcodeสีหรือส่ง style IDตรง ๆ; clientเลือกจาก identity/relationship/death path. Implementationต้องคง canonical identityภายในและปิด wire mapping/reference seamsให้ครบ

## Artifact ที่ตรวจซ้ำได้

- `PF_MONSTER_COLOR_GATE.tsv` — 110,234 B — SHA-256 `8d236351d827a39a74fe9b5e1b9ac694f5f51af5328fcedc1d9f207720bcbaa0`
- `PF_MONSTER_COLOR_GATE.md` — 40,103 B — SHA-256 `1550827abd80711236f6345f34af481108a0469cb4feea10aa54c71ed2591165`
- `PF_MONSTER_COLOR_GATE.pair.json` — 529 B — SHA-256 `83666a082354444dec686afe54266fc6f6fd23545ba7e5e6216b3bab0f49eb09`
- `pf_rederive_monster_color_gate.py` — 202,548 B — SHA-256 `70762a525dabe1f0f50538106e7de130887197680927385d840009db9f6509dd`
- rows 66 = IMAGE 58 / DATA 8; `--check` read-only PASS; IMAGE before/after `14,759,424` B / `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`

Codexไม่ได้แก้ ServerProject, queue, workflow, lease หรือ Git และไม่ได้รัน client/server/tests/dump/capture.
