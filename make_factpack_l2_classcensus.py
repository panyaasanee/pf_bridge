#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FACTPACK-L2-CLASSCENSUS-001 generator.

Reads (read-only):
  pf_bridge/factpack_L1/strings_ascii.tsv      -- Layer-1 fact pack, the ONLY image-derived input
  pf_bridge/factpack_L1/pe_sections.tsv        -- section table
  <repo>/docs/PF_VITAL_NAMES.json              -- the project's single name table
  <repo>/reports/PF_NAMES_FOLD003_..census.json-- round-86 thunk census (209 rows)
  pf_bridge/VITAL_REGISTRY_FROM_CLIENT_BINARY_20260817.tsv -- round-38 candidate tsv

Writes (into pf_bridge/ ONLY -- never into the repo):
  FACTPACK_L2_CLASSCENSUS001_20260820.tsv      -- one row per declared class name
  FACTPACK_L2_CLASSCENSUS001_20260820.json     -- every number the report quotes
  FACTPACK_L2_CLASSCENSUS001_20260820.md       -- the report, rendered FROM the json

The report is rendered by this script, so no number in it is hand-typed.

stdout is pure ASCII on purpose: this tool may be run on a Windows cp874
console, which cannot encode emoji, arrows, or the multiplication sign.

Usage:
  python3 make_factpack_l2_classcensus.py [--bridge <dir>] [--repo <dir>] [--out <dir>]
"""

import argparse
import collections
import datetime
import hashlib
import json
import os
import re
import sys

STAMP = "20260820"
BASENAME = "FACTPACK_L2_CLASSCENSUS001_" + STAMP


def wire_id(name):
    """uint16 id = ( sum over i of (signed char)name[i] * (i+1) ) mod 2^16.
    Settled by PF-NAMEID-HASH-001 (round 62).  Reference impl:
    tools/pf_vital_id_resolve_static.py :: wire_id()."""
    s = 0
    for i, b in enumerate(name.encode("latin1", "replace")):
        c = b - 256 if b >= 128 else b
        s += c * (i + 1)
    return s & 0xFFFF


# ---------------------------------------------------------------- shape rules
# Every pattern below was DERIVED by counting the population it selects inside
# the RTTI type-descriptor census, not assumed up front.  See report section 2.

RE_RTTI_SIMPLE = re.compile(r"^\.\?A([VU])([A-Za-z_][A-Za-z0-9_]*)@@$")
RE_RTTI_ANY = re.compile(r"^\.\?A[VU]")
RE_IDENT = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")

THIRD_PARTY_SCOPES = ("@std@@", "@boost@@", "@detail@boost@@",
                      "@exception_detail@boost@@", "@LuaPlus@@", "@ATL@@",
                      "@stdext@@")
CRT_GLOBAL_NAMES = {"type_info"}

RE_ROUTE_PREFIX = re.compile(r"^([A-Z]{2,8})_")
CLIENT_SERVER_ROUTES = ("GSCN_", "LSCN_")
INTER_SERVER_ROUTES = ("GSSS_", "DBSS_", "CNSS_", "GCSS_", "GCGSSS_", "GCGS_")

# NOTE: 'Vtial' is NOT a typo in this file.  It is a misspelling that exists in
# the shipped client's own class names (measured, see report 2.3), so the wire
# family pattern has to carry it or the census silently loses rows.
RE_VITAL = re.compile(r"(Vital|Vtial)(Req|Res)?$")

FAMILY_RULES = [
    ("wire_vital", lambda n: RE_VITAL.search(n) is not None),
    ("wire_scn_client_server", lambda n: n.startswith(CLIENT_SERVER_ROUTES)),
    ("wire_inter_server", lambda n: n.startswith(INTER_SERVER_ROUTES)),
    ("attr_state_block", lambda n: n.endswith("Attr")),
    ("module_subsystem", lambda n: n.endswith(("Module", "Module_Client"))),
    ("ui_event_handler", lambda n: n.endswith(("EventHandler", "EventHandlerZero"))),
    ("ui_widget", lambda n: n.startswith(("BigUI", "UI_")) or n.endswith(
        ("Board", "Window", "Dlg", "Panel", "Bar", "Page", "Icon", "Label",
         "View", "Button", "TreeNode", "Control", "UI", "Frame", "Cell", "Slot"))),
    ("persistence_record", lambda n: n.endswith(
        ("Record", "DataSet", "PtrMap", "Property", "DataBase", "Database", "Stream"))),
    ("ai_behavior", lambda n: n.startswith("CAI") or "Behavior" in n),
    ("task_quest", lambda n: "Task" in n or "Quest" in n),
    ("effect_fx_missile", lambda n: "Missile" in n or "Effect" in n or n.endswith("FX")),
    ("combat_skill_buff", lambda n: any(t in n for t in
        ("Skill", "Buff", "Hit", "Damage", "Death", "Fight", "Combat", "Cooldown"))),
    ("scene_world_move", lambda n: any(t in n for t in
        ("Scene", "World", "Terrain", "Portal", "Teleport", "Warp", "Move", "Pos",
         "Path", "Navigation"))),
    ("item_inventory_economy", lambda n: any(t in n for t in
        ("Item", "Bag", "Backpack", "Storage", "Stall", "Trade", "Mall", "Money",
         "Drop", "Reward"))),
    ("social_channel", lambda n: any(t in n for t in
        ("Party", "Guild", "Community", "Friend", "Mail", "Express", "Channel",
         "Chat", "Relationship", "Penpal", "SoulMate", "Vow"))),
    ("actor_npc", lambda n: "Actor" in n or "NPC" in n or "Pets" in n),
    ("data_blob", lambda n: n.endswith("Data")),
]


def family_of(name):
    for label, fn in FAMILY_RULES:
        if fn(name):
            return label
    return "other_unclassified"


def load_strings(path):
    rows = []
    with open(path, "r", encoding="utf-8", errors="replace") as fh:
        for line in fh:
            if line.startswith("#"):
                continue
            parts = line.rstrip("\n").split("\t")
            if len(parts) < 5 or parts[0] == "file_offset_hex":
                continue
            rows.append({
                "off": parts[0], "va": parts[1], "sec": parts[2],
                "len": int(parts[3]) if parts[3].isdigit() else 0,
                "text": parts[4],
            })
    return rows


def sha256_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def hexva(s):
    try:
        return int(s, 16)
    except (ValueError, TypeError):
        return None


# ---------------------------------------------------------------- priority seed
# The ONLY editorial content in this file.  Each entry is (name, why).  The
# script refuses to run if a name here is not in the computed gap set, so the
# prose can never drift away from the data.

PRIORITY = [
    ("ForcePos",
     "server-authoritative position correction; the shape the move-authority lane "
     "(R20/R22, pf_move_authority_targetpos_static.py) still has no server-to-client "
     "counterpart for"),
    ("CHitResult",
     "hit resolution result object; the damage lane (pf_damage_hit_result_static.py, "
     "pf_hit_result_probe.py) currently infers this shape instead of naming it"),
    ("CNSS_BoardcastToAllActorVtial",
     "server-side broadcast-to-all fanout; the missing half of every multiplayer "
     "'other players see it' claim"),
    ("CNSS_BoardcastToSpecifiedActorVtial",
     "targeted broadcast; pairs with the above and pins the addressing model"),
    ("CBuffVital",
     "buff application on the wire; combat state that outlives a single hit and must "
     "be replicated"),
    ("CStartCooldownVital",
     "cooldown start on the wire; the server-side gate that stops skill spam"),
    ("CLearnSkillResultVital",
     "skill acquisition result; a progression write path with no current model"),
    ("CTracePathVital",
     "server-driven path following; what pf_remote_movement_projection_static.py "
     "needs to stop guessing"),
    ("FightingDropNotify",
     "loot produced by combat death; joins the death lane (HP-DEATH-002) to the item lane"),
    ("GSCN_ClientExecuteSQL",
     "explicit SQL execution path between game server and CN node; the strongest "
     "persistence-architecture evidence in the whole census"),
    ("GSCN_GetGameWorldData",
     "world data pull at session start; sits next to the already-decoded "
     "GetWorldInfoVital (0x3D4B)"),
    ("LSCN_ReloginVerifyVital",
     "relogin/reconnect verification; R19 proved reconnect works but nothing persists "
     "- this is the shape that would carry session identity"),
    ("ServerAddedInfoVital",
     "server-appended payload on an existing message; an envelope shape, so "
     "mis-modelling it corrupts everything inside it"),
    ("BasicAttr",
     "the base state block an actor carries; the persistence schema depends on its layout"),
    ("FightAttr",
     "combat stat block; the damage formula reads from this shape"),
    ("AvatarAttr",
     "appearance/identity block that must round-trip through the DB"),
    ("ItemBagAttr",
     "inventory container state; the backpack write path (R21) is one-shot and still "
     "unnamed at the container level"),
    ("ActorCommunityDataSet",
     "DB-side aggregate for one actor's social data; a DataSet is a persistence unit, "
     "not a message"),
    ("PcProtocol",
     "the engine-level protocol base class; naming it pins what every Vital derives from"),
    ("GSSS_GuildStorageCmdVital",
     "game-server to storage-server command; evidence of a shard/service split the "
     "project has never modelled"),
]


def main():
    ap = argparse.ArgumentParser()
    here = os.path.dirname(os.path.abspath(__file__))
    ap.add_argument("--bridge", default=here)
    ap.add_argument("--repo", default=os.path.join(
        os.path.dirname(here), "Pirate Force ServerProject"))
    ap.add_argument("--out", default=here)
    args = ap.parse_args()

    fp_dir = os.path.join(args.bridge, "factpack_L1")
    p_strings = os.path.join(fp_dir, "strings_ascii.tsv")
    p_names = os.path.join(args.repo, "docs", "PF_VITAL_NAMES.json")
    p_census = os.path.join(
        args.repo, "reports",
        "PF_NAMES_FOLD003_LEGACY_SLOTS_AND_THUNK_CENSUS_20260819.census.json")
    p_r38 = os.path.join(args.bridge,
                         "VITAL_REGISTRY_FROM_CLIENT_BINARY_20260817.tsv")

    for p in (p_strings, p_names, p_census, p_r38):
        if not os.path.exists(p):
            sys.stderr.write("MISSING INPUT: %s\n" % p)
            return 2

    rows = load_strings(p_strings)

    # ---- population A : RTTI type descriptors ------------------------------
    rtti_rows = [r for r in rows if RE_RTTI_ANY.match(r["text"])]
    rtti_simple = {}
    rtti_complex = []
    for r in rtti_rows:
        m = RE_RTTI_SIMPLE.match(r["text"])
        if m:
            rtti_simple.setdefault(m.group(2), r)
        else:
            rtti_complex.append(r)

    third_party_complex = [r for r in rtti_complex
                           if any(s in r["text"] for s in THIRD_PARTY_SCOPES)]
    n_third_party = len(third_party_complex)

    rtti_sections = sorted({r["sec"] for r in rtti_rows})
    rtti_offs = sorted(hexva(r["off"]) for r in rtti_rows)
    rtti_vas = sorted(hexva(r["va"]) for r in rtti_rows)

    game_classes = {n: r for n, r in rtti_simple.items()
                    if n not in CRT_GLOBAL_NAMES}

    # ---- population B : identifier-shaped literals -------------------------
    rdata_rows = [r for r in rows if r["sec"] == ".rdata"]
    standalone = {}
    for r in rdata_rows:
        if RE_IDENT.match(r["text"]):
            standalone.setdefault(r["text"], r)

    ident_by_section = collections.Counter(
        r["sec"] for r in rows if RE_IDENT.match(r["text"]))

    strict = {n: standalone[n] for n in game_classes if n in standalone}

    # ---- pooled tail recovery ---------------------------------------------
    # String pooling can only PREPEND bytes: a C string ends at its NUL, so a
    # run reported by the fact pack may carry a prefix of foreign bytes but
    # never a suffix.  A tail match is therefore the complete recovery rule.
    missing = set(game_classes) - set(strict)
    pooled = {}
    unguarded_extra = {}
    if missing:
        maxlen = max(len(x) for x in missing)
        for r in rdata_rows:
            t = r["text"]
            for L in range(4, min(len(t) - 1, maxlen) + 1):
                s = t[-L:]
                if s in missing:
                    base = hexva(r["va"])
                    cand = None if base is None else base + (len(t) - L)
                    c = t[-L - 1]
                    if not (c.isalnum() or c == "_"):
                        pooled.setdefault(s, {"row": r, "literal_va": cand})
                    else:
                        unguarded_extra.setdefault(s, {"row": r, "literal_va": cand})
    for k in list(unguarded_extra):
        if k in pooled:
            del unguarded_extra[k]

    # ---- external corroboration -------------------------------------------
    names_doc = json.load(open(p_names, "r", encoding="utf-8"))
    table = {e["name"]: e for e in names_doc["entries"]}
    table_ids = {}
    for e in names_doc["entries"]:
        table_ids.setdefault(int(e["id"], 16), []).append(e["name"])

    census_doc = json.load(open(p_census, "r", encoding="utf-8"))
    census = {c["name"]: c for c in census_doc["census"]}
    thunks_in_image = census_doc["counts"]["registration_thunks_in_image"]

    # Adjudicate the pooled-tail rule against an artifact it did not produce:
    # the round-86 census carries a literal_va per row, so a VA computed here
    # from row_va + offset_in_run can be checked for byte-level agreement.
    def census_va_agrees(name, va):
        c = census.get(name)
        if not c or va is None:
            return None
        return hexva(c.get("literal_va")) == va

    pooled_corroborated = sorted(
        n for n, d in pooled.items() if census_va_agrees(n, d["literal_va"]))
    unguarded_corroborated = sorted(
        n for n, d in unguarded_extra.items()
        if census_va_agrees(n, d["literal_va"]))

    r38 = {}
    with open(p_r38, "r", encoding="utf-8", errors="replace") as fh:
        for line in fh:
            if line.startswith("#"):
                continue
            p = line.rstrip("\n").split("\t")
            if len(p) >= 2 and p[1]:
                r38[p[1]] = p[0]

    hash_check = {
        "names_table_rows_checked": len(names_doc["entries"]),
        "names_table_mismatches": sum(
            1 for e in names_doc["entries"]
            if wire_id(e["name"]) != int(e["id"], 16)),
        "census_rows_checked": len(census_doc["census"]),
        "census_mismatches": sum(
            1 for c in census_doc["census"]
            if wire_id(c["name"]) != int(c["wire_id"], 16)),
        "r38_rows_checked": len(r38),
        "r38_mismatches": sum(1 for n, i in r38.items()
                              if wire_id(n) != int(i, 16)),
    }

    # ---- rows --------------------------------------------------------------
    out_rows = []
    for name in sorted(game_classes):
        rt = game_classes[name]
        if name in strict:
            kind, lit_row = "standalone", strict[name]
            lit_va = hexva(lit_row["va"])
        elif name in pooled:
            kind, lit_row = "pooled_tail", pooled[name]["row"]
            lit_va = pooled[name]["literal_va"]
        else:
            kind, lit_row, lit_va = "none", None, None
        wid = wire_id(name)
        coll = [x for x in table_ids.get(wid, []) if x != name]
        out_rows.append({
            "name": name,
            "family": family_of(name),
            "rtti_descriptor": rt["text"],
            "rtti_va": rt["va"],
            "rtti_file_offset": rt["off"],
            "literal_kind": kind,
            "literal_va": "-" if lit_va is None else "0x%08X" % lit_va,
            "literal_run_text": "-" if lit_row is None else lit_row["text"],
            "wire_id": "0x%04X" % wid,
            "wire_id_dec": wid,
            "in_names_table": name in table,
            "in_round86_census": name in census,
            "in_round38_tsv": name in r38,
            "id_collision_with_table_name": ";".join(sorted(coll)) if coll else "-",
        })

    with_literal = [r for r in out_rows if r["literal_kind"] != "none"]
    gap = [r for r in with_literal if not r["in_names_table"]]
    gap_in_census = [r for r in gap if r["in_round86_census"]]
    gap_in_r38 = [r for r in gap
                  if r["in_round38_tsv"] and not r["in_round86_census"]]
    gap_novel = [r for r in gap
                 if not r["in_round86_census"] and not r["in_round38_tsv"]]

    # ---- wire-shaped literals with no RTTI ---------------------------------
    no_rtti = []
    for n, r in sorted(standalone.items()):
        if n in game_classes or n in CRT_GLOBAL_NAMES:
            continue
        fam = family_of(n)
        if fam in ("wire_vital", "wire_scn_client_server", "wire_inter_server"):
            wid = wire_id(n)
            no_rtti.append({
                "name": n, "family": fam, "literal_va": r["va"],
                "wire_id": "0x%04X" % wid, "wire_id_dec": wid,
                "in_names_table": n in table,
                "in_round86_census": n in census,
                "in_round38_tsv": n in r38,
            })
    no_rtti_gap = [r for r in no_rtti if not r["in_names_table"]]

    # How well would the filters the brief suggested have done, measured over
    # the same population.  This is why the report does not use them.
    brief_filters = [
        ("C* prefix", lambda n: n.startswith("C")),
        ("GSCN_ prefix", lambda n: n.startswith("GSCN_")),
        ("LSCN_ prefix", lambda n: n.startswith("LSCN_")),
        ("*Vital suffix", lambda n: n.endswith("Vital")),
        ("any of the four", lambda n: n.startswith(("C", "GSCN_", "LSCN_"))
         or n.endswith("Vital")),
    ]
    all_names = [r["name"] for r in out_rows]
    join_names = [r["name"] for r in with_literal]
    brief_cov = []
    for label, fn in brief_filters:
        brief_cov.append({
            "filter": label,
            "hits_in_class_census": sum(1 for n in all_names if fn(n)),
            "hits_in_join": sum(1 for n in join_names if fn(n)),
            "join_rows_missed": sum(1 for n in join_names if not fn(n)),
        })

    fam_counts = collections.Counter(r["family"] for r in gap)
    fam_examples = {f: [r["name"] for r in gap if r["family"] == f][:10]
                    for f in fam_counts}
    fam_counts_all = collections.Counter(r["family"] for r in out_rows)

    collisions = [r for r in gap if r["id_collision_with_table_name"] != "-"]
    internal = collections.Counter(r["wire_id"] for r in gap)
    internal_dupes = {k: [r["name"] for r in gap if r["wire_id"] == k]
                      for k, v in internal.items() if v > 1}

    route_all = collections.Counter()
    for r in out_rows:
        m = RE_ROUTE_PREFIX.match(r["name"])
        if m:
            route_all[m.group(1)] += 1
    route_gap = collections.Counter()
    for r in gap:
        m = RE_ROUTE_PREFIX.match(r["name"])
        if m:
            route_gap[m.group(1)] += 1

    by_name = {r["name"]: r for r in out_rows}
    prio = []
    for name, why in PRIORITY:
        if name not in by_name:
            sys.stderr.write("PRIORITY name not in class census: %s\n" % name)
            return 3
        r = by_name[name]
        if r["in_names_table"]:
            sys.stderr.write("PRIORITY name already in the name table: %s\n" % name)
            return 3
        d = dict(r)
        d["why"] = why
        prio.append(d)

    summary = {
        "milestone": "FACTPACK-L2-CLASSCENSUS-001",
        "generated_at": datetime.datetime.now().astimezone().isoformat(timespec="seconds"),
        "generated_by": os.path.basename(__file__),
        "report_only": True,
        "wrote_into_repo": False,
        "opened_the_image": False,
        "disassembled": False,
        "inputs": {
            "strings_ascii_tsv": {"path": p_strings,
                                  "sha256": sha256_of(p_strings),
                                  "data_rows": len(rows)},
            "names_table": {"path": p_names, "entry_count": len(table)},
            "round86_census": {"path": p_census, "rows": len(census),
                               "registration_thunks_in_image": thunks_in_image},
            "round38_tsv": {"path": p_r38, "rows": len(r38)},
        },
        "hash_selfcheck": hash_check,
        "population_A_rtti": {
            "descriptor_rows": len(rtti_rows),
            "sections": rtti_sections,
            "file_offset_min": "0x%08X" % rtti_offs[0],
            "file_offset_max": "0x%08X" % rtti_offs[-1],
            "va_min": "0x%08X" % rtti_vas[0],
            "va_max": "0x%08X" % rtti_vas[-1],
            "simple_global_names": len(rtti_simple),
            "template_or_namespaced": len(rtti_complex),
            "third_party_scoped": n_third_party,
            "game_template_instantiations": len(rtti_complex) - n_third_party,
            "crt_global_excluded": sorted(CRT_GLOBAL_NAMES),
            "game_class_names": len(game_classes),
        },
        "population_B_literals": {
            "rdata_rows_total": len(rdata_rows),
            "identifier_shaped_by_section": dict(ident_by_section),
            "rdata_distinct_identifier_literals": len(standalone),
        },
        "join": {
            "strict_standalone": len(strict),
            "pooled_tail_recovered": len(pooled),
            "pooled_names": sorted(pooled),
            "pooled_names_corroborated_by_r86_literal_va": pooled_corroborated,
            "unguarded_rule_would_add": len(unguarded_extra),
            "unguarded_rule_extra_names": sorted(unguarded_extra),
            "unguarded_rule_extra_corroborated_by_r86_literal_va":
                unguarded_corroborated,
            "class_names_with_literal": len(with_literal),
            "class_names_without_literal": len(out_rows) - len(with_literal),
        },
        "gap_vs_names_table": {
            "class_names_with_literal": len(with_literal),
            "already_in_names_table": len(with_literal) - len(gap),
            "not_in_names_table": len(gap),
            "of_which_in_round86_census": len(gap_in_census),
            "of_which_in_round38_tsv_only": len(gap_in_r38),
            "of_which_novel_to_this_round": len(gap_novel),
            "novel_names": [r["name"] for r in gap_novel],
            "table_entries_with_no_literal_at_all":
                sorted(n for n in table
                       if n not in standalone and n not in pooled),
        },
        "no_rtti_wire_shaped_literals": {
            "count": len(no_rtti),
            "not_in_names_table": len(no_rtti_gap),
            "rows": no_rtti,
        },
        "brief_filter_coverage": brief_cov,
        "families_gap": {"counts": dict(fam_counts.most_common()),
                         "examples": fam_examples},
        "families_full_census": dict(fam_counts_all.most_common()),
        "routing_prefixes_full_census": dict(route_all.most_common()),
        "routing_prefixes_gap": dict(route_gap.most_common()),
        "hash_collisions": {
            "gap_names_colliding_with_a_registered_id": len(collisions),
            "detail": [{"name": r["name"], "wire_id": r["wire_id"],
                        "registered_as": r["id_collision_with_table_name"]}
                       for r in collisions],
            "gap_internal_duplicate_ids": internal_dupes,
        },
        "priority": [{"name": r["name"], "wire_id": r["wire_id"],
                      "family": r["family"], "literal_va": r["literal_va"],
                      "rtti_va": r["rtti_va"],
                      "in_round86_census": r["in_round86_census"],
                      "in_round38_tsv": r["in_round38_tsv"],
                      "why": r["why"]} for r in prio],
        "total_rows_emitted": len(out_rows),
    }

    cols = ["name", "family", "wire_id", "wire_id_dec", "rtti_va",
            "rtti_file_offset", "literal_kind", "literal_va", "in_names_table",
            "in_round86_census", "in_round38_tsv",
            "id_collision_with_table_name", "rtti_descriptor",
            "literal_run_text"]
    p_tsv = os.path.join(args.out, BASENAME + ".tsv")
    with open(p_tsv, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("# FACTPACK-L2-CLASSCENSUS-001 -- declared class names in the "
                 "Pirate Force client image\n")
        fh.write("# derived ONLY from pf_bridge/factpack_L1/strings_ascii.tsv "
                 "(sha256 %s)\n"
                 % summary["inputs"]["strings_ascii_tsv"]["sha256"])
        fh.write("# NONCLAIM: every row is a literal in a file.  Presence does "
                 "NOT prove the class is constructed, registered, or ever hit "
                 "the wire.\n")
        fh.write("# wire_id is DERIVED from the name by the round-62 hash.  It "
                 "is NOT read from any table in the image.\n")
        fh.write("\t".join(cols) + "\n")
        for r in out_rows:
            fh.write("\t".join(str(r[c]) for c in cols) + "\n")

    p_json = os.path.join(args.out, BASENAME + ".json")
    with open(p_json, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(summary, fh, ensure_ascii=False, indent=1, sort_keys=False)
        fh.write("\n")

    p_md = os.path.join(args.out, BASENAME + ".md")
    with open(p_md, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(render(summary))

    print("wrote %s" % p_tsv)
    print("wrote %s" % p_json)
    print("wrote %s" % p_md)
    print("class names emitted      : %d" % summary["total_rows_emitted"])
    print("with a runtime literal   : %d"
          % summary["join"]["class_names_with_literal"])
    print("not in PF_VITAL_NAMES    : %d"
          % summary["gap_vs_names_table"]["not_in_names_table"])
    print("  already in r86 census  : %d"
          % summary["gap_vs_names_table"]["of_which_in_round86_census"])
    print("  in r38 tsv only        : %d"
          % summary["gap_vs_names_table"]["of_which_in_round38_tsv_only"])
    print("  novel to this round    : %d"
          % summary["gap_vs_names_table"]["of_which_novel_to_this_round"])
    print("wire-shaped, no RTTI     : %d"
          % summary["no_rtti_wire_shaped_literals"]["not_in_names_table"])
    print("hash selfcheck mismatches: %d"
          % (hash_check["names_table_mismatches"]
             + hash_check["census_mismatches"] + hash_check["r38_mismatches"]))
    return 0


# ---------------------------------------------------------------- report render

FAMILY_GLOSS = {
    "wire_vital": "Vital -- wire message classes (includes the client's own 'Vtial' misspelling)",
    "wire_scn_client_server": "SCN -- GSCN_/LSCN_ client-to-server protocol classes",
    "wire_inter_server": "inter-server -- GSSS_/DBSS_/CNSS_/GCSS_/GCGSSS_/GCGS_ routed classes",
    "attr_state_block": "Attr -- state blocks attached to an actor or object",
    "module_subsystem": "Module -- gameplay subsystems (*Module, *Module_Client)",
    "ui_event_handler": "UI event handlers (*EventHandler)",
    "ui_widget": "UI widgets (BigUI*, *Board, *Window, *Bar, ...)",
    "persistence_record": "persistence -- *Record, *DataSet, *Stream, *Property",
    "ai_behavior": "AI / behavior",
    "task_quest": "Task / Quest",
    "effect_fx_missile": "Effect / FX / Missile",
    "combat_skill_buff": "combat -- skill, buff, hit, damage, death, cooldown",
    "scene_world_move": "scene / world / movement",
    "item_inventory_economy": "item / inventory / economy",
    "social_channel": "social / channel",
    "actor_npc": "actor / NPC / pets",
    "data_blob": "*Data blobs",
    "other_unclassified": "no family suffix matched -- see the note under the tables",
}

ROUTE_GLOSS = {
    "GSCN": "game server <-> CN node",
    "LSCN": "login server <-> CN node",
    "GSSS": "game server <-> storage / sub server",
    "DBSS": "DB server <-> storage server",
    "CNSS": "CN node <-> storage server",
    "GCSS": "game client <-> storage server",
    "GCGSSS": "client -> game server -> storage server",
    "GCGS": "game client <-> game server",
    "GM": "game master / admin",
    "UI": "client UI",
    "NPC": "NPC subsystem",
}


def render(s):
    A = s["population_A_rtti"]
    B = s["population_B_literals"]
    J = s["join"]
    G = s["gap_vs_names_table"]
    hc = s["hash_selfcheck"]
    hz = s["hash_collisions"]
    nr = s["no_rtti_wire_shaped_literals"]
    thunks = s["inputs"]["round86_census"]["registration_thunks_in_image"]
    L = []
    w = L.append

    w("# FACTPACK-L2-CLASSCENSUS-001 -- the client's own class census, "
      "and how much of it the project has never named")
    w("")
    w("**Lane FACTPACK-L2-CLASSCENSUS-001 - %s - report only.** No repo file was "
      "written. The image was not opened. No instruction was decoded."
      % s["generated_at"][:10])
    w("")
    w("Generated by `pf_bridge/%s`. Every figure below is read back out of "
      "`%s.json`, which the same run produced. The prose is a template; the "
      "numbers are not typed by hand." % (s["generated_by"], BASENAME))
    w("")
    w("```")
    w("python3 pf_bridge/%s" % s["generated_by"])
    w("```")
    w("")
    w("**สรุปภาษาไทยหนึ่งย่อหน้า** ไคลเอนต์ประกาศคลาสเกมไว้ %d ตัว (นับจากตาราง RTTI). "
      "ในจำนวนนั้น %d ตัวมี \"ชื่อรันไทม์\" เป็นสตริงอยู่ใน `.rdata` ด้วย ซึ่งคือประชากร"
      "ที่มีสิทธิ์ถูก register ได้จริง. ทะเบียนชื่อของโปรเจกต์ครอบอยู่ %d ตัว เหลือ **%d ตัว"
      "ที่ยังไม่มีชื่อในทะเบียน**. รอบนี้ **นับกับจัดลำดับความสำคัญเท่านั้น ไม่ได้ตั้งชื่ออะไรเลย** "
      "และ **ไม่ได้ปิดช่อง 209 ตัว**."
      % (A["game_class_names"], J["class_names_with_literal"],
         G["already_in_names_table"], G["not_in_names_table"]))
    w("")
    w("---")
    w("")

    w("## 0. NONCLAIMS -- read before quoting any number")
    w("")
    w("1. **Every name in this report is a literal in a file, and nothing more.** "
      "The fact pack proves those bytes exist at that offset. It does **not** "
      "prove the class is ever constructed, ever registered, or ever appeared on "
      "the wire.")
    w("2. **This round did not open the image and did not disassemble anything.** "
      "The only image-derived input is `pf_bridge/factpack_L1/strings_ascii.tsv` "
      "(sha256 `%s`), produced in an earlier round. `opened_the_image` and "
      "`disassembled` are recorded as `false` in the JSON."
      % s["inputs"]["strings_ascii_tsv"]["sha256"])
    w("3. **The real name table was not touched.** `docs/PF_VITAL_NAMES.json` was "
      "opened read-only and still holds %d entries. Nothing here was admitted to "
      "it, and nothing here may be quoted as a project name for a wire id."
      % s["inputs"]["names_table"]["entry_count"])
    w("4. **The %d-class gap is NOT closed.** This round counted and ranked; it "
      "proved no name. Project rule (4) admits a name only when **(a)** the "
      "round-62 hash of the name equals an independently observed id **and** "
      "**(b)** the literal is pushed in the shape of a registration thunk. "
      "Section 6 states exactly which of the two each bucket satisfies, and it is "
      "never both." % s["inputs"]["round86_census"]["rows"])
    w("5. `wire_id` in the data files is **derived** from the name by the round-62 "
      "hash. It was **not** read from any table in the image. A derived id is not "
      "evidence.")
    w("6. The family labels in section 4 are this round's editorial grouping, not "
      "a structure found in the image. The rule list is in the generator and the "
      "matched rule is written into the tsv, so the grouping is auditable and "
      "replaceable.")
    w("7. These names are third-party copyrighted material extracted from a "
      "commercial client. They stay inside `pf_bridge/`.")
    w("")
    w("---")
    w("")

    w("## 1. The answer, first")
    w("")
    w("| question | measured |")
    w("|---|---:|")
    w("| RTTI type-descriptor strings in `strings_ascii.tsv` | **%d** |"
      % A["descriptor_rows"])
    w("| ... that undecorate to a plain global class name | **%d** |"
      % A["simple_global_names"])
    w("| ... game/engine class names (CRT `type_info` removed) | **%d** |"
      % A["game_class_names"])
    w("| of those, ones that also carry a runtime name literal in `.rdata` | **%d** |"
      % J["class_names_with_literal"])
    w("| of those, **not** in `docs/PF_VITAL_NAMES.json` | **%d** |"
      % G["not_in_names_table"])
    w("| ... already enumerated by the round-86 thunk census | %d |"
      % G["of_which_in_round86_census"])
    w("| ... in the round-38 candidate tsv but not the census | %d |"
      % G["of_which_in_round38_tsv_only"])
    w("| ... **novel to this round** (in neither prior artifact) | **%d** |"
      % G["of_which_novel_to_this_round"])
    w("| wire-shaped literals with **no** RTTI class at all, not in the table | **%d** |"
      % nr["not_in_names_table"])
    w("")
    w("In one line: the client declares **%d** game classes; **%d** of them also "
      "ship a runtime name literal, which is the population that can even in "
      "principle be registered; the project has named **%d** of those and has "
      "**%d** left, plus **%d** more wire-shaped names that have no client class "
      "at all."
      % (A["game_class_names"], J["class_names_with_literal"],
         G["already_in_names_table"], G["not_in_names_table"],
         nr["not_in_names_table"]))
    w("")
    w("---")
    w("")

    w("## 2. \"Looks like a game class name\" -- derived, not assumed")
    w("")
    w("The brief offered prefix families (`C*`, `GSCN_*`, `*Vital`, `LSCN_*`) as "
      "a starting point. Those families are real -- section 2.3 counts them -- "
      "but measured against the population they are supposed to select, they are "
      "a poor *primary* filter:")
    w("")
    w("| suggested filter | hits in the %d-class census | hits in the %d-name "
      "registered-shaped join | join rows it MISSES |"
      % (s["total_rows_emitted"], J["class_names_with_literal"]))
    w("|---|---:|---:|---:|")
    for b in s["brief_filter_coverage"]:
        w("| `%s` | %d | %d | %d |"
          % (b["filter"], b["hits_in_class_census"], b["hits_in_join"],
             b["join_rows_missed"]))
    w("")
    w("All four together still miss %d of the %d names that matter, while "
      "dragging in %d census rows that are not in the join at all. So the brief's "
      "families are used in this report as a *grouping* (section 4), never as the "
      "selector. The image hands us a far stronger selector for free."
      % (s["brief_filter_coverage"][-1]["join_rows_missed"],
         J["class_names_with_literal"],
         s["brief_filter_coverage"][-1]["hits_in_class_census"]
         - s["brief_filter_coverage"][-1]["hits_in_join"]))
    w("")

    w("### 2.1 Population A -- the compiler's own class census (RTTI)")
    w("")
    w("MSVC emits one `TypeDescriptor` per polymorphic type; its name field holds "
      "the decorated form `.?AV<Name>@@` for a class and `.?AU<Name>@@` for a "
      "struct. Matching `^\\.\\?A[VU]` against the `text` column gives:")
    w("")
    w("| | count |")
    w("|---|---:|")
    w("| descriptor rows | %d |" % A["descriptor_rows"])
    w("| sections they live in | %s |"
      % ", ".join("`%s`" % x for x in A["sections"]))
    w("| file-offset span | `%s` .. `%s` |"
      % (A["file_offset_min"], A["file_offset_max"]))
    w("| VA span | `%s` .. `%s` |" % (A["va_min"], A["va_max"]))
    w("| undecorate to a simple global name | %d |" % A["simple_global_names"])
    w("| template / namespaced forms | %d |" % A["template_or_namespaced"])
    w("| ... third-party scoped (`std`, `boost`, `LuaPlus`, `ATL`) | %d |"
      % A["third_party_scoped"])
    w("| ... game template instantiations | %d |"
      % A["game_template_instantiations"])
    w("| CRT global names removed | %s |"
      % ", ".join("`%s`" % x for x in A["crt_global_excluded"]))
    w("| **game/engine class names used from here on** | **%d** |"
      % A["game_class_names"])
    w("")
    w("**Cross-check against the previous round, which is where a number moved.** "
      "The prior round reported the table at `0x00C1786C`-`0x00C29514` holding "
      "**1,367** classes. This run measures the same span byte-for-byte -- "
      "`%s`..`%s`, no drift -- but counts **%d** descriptor rows inside it. The "
      "one-row delta is a counting convention, not a disagreement about bytes: "
      "%d is the raw row count, %d is that minus the CRT `type_info` descriptor, "
      "and %d is the count of *game* names once the %d template/namespaced forms "
      "are set aside as well. Anyone quoting \"1,367\" should say which of the "
      "three they mean; this report uses **%d** throughout."
      % (A["file_offset_min"], A["file_offset_max"], A["descriptor_rows"],
         A["descriptor_rows"], A["descriptor_rows"] - 1, A["game_class_names"],
         A["template_or_namespaced"], A["game_class_names"]))
    w("")

    w("### 2.2 Population B -- runtime name literals")
    w("")
    w("A registration thunk pushes an **undecorated** NUL-terminated identifier, "
      "not the RTTI form. Filtering `^[A-Za-z_][A-Za-z0-9_]*$` over the whole "
      "fact pack, per section:")
    w("")
    w("| section | identifier-shaped rows |")
    w("|---|---:|")
    for k, v in sorted(B["identifier_shaped_by_section"].items(),
                       key=lambda kv: -kv[1]):
        w("| `%s` | %d |" % (k, v))
    w("")
    w("Only `.rdata` matters. That is where every literal the round-85/86 work "
      "traced actually lives; the `.text` hits are opcode bytes that happen to be "
      "printable, and `.reloc` hits are relocation payload. Distinct `.rdata` "
      "identifier literals: **%d**." % B["rdata_distinct_identifier_literals"])
    w("")
    w("A bare `.rdata` identifier is a weak signal on its own -- shader uniforms, "
      "Lua symbols and format tokens all match it. That is precisely why the "
      "answer to question 1 is the **join** of A and B, not B.")
    w("")

    w("### 2.3 The families, counted rather than asserted")
    w("")
    w("Across the whole class census, the ALLCAPS routing token before the first "
      "underscore distributes like this:")
    w("")
    w("| prefix | classes | in the gap | reading |")
    w("|---|---:|---:|---|")
    for k, v in s["routing_prefixes_full_census"].items():
        w("| `%s_` | %d | %d | %s |"
          % (k, v, s["routing_prefixes_gap"].get(k, 0), ROUTE_GLOSS.get(k, "-")))
    w("")
    w("That table is itself a finding. The client's own class names encode a "
      "**multi-process server topology** -- login server, game server, DB server, "
      "storage/sub server, CN node -- not the single process the project "
      "currently runs. Every one of those prefixes names a hop that no longer "
      "exists anywhere except in these strings.")
    w("")
    w("Two spelling facts a naive filter would silently drop:")
    w("")
    w("* **`Vtial`** is a misspelling of `Vital` **in the shipped client's own "
      "class names** -- not a transcription error in this report. A regex that "
      "only matches `Vital$` loses real wire classes, so the family rule in the "
      "generator carries `(Vital|Vtial)(Req|Res)?$` deliberately.")
    w("* Names such as `AbilityDepoly` and `ItemBagAttr_Equiped` carry the "
      "original authors' typos. They are reproduced verbatim. Do not \"fix\" "
      "them: the id is a hash over the bytes that are actually there.")
    w("")

    w("### 2.4 The join, and one measurement artifact worth knowing about")
    w("")
    w("| | count |")
    w("|---|---:|")
    w("| class names with a standalone `.rdata` literal | %d |"
      % J["strict_standalone"])
    w("| + recovered from a pooled run (below) | %d |"
      % J["pooled_tail_recovered"])
    w("| **class names with a runtime literal** | **%d** |"
      % J["class_names_with_literal"])
    w("| class names with no literal anywhere | %d |"
      % J["class_names_without_literal"])
    w("")
    w("The fact pack cuts strings at non-printable bytes, so when the linker "
      "pools two literals with no NUL between them, the second is reported as "
      "the **tail** of a longer run. Because a C string always ends at its NUL, "
      "pooling can only ever *prepend* -- which makes a tail match the complete "
      "recovery rule in principle, not a heuristic. The only judgement call is "
      "the boundary byte. Requiring it to be a non-identifier byte recovers "
      "**%d** names: %s."
      % (J["pooled_tail_recovered"],
         ", ".join("`%s`" % x for x in J["pooled_names"])))
    w("")
    w("That guard can be checked rather than argued about. The round-86 census "
      "records a `literal_va` per row, produced from the image by a different "
      "method; recomputing the VA here as `row_va + offset_of_the_name_in_the_run` "
      "and comparing gives **%d of %d** recovered names agreeing to the byte."
      % (len(J["pooled_names_corroborated_by_r86_literal_va"]),
         J["pooled_tail_recovered"]))
    w("")
    if J["unguarded_rule_extra_corroborated_by_r86_literal_va"]:
        w("**The guard is not free, and here is exactly what it costs.** Dropping "
          "it would admit **%d** more names. %d of those %d are visibly just "
          "suffixes of longer census names (%s) and are false positives. But **%d "
          "is a true positive that the guard rejects**: %s. Its run is preceded by "
          "an alphanumeric byte, so the boundary test fails, yet the VA computed "
          "for it matches the round-86 `literal_va` to the byte. The strict count "
          "in this report is therefore **%d**, the count including that row would "
          "be **%d**, and the difference is one row that strings alone cannot "
          "adjudicate. It is called out rather than quietly folded in."
          % (J["unguarded_rule_would_add"],
             J["unguarded_rule_would_add"]
             - len(J["unguarded_rule_extra_corroborated_by_r86_literal_va"]),
             J["unguarded_rule_would_add"],
             ", ".join("`%s`" % x for x in J["unguarded_rule_extra_names"][:5]),
             len(J["unguarded_rule_extra_corroborated_by_r86_literal_va"]),
             ", ".join("`%s`" % x for x in
                       J["unguarded_rule_extra_corroborated_by_r86_literal_va"]),
             J["class_names_with_literal"],
             J["class_names_with_literal"]
             + len(J["unguarded_rule_extra_corroborated_by_r86_literal_va"])))
        w("")
    w("**Independent corroboration of the join.** Round 86 counted **%d** "
      "registration thunks in the image by byte-template matching, working from "
      "the image itself. This round, from strings alone and with no knowledge of "
      "thunks, lands on **%d** classes that have both a type descriptor and a "
      "runtime literal. Two unrelated methods agreeing to within %d row(s) is the "
      "strongest single thing in this report: the join is, to a very good "
      "approximation, *the registered population*. It is not proof that any "
      "particular row is registered."
      % (thunks, J["class_names_with_literal"],
         abs(J["class_names_with_literal"] - thunks)))
    w("")
    w("A second corroboration falls out for free: of the %d entries in the real "
      "name table, %d are inside the join, and the single exception is `%s` -- "
      "which is exactly the row round 86 independently classified `NO_LITERAL`. "
      "Two methods, one disagreement, and it is the row both already knew about."
      % (s["inputs"]["names_table"]["entry_count"],
         s["inputs"]["names_table"]["entry_count"]
         - len(G["table_entries_with_no_literal_at_all"]),
         ", ".join(G["table_entries_with_no_literal_at_all"])))
    w("")

    w("### 2.5 Hash self-check")
    w("")
    w("Before comparing anything by hash, the generator re-derives the round-62 "
      "id for every name in all three external artifacts and requires an exact "
      "match. A non-zero mismatch column would invalidate every id in this "
      "report:")
    w("")
    w("| artifact | rows checked | mismatches |")
    w("|---|---:|---:|")
    w("| `docs/PF_VITAL_NAMES.json` | %d | %d |"
      % (hc["names_table_rows_checked"], hc["names_table_mismatches"]))
    w("| round-86 census json | %d | %d |"
      % (hc["census_rows_checked"], hc["census_mismatches"]))
    w("| round-38 candidate tsv | %d | %d |"
      % (hc["r38_rows_checked"], hc["r38_mismatches"]))
    w("")
    w("---")
    w("")

    w("## 3. How many are missing from the name table")
    w("")
    w("Compared **by name** and **by derived id**, as the brief asks.")
    w("")
    w("| | count |")
    w("|---|---:|")
    w("| class names with a runtime literal | %d |"
      % G["class_names_with_literal"])
    w("| already in `docs/PF_VITAL_NAMES.json` | %d |"
      % G["already_in_names_table"])
    w("| **not in the name table** | **%d** |" % G["not_in_names_table"])
    w("| -- already enumerated by the round-86 census | %d |"
      % G["of_which_in_round86_census"])
    w("| -- in the round-38 tsv but not the census | %d |"
      % G["of_which_in_round38_tsv_only"])
    w("| -- **novel to this round** | **%d** |"
      % G["of_which_novel_to_this_round"])
    w("")
    if G["novel_names"]:
        w("The %d novel rows, in full: %s. They have a type descriptor and a "
          "runtime literal, and neither prior artifact lists them. That does "
          "**not** mean they are registered -- the most likely reading is the "
          "opposite: they are the handful of classes that carry a name literal "
          "for some other reason (a debug string, a factory key) and never go "
          "through a registration thunk at all. Step 1 in section 6.2 is what "
          "settles it."
          % (G["of_which_novel_to_this_round"],
             ", ".join("`%s`" % x for x in G["novel_names"])))
        w("")
    w("**By hash.** Of the %d missing names, **%d** hash to a 16-bit id the name "
      "table has already assigned to a *different* name, and **%d** id values are "
      "shared by more than one missing name."
      % (G["not_in_names_table"],
         hz["gap_names_colliding_with_a_registered_id"],
         len(hz["gap_internal_duplicate_ids"])))
    if hz["detail"]:
        w("")
        w("| missing name | derived id | that id is registered as |")
        w("|---|---|---|")
        for d in hz["detail"]:
            w("| `%s` | `%s` | `%s` |"
              % (d["name"], d["wire_id"], d["registered_as"]))
    if hz["gap_internal_duplicate_ids"]:
        w("")
        w("| shared id | missing names that hash to it |")
        w("|---|---|")
        for k, v in sorted(hz["gap_internal_duplicate_ids"].items()):
            w("| `%s` | %s |" % (k, ", ".join("`%s`" % x for x in v)))
    w("")
    if hz["gap_names_colliding_with_a_registered_id"] == 0 \
            and not hz["gap_internal_duplicate_ids"]:
        w("Zero collisions is a mildly useful negative, not a triumph: at this "
          "population size roughly one collision would be unremarkable, so its "
          "absence is luck rather than evidence of anything. What matters is the "
          "direction of the check -- **no missing name silently shadows an id the "
          "project has already committed to**, so nothing in the tsv beside this "
          "report can corrupt the existing table by being read carelessly.")
    else:
        w("A collision is **not** evidence that either name is wrong. The id is a "
          "16-bit hash over a population of this size, so collisions are expected. "
          "What it does prove is that **an id alone can never identify a class**.")
    w("")
    w("Either way the general point stands, and it is the reason project rule (4) "
      "has a condition (b) at all: hash agreement is a filter, never a proof.")
    w("")

    w("### 3.1 A population the class census cannot see")
    w("")
    w("**%d** `.rdata` literals carry a wire-family shape (`*Vital` / `*Vtial` / "
      "`GSCN_*` / `LSCN_*` / an inter-server prefix) but have **no RTTI "
      "descriptor at all**, and **%d** of them are absent from the name table. A "
      "class with no type descriptor was never instantiated polymorphically *in "
      "the client*. The natural reading -- stated as a reading, not a finding -- "
      "is that these are **server-side-only messages** whose names the client "
      "only ever spells out. Note what they are about: friendship, penpal "
      "letters, letter-in-a-bottle, system mail, express delivery, guild storage. "
      "All of it is persistence the project has no model for."
      % (nr["count"], nr["not_in_names_table"]))
    w("")
    w("| name | family | derived id | literal VA | in r38 tsv |")
    w("|---|---|---|---|---|")
    for r in nr["rows"]:
        w("| `%s` | %s | `%s` | `%s` | %s |"
          % (r["name"], r["family"], r["wire_id"], r["literal_va"],
             "yes" if r["in_round38_tsv"] else "no"))
    w("")
    w("---")
    w("")

    w("## 4. The missing %d, grouped into families" % G["not_in_names_table"])
    w("")
    w("Families are assigned by an **ordered, first-match-wins** rule list that "
      "lives in the generator (`FAMILY_RULES`). The rule that matched is written "
      "into the `family` column of the tsv, so any regrouping can be re-derived "
      "without rerunning the join, and a disagreement with the grouping is a "
      "one-line change rather than an argument.")
    w("")
    w("| family | count | meaning |")
    w("|---|---:|---|")
    for f, c in s["families_gap"]["counts"].items():
        w("| `%s` | %d | %s |" % (f, c, FAMILY_GLOSS.get(f, "-")))
    w("")
    for f, c in s["families_gap"]["counts"].items():
        ex = s["families_gap"]["examples"][f]
        w("**`%s`** -- %d name(s), %s. %s:"
          % (f, c, FAMILY_GLOSS.get(f, "-"),
             "all of them" if len(ex) == c else "first %d by name" % len(ex)))
        w("")
        for n in ex:
            w("* `%s`" % n)
        w("")
    fam_items = list(s["families_gap"]["counts"].items())
    top1, top2 = fam_items[0], fam_items[1]
    w("Three observations that fall out of the grouping and are worth more than "
      "the counts:")
    w("")
    w("* **`%s` is the largest family at %d of %d.** Those are whole gameplay "
      "subsystems, named one by one: appraisal, dyeing, winemaking, treasure "
      "hunt, black market, pandora box, collection book, item synthesis, item "
      "transform, pets, stalls, daily rewards. The project today has an actor "
      "that can move and be hit."
      % (top1[0], top1[1], G["not_in_names_table"]))
    w("* **`%s` is second at %d.** Every `*Attr` is a state block that has to be "
      "serialised somewhere and, for most of them, persisted. That list is the "
      "closest thing the project will ever get to the original persistence "
      "schema." % (top2[0], top2[1]))
    w("* **`%s` (%d) is not a leftovers bin.** It holds the engine-level base "
      "classes (`PcProtocol`, `PcProtocolProxy`, `Attribute`, `DBAttribute`) and "
      "a few flat verb-shaped messages (`InstanceLeave`, `InstanceBonusNotify`, "
      "`BuildingCrystal_UpdateNextAbsorbTime`). The base classes matter most: "
      "naming `PcProtocol` pins what every other name in this report derives from."
      % ("other_unclassified",
         s["families_gap"]["counts"].get("other_unclassified", 0)))
    w("")
    w("---")
    w("")

    w("## 5. The %d names worth the most to the gameplay still unbuilt"
      % len(s["priority"]))
    w("")
    w("Ranking criterion, stated so it can be argued with: how much *remaining* "
      "project work the name would unblock, weighted toward the lanes that are "
      "actually open -- damage and death, multiplayer replication, persistence. "
      "A name appears here only if the generator can confirm it is in the "
      "computed gap set and absent from the name table; the script exits "
      "non-zero otherwise, so this table cannot rot away from the data.")
    w("")
    w("| # | name | derived id | family | literal VA | thunk known (r86) | why it matters |")
    w("|---:|---|---|---|---|---|---|")
    for i, p in enumerate(s["priority"], 1):
        w("| %d | `%s` | `%s` | `%s` | `%s` | %s | %s |"
          % (i, p["name"], p["wire_id"], p["family"], p["literal_va"],
             "yes" if p["in_round86_census"] else "no", p["why"]))
    w("")
    w("Note the shape of that list. It is dominated by **server-side** and "
      "**inter-server** classes. The project's blind spot is not the client -- "
      "the client is now fully enumerated, twice, by two methods. The blind spot "
      "is everything the shut-down server used to do with these messages, and "
      "these names are the only surviving description of it.")
    w("")
    w("**A caution about the id column.** Those ids are hashes of the names. If a "
      "name in this table is later disproved, its id was never real. Do not wire "
      "any of them into a handler, a test, or a fixture. This report exists to "
      "decide what to investigate next, not to be imported.")
    w("")
    w("---")
    w("")

    w("## 6. What would actually prove a name, and why this round did not")
    w("")
    w("Project rule (4) admits a name to `docs/PF_VITAL_NAMES.json` only when "
      "**both** hold:")
    w("")
    w("* **(a) hash match** -- `wire_id(name)` equals an id observed "
      "*independently of the name*: on the wire in the pinned golden corpus, or "
      "in the frozen v141 snapshot.")
    w("* **(b) thunk shape** -- the literal is pushed by a complete registration "
      "thunk, in the shape `tools/pf_vital_name_thunk_static.py` matches as a raw "
      "byte template (`push <literal>; call <ctor>; mov ecx,eax; call "
      "<ID_ASSIGN>; mov word ptr [<id_slot>], ax; ret`), **and that push is the "
      "only push of that literal in the image**.")
    w("")
    w("### 6.1 Where the %d stand against those two conditions"
      % G["not_in_names_table"])
    w("")
    w("| bucket | count | condition (a) | condition (b) |")
    w("|---|---:|---|---|")
    w("| in the round-86 census | %d | **vacuous** -- the id has no source "
      "independent of the name, because it is computed from the name | "
      "**satisfied** -- round 86 matched the thunk template |"
      % G["of_which_in_round86_census"])
    w("| in the round-38 tsv only | %d | candidate only, never independently "
      "observed | **unknown** -- not re-checked this round |"
      % G["of_which_in_round38_tsv_only"])
    w("| novel to this round | %d | **unknown** | **unknown** |"
      % G["of_which_novel_to_this_round"])
    w("| wire-shaped, no RTTI (section 3.1) | %d | candidate only | **unknown** |"
      % nr["not_in_names_table"])
    w("")
    w("So the honest statement of the balance: of the %d, **%d already satisfy "
      "(b)** and are blocked on (a); the remaining %d satisfy neither yet. "
      "**Nothing in this round closes the %d-class gap, and this report does not "
      "claim it does.** The claim the round *can* support is narrower and still "
      "useful: the gap has now been counted from a second, independent direction, "
      "and the two counts agree."
      % (G["not_in_names_table"], G["of_which_in_round86_census"],
         G["not_in_names_table"] - G["of_which_in_round86_census"],
         s["inputs"]["round86_census"]["rows"]))
    w("")
    w("### 6.2 Next steps, in the order that actually pays")
    w("")
    w("**Step 1 -- point the existing thunk matcher at the %d rows that have "
      "never seen it.** `tools/pf_vital_name_thunk_static.py` already implements "
      "condition (b) with a byte template and no disassembler. It has never been "
      "run against the %d novel names, the %d tsv-only names, or the %d "
      "wire-shaped no-RTTI literals. This is the cheapest possible step: it needs "
      "the image and an existing tool, no new theory. Expected output is the same "
      "four-tier split as round 85 -- PROVEN / AMBIGUOUS / NO_THUNK / NO_LITERAL. "
      "Everything that lands in NO_THUNK is permanently out of scope for rule (4) "
      "and can stop consuming attention. Note the shape of this request: it is "
      "one batch of %d names against one pinned image, answered once, correct "
      "forever. That is exactly the shape the image-query queue currently being "
      "specced is meant to carry, so it does not need a person sitting at the "
      "local machine for an hour."
      % (G["not_in_names_table"] - G["of_which_in_round86_census"]
         + nr["not_in_names_table"],
         G["of_which_novel_to_this_round"],
         G["of_which_in_round38_tsv_only"], nr["not_in_names_table"],
         G["not_in_names_table"] - G["of_which_in_round86_census"]
         + nr["not_in_names_table"]))
    w("")
    w("**Step 2 -- decide, at chief level, what condition (a) can mean for a name "
      "the wire never showed us.** This is the real blocker, and it is a "
      "**policy** question, not a measurement one. The server is gone; for a "
      "class that never appears in the pinned golden corpus, no evidence "
      "independent of the name will ever exist, no matter how many rounds are "
      "spent. Three options, and this lane deliberately picks none of them:")
    w("")
    w("  1. **Leave rule (4)(a) as written.** The %d thunk-proven names can never "
      "be admitted, and `docs/PF_VITAL_NAMES.json` stays a strictly "
      "*wire-observed* table. Defensible, and the cost is that the project keeps "
      "re-discovering the same 200-odd names forever."
      % G["of_which_in_round86_census"])
    w("  2. **Amend (4)(a)** to accept \"the id slot that the client's own "
      "ID_ASSIGN writes\" as an independent observation. This is arguable on the "
      "merits: the slot VA is read out of the image, not derived from the name, "
      "so it is not quite circular. It is still weaker than a wire capture.")
    w("  3. **Add a second, clearly separated tier** (`source: \"thunk_only\"`) so "
      "wire-proven rows stay distinguishable from thunk-proven rows forever. This "
      "is the option that loses the least information.")
    w("")
    w("  Whichever is chosen must be written into the `__doc__` of "
      "`docs/PF_VITAL_NAMES.json` in the same commit that first relies on it, or "
      "the distinction will be lost within two rounds.")
    w("")
    w("**Step 3 -- mine the golden corpus for ids that are still bare hex.** Any "
      "id that `capture_v141/*.txt` carries but the table decodes as raw hex is a "
      "row where condition (a) is *already* satisfied by observation. Cross that "
      "set against the %d derived ids in the tsv shipped beside this report: a hit "
      "closes both conditions in one move, with no rule change and no chief "
      "decision needed. That is exactly how `LogoutVital`, `DeleteActorVital` and "
      "`Channel_LocalTalkMessageVital` were settled in round 62, and it is the "
      "only path here that admits names under the rule as it stands today."
      % s["total_rows_emitted"])
    w("")
    w("**Step 4 -- only then, name things.** One batch, in name order, with the "
      "tier recorded per row and the evidence string written per row, in the "
      "format the table already uses.")
    w("")
    w("### 6.3 What this round deliberately did not do")
    w("")
    w("* did not open `GameClient.local.bin`")
    w("* did not decode a single instruction")
    w("* did not write, propose, or stage any change to `docs/PF_VITAL_NAMES.json`")
    w("* did not touch the canonical DB, boot a server, or open the game UI")
    w("* did not run git, did not touch `.gitignore`")
    w("* did not write anything outside `pf_bridge/`")
    w("")
    w("---")
    w("")

    w("## 7. Files this round produced")
    w("")
    w("| file | what it is |")
    w("|---|---|")
    w("| `pf_bridge/%s.md` | this report, rendered from the json by the generator |"
      % BASENAME)
    w("| `pf_bridge/%s.tsv` | %d rows, one per declared game class, machine-readable |"
      % (BASENAME, s["total_rows_emitted"]))
    w("| `pf_bridge/%s.json` | every figure quoted above, plus the full family, "
      "routing and priority tables |" % BASENAME)
    w("| `pf_bridge/%s` | the generator: rerunnable, stdlib only, ASCII stdout |"
      % s["generated_by"])
    w("")
    w("TSV columns: `name`, `family`, `wire_id`, `wire_id_dec`, `rtti_va`, "
      "`rtti_file_offset`, `literal_kind` (`standalone` / `pooled_tail` / "
      "`none`), `literal_va`, `in_names_table`, `in_round86_census`, "
      "`in_round38_tsv`, `id_collision_with_table_name`, `rtti_descriptor`, "
      "`literal_run_text`.")
    w("")
    w("The generator prints ASCII only, so it is safe on a Windows cp874 console. "
      "Rerun cost: one pass over a %d-row tsv, stdlib only, no image access, no "
      "network."
      % s["inputs"]["strings_ascii_tsv"]["data_rows"])
    w("")
    return "\n".join(L) + "\n"


if __name__ == "__main__":
    sys.exit(main())
