# Info-file convention for pf_bridge jobs (fix for the 069/081 path-space bug)

**บั๊กที่แก้:** boot jobs เคยเขียน info file เป็นบรรทัดเดียว `key=value` คั่นช่องว่าง เช่น

```
clientpid=3344 console=18308 server=14132 stamp=20260817_192713 rundb=C:\Users\Panya\Desktop\Pirate Force\Pirate Force ServerProject\state\pirateforce_gt007_20260817_192713.sqlite3 title=Pirate Force
```

teardown ที่ parse ด้วย whitespace-split หรือ regex ต่อบรรทัด จะตัด path ที่มี space ขาด
(`C:\Users\Panya\Desktop\Pirate` …) → เปิด DB ผิดไฟล์เงียบ ๆ → DB snapshot เป็นค่าขยะ
เกิดแล้ว 2 ครั้ง: job 069 (GT-002) และ job 081 (GT-007) — snapshot fail ≠ เทส fail แต่เสียเวลาอ่านซ้ำ

## กติกาใหม่ (บังคับทุก job ที่เขียน/อ่าน info file ตั้งแต่ 084 เป็นต้นไป)

1. **เขียน: หนึ่ง key ต่อหนึ่งบรรทัด** ห้ามรวมบรรทัดเดียว:

```powershell
@(
  "clientpid=$clientPid"
  "console=$consolePid"
  "server=$serverPid"
  "stamp=$stamp"
  "rundb=$runDbPath"
  "title=$windowTitle"
) | Out-File -FilePath $infoFile -Encoding ascii
```

2. **อ่าน: split ที่ `=` ตัวแรกเท่านั้น** (path มี `=` ไม่ได้อยู่แล้วบน Windows แต่กันไว้):

```powershell
$info = @{}
Get-Content $infoFile | ForEach-Object {
  $i = $_.IndexOf('=')
  if ($i -gt 0) { $info[$_.Substring(0,$i)] = $_.Substring($i+1) }
}
# $info['rundb'] ได้ path เต็มรวม space
```

3. ทุกครั้งที่ส่ง path เป็น argument ให้ native command: **quote เสมอ** (`"$($info['rundb'])"`)
   — บทเรียนเดิมจาก 069 ที่ proven แล้วใน staged 072/073

4. sanity check หลัง parse: ถ้า key ที่คาดหวังหายหรือค่าว่าง ให้ log `PARSE FAIL` ชัด ๆ
   แล้วข้าม DB snapshot — ห้ามรันต่อด้วยค่า default/ว่าง (069 เคย cast ได้ PID 0 = System Idle)
