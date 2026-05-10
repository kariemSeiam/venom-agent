#!/usr/bin/env python3
"""
VENOM Compass — Proprioceptor (L12)
Runs every 40 minutes. Checks system state, swarm health, ven0m status.
Delivers a direction pulse to Kariem.
"""

import json
import subprocess
import sys
from datetime import datetime

def run(cmd, timeout=15):
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
        return r.stdout.strip()
    except:
        return "ERR"

def main():
    now = datetime.utcnow().strftime("%H:%M UTC")
    
    # 1. System vitals
    load = run("cat /proc/loadavg | awk '{print $1,$2,$3}'")
    mem = run("free -m | awk 'NR==2{printf \"%d/%dMB (%.0f%%)\", $3,$2,$3*100/$2}'")
    disk = run("df -h / | awk 'NR==2{print $3\"/\"$2\" (\"$5\")\"}'")
    
    # 2. Swarm health — which workers are alive
    swarm_check = run("for id in swarm1 swarm2 swarm3 swarm4 swarm5 swarm6 swarm7 swarm8 swarm9 swarm10 swarm11 swarm12; do tmux has-session -t $id 2>/dev/null && echo \"$id:ALIVE\" || echo \"$id:DOWN\"; done")
    alive = [w.split(":")[0] for w in swarm_check.split("\n") if "ALIVE" in w]
    alive_count = len(alive)
    
    # 3. Fang fleet ports
    fleet = {}
    for name, port in [("Pi", 3001), ("Claude", 3002), ("Cursor", 3003), ("OpenCode", 3004), ("Claw", 3005)]:
        fleet[name] = "UP" if run(f"curl -s --max-time 2 http://localhost:{port}/health") else "DOWN"
    
    # 4. ven0m repo state
    ven0m_branch = run("cd /root/ven0m && git branch --show-current 2>/dev/null")
    ven0m_status = run("cd /root/ven0m && git status --short 2>/dev/null | wc -l")
    ven0m_tests = run("cd /root/ven0m && python -m pytest tests/ -q --tb=no 2>&1 | tail -1")
    
    # 5. Hermes main agent
    hermes_model = run("grep 'model:' ~/.hermes/config.yaml 2>/dev/null | head -1")
    
    # 6. MCRM health
    mcrm = run("curl -s --max-time 5 http://localhost:5252/health 2>/dev/null | head -1") or "offline"
    
    # Build compass reading
    lines = [
        f"🧭 VENOM Compass — {now}",
        f"",
        f"📊 System: load={load} | mem={mem} | disk={disk}",
        f"",
        f"🐙 Swarm: {alive_count}/12 alive | {', '.join(alive) if alive else 'none'}",
        f"🐺 Fleet: Pi={fleet['Pi']} Claude={fleet['Claude']} Cursor={fleet['Cursor']} OpenCode={fleet['OpenCode']} Claw={fleet['Claw']}",
        f"",
        f"📦 ven0m: branch={ven0m_branch} | dirty={ven0m_status} files | {ven0m_tests}",
        f"🧠 Main: {hermes_model}",
        f"🏥 MCRM: {mcrm[:60]}",
    ]
    
    # Decision: is anything wrong?
    issues = []
    if alive_count == 0:
        issues.append("⚠️ No swarm workers running")
    if int(ven0m_status or 0) > 5:
        issues.append(f"⚠️ ven0m has {ven0m_status} uncommitted files")
    if "DOWN" in fleet.values():
        down = [k for k,v in fleet.items() if v == "DOWN"]
        issues.append(f"⚠️ Fleet down: {', '.join(down)}")
    if "failed" in ven0m_tests.lower():
        issues.append(f"⚠️ Tests failing: {ven0m_tests}")
    
    if issues:
        lines.append("")
        lines.append("— Flags —")
        lines.extend(issues)
    else:
        lines.append("")
        lines.append("✅ All green.")
    
    print("\n".join(lines))

if __name__ == "__main__":
    main()
