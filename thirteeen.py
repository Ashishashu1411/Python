import re
import csv
import argparse
import os
import sys
from collections import Counter, defaultdict

ALERT_FILE = "alert"   # default to local "alert" file for portability

# Regex patterns
# Header line: [**] [1:1000001:1] msg [**]
re_sid = re.compile(r"\[\*\*\]\s*\[(?P<gen>\d*):(?P<sid>\d+):(?P<rev>\d+)\]\s*(?P<msg>.+?)\s*\[\*\*\]")
# address line: 11/05-20:30:12.345678 192.0.2.15:1234 -> 192.168.1
re_addr = re.compile(r"(?P<ts>\d{2}/\d{2}-\d{2}:\d{2}:\d{2}\.\d+)\s+(?P<src>[\d\.]+)(?::(?P<srcp>\d+))?\s+->\s+(?P<dst>[\d\.]+)(?::(?P<dstp>\d+))?")

def parse_alert_file(path):
    events = []
    with open(path, 'r', errors='ignore') as f:
        lines = [ln.rstrip() for ln in f]

    i = 0
    while i < len(lines):
        line = lines[i]
        m = re_sid.search(line)
        if m:
            sid = m.group('sid')
            msg = m.group('msg').strip()
            # next non-empty line likely contains addresses
            j = i + 1
            addr_line = ""
            while j < len(lines) and not lines[j].strip():
                j += 1
            if j < len(lines):
                addr_line = lines[j]
            am = re_addr.search(addr_line)
            if am:
                events.append({
                    "sid": sid,
                    "msg": msg,
                    "timestamp": am.group('ts'),
                    "src": am.group('src'),
                    "src_port": am.group('srcp') or "",
                    "dst": am.group('dst'),
                    "dst_port": am.group('dstp') or ""
                })
                i = j
            else:
                # no addr match — still record SID/msg
                events.append({"sid": sid, "msg": msg, "timestamp": "", "src": "", "src_port": "", "dst": "", "dst_port": ""})
        i += 1
    return events

def summarize(events, topn=10):
    sid_counts = Counter()
    src_counts = Counter()
    dstport_counts = Counter()
    by_sid = defaultdict(list)

    for e in events:
        sid_counts[e['sid']] += 1
        if e['src']:
            src_counts[e['src']] += 1
        if e['dst_port']:
            dstport_counts[e['dst_port']] += 1
        by_sid[e['sid']].append(e)

    print("=== Snort Alert Summary ===")
    print(f"Total events parsed: {len(events)}\n")

    print("Top SIDs:")
    for sid, cnt in sid_counts.most_common(topn):
        print(f" SID {sid}: {cnt} alerts  -> Message example: {by_sid[sid][0]['msg'] if by_sid[sid] else ''}")
    print()

    print("Top Source IPs:")
    for ip, cnt in src_counts.most_common(topn):
        print(f" {ip}: {cnt}")
    print()

    print("Top Destination Ports:")
    for p, cnt in dstport_counts.most_common(topn):
        print(f" {p}: {cnt}")
    print()

def export_csv(events, outpath="snort_events_summary.csv"):
    with open(outpath, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=["timestamp","sid","msg","src","src_port","dst","dst_port"])
        w.writeheader()
        for e in events:
            w.writerow({
                "timestamp": e.get("timestamp",""),
                "sid": e.get("sid",""),
                "msg": e.get("msg",""),
                "src": e.get("src",""),
                "src_port": e.get("src_port",""),
                "dst": e.get("dst",""),
                "dst_port": e.get("dst_port","")
            })
    print(f"Exported {len(events)} events to {outpath}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Parse Snort ascii alert file and summarize.")
    parser.add_argument("-f","--file", help="Path to Snort alert file", default=ALERT_FILE)
    parser.add_argument("--csv", help="Export parsed events to CSV", action="store_true")
    parser.add_argument("--top", help="Top N list length", type=int, default=10)
    args = parser.parse_args()

    events = parse_alert_file(args.file)
    summarize(events, topn=args.top)
    if args.csv:
        export_csv(events)
