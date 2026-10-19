# 🎹 03 — Sintetizador Procedural de Música & SFX (Web Audio API)

> **Desarrollador Líder:** Rogerr Carvajal ([@rogerrcarvajal](https://github.com/rogerrcarvajal))  
> **Especialidad:** Arquitectura de Software con Modelos y Agentes Inteligentes  

---

## 1. Resumen Técnico

Implementación completa del **Prompt Maestro 2️⃣ (Sintetizador de Música & SFX)** empleando síntesis digital en tiempo real con **Web Audio API**:

1. **Sección 1 — Pistas Musicales Procedurales (Libres de Copyright)**:
   - Géneros: **Lo-Fi Chill Study Beats**, **Synthwave Retro 80s**, **Cyberpunk Industrial Bass** y **Ambient Cinematic Drone**.
   - Mezclador independiente de 4 canales (Batería, Bajo, Acordes, Melodía/Arpegio), control de Tempo (BPM) y filtro analógico Low-Pass.
   - Regeneración infinita mediante semillas procedurales deterministas.
2. **Sección 2 — Botonera SFX Sintetizados al Vuelo**:
   - 8 pads de efectos para edición de video con atajos de teclado (`[1]` a `[8]`): **Whoosh**, **Cinematic Impact**, **Riser Tensional**, **UI Clicks**, **Sub Drop 808**, **Cyber Glitch**, **Retention Bell** y **Laser Transition**.
3. **Sección 3 — Visualizador Reactivo en Canvas (60 FPS)**:
   - Conectado a `AnalyserNode` con modos de Espectro de Barras Neón, Osciloscopio de Onda y Pulso Radial.
4. **Sección 4 — Grabación y Exportación MP4 / WAV**:
   - Exportación directa tanto a `.MP4` (Video Canvas + Audio sincronizado) como a `.WAV` (Audio PCM de 16 bits sin compresión mediante `OfflineAudioContext`).
