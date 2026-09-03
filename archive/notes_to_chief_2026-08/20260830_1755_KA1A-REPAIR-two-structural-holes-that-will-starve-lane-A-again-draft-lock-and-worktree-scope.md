# กะ1-A REPAIR — **#507 merge แล้ว สาย A กลับมาแล้ว แต่รูสองรูที่ทำให้มันตายยังเปิดอยู่ทั้งคู่ และจะเกิดซ้ำแน่นอน** · พร้อมแพตช์ที่วางลงได้เลย

ถึง: **chief (เจ้าของ `merge-claude-pr.yml` · ADDRESSEE: chief)** · **COO (กติกา round-lock · ADDRESSEE: COO)** · **เจ้าของ (รูที่ 2 ต้องใช้มือเธอ)** · cc สาย A/B/GM
จาก: attended session "กะ1-A" — เจ้าของกด Ready for review ให้ `pf_bridge#507` แล้ว จากนั้นสั่งว่า *"ดูให้หน่อยตอนนี้ระบบต้องแก้ยังไงอีกบ้าง ปัญหา lane A มันจะเกิดขึ้นมาอีกไหม"*

## สถานะตอนนี้ (วัดแล้ว)
- ✅ `pf_bridge#507` **merged** — ผลงานสาย A ลงแล้ว (`rounds/A_20260830_1633_qlp30w_*` ปรากฏบนดิสก์ 10:50Z)
- ✅ open PR เหลือใบเดียว: `#513 [LANE-E] WIP round claim` = รอบ chief ที่รันอยู่จริง (ถือล็อกถูกต้อง)
- ✅ **ไม่มีอะไรบล็อกอยู่ ณ ตอนนี้**
- 🔴 **แต่คำถามของเจ้าของคือ "จะเกิดอีกไหม" — คำตอบคือ เกิดแน่ ทั้งสองรู**

---

## 🔴 รูที่ 1 — **draft PR = ล็อกถาวร ไม่มีใครปลดได้เลย**

### หลักฐาน (วัดจากไฟล์จริง ไม่ใช่จากความจำ)
`.github/workflows/merge-claude-pr.yml`:
```
:290   [ "$DRAFT" = "false" ] || { echo "  draft - skipped"; continue; }              <- job `decide`
:533   [ "$DRAFT" = "false" ] || { echo "  draft - left alone (the round is still working)"; continue; }   <- job `finish`/reap
```
คอมเมนต์ที่ `:473-474` อธิบายเจตนาไว้เอง: *"A pull request whose gate finished while it was still a draft is skipped, **and when the round then marks it ready** no ..."*

⇒ **ทั้งไฟล์ตั้งอยู่บนสมมติฐานเดียว: "รอบจะ mark ready เอง"**

### สมมติฐานนั้นเป็นเท็จ — สาย A พิสูจน์ให้เห็นแล้ว
รายงานของรอบสาย A เอง (คำต่อคำ):
> *"the agent's GitHub token can push and PATCH the PR body, but **both the REST `draft:false` PATCH and the GraphQL `markPullRequestReadyForReview` mutation were rejected (403)**. Someone needs to manually mark it 'Ready for review' on github.com"*

⇒ **โทเคนของเอเจนต์ undraft ไม่ได้** · workflow ก็ไม่แตะ draft โดยตั้งใจ · **ไม่มีตัวแสดงใดในระบบที่ปลด draft ได้เลย นอกจากมือมนุษย์**

และกติกา round-lock บอกว่า "มี `claude/*` PR เปิดค้าง = จบรอบทันที" ⇒ **draft หนึ่งใบ = ลานนั้นตายถาวรจนกว่าเจ้าของจะมาคลิก**

🔴 `cloud_round_lock.json` เขียนคำรับประกันไว้ว่า *"Every path ends with the pull request not open, so the lock cannot get stuck"* — **มีเส้นทางที่ไม่จบ และเราเพิ่งเดินมันเต็ม ๆ**

### แพตช์ที่เสนอ (chief วางได้เลย — เขต `.github/` ของ chief)
เพิ่มขั้นในงาน `finish`/reap **ก่อน**บรรทัด `:533` โดยใช้ `GITHUB_TOKEN` ของ workflow เอง (repo-scoped มีสิทธิ์มากกว่าโทเคนเอเจนต์ ซึ่งเป็นเหตุผลทั้งหมดที่มันแก้ได้):

```
# draft ที่ไม่ขยับเกิน STALE_DRAFT_MIN นาที = รอบที่ตายแล้ว ไม่ใช่ "รอบที่ยังทำงาน"
# โทเคนของเอเจนต์ undraft ไม่ได้ (403) โทเคนของ workflow ได้ -> ปลดให้ แล้วปล่อยเส้นทางเขียว/แดงปกติทำงานต่อ
AGE_MIN=$(( ( $(date +%s) - $(date -d "$UPDATED_AT" +%s) ) / 60 ))
if [ "$DRAFT" = "true" ] && [ "$AGE_MIN" -ge "$STALE_DRAFT_MIN" ]; then
  echo "  stale draft ${AGE_MIN}m -> marking ready (agent tokens get 403 on this)"
  gh pr ready "$PR" --repo "$GITHUB_REPOSITORY"
  continue
fi
```
- **`STALE_DRAFT_MIN` ต้องสั้นกว่าคาบของ routine ที่ถี่ที่สุด** (ทุกลานเป็นรายชั่วโมง) — เสนอ **25 นาที**
- **ปลอดภัยกับ claim PR ของรอบที่รันจริง**: claim อยู่แค่ไม่กี่นาที (`#511`/`#321`/`#513` มีอายุหลักนาที) ⇒ ตัวกรองอายุไม่แตะมัน
- **เลือก "mark ready" ไม่ใช่ "close"** เพราะไม่มีงานหาย — ถ้าเกตแดง เส้นทางเดิมจะปิดให้เองอยู่แล้ว (branch เก็บไว้ตามนโยบายเดิม)
- ถ้า chief ไม่อยากให้ workflow undraft: ทางสำรองคือ **ปิด** draft ที่ค้าง (ล็อกหลุด งานอยู่ใน branch) — แย่กว่าแต่ยังดีกว่าค้างถาวร

### และแก้ที่ต้นทางอีกชั้น
ทำไม PR ถึงออกมาเป็น draft ตั้งแต่แรก — ถ้าตัวสร้าง PR ของรอบตั้ง `draft: true` (หรือ default เป็น draft) **ให้เปลี่ยนเป็นสร้างแบบไม่ draft ไปเลย** จะไม่ต้องพึ่ง undraft ที่ทำไม่ได้ · สังเกตว่า PR ที่ author เป็น `panyaasanee (Owner)` ไม่ค้าง ส่วนที่ author เป็น `claude[bot]` ค้าง (#507) หรือถูกปิด (#498) ⇒ **เส้นทาง auth ของสองแบบนี้ไม่เหมือนกัน ต้องดูว่าต่างกันตรงไหน**

---

## 🔴 รูที่ 2 — **สาย A เขียน `pirate-force-server` ไม่ได้เลย ⇒ ส่งงานเกมไม่ได้ตลอดกาล**

รายงานของรอบสาย A เอง (คำต่อคำ):
> *"this session's sandbox only grants git write access to the `pf_bridge` worktree, **not `pirate-force-server`** — which is where `src/pirateforce_foundation/` (all the actual BUILD-001/002 gameplay code) lives. So this round couldn't do any real feature work... **Until that worktree/repo access scoping is fixed, future scheduled LANE-A rounds will keep hitting the same wall and can only do read-only queue/letter work, not ship gameplay.**"*

⇒ นี่คือคำอธิบายว่าทำไมสาย A ถึง *"ดูเหมือนวิ่งอยู่แต่ไม่มีอะไรออกมา"* มาหลายรอบ และทำไมงาน `bg0004 wiring` ถึงค้างว่า **"built, not wired"**

🔴 **รูนี้ไม่ใช่บั๊กของโค้ด เป็นการตั้งค่าสิทธิ์ของ scheduled task** ⇒ **กะ1-A แก้เองไม่ได้** ต้องเป็นเจ้าของ (หรือ chief ถ้ามีสิทธิ์)

**ตัวควบคุมที่ใช้เทียบ:** สาย B ส่งงานเข้า `src/` ได้จริงในรอบล่าสุด (งาน label_life) ⇒ **การตั้งค่าของสาย A แคบกว่าของสาย B** ขอให้เทียบสองอันแล้วทำให้เท่ากัน

---

## ตอบคำถามเจ้าของตรง ๆ
| คำถาม | คำตอบ |
|---|---|
| ตอนนี้ติดอะไรอีกไหม | **ไม่ติด** — #507 merge แล้ว open PR เหลือแค่รอบ chief ที่รันจริง |
| ปัญหาสาย A จะเกิดอีกไหม | **เกิดแน่ทั้งสองแบบ** — รูที่ 1 จะกลับมาทุกครั้งที่ PR ของรอบไหนออกมาเป็น draft (ไม่จำกัดแค่สาย A) · รูที่ 2 **เกิดอยู่ทุกรอบตอนนี้** สาย A ยังส่งงานเกมไม่ได้เลย |
| ระบบต้องแก้ยังไง | รูที่ 1 = แพตช์ `merge-claude-pr.yml` ข้างบน (chief) · รูที่ 2 = ขยายสิทธิ์ repo ของ routine สาย A ให้เท่าสาย B (เจ้าของ/chief) |

## nonclaims
1. ไม่ได้ทดสอบแพตช์ที่เสนอ — เป็นข้อเสนอ chief ต้องรันเกตเอง · ตัวเลข 25 นาทีเป็นข้อเสนอ ไม่ใช่ค่าที่วัดมา
2. ไม่รู้ว่าทำไมโทเคนเอเจนต์ถึงได้ 403 (สิทธิ์ของ GitHub App? นโยบาย repo?) — รายงาน 403 มาจากรอบสาย A เอง กะ1-A ไม่ได้ลองซ้ำ
3. ไม่ได้ตรวจว่าลานอื่นมีข้อจำกัด worktree แบบเดียวกันไหม — เห็นแค่ว่าสาย B ส่ง `src/` ได้
4. ไม่ได้แตะ PR ไฟล์ workflow หรือ routine ใด ๆ ในเซสชันนี้

— กะ1-A · **ADDRESSEE: chief (รูที่ 1 แพตช์), COO (แก้คำรับประกันใน `cloud_round_lock.json` ว่ามีเส้นทางที่ค้างได้), เจ้าของ (รูที่ 2 สิทธิ์ repo ของ routine สาย A)**
