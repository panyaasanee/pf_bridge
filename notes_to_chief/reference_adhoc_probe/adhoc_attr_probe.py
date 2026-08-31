"""AD-HOC ActorAttr probe lane (owner-sanctioned experiment, NOT a production lane).

Enabled only when the environment variable PF_ADHOC_ATTR_PROBE=1 is set at
server start.  Chat input frames (0xAC52) typed by the attended tester are
parsed as commands:

    probe <x> <y>      set field x (1..55, see FIELDS) to value y, then send the
                       WHOLE current ActorAttr block as one UpdateAttrVital
    probe base [cls]   fill the 22 named fields from the client tables
                       (CHARCREATE_CLASS s_SCORE, level 1, exp 0 ...) -- group 1
    probe reset        back to the minimal start-game baseline
    probe show         print the current block to the server console
    probe help         list the fields in the client chat (5 per line)

Every send carries the FULL block because the client's ActorAttr apply copies
the incoming object whole (v141 note on 0x464F30) -- a sparse delta would zero
what it omits.  State lives on the session object (per connection) and is
never written to the database.

Field table: reports/PF_CHUNK2_Q1_ACTORATTR_MASK_FINDINGS_20260819.md (43
ActorAttr rows + 12 BasicAttr rows, every row pinned to a gate VA) and
stats_progression_hypothesis.py (names with a proven consumer).
"""
import os
import struct

ENABLED = os.environ.get("PF_ADHOC_ATTR_PROBE", "") == "1"

CHAT_INPUT_VITAL_ID = 0xAC52
UPDATE_ATTR_VITAL_ID = 0x309A
ACTOR_ATTR_ID = 0x12AD
DB_ATTRIBUTE_IDENTITY_BIT = 1
ACTOR_ATTR_EXTRA_GROUP_VALUE = 1

# x, block, mask_bit, offset, tag, kind, name, note
# kinds: u8 u16 u32 i32 f32 u64 wstr blob
FIELDS = (
    (1,  "basic", 0x0001, 0x028, 0x48, "wstr", "NAME",            "[รู้] ป้ายชื่อ LABEL_NAME"),
    (2,  "basic", 0x0002, 0x05E, 0x12, "u16",  "level",           "[รู้] GetLv"),
    (3,  "basic", 0x0004, 0x044, 0x14, "u32",  "hp_current",      "[รู้] HP bar"),
    (4,  "basic", 0x0008, 0x048, 0x14, "u32",  "hp_max",          "[รู้]"),
    (5,  "basic", 0x0010, 0x04C, 0x14, "u32",  "mp_current",      "[รู้]"),
    (6,  "basic", 0x0020, 0x050, 0x14, "u32",  "mp_max",          "[รู้]"),
    (7,  "basic", 0x0040, 0x054, 0x2A, "f32",  "basic_f32_54",    "[ไม่รู้] f32"),
    (8,  "basic", 0x0080, 0x058, 0x2A, "f32",  "death_timer",     "[รู้] dying countdown f32"),
    (9,  "basic", 0x0100, 0x05C, 0x12, "u16",  "category_5C",     "[รู้บางส่วน] ==8 สลับ HP ไป x52/53 (เดิมเรียก scene id)"),
    (10, "basic", 0x0200, 0x060, 0x32, "u64",  "basic_q60",       "[ไม่รู้] (เดิมเรียก scene seq)"),
    (11, "basic", 0x0400, 0x068, 0x14, "u32",  "basic_faction",   "[รู้] 1 = ฝ่ายผู้เล่น"),
    (12, "basic", 0x0800, 0x06C, 0x14, "u32",  "basic_u32_6C",    "[ไม่รู้]"),
    (13, "actor", 1 << 0,  0x08C, 0x19, "u32",  "class_id",        "[รู้] GetClass (1 Gladiator 2 Paladin 4 Sniper 16 Necro 32 Sorcerer)"),
    (14, "actor", 1 << 1,  0x090, 0x19, "u32",  "nameboard_key",   "[รู้บางส่วน] NameBoard nickname key"),
    (15, "actor", 1 << 2,  0x078, 0x26, "i32",  "actor_x26_78",    "[ไม่รู้] tag 0x26"),
    (16, "actor", 1 << 3,  0x07C, 0x19, "u32",  "skill_points",    "[รู้] SP"),
    (17, "actor", 1 << 4,  0x080, 0x12, "u16",  "unspent_points",  "[รู้] แต้มอัพสเตตัสค้าง"),
    (18, "actor", 1 << 5,  0x082, 0x12, "u16",  "str",             "[รู้] LABEL_STR"),
    (19, "actor", 1 << 6,  0x084, 0x12, "u16",  "con",             "[รู้] LABEL_CON"),
    (20, "actor", 1 << 7,  0x086, 0x12, "u16",  "dex",             "[รู้] LABEL_DEX"),
    (21, "actor", 1 << 8,  0x088, 0x12, "u16",  "int",             "[รู้] LABEL_INT"),
    (22, "actor", 1 << 9,  0x08A, 0x12, "u16",  "per",             "[รู้] LABEL_PER"),
    (23, "actor", 1 << 10, 0x0A0, 0x32, "u64",  "experience",      "[รู้] XP bar"),
    (24, "actor", 1 << 11, 0x0A8, 0x32, "u64",  "cash",            "[รู้] GetCash"),
    (25, "actor", 1 << 12, 0x0B0, 0x48, "wstr", "wstr_B0",         "[ไม่รู้] ข้อความ 1"),
    (26, "actor", 1 << 13, 0x099, 0x0B, "u8",   "u8_99",           "[ไม่รู้]"),
    (27, "actor", 1 << 14, 0x09A, 0x0B, "u8",   "u8_9A",           "[ไม่รู้]"),
    (28, "actor", 1 << 15, 0x13E, 0x12, "u16",  "u16_13E",         "[ไม่รู้]"),
    (29, "actor", 1 << 16, 0x13C, 0x12, "u16",  "u16_13C",         "[ไม่รู้]"),
    (30, "actor", 1 << 17, 0x148, 0x44, "blob", "blob_148",        "[ไม่รู้] hex"),
    (31, "actor", 1 << 18, 0x182, 0x12, "u16",  "bonus_str",       "[รู้]"),
    (32, "actor", 1 << 19, 0x184, 0x12, "u16",  "bonus_con",       "[รู้]"),
    (33, "actor", 1 << 20, 0x186, 0x12, "u16",  "bonus_dex",       "[รู้]"),
    (34, "actor", 1 << 21, 0x188, 0x12, "u16",  "bonus_int",       "[รู้]"),
    (35, "actor", 1 << 22, 0x18A, 0x12, "u16",  "bonus_per",       "[รู้]"),
    (36, "actor", 1 << 23, 0x18C, 0x0B, "u8",   "u8_18C",          "[ไม่รู้]"),
    (37, "actor", 1 << 24, 0x164, 0x48, "wstr", "wstr_164_guild",  "[รู้] -> LABEL_GUILD (เราเคยส่งชื่อตัวละครลงช่องนี้)"),
    (38, "actor", 1 << 25, 0x180, 0x0B, "u8",   "u8_180",          "[ไม่รู้]"),
    (39, "actor", 1 << 26, 0x098, 0x0B, "u8",   "u8_98_pairA",     "[ไม่รู้] บิตร่วมกับ x40"),
    (40, "actor", 1 << 26, 0x094, 0x19, "u32",  "u32_94_pairA",    "[ไม่รู้] บิตร่วมกับ x39"),
    (41, "actor", 1 << 27, 0x140, 0x32, "u64",  "q_140_pairB",     "[ไม่รู้] บิตร่วมกับ x42"),
    (42, "actor", 1 << 27, 0x09B, 0x0B, "u8",   "u8_9B_pairB",     "[ไม่รู้] บิตร่วมกับ x41"),
    (43, "actor", 1 << 28, 0x0CC, 0x48, "wstr", "wstr_CC",         "[ไม่รู้] ข้อความ 2"),
    (44, "actor", 1 << 29, 0x198, 0x32, "u64",  "q_198",           "[ไม่รู้]"),
    (45, "actor", 1 << 30, 0x190, 0x32, "u64",  "q_190",           "[ไม่รู้]"),
    (46, "actor", 1 << 32, 0x1A0, 0x0B, "u8",   "u8_1A0",          "[ไม่รู้]"),
    (47, "actor", 1 << 33, 0x1A2, 0x12, "u16",  "u16_1A2",         "[ไม่รู้]"),
    (48, "actor", 1 << 34, 0x1A4, 0x12, "u16",  "u16_1A4",         "[ไม่รู้]"),
    (49, "actor", 1 << 35, 0x0E8, 0x48, "wstr", "wstr_E8",         "[ไม่รู้] ข้อความ 3"),
    (50, "actor", 1 << 36, 0x104, 0x48, "wstr", "wstr_104",        "[ไม่รู้] ข้อความ 4"),
    (51, "actor", 1 << 37, 0x120, 0x48, "wstr", "wstr_120",        "[ไม่รู้] ข้อความ 5"),
    (52, "actor", 1 << 38, 0x1A8, 0x14, "u32",  "alt_hp_current",  "[รู้] ใช้เมื่อ x9 == 8"),
    (53, "actor", 1 << 39, 0x1AC, 0x14, "u32",  "alt_hp_max",      "[รู้]"),
    (54, "actor", 1 << 40, 0x1B0, 0x12, "u16",  "u16_1B0",         "[ไม่รู้]"),
    (55, "actor", 1 << 41, 0x1B2, 0x0B, "u8",   "u8_1B2",          "[ไม่รู้]"),
)
BY_X = {f[0]: f for f in FIELDS}

# CHARCREATE_CLASS.s_SCORE per class id (client table, 6 numbers; the first
# five are mapped STR/CON/DEX/INT/PER here -- [เดา], the 6th is not used).
CLASS_SCORE = {
    1: (4, 3, 4, 1, 1, 2),
    2: (4, 3, 4, 1, 1, 3),
    4: (1, 3, 4, 1, 3, 2),
    16: (4, 1, 3, 5, 1, 3),
    32: (2, 5, 1, 3, 2, 4),
}
CLASS_NAME = {1: "Gladiator", 2: "Paladin", 4: "Sniper", 16: "Necromancer", 32: "Sorcerer"}

INITIAL_CASH = 10000
MP_PLACEHOLDER = 50   # probe value, no table source -- flagged in the log


class ProbeState:
    """Per-connection current ActorAttr block, keyed by x."""

    def __init__(self, identity_lo, identity_hi, name, scene_id, scene_seq):
        self.identity_lo = identity_lo
        self.identity_hi = identity_hi
        self.name = name
        self.scene_id = scene_id
        self.scene_seq = scene_seq
        self.values = {}
        self.sent = 0
        self.reset()

    def reset(self):
        """The exact start-game baseline player_wire puts on the wire today."""
        self.values = {
            3: 100, 4: 100,
            9: self.scene_id, 10: self.scene_seq, 11: 1,
            24: INITIAL_CASH, 37: self.name,
        }

    def base(self, class_id):
        """Group 1: fill the named fields from the client tables."""
        score = CLASS_SCORE.get(class_id)
        if score is None:
            raise ValueError("unknown class id %d (known: %s)" % (
                class_id, ",".join(str(k) for k in sorted(CLASS_SCORE))))
        self.reset()
        self.values.update({
            1: self.name,          # NAME wstring (LABEL_NAME)
            2: 1,                  # level 1
            5: MP_PLACEHOLDER, 6: MP_PLACEHOLDER,   # MP placeholder (no table)
            13: class_id,          # class
            16: 0, 17: 0,          # skill points / unspent
            18: score[0], 19: score[1], 20: score[2], 21: score[3], 22: score[4],
            23: 0,                 # experience
            31: 0, 32: 0, 33: 0, 34: 0, 35: 0,
        })


def parse_value(kind, text):
    if kind in ("u8", "u16", "u32", "u64"):
        v = int(text, 0)
        width = {"u8": 1, "u16": 2, "u32": 4, "u64": 8}[kind]
        if v < 0 or v >= (1 << (8 * width)):
            raise ValueError("value out of range for %s" % kind)
        return v
    if kind == "i32":
        v = int(text, 0)
        if v < -(1 << 31) or v >= (1 << 31):
            raise ValueError("value out of range for i32")
        return v
    if kind == "f32":
        return float(text)
    if kind == "wstr":
        return text.replace("_", " ")
    if kind == "blob":
        return bytes.fromhex(text)
    raise ValueError("unknown kind " + kind)


def encode_field(legacy, field, value):
    _x, _blk, _bit, _off, tag, kind, _name, _note = field
    if kind == "u8":
        return legacy.u8tag(tag, value)
    if kind == "u16":
        return legacy.u16tag(tag, value)
    if kind == "u32":
        return legacy.u32tag(tag, value)
    if kind == "i32":
        return bytes([tag]) + struct.pack("<i", value)
    if kind == "f32":
        return bytes([tag]) + struct.pack("<f", float(value))
    if kind == "u64":
        return legacy.qwordtag(tag, value)
    if kind == "wstr":
        b = value.encode("utf-16le")
        return bytes([tag]) + struct.pack("<I", len(b)) + b
    if kind == "blob":
        return bytes([tag]) + struct.pack("<I", len(value)) + bytes(value)
    raise ValueError(kind)


def encode_block(legacy, state):
    """DBAttribute -> BasicAttr(mask u16 + fields asc) -> ActorAttr(mask qword + flag + fields asc)."""
    basic_mask = 0
    basic_body = b""
    actor_mask = 0
    actor_body = b""
    # FIELDS is already in ascending bit order within each block; paired bits
    # keep the report's row order (u8 +0x98 then u32 +0x94; qword +0x140 then u8 +0x9B).
    for f in FIELDS:
        x, blk, bit = f[0], f[1], f[2]
        if x not in state.values:
            continue
        if blk == "basic":
            basic_mask |= bit
            basic_body += encode_field(legacy, f, state.values[x])
        else:
            actor_mask |= bit
            actor_body += encode_field(legacy, f, state.values[x])
    # paired bits: if one half is set the other must be emitted too (value 0)
    for a, b in ((39, 40), (41, 42)):
        if (a in state.values) != (b in state.values):
            raise ValueError("fields %d and %d share one mask bit - set both (probe %d 0)" % (a, b, b if a in state.values else a))
    body = (
        legacy.u8tag(0x0B, DB_ATTRIBUTE_IDENTITY_BIT)
        + bytes([0x32]) + struct.pack("<II", state.identity_lo & 0xFFFFFFFF, state.identity_hi & 0xFFFFFFFF)
        + legacy.u16tag(0x12, basic_mask)
        + basic_body
        + legacy.qwordtag(0x32, actor_mask)
        + legacy.u8tag(0x05, ACTOR_ATTR_EXTRA_GROUP_VALUE)
        + actor_body
    )
    return body, basic_mask, actor_mask


def make_update_attr_frames(legacy, state):
    body, bm, am = encode_block(legacy, state)
    payload = (
        legacy.u16tag(0x12, 1)
        + legacy.u16tag(0x12, ACTOR_ATTR_ID)
        + legacy.u32tag(0x14, len(body))
        + body
    )
    pc, frame = legacy.make_runtime_vitals([(UPDATE_ATTR_VITAL_ID, 0, payload)])
    return pc, frame, body, bm, am


def decode_chat_text(payload):
    """Read every tag-0x48 wstring in the 0xAC52 payload; return the last non-empty one."""
    texts = []
    i = 0
    n = len(payload)
    while i < n:
        tag = payload[i]
        if tag == 0x48 and i + 5 <= n:
            ln = struct.unpack_from("<I", payload, i + 1)[0]
            raw = payload[i + 5:i + 5 + ln]
            try:
                texts.append(raw.decode("utf-16le", errors="replace"))
            except Exception:
                texts.append("")
            i += 5 + ln
        else:
            i += 1
    for t in reversed(texts):
        if t.strip():
            return t.strip()
    return ""


def fmt_value(kind, v):
    if kind == "blob":
        return bytes(v).hex()
    if kind == "wstr":
        return '"%s"' % v
    return str(v)


def state_lines(state):
    out = []
    for f in FIELDS:
        x = f[0]
        if x in state.values:
            out.append("  x=%-2d %-16s = %s" % (x, f[6], fmt_value(f[5], state.values[x])))
    return out


def dispatch(session, legacy, parsed):
    """Handle one 0xAC52 chat frame.  Returns the runtime action list."""
    session.rx_frames += 1
    text = decode_chat_text(parsed.nested_payload)
    words = text.split()
    if not words or words[0].lower() != "probe":
        print("ADHOC_PROBE ignored_chat text=%r" % text, flush=True)
        return []
    selected = session.foundation.selected
    if selected is None:
        print("ADHOC_PROBE no_selected_character", flush=True)
        return []
    st = getattr(session, "_adhoc_probe_state", None)
    if st is None:
        pos = selected.position
        st = ProbeState(selected.identity_lo, selected.identity_hi, selected.name,
                        pos.scene_id, pos.scene_seq)
        session._adhoc_probe_state = st
    cmd = words[1].lower() if len(words) > 1 else "help"
    msg = None
    try:
        if cmd == "help":
            names = ["%d=%s" % (f[0], f[6]) for f in FIELDS]
            actions = []
            for i in range(0, len(names), 5):
                pc, frame = legacy.make_show_message("probe: " + " ".join(names[i:i + 5]))
                actions.append(("ADHOC_PROBE_HELP", pc, frame, 0.0 if i == 0 else 0.15))
            return actions
        if cmd == "show":
            print("ADHOC_PROBE show sent=%d" % st.sent, flush=True)
            for line in state_lines(st):
                print(line, flush=True)
            pc, frame = legacy.make_show_message("probe: state printed on server console (%d fields)" % len(st.values))
            return [("ADHOC_PROBE_SHOW", pc, frame, 0.0)]
        if cmd == "reset":
            st.reset()
            msg = "probe reset -> minimal baseline"
        elif cmd == "base":
            cls = int(words[2], 0) if len(words) > 2 else 1
            st.base(cls)
            msg = "probe base class=%d %s (MP %d/%d placeholder)" % (cls, CLASS_NAME.get(cls, "?"), MP_PLACEHOLDER, MP_PLACEHOLDER)
        else:
            x = int(cmd, 0)
            if x not in BY_X:
                raise ValueError("x must be 1..55 (b31 has no field)")
            if len(words) < 3:
                raise ValueError("usage: probe x y")
            f = BY_X[x]
            val = parse_value(f[5], words[2])
            st.values[x] = val
            # paired bit: make sure the partner exists
            pair = {39: 40, 40: 39, 41: 42, 42: 41}.get(x)
            if pair is not None and pair not in st.values:
                st.values[pair] = 0 if BY_X[pair][5] != "wstr" else ""
            msg = "probe x=%d %s = %s %s" % (x, f[6], fmt_value(f[5], val), f[7])
        pc, frame, body, bm, am = make_update_attr_frames(legacy, st)
    except Exception as exc:  # fail loud on the console AND in the client chat
        print("ADHOC_PROBE rejected text=%r reason=%s" % (text, exc), flush=True)
        pc, frame = legacy.make_show_message("probe rejected: %s" % exc)
        return [("ADHOC_PROBE_REJECTED", pc, frame, 0.0)]
    st.sent += 1
    print("ADHOC_PROBE send#%d cmd=%r basic_mask=0x%04X actor_mask=0x%016X body=%dB pc=%dB" % (
        st.sent, text, bm, am, len(body), len(pc)), flush=True)
    for line in state_lines(st):
        print(line, flush=True)
    print("ADHOC_PROBE body_hex=" + body.hex(), flush=True)
    mpc, mframe = legacy.make_show_message("[%d] %s" % (st.sent, msg))
    return [
        ("ADHOC_PROBE_UPDATE_ATTR_%d" % st.sent, pc, frame, 0.0),
        ("ADHOC_PROBE_ECHO_%d" % st.sent, mpc, mframe, 0.3),
    ]
