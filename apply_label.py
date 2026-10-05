import json, csv, argparse, collections
import io
def read_text_any(path):
    for enc in ("utf-8-sig", "cp949", "utf-8"):
        try:
            return open(path, encoding=enc).read(), enc
        except UnicodeDecodeError:
            continue
    raise SystemExit(f"{path}: 인코딩 판별 실패")
def main(a):
    # CSV에서 라벨 로드
    label = {}
 
    text, enc = read_text_any(a.csv)
    print(f"(CSV 인코딩: {enc})")
    for row in csv.DictReader(io.StringIO(text)):
            v = row["gold_mr_violated(true/false)"].strip().lower()
            if v in ("true", "false"):
                label[row["id"]] = (v == "true")

    rows = [json.loads(l) for l in open(a.pairs, encoding="utf-8")]
    labeled, missing = 0, []
    for r in rows:
        if r["id"] in label:
            r["gold_mr_violated"] = label[r["id"]]
            labeled += 1
        else:
            missing.append(r["id"])

    with open(a.pairs, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    viol = sum(1 for r in rows if r["gold_mr_violated"] is True)
    print(f"{labeled}/{len(rows)} 라벨됨 -> {a.pairs}")
    print(f"MR 위반(true): {viol}, 정상(false): {labeled-viol}")
    if missing:
        print(f"[미라벨 {len(missing)}건] {missing[:10]}{'...' if len(missing)>10 else ''}")
    # 카테고리별 위반율
    by = collections.defaultdict(lambda: [0,0])
    for r in rows:
        if r["gold_mr_violated"] is not None:
            by[r["cat"]][0 if r["gold_mr_violated"] else 1] += 1
    print("카테고리별 (위반/정상):")
    for c in sorted(by):
        v, nv = by[c]
        print(f"  {c}: {v}/{nv}  위반율 {v/(v+nv)*100:.0f}%")

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--pairs", required=True)
    p.add_argument("--csv", required=True)
    main(p.parse_args())