"""Auditoría reproducible, sin Streamlit. Ejecutar desde la raíz."""
import argparse
from pathlib import Path
import json
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from modelo import preparar, entrenar, predecir, VARIABLES

ROOT = Path(__file__).resolve().parent
def medir(y, p):
    return {"n": len(y), "MAE": float(mean_absolute_error(y,p)),
            "RMSE": float(np.sqrt(mean_squared_error(y,p))),
            "R2": float(r2_score(y,p))}

def particiones(d):
    for year in range(2018, 2023):
        train, val = d[d.anio < year], d[d.anio == year]
        if train.empty or val.empty:
            raise ValueError(f"Corte temporal vacío: {year}")
        yield year, train, val

def candidatos():
    return {"persistencia": (None, ["anterior"]),
            "lineal_previo": (LinearRegression(), ["anterior"]),
            "lineal_local": (LinearRegression(), VARIABLES[:2]),
            "lineal_completa": (LinearRegression(), VARIABLES),
            **{f"ridge_{a}": (make_pipeline(StandardScaler(), Ridge(alpha=a)), VARIABLES)
               for a in (0.1, 1, 10, 100)}}

def ajuste_pred(model, cols, train, sample):
    if model is None:
        return sample.anterior.to_numpy()
    return model.fit(train[cols], train.real).predict(sample[cols])

def ejecutar(archivo):
    d = preparar(archivo).dropna(subset=["real"])
    train = d[d.anio <= 2022]
    val = d[d.anio.between(2023, 2024)]
    if train.empty or val.empty:
        raise ValueError("Faltan datos de entrenamiento o evaluación")
    folds = []
    for year, t, v in particiones(train):
        for name, (m, cols) in candidatos().items():
            folds.append(dict(modelo=name, anio=year, **medir(v.real, ajuste_pred(m, cols, t, v))))
    cv = pd.DataFrame(folds)
    ranking = ((cv.MAE * cv.n).groupby(cv.modelo).sum() / cv.groupby("modelo").n.sum()).sort_values()
    rows = []
    _, gb, _ = entrenar(archivo)
    for name, (m, cols) in {**candidatos(), "gradient_boosting": (None, VARIABLES)}.items():
        if name == "gradient_boosting":
            p = lambda s: predecir(gb, s)
        elif m is None:
            p = lambda s: s.anterior.to_numpy()
        else:
            m.fit(train[cols], train.real)
            p = lambda s: m.predict(s[cols])
        tr = medir(train.real, p(train))
        va = medir(val.real, p(val))
        gap = 100 * (va["MAE"] - tr["MAE"]) / tr["MAE"] if tr["MAE"] > 0 else None
        rows.append({"modelo":name, "train":tr, "retrospectiva":va,
                     "brecha_MAE_pct":gap, "brecha_R2_pp":100*(tr["R2"]-va["R2"]),
                     "por_anio":{str(y):medir(s.real,p(s)) for y,s in val.groupby("anio")}})
    return {"aviso":"2023–2024 retrospectivo; no es test independiente nuevo",
            "seleccion_lineal_o_ridge_por_cv": ranking.index[0],
            "ranking_cv_mae":ranking.to_dict(), "gb_cv_mae_no_ponderado":float(-gb.best_score_),
            "cortes":folds, "metricas":rows}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--datos", type=Path, default=ROOT/"datos"/"Atlas_Malaga_datos.zip")
    parser.add_argument("--salida", type=Path, default=ROOT/"resultados"/"validacion.json")
    args = parser.parse_args()
    result = ejecutar(args.datos)
    args.salida.parent.mkdir(parents=True, exist_ok=True)
    args.salida.write_text(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False), encoding="utf-8")
    print(f"Informe guardado en {args.salida}")
