# ต้นเหตุจริงของ sync ที่ตัน 94 ครั้ง + แพตช์ `pf_git_sync.ps1` (ให้ chief ลงมือ)

**ผู้เขียน:** ผู้ช่วย (cloud) · **ถึง:** chief (cc) และ Panya
**สถานะ:** ผู้ช่วยเขียนแพตช์ให้ครบ **แต่แตะ `pf_git_sync.ps1` เองไม่ได้** — มันเป็นไฟล์ที่ track แล้วแต่อยู่นอก
push allowlist ⇒ ผู้ช่วยแก้บนดิสก์เมื่อไหร่ = สร้างการตันครั้งที่ 95 ทันที (นั่นคืออาการที่จดหมายนี้กำลังอธิบาย)

---

## ① ข้อมูล ไม่ใช่ความเห็น

```
grep -c "fast-forward refused" sync.log   ->  94
```

94 ครั้ง ติดที่ไฟล์แค่ **สองไฟล์**:

| ไฟล์ | ครั้ง | ช่วง | ตันนานเท่าไร |
|---|---:|---|---|
| `CHIEF_CONTINUATION.md` | 40 | 2026-08-21 03:42 เป็นต้นไป | ~3 ชม. 20 นาที |
| `AGENTS.md` | 56 | 2026-08-24 03:22 เป็นต้นไป | ~4 ชม. 40 นาที |

คนละคน คนละไฟล์ คนละวัน **อาการเดียวกันเป๊ะ** ⇒ ไม่ใช่ความผิดพลาดรายบุคคล เป็นหลุมเชิงโครงสร้าง

## ② กลไกที่ทำให้เกิด

- `git merge --ff-only` ปฏิเสธเมื่อไฟล์ที่ **track อยู่** ถูกแก้ในเครื่อง
- push allowlist = `notes_to_chief` + `evidence_screens` เท่านั้น ⇒ ไฟล์นอกนั้น **ออกไม่ได้**
- รวมกัน: **ไฟล์ที่ "อยู่ใน git แล้ว แต่ push ออกไม่ได้" = กับดัก** แก้ทีไรล็อกตายทันที ทั้งขาเข้าและขาออก

🔴 **และตอนตัน มันบอกใครไม่ได้:**

```
บรรทัด 391   Finish 4 'STOP_LOCAL_EDITS_BLOCK_PULL'   <- ออกจากสคริปต์ตรงนี้
บรรทัด 402   # [4] bridge push                         <- ไม่เคยถึง
```

pull กับ push เป็นงานคนละงานที่ไม่ขึ้นต่อกัน แต่พอ pull ตัน สคริปต์ `Finish` ก่อนถึงขา push
⇒ **จดหมายที่จะบอกว่า "ฉันตัน" ก็ออกไม่ได้** สัญญาณเดียวคือ `SYNC_ATTENTION.txt` นอนอยู่บนดิสก์
**องค์ประกอบเดียวที่ตรวจเจอว่าระบบตัน คือองค์ประกอบเดียวที่รายงานไม่ได้**

เหตุการณ์วันนี้ยืนยันซ้ำอีกชั้น: หลังปลดบล็อกที่ 1 ได้ รอบก็ตายที่บรรทัด 416 (`REFUSED_PROPRIETARY`
ไฟล์เกิน 2 MB สามตัว) **ก่อนถึงขา push อีกเช่นกัน** ⇒ ไฟล์วิดีโอหนึ่งไฟล์ปิดทั้งระบบได้

---

## ③ แพตช์ที่เสนอ — 3 จุด (+1 ของแถม)

### แพตช์ ① — เปิดทางให้ "ไฟล์ที่เขียนกันสองฝ่าย" เดินทางออกได้

**หลักคิด:** allowlist มีหน้าที่จริงคือ **กันไฟล์ใหม่แปลกปลอมไม่ให้หลุดขึ้น remote**
ไฟล์ที่ **อยู่ใน git history แล้ว = อยู่ใน repo แล้ว** การ commit การแก้ไขของมัน **ไม่ทำให้อะไรรั่วเพิ่ม**
และ guard เนื้อหา (นามสกุล / ชื่อ / 2 MB) ยังทำงานกับทุกไฟล์เหมือนเดิม

🔴 **แต่ไม่ใช่ "ปล่อยไฟล์ที่ track ทั้งหมด"** — ต้องแยกให้ออกระหว่าง
- **ไฟล์ที่มีสองฝ่ายเขียนโดยชอบธรรม** (`AGENTS.md` — chief เขียนบน main, ผู้ช่วย/ผู้เทสเขียนบนดิสก์) ⇒ ควรเดินทางออกได้
- **ไฟล์ที่มีเจ้าของคนเดียว** (`CHIEF_CONTINUATION.md`, `GAME_TEST_QUEUE.md`, `CLIENT_RE_QUEUE.md`)
  ⇒ การแก้ในเครื่อง **ยังเป็นความผิดพลาดเหมือนเดิม** ห้ามให้มันเงียบ ๆ ทับงาน chief

```powershell
# ใกล้บรรทัด 86 ข้าง $ALLOWLIST
$ALLOWLIST      = @('notes_to_chief', 'evidence_screens')   # ไฟล์ "ใหม่" ได้แค่สองที่นี้เหมือนเดิม
$SHARED_TRACKED = @('AGENTS.md', '.gitignore', 'agent_kit') # ไฟล์ "ที่แก้" ของสองฝ่าย - เดินทางออกได้
```

```powershell
# ต่อท้ายบล็อก candidate scan (หลังบรรทัด ~295)
# ไฟล์ที่ track อยู่แล้วและถูกแก้ ในพาธที่ประกาศว่าเขียนกันสองฝ่าย
# --untracked-files=no คือกุญแจ: ไฟล์ใหม่ที่ยังไม่ track จะไม่ติดมาทางนี้เด็ดขาด
$stShared = GitRun $BridgeRepo (@('status','--porcelain','--untracked-files=no','--') + $SHARED_TRACKED)
foreach ($line in ($stShared.Out -split "`n")) {
    if ($line.Trim().Length -lt 4) { continue }
    $xy   = $line.Substring(0, 2)
    $path = ParsePorcelainPath $line.Substring(3)
    if ($path.Length -eq 0) { continue }
    if ($xy -match 'D' -or $xy -match 'R') { $deletions += ($xy.Trim() + ' ' + $path); continue }
    if ($candidates -notcontains $path) { $candidates += $path }
}
```

**ผลที่ได้:** เหตุการณ์ตระกูล `AGENTS.md` (56 จาก 94 ครั้ง) หายไปทั้งคลาส —
การแก้จะถูก commit และ push ในรอบถัดไปเอง แทนที่จะขวางประตู

### แพตช์ ② — ไฟล์เสียยกเลิก *commit* ไม่ใช่ยกเลิก *รอบ*

```powershell
# บรรทัด ~412-417 เดิม
if ($refusals.Count -gt 0) {
    Shout '[4]' (...)
    foreach ($r in $refusals) { Log '[4]' ('  X ' + $r) }
    Finish 5 'REFUSED_PROPRIETARY' (...)      # <-- บรรทัดนี้ฆ่าทั้งรอบ
}
```

```powershell
# ที่ควรเป็น
$skipCommit = $false
if ($refusals.Count -gt 0) {
    Shout '[4]' ('skipping the commit: ' + $refusals.Count + ' file(s) failed the proprietary guard')
    foreach ($r in $refusals) { Log '[4]' ('  X ' + $r) }
    Log '[4]' 'the commit is cancelled, but commits already made still get pushed below.'
    $skipCommit = $true
}
```
แล้วครอบบล็อก commit ด้วย `if (-not $skipCommit -and $candidates.Count -gt 0) { ... }`
**ขา push (บรรทัด ~467) ต้องทำงานเสมอ** ไม่ว่ารอบนี้จะ commit ได้หรือไม่

**ผลที่ได้:** ไฟล์วิดีโอหนึ่งไฟล์ **ปิดทั้งระบบไม่ได้อีก** งานที่ commit ไปแล้วยังออกได้ตามปกติ

### แพตช์ ③ — pull ตัน ต้องไม่ฆ่ารอบ และต้องส่งเสียงออกไปได้

```powershell
# บรรทัด ~388-391 เดิม -> Finish 4
# ที่ควรเป็น: บันทึก, ข้าม merge, ไปต่อ
Shout '[3]' ('fast-forward refused - a chief-owned file is modified here: ' + (...))
WriteAsciiFile $attnPath @(...)                       # เก็บไว้เหมือนเดิม
$blockedPull = $true                                  # ไม่ Finish
# แล้วเขียนจดหมายลง notes_to_chief\ เพื่อให้มันติดไปกับ push รอบนี้เลย
$stuckLetter = Join-Path $notesDir ('SYNC_STUCK_' + (Get-Date -Format 'yyyyMMdd_HHmm') + '.md')
if (-not (Test-Path -LiteralPath $stuckLetter)) {
    WriteAsciiFile $stuckLetter @(
        '# SYNC STUCK - the bridge cannot fast-forward',
        '',
        ('time   : ' + (Stamp)),
        ('behind : ' + $behind + '   ahead: ' + $ahead),
        'git said:',
        ($mg.Out),
        '',
        'The bridge is still pushing, so this letter travels.  Nothing is lost;',
        'the local edits are on the disk.  Resolve by committing or discarding',
        'the named file on the bridge machine.'
    )
}
```

**ผลที่ได้:** การตันแบบเงียบ 3-4 ชั่วโมง **เป็นไปไม่ได้อีก** — cc เห็นจดหมายในรอบถัดไปแล้วบอก Panya ได้

### ของแถม ④ — วิดีโอไม่ควรเกิดใน `evidence_screens\` ตั้งแต่แรก

`AGENTS.md` §5 เขียนไว้เองว่า **"ห้าม push วิดีโอ ให้อ้างพาธแทน"**
แต่จ็อบบูตกลับเขียน `.mkv` ลง `evidence_screens\` ซึ่งเป็น **โฟลเดอร์เดียวที่ถูก commit และมีเพดาน 2 MB**
⇒ เปลี่ยนปลายทางของ recorder เป็น **`pf_bridge\evidence_video\`** (นอก allowlist โดยตั้งใจ)
และเพิ่มบรรทัดใน `AGENTS.md` §5 ว่าวิดีโออยู่ที่นั่น · ภาพนิ่ง/เฟรมย่อไปที่ `evidence_screens\` เหมือนเดิม

---

## ④ ผลรวมที่คาดไว้ (เขียนล่วงหน้าเพื่อให้ตรวจสอบได้)

| อาการ | ครั้งที่เกิดมาแล้ว | แพตช์ที่ปิด |
|---|---:|---|
| `AGENTS.md` แก้ในเครื่อง -> ตัน | 56 | ① |
| `CHIEF_CONTINUATION.md` แก้ในเครื่อง -> ตัน | 40 | ③ (ยังเตือนดัง แต่ไม่ปิดระบบ) |
| ไฟล์ใหญ่ 1 ไฟล์ปิดทั้ง commit และทั้งรอบ | วันนี้ | ② |
| ตันแล้วเงียบ ไม่มีใครรู้ | ทั้ง 94 ครั้ง | ③ |
| วิดีโอไปนอนในโฟลเดอร์ที่มีเพดาน 2 MB | วันนี้ | ④ |

## ⑤ ที่ยัง **ไม่** เปลี่ยน (สำคัญ)

- ไฟล์ **ใหม่ที่ยังไม่ track** ยังขึ้นได้แค่ `notes_to_chief` + `evidence_screens` เหมือนเดิมทุกประการ
- guard เนื้อหา (นามสกุล / ชื่อ / 2 MB) ยังใช้กับทุกไฟล์รวมทั้งของใหม่ในแพตช์ ①
- **ห้ามลบ / rename ใน allowlist** ยังเป็นกฎเหล็กเหมือนเดิม (`REFUSED_DELETION` ไม่ถูกแตะ)
- เส้น "ห้ามอัปโหลด client binary / capture corpus / .dmp / canonical DB" **ไม่ถูกแตะแม้แต่นิดเดียว**
- ไฟล์ที่ chief เป็นเจ้าของคนเดียว (`CHIEF_CONTINUATION.md`, ไฟล์คิวทั้งสาม) **ไม่ได้ถูกใส่ใน `$SHARED_TRACKED`**
  การแก้ในเครื่องยังผิดเหมือนเดิม แค่ไม่ปิดระบบอีกต่อไป

## ⑥ nonclaims

- ผู้ช่วย **ไม่ได้รันสคริปต์นี้ทดสอบ** — อ่านโค้ดกับ `sync.log` อย่างเดียว ⇒ chief ต้อง `-DryRun` และ `-SelfCheck` ก่อนใช้จริง
- เลข 94 / 56 / 40 มาจาก `sync.log` บนดิสก์เครื่องสะพานเท่านั้น ถ้าล็อกเคยถูกตัด ตัวเลขจริงจะมากกว่านี้
- แพตช์ ① เปลี่ยน **ขอบเขตของสิ่งที่ถูก push อัตโนมัติ** ⇒ เป็นเรื่องที่ **Panya ต้องเคาะ** ไม่ใช่ chief ตัดสินเอง
- ไม่ได้พิสูจน์ว่า 94 ครั้งนั้นไม่มีสาเหตุอื่นปนอยู่ — พิสูจน์แค่ว่าไฟล์ที่ git ระบุชื่อมีสองไฟล์นี้เท่านั้น
