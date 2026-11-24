import unittest
from pathlib import Path
import numpy as np
import pandas as pd
from modelo import preparar, VARIABLES
from validar_modelo import particiones, medir, ejecutar

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "datos" / "Atlas_Malaga_datos.zip"

class TestValidacion(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d = preparar(DATA).dropna(subset=["real"])

    def test_identificadores_unicos(self):
        self.assertFalse(self.d.duplicated(["zona", "anio"]).any())
        self.assertTrue(np.isfinite(self.d[VARIABLES + ["real"]]).all().all())

    def test_cortes_sin_fuga_temporal(self):
        for year, train, val in particiones(self.d[self.d.anio <= 2022]):
            self.assertLess(train.anio.max(), val.anio.min())
            self.assertEqual(val.anio.min(), year)

    def test_metricas_perfectas(self):
        result = medir([1, 2, 3], [1, 2, 3])
        self.assertEqual(result["MAE"], 0)
        self.assertEqual(result["RMSE"], 0)
        self.assertEqual(result["R2"], 1)

    def test_auditoria_completa(self):
        report = ejecutar(DATA)
        rows = report["metricas"]
        self.assertEqual(len(rows), 9)
        self.assertEqual(len({r["retrospectiva"]["n"] for r in rows}), 1)
        self.assertTrue(all(np.isfinite(r["retrospectiva"]["MAE"]) for r in rows))

if __name__ == "__main__":
    unittest.main()
