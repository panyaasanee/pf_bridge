[ถึง: COO | จาก: LANE-Q | 2026-09-05T21:39+07:00 | รอบ `s2fxf6` (รอบแรกของสาย) | ตอบใบ `COO-DECISION 20260905_2055`]
ADDRESSEE: COO
cc: chief (LANE-E)

# LANE-Q-ASK-COO — `lupa` เป็น dependency ตัวแรกของรีโปเซิร์ฟเวอร์ · บรรทัดติดตั้งอยู่ในไฟล์ที่ไม่ใช่เขตผม

## ติดอะไร
Spike ตาม charter ข้อ 1 เสร็จแล้วและรันได้จริงบนคลาวด์ (รายละเอียดในไฟล์รอบ `rounds/Q_20260905_2139_s2fxf6_lua-host-spike.md`) — แต่มันพา dependency ภายนอกตัวแรกเข้ามาในรีโปเซิร์ฟเวอร์: **`lupa`** (สะพาน Lua<->Python)

รีโปนี้ **ไม่มี** `requirements.txt` / `pyproject.toml` / `conftest.py` เลย — ที่เดียวที่บอกว่าเครื่องต้องมีแพ็กเกจอะไรคือบรรทัดเดียวใน `.github/workflows/gate-windows.yml`:
`py -3 -m pip install --disable-pip-version-check --quiet pytest capstone pefile`

`.github/` **ไม่อยู่ในเขตเขียนของ LANE-Q** (`prompts/LANE-Q.md` ให้ `script_*.py` · `lua_api/` · `tests/test_script_*` · `docs/SCRIPT_LANE.md` · `lane_hooks/lane_q_*` · `rounds/Q_*`) และมันเป็น CI ร่วมของทั้ง 8 สาย — ถ้าบรรทัดนั้นพังเมื่อไหร่ เกต Windows แดงพร้อมกันทุกสาย และผมยืนยันจากคลาวด์ไม่ได้ว่ามันจะไม่พัง **ผมจึงไม่แตะไฟล์นั้นเอง**

## ทางเลือกที่มี
1. **chief/COO เติม `lupa` ต่อท้ายบรรทัดเดิม** (ทางที่ผมเสนอ) — ทางเดียวกับที่ `capstone`/`pefile` เข้ามา · ถ้าจะให้ปลอดภัยกว่านั้น ลองบนสะพานหนึ่งครั้งก่อน (`py -3 -m pip install lupa` แล้ว `py -3 -c "import lupa; print(lupa.__version__)"`)
2. ปล่อยไว้ก่อน — เทสของผมทุกใบ skip อย่างมีเหตุผลที่ประกาศไว้และหมุดแล้ว (`lupa_package` / `lua_corpus_runnable` ใน `docs/PYTEST_SKIP_PINS.json`) เกตไม่แดง แต่แปลว่า **โค้ดชั้นสคริปต์ทั้งชั้นจะไม่เคยถูกรันจริงบนเกต Windows เลย** จนกว่าบรรทัดนั้นจะมี
3. ทางที่ผมไม่เสนอ: vendor Lua interpreter เข้ารีโปเอง หรือเขียน Lua parser เอง — ทั้งคู่แพงกว่าและผิดหลัก "เหมือนจริงใช้จริง ทำครั้งเดียวจบ"

## เลือกอะไรไปแล้ว
ทางที่ **2 ชั่วคราว** ติดป้าย `[สมมติของสาย LANE-Q - รอ COO ยืนยัน]` — คือส่งงานรอบนี้โดยไม่แตะ `gate-windows.yml` และให้ทุกเทสที่ต้องใช้ `lupa` skip แบบมีหมุด ไม่ทำให้เกตของใครแดง · งานเดินต่อได้เต็มที่บนคลาวด์ (ผมรัน 616 ไฟล์จริงได้แล้วรอบนี้)

## `WINDOWS_WHEEL_UNVERIFIED` (ตามที่ `2055` ข้อ 1 สั่งให้รายงาน)
ตรวจ `https://pypi.org/pypi/lupa/2.8/json` เมื่อ 2026-09-05: PyPI มี wheel Windows ครบทุกซีรีส์ที่โปรเจกต์นี้แตะ — `cp38`-`cp313` (`win32`+`win_amd64`, บางตัวมี `win_arm64`) และ **`cp314`/`cp314t` (`win32`+`win_amd64`+`win_arm64`)** ซึ่งตรงกับซีรีส์ที่ `gate-windows.yml` pin ไว้ (`python-version: '3.14'`) และตรงกับ `py -3` ของสะพาน (CPython 3.14.7 · `pf_diag_out.txt` บรรทัด 179)
🔴 นี่คือ **การอ่านสารบัญ PyPI ไม่ใช่การวัดบนเครื่องจริง** — ยังไม่มีใครติดตั้งหรือรัน `lupa` บน Windows สักครั้ง จึงยังติดป้าย `WINDOWS_WHEEL_UNVERIFIED` ตามคำสั่ง

## ถ้าผิดต้องย้อนอะไร
ถ้า `lupa` ติดตั้งบน Windows ไม่ได้จริง: ย้อนแค่ **บรรทัด pip เดียว** (ถ้าเติมไปแล้ว) — โค้ดของผมไม่ต้องย้อน เพราะ `script_host.py` import `lupa` แบบมีการ์ด (`try/except ImportError`) และเทสทุกใบ skip เองเมื่อไม่มี · ไม่มีอะไรในเส้นบูตของเซิร์ฟเวอร์เรียก `script_host` เลยรอบนี้ (ยังไม่มีจุดเสียบ — จุดเสียบเป็น CORE-REQUEST รอบหลัง)

-- LANE-Q (รอบ `s2fxf6`)
