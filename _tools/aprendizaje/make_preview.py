"""Generates converted/learning.html: local preview of the candidate scenes with learning value.

Four tabs: high (catalogo.csv, first round), medium (catalogo_medium.csv, second round), high-low
(catalogo_highlow.csv: high total score and little original code) and low (the rest of the rendered scenes). It also uses the classification of pi dialogues (../pi_dialogo/clasificacion.json). The page is local because the videos are on disk:
open it with the browser from converted/. Usage: python make_preview.py"""
import csv
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE.parent))
sys.argv = sys.argv[:1]
import pipeline as P


def rel(path):
    try:
        return str(Path(path).relative_to(ROOT)) if path else ""
    except ValueError:
        return ""


def split(value):
    return [v.strip() for v in (value or "").split(";") if v.strip()]


pi_path = HERE.parent / "pi_dialogo" / "clasificacion.json"
pi = {(e["fuente"], e["escena"]): e for e in json.load(open(pi_path))} if pi_path.exists() else {}


def link(fuente, escena, meta=None):
    meta = meta or P.load_meta(P.META / Path(fuente).with_suffix("") / f"{escena}.json")
    cat = P.category(meta)
    folder = P.CATEGORY_DIRS.get(cat)
    video = (meta.get("render") or {}).get("video") or ""
    if video and not Path(video).exists():  # no published video (e.g. PascalColored)
        video = ""
    return {
        "cat": cat, "video": rel(video), "thumb": rel(video.rsplit(".", 1)[0] + ".jpg") if video else "",
        "file": f"{folder}/{P.display_dir(Path(fuente))}/{escena}.py" if folder else "",
    }


def full_items(csv_name, cands_name):
    """Scenes of a tier: what an agent described (catalogo*.csv) and, if missing, the automatic score's"""
    cands = {(c["fuente"], c["escena"]): c for c in json.load(open(HERE / cands_name))}
    described = {}
    if (HERE / csv_name).exists():
        for row in csv.DictReader(open(HERE / csv_name, encoding="utf-8")):
            described[(row["fuente"], row["escena"])] = row
    out = []
    for key, c in cands.items():
        row = described.get(key)
        if row is None:  # not described yet
            out.append({"escena": c["escena"], "fuente": c["fuente"], "año": c["año"], "tema": [], "tipo": [],
                        "desc": "Pendiente de describir.", "tecnica": "", "nivel": "", "valor": "",
                        "motivo": "", "variantes": c["variantes"], "puntaje": c["puntaje"],
                        "tags": c["tecnicas_propias"], "pi": key in pi, **link(c["fuente"], c["escena"])})
            continue
        out.append({
            "escena": row["escena"], "fuente": row["fuente"], "año": row["año"],
            "tema": split(row["tema"]), "tipo": split(row["tipo_visual"]),
            "desc": row["descripcion"], "tecnica": row["tecnica_destacada"], "nivel": row["nivel"],
            "valor": row["valor"], "motivo": row["motivo_valor"], "variantes": split(row["variantes"]),
            "puntaje": float(row["puntaje"] or 0), "tags": c.get("tecnicas_propias", []), "pi": key in pi,
            **link(row["fuente"], row["escena"]),
        })
    return out


high = full_items("catalogo.csv", "candidatos.json")
# Variants of high scenes found by the finer grouping of the second round
extra_path = HERE / "variantes_extra_high.json"
extra = json.load(open(extra_path)) if extra_path.exists() else {}
for d in high:
    more = extra.get(f"{d['fuente']}::{d['escena']}", [])
    d["variantes"] = sorted(set(d["variantes"]) | set(more))
medium = full_items("catalogo_medium.csv", "candidatos_medium.json")
highlow = full_items("catalogo_highlow.csv", "candidatos_highlow.json")
# Low: all the other rendered scenes, except the variants already represented by a scene of another tier
taken = set()
for d in high + medium + highlow:
    taken.add((d["fuente"], d["escena"]))
    taken.update((d["fuente"], v) for v in d["variantes"])
# Pi sections: the classification of pi creature dialogues (../pi_dialogo). Pi-High repeats those that are
# also in another tier, marking it; Pi-Low comes from Low
tier_of = {}
for name, tier in (("High", high), ("Medium", medium), ("High-Low", highlow)):
    for d in tier:
        tier_of[(d["fuente"], d["escena"])] = name
        for v in d["variantes"]:
            tier_of.setdefault((d["fuente"], v), name)
scores = {(r["fuente"], r["escena"]): r["puntaje"] for r in json.load(open(HERE / "puntajes.json"))}
pi_high, pi_low = [], []
for key, e in pi.items():
    item = {"escena": e["escena"], "fuente": e["fuente"], "año": e["año"], "desc": e["motivo"],
            "confianza": e.get("confianza", ""), "en": tier_of.get(key, "solo pi"),
            "puntaje": scores.get(key, 0), **link(e["fuente"], e["escena"])}
    (pi_high if e["pi_dialogo"] == "posible_util" else pi_low).append(item)
pi_high.sort(key=lambda d: -d["puntaje"])
pi_low.sort(key=lambda d: (d["fuente"], d["escena"]))

low = []
for r in json.load(open(HERE / "puntajes.json")):
    key = (r["fuente"], r["escena"])
    if key in taken or pi.get(key, {}).get("pi_dialogo") == "descartada":
        continue
    low.append({"escena": r["escena"], "fuente": r["fuente"], "año": r["año"], "puntaje": r["puntaje"],
                "pi": pi.get(key, {}).get("pi_dialogo", ""), "estatica": r["estatica"],
                **link(r["fuente"], r["escena"])})
low.sort(key=lambda d: -d["puntaje"])

html = (HERE / "preview_template.html").read_text(encoding="utf-8")
data = {"high": high, "medium": medium, "highlow": highlow, "low": low, "pihigh": pi_high, "pilow": pi_low}
html = html.replace("/*__DATA__*/{}", json.dumps(data, ensure_ascii=False, separators=(",", ":")))
(ROOT / "learning.html").write_text(html, encoding="utf-8")
print(f"high {len(high)} · medium {len(medium)} · high-low {len(highlow)} · low {len(low)} · "
      f"pi-high {len(pi_high)} · pi-low {len(pi_low)} -> {ROOT / 'learning.html'}")
