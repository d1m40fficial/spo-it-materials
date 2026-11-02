#!/usr/bin/env python3
"""SVG Feedback Loop: mandatory render-view-fix cycle.

Commands:
  python svg_loop.py render <svg_file>
      Renders the SVG to a PNG preview and records the iteration.
      You MUST view the PNG after this, then fix and render again.

  python svg_loop.py finish <svg_file> [output_name.svg]
      Finalises the SVG. Refuses when nothing was rendered.

  python svg_loop.py status
      Shows the current iteration count and history.

  python svg_loop.py reset
      Clears the iteration history for a fresh start.

Rendering uses CairoSVG when it is installed, otherwise headless Chromium
through Playwright. Both paths write the same PNG preview.
"""

import json
import os
import shutil
import sys
from pathlib import Path

WORK = Path(os.environ.get("SVG_LOOP_DIR") or (Path(os.environ.get("TEMP", "/tmp")) / "svg_loop"))
STATE_FILE = WORK / ".svg_loop_state.json"
PREVIEW_PNG = WORK / "svg_preview.png"
OUTPUT_DIR = Path(os.environ.get("SVG_LOOP_OUT") or (WORK / "outputs"))


def ensure_cairosvg():
    """Return the cairosvg module, or None when it cannot be used here."""
    import importlib.util

    try:
        import cairosvg
        return cairosvg
    except Exception:
        pass
    if importlib.util.find_spec("cairosvg") is not None:
        # Installed but the native cairo library is missing: do not reinstall.
        return None
    try:
        os.system(f'"{sys.executable}" -m pip install cairosvg -q')
        import cairosvg
        return cairosvg
    except Exception:
        return None


def render_with_chromium(svg_file, png_path):
    """Fallback renderer: headless Chromium screenshots the inline SVG."""
    from playwright.sync_api import sync_playwright

    svg = Path(svg_file).read_text(encoding="utf-8")
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(device_scale_factor=2, viewport={"width": 1400, "height": 900})
        page.set_content(
            '<!doctype html><html><body style="margin:0;background:#fff">'
            + svg + "</body></html>",
            wait_until="load",
        )
        page.wait_for_timeout(150)
        page.locator("svg").first.screenshot(path=str(png_path))
        browser.close()


def load_state():
    if STATE_FILE.exists():
        with open(STATE_FILE, encoding="utf-8") as f:
            return json.load(f)
    return {"iterations": 0, "history": [], "svg_file": None}


def save_state(state):
    WORK.mkdir(parents=True, exist_ok=True)
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)


def cmd_render(svg_file):
    path = Path(svg_file)
    if not path.exists():
        print(f"ERROR: File not found: {svg_file}")
        sys.exit(1)

    svg_content = path.read_text(encoding="utf-8")
    if "<svg" not in svg_content:
        print("ERROR: File does not contain valid SVG.")
        sys.exit(1)

    WORK.mkdir(parents=True, exist_ok=True)
    cairosvg = ensure_cairosvg()
    engine = "CairoSVG"
    try:
        if cairosvg is None:
            raise RuntimeError("cairosvg is not installed")
        cairosvg.svg2png(
            bytestring=svg_content.encode("utf-8"),
            write_to=str(PREVIEW_PNG),
            output_width=1000,
        )
    except Exception as exc:
        # CairoSVG needs native cairo libraries; Chromium usually is present.
        try:
            render_with_chromium(path, PREVIEW_PNG)
            engine = "Chromium"
        except Exception as exc2:
            print(f"RENDER ERROR: {exc}")
            print(f"CHROMIUM FALLBACK ERROR: {exc2}")
            print("Fix the SVG syntax and try again.")
            sys.exit(1)

    state = load_state()
    state["iterations"] += 1
    state["svg_file"] = str(path.resolve())
    state["history"].append({
        "iteration": state["iterations"],
        "file": str(path.resolve()),
        "size": len(svg_content),
    })
    save_state(state)

    print("=" * 54)
    print(f"  RENDERED with {engine}: iteration #{state['iterations']}")
    print("=" * 54)
    print(f"  Preview: {PREVIEW_PNG}")
    print("")
    print("  >>> OPEN AND LOOK AT THE PREVIEW IMAGE.")
    print("  >>> Assess it, fix the SVG, run 'render' again.")
    print("=" * 54)


def cmd_finish(svg_file, output_name=None):
    state = load_state()
    if state["iterations"] == 0:
        print("=" * 54)
        print("  BLOCKED: this SVG was never rendered and viewed.")
        print(f"    python svg_loop.py render {svg_file}")
        print("=" * 54)
        sys.exit(1)

    if state["iterations"] < 2:
        print("=" * 54)
        print(f"  WARNING: only {state['iterations']} render(s) done.")
        print("  Best results need 2 or more render-view-fix cycles.")
        print("=" * 54)

    if output_name is None:
        output_name = os.path.basename(svg_file)
    if not output_name.endswith(".svg"):
        output_name += ".svg"

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = OUTPUT_DIR / output_name
    shutil.copy2(svg_file, output_path)

    preview_output = OUTPUT_DIR / output_name.replace(".svg", "_preview.png")
    if PREVIEW_PNG.exists():
        shutil.copy2(PREVIEW_PNG, preview_output)

    print("=" * 54)
    print(f"  DELIVERED after {state['iterations']} iteration(s)")
    print(f"  SVG: {output_path}")
    print(f"  Preview: {preview_output}")
    print("=" * 54)
    save_state({"iterations": 0, "history": [], "svg_file": None})


def cmd_status():
    state = load_state()
    print(f"Work dir: {WORK}")
    print(f"Iterations: {state['iterations']}")
    print(f"Current file: {state.get('svg_file', 'None')}")
    for h in state["history"]:
        print(f"  #{h['iteration']}: {h['file']} ({h['size']} bytes)")


def cmd_reset():
    save_state({"iterations": 0, "history": [], "svg_file": None})
    if PREVIEW_PNG.exists():
        PREVIEW_PNG.unlink()
    print("State reset. Ready for a new SVG.")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    cmd = sys.argv[1]
    if cmd == "render":
        if len(sys.argv) < 3:
            print("Usage: python svg_loop.py render <svg_file>")
            sys.exit(1)
        cmd_render(sys.argv[2])
    elif cmd == "finish":
        if len(sys.argv) < 3:
            print("Usage: python svg_loop.py finish <svg_file> [name.svg]")
            sys.exit(1)
        cmd_finish(sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else None)
    elif cmd == "status":
        cmd_status()
    elif cmd == "reset":
        cmd_reset()
    else:
        print(f"Unknown command: {cmd}")
        print("Commands: render, finish, status, reset")
        sys.exit(1)
