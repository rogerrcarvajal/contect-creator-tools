# 📱 04 — Extractor Automático de Shorts Virales (Python + Whisper + LLM + FFmpeg)

> **Desarrollador Líder:** Rogerr Carvajal ([@rogerrcarvajal](https://github.com/rogerrcarvajal))  
> **Especialidad:** Arquitectura de Software con Modelos y Agentes Inteligentes  

---

## 1. Resumen Técnico

Implementación dual (Pipeline CLI en **Python 3.11+ con Pydantic v2** + **Estudio Web Interactivo 1080x1920**) del **Prompt Maestro 3️⃣ (Extractor de Shorts Virales)**:

1. **Extracción de Audio y Transcripción con Whisper**: Obtención de marcas de tiempo palabra por palabra (`word_timestamps=True`).
2. **Análisis con LLM (Controversia & Valor)**: Selección de los **3 fragmentos exactos de 40 segundos** con mayor potencial de retención viral.
3. **Reencuadre Vertical 9:16 con FFmpeg**: Filtro `crop=ih*9/16:ih,scale=1080:1920,fps=60`.
4. **Subtítulos Gruesos al Centro con Palabra Activa en Amarillo**: Generador automático de subtítulos `.ASS` (Advanced SubStation Alpha) y motor Canvas que ilumina en amarillo (`#FACC15`) la palabra actual.
5. **Renderizado de los 3 Videos Independientes**: Exportación de `short_01_viral_1080x1920.mp4`, `short_02_viral_1080x1920.mp4` y `short_03_viral_1080x1920.mp4`.

---

## 2. Uso por Consola (Python 3.11+)

```bash
python extractor_shorts.py --input podcast_full.mp4 --output-dir output_shorts --render
```
