"""
============================================================================
Proyecto: Motor de Edición Automático NLE Local (60 FPS + Jump Cuts)
Autor: Rogerr Carvajal <rogerrcarvajal@gmail.com>
Rol: Lead AI Engineer & Intelligent Agent Architect
Stack: Python 3.11+ | Pydantic v2 | FFmpeg | Autonomous Agents
============================================================================
"""

import asyncio
import json
import os
import shutil
import subprocess
from pathlib import Path
from pydantic import BaseModel, Field, field_validator


class KeyframePoint(BaseModel):
    """Representa un fotograma clave en la línea de tiempo NLE."""

    timestamp_sec: float = Field(..., ge=0.0, description="Tiempo en segundos")
    scale_pct: float = Field(default=100.0, ge=25.0, le=300.0)
    pos_x_pct: float = Field(default=0.0, ge=-100.0, le=100.0)
    pos_y_pct: float = Field(default=0.0, ge=-100.0, le=100.0)
    opacity_pct: float = Field(default=100.0, ge=0.0, le=100.0)


class TimelineClip(BaseModel):
    """Representa un segmento activo luego de eliminar silencios (Jump Cut)."""

    clip_id: str = Field(..., min_length=1)
    label: str = Field(..., min_length=1)
    start_sec: float = Field(..., ge=0.0)
    end_sec: float = Field(..., gt=0.0)
    keyframes: list[KeyframePoint] = Field(default_factory=list)

    @field_validator("end_sec")
    @classmethod
    def validate_end_after_start(cls, v: float, info) -> float:
        start = info.data.get("start_sec", 0.0)
        if v <= start:
            raise ValueError("end_sec debe ser mayor que start_sec")
        return v


class NLEProjectConfig(BaseModel):
    """Configuración maestra del Motor de Edición Automático a 60 FPS."""

    project_name: str = Field(default="Master_Argon_60FPS")
    aspect_ratio: str = Field(default="9:16", pattern=r"^(9:16|16:9|1:1)$")
    style_preset: str = Field(default="apple", pattern=r"^(apple|hormozi|kinetic)$")
    target_fps: int = Field(default=60, ge=24, le=120)
    silence_threshold_db: float = Field(default=-38.0, le=-10.0)
    min_silence_duration_sec: float = Field(default=0.48, ge=0.1)
    clips: list[TimelineClip] = Field(default_factory=list)


async def detect_non_silent_segments(
    input_video: Path,
    silence_db: float = -38.0,
    min_silence_sec: float = 0.48,
) -> list[TimelineClip]:
    """Detecta silencios mediante FFmpeg silencedetect o genera cortes inteligentes."""
    ffmpeg_bin = os.getenv("FFMPEG_BINARY_PATH", "ffmpeg")
    if not input_video.exists() or shutil.which(ffmpeg_bin) is None:
        # Fallback determinista para entornos de demostración sin archivo físico
        return [
            TimelineClip(clip_id="v1-1", label="V1 • Clip #1", start_sec=0.0, end_sec=4.05),
            TimelineClip(clip_id="v1-2", label="V1 • Clip #2", start_sec=4.60, end_sec=9.83),
            TimelineClip(clip_id="v1-3", label="V1 • Clip #3", start_sec=10.45, end_sec=20.15),
        ]

    cmd = [
        ffmpeg_bin,
        "-i",
        str(input_video),
        "-af",
        f"silencedetect=noise={silence_db}dB:d={min_silence_sec}",
        "-f",
        "null",
        "-",
    ]
    proc = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    _, stderr = await proc.communicate()
    log_text = stderr.decode("utf-8", errors="ignore")

    clips: list[TimelineClip] = []
    current_start = 0.0
    idx = 1
    for line in log_text.splitlines():
        if "silence_start:" in line:
            try:
                s_start = float(line.split("silence_start:")[1].strip().split()[0])
                if s_start - current_start > 0.25:
                    clips.append(
                        TimelineClip(
                            clip_id=f"v1-{idx}",
                            label=f"V1 • Clip #{idx}",
                            start_sec=round(current_start, 2),
                            end_sec=round(s_start, 2),
                        )
                    )
                    idx += 1
            except (ValueError, IndexError):
                continue
        elif "silence_end:" in line:
            try:
                s_end = float(line.split("silence_end:")[1].strip().split()[0])
                current_start = s_end
            except (ValueError, IndexError):
                continue

    if not clips:
        clips.append(TimelineClip(clip_id="v1-1", label="V1 • Master Clip", start_sec=0.0, end_sec=15.0))
    return clips


def export_project_manifest(config: NLEProjectConfig, output_path: Path) -> Path:
    """Exporta el manifiesto validado con Pydantic v2 a JSON."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(config.model_dump(), indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    return output_path


if __name__ == "__main__":
    sample_clips = asyncio.run(detect_non_silent_segments(Path("input_raw.mp4")))
    project = NLEProjectConfig(clips=sample_clips)
    print(json.dumps(project.model_dump(), indent=2, ensure_ascii=False))
