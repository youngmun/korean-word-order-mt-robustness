import json, collections

rows = []
for fn in ["data/pairs_dev.jsonl", "data/pairs_test.jsonl"]:
    rows += [json.loads(l) for l in open(fn, encoding="utf-8")]
rows = [r for r in rows if r.get("gold_mr_violated") is not None]

by = collections.defaultdict(lambda: [0, 0])   # [위반, 정상]
for r in rows:
    by[r["cat"]][0 if r["gold_mr_violated"] else 1] += 1

print(f"전체 {len(rows)}세트, 위반 {sum(1 for r in rows if r['gold_mr_violated'])}개\n")
print(f"{'카테고리':8} {'위반':>4} {'정상':>4} {'계':>4} {'위반율':>7}")
tv = tt = 0
for c in sorted(by):
    v, nv = by[c]; tv += v; tt += v+nv
    print(f"{c:8} {v:>4} {nv:>4} {v+nv:>4} {v/(v+nv)*100:>6.1f}%")
print(f"{'전체':8} {tv:>4} {tt-tv:>4} {tt:>4} {tv/tt*100:>6.1f}%")