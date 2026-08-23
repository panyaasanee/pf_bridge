[ถึง: chief cloud (cc) และ Panya · จาก: ผู้เทส LOCAL / คนหน้าเครื่องสะพาน]

# GT-054 SPAN-VERIFY-EXTERNAL-REGISTRY — RESULT

- เวลา: 2026-08-24 00:33:39 +07:00
- สถานะที่เสนอ: `[PASS]` / `[DONE]`
- ลักษณะงาน: static บนสะพานเท่านั้น; ไม่เปิดเกม, ไม่บูต server/client, ไม่จับ `LOCK_GAME`, ไม่แตะ canonical DB
- server clone commit ที่รัน: `1e0b20bd240b27f9a234ff0e4f3a45a353d7634e` (`main`; `git pull --ff-only` ตอบ `Already up to date`)
- ยืนยัน tool หลัง pull: `tools\pf_external_registry.py` มีจริง

## ช่องค้นบังคับ

- ค้นใน `pf_bridge\external\` แล้ว: **เจอ** `PF_SERIALIZER_FIELDS.tsv` ซึ่งมี `span_start`, `span_end`, `span_sha256` และเป็น object under test ของใบนี้
- ค้น gamedata แล้ว: **ไม่เจอ** ตารางหรือข้อมูล span/registry ที่ตอบใบนี้; พบเพียง `gamedata\00_SEARCH_HERE_FIRST.md` อ้างกลับไปยัง `external\PF_SERIALIZER_FIELDS.tsv` เพื่อย้ำว่า gamedata ไม่ใช่ชั้น wire

## คำสั่งและผล

รันครั้งเดียวตาม exact-command variant ที่ให้ JSON:

```text
py -3 tools\pf_external_registry.py --verify-spans ..\GameClient\GameClient.local.bin --json
```

ผลเต็ม:

```json
{
  "image": "..\\GameClient\\GameClient.local.bin",
  "image_sha256": "9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623",
  "distinct_spans": 392,
  "verified": 392,
  "mismatched": 0,
  "unreadable": 0,
  "mismatched_spans": [],
  "unreadable_spans": []
}
```

- exit code: `0`
- บรรทัดสรุปเต็ม: `spans=392 verified=392 mismatched=0 unreadable=0`
- image_sha256: `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`
- คำตัดสินชั้น artifact / wire-equivalent: span ทั้ง 392 distinct spans ตรงกับไบต์จริงในอิมเมจ; ไม่มี mismatch และไม่มี span ที่อ่านไม่ได้
- ชั้น client-observable / human screen: ว่างเปล่าโดยเจตนา — ใบ static นี้ไม่มีเกมและไม่มีข้อสังเกตบนจอ

## SHA256 ก่อน → หลัง

ทุกไฟล์ตรงกัน; ไม่มี input ใดเปลี่ยน:

| ไฟล์ | bytes | ก่อน | หลัง |
|---|---:|---|---|
| `GameClient\GameClient.local.bin` | 14,759,424 | `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623` | `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623` |
| `external\PF_PROTOCOL_REGISTRY.tsv` | 89,506 | `27daac0c6fbbc45d88281c31b98e3a8b56f421bd1e8bc16f970fdff5716cfb4d` | `27daac0c6fbbc45d88281c31b98e3a8b56f421bd1e8bc16f970fdff5716cfb4d` |
| `external\PF_SERIALIZER_FIELDS.tsv` | 25,195,473 | `99282bdf3f492eaebdbab4918aecc0e37bf8efb42b904b18e1ba306767b5c123` | `99282bdf3f492eaebdbab4918aecc0e37bf8efb42b904b18e1ba306767b5c123` |
| `external\PF_RUNTIME_CLASSMAP.tsv` | 1,947,472 | `c53a6eaf23911765ebabd5e86ccaecf827ffdd88a1f514fc3f0f3ea2c3484985` | `c53a6eaf23911765ebabd5e86ccaecf827ffdd88a1f514fc3f0f3ea2c3484985` |
| `external\PF_FIELD_VALIDATION.tsv` | 72,849 | `080a5f32580df575632fee69d3f8faa6e2e745ad1775d05daf3e272e4e0941c3` | `080a5f32580df575632fee69d3f8faa6e2e745ad1775d05daf3e272e4e0941c3` |
| `external\PF_INPUT_INVENTORY.tsv` | 364,080 | `729b5e73383de8fd6e0008875d4b9b685de2ad8d72a55118aa862093f10259d1` | `729b5e73383de8fd6e0008875d4b9b685de2ad8d72a55118aa862093f10259d1` |
| `tools\pf_external_registry.py` | 24,500 | `e9a4e202afe79699e05671b210c59ba99bf574129c1a6f1a6880e41cf7573fce` | `e9a4e202afe79699e05671b210c59ba99bf574129c1a6f1a6880e41cf7573fce` |

## Nonclaims

- ผลผ่านนี้พิสูจน์เฉพาะว่าไบต์ของ 392 spans ตรงกับ `span_sha256`; **ไม่ได้พิสูจน์ความหมายของฟิลด์**
- ไม่พิสูจน์ว่า client ส่งแถว `W` จริง; แถว `W` บอกเพียงว่า serializer มีทางเขียนฟิลด์
- ครอบเฉพาะ 392 spans ของ 503 known-serializer messages; 16 UNKNOWN-serializer messages และ 32 spanless field rows ไม่มี span ให้ verify โดยเจตนา
- ไม่ claim พฤติกรรม runtime, สิ่งที่เห็นบนจอ, หรือพฤติกรรมของเซิร์ฟเวอร์ต้นฉบับซึ่งปิดไปแล้ว

## สภาพหลังจบ

- SHA ของอิมเมจและ TSV ที่พึ่งตรงก่อน/หลังทั้งหมด
- server clone worktree สะอาดหลังรัน
- ไม่ได้สร้างสคริปต์ระหว่างทาง และไม่ได้แก้ queue/continuation/source/test/tool ใด
