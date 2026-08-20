# FACTPACK R106 - บัญชีวัดจริงของ 42 โมดูลที่ CI ซ่อนด้วย --ignore

## 0. ไฟล์นี้มีอยู่ทำไม

GitHub Actions run #3 (2026-08-20) เป็นครั้งแรกในประวัติโปรเจกต์ที่ gate ได้รันบน
เครื่องที่สอง (fresh clone, windows-latest) และ pytest แดง 4 ตัวเพราะเทสไปคว้าหลักฐาน
ที่อยู่นอก git. workflow `.github/workflows/gate-windows.yml` แก้ปัญหานั้นด้วยการตัด
โมดูลออกจาก pytest ทั้งไฟล์ ด้วย heuristic บรรทัดเดียว (บรรทัด 374-378):

```
$excluded = @(
  Select-String -Path 'tests\*.py' -Pattern 'GameClient|capture_v141' -List |
    ForEach-Object { 'tests/' + (Split-Path $_.Path -Leaf) } |
    Sort-Object -Unique
) | Where-Object { $_ -ne 'tests/test_foundation_legacy_seam.py' }
```

ผลคือ 42 โมดูลหายไปจาก runner. Panya ตัดสินเมื่อ 2026-08-20 ~15:45 ว่าท่าที่ถูกคือ
"ให้เทสประกาศ precondition ของตัวเองแล้ว skip" ไม่ใช่ให้ CI ซ่อน เพราะ `--ignore`
ทำให้เทสหายเงียบ ๆ ในขณะที่ตัวเลขรวมยังดูเหมือนเดิม. รอบ 106 (chief) แก้ 4 เทสที่แดงจริง
ไปแล้ว และวางโครง `tests/pf_preconditions.py` + `tools/pf_pytest_precondition_census.py`
+ `docs/PYTEST_SKIP_PINS.json` ไว้แล้ว.

**Stage B คือเลิกใช้ `--ignore` ทั้ง 42 โมดูล** และไฟล์นี้คือบัญชีวัดจริงเพื่อให้รอบถัดไป
หยิบไปทำได้ทันที โดยไม่ต้องวัดใหม่. ทุกตัวเลขในไฟล์นี้ได้จากการ **รันจริง** ไม่ใช่ grep.

## 1. วัดเมื่อไหร่ ที่ไหน ด้วยอะไร

| หัวข้อ | ค่า |
|---|---|
| วันที่วัด | 2026-08-20 |
| HEAD | `7f893b8` (round 105) |
| ต้นทาง | fresh clone จริง (`git clone` เต็ม history) วางไว้ที่ `/tmp/fc2` ใน Linux sandbox |
| OS / interpreter | Linux, CPython **3.10.12** (เครื่องจริงคือ Windows + CPython 3.14 - ดู NONCLAIMS) |
| แพ็กเกจ | pytest, pytest-subtests, capstone, pefile ติดตั้งครบ |
| artifact ที่มี | **ไม่มีสักตัว** - ทั้ง 7 คีย์ใน REGISTRY ตอบ ABSENT |
| ห้ามทำ | ไม่ได้รัน pytest จาก mount ของ Windows เลย, ไม่แตะ canonical DB, ไม่บูต server, ไม่เปิด client |

re-derive สถานะ artifact:

```
cd /tmp/fc2 && python3 -c "
import sys; sys.path.insert(0,'tests')
import pf_preconditions as p
for k,v in p.REGISTRY.items(): print(k, 'PRESENT' if v.present else 'ABSENT')"
```

ผลที่ได้: `canonical_db backups_tree bridge_sibling capture_v141 client_image
game_install_tree login_req_capture` = ABSENT ทั้งเจ็ด.

## 2. ตัวเลขรวม (re-derivable)

คำสั่งที่ใช้เก็บฐานข้อมูลทั้งหมด (รันทีละโมดูล):

```
while read m; do b=$(basename "$m" .py)
  python3 -m pytest "$m" -v --tb=no -p no:cacheprovider \
  | grep -E "^tests/\S+::\S+ (PASSED|FAILED|ERROR|SKIPPED)|^SUBFAILED" > /tmp/v42b/$b.txt
done < /tmp/excluded.txt
```

| ตัวเลข | ค่า | ได้มาจาก |
|---|---|---|
| โมดูลที่ถูก exclude | 42 | `wc -l /tmp/excluded.txt` |
| test node ที่ collect ได้ | **890** | `python3 -m pytest $(cat /tmp/excluded.txt) --collect-only -q` |
| collection ERROR | **0** | คำสั่งเดียวกัน ไม่มี error block |
| node ที่ผ่านสะอาด | 611 | นับจาก /tmp/v42b |
| node ที่ FAILED | 180 | นับจาก /tmp/v42b |
| node ที่ ERROR (setUpClass) | 70 | นับจาก /tmp/v42b |
| node ที่ผ่านแต่มี subtest ล่ม | 7 | บรรทัด `SUBFAILED` |
| node ที่ SKIPPED อยู่แล้ว | 22 | นับจาก /tmp/v42b |
| module-level skip (ไม่ collect เลย) | 3 โมดูล = 3 skip | pytest ตอบ `1 skipped`, `0 collected` |
| **node ที่ต้องใส่ guard ใหม่** | **257** | 180 + 70 + 7 |
| skip ที่มีอยู่แล้ว | **25** | 22 node-level + 3 module-level |

**ข้อสำคัญเรื่องการนับ:** สรุปท้าย `pytest -q` นับ subtest ที่ล่มเป็น "failed" เพิ่มอีกหนึ่ง
บรรทัดต่อ node ทำให้ตัวเลขในสรุป `-q` สูงกว่าจำนวน node จริง (เช่น
`test_capture_corpus` สรุปว่า "10 failed" แต่มี node ที่เกี่ยวข้องแค่ 5).
ตัวเลขในไฟล์นี้เป็น **node-level** ทุกจุด และผลรวม 611+7+180+70+22 = 890 ตรงกับ
`--collect-only` พอดี.

### การวัดสภาพปลายทาง (Stage B ทำเสร็จโดยไม่แก้โค้ดเลย)

```
cd /tmp/fc2
python3 -m pytest tests -q -rs -p no:cacheprovider --tb=no > /tmp/full_noignore.txt
: > /tmp/empty.txt
python3 tools/pf_pytest_precondition_census.py --report /tmp/full_noignore.txt --excluded /tmp/empty.txt
```

- pytest: `193 failed, 1562 passed, 29 skipped, 70 errors, 3346 subtests passed`
- โมดูลเดียวที่แดงและ **ไม่ได้** อยู่ใน 42 คือ `tests/test_server_shutdown.py`
  (เป็นผลของ py3.10 ใน sandbox เรื่อง `__notes__` ซึ่งเป็นของ 3.11+ - **ไม่ใช่ปัญหาของรีโป**
  และไม่นับในเอกสารนี้). แปลว่า ignore list 42 ตัวครอบคลุมชุดที่แดงจริงพอดี ไม่ขาดไม่เกิน.
- census: `RESULT: FAIL` โดยมี 8 ปัญหา **ทั้งหมดเป็นชนิด `UNDECLARED SKIP`** ไม่มี PIN DRIFT
  และไม่มี unknown key เลย. รายละเอียดอยู่หัวข้อ 5.

## 3. ตารางหลัก - 42 แถว

คอลัมน์ `guard ที่เสนอ` ใช้กติกา: ถ้าโมดูลมีเทส pure-stdlib ที่รันผ่านได้โดยไม่มี artifact
**ห้าม** module-level. คอลัมน์ `skip` คือจำนวน skip event ที่จะเกิดบน fresh clone ถ้าใส่ guard
ตามที่เสนอ (นี่คือเลขที่จะกลายเป็น pin).

| # | module | collect ok | pass | fail | err | subF | skip เดิม | artifact ที่ต้องการจริง | ระดับ guard ที่เสนอ | skip ที่จะเกิด |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | tests/test_action_consumer_probe.py | ใช่ (10) | 8 | 2 | 0 | 0 | 0 | client_image_original (1), game_install_tree (1) | method x2 | 2 |
| 2 | tests/test_action_producer_probe.py | ใช่ (9) | 8 | 1 | 0 | 0 | 0 | game_install_tree | method x1 | 1 |
| 3 | tests/test_actor_type_dispatch_static.py | ใช่ (37) | 7 | 29 | 0 | 1 | 0 | client_image | class x6 + method x3 | 30 |
| 4 | tests/test_behavior_entry_probe.py | ใช่ (6) | 4 | 2 | 0 | 0 | 0 | client_image_original (1), game_install_tree (1) | method x2 | 2 |
| 5 | tests/test_behavior_lookup_probe.py | ใช่ (7) | 4 | 3 | 0 | 0 | 0 | client_image_original (2), game_install_tree (1) | method x3 | 3 |
| 6 | tests/test_behavior_range_gate_probe.py | ใช่ (7) | 5 | 2 | 0 | 0 | 0 | client_image_original (1), game_install_tree (1) | method x2 | 2 |
| 7 | tests/test_capture_corpus.py | ใช่ (19) | 14 | 2 | 0 | 3 | 0 | capture_v141 + backups_tree + analysis_tree | method x5 | 5 |
| 8 | tests/test_channel_message_hypothesis.py | ใช่ (40) | 40 | 0 | 0 | 0 | 0 | **ไม่ต้องการเลย** | ไม่ต้องแก้ | 0 |
| 9 | tests/test_chat_channel_family_static.py | ใช่ (0 - ข้ามทั้งโมดูล) | 0 | 0 | 0 | 0 | 1 | client_image | มี module-level อยู่แล้ว | 1 |
| 10 | tests/test_client_ui_asset_inventory.py | ใช่ (14) | 12 | 0 | 0 | 0 | 2 | game_install_tree | มี class-level อยู่แล้ว | 2 |
| 11 | tests/test_damage_hit_result_static.py | ใช่ (56) | 3 | 53 | 0 | 0 | 0 | client_image | class x10 + method x6 | 53 |
| 12 | tests/test_damage_hp_link_hypothesis.py | ใช่ (141) | 141 | 0 | 0 | 0 | 0 | **ไม่ต้องการเลย** | ไม่ต้องแก้ | 0 |
| 13 | tests/test_damage_model_hypothesis.py | ใช่ (102) | 102 | 0 | 0 | 0 | 0 | **ไม่ต้องการเลย** | ไม่ต้องแก้ | 0 |
| 14 | tests/test_delete_refresh_hypothesis.py | ใช่ (16) | 16 | 0 | 0 | 0 | 0 | **ไม่ต้องการเลย** | ไม่ต้องแก้ | 0 |
| 15 | tests/test_delete_refresh_static.py | ใช่ (8) | 0 | 0 | 0 | 0 | 8 | client_image | มี class-level อยู่แล้ว | 8 |
| 16 | tests/test_equip_state_static.py | ใช่ (6) | 1 | 5 | 0 | 0 | 0 | client_image_original | method x5 | 5 |
| 17 | tests/test_hit_result_probe.py | ใช่ (9) | 6 | 3 | 0 | 0 | 0 | client_image_original (2), game_install_tree (1) | method x3 | 3 |
| 18 | tests/test_hp_death_erratum.py | ใช่ (16) | 16 | 0 | 0 | 0 | 0 | **ไม่ต้องการเลย** | ไม่ต้องแก้ | 0 |
| 19 | tests/test_hp_death_respawn_static.py | ใช่ (36) | 16 | 19 | 0 | 1 | 0 | client_image | class x4 + method x6 | 20 |
| 20 | tests/test_image_query_runner.py | ใช่ (12) | 12 | 0 | 0 | 0 | 0 | **ไม่ต้องการเลย** | ไม่ต้องแก้ | 0 |
| 21 | tests/test_item_move_consumer_static.py | ใช่ (3) | 0 | 3 | 0 | 0 | 0 | client_image_original | class x1 (ทั้งโมดูล) | 3 |
| 22 | tests/test_item_order_static.py | ใช่ (3) | 1 | 2 | 0 | 0 | 0 | client_image_original | method x2 | 2 |
| 23 | tests/test_knockdown_consumer_probe.py | ใช่ (8) | 6 | 2 | 0 | 0 | 0 | client_image_original (1), game_install_tree (1) | method x2 | 2 |
| 24 | tests/test_login_vital_req_static.py | ใช่ (30) | 7 | 3 | 19 | 1 | 0 | client_image | class x4 + method x4 | 23 |
| 25 | tests/test_move_authority_targetpos_static.py | ใช่ (10) | 0 | 0 | 10 | 0 | 0 | client_image | class x1 (ทั้งโมดูล) | 10 |
| 26 | tests/test_names_fold003_thunk_census.py | ใช่ (25) | 20 | 0 | 0 | 0 | 5 | client_image (+ bridge_sibling แฝง) | มี method-level อยู่แล้ว | 5 |
| 27 | tests/test_relation_probe.py | ใช่ (4) | 4 | 0 | 0 | 0 | 0 | **ไม่ต้องการเลย** | ไม่ต้องแก้ | 0 |
| 28 | tests/test_remote_movement_projection_static.py | ใช่ (12) | 0 | 0 | 12 | 0 | 0 | client_image | class x1 (ทั้งโมดูล) | 12 |
| 29 | tests/test_remote_player_hypothesis.py | ใช่ (63) | 63 | 0 | 0 | 0 | 0 | **ไม่ต้องการเลย** | ไม่ต้องแก้ | 0 |
| 30 | tests/test_runtimeres_actor_entry_static.py | ใช่ (21) | 2 | 19 | 0 | 0 | 0 | client_image | class x2 + method x11 | 19 |
| 31 | tests/test_runtimeres_death_hypothesis.py | ใช่ (49) | 47 | 0 | 0 | 0 | 2 | client_image (1) + design skip (1) | มี method-level อยู่แล้ว | 2 |
| 32 | tests/test_skill_trigger_probe.py | ใช่ (7) | 5 | 2 | 0 | 0 | 0 | client_image_original (1), game_install_tree (1) | method x2 | 2 |
| 33 | tests/test_split_operate_family_static.py | ใช่ (9) | 0 | 0 | 9 | 0 | 0 | client_image | class x1 (ทั้งโมดูล) | 9 |
| 34 | tests/test_split_operate_static.py | ใช่ (9) | 0 | 0 | 9 | 0 | 0 | client_image | class x1 (ทั้งโมดูล) | 9 |
| 35 | tests/test_split_operate_verb_panels_static.py | ใช่ (11) | 0 | 0 | 11 | 0 | 0 | client_image | class x1 (ทั้งโมดูล) | 11 |
| 36 | tests/test_stats_progression_static.py | ใช่ (0 - ข้ามทั้งโมดูล) | 0 | 0 | 0 | 0 | 1 | client_image | มี module-level อยู่แล้ว | 1 |
| 37 | tests/test_structural_corpus_audit.py | ใช่ (5) | 3 | 2 | 0 | 0 | 0 | **evidence_tree (คีย์ใหม่)** | method x2 | 2 |
| 38 | tests/test_teleportcheck_0x4477_corpus.py | ใช่ (19) | 17 | 2 | 0 | 0 | 0 | backups_tree (2) + client_image (1) | method x2 | 2 |
| 39 | tests/test_ui_state_refresh_static.py | ใช่ (33) | 8 | 24 | 0 | 1 | 0 | client_image | class x5 + method x3 | 25 |
| 40 | tests/test_use_drop_sell_static.py | ใช่ (0 - ข้ามทั้งโมดูล) | 0 | 0 | 0 | 0 | 1 | client_image | มี module-level อยู่แล้ว | 1 |
| 41 | tests/test_vital_id_resolve_scope.py | ใช่ (14) | 9 | 0 | 0 | 0 | 5 | client_image | มี method-level อยู่แล้ว | 5 |
| 42 | tests/test_wait_for_pf_stage.py | ใช่ (4) | 4 | 0 | 0 | 0 | 0 | **ไม่ต้องการเลย** | ไม่ต้องแก้ | 0 |
| | **รวม** | **890 node, 0 collection error** | **611** | **180** | **70** | **7** | **25** | | | **282** |

282 = 257 (guard ใหม่) + 25 (skip ที่มีอยู่แล้ว). เมื่อรวมกับ pin เดิม 4 ตัวที่อยู่นอก 42
(canonical_db x2, backups_tree x1, login_req_capture x1) ทั้งสวีตบน fresh clone จะรายงาน
**286 skip**.

ตอบข้อ 1 ของโจทย์ให้ชัด: **ไม่มีโมดูลใดใน 42 ตัวที่พังตั้งแต่ collection.**
`--collect-only` เก็บได้ 890 node โดยไม่มี ERROR block เลย. ที่ล้มทั้งหมดล้มตอนรัน
โดยแบ่งเป็นสองแบบ: FAILED (ล้มในตัวเทส) 180 node และ ERROR ที่ `setUp`/`setUpClass`
70 node. แปลว่า **module-level `raise unittest.SkipTest(...)` ก่อน import tool
ไม่จำเป็นสำหรับโมดูลใดเลย** - ไม่มีโมดูลไหนระเบิดตอน import.

## 4. หัวข้อสำคัญที่สุด: false positive ของ heuristic - เอาออกจาก ignore ได้ฟรี

9 โมดูลนี้ **ผ่าน 100% บน fresh clone ที่ไม่มี artifact สักตัว** ไม่มี fail ไม่มี error
ไม่มี skip ไม่มี subtest ล่ม. heuristic จับมันได้เพราะคำว่า GameClient หรือ capture_v141
ปรากฏใน **คอมเมนต์/docstring** หรือใน **ชื่อไฟล์ปลอมที่เทสสร้างเองใน tempdir** เท่านั้น.
เอาออกจาก ignore ได้ทันที **โดยไม่ต้องแก้อะไรในรีโปเลย ไม่เพิ่ม skip แม้แต่ตัวเดียว
ไม่ต้องแตะ pin file**.

| module | test ที่ได้คืนมา | บรรทัดเดียวที่ heuristic จับ | ประเภท |
|---|---|---|---|
| tests/test_channel_message_hypothesis.py | 40 | บรรทัด 4: `... no network, no database, no GameClient, no UI.` | docstring "ไม่ใช้" |
| tests/test_damage_hp_link_hypothesis.py | 141 | บรรทัด 38: `No socket, no server, no GameClient, no canonical database...` | docstring "ไม่ใช้" |
| tests/test_damage_model_hypothesis.py | 102 | บรรทัด 57: `No socket, no server, no GameClient, no canonical database...` | docstring "ไม่ใช้" |
| tests/test_delete_refresh_hypothesis.py | 16 | บรรทัด 31: `... no server is booted and no GameClient is launched` | docstring "ไม่ใช้" |
| tests/test_hp_death_erratum.py | 16 | บรรทัด 32: `no network, no database, no GameClient.` | docstring "ไม่ใช้" |
| tests/test_image_query_runner.py | 12 | บรรทัด 26: `... touch no database and launch no GameClient.` | docstring "ไม่ใช้" |
| tests/test_relation_probe.py | 4 | บรรทัด 49: `path = root / "GameClient.local.bin"` | ไฟล์ปลอมใน tempdir |
| tests/test_remote_player_hypothesis.py | 63 | บรรทัด 22: `No socket, no server, no GameClient, no canonical database.` | docstring "ไม่ใช้" |
| tests/test_wait_for_pf_stage.py | 4 | บรรทัด 20: `nested = root / "capture_v141"` | โฟลเดอร์ปลอมใน tempdir |
| | **398** | | |

เรื่องตลกร้ายที่ควรบันทึกไว้: 7 ใน 9 ตัวโดนจับเพราะ docstring ประกาศว่า
**"ไม่ใช้ GameClient"** - heuristic ตัดออกเพราะประโยคที่บอกว่าตัวเองไม่ต้องการมัน.

re-derive:

```
cd /tmp/fc2
for b in test_channel_message_hypothesis test_damage_hp_link_hypothesis \
         test_damage_model_hypothesis test_delete_refresh_hypothesis \
         test_hp_death_erratum test_image_query_runner test_relation_probe \
         test_remote_player_hypothesis test_wait_for_pf_stage; do
  python3 -m pytest tests/$b.py -q -rs -p no:cacheprovider
  grep -n 'GameClient\|capture_v141' tests/$b.py
done
```

ทั้งเก้าตอบ `N passed` โดยไม่มี skipped ไม่มี failed ไม่มี error และแต่ละไฟล์ grep เจอ
บรรทัดเดียว.

## 5. โมดูลที่ป้องกันตัวเองอยู่แล้ว - เอาออกจาก ignore ได้ แต่ **ไม่ฟรี**

8 โมดูลนี้ไม่แดงเลยบน fresh clone เพราะมี guard อยู่แล้ว แต่ reason string ของมัน
**ไม่มี token `[precondition:<key>]`** ดังนั้น `tools/pf_pytest_precondition_census.py`
จะตีเป็น `UNDECLARED SKIP` และ census จะแดง. นี่คือกับดักที่รอบหน้าจะเจอทันทีที่เอา
`--ignore` ออก และเป็นเหตุผลว่าทำไม 8 โมดูลนี้ **ไม่ใช่** false positive.

วัดจริงด้วยคำสั่งในหัวข้อ 2 - census ตอบ `RESULT: FAIL` พร้อม 8 ข้อ ทั้งหมดเป็น UNDECLARED SKIP:

| module | skip | reason string ปัจจุบัน (ต้องเปลี่ยนเป็น token) | key ที่ควรใช้ |
|---|---|---|---|
| tests/test_chat_channel_family_static.py | 1 | `client binary /tmp/GameClient/GameClient.local.bin not present` | client_image |
| tests/test_stats_progression_static.py | 1 | `client binary /tmp/GameClient/GameClient.local.bin not present` | client_image |
| tests/test_use_drop_sell_static.py | 1 | `client binary not reachable: ...GameClient.local.bin` | client_image |
| tests/test_delete_refresh_static.py | 8 | `read-only client image is not available in this checkout` | client_image |
| tests/test_client_ui_asset_inventory.py | 2 | `game install tree not present beside the repository` | game_install_tree |
| tests/test_names_fold003_thunk_census.py | 5 | `the read-only client image is not at ... with sha256 9627211412AC60D5...` | client_image |
| tests/test_vital_id_resolve_scope.py | 5 | `the read-only client image ... is not present ...` | client_image |
| tests/test_runtimeres_death_hypothesis.py | 1 | `GameClient.local.bin is not available here` | client_image |
| tests/test_runtimeres_death_hypothesis.py | 1 | `runtime.py now carries the dispatcher branch` | **pin ไว้แล้ว** ใน design_skips |
| | **25** | | |

หมายเหตุสำคัญ 2 ข้อ:

1. reason string ปัจจุบัน **ฝัง path เต็มของเครื่อง** (`/tmp/GameClient/...` ที่นี่ จะเป็น
   `D:\a\...\GameClient\...` บน runner). ถ้าเปลี่ยนไปใช้ `Precondition.reason` จะได้
   string คงที่ทุกเครื่อง ซึ่งจำเป็นเพราะ census จับคู่ design_skips ด้วย reason string ตรง ๆ.
   ตอนนี้ 4 ใน 8 reason ผูกกับ path ของเครื่อง = pin จะเดี้ยงข้ามเครื่องแน่นอน.
2. 3 โมดูลที่ใช้ `pytest.skip(..., allow_module_level=True)`
   (`test_chat_channel_family_static`, `test_stats_progression_static`,
   `test_use_drop_sell_static`) ทำให้ collector มองไม่เห็นเทสข้างในเลย: มี
   `def test_` อยู่ 15 + 25 + 16 = **56 ตัว** แต่ทั้งสามโมดูลรายงานแค่ `1 skipped` และ
   `0 collected`. pin ที่ได้จึงเป็น 1 ซึ่งจะ **ไม่ขยับ** แม้จะมีคนเพิ่มเทสเข้าไปอีกยี่สิบตัว.
   ถ้ารอบหน้าอยากให้ pin ทำงานตามที่ COVERAGE pin โฆษณาตัวเอง ควรเลื่อนเป็น class-level
   ซึ่งจะเปลี่ยนเลขจาก 1/1/1 เป็น 15/25/16 - **ต้องเปลี่ยน pin ในคอมมิตเดียวกัน**.
   re-derive: `grep -c 'def test_' tests/<module>.py`

## 6. คีย์ artifact ที่มีอยู่แล้วพอไหม - เสนอเพิ่ม 3 คีย์

การกระจายของ 257 node ที่ต้อง guard ใหม่ ตามคีย์:

| key | สถานะ | node | path |
|---|---|---|---|
| client_image | มีอยู่แล้ว | 222 | `../GameClient/GameClient.local.bin` |
| **client_image_original** | **เสนอใหม่** | 19 | `../GameClient/GameClient.bin` |
| game_install_tree | มีอยู่แล้ว | 8 | `../GameClient/` |
| capture_v141 / backups_tree / analysis_tree | มี 2 + เสนอใหม่ 1 | 6 | ดูล่าง |
| **evidence_tree** | **เสนอใหม่** | 2 | `<repo>/evidence/` |
| | | **257** | |

### 6.1 `client_image_original` - จำเป็น ไม่ใช่ของฟุ่มเฟือย

ในรีโปมีอิมเมจไคลเอนต์ **สองตัวที่ไม่ใช่ตัวเดียวกัน** และ REGISTRY รู้จักแค่ตัวเดียว:

- `../GameClient/GameClient.local.bin` sha256 `9627211412AC60D5...` = `client_image` ปัจจุบัน
- `../GameClient/GameClient.bin` sha256 `C528BF43070E2789...` = ตัวที่ shipped มา ยังไม่ถูก patch

หลักฐาน: `tests/test_equip_state_static.py:15-16` ประกาศ sha ทั้งสองไว้คนละค่า และเทส
`test_exact_original_and_local_spans_are_identical` มีอยู่เพื่อพิสูจน์ว่าสองไฟล์นี้เหมือนกัน
ในช่วงที่สนใจ - ซึ่งแปลว่ามันต่างกันที่อื่น.

19 node ที่ต้องการตัว `.bin` (ไม่ใช่ `.local.bin`) - วัดจาก path ใน FileNotFoundError จริง:

| module | node |
|---|---|
| test_action_consumer_probe | `ConsumerProbeTests::test_exact_real_binary_guards_both_profiles` |
| test_behavior_entry_probe | `BehaviorEntryProbeTests::test_exact_profiles_disk_guards_and_hook_provenance` |
| test_behavior_lookup_probe | `::test_exact_profiles_and_disk_guards`, `::test_hook_is_instruction_aligned_and_has_no_relocations` |
| test_behavior_range_gate_probe | `::test_profiles_guards_instructions_and_relocations` |
| test_hit_result_probe | `::test_hook_spans_do_not_overlap_pe_relocations`, `::test_real_binary_guards_both_profiles` |
| test_knockdown_consumer_probe | `::test_profiles_actual_binaries_boundaries_relocations_cross_pair` |
| test_skill_trigger_probe | `::test_profiles_guards_boundaries_and_relocations` |
| test_equip_state_static | ทั้ง 5 ตัวที่แดง |
| test_item_move_consumer_static | ทั้ง 3 ตัว |
| test_item_order_static | 2 ตัวที่แดง |

re-derive ต่อ node:
```
python3 -m pytest "<nodeid>" -q -p no:cacheprovider --tb=line 2>&1 | grep -oE "'/tmp/GameClient[^']*'"
```

**เหตุผลว่าทำไมใช้ `client_image` แทนไม่ได้:** บนเครื่องที่มี `.local.bin` แต่ไม่มี `.bin`
(สถานการณ์ที่เป็นไปได้จริง เพราะ `.local.bin` เป็นสำเนาที่เราสร้างเอง) guard ที่เช็ค
`client_image` จะไม่ยิง แล้วเทสจะแดงด้วย FileNotFoundError อยู่ดี - คือ bug เดิมย้ายที่.

### 6.2 `evidence_tree` - `<repo>/evidence/`

`tests/test_structural_corpus_audit.py` 2 node ต้องการ
`evidence/v74-v76/GAME_20260813_145705_866858_59540_v74.txt` และ `.zip` ข้างกัน.
`git ls-files evidence` ตอบ 0 ไฟล์ และ `git check-ignore -v evidence` ตอบ `.gitignore:1:/*`
คือโดนกฎ deny-all บรรทัดแรกกิน. เป็น corpus เฉพาะเครื่อง ไม่มีทางอยู่ในโคลน.

### 6.3 `analysis_tree` - `<repo>/analysis/`

`tests/test_capture_corpus.py` มี capture set ชื่อ `login_archived` ที่ `scan_dir` เป็น `"."`
คือกวาดทั้งรีโปหา `LOGIN_*.txt`. ไฟล์ที่หายไป 63 ไฟล์กระจายอยู่ใต้ `analysis/` และ `backups/`.
`backups_tree` มีในทะเบียนแล้ว แต่ `analysis/` ยังไม่มี (`LOGIN_REQ_CAPTURE` ชี้ไฟล์เดียว
ข้างใน ไม่ใช่ทั้งต้นไม้). `git ls-files analysis` ตอบ 0.

re-derive ว่า set ไหนกวาดที่ไหน:
```
python3 -c "import json;d=json.load(open('docs/PF_CAPTURE_CORPUS.json'))
for k,v in d.items():
  if isinstance(v,dict): print(k, v.get('scan_dir') or v.get('scan_dirs'))"
```
ตอบ: `game_v141_archived -> capture_v141`, `login_archived -> .`,
`game_teleportcheck_0x4477 -> ['backups/v131.../capture_v131', ... 6 โฟลเดอร์]`

**ทางเลือกถ้าไม่อยากเพิ่มคีย์:** ทั้งสองกรณีสามารถ guard ด้วยการเช็คว่า scan target
ของแต่ละ set มีอยู่ไหม แล้วให้ `Precondition` ตัวเดียวชื่อ `capture_corpus_tree`
ครอบ `capture_v141` + `backups` + `analysis` + `evidence` ก็ได้ แต่จะเสียความละเอียด
ตอนอ่านผล census (จะไม่รู้ว่าขาดต้นไม้ไหน). แนะนำให้แยกคีย์.

## 7. `tools/pf_vital_name_thunk_static.py:127` - `ROOT.parent / "pf_bridge"`

**คำตอบตรง ๆ: เมื่อเลิกใช้ `--ignore` บน fresh clone จะไม่มีเทสตัวไหนระเบิดเพราะข้อนี้เลย
- ศูนย์ตัว.** แต่เป็นระเบิดเวลาที่ยังไม่ถูกปลด ไม่ใช่ปัญหาที่ไม่มีอยู่.

หลักฐานที่วัดได้:

1. บรรทัด 127 เป็นแค่ `DEFAULT_TSV = ROOT.parent / "pf_bridge" / "VITAL_REGISTRY_FROM_CLIENT_BINARY_20260817.tsv"`
   ซึ่ง**ไม่เปิดไฟล์ตอน import**. พิสูจน์:
   ```
   cd /tmp/fc2 && python3 -c "
   import sys; sys.path.insert(0,'.')
   import tools.pf_vital_name_thunk_static as a; print('thunk import OK', a.DEFAULT_TSV)
   import tools.pf_vital_thunk_census_static as b; print('census import OK')"
   ```
   ตอบ OK ทั้งสองบรรทัด ทั้งที่ `/tmp/pf_bridge` ไม่มีอยู่.

2. `main()` อ่าน binary **ก่อน** tsv: บรรทัด 469 `image = Image(binary)` มาก่อนบรรทัด 500
   `candidates = load_candidates(tsv)`. พิสูจน์ด้วยการรันเปล่า:
   ```
   cd /tmp/fc2 && python3 tools/pf_vital_name_thunk_static.py 2>&1 | tail -3
   ```
   ตอบ `FileNotFoundError: ... '/tmp/GameClient/GameClient.local.bin'` - ตายที่ไบนารี
   ไม่เคยไปถึง tsv.

3. เทสที่ **รัน** tool นี้เป็น subprocess มีแค่ใน `tests/test_names_fold003_thunk_census.py`
   คลาส `ToolRunTests` (`run_tool(THUNK_TOOL)` บรรทัด 437 และ 459, `run_tool(CENSUS_TOOL)`
   บรรทัด 472 และ 563) และทุกเมธอดในคลาสนั้นมี `@unittest.skipUnless(client_available(), ...)`
   คุมอยู่แล้ว. บน fresh clone ที่ไม่มี client image ทั้ง 5 ตัว skip ก่อน จึงไม่มีทางไปแตะ tsv.

4. `tests/test_vital_names_table.py` เอ่ยชื่อ tool นี้ใน **ข้อความ error hint** เท่านั้น
   ไม่ได้รันมัน - โมดูลนี้ไม่ได้อยู่ใน 42 และผ่านอยู่แล้วบน runner
   (`26 passed, 615 subtests passed`).
   `tests/test_vital_id_resolve_scope.py:309` ก็แค่ assert ว่าชื่อไฟล์นี้ปรากฏใน stdout
   ของ `pf_vital_id_resolve_static.py` ซึ่งไม่อ่าน tsv.

5. ทั้งรีโปมี reference ถึง `pf_bridge` ในโค้ดจริงแค่บรรทัดเดียวคือบรรทัด 127 นี้
   (ที่เหลือเป็นข้อความใน docstring/คอมเมนต์):
   ```
   grep -rn "pf_bridge" --include=*.py . | grep -v tests/pf_preconditions.py
   ```

**เมื่อไหร่มันจะระเบิด:** บนเครื่องที่ **มี** `../GameClient/GameClient.local.bin` แต่
**ไม่มี** `../pf_bridge/`. ตอนนั้น `client_available()` เป็นจริง guard ไม่ยิง เทส 3 ตัวใน
`ToolRunTests` ที่เรียก `run_tool` จะได้ returncode ไม่ใช่ 0 แล้ว assert ล่ม:
`test_thunk_verifier_runs_clean_and_reports_half_alpha`,
`test_census_verifier_runs_clean_against_the_committed_artifact`,
และตัวที่บรรทัด 563. (`test_both_tools_print_nothing_the_windows_console_cannot_encode`
ก็เรียก tool เช่นกัน).

**สิ่งที่ควรทำในรอบหน้า:** เพิ่ม `BRIDGE_SIBLING` เป็น guard ตัวที่สองซ้อนกับ
`client_image` ใน `ToolRunTests` ของ `test_names_fold003_thunk_census.py`
(`bridge_sibling` มีในทะเบียนอยู่แล้วและ docstring ของมันอ้างบรรทัด 127 นี้ตรง ๆ อยู่แล้ว).
เลขที่จะเปลี่ยน: บน fresh clone ยังคง 5 skip เท่าเดิม (client_image ยิงก่อน) - **pin ไม่ขยับ**
ซึ่งเป็นเหตุผลที่งานนี้ทำได้ทุกเมื่อโดยไม่ต้องแก้ pin.

## 8. รายละเอียดระดับ guard - เทสที่ต้อง **ไม่** ถูก guard

ส่วนนี้คือหัวใจของกติกา "ห้าม module-level ถ้ามีเทส pure-stdlib". รายชื่อข้างล่างคือเทส
ที่ **ผ่านบน fresh clone** และอยู่ในคลาสเดียวกับเทสที่แดง - ถ้าเผลอ guard ทั้งคลาสหรือทั้งโมดูล
จะเสียความครอบคลุมบน runner ทันที.

re-derive: `python3 -m pytest tests/<m>.py -v --tb=no -p no:cacheprovider` แล้วดูบรรทัด PASSED

| module | คลาสที่ guard ได้ทั้งคลาส | เมธอดที่ต้อง guard เดี่ยว | เมธอดที่ต้องปล่อยไว้ (pure-stdlib) |
|---|---|---|---|
| test_actor_type_dispatch_static | VerifierRunsCleanTests(3), DispatchShapeTests(5), RemotePlayerBranchTests(5), AttrClassGateTests(6), NameSourceTests(5), ServerCrossCheckTests(3) | ReportMatchesTheBinaryTests: test_every_reported_key_exists_in_the_live_counts, test_every_reported_value_matches_exactly; ArtifactsExistTests: test_report_manifest_tool_and_client_all_exist | ArtifactsExistTests อีก 2, ReportMatchesTheBinaryTests อีก 1, ReportDisciplineTests ทั้ง 4 |
| test_damage_hit_result_static | TagMapTests(4), HeaderFieldTableTests(4), HitElementTableTests(5), SignedDamageFieldTests(4), AngleNotDamageTests(4), ResultFlagsTests(3), DisplayPathTests(5), NoArithmeticNegativeTests(7), DyingAndReviveTests(6), TrapTests(5) | ArtifactsExistTests: test_the_binary_the_tool_chose_exists_and_is_the_pinned_one; VerifierRunsCleanTests x5 | ArtifactsExistTests::test_the_tool_exists, VerifierRunsCleanTests::test_the_verifier_is_pure_stdlib, ::test_the_verifier_never_opens_the_binary_for_writing |
| test_hp_death_respawn_static | HpFieldIdentityTests(3), DeathDerivationTests(3), VerbFamilyTests(4), ServerGapTests(4) | VerifierRunsCleanTests x3, ReportMatchesTheBinaryTests x2, ArtifactsExistTests::test_report_manifest_tool_and_client_all_exist | ArtifactsExistTests อีก 3, CoverageRowTests ทั้ง 7, ReportDisciplineTests ทั้ง 4, VerifierRunsCleanTests::test_the_verifier_is_pure_stdlib, ReportMatchesTheBinaryTests อีก 1 |
| test_ui_state_refresh_static | VerifierRunsCleanTests(4), CharacterListBufferTests(6), DeleteAckTests(4), LogoutTests(3), TransitionGraphTests(5) | ReportMatchesTheBinaryTests x2, ArtifactsExistTests::test_report_manifest_tool_and_client_all_exist | ArtifactsExistTests อีก 3, ReportDisciplineTests ทั้ง 4, ReportMatchesTheBinaryTests อีก 1 |
| test_login_vital_req_static | ReportMatchesTheBinaryTests(2), FrameShapeTests(5), AccountIsAVariableTests(7), CorpusTests(5) | VerifierRunsCleanTests x3, EvidenceExistsTests::test_every_input_and_output_exists | EvidenceExistsTests อีก 3, OurServerTests ทั้ง 4 |
| test_runtimeres_actor_entry_static | TestReportMatchesTheBinary(2), TestTraps(6) | TestVerifierItself x2, TestTheAnswer x9 | TestVerifierItself::test_it_needs_no_third_party_package, TestTheAnswer::test_the_erratum_is_present_and_does_not_rewrite_the_original |
| test_capture_corpus | - | PinnedFilesTests: test_hashes_are_reproducible, test_every_pinned_capture_is_present_and_byte_identical, test_no_capture_exists_outside_the_pinned_set, test_no_pinned_capture_has_vanished; LiveFileExclusionTests: test_the_live_tails_still_match_the_pattern | CaptureCorpusTableTests ทั้ง 7, StrayDetectionTests ทั้ง 5, PinnedFilesTests อีก 3 (ที่เหลือ), LiveFileExclusionTests อีก 2 |
| test_teleportcheck_0x4477_corpus | - | RealCorpusTests::test_the_wire_guards_all_pass_on_the_real_corpus (backups_tree), ExitCodeTests::test_the_real_run_still_passes (client_image + backups_tree) | FrameDecodingTests ทั้ง 3, TrapTests ทั้ง 8, RealCorpusTests อีก 4, ExitCodeTests อีก 2 |
| test_structural_corpus_audit | - | test_exact_guarded_corpus_and_determinism, test_zip_member_guard_and_safe_output | test_anchored_parsers_only_and_malformed_fail, test_direction_duplicate_and_drift_fail, test_source_has_no_raw_search_or_mutation |
| test_equip_state_static | - | 5 ตัวที่แดง | test_current_foundation_has_no_equipped_container_builder |
| test_item_order_static | - | test_exact_original_and_local_spans_are_identical, test_item_identity_is_the_tree_key_and_writer_uses_successor_order | test_exact_post_merge_slot2_is_unoccupied_but_policy_remains_hypothesis |
| probe ทั้ง 8 ตัว | - | ดูตารางหลักและหัวข้อ 6.1 | 4-8 ตัวต่อโมดูล ทั้งหมดเป็น config/schema/fail-closed test ที่สร้าง PE ปลอมเอง |
| move_authority_targetpos, remote_movement_projection, split_operate x3, item_move_consumer | ทั้งคลาสเดียวของโมดูล (ทุกเทสต้องการ artifact) | - | **ไม่มี** - 6 โมดูลนี้เท่านั้นที่ module-level guard ไม่เสียความครอบคลุม |

**ข้อสังเกตเรื่อง subTest:** 4 เมธอดชื่อ `test_report_manifest_tool_and_client_all_exist`
(และ `test_every_input_and_output_exists` ใน login_vital_req) วน `subTest` เช็คว่าไฟล์
4 ตัวมีอยู่จริง - REPORT, MANIFEST, TOOL, CLIENT - และล่มเฉพาะ subtest ของ CLIENT.
ถ้า guard ทั้งเมธอด จะเสียการเช็คของอีก 3 path ที่อยู่ในรีโปไปด้วย.
**เสนอ:** ผ่าเป็นสองเมธอด - ตัวหนึ่งเช็ค 3 path ในรีโป (ไม่ guard) อีกตัวเช็ค CLIENT
(guard ด้วย client_image). ไม่ว่าจะเลือกทางไหน จำนวน skip ยังเป็น 1 ต่อโมดูลเท่าเดิม.
อย่าใช้ `skipTest` ข้างใน `subTest` เพราะ pytest-subtests จะพ่นบรรทัด SKIPPED เพิ่ม
ซึ่งจะทำให้ pin ที่คำนวณไว้ในเอกสารนี้ไม่ตรง.

## 9. ลำดับงานที่แนะนำสำหรับรอบหน้า (เรียงจากเสี่ยงน้อยไปมาก)

| wave | ทำอะไร | โมดูล | test ที่ได้คืน | skip ใหม่ | pin ที่ต้องเพิ่ม | ความเสี่ยง |
|---|---|---|---|---|---|---|
| 0 | ลบ 9 โมดูลออกจาก ignore เฉย ๆ | 9 | **398** | **0** | **0** | ต่ำสุด. ไม่แตะไฟล์เทสสักไฟล์ ไม่แตะ pin file. ถ้าแดง แปลว่าเป็นเรื่อง Windows/py3.14 ล้วน ๆ ซึ่งเป็นข้อมูลที่มีค่าในตัวเอง |
| 1 | ลบอีก 8 โมดูล + ย้าย reason string ไปใช้ `Precondition.reason` + เพิ่ม pin 8 รายการ | 8 | 88 | 25 | 8 | ต่ำ. ไม่มีเทสไหนต้องเปลี่ยน logic เปลี่ยนแค่ข้อความ. **จำเป็น** เพราะไม่ทำแล้ว census แดง (วัดแล้ว: `UNDECLARED SKIP` 8 ข้อ) |
| 2 | เพิ่มคีย์ `client_image_original` + `evidence_tree` + `analysis_tree` แล้ว guard ระดับเมธอดในโมดูลเล็ก | 14 | 82 | 36 | 14+ | กลาง. แตะไฟล์เยอะแต่แต่ละไฟล์แก้ 1-5 บรรทัด. ทำ `client_image_original` ให้จบก่อน แล้วค่อยแตะ probe |
| 3 | guard ระดับคลาส 5 โมดูลที่ทุกเทสตายที่ `setUpClass` | 5 | 0 | 51 | 5 | กลาง. ตรงไปตรงมาที่สุดในกลุ่มที่ต้องแก้โค้ด เพราะไม่มีเทส pure-stdlib ให้ต้องระวัง แต่ได้ test คืน 0 ตัว จึงคุ้มค่าน้อยกว่า wave 2 |
| 4 | 6 โมดูล static ใหญ่ - class + method ผสม | 6 | 43 | 170 | 6+ | สูงสุด. 170 skip = 60% ของ pin ทั้งหมด และเป็นที่ที่พลาดง่ายที่สุดเพราะแต่ละโมดูลมีคลาส "รายงาน/วินัย" ที่ต้องปล่อยไว้ ดูหัวข้อ 8 |
| | **รวม** | **42** | **611** | **282** | | |

หมายเหตุ:
- ตัวเลข 611 ตรงกับจำนวน node ที่ผ่านสะอาดในตารางหลักพอดี (398+88+82+0+43 = 611)
  และ 282 ตรงกับ 257+25 พอดี - เป็น cross-check ว่าไม่มีโมดูลตกหล่นระหว่าง wave.
- **หลังจบ wave 0 ควรลบ `Select-String` heuristic ทิ้งทันที** แล้วเปลี่ยนเป็นรายชื่อ hard-coded
  ที่พิมพ์ออกมาเต็ม ๆ เพราะ heuristic จะจับ false positive ตัวใหม่ทุกครั้งที่มีคนเขียน docstring
  ว่า "no GameClient" - ซึ่งเป็นสิ่งที่โปรเจกต์นี้ส่งเสริมให้เขียน.
- ถ้าอยากได้ deliberate red ที่ checklist ยังค้างอยู่ wave 1 เป็นที่ที่ปลูกได้สะอาดที่สุด:
  เปลี่ยน pin ตัวใดตัวหนึ่งจาก 8 เป็น 7 แล้ว push - census ต้องแดงด้วยข้อความ PIN DRIFT
  แล้วค่อยแก้กลับ.

## 10. NONCLAIMS - สิ่งที่งานนี้ไม่ได้พิสูจน์

1. **วัดบน Linux + CPython 3.10.12 ไม่ใช่ Windows + CPython 3.14.** ทุกตัวเลขในเอกสารนี้
   เป็นของ sandbox. เครื่องจริงและ runner เป็น Windows/3.14 และโปรเจกต์นี้มีประวัติชัดเจน
   (รอบ 142, cp874) ว่า "green" เปลี่ยนความหมายข้ามเครื่อง. ที่ยืนยันได้แล้วว่าต่างจริง:
   `tests/test_server_shutdown.py::test_primary_exception_is_preserved_with_cleanup_failure`
   แดงเฉพาะที่นี่เพราะ `__notes__` เป็นของ 3.11+ - เอกสารนี้จึงไม่นับมันเป็นปัญหาของรีโป
   และมันคือหลักฐานว่าความต่างระหว่างสองเครื่องมีจริงและวัดได้.
2. **ไม่ได้วัดฝั่งที่ artifact มีครบ.** ทุกอย่างวัดบน fresh clone ที่ทั้ง 7 คีย์ ABSENT.
   เอกสารนี้จึงพูดไม่ได้เลยว่าบนเครื่องของ Panya (client image + capture corpus + backups +
   pf_bridge ครบ) เทสเหล่านี้ **ผ่าน** - พูดได้แค่ว่ามันจะไม่ skip. โดยเฉพาะ guard ที่เสนอ
   ทุกตัวควรเป็น no-op บนเครื่องนั้น แต่ **ยังไม่ได้พิสูจน์** ว่าเป็นเช่นนั้นจริง.
3. **ตัวเลข skip ทุกตัวเป็นคำทำนาย ไม่ใช่การวัด** จนกว่าจะเขียน guard จริงแล้วรันจริง.
   สิ่งที่วัดจริงคือ "มี N node ที่ล้มเพราะ artifact หาย"; การบอกว่า "ถ้าใส่ guard จะเกิด N skip"
   ตั้งอยู่บนสมมติฐานว่า guard หนึ่งตัวต่อหนึ่ง node และ pytest รายงาน skip หนึ่งบรรทัด
   ต่อหนึ่งเมธอด. รูปแบบ guard ที่ต่างออกไป (subTest skip, module-level, fixture) จะให้เลข
   ต่างออกไป - ดูคำเตือนท้ายหัวข้อ 8.
4. **ไม่ได้พิสูจน์ว่า 9 โมดูล false positive จะเขียวบน runner.** พิสูจน์แค่ว่ามันไม่ต้องการ
   artifact ใด ๆ. มันยังอาจแดงด้วยเหตุอื่น (cp874, path separator, ลำดับไฟล์บน NTFS,
   ความต่างของ 3.14). wave 0 คือการทดลองที่จะตอบคำถามนี้ - และถูกจัดเป็นเสี่ยงต่ำสุด
   ก็เพราะมันตอบคำถามนี้ด้วยราคาถูกที่สุด.
5. **ไม่ได้ตรวจสอบว่าเทสที่ผ่าน "ผ่านด้วยเหตุผลที่ถูก".** เอกสารนี้อ่านสถานะ pass/fail
   ไม่ได้อ่านว่า assertion ที่รันไปนั้นแข็งแรงแค่ไหน. เทสที่ผ่านบน fresh clone อาจผ่าน
   เพราะมันไม่ได้ยืนยันอะไรเลยก็ได้ - นั่นเป็นคำถามคนละข้อและเอกสารนี้ไม่ตอบ.
6. **ไม่ได้แก้อะไรในรีโปเลย.** งานนี้เป็นงานวัดล้วน. ไม่มีการ commit/push/add/reset/clean/stash
   ไม่แตะ canonical DB ไม่เปิด UI/GameClient ไม่บูต server ไม่แตะ `Pirate Force ServerProject/`
   ไม่แตะธง LOCK_* / GAME_TEST_QUEUE.md / CHIEF_CONTINUATION.md.
   fresh clone ที่ `/tmp/fc2` เป็นสำเนาชั่วคราวใน Linux sandbox ไม่ได้อยู่บนเครื่อง Panya.
7. **`--collect-only` ที่ตอบ 890 node ไม่ได้แปลว่าเห็นเทสครบ.** 3 โมดูลที่ใช้
   module-level skip ซ่อน `def test_` ไว้ 56 ตัวจาก collector. ตัวเลข 890 คือ
   "สิ่งที่ collector เห็น" ไม่ใช่ "สิ่งที่เขียนไว้".

## 11. ไฟล์ที่งานนี้แตะ

- `pf_bridge/FACTPACK_R106_PYTEST_EXCLUSION_INVENTORY.md` (ไฟล์นี้ - สร้างใหม่)

ไฟล์อื่นในรีโป Pirate Force: **ไม่แตะเลยแม้แต่ไฟล์เดียว**.
