# PF protocol registry

ไฟล์นี้สร้างจาก `GameClient.local.bin` โดย `pf_extract_protocol.py` แบบอ่านอย่างเดียว
และไม่ใช้ความใกล้กันของสตริงกับ vtable เป็นหลักฐาน; ทุกแถว TSV ติด `source=IMAGE`

## วิธีวัด

- สแกนเฉพาะ `.text` ด้วยรูป 24 ไบต์ `push literal; call 0x89C080; mov ecx,eax; call 0x89BD00; mov word [slot],ax; ret`.
- หา getter จากไบต์ 7 ไบต์ `66 A1 <slot> C3`.
- sweep dword ทั้งไฟล์หา getter และรับ vtable เฉพาะเมื่อ marker ที่ `+0x08` เป็น `0x00401B20` และ getter อยู่ที่ `+0x10`.
- ถ้า getter/marker ให้ vtable หลาย candidate ใช้ RTTI เป็น escape hatch เฉพาะ candidate เดียวที่ `vtable[-4]` ชี้ primary x86 MSVC Complete Object Locator แบบครบโครงสร้าง, ทุกช่วงไบต์ที่อ่านอยู่ครบภายใน PE section เดียว, self BaseClassDescriptor ย้อนกลับ TypeDescriptor เดิม และชื่อเต็มตรง `.?AV<registry-name>@@` ทุกตัวอักษร; ไม่ใช้ชื่อใกล้เคียงหรือระยะห่างของสตริง.
- ถ้า vtable ยังแยกไม่ได้ จะคง vtable เป็น `UNKNOWN`; serializer หรือ handler แยกเป็นค่าที่พิสูจน์ได้เฉพาะเมื่อ slot นั้นมี executable VA ค่าเดียวกันใน candidate getter/marker ครบทั้ง census และ table 0x20 ไบต์ของทุก candidate อยู่ครบใน PE section เดียว โดยบันทึก pointer file offset ทุก candidate.
- อ่าน serializer และ handler จาก `+0x18` และ `+0x1C`; ช่องที่ไม่เป็น executable VA หรือไม่เอกฐานเป็น `UNKNOWN`.
- คอลัมน์ `file_off_*` ระบุตำแหน่งไบต์ของ registration, name, getter, vtable และ pointer slots เพื่อให้ตรวจทุกข้ออ้างจาก image ได้ตรงจุด; หลาย offset ในหนึ่งช่องคั่นด้วย `|`.

## จำนวน

- protocol: 519
- getter UNKNOWN: 15
- vtable UNKNOWN: 17
- serializer UNKNOWN: 16
- handler UNKNOWN: 15
- exact RTTI vtable disambiguation: 1
- candidate-invariant serializer: 1
- candidate-invariant handler: 2
- image SHA-256: `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`

## หลักฐาน RTTI ที่ใช้แก้ความกำกวม

- `PcThreadRunObject`: `rtti_vtable_name_match vtable=0x00F86F04 file_off=0x00B85304 locator_pointer_file_off=0x00B85300 locator=0x00FCCFB8 locator_file_off=0x00BCB3B8 type_descriptor=0x0101E768 type_descriptor_file_off=0x00C1BF68 type_name_file_off=0x00C1BF70 hierarchy=0x00FCCFCC hierarchy_file_off=0x00BCB3CC base_array=0x00FCCFDC base_array_file_off=0x00BCB3DC self_base=0x00FCCFF0 self_base_file_off=0x00BCB3F0 basis=exact_primary_msvc_x86_col_and_full_class_name`

## หลักฐานค่าคงที่ข้าม vtable candidate

- `ItemAttr` serializer: `candidate_invariant_serializer candidate_count=2 vtables=0x00F0EBB0|0x00F4A188 pointer_file_offs=0x00B0CFC8|0x00B485A0 value=0x0043BB80 basis=complete_same_section_getter_marker_census`
- `ItemAttr` handler: `candidate_invariant_handler candidate_count=2 vtables=0x00F0EBB0|0x00F4A188 pointer_file_offs=0x00B0CFCC|0x00B485A4 value=0x0046B530 basis=complete_same_section_getter_marker_census`
- `VitalData` handler: `candidate_invariant_handler candidate_count=2 vtables=0x00F0B930|0x00F375FC pointer_file_offs=0x00B09D4C|0x00B35A18 value=0x00B3798C basis=complete_same_section_getter_marker_census`

## เหตุผล UNKNOWN

- `getter_hits=0`: 15
- `vtable_hits=2`: 2
