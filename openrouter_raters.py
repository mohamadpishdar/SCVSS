"""Amendment 02: raters R3 and R4 via OpenRouter (items 2-6 and 9-11 of amendment_02_R3_R4_openrouter.md).

Modes (exactly one):
  --dry-run          no network call and no key read: checks freeze, prompt hash (variant 3), text hashes, builds all
                     363 prompts and request bodies for R3 and R4, prints counts and the cost estimate (item 9).
  --smoke            item 10: each rater codes the first 3 texts of its seeded order outside the human coding form.
                     Prints only call status, parse success, provider and token counts.
  --run R3 R4        full run (item 3); refused unless the smoke test passed for BOTH raters. Findings with a parsed
                     record are skipped, so running the same command again is the one rerun of failed findings.
  --status           counts only: parsed, failed records, missing findings per rater and group (item 11).

The frozen rule2.py is imported and not changed (SYSTEM_PROMPT, render_user, decode, codebook, check_freeze, SEED,
human_pick, append, jsonl). The API key is read at call time only from KEY_PATH, stripped of whitespace, and is
never printed, logged or written; every error text is scrubbed of it before it is stored or printed.
Answer content is never printed by any mode.
Usage: python -I work/rule2/scripts/openrouter_raters.py --dry-run | --smoke | --run R3 R4 | --status"""
import hashlib, json, random, re, sys, time, urllib.error, urllib.request
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from pathlib import Path

S = Path(__file__).resolve().parent
OUT = S.parent
sys.path.insert(0, str(S.parents[2]))
import rule2 as R2  # noqa: E402

KEY_PATH = Path(r"C:\Workdir\Develop\secrets\openrouter_key.txt")
URL = "https://openrouter.ai/api/v1/chat/completions"
RATERS = {  # item 2 and 4: rater -> (model, provider slug, prompt variant, replicate, seed or None, $/M input, $/M output)
    "R3": ("qwen/qwen3-235b-a22b-2507", "parasail", 3, 1, 20261125, 0.14, 0.80),
    "R4": ("deepseek/deepseek-chat-v3-0324", "siliconflow", 3, 1, None, 0.25, 1.00),
}
TEMPERATURE, MAX_TOKENS = 0, 6000                # item 3, as rule2.call_openai
TIMEOUT, ATTEMPTS, WORKERS = 900, 4, 2           # item 3
N_SMOKE = 3                                       # item 10
LOG = OUT / "openrouter_run.log"
ANS = {r: OUT / f"answers_{r}_openrouter.jsonl" for r in RATERS}
_KEY = None


def key():
    global _KEY
    if _KEY is None:
        _KEY = KEY_PATH.read_text(encoding="utf-8").strip()
        if not _KEY:
            sys.exit("API key file is empty.")
    return _KEY


def scrub(s):
    s = str(s)
    return s.replace(_KEY, "[KEY]") if _KEY else s


def say(m):
    m = scrub(m)
    print(m, flush=True)
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(m + "\n")


# ------------------------------------------------------------------ texts and checks (items 3, 5)
def load_texts():
    R2.check_freeze(strict=True)
    frz = json.loads((OUT / "freeze.json").read_text(encoding="utf-8"))
    cb = R2.codebook()
    h3 = hashlib.sha256((R2.SYSTEM_PROMPT + R2.render_user(cb, 3, "TITLE", "TEXT")).encode()).hexdigest()
    assert h3 == frz["prompt_sha256"]["variant_3"], "prompt variant 3 differs from freeze.json"
    fp = OUT / "redacted.jsonl"
    assert R2.sha(fp) == frz["redacted_sha256"], "redacted.jsonl differs from freeze.json"
    cbp = OUT / "controlB_redacted_v2.jsonl"
    e15 = json.loads((OUT / "amendments.json").read_text(encoding="utf-8"))[14]
    assert e15["file"].endswith("controlB_redacted_v2.jsonl")
    assert hashlib.sha256(cbp.read_bytes().replace(b"\r\n", b"\n")).hexdigest() == e15["lf_sha256"], "control-B v2 differs from entry 15"
    red = {}
    for p in (fp, cbp):
        for l in p.read_text(encoding="utf-8").splitlines():
            if l.strip():
                x = json.loads(l)
                assert x["finding_id"] not in red, f"duplicate {x['finding_id']}"
                red[x["finding_id"]] = x
    groups = {"main": {r["finding_id"] for r in R2.read_csv(OUT / "selection_sample.csv")},
              "original control": {r["finding_id"] for r in R2.read_csv(OUT / "fresh_sample.csv")},
              "control-B": {r["finding_id"] for r in R2.read_csv(OUT / "controlB_sample.csv")}}
    assert set(red) == set().union(*groups.values()), "redacted texts and samples differ"
    return cb, red, groups, frz, h3


def order(rater, red):
    o = sorted(red)
    random.Random(R2.SEED + "-order-" + rater).shuffle(o)
    return o


def smoke_ids(rater, red):
    human = {r["finding_id"] for r in R2.human_pick()[0]}
    return [f for f in order(rater, red) if f not in human][:N_SMOKE]


def body(rater, cb, x):
    model, slug, variant, _, seed, *_ = RATERS[rater]
    b = {"model": model, "temperature": TEMPERATURE, "max_tokens": MAX_TOKENS,
         "messages": [{"role": "system", "content": R2.SYSTEM_PROMPT},
                      {"role": "user", "content": R2.render_user(cb, variant, x["title"], x["text"])}],
         "provider": {"order": [slug], "allow_fallbacks": False, "require_parameters": True, "data_collection": "deny"}}
    if seed is not None:
        b["seed"] = seed
    return b


# ------------------------------------------------------------------ call (items 2, 3, 11)
def call(b):
    data = json.dumps(b).encode()
    err, last = None, {}
    for attempt in range(1, ATTEMPTS + 1):
        try:
            req = urllib.request.Request(URL, data=data, headers={
                "Content-Type": "application/json", "Authorization": "Bearer " + key(),
                "User-Agent": "rule2-raters", "X-Title": "rule2-raters"})
            with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
                j = json.loads(r.read().decode())
            last = {"returned_model": j.get("model"), "provider": j.get("provider"), "generation_id": j.get("id"),
                    "usage": j.get("usage")}
            res = j["choices"][0]["message"]["content"]
            m = re.search(r"\{.*\}", res, re.S)
            return json.loads(m.group(0)), dict(last, attempts=attempt, error=None)
        except urllib.error.HTTPError as e:
            err = f"HTTP {e.code}"
            try:
                err += ": " + scrub(e.read().decode(errors="replace"))[:300]
            except Exception:
                pass
        except Exception as e:
            err = scrub(f"{type(e).__name__}: {e}")[:300]
        time.sleep(10)
    return None, dict(last, attempts=ATTEMPTS, error=err)


def run(rater, ids, cb, red):
    model, slug, variant, rep, seed, *_ = RATERS[rater]
    done = {j["finding_id"] for j in R2.jsonl(ANS[rater]) if j.get("parsed")}
    todo = [f for f in ids if f not in done]
    say(f"{datetime.now().isoformat(timespec='seconds')} rater {rater} ({model} @ {slug}, variant {variant}, "
        f"replicate {rep}, seed {seed}): {len(todo)} to do, {len(done)} done")

    def work(fid):
        x = red[fid]
        raw, info = call(body(rater, cb, x))
        dec, flags = R2.decode(cb, variant, raw or {}, x["text"]) if raw else ({}, {})
        rec = {"finding_id": fid, "rater": rater, "model": model, "returned_model": info.get("returned_model"),
               "provider_requested": slug, "provider": info.get("provider"), "generation_id": info.get("generation_id"),
               "usage": info.get("usage"), "seed": seed, "variant": variant, "replicate": rep,
               "parsed": raw is not None and all(v is not None for v in dec.values()), "answers": dec, "flags": flags,
               "raw": raw, "attempts": info.get("attempts"), "error": info.get("error"),
               "time": datetime.now().isoformat(timespec="seconds")}
        R2.append(ANS[rater], rec)
        return rec

    out = []
    with ThreadPoolExecutor(WORKERS) as ex:
        for i, rec in enumerate(ex.map(work, todo), 1):
            u = rec["usage"] or {}
            say(f"  {rater} [{i}/{len(todo)}] {rec['finding_id']} status={'ok' if rec['error'] is None else 'FAILED'} "
                f"parsed={rec['parsed']} provider={rec['provider']} prompt_tokens={u.get('prompt_tokens')} "
                f"completion_tokens={u.get('completion_tokens')}" + (f" error={rec['error'][:120]}" if rec["error"] else ""))
            out.append(rec)
    ok = sum(r["parsed"] for r in out)
    say(f"rater {rater}: parsed {ok}, failed {len(out) - ok}")
    return out


# ------------------------------------------------------------------ modes
def dry_run():
    cb, red, groups, frz, h3 = load_texts()
    print(f"freeze check OK (protocol, codebook, rule2.py); prompt variant 3 sha256 {h3} = freeze.json")
    print(f"redacted.jsonl sha256 = freeze.json redacted_sha256; controlB_redacted_v2.jsonl LF sha256 = amendments.json entry 15")
    print("texts: " + ", ".join(f"{g} {len(v)}" for g, v in groups.items()) + f"; total {len(red)}")
    human = {r["finding_id"] for r in R2.human_pick()[0]}
    for rater, (model, slug, variant, rep, seed, pin, pout) in RATERS.items():
        bodies = [body(rater, cb, red[f]) for f in order(rater, red)]
        chars = [len(b["messages"][0]["content"]) + len(b["messages"][1]["content"]) for b in bodies]
        enc = [len(json.dumps(b).encode()) for b in bodies]
        ok_v = all(R2.render_user(cb, 3, red[f]["title"], red[f]["text"]) == b["messages"][1]["content"]
                   for f, b in zip(order(rater, red), bodies))
        skel = {k: v for k, v in bodies[0].items() if k != "messages"}
        tin = sum(chars) / 3.6 / 1e6
        print(f"\n{rater}: {len(bodies)} prompts built ({len(set(order(rater, red)))} distinct findings); variant-3 user prompts "
              f"identical to render_user: {ok_v}; system prompt = SYSTEM_PROMPT: "
              f"{all(b['messages'][0]['content'] == R2.SYSTEM_PROMPT for b in bodies)}")
        print(f"  request settings: {json.dumps(skel)}")
        print(f"  prompt characters: total {sum(chars):,}, median {sorted(chars)[len(chars)//2]:,}, max {max(chars):,}; "
              f"request body bytes max {max(enc):,}")
        print(f"  smoke-test findings (first {N_SMOKE} of the seeded order outside the human form): "
              f"{smoke_ids(rater, red)}; in human form: {sum(f in human for f in smoke_ids(rater, red))}")
        print(f"  cost estimate (~3.6 characters/token): input ~{tin:.2f}M tokens = USD {tin * pin:.2f}; output 1,000-3,000 tokens/call "
              f"= USD {363e3 / 1e6 * pout:.2f}-{1089e3 / 1e6 * pout:.2f}; upper bound USD {tin * pin + 363 * MAX_TOKENS / 1e6 * pout:.2f}")
    print(f"\nanswer files (not created by dry run): {[str(p.name) for p in ANS.values()]}; exist now: "
          f"{[p.exists() for p in ANS.values()]}; key file read: no; network calls: 0")


def smoke():
    cb, red, groups, *_ = load_texts()
    say(f"{datetime.now().isoformat(timespec='seconds')} smoke test (Amendment 02 item 10)")
    for rater in RATERS:
        run(rater, smoke_ids(rater, red), cb, red)
    passed = smoke_passed(red)
    say(f"smoke test passed for both raters: {passed}" + ("" if passed else " -> full run blocked; report before any change"))


def smoke_passed(red):
    return all(all(any(j["finding_id"] == f and j.get("parsed") for j in R2.jsonl(ANS[r])) for f in smoke_ids(r, red))
               for r in RATERS)


def full(raters):
    cb, red, *_ = load_texts()
    if not smoke_passed(red):
        sys.exit("Smoke test has not passed for both raters (Amendment 02 item 10); full run refused.")
    for rater in raters:
        run(rater, order(rater, red), cb, red)


def status():
    _, red, groups, *_ = load_texts()
    for rater in RATERS:
        recs = R2.jsonl(ANS[rater])
        for g, fs in groups.items():
            parsed = {j["finding_id"] for j in recs if j.get("parsed") and j["finding_id"] in fs}
            failed = sum(1 for j in recs if not j.get("parsed") and j["finding_id"] in fs)
            print(f"{rater} {g}: parsed {len(parsed)}/{len(fs)}, failed records {failed}, missing {len(fs) - len(parsed)}")


if __name__ == "__main__":
    a = sys.argv[1:]
    if a == ["--dry-run"]:
        dry_run()
    elif a == ["--smoke"]:
        smoke()
    elif a[:1] == ["--run"] and a[1:] and all(r in RATERS for r in a[1:]):
        full(a[1:])
    elif a == ["--status"]:
        status()
    else:
        sys.exit(__doc__)
