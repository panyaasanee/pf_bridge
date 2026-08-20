"""Bounded Ctrl+C helper for the visible Foundation server console.

Attaches to the console owned by an exact target PID and raises one CTRL_C_EVENT.
Observation/control only: it sends no packets and touches no project file.

usage: py -3 pf_stop_visible_server.py <pid> [--json <path>]
"""

import ctypes
import json
import sys
import time

CTRL_C_EVENT = 0
ERROR_ACCESS_DENIED = 5

kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: pf_stop_visible_server.py <pid> [--json <path>]")
        return 2

    pid = int(sys.argv[1])
    json_path = None
    if "--json" in sys.argv:
        json_path = sys.argv[sys.argv.index("--json") + 1]

    record = {
        "target_pid": pid,
        "free_console": None,
        "attach_console": None,
        "attach_error": None,
        "ctrl_c_sent": False,
        "ctrl_c_error": None,
        "started_utc": time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime()),
    }

    # Detach from the bridge console so we can attach to the target's console.
    record["free_console"] = bool(kernel32.FreeConsole())

    attached = bool(kernel32.AttachConsole(pid))
    record["attach_console"] = attached
    if not attached:
        record["attach_error"] = ctypes.get_last_error()
    else:
        # Ignore the event in this helper process so only the target reacts.
        kernel32.SetConsoleCtrlHandler(None, True)
        sent = bool(kernel32.GenerateConsoleCtrlEvent(CTRL_C_EVENT, 0))
        record["ctrl_c_sent"] = sent
        if not sent:
            record["ctrl_c_error"] = ctypes.get_last_error()
        time.sleep(1.0)
        kernel32.FreeConsole()

    record["finished_utc"] = time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime())

    payload = json.dumps(record, indent=2)
    if json_path:
        with open(json_path, "w", encoding="utf-8") as handle:
            handle.write(payload)

    # stdout is gone after FreeConsole; the JSON sidecar is the record.
    return 0 if record["ctrl_c_sent"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
