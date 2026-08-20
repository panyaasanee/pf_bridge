# R100 Agent B fact pack: B_CONSTDATA monster + loot side

Date: 2026-08-20. Worker: data-mining agent B (read-only run).
Source: `Pirate Force ServerProject/backups/v103_one_item_backpack_20260814_103143/derived/v97_mapping_audit/B_CONSTDATA_TH.pc_.dec`
(8,443,000 bytes; sha256 verified this session = 496DFB2EF2CF517482A7B426C9DD5EDF0278564FE11195B96F36DF90607F0D2D).

Scope respected: BEHAVIOR table (012) NOT re-audited (COMBAT-KNOCK-DATA-001 already covers it,
including the proven NEGATIVE binding BEHAVIOR-row -> CKnockdownVital+0x20).

## 0. Parse method and root cause of the prior "utf-16 decode" crash

- Parser: copy of `parse_pc_tables.py` -> `/tmp/pf/parse_hardened.py`, with
  `decode("utf-16le", errors="replace")` added as instructed.
- ROOT CAUSE FINDING: the historical all-tables crash was NOT primarily a bad-string problem.
  `B_CONSTDATA_TH.pc_.dec` is in the LINKED-TIP header format (per-table header =
  name, serialized_size, version, linked TIP-table-name string, column list). Running the
  parser WITHOUT `--linked-tip-format` consumes the TIP-name string length as
  `table_flags`/`column_count` and walks into row data (observed: column_count read as
  4522070 = 0x00450056 = UTF-16 text "VE" of "VERSION_PHASE_TIP"). With
  `--linked-tip-format` + errors="replace", the FULL file parses cleanly:
  120 tables (indices 000-119), exit code 0, no mid-file errors.
- Trailing 146 bytes at 0x80D3E6 (end of table 119) are a footer, not a table:
  u32=4, u32=0x65876CF0, UTF-16 "1.41.0000", UTF-16 "2014/12/11 <CJK 'PM'> 02:52:06",
  UTF-16 32-hex-char digest "65ED12EA5470536BED75FAEBC4660D77" (algorithm [UNKNOWN], length matches MD5).
  So the const data self-identifies as client data version 1.41.0000 built 2014-12-11.

## 1. FULL table inventory (all 120 tables)

Format: `idx offset-range NAME rows x cols` (offsets from the clean full parse, byte offsets in the .dec).
Flags: [LOOT] = drops/loot/reward-related, [FACTION] = faction/camp, [MOB] = monster-side, [ACQ] = other item-acquisition.

```
000 0x00000004-0x000000F6 VERSION_PHASE          6 x 2
001 0x000000F6-0x00001C40 MAINMENU              29 x 15
002 0x00001C40-0x000021AA FUNCTION_CONTROL       8 x 9
003 0x000021AA-0x00002522 DROPS_ACTIVITY         4 x 11   [LOOT]
004 0x00002522-0x0000460A VARIABLE_FLOATING    178 x 3
005 0x0000460A-0x0000830E VARIABLE_INTEGER     325 x 3
006 0x0000830E-0x0000B3D4 HOTKEY                95 x 9
007 0x0000B3D4-0x0001D148 SCENE_NAME           271 x 24
008 0x0001D148-0x0001F292 STANDARD_STATUS      255 x 8    (player per-level EXP/ability/deadloss)
009 0x0001F292-0x0001F6AA LEVEL_SP             120 x 2
010 0x0001F6AA-0x00022D32 CURRICULUM           137 x 7
011 0x00022D32-0x0006A622 SKILL_CONTEXT       2165 x 20   [MOB] (s_SKILLS targets; has s_CAST_BEHAVIOR)
012 0x0006A622-0x00110B0C BEHAVIOR            2279 x 30   (already audited; out of scope)
013 0x00110B0C-0x001BCFCA Missile             3429 x 26   [MOB] (MOBS.n_DEADMISSILE)
014 0x001BCFCA-0x00312B18 BUFF                9302 x 14
015 0x00312B18-0x00312F06 BUFFLINK               3 x 11
016 0x00312F06-0x003130A4 POTENTIAL              0 x 11
017 0x003130A4-0x0031C67C STANDARD_BUFF        256 x 36
018 0x0031C67C-0x0031E1A4 STACK                423 x 4
019 0x0031E1A4-0x003240D2 CHARCREATE_LOOK      218 x 12
020 0x003240D2-0x00324B2E CHARCREATE_SKIN       20 x 10
021 0x00324B2E-0x00325B02 CHARCREATE_CLASS       5 x 38
022 0x00325B02-0x00327032 CHARCREATE_PACKAGE    30 x 14
023 0x00327032-0x00329A46 CD_TIMER            1335 x 2
024 0x00329A46-0x0032AA74 AI_WANDER             73 x 5    [MOB][FACTION] (carries n_FACTION)
025 0x0032AA74-0x0032BC36 AI_TACTIC              9 x 5    [MOB]
026 0x0032BC36-0x00351094 AI_COMBAT            276 x 3    [MOB]
027 0x00351094-0x0035AE0A STANDARD_MOB         255 x 38   [MOB] (per-level mob stat baseline)
028 0x0035AE0A-0x004A327E MOBS                3210 x 54   [MOB][LOOT] (linked TIP: MOBS_TIP)
029 0x004A327E-0x004E61DC CLINE               3599 x 19
030 0x004E61DC-0x004E6CEE MOB_TALK               9 x 5    [MOB] (talk triggers keyed off BEHAVIOR(id) events)
031 0x004E6CEE-0x004F2668 NPC_VOICE            373 x 6
032 0x004F2668-0x004F2C16 PLAYER_VOICE           6 x 10
033 0x004F2C16-0x004FE722 INSTANCE             338 x 17
034 0x004FE722-0x0050000A SCORECOUNT            87 x 14
035 0x0050000A-0x005004F4 PARTY_SEARCH          10 x 7
036 0x005004F4-0x00500F38 EQUIP_VALUE           17 x 16
037 0x00500F38-0x00546BC6 EQUIPMENT_BASE       974 x 39   (item id space, prefix 22)
038 0x00546BC6-0x0054D356 CHANGE_MODEL         249 x 12
039 0x0054D356-0x0055BC74 EQUIP_AVATAR         212 x 39
040 0x0055BC74-0x0055BDF2 EQUIP_AVATAR_COMBINE   0 x 9
041 0x0055BDF2-0x005B53FE ITEM_CONSUMABLES    1260 x 39   (item id space, prefix 24)
042 0x005B53FE-0x0062CF7E ITEM_MISC           1646 x 39   (item id space, prefix 26)
043 0x0062CF7E-0x006473E8 ITEM_ITEMMALL        366 x 39
044 0x006473E8-0x0066E1B6 ITEM_QUEST           579 x 38   (item id space, prefix 25)
045 0x0066E1B6-0x0066EB54 EQUIPMENT_ROOT        71 x 6
046 0x0066EB54-0x0066F71E VARYDATA             178 x 4
047 0x0066F71E-0x0067BA24 ITEM_USING           947 x 9
048 0x0067BA24-0x0067E4D6 DROPS_EQUIPMENT       53 x 44   [LOOT]
049 0x0067E4D6-0x0069ED1A DROPS_NORMAL         267 x 121  [LOOT]
050 0x0069ED1A-0x006C3E2C DROPS_SPECIALLY      584 x 64   [LOOT]
051 0x006C3E2C-0x006C5180 DECOMPOSITION         48 x 9    [ACQ]
052 0x006C5180-0x006C525A APPRAISE               7 x 3
053 0x006C525A-0x00790648 ADDITIONAL          6305 x 14
054 0x00790648-0x00790B6E E_DROPS_QUALITY       26 x 9    [LOOT] (equipment-drop quality weights)
055 0x00790B6E-0x007910A4 CRYSTAL_PLATE          9 x 9
056 0x007910A4-0x00792972 CULTURED_CRYSTAL      27 x 43
057 0x00792972-0x007933F4 GATHER                52 x 7    [ACQ]
058 0x007933F4-0x00794E64 FORMULA_DRINK         85 x 16
059 0x00794E64-0x00796AF0 COMBINE               47 x 18   [ACQ]
060 0x00796AF0-0x00797932 STORE_NORMAL          15 x 26
061 0x00797932-0x007982B6 STORE_CONDITION       55 x 8
062 0x007982B6-0x0079DC42 STORE_GOODS          164 x 16
063 0x0079DC42-0x0079DF3E STORE_SMITH            0 x 20
064 0x0079DF3E-0x007A5F2C DAILY_REWARD          78 x 94   [LOOT]
065 0x007A5F2C-0x007A600E ONLINE_REWARD          8 x 3    [LOOT]
066 0x007A600E-0x007A6802 DAILY_INFO_REWARD      7 x 26   [LOOT]
067 0x007A6802-0x007A6C6A ENHANCEMENT_RULES     25 x 6
068 0x007A6C6A-0x007A6EB4 EQUIPMENT_ZONE         9 x 7
069 0x007A6EB4-0x007A90FC PETDATA              109 x 13
070 0x007A90FC-0x007A94AC SAILOR_AVATAR          3 x 17
071 0x007A94AC-0x007A9680 SAILOR_QUALITY         5 x 8
072 0x007A9680-0x007A985A SAILOR_FRIENDLY        4 x 5
073 0x007A985A-0x007ACC50 SAILOR_SKILL         144 x 11
074 0x007ACC50-0x007B1BAC PET_MIX              178 x 10
075 0x007B1BAC-0x007B25FA COIN_CONSUME          21 x 9
076 0x007B25FA-0x007B57B6 SUIT                 101 x 13
077 0x007B57B6-0x007B869E EFFECT_STORAGE       100 x 11
078 0x007B869E-0x007BD5E2 EFFECT_RESIDENT      249 x 15
079 0x007BD5E2-0x007BD732 EFFECT_COLLECT         4 x 2
080 0x007BD732-0x007BDACC SCENE_WEATHER          7 x 11
081 0x007BDACC-0x007BDD18 SCENE_TILE            18 x 5
082 0x007BDD18-0x007C026C MARKER               390 x 6
083 0x007C026C-0x007C3A2C SCENE_AREA           270 x 7
084 0x007C3A2C-0x007C5046 Trigger              312 x 4
085 0x007C5046-0x007C52C0 FACTION               38 x 2    [FACTION]
086 0x007C52C0-0x007C55F8 GUILD_STATUS          10 x 8
087 0x007C55F8-0x007C6884 GUILD_MEMBER           6 x 25
088 0x007C6884-0x007C976E GUILD_AURA            96 x 12
089 0x007C976E-0x007C9968 GUILD_GOLD            19 x 4
090 0x007C9968-0x007CAA16 STANDARD_QUEST       255 x 4
091 0x007CAA16-0x007CAE3E FONT_COLOR            57 x 4
092 0x007CAE3E-0x007CB686 ACTIVITY               2 x 35
093 0x007CB686-0x007CB878 DAILY_PLAN             3 x 7
094 0x007CB878-0x007CE31E COLLECT               64 x 12   [ACQ]
095 0x007CE31E-0x007CF2AE VEHICLE               79 x 10
096 0x007CF2AE-0x007EEB9E DROPS_QUEST          311 x 101  [LOOT]
097 0x007EEB9E-0x007EF518 VOW_LOCK              14 x 15
098 0x007EF518-0x007F05C0 STANDARD_LV          255 x 4    [LOOT] (per-level quest cash/exp/sp reward baseline)
099 0x007F05C0-0x007F94D8 ACHIEVEMENT          156 x 20
100 0x007F94D8-0x007F9580 7SINS                  7 x 2
101 0x007F9580-0x007FA044 MAP_SCENE_LIST        15 x 15
102 0x007FA044-0x007FB30C UI_CONFIRM           106 x 8
103 0x007FB30C-0x007FB9A6 EMOTION               16 x 6
104 0x007FB9A6-0x007FC0B2 REPORT                20 x 5
105 0x007FC0B2-0x007FC902 MOVIE                 14 x 9
106 0x007FC902-0x007FEC6C HELP_DATA             88 x 7
107 0x007FEC6C-0x007FFC82 HELP_IMAGE            27 x 11
108 0x007FFC82-0x0080791C SAILING_RESULT       138 x 19   [ACQ] (sailing outcome rewards; not mob loot)
109 0x0080791C-0x0080842E SHIP                  17 x 12
110 0x0080842E-0x00808612 FLOOR_EFFECT           0 x 13
111 0x00808612-0x00808C52 GET_SHIPCORPSE         8 x 11   [LOOT] (ship-corpse salvage pickup)
112 0x00808C52-0x00809168 PVP_PROPERTIES         4 x 17
113 0x00809168-0x0080B06E GAME_TARGET_HINT      52 x 17
114 0x0080B06E-0x0080C0C0 BUFF_GROUP           250 x 4
115 0x0080C0C0-0x0080C85A STALL_SET             11 x 10
116 0x0080C85A-0x0080CAE0 CUTIN                 15 x 4
117 0x0080CAE0-0x0080CCD6 GUILDEVENT             0 x 13
118 0x0080CCD6-0x0080CF14 RANK_REWARD            0 x 15   [LOOT] (schema present, ZERO rows shipped)
119 0x0080CF14-0x0080D3E6 SCROLL_VOICE          11 x 3
```

No table named TREASURE/BOX/PICKUP/CAMP exists. "Camp" as a concept is the FACTION table (085).
Empty-but-schemad tables: POTENTIAL(016), EQUIP_AVATAR_COMBINE(040), STORE_SMITH(063),
FLOOR_EFFECT(110), GUILDEVENT(117), RANK_REWARD(118).

## 2. MOBS (table 028, 3210 rows x 54 cols, 0x35AE0A-0x4A327E, linked TIP table = MOBS_TIP)

Full column list (name, type, size, record offset) from MOBS.json (type 0=int, 2=float, 3=utf16 string):

```
 0 n_ID              int   +0     28 n_INTIMATE          int   +112
 1 s_NAME            str   +4     29 n_CREDIT            int   +116
 2 s_ID_MODEL_CLASS  str   +8     30 n_PVPSCORE          int   +120
 3 n_ID_MODEL        int   +12    31 n_MOB_APPEAR        int   +124
 4 n_ID_MAP          int   +16    32 n_DROP_RANGE        int   +128
 5 s_PREDESCRIPT     str   +20    33 n_DROPS_EQUIPMENT   int   +132
 6 s_OUTFIT          str   +24    34 n_DROPS_NORMAL      int   +136
 7 n_BOUNDARY        int   +28    35 n_DROPS_SPECIALLY   int   +140
 8 n_HEIGHT          int   +32    36 n_DROP_FLOOR        int   +144
 9 n_LEVEL_MIN       int   +36    37 n_DROPS_QUEST       int   +148
10 n_LEVEL_MAX       int   +40    38 s_QUEST_BEGIN       str   +152
11 n_RANK            int   +44    39 s_QUEST_END         str   +156
12 f_RATIO_EXP       flt   +48    40 n_CAPABILITY        int   +160
13 f_RATIO_SP        flt   +52    41 s_ICON              str   +164
14 s_PROPERTIES      str   +56    42 s_LOCATION          str   +168
15 n_SPEED_WALK      int   +60    43 n_GM_SWITCH         int   +172
16 n_SPEED_RUN       int   +64    44 n_FITTINGROOM_DISTANCE int +176
17 n_VEHICLE         int   +68    45 n_FITTINGROOM_HEIGHT int  +180
18 n_AI_WANDER       int   +72    46 s_NPC_VOICE         str   +184
19 n_AI_COMBAT       int   +76    47 s_ROLE_GRAPHIC      str   +188
20 n_AI_TACTIC       int   +80    48 n_BROADCAST         int   +192
21 s_SKILLS          str   +84    49 n_MOB_USAGE         int   +196
22 n_DEADMISSILE     int   +88    50 s_HK_VER            str   +200
23 n_CONDITION       int   +92    51 s_TC_VER            str   +204
24 n_SKIN_COLOR      int   +96    52 s_JP_VER            str   +208
25 s_PROPERTIES...   --           53 s_TH_VER            str   +212
```
(Offsets +72/+76/+80 confirm the v103 handoff notes "n_AI_WANDER @ +72" etc.)

Column categories requested:
- (a) BEHAVIOR/skill/action refs: `s_SKILLS` (semicolon list). 586 distinct ids across all rows;
  496/586 resolve as SKILL_CONTEXT.n_ID (table 011). Unresolved sample: 0, 3820-3826 block
  [UNKNOWN - probably stripped skills]. SKILL_CONTEXT itself carries `s_CAST_BEHAVIOR`, i.e. the
  chain is MOBS.s_SKILLS -> SKILL_CONTEXT -> BEHAVIOR, not MOBS -> BEHAVIOR directly.
  `n_DEADMISSILE` references the Missile table (013) [INFERENCE from name, not row-verified].
- (b) AI refs: `n_AI_WANDER` -> AI_WANDER.n_ID (61 distinct nonzero values, 100% resolve),
  `n_AI_COMBAT` -> AI_COMBAT.n_ID (184 distinct nonzero, 100% resolve),
  `n_AI_TACTIC` -> AI_TACTIC.n_ID (nonzero values {1,2,3,11,1001,1002}, 100% resolve).
  Value distribution: n_AI_TACTIC {1:1852, 0:1326, 11:15, 1001:8, 1002:7, 2:1, 3:1};
  top n_AI_WANDER {11:1140, 2:724, 1:289, 16:253, 4:163, 39:121, ...};
  n_AI_COMBAT {0:1326, 1:251, 110:62, 111:58, ...}.
- (c) faction/camp: MOBS has NO direct faction column. Faction comes via
  MOBS.n_AI_WANDER -> AI_WANDER.n_FACTION. Distribution over all 3210 rows:
  faction 6 (hostile monster camp) 1716; faction 4 (neutral) 1114; faction 1 218; faction 17 26;
  faction 7 25; faction 10 16; faction 5 13; the rest small; 17 rows have n_AI_WANDER=0 ->
  faction [UNKNOWN] for those.
- (d) level/HP/stats: `n_LEVEL_MIN`/`n_LEVEL_MAX` (level band), `n_RANK` (bitmask-style rank:
  distribution 0:1506, 1:1232, 2:228, 4:125, 64:57, 128:40, 4096:17, 512:5), `f_RATIO_EXP`,
  `f_RATIO_SP`, `n_SPEED_WALK`, `n_SPEED_RUN`. MOBS carries NO HP/damage columns at all;
  base combat stats come from STANDARD_MOB indexed by level (section 3).
- (e) drop/loot refs: `n_DROP_RANGE` (nonzero in 3198/3210 rows, usually 200),
  `n_DROPS_EQUIPMENT` (nonzero 1436), `n_DROPS_NORMAL` (nonzero 1393),
  `n_DROPS_SPECIALLY` (nonzero 747), `n_DROPS_QUEST` (nonzero 2596),
  `n_DROP_FLOOR` (nonzero 0 - dead column in shipped data).
  ENCODING RULE (proven, section 5): value = prefix*100000 + target-table n_ID.

MOBS n_ID range 1..10080 (3210 rows, sparse). Linked MOBS_TIP (3139 rows):
n_ID, s_NAME (localized display name, e.g. n_ID 1 = "Navy Transfer"), s_TITLE, s_NPC_CHATS.

### Representative rows (all values from MOBS.json rows; names shown as unicode escapes)

LOW - MOBS n_ID 28 (lowest-level mob with a normal-drop set), s_NAME = \u9189\u72fc\u6d77\u8cca\u5718 ("Drunk Wolf pirates"):
```
n_LEVEL_MIN/MAX = 16/18   n_RANK = 1        n_MOB_USAGE = 1
n_AI_WANDER = 16 (-> FACTION=6, OFFESIVE=0, AGGRO=0)
n_AI_COMBAT = 110         n_AI_TACTIC = 1   s_SKILLS = 3020;3020;3020;3020
n_DROPS_NORMAL = 2701001  n_DROPS_EQUIPMENT = 5400001  n_DROPS_SPECIALLY = 0
n_DROPS_QUEST = 8700028   n_DROP_RANGE = 200
f_RATIO_EXP = 1.0  n_SPEED_WALK/RUN = 100/650  s_PROPERTIES = 400;7005  n_CREDIT = 0
s_OUTFIT = M001_000_000_N;M001_000_000_SP1 (multi-variant outfit)
```

MID - MOBS n_ID 6005 (lvl ~52 boss-rank), s_NAME = \u541e\u98df\u8005 ("Devourer"):
```
n_LEVEL_MIN/MAX = 52/54   n_RANK = 4096     n_MOB_USAGE = 1
n_AI_WANDER = 16 (-> FACTION=6)  n_AI_COMBAT = 144  n_AI_TACTIC = 1
s_SKILLS = 3080;3081;3086
n_DROPS_NORMAL = 2702002  n_DROPS_EQUIPMENT = 5400102  n_DROPS_SPECIALLY = 2801553
n_DROPS_QUEST = 8706005   n_DROP_RANGE = 200
f_RATIO_EXP = 48.0  n_SPEED_WALK/RUN = 100/800  s_PROPERTIES = 433;7024  n_CREDIT = 10
s_OUTFIT = M004_000_000_BOSS
```
(Note: no rank-2/rank-64 mob in lvl 45-60 carries drop sets; the mid pick is therefore a
low-band rank-4096 boss.)

BOSS - MOBS n_ID 6001 (first n_RANK=4096 row), s_NAME = \u8352\u5cf6\u60e1\u9738 ("Desert Island Tyrant"):
```
n_LEVEL_MIN/MAX = 64/66   n_RANK = 4096     n_MOB_USAGE = 1
n_AI_WANDER = 16 (-> FACTION=6)  n_AI_COMBAT = 335  n_AI_TACTIC = 1
s_SKILLS = 3460;3462;3463;3464;3468
n_DROPS_NORMAL = 2702003  n_DROPS_EQUIPMENT = 5400102  n_DROPS_SPECIALLY = 2801554
n_DROPS_QUEST = 8706001   n_DROP_RANGE = 200
f_RATIO_EXP = 48.0  n_SPEED_WALK/RUN = 100/800  s_PROPERTIES = 445;7115  n_CREDIT = 10
s_OUTFIT = M023_000_002_SP4
```
Its AI_COMBAT row 335 is a real HP-phase script:
COND = `BUFF_I(4983,0,0);BUFF_I(4982,0,1);RATE(40) / BUFF_I(4982,0,0);HP_I<(0.9);RATE(25) /
BUFF_I(4983,0,0);HP_I<(0.6);RATE(25) / HP_I<(0.45);RATE(15) / HP_I<(0.3);R...`
ACTION = `CHASE(4) / CHASE(3) / CHASE(4) / CHASE(3) / CHASE(4) / CHASE(2) / CHASE(1)`
(CHASE(n) [INFERENCE] = use n-th entry of the mob's s_SKILLS list.)

All 17 rank-4096 bosses (n_ID, level_min): (6001,64) (6002,84) (6003,33) (6004,43) (6005,52)
(6006,54) (6007,62) (6008,64) (6009,72) (6010,74) (6011,82) (6012,91) (6013,95) (6014,101)
(6015,105) (6016,108) (6017,108).

NPC example (Port Royal template 1) is in section 7.

## 3. STANDARD_MOB (table 027, 255 rows x 38 cols, 0x351094-0x35AE0A)

Columns:
```
n_ID, n_MOBEXP, n_SP, n_HPMAX, n_RECOVER_HP, n_STAMINAMAX, n_RECOVER_STAMINA, n_SPEED_RUN,
n_STRENGH, n_CONSITUTION, n_AGILITY, n_PERCEPTION, n_INTELLECT,
n_DAMMIN_PHYSICS, n_DAMMIN_MAGIC, n_DAMPLUS_PHYSICS, n_DAMPLUS_MAGIC,
n_AC_PHYSICS, n_AC_MAGIC, n_ABSORB_PHYSICS, n_ABSORB_MAGIC,
n_PENETRATE_PHYSICS, n_PENETRATE_MAGIC,
f_ANTI_STUN, f_STUN, f_ANTI_CURSE, f_CURSE, f_HITRATE, f_DODGE, f_POWERHIT, f_ANTI_POWERHIT,
f_BYPASS, f_OVERHIT, f_MULTIPLY_POWERDAM, f_ABSORB_POWERDAM, f_ABSORB_SHIELD, f_BLOCKRATE, f_MUL_DAMAGE
```
Keying: n_ID runs exactly 1..255 contiguous = MOB LEVEL. It is the per-level baseline stat
table for monsters. Relation to MOBS [INFERENCE, consistent with data]: a mob's effective level
is drawn from MOBS.n_LEVEL_MIN..n_LEVEL_MAX, then STANDARD_MOB[level] supplies HP/EXP/damage/
AC etc.; MOBS.f_RATIO_EXP / f_RATIO_SP scale n_MOBEXP / n_SP (rank-4096 bosses carry ratio 48.0).
MOBS itself has no HP column, so this is the only client-side source of mob HP.
Samples: level 1: HPMAX=106, MOBEXP=6, DAMMIN_PHYS=4, AC_PHYS=10.
level 27 (Port Royal Fighting Fish band): HPMAX=3857, MOBEXP=89, DAMMIN_PHYS=144, AC_PHYS=86.
level 50: HPMAX=23976, MOBEXP=231, DAMMIN_PHYS=722. level 255: HPMAX=1771680, MOBEXP=142528.
(Companion tables: STANDARD_STATUS(008) = player per-level EXP/deadloss; STANDARD_LV(098) =
per-level quest reward baseline n_QUEST_CASH/n_QUEST_EXP/n_QUEST_SP; STANDARD_BUFF(017),
STANDARD_QUEST(090) same 255-row pattern.)

## 4. AI tables (client-local AI FSM parameters)

MOBS pointers: n_AI_WANDER -> AI_WANDER (peace/patrol state + faction + aggro),
n_AI_COMBAT -> AI_COMBAT (combat action selection), n_AI_TACTIC -> AI_TACTIC (target selection).

### AI_WANDER (024, 73 rows x 5): n_ID, s_WANDER, n_FACTION, n_OFFESIVE, n_AGGRO
s_WANDER is a state script like `IDLE;9;15\nRUN;0;1` (state;min_s;max_s). n_OFFESIVE = attacks
on sight flag, n_AGGRO = aggro radius [INFERENCE: units approx mm/game-units].
This table is the FACTION CARRIER for mobs.
All 73 rows (n_ID, FACTION, OFFESIVE, AGGRO, s_WANDER):
```
1  4  0 0    IDLE;5;8|RUN;0;2        24 16 0 5000 IDLE;9;15|RUN;0;1      104 104 1 8000 IDLE;25;45|RUN;1;1
2  4  0 0    IDLE;9;15|RUN;0;1       25 17 1 1200 RUN;1;2|IDLE;45;120    105 105 1 8000 IDLE;25;45|RUN;1;1
3  1  1 1000 IDLE;45;45              26 6  0 0    RUN;1;2|IDLE;10;30     110 9  0 800  IDLE;25;45|RUN;1;1
4  1  0 0    RUN;1;2|IDLE;10;30      27 7  1 5000 IDLE;25;45|RUN;1;1     111 10 1 1000 IDLE;25;45|RUN;1;1
5  1  1 800  RUN;1;2|IDLE;10;30      28 6  1 5000 RUN;1;2|IDLE;10;30     112 10 1 200  IDLE;25;45|RUN;1;1
6  1  1 1200 RUN;1;2|IDLE;10;30      30 7  1 1500 IDLE;25;45|RUN;1;1     113 20 0 0    IDLE;25;45|RUN;1;1
7  1  1 1600 RUN;1;2|IDLE;10;30      31 8  1 1500 IDLE;9;15|RUN;0;1      114 20 0 0    IDLE;25;45|RUN;1;1
8  1  1 2000 RUN;1;2|IDLE;10;30      32 19 1 1500 IDLE;25;45|RUN;1;1     115 21 0 0    IDLE;25;45|RUN;1;1
9  13 0 0    RUN;1;2|IDLE;45;120     33 7  1 700  IDLE;25;45|RUN;1;1     116 22 1 2000 IDLE;3;7|RUN;1;1
10 6  1 600  RUN;1;2|IDLE;10;30      34 8  1 700  IDLE;9;15|RUN;0;1      117 23 0 0    IDLE;25;45|RUN;1;1
11 6  1 1200 RUN;1;2|IDLE;10;30      35 27 1 3000 IDLE;5;7|RUN;1;1       118 12 0 0    IDLE;5;7|RUN;1;3
12 6  1 1600 RUN;1;2|IDLE;10;30      36 7  1 2500 IDLE;25;45|RUN;1;1     119 25 0 0    IDLE;25;45|RUN;1;1
13 6  1 2000 RUN;1;2|IDLE;10;30      37 1  1 2000 RUN;1;2|IDLE;10;30     120 26 1 2500 IDLE;25;45|RUN;1;1
14 6  1 2400 RUN;1;2|IDLE;10;30      38 11 1 3000 RUN;1;2|IDLE;5;7       121 22 1 350  IDLE;3;7|RUN;1;1
15 6  1 8000 RUN;1;2|IDLE;10;30      39 6  1 8000 RUN;1;2|IDLE;5;7       201 6  0 0    IDLE;15;15
16 6  0 0    RUN;1;2|IDLE;10;30      40 28 0 3000 RUN;1;2|IDLE;5;7       1001 1 1 1200 IDLE;1;3|RUN;1;1
17 18 1 1200 RUN;1;2|IDLE;10;30      41 10 0 1000 IDLE;25;45|RUN;1;1     1002 1 0 0    IDLE;1;3|RUN;1;1
18 18 1 1600 RUN;1;2|IDLE;10;30      42 29 1 5000 RUN;1;2|IDLE;5;7       1003 1 0 0    IDLE;1;3|RUN;1;1
19 18 1 2000 RUN;1;2|IDLE;10;30      43 30 1 5000 RUN;1;2|IDLE;5;7       1004 13 0 0   IDLE;1;3|RUN;1;1
20 11 1 1500 RUN;1;2|IDLE;10;30      44 31 1 5000 RUN;1;2|IDLE;5;7       1005 4 0 0    IDLE;1;3|RUN;1;1
21 12 1 3000 RUN;1;2|IDLE;10;30      45 32 1 5000 RUN;1;2|IDLE;5;7       5102 5 1 1500 IDLE;25;45|RUN;1;1
22 4  1 5000 IDLE;9;15|RUN;0;1       46 15 0 500  IDLE;25;45|RUN;1;1     9000 4 0 1000 IDLE;9;15|RUN;0;1
23 15 1 2500 IDLE;25;45|RUN;1;1      101 101 1 5000 IDLE;25;45|RUN;1;1   9001 999 0 1000 IDLE;3;7|RUN;0;2
                                     102 102 1 5000 IDLE;25;45|RUN;1;1   9903 1 1 1000 IDLE;15;15
                                     103 102 0 5000 IDLE;25;45|RUN;1;1   9904 1 0 0    IDLE;15;15
```
(`|` = embedded newline in s_WANDER.)

### AI_TACTIC (025, 9 rows x 5): n_ID, s_CREWID, s_CONDITION, s_ENEMY, s_ALLY - ALL 9 ROWS
Columns are parallel newline-separated FSM entries: crew slot, gate condition, enemy-target
selector, ally-target selector. Selector vocabulary observed: MOST_CURE, MOST_DAM, WEAKEST_DAM,
CLOSEST_DAM, CLOSEST_CURE, CLOSEST_CREW, WEAKEST_CREW, MASTER_TARGET, MASTER, ME;
conditions: BUFF_I(id,mask,n), HP_I>(x), GO(0), PET_AI(n).
```
n_ID 1    CREW 0,0,1,1,1,2,2,3,3,4,4,5,5,6,6
          COND BUFF_I(0,16384,1)/GO(0)/BUFF_I(0,16384,1)/HP_I>(0.95)/GO(0)/... (repeating pairs)
          ENEMY MOST_CURE(1)/MOST_DAM(1)/MOST_CURE(1)/WEAKEST_DAM(0)/CLOSEST_DAM(0)/MOST_CURE(1)/
                WEAKEST_DAM(0)/MOST_CURE(1)/MOST_DAM(1)/... ALLY ME(0)x6/WEAKEST_CREW(1)/ME(0)/
                CLOSEST_CREW(0)/ME(0)/CLOSEST_CREW(0)/ME(0)/CLOSEST_CREW(0)/ME(0)/CLOSEST_CREW(0)
n_ID 2    CREW 0,0,1,1  COND BUFF_I(297,0,1)/GO(0) x2  ENEMY CLOSEST_DAM(0) x4  ALLY ME(0) x4
n_ID 3    CREW 0,0,1,1  COND BUFF_I(297,0,1)/GO(0) x2  ENEMY CLOSEST_DAM(0)/MOST_CURE(1)/
          CLOSEST_DAM(0)/MOST_DAM(1)  ALLY ME(0) x4
n_ID 4    same as 3 but ALLY ME(0)/ME(0)/CLOSEST_CREW(0)/CLOSEST_CREW(0)
n_ID 11   CREW 0,0,1,1,1,2,2,3,3,4,4,5,5,6,6 (boss variant of 1; ALLY uses WEAKEST_CREW(0) mid-list)
n_ID 100  CREW 0..6  COND GO(0) x8  ENEMY MOST_DAM(1)/CLOSEST_DAM(0)x4/CLOSEST_CURE(0)/
          CLOSEST_DAM(0)x2  ALLY ME/ME/CLOSEST_CREW...
n_ID 1001 CREW 0 x4  COND PET_AI(1..4)  ENEMY MOST_DAM/MOST_DAM/MASTER_TARGET/MOST_DAM  ALLY ME x4
n_ID 1002 same as 1001 but ALLY MASTER(0) x4   (pet variants)
n_ID 9903 CREW 0  COND GO(0)  ENEMY CLOSEST_DAM(0)  ALLY ME(0)
```
MOBS usage: 1852 mobs use tactic 1; 1326 use 0 (none); 15 use 11; 8/7 use pet tactics 1001/1002.

### AI_COMBAT (026, 276 rows x 3): n_ID, s_CONDITOIN (sic), s_ACTION - 5 sample rows
```
n_ID 1: COND GO(0)                                        ACTION CHASE(1)
n_ID 2: COND GO(0)                                        ACTION CHASE(1)
n_ID 3: COND RATE(25)/RATE(33)/RATE(50)/RATE(90)/GO(0)    ACTION CHASE(1)/CHASE(2)/CHASE(3)/CHASE(4)/CHASE(1)
n_ID 4: COND BUFF_I(4984,0,0)/BUFF_I(4990,0,0)/GO(0)      ACTION CHASE(1)/CHASE(2)/CHASE(3)
n_ID 5: COND BUFF_I(4981,0,0);HP_I<(0.8);RATE(25)/GO(0)   ACTION CHASE(2)/CHASE(1)
```
Plus boss row 335 shown in section 2. MOB_TALK (030, 9 rows: n_ID, s_EVENT, s_CONDITION,
s_TALK, s_WARNING) triggers talk lines off `BEHAVIOR(id)` events (e.g. row n_ID=187:
s_EVENT `BEHAVIOR(8010)/BEHAVIOR(8015)/BEHAVIOR(8016)`), tying mob barks to BEHAVIOR playback.

## 5. LOOT

### The id-encoding rule (PROVEN on full data)
`MOBS.n_DROPS_* = prefix*100000 + n_ID of a row in the matching DROPS_* table`:
- n_DROPS_NORMAL: all values prefix 27; all 62 distinct low-parts resolve in DROPS_NORMAL.n_ID (62/62).
- n_DROPS_SPECIALLY: prefix 28; 107/107 low-parts resolve in DROPS_SPECIALLY.
- n_DROPS_EQUIPMENT: prefix 54; 36/36 low-parts resolve in DROPS_EQUIPMENT.
- n_DROPS_QUEST: prefix 87; only 311 of 2478 distinct low-parts resolve in DROPS_QUEST -> see honesty note.
Item ids inside drop tables use the same scheme (prefix = item category table):
22 -> EQUIPMENT_BASE (2200201 -> 201 verified), 24 -> ITEM_CONSUMABLES (2400046 -> 46 verified),
25 -> ITEM_QUEST (2500021 -> 21 verified), 26 -> ITEM_MISC (2600041 -> 41 verified).
n_ITEM = 0 with nonzero rate/min/max [INFERENCE] = money drop slot.

### DROPS_ACTIVITY (003, 4 rows x 11, linked TIP DROPS_ACTIVITY_TIP) - FULL DUMP
Columns: n_ID, n_MODIFY, n_MOB_MIN, n_MOB_MAX, n_MOBRANK, n_DROPS_QUEST, n_DROPS_NORMAL, s_HK/TC/JP/TH_VER
```
n_ID=1  MODIFY=1 MOB_MIN=1 MOB_MAX=999 MOBRANK=1    DROPS_QUEST=0 DROPS_NORMAL=2700121 VER TH 1.07
n_ID=2  MODIFY=1 MOB_MIN=1 MOB_MAX=999 MOBRANK=6    DROPS_QUEST=0 DROPS_NORMAL=2700122 VER TH 1.07
n_ID=3  MODIFY=1 MOB_MIN=1 MOB_MAX=999 MOBRANK=192  DROPS_QUEST=0 DROPS_NORMAL=2700123 VER TH 1.07
n_ID=11 MODIFY=1 MOB_MIN=1 MOB_MAX=999 MOBRANK=4095 DROPS_QUEST=0 DROPS_NORMAL=2700124 VER HK/TC/JP=OUT TH=1.10
```
n_MOBRANK is a bitmask over MOBS.n_RANK (1, 2|4=6, 64|128=192, 4095=all normal ranks).
The referenced extra drop sets 2700121..2700124 -> DROPS_NORMAL rows 121-124, all present.
Reading: event-time bonus drop sets layered on mobs by rank band [INFERENCE].

### Drop-table schemas + samples
- DROPS_NORMAL (049, 267 x 121): n_ID + 30 slots of (n_ITEM_i, f_RATE_i, n_MIN_i, n_MAX_i).
  Per-slot independent percentage rates.
  Row n_ID=1: item0(money) rate 100 min 15 max 25; money rate 50 min 5 max 10; money rate 20 min 5 max 10.
  Row n_ID=1001 (used by Port Royal hostiles via 2701001): 2400046 (consumable 46) 30 pct x1;
  2400047 15 pct x1; 2600701 (misc 701) 0.5 pct x1; 2600751 0.5 pct x1; money 1 pct x1.
- DROPS_EQUIPMENT (048, 53 x 44): n_ID, f_DROPS_RATE, n_NUMBER_MIN/MAX + 20 x (n_ITEM_i, n_WEIGHT_i).
  One roll at f_DROPS_RATE then weighted pick. Row n_ID=1: rate 50 pct, 1 item, 15 equipment
  entries (2200201, 2200401, ... all EQUIPMENT_BASE refs) weight 100 each.
- DROPS_SPECIALLY (050, 584 x 64): same weighted-pick shape as equipment but 30 slots:
  n_ID, f_DROPS_RATE, n_NUMBER_MIN/MAX + 30 x (n_ITEM_i, n_WEIGHT_i).
  Row n_ID=1: rate 100 pct, 1-3 items, 2600041 w15 / 2600042 w40 / 2600043 w45.
- DROPS_QUEST (096, 311 x 101): n_ID + 20 x (n_ITEM_i, n_LIMIT_i, n_QUESTID_i, n_M_BUFF_i, f_RATE_i).
  Quest-gated drops: item only drops while quest n_QUESTID active and below n_LIMIT [INFERENCE].
  Row n_ID=27: 2500021 limit 5 quest 54 rate 100; 2500030 limit 10 quest 82 rate 100.
  KEY OBSERVATION: DROPS_QUEST.n_ID equals the MOB id (all 311 ids are MOBS n_IDs), and
  2472/2596 mobs set n_DROPS_QUEST = 8700000 + their own n_ID (the other 124 point at
  another mob's set).
- E_DROPS_QUALITY (054, 26 x 9): n_ID, n_MOB_RANK, n_MOB_LEVELMIN/MAX, n_WEIGHT_W/G/B/P/O -
  equipment-drop quality (White/Green/Blue/Purple/Orange) by mob rank + level band. Full table:
```
  1: rank1    lvl 1-15    W80 G20 | 2: rank1 16-30 W80 G20 | 3: rank1 31-50 W50 G50
  4: rank1    lvl 51-80   W60 G40 | 5: rank1 81-100 W70 G30 | 6: rank1 101-120 W75 G25
  7: rank1    lvl 121-130 W75 G25 | 8: rank1 131-999 W75 G25
  101: rank2  1-125  G100         | 102: rank2 126-999 G98 B2
  201: rank4  1-125  B100         | 202: rank4 126-999 B98 P2
  301: rank8  P100 | 401: rank16 P100 | 501: rank32 P100
  601: rank64 1-50 G70 B30 | 602: 51-70 G80 B20 | 603: 71-125 G90 B10 | 604: 126-999 G90 B8 P2
  701: rank128 1-130 B90 P10 | 702: 131-999 B90 P10
  801: rank256 P100 | 901: rank512 G70 B30 | 1001: rank1024 P100 | 1101: rank2048 G95 B5
  1201: rank4096 G700 B299 P1   (weights not normalized to 100 here)
```
- Other reward tables: DAILY_REWARD (064, 78 x 94: level-banded weighted item packages),
  ONLINE_REWARD (065, 8 x 3: n_ID/n_TYPE/n_TIME), DAILY_INFO_REWARD (066, 7 x 26:
  day/condition/reward), GET_SHIPCORPSE (111, 8 x 11: area/level-band ship corpse salvage),
  RANK_REWARD (118, schema only, 0 rows shipped).

### Honest assessment: do the client tables model loot?
YES for content: the client const data contains the complete drop MODEL for normal/equipment/
special drops - drop rates, quantity ranges, item weights, and quality weights. Every mob
drop-set reference for those three categories resolves inside the client tables (62/62, 36/36,
107/107). This is not presentation-only data; the numbers are sufficient to roll loot.
PARTIAL [NEGATIVE] for quest drops: mobs reference 2478 distinct quest-drop sets but the shipped
DROPS_QUEST table contains only 311 - so ~87 pct of quest-drop sets are absent client-side
(server-only or stripped).
[UNKNOWN]: whether the original game rolls loot client-side or server-side cannot be decided
from data alone; no client-code binding was traced in this run. For our server rebuild the
tables are directly usable as the authoritative drop model.

## 6. FACTION / CAMP (table 085, 38 rows x 2: n_ID, s_ENEMY) - ALL ROWS

s_ENEMY is a semicolon list of enemy faction ids; '0' = no enemies.
```
 1 -> 6;11;12;17;18;26      11 -> 1            21 -> 20        101 -> 102
 2 -> 3;6                   12 -> 0            22 -> 23        102 -> 101
 3 -> 2;6                   13 -> 0            23 -> 0         103 -> 104
 4 -> 0                     14 -> 4            24 -> 0         104 -> 103
 5 -> 6                     15 -> 6;16         25 -> 26        105 -> 103
 6 -> 1;2;3;12;13;18        16 -> 0            26 -> 25;1;2;3  999 -> 0
 7 -> 1;8                   17 -> 1            27 -> 11
 8 -> 7                     18 -> 1;2;3;12;13;6 28 -> 12
 9 -> 7;10                  19 -> 4            29 -> 0
10 -> 1                     20 -> 21           30 -> 0
                                               31 -> 7;29
                                               32 -> 7;30
```
ANSWER (GT-032 prediction): faction 6 IS an enemy of faction 1, MUTUALLY.
FACTION row n_ID=1 s_ENEMY contains 6 ("6;11;12;17;18;26") and row n_ID=6 s_ENEMY contains 1
("1;2;3;12;13;18"). If the player camp is faction 1 (218 MOBS rows also carry faction 1 via
AI_WANDER rows 3-8/37/1001-1003/9903/9904 - guard/companion style entries), the relation lookup
returns hostile for faction-6 monsters in both directions. Prediction for GT-032: HOSTILE = YES.
Note asymmetries exist elsewhere (e.g. 12 lists no enemies but 6 lists 12; 105 lists 103 but
103 lists only 104), so the lookup direction matters for edge factions - not for 1 vs 6.

MOBS faction values (via MOBS.n_AI_WANDER -> AI_WANDER.n_FACTION, all 3210 rows):
faction 6: 1716 rows; faction 4 (no enemies - town/critter): 1114; faction 1: 218;
faction 17: 26; faction 7: 25; faction 10: 16; faction 5: 13; factions 8/12: 6 each;
faction 11: 5; 13/101/102: 4; 15/19/22/26: 3; 9/16/18/21(x1)/23/25(x1)/27/29(x1)/30(x1)/31/32/
104/105: 1-2 each; 17 rows n_AI_WANDER=0 -> faction [UNKNOWN].
FACTION table covers ids 1-32, 101-105, 999; every faction used by AI_WANDER exists in FACTION.

## 7. Port Royal placements (bg0001_npc_placements_decoded.tsv + frozen server source)

TSV: 149 placement records (+1 header), columns idx, name, f0-f5 (x, y, z, facing?, PatrolRange,
TraceRange - matches handoff section 11 values), u16_0..u16_6, extra, groups, points.
All names are "Mob_Set_NN xx". u16_0=0, u16_1..u16_4=1 for all rows; u16_5=10 (141 rows) or 0
(8 rows); u16_6 = scene-local sequence (2..147); extra = 1 (116 rows) / 0 (33 rows)
[UNKNOWN semantics]; 11 records carry patrol point lists (e.g. idx 43 "Mob_Set_44 02").

Identity/template resolution (from `src/pirateforce_foundation/population.py` and the frozen
115-row source `PORT_ROYAL_UNAMBIGUOUS_PLACEMENTS` in `current/pf_login_game_server_v141.py`
line 1323, sha256-pinned 22D7430E...9618):
- actor_identity = 0x2000 + placement_index + 1, so 0x2001 = placement idx 0 = "Mob_Set_01 01".
- template_id = the NN in Mob_Set_NN = MOBS.n_ID (frozen row (0, 1, -9139.957..., -2780.045...,
  223.292..., 'P_MALE_002_000_SP1', 'Navy Transfer')).
- 115 frozen placements; template ids span 1..113, 88 distinct, ALL resolve in MOBS.

Placed population profile (join template -> MOBS -> AI_WANDER):
- 102 placements are faction 4 (no enemies) - town NPCs; n_MOB_USAGE mostly 2.
- 13 placements are faction 6 (hostile), all with combat AI + skills + drop sets:
```
pidx  identity tid name                        lvl    AI w/c/t     DROPS N/E/S
 12   0x200D   35  Fighting Fish Sergeant      27     16/352/1     2701001/5400001/2802264
 30   0x201F   31  Tornado Eagle               27     16/214/1     2701001/5400001/2802234
 33   0x2022   34  Fighting Fish soldier       25-27  16/350/1     2701001/5400001/2802264
 58   0x203B   60  Jungle Big Tiger            37-39  11/123/1     2701002/5400002/2802208
 59   0x203C   61  Toxic Vine                  38-40  16/140/1     2701002/5400002/2802219
 60   0x203D   62  Ancient Civ. Alert Weapon   39-41  16/240/1     2701002/5400002/0
 63   0x2040   65  Ward Apes                   43-45  11/133/1     2701002/5400002/2802215
 95   0x2060   94  An Gebo Little Firebird     47-49  16/300/1     2701003/5400002/2802253
103   0x2068   97  Mutant Green Eagle          51-53  16/214/1     2701003/5400003/2802236
105   0x206A   97  Mutant Green Eagle          51-53  (same row)
107   0x206C   97  Mutant Green Eagle          51-53  (same row)
109   0x206E   97  Mutant Green Eagle          51-53  (same row)
132   0x2085  103  Orc Chief                   58-60  11/332/1     2701003/5400003/0
```
  All their drop refs resolve client-side (e.g. 2701001 -> DROPS_NORMAL row 1001, dumped in
  section 5). AI_WANDER 16 = faction 6, non-offensive, aggro 0 (retaliate-only);
  AI_WANDER 11 = faction 6, offensive, aggro 1200 (attacks on approach).

First Port Royal NPC (identity 0x2001, template MOBS n_ID=1, MOBS_TIP name "Navy Transfer",
s_NAME = \u6d77\u8ecd\u50b3\u9001\u5175):
```
n_LEVEL_MIN/MAX = 20/20  n_RANK = 0  n_MOB_USAGE = 2 (NPC)
n_AI_WANDER = 2 (-> FACTION=4, OFFESIVE=0, AGGRO=0, wander IDLE;9;15 / RUN;0;1)
n_AI_COMBAT = 0  n_AI_TACTIC = 0  s_SKILLS = "" (no combat AI)
n_DROPS_EQUIPMENT/NORMAL/SPECIALLY = 0  n_DROP_RANGE = 200
n_DROPS_QUEST = 8700001 -> low part 1 is NOT in client DROPS_QUEST (min shipped id is 27)
  -> quest-drop set for this NPC absent client-side [NEGATIVE]
s_OUTFIT = P_MALE_002_000_SP1 (matches frozen visual preset)  s_PREDESCRIPT = P_MALE_FIST
n_SPEED_WALK/RUN = 150/650  s_QUEST_BEGIN/END = 3020/3020  s_NPC_VOICE = 160
```
So the first placed NPC has wander AI only, no combat AI, no lootable drop tables - consistent
with a town service NPC; the 13 faction-6 placements above are the mobs that matter for
monster-side tests in Port Royal.

## FILES TOUCHED

Read-only inputs (never modified):
- .../backups/v103_one_item_backpack_20260814_103143/derived/v97_mapping_audit/B_CONSTDATA_TH.pc_.dec
- .../v97_mapping_audit/parse_pc_tables.py, MOBS.json, MOBS_TIP.json, MOBS_parse.txt,
  const_high_value.json (not needed in the end), const_high_value_tables.txt,
  B_CONSTDATA_tables.txt, bg0001_npc_placements_decoded.tsv,
  client_tables/07_MOBS_and_Client_Data_Notes.md
- .../backups/v103_one_item_backpack_20260814_103143/handoff.txt
- Pirate Force ServerProject/src/pirateforce_foundation/population.py
- Pirate Force ServerProject/current/pf_login_game_server_v141.py

Scratch (isolated /tmp, not on user filesystem):
- /tmp/pf/parse_hardened.py (hardened copy), /tmp/pf/const.dec (copy),
  /tmp/pf/full_inventory.txt, /tmp/pf/dump1.json, /tmp/pf/items.json, /tmp/pf/sk.json,
  /tmp/pf/mobs.json (copy)

Written output (single file):
- /sessions/friendly-dreamy-hopper/mnt/outputs/r100_agentB_constdata_monster_loot.md (this file)

No git mutations. No server boot. No LOCK_* files. pirateforce.sqlite3 untouched.
