import json, random, collections

IN = r"data\pairs_reviewed.jsonl"
DEV_RATIO = 0.3          # dev 30% / test 70%
SEED = 42

rows = [json.loads(l) for l in open(IN, encoding="utf-8")]

# 카테고리별로 묶어 층화 분할
by_cat = collections.defaultdict(list)
for r in rows:
    by_cat[r["cat"]].append(r)

rng = random.Random(SEED)
dev, test = [], []
for cat, items in by_cat.items():
    items = items[:]            # 복사
    rng.shuffle(items)
    k = round(len(items) * DEV_RATIO)
    dev.extend(items[:k])
    test.extend(items[k:])

rng.shuffle(dev); rng.shuffle(test)

with open(r"data\pairs_dev.jsonl", "w", encoding="utf-8") as f:
    for r in dev:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")
with open(r"data\pairs_test.jsonl", "w", encoding="utf-8") as f:
    for r in test:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")

def dist(rs): return dict(sorted(collections.Counter(r["cat"] for r in rs).items()))
print(f"dev  {len(dev)}세트  {dist(dev)}")
print(f"test {len(test)}세트  {dist(test)}")
print(f"(seed={SEED}, dev_ratio={DEV_RATIO} — 논문에 명시)")