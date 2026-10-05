import json, csv, io

# 라벨 로드 (gold=true인 id)
viol = set()
for fn in ["data/pairs_dev.jsonl", "data/pairs_test.jsonl"]:
    for l in open(fn, encoding="utf-8"):
        r = json.loads(l)
        if r.get("gold_mr_violated") is True:
            viol.add(r["id"])

def read_any(path):
    for enc in ("utf-8-sig","cp949","utf-8"):
        try: return open(path,encoding=enc).read()
        except UnicodeDecodeError: continue

rows = []
for fn in ["data/label_dev.csv", "data/label_test.csv"]:
    for r in csv.DictReader(io.StringIO(read_any(fn))):
        if r["id"] in viol:
            rows.append(r)

with open("data/failures.csv","w",encoding="utf-8-sig",newline="") as f:
    w = csv.writer(f)
    w.writerow(["id","cat","src_orig","src_trans","O_orig","O_trans","원인(어순/오역)"])
    for r in rows:
        w.writerow([r["id"],r["cat"],r["src_orig"],r["src_trans"],
                    r["O_orig(번역)"],r["O_trans(번역)"],""])
print(f"{len(rows)}개 실패 사례 -> data/failures.csv")