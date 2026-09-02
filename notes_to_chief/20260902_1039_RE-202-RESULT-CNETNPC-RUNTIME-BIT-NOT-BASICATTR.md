ขอให้ chief กรอก ### result: และปิดหัวใบให้ด้วย — ผล RE-202: DONE/PASS; `+0x70 & 0x40` ใน quest selector setter เป็นบิต runtime ของ `CNetNPC` ไม่ใช่ presence mask ของ attached `BasicAttr`

# RE-202 result — CNetNPC runtime/model-ready bit

- ผู้รับ: chief / COO / LANE-A
- เวลาเริ่มใบ: `2026-09-02T10:30:02.572+07:00`
- เวลา checkpoint ผล: `2026-09-02T10:39:44.261+07:00`
- สถานะ: `DONE/PASS`
- งาน: job 1-2 ปิดครบ
- route hygiene: หัวใบ `RE-202` ไม่มี route tag แต่เนื้อหาเป็น static IMAGE/bridge และ COO `0741` ให้เป็น RE priority แรก จึงทำตามกติกาใหม่; ขอ chief/opener เติม `[STATIC-ON-BRIDGE]` ตอนปิดหัวใบ

## คำตอบสั้น

เลือก **ข. `CNetNPC+0x70` runtime/model-readiness bit**

ตัวเลข offset/mask ชนกับ `BasicAttr+0x70 & 0x40` จริง แต่ไม่มี crosswalk ให้ rebase เป็น `BasicAttr` ใน setter นี้ ตรงกันแค่ตัวเลขจึงห้ามจับคู่กัน

## หลักฐาน ownership แบบ exact

Pinned IMAGE: `GameClient.local.bin`, 14,759,424 bytes, SHA-256 `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`.

Setter exact span `[0x0045BC80,0x0045BCBC)`, raw `[0x0005B080,0x0005B0BC)`, SHA-256 `f808c0d68b1a782d3441e118a25a94ee73e1f4aea37824b06fd2e2c6fb112bc5`:

```text
0x0045BC81  mov  esi, ecx
0x0045BC83  F6 46 70 40       test byte ptr [esi+0x70], 0x40
0x0045BC89                    movsx eax, byte ptr [esi+0x364]
0x0045BC9C                    cmp dword ptr [esi+0x360], 0
0x0045BCA5                    mov ecx, [esi+0x360]
0x0045BCAC                    call 0x006078D0
0x0045BCB1                    mov byte ptr [esi+0x364], bl
```

ฐาน `ESI` เดียวกันเริ่มจาก setter `this` (`ECX`) และใช้กับ gate `+0x70`, QuestIconBoard `+0x360`, cache `+0x364` โดยไม่มีการ dereference ไป attached attr ระหว่างทาง ดังนั้น owner ของ gate คือ object เดียวกับ board/cache: `CNetNPC`.

Caller ยืนยันชนิดซ้ำ: QuestNPCModule refresh `[0x00616790,0x00616827)`, raw `[0x00215B90,0x00215C27)`, SHA-256 `4008a0568145fd75ae18286dd1582ceabe8393b98fa4f7b78648827b68075cc2` โหลด owner `CNetNPC` จาก `[QuestNPCModule+0x18]`; ที่ `0x006167D6` โหลด pointer เดิมเข้า `ECX` แล้ว direct-call setter ที่ `0x006167E4`. Path เดียวกันแยก attached `NPCAttr` ชัดเจนผ่าน `CNetNPC+0x358 -> NPCAttr+0x78`.

มี positive producer ฝั่ง client-local ด้วย: typed CNetNPC model callback `[0x00444730,0x0044497B)`, raw `[0x00043B30,0x00043D7B)`, SHA-256 `bff91e77c4570c959170e89cd65d96b175eb6a1728b26ac465bdc14da04f5a33`; ที่ `0x004448B4`, bytes `83 4F 70 40`, ทำ `or dword ptr [edi+0x70],0x40` หลัง callback/resource gates. นี่เป็น producer แบบ client-local ของบิต actor เดียวกัน ไม่ใช่ wire walk-speed field.

Control path ของความชนกัน: template path `[0x0045BF40,0x0045C15D)` SHA-256 `afb5662a3f1a81c98de8ed77d82262747b8563ce25be88d041c8dea89e52fb72` อ่าน `MOBS.n_SPEED_WALK` แล้วเรียก BasicAttr/NPCAttr setter `0x00464960` ผ่าน pointer `[CNetNPC+0x358]`; path นี้ไม่แตะ selector setter's `CNetNPC+0x70` gate. เพราะฉะนั้น server ส่ง/เปลี่ยน walk speed ไม่ใช่วิธีเปิด quest-board gate นี้

## ค้นของเดิมก่อนถอด

- `pf_bridge/external/`: ตรวจ inventory 2,683 files / 930,201,065 bytes, manifest SHA-256 `18f8d9750abe7d8b65fa06ca309a8eefa3708fc1db3daa76cacc10529cdfe8f5`; ค้น `0x0045BC80`, `QUEST_MARK_SELECTOR`, quest mark/icon, `CNetNPC`, `n_SPEED_WALK`. พบ generator/artifact เดิมที่ระบุ CNetNPC owner (`PF_ATTR_QUEST_MARK_SELECTOR`, `PF_COMBAT_LETHAL_TAIL_DELTA`, attr semantics corpus) แล้วตรวจ SHA และ re-verify span/bytes จาก IMAGE; ไม่พบหลักฐาน crosswalk ที่ทำให้ setter base เป็น BasicAttr
- `pf_bridge/gamedata/`: ตรวจ inventory 1,109 files / 15,319,585 bytes, manifest SHA-256 `d3031face2ffb3d2e93a018911fda4af2e792459e516d3d99d9764f27db63549`; ไม่พบ `0x0045BC80`, quest-mark/icon selector หรือ `CNetNPC`. พบเพียง schema/data ของ `MOBS.n_SPEED_WALK` ใน `PF_GAMEDATA_COLUMNS.tsv` และ `tables/CONSTDATA_TH__MOBS.tsv`; gamedata ไม่มี object-layout crosswalk จึงใช้พิสูจน์ owner ไม่ได้

## Input pins

- `CLIENT_RE_QUEUE.md`: `4e4b19fc4d0f569005fee646e5b51ba3dc2ee06b91b0867475a601bec37033d2`
- `NEW_ORDERS.txt`: `521a51e8e815d8a73fda4f3a51d67704e149dd7ad459ed06765d4118831c20b3`
- `PF_ATTR_QUEST_MARK_SELECTOR.tsv`: `3218d619a400dfcab52416489dcf8e6b85e6cbfd5a8bbd14d6ccad39dbfb9bf0`
- `PF_COMBAT_LETHAL_TAIL_DELTA.tsv`: `6f6cffddfc0d77d9853637051ef572576ceff9ba7bee50bb1a01eb21c7263170`
- `PF_ATTR_FIELD_SEMANTICS.tsv`: `1418b7559f5b05feef585490e76d33e8f72cd82c1ff854941d7faf37878c7f2f`
- `pf_rederive_attr_semantics.py`: `c7d6c560f0848b3eb0edc34bb147a66d5c3fc1661ed0d88fb9c4065ca0a7528c`

## Nonclaims

- เป็น static IMAGE ownership/result เท่านั้น ไม่ใช่ client-observable proof ว่า callback นี้รันกับ NPC จริงหรือ icon ปรากฏบนจอ
- ไม่อ้างว่าได้ทำ exhaustive census ของ writer/caller ทุกตัว และไม่ใช้ linear-disassembler absence เป็นหลักฐานผลลบ
- ไม่อ้าง original-server policy, runtime cadence/timing หรือความหมาย pixel ของ texture
- แยก wire/DB facts ออกจาก client-observable เสมอ; รอบนี้ไม่เปิดเกม/server ไม่แตะ canonical DB และไม่แก้ source/queue/external/gamedata

## BUILD_IMPACT

- สมมติฐานที่ให้ server walk-speed/BasicAttr presence เปิด quest-board gate ต้องคงสถานะ withdrawn
- หาก LANE-A จะทำ quest-mark ต่อ ต้องเคารพ lifecycle/model-readiness ของ `CNetNPC` หรือใช้ hook หลัง client-local gate; ห้ามผูกกับ `BasicAttr+0x54` เพียงเพราะ offset/mask เท่ากัน
- รอบนี้ไม่มี build/source change

