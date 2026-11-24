# Auditoría técnica · SPAIN 2035

## Hallazgos de revisión estática (24/11/2026)

- La versión multipágina tiene ocho vistas y compara cinco métodos de regresión.
- La regresión lineal con tendencias local y municipal presenta el menor MAE retrospectivo documentado (27,12 €/mes frente a 30,52 del Gradient Boosting). No equivale a una selección independiente para producción.
- El periodo 2023–2024 ya fue inspeccionado durante el desarrollo. La generalización debe comprobarse con observaciones posteriores no utilizadas en selección ni ajuste.
- Hay dos ZIP idénticos. Se conservan ambos provisionalmente porque el servidor HTTP anterior y su prueba necesitan el ZIP de la raíz, mientras que la multipágina lee el de datos/.
- Se elimina únicamente la copia idéntica del simulador que no utilizan los módulos principales; sigue accesible en Git.

## Protocolo de validación pendiente

1. Crear entorno limpio con Python y dependencias verificadas; registrar versiones reales.
2. Ejecutar notebook y aplicación de ocho vistas. Verificar compatibilidad del servidor HTTP anterior.
3. Comparar persistencia, regresiones lineales y Gradient Boosting mediante cortes temporales expansivos; usar las mismas filas por método.
4. Informar MAE, RMSE y R² por año y periodo, además del tamaño de muestra y cobertura. Para MAE, calcular brecha relativa como (MAE_validación − MAE_entrenamiento) / MAE_entrenamiento, si el denominador es positivo. Para R², informar diferencia en puntos porcentuales y no confundirla con brecha relativa de MAE.
5. Aspirar a una brecha relativa de MAE inferior al 5 %, sin ajustar sobre el conjunto final para alcanzar artificialmente ese objetivo. Reportar cualquier incumplimiento.
6. Evaluar un periodo posterior independiente cuando existan datos observados; distinguir predicción a un año de escenarios compuestos hasta 2035.

Esta revisión no ejecutó el entrenamiento ni verificó el despliegue. No acredita nuevas métricas ni ausencia de sobreajuste.
