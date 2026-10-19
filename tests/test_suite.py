"""
============================================================================
Proyecto: ContentCreator-Tools — Suite de Pruebas Unitarias e Integración
Autor: Rogerr Carvajal <rogerrcarvajal@gmail.com>
Rol: Lead AI Engineer & Intelligent Agent Architect
Stack: Python 3.11+ | Pytest | Pydantic v2 | Autonomous Agents
============================================================================
"""

from __future__ import annotations

import asyncio
import importlib.util
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent


def load_module_from_path(module_name: str, file_path: Path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_rf2_folder_structure_and_brand_headers() -> None:
    """Verifica RF2 (carpetas individuales por herramienta) y firma de marca personal."""
    required_files = [
        ROOT_DIR / "index.html",
        ROOT_DIR / "README.md",
        ROOT_DIR / "assets" / "css" / "brand-quantum.css",
        ROOT_DIR / "01-editor-video-automatico" / "index.html",
        ROOT_DIR / "01-editor-video-automatico" / "dashboard_argon.html",
        ROOT_DIR / "01-editor-video-automatico" / "motor_edicion_local.py",
        ROOT_DIR / "02-motion-graphics-lower-thirds" / "index.html",
        ROOT_DIR / "03-sintetizador-musica-sfx" / "index.html",
        ROOT_DIR / "04-extractor-shorts-virales" / "index.html",
        ROOT_DIR / "04-extractor-shorts-virales" / "extractor_shorts.py",
    ]
    for fpath in required_files:
        assert fpath.exists(), f"Falta archivo requerido: {fpath}"
        content = fpath.read_text(encoding="utf-8")
        assert "Rogerr Carvajal" in content, f"Falta firma de autoría en {fpath}"


def test_rf3_hub_links_to_all_tools() -> None:
    """Verifica RF3: El website principal contiene los enlaces a las 4 herramientas."""
    hub_html = (ROOT_DIR / "index.html").read_text(encoding="utf-8")
    expected_links = [
        "01-editor-video-automatico/index.html",
        "02-motion-graphics-lower-thirds/index.html",
        "03-sintetizador-musica-sfx/index.html",
        "04-extractor-shorts-virales/index.html",
    ]
    for link in expected_links:
        assert link in hub_html, f"El Hub principal no enlaza a {link}"


def test_tool01_nle_python_engine(tmp_path: Path) -> None:
    """Verifica el motor Python con Pydantic v2 de la Herramienta 01."""
    mod_path = ROOT_DIR / "01-editor-video-automatico" / "motor_edicion_local.py"
    nle_mod = load_module_from_path("motor_edicion_local", mod_path)

    clips = asyncio.run(nle_mod.detect_non_silent_segments(tmp_path / "nonexistent.mp4"))
    assert len(clips) == 3
    config = nle_mod.NLEProjectConfig(clips=clips)
    assert config.target_fps == 60

    out_manifest = tmp_path / "manifest.json"
    nle_mod.export_project_manifest(config, out_manifest)
    assert out_manifest.exists()


def test_tool04_viral_shorts_extractor_pipeline(tmp_path: Path) -> None:
    """Verifica los 5 pasos del Extractor de Shorts Virales (Whisper + LLM + FFmpeg + ASS)."""
    mod_path = ROOT_DIR / "04-extractor-shorts-virales" / "extractor_shorts.py"
    shorts_mod = load_module_from_path("extractor_shorts", mod_path)

    report = asyncio.run(
        shorts_mod.run_shorts_extraction_pipeline(
            source_video=tmp_path / "podcast_full.mp4",
            output_dir=tmp_path / "out_shorts",
            execute_ffmpeg=False,
        )
    )
    assert report.resolution == "1080x1920"
    assert len(report.candidates) == 3
    for cand in report.candidates:
        assert cand.duration_sec == 40.0
        ass_file = tmp_path / "out_shorts" / f"short_0{cand.rank}_subtitles.ass"
        assert ass_file.exists()
        ass_text = ass_file.read_text(encoding="utf-8")
        # Verifica resolución 1080x1920 y color amarillo activo (&H0015CCFA&)
        assert "PlayResX: 1080" in ass_text
        assert "PlayResY: 1920" in ass_text
        assert "&H0015CCFA&" in ass_text
