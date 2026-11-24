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

La auditoría automatizada ejecutó el entrenamiento y las pruebas de validación. No verificó el despliegue ni acredita ausencia de sobreajuste.

## Resultados reproducidos · 24/11/2026

[GitHub Actions: ejecución correcta y artefacto de métricas](https://github.com/EddySantanaBootcamp3/SPAIN-2035-Malaga/actions/runs/45363015965). Entrenamiento: 3.549 filas; evaluación retrospectiva 2023–2024: 786 filas.

| Modelo | MAE train | MAE retrospectivo | R² retrospectivo | Brecha MAE |
|---|---:|---:|---:|---:|
| Persistencia | 28,50 | 47,67 | 0,8601 | 67,25 % |
| Lineal completa | 22,98 | 27,12 | 0,9375 | 18,02 % |
| Ridge 10 | 22,97 | 27,28 | 0,9368 | 18,76 % |
| Gradient Boosting | 21,37 | 30,52 | 0,9244 | 42,78 % |

La brecha de R² de la lineal completa es 0,30 puntos porcentuales; la brecha relativa de MAE es 18,02 %. No se alcanza el objetivo de 5 % en MAE. Ridge 10 gana entre candidatos lineales por CV ponderada (29,09 €/mes), pero no mejora la lineal completa en la evaluación retrospectiva. No comparar directamente ese ranking con el MAE CV no ponderado del ensemble. Se mantiene el modelo del simulador para no alterar su comportamiento; cualquier sustitución requiere validación prospectiva y pruebas del dashboard.
