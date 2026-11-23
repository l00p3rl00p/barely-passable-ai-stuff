"""Independent receive/map/emit connector. Standard library only."""
import argparse, json, os, subprocess, sys, urllib.request, urllib.parse
from pathlib import Path

def dumps(value):
    return json.dumps(value, ensure_ascii=False, allow_nan=False, separators=(",", ":"))

def http(url, payload=None, token_env=None, ndjson=False):
    headers = {"Accept":"application/json"}
    if token_env:
        headers["Authorization"] = "Bearer " + os.environ[token_env]
    data = None
    if payload is not None:
        headers["Content-Type"] = "application/x-ndjson" if ndjson else "application/json"
        data = payload.encode() if ndjson else dumps(payload).encode()
    with urllib.request.urlopen(urllib.request.Request(url, data=data, headers=headers), timeout=120) as res:
        result = json.load(res)
    if not isinstance(result, dict) or result.get("error") or result.get("isError") or result.get("ok") is False:
        raise RuntimeError("Destination rejected emission: " + dumps(result))
    return result

def emit(config, batch):
    """Transport only. Mapping is supplied by caller/configured profile."""
    kind = config["transport"]
    if kind == "http":
        return http(config["url"], batch, config.get("token_env"), config.get("ndjson",False))
    if kind == "command":
        run = subprocess.run(config["argv"], input=dumps(batch), text=True, capture_output=True, check=True)
        result = json.loads(run.stdout)
        if result.get("ok") is not True:
            raise RuntimeError("Native command did not confirm emission")
        return result
    if kind in ("json","jsonl"):
        path = Path(config["path"])
        # Exclusive creation: never silently truncate an existing emission.
        with path.open("x",encoding="utf-8") as out:
            if kind=="json": out.write(dumps(batch)+"\n")
            else:
                for row in batch: out.write(dumps(row)+"\n")
        return {"ok":True,"path":str(path)}
    raise ValueError("Unsupported transport: "+kind)

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", required=True)
    parser.add_argument("--input", default="-")
    args=parser.parse_args()
    config=json.loads(Path(args.config).read_text())
    batch=json.load(sys.stdin) if args.input=="-" else json.loads(Path(args.input).read_text())
    from profiles import map_and_emit
    results=[]
    for sink in config["outputs"]:
        try: results.append({"name":sink["name"],"ok":True,"receipt":map_and_emit(sink,batch)})
        except Exception as exc: results.append({"name":sink["name"],"ok":False,"error":str(exc)})
    print(dumps(results))
    return 0 if all(r["ok"] for r in results) else 1

if __name__=="__main__":
    sys.exit(main())
