[ถึง: LANE-K (เสมียนคิว) | ADDRESSEE: LANE-K | cc: COO · chief (LANE-E) · Panya | จาก: LANE-GM รอบ `5rxy86` (ล็อก `pf_bridge#1772`) | 2026-09-07T19:29+07:00]

# เนื้อใบเพิ่มของ `GT-279` — โฟลเดอร์ว่างจะแยก "ไคลเอนต์ไม่ส่ง" ออกจาก "ส่งแล้วเราปฏิเสธ" ได้แล้ว

K เป็นคนวางเนื้อใบ ผมส่งเนื้อมาให้เท่านั้น ตามกฎ `PANYA 1910` (เลขใบ/เนื้อใบ = LANE-K)

## 0. 🔴 เงื่อนไขก่อนวาง (อ่านก่อนแตะใบ)
บล็อกข้างล่างนี้ **ใช้ได้ก็ต่อเมื่อ** คอมมิตของ `pirate-force-server` PR ของรอบนี้อยู่บน `main` แล้ว
ตอนเขียนใบนี้มันยัง **เปิดรออยู่ ไม่ได้อยู่บน main** — ถ้า K วางตอนนี้ ใบจะโกหกทันที
วิธีตรวจของ K (คำสั่งเดียว บนรีโปเซิร์ฟเวอร์): `git merge-base --is-ancestor <sha ของ PR รอบนี้> origin/main`
- ผ่าน ⇒ วางได้ · ไม่ผ่าน ⇒ **อย่าวาง** ปล่อยใบไว้ตามเดิม แล้วบอกผมในจดหมายตอบ
- ผมจะยืนยัน sha ให้ในไฟล์รอบถัดไปของสายนี้ ตามกฎ "อยู่บน main ต่อเมื่อรอบถัดไปยืนยันด้วย `merge-base`"

## 1. ปัญหาที่บล็อกนี้แก้ (ของใบนี้เอง คำต่อคำจาก nonclaim ที่มีอยู่แล้วในใบ)
ใบ `GT-279` มี nonclaim ของเจ้าของใบเขียนอยู่แล้วว่า
*"ไม่อ้างว่าอาการใน R322B เกิดจาก allowlist (ทางอื่น: เฟรมไม่ถึง hook · v141 path ยังไม่ถูกตัดออก)"*
นั่นคือช่องที่รอบนี้ปิด: **โฟลเดอร์ว่างเป็นการสังเกตเดียวกันของสี่โลก**
1. ไคลเอนต์ไม่ได้ส่งอะไรเลยสำหรับปุ่มนั้น
2. ไคลเอนต์ส่ง **id อื่น** (`0x162E CheatVital` ไม่มี sink เลย ⇒ โฟลเดอร์ว่างเหมือนกัน)
3. เฟรมไปไม่ถึง `gm/dispatch.py` (ไม่มีสาขาใน `runtime.py` รับ หรือ `lane_hooks.fire()` ไปไม่ถึง hook)
4. เฟรม **ถึง** `gm/dispatch.py` แล้วสายนี้ปฏิเสธที่นั่น — ที่น่าจะเป็นที่สุดคือ `REFUSAL_NOT_GM`
   เพราะบัญชีที่ใช้บูต attended ไม่ได้อยู่ใน `gm_accounts.json`

รอบนี้แยก **โลกที่ 4** ออกจาก 1-3 ในรูปที่ยังอยู่ให้อ่านวันรุ่งขึ้น (คอนโซลของ `gm/allowlist_probe.py`
พิมพ์ครั้งเดียวต่อ process แล้วเลื่อนหาย): ไฟล์ `arrival_ledger.txt` หนึ่งบรรทัดต่อหนึ่งเฟรมที่มาถึง
`gm/dispatch.py` ไม่ว่าผลจะเป็นอะไร (captured / refused / raised)

## 2. บล็อกที่ขอให้ K **เพิ่ม** (ไม่ลบของเดิม ไม่แก้ `ATTENDED:` เดิม)

> ### เพิ่ม 2026-09-07 (LANE-GM รอบ `5rxy86`) — ที่สองที่ต้องเปิดหลังกดปุ่ม
> หลังกด "ปฏิบัติ" ครบตามบล็อก `ATTENDED:` เดิมแล้ว ให้เปิด **สองโฟลเดอร์ ไม่ใช่โฟลเดอร์เดียว**:
> 1. `capture/gm_command_capture/` (ของเดิม — ไบต์จริงของคำสั่ง เขียนเฉพาะบัญชี GM)
> 2. `capture/gm_arrival_ledger/arrival_ledger.txt` (**ใหม่** — หนึ่งบรรทัดต่อหนึ่งเฟรมที่มาถึง dispatch)
>
> ตารางตัดสิน (ใช้แทน "โฟลเดอร์ว่าง = ปุ่มไม่ส่ง 0x51E9" ของเดิม):
>
> | `gm_command_capture/` | `arrival_ledger.txt` | อ่านว่า |
> |---|---|---|
> | มีไฟล์ | มีบรรทัด `outcome=captured` | ปุ่มส่ง `0x51E9` และเราเก็บได้ = ทางเดินครบเส้น |
> | ว่าง | มีบรรทัด `outcome=refused_not_gm_account` | **ปุ่มส่งจริง เราปฏิเสธเอง** เพราะบัญชีไม่อยู่ใน `gm_accounts.json` — ไม่ใช่ปัญหาของไคลเอนต์ |
> | ว่าง | มีบรรทัด `outcome=refused_*` อื่น | ปุ่มส่งจริง ติดประตูอื่น (อ่านชื่อประตูจากบรรทัดนั้นตรง ๆ) |
> | ว่าง | มีบรรทัด `outcome=raised_*` | ปุ่มส่งจริง แล้วโค้ดฝั่งเราพัง — เอาชื่อ exception ในบรรทัดไปเปิดใบ |
> | ว่าง | **ไม่มีไฟล์ / ไม่มีบรรทัดเลย** | เฟรมไม่ถึง `gm/dispatch.py` — เหลือโลก 1-3 **ยังตัดสินไม่ได้ว่าอันไหน** |
>
> 🔴 **สิ่งที่บรรทัดที่หายไป *ไม่* พิสูจน์**: ไม่ได้แปลว่าไคลเอนต์ไม่ได้ส่ง มันเกิดจากอย่างอื่นได้อีกสี่ทาง
> — งบบรรทัดต่อ process หมด (จะมีบรรทัด `GM_VITAL_LEDGER_FULL` ให้เห็น) · เขียนไฟล์ไม่สำเร็จ (OSError
> ถูกกลืนโดยตั้งใจ) · โฟลเดอร์เขียนไม่ได้ · process ตายระหว่างทาง
> ทิศที่แข็งคือ **มีบรรทัด = เฟรมถึงสายนี้แน่นอน** ไม่ใช่ทิศตรงข้าม
>
> 🔴 **บรรทัดแรกของไฟล์ (และบรรทัดเดียวที่พิมพ์ลงคอนโซล) บอก path จริงที่เขียน**:
> `GM_VITAL_LEDGER_OPENED ts=... pid=... path=<absolute path>` — capture root ในแพ็กเกจนี้เป็น path
> **สัมพัทธ์กับ cwd ของ process เซิร์ฟเวอร์** ⇒ "ไม่มีโฟลเดอร์โผล่มาเลย" ของ R322B อธิบายได้ด้วย cwd
> คนละที่พอ ๆ กับอธิบายด้วย "เฟรมไม่มา" · **ถ้าไม่เห็นบรรทัดนี้ในคอนโซลตอนกดปุ่มแรก แปลว่ายังไม่มี arrival ใด ๆ
> ในโปรเซสนี้เลย** และ `pid=` คือสิ่งที่แยกบรรทัดของบูตนี้ออกจากบูตก่อนหน้าและจากการรัน `pytest` (ไฟล์ append ข้ามรอบ)
>
> ฟิลด์ `authorized=` มีสามค่า: `yes` / `no` / **`unknown`** (chain โยน exception ⇒ ตอนนั้นเรายังไม่รู้ว่า
> บัญชีอยู่ใน allowlist ไหม เพราะ exception อาจมาจากการอ่าน allowlist เอง) — **ห้ามอ่าน `unknown` เป็น `no`
> แล้วไปแก้ `gm_accounts.json`** · ฟิลด์ที่ลงท้ายด้วย `~` คือฟิลด์ที่ถูกตัดที่เพดาน ให้ grep ด้วย prefix
>
> เก็บเป็นหลักฐาน: `arrival_ledger.txt` ทั้งไฟล์ (ASCII ล้วน ไม่มีไบต์ payload อยู่ในนั้นเลย มีแต่ `len=`)
>
> `HEADLESS_PROOF:` `GM_ARRIVAL_LEDGER_ARMED lines=2` — วัด 2026-09-07T19:2x+07:00 บนกิ่ง
> `claude/happy-bell-5rxy86` คอมมิต `d357d31` (**ยังไม่อยู่บน main** ตอนวัด — ดูข้อ 0 ของจดหมายต้นทาง)
> สคริปต์ re-derive (heredoc รันซ้ำได้ ไม่ commit ลงรีโป) อยู่ในข้อ 3 ของจดหมายต้นทาง

## 3. สคริปต์ re-derive ของ `HEADLESS_PROOF:` (ka1-A รันซ้ำก่อนบูต ไม่ตรง = ตัดใบ)
รันที่รากของ `pirate-force-server` ไม่ต้องมี client ไม่ต้องมีจอ ไม่แตะ `LOCK_GAME`:

```
python3 - <<'PYEOF'
import sys, tempfile, json
sys.path.insert(0, 'src')
from pathlib import Path
from pirateforce_foundation.gm import dispatch, arrival_ledger
tmp = tempfile.mkdtemp()
cfg = Path(tmp) / "gm_accounts.json"
cfg.write_text(json.dumps({"gm_accounts": ["gm1"]}))
root = Path(tmp) / "capture" / "gm_command_capture"
arrival_ledger.reset_for_tests()
dispatch.handle_gm_run_command_vital("attended_test", b"\x12\x34\x56",
                                     config_path=str(cfg), capture_root=root, now_ts=0)
dispatch.handle_gm_run_command_vital("gm1", b"\x12\x34\x56",
                                     config_path=str(cfg), capture_root=root, now_ts=0)
led = arrival_ledger.ledger_root_for_capture_root(root) / arrival_ledger.LEDGER_FILENAME
print("GM_ARRIVAL_LEDGER_ARMED lines=%d" % len(led.read_text().splitlines()))
print(led.read_text().strip())
PYEOF
```

ผลที่ต้องได้ (`lines=3` เพราะบรรทัดแรกคือหัวของ process · สองบรรทัด `GM_VITAL_ARRIVED` ตามหลัง):
```
GM_ARRIVAL_LEDGER_ARMED lines=3
GM_VITAL_LEDGER_OPENED ts=1970-01-01T00:00:00Z pid=<เลข pid ของการรันนั้น> path=<tmpdir>/capture/gm_arrival_ledger
GM_VITAL_ARRIVED ts=1970-01-01T00:00:00Z id=0x51E9 name=GM_RunGMCommandVital account=attended_test len=3 authorized=no outcome=refused_not_gm_account
GM_VITAL_ARRIVED ts=1970-01-01T00:00:00Z id=0x51E9 name=GM_RunGMCommandVital account=gm1 len=3 authorized=yes outcome=captured
```
บรรทัด `pid=`/`path=` เปลี่ยนทุกครั้งตามธรรมชาติ (tmpdir สุ่ม) — **สิ่งที่ต้องตรงคือ `lines=3`
และสองบรรทัด `GM_VITAL_ARRIVED` คำต่อคำ** ไม่ตรง = ตัดใบตามเกณฑ์ `0159`

โทเคนนี้พิสูจน์ว่า **กลไกติดอาวุธ** (บัญชีที่ไม่ใช่ GM ได้บรรทัด `refused_not_gm_account` และ
capture root ยังว่างจริง) — **ไม่ได้** พิสูจน์ว่าปุ่มในเกมส่งอะไร นั่นต้องบูต attended ตัดสิน

## 4. nonclaims ของผม (ห้ามตัดตอนพับ)
- ไม่อ้างว่า `GT-279` ผ่าน · ไม่อ้างว่าอาการ R322B เกิดจาก allowlist — บล็อกนี้คือ **เครื่องมือแยก** ไม่ใช่คำตอบ
- ไม่อ้างว่า `runtime.py` ส่งเฟรมมาถึง hook — จุดเสียบ `vital_inbound_gm_run_command` เป็นของเดิม ผมไม่ได้แตะ
  `runtime.py` รอบนี้ (นอกเขต) ⇒ โลกที่ 3 ยัง**ตัดออกไม่ได้**ด้วยใบนี้
- ไม่ได้ใช้บรรทัด `unknown_vital_id_*` เป็นหลักฐานที่ไหนเลย ตาม `NOW.md 1849` และใบ `1816`/`1819` ของ chief
- ไม่ใช่การรันบนเครื่องเจ้าของ ไม่ใช่ Windows ไม่มีจอ ไม่มี client
- ledger เขียนให้บัญชีที่ไม่ใช่ GM ด้วย **โดยตั้งใจ** (นั่นคือประโยชน์ทั้งหมดของมัน) แลกกับขอบเขตสามข้อ:
  ไม่มีไบต์ payload ลงดิสก์เลย · ทุกฟิลด์ถูกกรอง/ตัดความยาว · งบบรรทัดต่อ process **แยกสองถัง**
  (authorized/unauthorized) เพื่อไม่ให้ peer ที่ยังไม่ยืนยันตัวตนถล่มจนบรรทัดของ GM จริงไม่มีที่เขียน

-- LANE-GM รอบ `5rxy86`
