# PF monster presentation - source-separated P0-7 checkpoint

[MEASURED][LOCAL TOOLING] P0-7 status: **PARTIAL / CHECKPOINT_2**. It publishes 8,950 deterministic, source-separated rows (8,940 DATA; 10 IMAGE). CHECKPOINT_2 adds 6,248 authored placement-group records, four CLINE map-list projection ambiguity guards, and one manager-identity-sensitive f_SCALE census row. All 2,697 CHECKPOINT_1 rows retain every prior column value and key.

[MEASURED][LOCAL TOOLING] Method/control: guard the pinned GameClient image by size/SHA-256/mtime before and after; revalidate all 289 original `.npc` files against the pinned scene index and source manifest; validate all 289 derived placement TSVs against their pinned manifest; derive descriptor names only from the guarded MOBS s_OUTFIT corpus; decode XML only in memory; and restrict IMAGE claims to exact pinned evidence windows. No client, server, dump, capture, or runtime execution was used.

- [MEASURED][IMAGE] Image SHA-256: `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`.
- [MEASURED][DATA] Original scene source manifest: `47fbf59d311bfecac92c3f2487c84a36a1cfa8acabc9577f5e0963b9f618d3bc`; derived placement manifest: `e97c34aa7419c5cf0deab96ece6fbbe4d059e77ad7f2e55599272af0a5e8770a`.
- [MEASURED][DATA] Authored placement groups: 6,248 across 268 nonempty scene files; 21 additional guarded scene files have zero base placement rows (289 files total). Exactly 6,230 groups have a lexical Mob/Monster marker in the literal name or set-name tokens; 18 do not. These are authored groups, not actors, spawns, models, monsters, live density, or a current server roster.
- [MEASURED][DATA] 238 base placement records carry 7,194 preserved extra triples, and two placement rows retain the literal decoder result `UNRESOLVED` in `placement_template_ids`. Extra triples are not actors/spawns or additional authored groups; `UNRESOLVED` is only decoder token-resolution status and is not an unknown actor class or identity.
- [MEASURED][DATA] Lexical M### outfit references: 2,686 across 2,186 MOBS rows; 615 distinct descriptors. A lexical `M###` prefix is a corpus-selection rule, not proof of a concrete monster class.
- [MEASURED][DATA] Explicit non-M target: Pike MOBS ID 5 (`P_MALE_002_000_PAK`).
- [MEASURED][LOCAL TOOLING] Guarded descriptors: 616 total. `lexical_M_token_keyset_sha256=5418f7cbcba3105faf62d093eab8b0a5777b7f640bba00860c81cf6ec6a68be7` covers only the 615 lexical M descriptors; Pike is the additional guarded descriptor.
- [MEASURED][DATA] Weighted active classes: READY 2167, SENTRY 286, ATTACK 74, WALK 55, TALK 43, HAPPY 23, NO_ACTIVE 17, DIE 13, FORWARD 8.
- [MEASURED][DATA] Distinct-asset active classes: READY 489, SENTRY 77, ATTACK 14, WALK 14, TALK 4, HAPPY 4, NO_ACTIVE 5, DIE 2, FORWARD 6.
- [MEASURED][DATA] n_BOUNDARY: 3210 numeric rows, 33 distinct, min 1, max 1600.
- [MEASURED][DATA] n_HEIGHT: 3210 numeric rows, 71 distinct, min 1, max 2600.

## Authored placement-group census

[MEASURED][DATA] Each decoded base placement row is counted once. `extra_triple_count` is preserved but is never added to actor/spawn cardinality. SCENE_NAME and CLINE are not generalized into world-actor identity. The four Bg0002 guards prove why: template tokens `38/39/40/41` project through the client map-list crosswalk to distinct MOBS candidates `231/742/743/914`; both candidate s_OUTFIT vectors are preserved, but neither candidate is promoted to placement identity.

| Scene | Authored groups | Lexical markers | Nonlexical | Extra-triple records (not actors) |
|---|---:|---:|---:|---:|
| AirTest | 19 | 16 | 3 | 0 |
| AirTest01 | 0 | 0 | 0 | 0 |
| AirTest02 | 4 | 4 | 0 | 0 |
| AitTest03 | 24 | 24 | 0 | 0 |
| AlbertTest | 51 | 51 | 0 | 0 |
| bg0001 | 149 | 149 | 0 | 710 |
| Bg0002 | 106 | 106 | 0 | 0 |
| Bg0003 | 72 | 72 | 0 | 0 |
| bg0004 | 116 | 116 | 0 | 1 |
| bg0005 | 92 | 92 | 0 | 0 |
| bg0006 | 80 | 80 | 0 | 0 |
| Bg0007 | 68 | 68 | 0 | 0 |
| Bg0008 | 76 | 76 | 0 | 0 |
| Bg0009 | 63 | 63 | 0 | 0 |
| Bg0010 | 100 | 100 | 0 | 0 |
| Bg0011 | 56 | 56 | 0 | 0 |
| Bg0012 | 67 | 67 | 0 | 0 |
| Bg0015 | 91 | 91 | 0 | 0 |
| Bg0016 | 74 | 74 | 0 | 0 |
| bg0017 | 61 | 61 | 0 | 0 |
| bg0020 | 93 | 93 | 0 | 0 |
| Bg0021 | 105 | 105 | 0 | 0 |
| Bg0022 | 69 | 69 | 0 | 0 |
| Bg0023 | 80 | 80 | 0 | 0 |
| Bg0030 | 0 | 0 | 0 | 0 |
| Bg0031 | 0 | 0 | 0 | 0 |
| Bg0032 | 0 | 0 | 0 | 0 |
| Bg0033 | 0 | 0 | 0 | 0 |
| Bg1001 | 8 | 8 | 0 | 0 |
| Bg1002 | 8 | 8 | 0 | 11 |
| Bg1003 | 8 | 8 | 0 | 16 |
| Bg1004 | 10 | 10 | 0 | 0 |
| Bg1005 | 13 | 13 | 0 | 0 |
| Bg1006 | 20 | 20 | 0 | 12 |
| Bg1007 | 12 | 12 | 0 | 0 |
| Bg1008 | 6 | 6 | 0 | 0 |
| Bg1009 | 9 | 9 | 0 | 9 |
| Bg1010 | 14 | 14 | 0 | 8 |
| Bg1011 | 8 | 8 | 0 | 0 |
| Bg1012 | 8 | 8 | 0 | 8 |
| Bg1013 | 16 | 16 | 0 | 0 |
| Bg1014 | 15 | 15 | 0 | 0 |
| Bg1016 | 12 | 12 | 0 | 0 |
| Bg1017 | 11 | 11 | 0 | 0 |
| Bg1018 | 12 | 12 | 0 | 0 |
| Bg1019 | 20 | 20 | 0 | 0 |
| Bg1020 | 27 | 27 | 0 | 0 |
| Bg1021 | 12 | 12 | 0 | 0 |
| Bg1022 | 22 | 22 | 0 | 0 |
| Bg1023 | 11 | 11 | 0 | 0 |
| Bg1024 | 37 | 37 | 0 | 0 |
| Bg1025 | 10 | 10 | 0 | 0 |
| Bg1026 | 21 | 21 | 0 | 0 |
| Bg1027 | 17 | 17 | 0 | 0 |
| Bg1028 | 14 | 14 | 0 | 0 |
| Bg1029 | 12 | 12 | 0 | 0 |
| Bg1030 | 11 | 11 | 0 | 2 |
| Bg1031 | 9 | 9 | 0 | 0 |
| Bg1032 | 13 | 13 | 0 | 0 |
| Bg1033 | 16 | 16 | 0 | 0 |
| Bg1034 | 16 | 16 | 0 | 0 |
| Bg1035 | 14 | 14 | 0 | 0 |
| Bg1036 | 12 | 12 | 0 | 0 |
| Bg1037 | 19 | 19 | 0 | 0 |
| Bg1038 | 21 | 21 | 0 | 0 |
| Bg1039 | 23 | 23 | 0 | 0 |
| Bg1040 | 17 | 17 | 0 | 0 |
| Bg1041 | 19 | 19 | 0 | 0 |
| Bg1042 | 24 | 24 | 0 | 0 |
| Bg1043 | 22 | 22 | 0 | 0 |
| Bg1044 | 18 | 18 | 0 | 0 |
| Bg1045 | 40 | 40 | 0 | 0 |
| Bg1046 | 10 | 10 | 0 | 0 |
| Bg1047 | 7 | 7 | 0 | 0 |
| Bg1048 | 11 | 11 | 0 | 0 |
| Bg1049 | 16 | 16 | 0 | 12 |
| Bg1050 | 18 | 18 | 0 | 11 |
| Bg1051 | 9 | 9 | 0 | 0 |
| Bg1052 | 9 | 9 | 0 | 10 |
| Bg1053 | 13 | 13 | 0 | 9 |
| Bg1054 | 7 | 7 | 0 | 0 |
| Bg1055 | 5 | 5 | 0 | 0 |
| Bg1056 | 18 | 18 | 0 | 14 |
| Bg1057 | 14 | 14 | 0 | 0 |
| Bg1058 | 12 | 12 | 0 | 0 |
| Bg1059 | 12 | 12 | 0 | 0 |
| Bg1060 | 19 | 19 | 0 | 0 |
| Bg1061 | 9 | 9 | 0 | 0 |
| Bg1062 | 11 | 11 | 0 | 0 |
| Bg1063 | 13 | 13 | 0 | 0 |
| Bg1064 | 13 | 13 | 0 | 0 |
| Bg1065 | 14 | 14 | 0 | 0 |
| Bg1066 | 21 | 21 | 0 | 0 |
| Bg1067 | 9 | 9 | 0 | 0 |
| Bg1068 | 18 | 18 | 0 | 0 |
| Bg1069 | 21 | 21 | 0 | 0 |
| Bg1070 | 14 | 14 | 0 | 0 |
| Bg1071 | 16 | 16 | 0 | 0 |
| Bg1072 | 19 | 19 | 0 | 0 |
| Bg1073 | 10 | 10 | 0 | 0 |
| Bg1074 | 11 | 11 | 0 | 0 |
| Bg1075 | 17 | 17 | 0 | 0 |
| Bg1076 | 17 | 17 | 0 | 0 |
| Bg1077 | 15 | 15 | 0 | 0 |
| Bg1078 | 27 | 27 | 0 | 0 |
| Bg1079 | 14 | 14 | 0 | 0 |
| Bg1080 | 21 | 21 | 0 | 0 |
| Bg1081 | 19 | 19 | 0 | 0 |
| Bg1082 | 19 | 19 | 0 | 0 |
| Bg1083 | 21 | 21 | 0 | 0 |
| Bg1084 | 19 | 19 | 0 | 0 |
| Bg1085 | 22 | 22 | 0 | 0 |
| Bg1086 | 20 | 20 | 0 | 0 |
| Bg1087 | 23 | 23 | 0 | 0 |
| Bg1088 | 25 | 25 | 0 | 0 |
| Bg1089 | 20 | 20 | 0 | 0 |
| Bg1090 | 19 | 19 | 0 | 0 |
| Bg1091 | 21 | 21 | 0 | 0 |
| Bg1092 | 19 | 19 | 0 | 0 |
| Bg1093 | 21 | 21 | 0 | 0 |
| Bg1094 | 23 | 23 | 0 | 0 |
| Bg1095 | 34 | 34 | 0 | 0 |
| Bg1096 | 1 | 1 | 0 | 0 |
| Bg1097 | 8 | 8 | 0 | 21 |
| Bg1098 | 7 | 7 | 0 | 0 |
| Bg1099 | 1 | 1 | 0 | 7 |
| Bg1100 | 4 | 4 | 0 | 0 |
| Bg1101 | 4 | 4 | 0 | 0 |
| Bg1102 | 3 | 3 | 0 | 0 |
| Bg1103 | 6 | 6 | 0 | 0 |
| Bg1104 | 1 | 1 | 0 | 0 |
| Bg1105 | 4 | 4 | 0 | 10 |
| Bg1106 | 11 | 11 | 0 | 0 |
| Bg1107 | 2 | 2 | 0 | 0 |
| Bg1108 | 3 | 3 | 0 | 0 |
| Bg1109 | 3 | 3 | 0 | 0 |
| Bg1110 | 3 | 3 | 0 | 0 |
| Bg1111 | 4 | 4 | 0 | 0 |
| Bg1112 | 4 | 4 | 0 | 0 |
| Bg1113 | 1 | 1 | 0 | 0 |
| Bg1114 | 9 | 9 | 0 | 0 |
| Bg1115 | 5 | 5 | 0 | 0 |
| Bg1116 | 10 | 10 | 0 | 0 |
| Bg1117 | 5 | 5 | 0 | 0 |
| Bg1118 | 6 | 6 | 0 | 28 |
| Bg1119 | 4 | 4 | 0 | 0 |
| Bg1120 | 11 | 11 | 0 | 0 |
| Bg1121 | 10 | 10 | 0 | 0 |
| Bg1122 | 8 | 8 | 0 | 4 |
| Bg1124 | 10 | 10 | 0 | 0 |
| Bg1125 | 9 | 9 | 0 | 50 |
| Bg1126 | 14 | 14 | 0 | 0 |
| Bg1127 | 13 | 13 | 0 | 0 |
| Bg1128 | 11 | 11 | 0 | 0 |
| Bg1129 | 12 | 12 | 0 | 0 |
| Bg1130 | 20 | 20 | 0 | 0 |
| Bg1131 | 3 | 3 | 0 | 0 |
| Bg1132 | 17 | 17 | 0 | 0 |
| Bg1133 | 10 | 10 | 0 | 0 |
| Bg1134 | 18 | 18 | 0 | 0 |
| Bg1135 | 12 | 12 | 0 | 0 |
| Bg1136 | 12 | 12 | 0 | 0 |
| Bg1137 | 10 | 10 | 0 | 0 |
| Bg1138 | 10 | 10 | 0 | 0 |
| Bg1139 | 9 | 9 | 0 | 78 |
| Bg1140 | 9 | 9 | 0 | 52 |
| Bg1141 | 13 | 13 | 0 | 0 |
| Bg1142 | 10 | 10 | 0 | 0 |
| Bg1143 | 7 | 7 | 0 | 0 |
| Bg1144 | 17 | 17 | 0 | 0 |
| Bg1145 | 11 | 11 | 0 | 0 |
| Bg1146 | 15 | 15 | 0 | 0 |
| Bg1147 | 21 | 21 | 0 | 0 |
| Bg1148 | 15 | 15 | 0 | 0 |
| Bg1149 | 13 | 13 | 0 | 0 |
| Bg1150 | 13 | 13 | 0 | 0 |
| Bg1151 | 13 | 13 | 0 | 0 |
| Bg1152 | 16 | 16 | 0 | 0 |
| Bg1153 | 15 | 15 | 0 | 0 |
| Bg1154 | 1 | 1 | 0 | 0 |
| Bg1155 | 9 | 9 | 0 | 0 |
| Bg1156 | 14 | 14 | 0 | 0 |
| Bg1157 | 18 | 18 | 0 | 0 |
| Bg1158 | 1 | 1 | 0 | 0 |
| Bg1159 | 1 | 1 | 0 | 0 |
| Bg1160 | 1 | 1 | 0 | 0 |
| Bg1161 | 0 | 0 | 0 | 0 |
| Bg1162 | 5 | 5 | 0 | 0 |
| Bg1163 | 3 | 3 | 0 | 0 |
| Bg1164 | 5 | 5 | 0 | 172 |
| Bg1165 | 1 | 1 | 0 | 0 |
| Bg1166 | 17 | 17 | 0 | 142 |
| Bg1167 | 11 | 11 | 0 | 0 |
| Bg1168 | 5 | 5 | 0 | 0 |
| Bg1169 | 0 | 0 | 0 | 0 |
| Bg1170 | 15 | 15 | 0 | 0 |
| Bg1171 | 7 | 7 | 0 | 0 |
| Bg1172 | 8 | 8 | 0 | 0 |
| Bg1173 | 10 | 10 | 0 | 0 |
| Bg1174 | 0 | 0 | 0 | 0 |
| Bg1175 | 4 | 4 | 0 | 0 |
| Bg1176 | 4 | 4 | 0 | 0 |
| Bg1177 | 9 | 9 | 0 | 0 |
| Bg1178 | 168 | 168 | 0 | 0 |
| Bg1179 | 1 | 1 | 0 | 0 |
| Bg1180 | 37 | 37 | 0 | 0 |
| Bg1181 | 0 | 0 | 0 | 0 |
| Bg1182 | 2 | 2 | 0 | 0 |
| Bg1183 | 11 | 11 | 0 | 0 |
| Bg1184 | 1 | 1 | 0 | 0 |
| Bg1185 | 1 | 1 | 0 | 0 |
| Bg1186 | 21 | 21 | 0 | 0 |
| Bg1187 | 21 | 21 | 0 | 0 |
| Bg1188 | 8 | 8 | 0 | 32 |
| Bg1189 | 10 | 10 | 0 | 0 |
| Bg1190 | 28 | 28 | 0 | 108 |
| Bg1191 | 2 | 2 | 0 | 0 |
| Bg1192 | 11 | 11 | 0 | 0 |
| Bg1193 | 20 | 20 | 0 | 0 |
| Bg1194 | 12 | 12 | 0 | 0 |
| Bg1195 | 11 | 11 | 0 | 0 |
| Bg1196 | 10 | 10 | 0 | 0 |
| Bg1197 | 17 | 17 | 0 | 0 |
| Bg1198 | 12 | 12 | 0 | 0 |
| Bg1199 | 9 | 9 | 0 | 0 |
| Bg1200 | 16 | 16 | 0 | 0 |
| Bg1201 | 14 | 14 | 0 | 0 |
| Bg1202 | 19 | 19 | 0 | 0 |
| Bg1203 | 23 | 23 | 0 | 0 |
| Bg1204 | 18 | 18 | 0 | 0 |
| Bg1205 | 19 | 19 | 0 | 0 |
| Bg1206 | 13 | 13 | 0 | 0 |
| Bg1207 | 14 | 14 | 0 | 0 |
| Bg1208 | 21 | 21 | 0 | 0 |
| Bg1209 | 18 | 18 | 0 | 0 |
| Bg1210 | 14 | 14 | 0 | 0 |
| Bg1211 | 19 | 19 | 0 | 0 |
| bg2001 | 41 | 41 | 0 | 79 |
| Bg2002 | 67 | 67 | 0 | 46 |
| bg2003 | 18 | 18 | 0 | 0 |
| bg2004 | 64 | 64 | 0 | 57 |
| Bg2006 | 227 | 227 | 0 | 86 |
| bg2007 | 72 | 72 | 0 | 11 |
| Bg2008 | 54 | 54 | 0 | 0 |
| Bg2009 | 36 | 36 | 0 | 0 |
| Bg2010 | 25 | 25 | 0 | 144 |
| bg2012 | 0 | 0 | 0 | 0 |
| bg2013 | 43 | 43 | 0 | 0 |
| bg2014 | 18 | 18 | 0 | 0 |
| Bg2015 | 57 | 57 | 0 | 169 |
| Bg2016 | 240 | 240 | 0 | 30 |
| Bg2017 | 91 | 91 | 0 | 0 |
| Bg2018 | 68 | 68 | 0 | 286 |
| Bg2020 | 4 | 4 | 0 | 0 |
| bg2021 | 0 | 0 | 0 | 0 |
| Bg2030 | 0 | 0 | 0 | 0 |
| Bg2031 | 0 | 0 | 0 | 0 |
| Bg2032 | 44 | 44 | 0 | 79 |
| Bg2033 | 0 | 0 | 0 | 0 |
| Bg3001 | 38 | 38 | 0 | 814 |
| Bg3002 | 39 | 39 | 0 | 844 |
| Bg3003 | 42 | 42 | 0 | 819 |
| Bg3004 | 46 | 46 | 0 | 98 |
| Bg3005 | 22 | 22 | 0 | 332 |
| Bg3006 | 0 | 0 | 0 | 0 |
| Bg3007 | 66 | 66 | 0 | 656 |
| Bg3008 | 59 | 59 | 0 | 780 |
| Bg3009 | 14 | 14 | 0 | 299 |
| Bg4001 | 42 | 42 | 0 | 0 |
| Bg4002 | 1 | 1 | 0 | 0 |
| BG4003 | 9 | 9 | 0 | 14 |
| bg5001 | 0 | 0 | 0 | 0 |
| Bg5002 | 38 | 38 | 0 | 0 |
| Bg5003 | 74 | 74 | 0 | 0 |
| Bg5004 | 30 | 30 | 0 | 0 |
| dupliacte_clear | 1 | 1 | 0 | 0 |
| duplicate | 2 | 2 | 0 | 0 |
| FilmScene | 0 | 0 | 0 | 0 |
| GVGTEST | 3 | 0 | 3 | 0 |
| GVGTEST01 | 0 | 0 | 0 | 0 |
| InstanceTest | 1 | 1 | 0 | 0 |
| MobTest | 18 | 18 | 0 | 0 |
| NoviceTest | 1 | 0 | 1 | 0 |
| PlayerViewer | 0 | 0 | 0 | 0 |
| Prototype | 14 | 14 | 0 | 0 |
| SailingTest | 0 | 0 | 0 | 0 |
| Seatest | 14 | 4 | 10 | 0 |
| TenYooScene | 0 | 0 | 0 | 0 |
| trigger_test | 1 | 0 | 1 | 14 |

## Exact targets

- [MEASURED][DATA] Pike ID 5 stores outfit `P_MALE_002_000_PAK`, boundary/height `75/75`, and AI_WANDER `2`; the shipped six-part composite descriptor has NifFile inventory `.\Data\GC\M\MAN_SKINBONE.nif;.\Data\GC\M\VM_CT_002.nif;.\Data\GC\M\DM_HD_000.nif;.\Data\GC\M\DM_HR_002.nif;.\Data\GC\M\VM_HT_002.nif;.\Data\GC\M\VM_LG_002.nif`, 0 Action entries, and no active action.
- [MEASURED][LOCAL TOOLING] The configured Pike comparison token matches original DATA; runtime selection and rendered equivalence are unproved.
- [MEASURED][DATA] Mountain Deer ID 27 lists `M005_000_000_SP1;M005_000_000_SP2`, boundary/height `110/160`, and AI_WANDER `16`. Both descriptors have 17 actions and the same active class/file metadata `SENTRY` / `.\Data\GC\A\M005_F_SENTRY_000.kf`; this metadata does not prove runtime selection or visual equivalence.

## Counterexamples

- [MEASURED][DATA] MOBS ID 30 pairs `M011_000_000_SP1` (READY) with `M011_000_000_SP2` (DIE).
- [MEASURED][DATA] MOBS ID 1365 pairs `M011_001_000_SP2` (SENTRY) with `M011_001_000_SP3` (DIE).
- [PROPOSED SAFETY RULE] Treat these only as DATA counterexamples; never rename `DIE` as sleep or idle.

## IMAGE boundary and open work

- [MEASURED][IMAGE] Exact named loads establish n_BOUNDARY +0x04, n_HEIGHT +0x08, and s_OUTFIT tokenization into +0x108; separate pinned spans establish the Avatar NifFile/KfFile/ActionList parser surfaces.
- [MEASURED][IMAGE] The f_SCALE key, 0.0 constructor default, and load into MOBS runtime +0x0C remain exact role-only evidence. CHECKPOINT_2 pins the CNetNPC initializer window: `0x0045BF5E` obtains the singleton, `0x0045BF65` calls primary lookup `0x004A1C70`, and `0x0045BF6A` stores the returned MOBS pointer at CNetNPC +0x35C. That bounded window reads several MOBS fields but not +0x0C.
- [MEASURED][IMAGE] The direct-call census finds 13 singleton calls, 68 primary-lookup calls, five immediate singleton-to-primary pairs, and four singleton-to-alternate pairs. Three pinned CNetNPC-related paths use MOBS +0x7C as a key to the different lookup `0x004A1E90`; returned-record +0x0C at `0x0044F8D1` is therefore a secondary-record field, not MOBS f_SCALE. This is a bounded false-join refutation, not whole-function coverage or global absence.
- [MEASURED][IMAGE] The proposed `Actived` candidate at `0x009F939B -> 0x009F9040(1)` is refuted for Avatar use: it is the SceneFogCmp property family.
- [MEASURED][IMAGE] The exact Avatar action parser reads `KfFile` and `GetAllowActionPlus`; it does not read `Action/@Actived` on the bounded path.
- [MEASURED][IMAGE] No type-preserving +0x108 full-token-vector to Avatar registry/active-outfit/action/idle selection bridge is proved. `MONSTER_PRESENTATION@ACTIVE_SELECTION#N` remains the one explicit active unresolved item. Full candidate vectors are preserved in DATA; first-token selection is not claimed as original policy.
- [MEASURED][IMAGE] Exact ASCII/UTF-16 `IDLE` and `s_WANDER` literal checks find no direct named IMAGE action/task consumer. This does not exclude unnamed, indexed, virtual, offset-based, or runtime-only consumers.

## Comparator and status delta

- [MEASURED][LOCAL TOOLING] CHECKPOINT_1 V2 presentation fingerprint: `70cab27f6bcf9c8c1a5895e0f4f751fcecd6026518fd2f0cfba116dae6898bef`; CHECKPOINT_2 V2: `c942fd4ef6d6347b13977a6d503d9fb8886497a13bfd4f6095628068aa8452e7`. V2 includes row/status fields, so its change records expanded evidence/coverage and cannot by itself be read as a semantic closure.
- [MEASURED][LOCAL TOOLING] V3 introduces deterministic status/evidence-independent `subject_id`. Subject-set fingerprint: `9e05ee4153eb9ccb703a467e879fa3b51264b93dda812862942d5f5a7e0b4a37`; subject+status fingerprint: `17d691d8de7b6f096f8cabd22a9a6355802e1be2f3726de620821202126c3222`. Subject IDs are nonempty and unique at the published comparison grain.
- [MEASURED][LOCAL TOOLING] Semantic status closures in this checkpoint: **0**. f_SCALE remains role-only/open for typed effect semantics and active outfit/action/idle selection remains UNKNOWN. The evidence/coverage fingerprint changed, so `no_change_streak=0`; CHECKPOINT_2 establishes the V3 baseline rather than claiming a two-checkpoint stop.

## Nonclaims

[PROPOSED SAFETY RULE] Do not infer original-server selection from token order, call the first outfit a default, multiply authored groups or CLINE count-like fields into spawn density, treat CLINE projection as actor identity, assign collision/physics semantics to n_BOUNDARY/n_HEIGHT, treat f_SCALE zero as a no-op, rename DIE as sleep, or use SceneFog Action/@Actived as Avatar/server policy without a new type-preserving proof.

[MEASURED][LOCAL TOOLING] CHECKPOINT_2 is an evidence/coverage delta, not an UNKNOWN/status closure. A future checkpoint must compare the same V3 subject/status scheme before any no-change stopping rule can be evaluated.
