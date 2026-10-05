import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
os.environ["OMP_NUM_THREADS"] = "1"
import json, csv, argparse
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

def load_llm(name):
    tok = AutoTokenizer.from_pretrained(name)
    model = AutoModelForCausalLM.from_pretrained(
        name, dtype=torch.float16 if DEVICE=="cuda" else torch.float32,
        low_cpu_mem_usage=True)
    model.to(DEVICE); model.eval()
    return tok, model

def translate(text, tok, model):
    msgs = [{"role":"system","content":"Translate the following Korean sentence to English. Output only the translation."},
            {"role":"user","content":text}]
    prompt = tok.apply_chat_template(msgs, tokenize=False, add_generation_prompt=True)
    inp = tok(prompt, return_tensors="pt").to(model.device)
    with torch.no_grad():
        out = model.generate(**inp, max_new_tokens=64, do_sample=False)
    return tok.decode(out[0][inp.input_ids.shape[1]:], skip_special_tokens=True).strip()

def main(a):
    tok, model = load_llm(a.llm)
    rows = [json.loads(l) for l in open(a.pairs, encoding="utf-8")]
    with open(a.out, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["id","cat","src_orig","src_trans","O_orig(번역)","O_trans(번역)",
                    "gold_mr_violated(true/false)","note"])
        for i, r in enumerate(rows, 1):
            o_orig = translate(r["src_orig"], tok, model)
            o_trans = translate(r["src_trans"], tok, model)
            w.writerow([r["id"], r["cat"], r["src_orig"], r["src_trans"],
                        o_orig, o_trans, "", ""])
            if i % 20 == 0:
                print(f"  {i}/{len(rows)}")
    print(f"완료: {len(rows)}행 -> {a.out}")

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--pairs", required=True)
    p.add_argument("--out", required=True)
    p.add_argument("--llm", default="Qwen/Qwen2.5-1.5B-Instruct")
    main(p.parse_args())