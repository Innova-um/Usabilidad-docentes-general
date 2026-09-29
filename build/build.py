import pandas as pd, json, os, sys, re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
# Tablero de un solo informe: "Usabilidad Docentes.xlsx" (todas las modalidades, un periodo)
SRC = next((a for a in sys.argv[1:] if not a.startswith("--")), os.path.join(ROOT, "Usabilidad Docentes.xlsx"))
# Periodo del informe: (etiqueta, fecha inicial, fecha final)
PERIODO = ("1 ago – 28 sep", "2026-08-01", "2026-09-28")

d = pd.read_excel(SRC)
label, ini, fin = PERIODO
ini, fin = pd.Timestamp(ini), pd.Timestamp(fin)
fin_exclusivo = fin + pd.Timedelta(days=1)
ult = pd.to_datetime(d.ultima_accion_periodo.replace("Sin actividad", None).dropna()).max()
parcial = pd.notna(ult) and ult < fin_exclusivo - pd.Timedelta(hours=1)
primera = pd.to_datetime(d.ultima_accion_periodo.replace("Sin actividad", None).dropna()).min()
if ult >= fin_exclusivo or primera < ini:
    print(f"AVISO: el Excel tiene actividad entre {primera:%d/%m/%Y} y {ult:%d/%m/%Y}, fuera de PERIODO. Revisa las fechas.")
dias = round((ult - ini).total_seconds() / 86400, 2) if parcial else (fin_exclusivo - ini).days
meta = [{"label": label, "days": dias,
         "note": f"corte {ult.strftime('%d/%m %H:%M')}" if parcial else "semana completa" if dias == 7 else "periodo completo"}]

# Nombres de facultad escritos distinto según la modalidad
ALIAS = {"facultad de ingenieria": "Facultad de Ingeniería", "otros": "Otros"}
MODS = {"PREGRADO PRESENCIAL": "Pregrado presencial", "DISTANCIA": "Distancia", "POSGRADO": "Posgrado"}

def split(h):
    parts = [p.strip() for p in str(h).split(" > ")]
    mod = MODS.get(parts[0], parts[0].capitalize())
    fac = ALIAS.get(parts[1].lower(), parts[1]) if len(parts) > 1 else "Sin facultad"
    prog = " > ".join(parts[2:]) if len(parts) > 2 else "(Cursos directos de la facultad)"
    return mod, fac, prog

def n(v):
    return int(v) if pd.notna(v) else 0

cats, cat_idx, courses, course_idx, teachers, teacher_idx, rows = [], {}, [], {}, [], {}, []
TIPOS = ("contenidos_creados_periodo", "tareas_creadas_periodo", "cuestionarios_creados_periodo", "foros_creados_periodo")
for _, r in d.iterrows():
    k = split(r["categorias_jerarquia"])
    if k not in cat_idx:
        cat_idx[k] = len(cats); cats.append(list(k))
    cid, uid = r["course_id"], r["userid"]
    if cid not in course_idx:
        course_idx[cid] = len(courses)
        courses.append([str(r["course_shortname"]).strip(), str(r["course_name"]).strip(), cat_idx[k],
                        [n(r[t]) for t in TIPOS]])
    if uid not in teacher_idx:
        teacher_idx[uid] = len(teachers)
        teachers.append([str(r["nombre_profesor"]).strip(), str(r["profesor"]).strip()])
    rows.append([teacher_idx[uid], course_idx[cid], [n(r["tiempo_dedicado_minutos"])], [n(r["acciones_edicion_periodo"])]])

data = {"p": meta, "cats": cats, "courses": courses, "teachers": teachers, "rows": rows}
tpl = open(os.path.join(HERE, "template.html"), encoding="utf-8").read()
js = re.sub("�+", "Ñ", json.dumps(data, ensure_ascii=False, separators=(",", ":")))
out = tpl.replace("/*__DATA__*/null", js)
if "--fragment" not in sys.argv:
    out = ('<!doctype html>\n<html lang="es">\n<head>\n<meta charset="utf-8">\n'
           '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
           '<meta name="robots" content="noindex, nofollow">\n'
           + out.replace("</style>\n", "</style>\n</head>\n<body>\n", 1) + "\n</body>\n</html>\n")
dest = next((a.split("=", 1)[1] for a in sys.argv if a.startswith("--out=")), os.path.join(ROOT, "index.html"))
open(dest, "w", encoding="utf-8").write(out)
print("ok", len(rows), len(courses), len(teachers), len(cats), meta, len(out), dest)
