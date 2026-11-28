# Video Explainer on Windows

The upstream skill assumes bash, `ffmpeg` on PATH and a POSIX venv. This copy runs on
Windows with four local adjustments.

## Toolchain

- Python 3.15 at `python` (system).
- Node 22 at `C:\Users\Visitor\AppData\Local\Programs\nodejs\npx.cmd`.
- FFmpeg 9.1 in `C:\Users\Visitor\AppData\Local\Temp\opencode\ffmpeg\ffmpeg-9.1-essentials_build\bin`.
  Add that folder to `PATH` before any script call; `ffprobe` lives next to `ffmpeg`.
- Python packages (`numpy`, `edge-tts`, `mutagen`) in
  `C:\Users\Visitor\.cache\video-explainer\venv-win`. There is no `py` launcher: call
  `Scripts\python.exe` from that venv and set `PYTHONPATH` to this `scripts` folder.

## Local patch

`scripts/common.py` (`hf_cmd`) uses `hyperframes.cmd` from the npx cache on Windows and
falls back to `shutil.which("npx")`. Upstream looked only for the POSIX `hyperframes`
launcher, which Windows cannot execute.

## Russian voice

Kokoro has no Russian voice. The preferred speaker is the male Edge voice, which handles
Russian stress better than the offline Piper models:

```
Voice: edge:ru-RU-DmitryNeural
```

`narrate.py` synthesizes each scene, retries the public endpoint, trims and pads the audio,
aligns it with Parakeet v3 and then replaces the ASR spellings with the exact narration
text, so captions keep the right case endings. `edge-tts` is installed in `venv-win`; add it
with `pip install edge-tts` on a fresh machine.

If Edge TTS refuses a request for a long time, the offline fallback is
`piper:ru_RU-ruslan-medium`; its stress is worse (`тЕсты`, `критЕрии`), so use it only when
the cloud voice is unavailable. The Piper binary and voice live in
`C:\Users\Visitor\.cache\video-explainer\piper`:

```powershell
curl.exe -L -o piper.zip https://github.com/rhasspy/piper/releases/download/2023.11.14-2/piper_windows_amd64.zip
Expand-Archive piper.zip -DestinationPath .
curl.exe -L -o ru_RU-ruslan-medium.onnx https://huggingface.co/rhasspy/piper-voices/resolve/main/ru/ru_RU/ruslan/medium/ru_RU-ruslan-medium.onnx
curl.exe -L -o ru_RU-ruslan-medium.onnx.json https://huggingface.co/rhasspy/piper-voices/resolve/main/ru/ru_RU/ruslan/medium/ru_RU-ruslan-medium.onnx.json
```

## Commands

```powershell
$bin = "C:\Users\Visitor\AppData\Local\Temp\opencode\ffmpeg\ffmpeg-9.1-essentials_build\bin"
$env:PATH = "$bin;$env:PATH"
$env:PYTHONUTF8 = "1"
$env:PYTHONPATH = "C:\Belousov\Projects\mdk\.opencode\skills\video-explainer\scripts"
$py = "C:\Users\Visitor\.cache\video-explainer\venv-win\Scripts\python.exe"

& $py "...\scripts\narrate.py"  <project>
& $py "...\scripts\render.py"   <project> --preview
& $py "...\scripts\render.py"   <project> --draft
& $py "...\scripts\qa.py"       <project>
& $py "...\scripts\render.py"   <project>
```

Project sources for the test live in `courses/2/МДК.02.01/media/lek-01/`; the site-ready
720p file is `courses/2/МДК.02.01/media/lek-01.mp4`.
