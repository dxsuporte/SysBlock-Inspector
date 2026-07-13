# 🤖 SysBlock-Inspector: AI Development & Maintenance Rules

This file acts as a permanent architectural memory anchor for any Advanced Language Model (AI) or LLM assistant tasked with modifying, refactoring, or updating the **SysBlock-Inspector** source code.

To prevent graphical glitches, concurrency deadlocks, and compatibility regressions, **you must read and strictly adhere to the following rules.**

---

## 🏗️ 1. Architecture Constraints (Read-Only Blueprint)

- **Decoupled Architecture**: Keep the codebase split strictly into `core.py` (hardware querying logic via native POSIX files like `/sys/` and `/proc/`) and the `gui/` package (Tkinter visualization layout layers). Never mix telemetry polling inside GUI code.
- **Root Elevation standard (`main.py`)**: The application uses the Polkit graphical launcher (`pkexec`) to escalate to root permissions securely. It handles frozen PyInstaller binaries (`sys.executable`) and text scripts (`sys.argv`) differently to prevent binary string `ELF` null bytes syntax crashes. Do NOT refactor the initialization loop unless a Polkit API evolution occurs.
- **No External Packages Dependencies**: The core engine must remain purely portable. Do not import heavy frameworks like `psutil`, `GPUtil`, or external graphic toolkits. Stick to native subshell pipes (`subprocess`), JSON parsing, text regex parsing, and standard library components.

---

## 🎨 2. GUI & Tkinter Engineering Rules (Crucial)

- **The Canvas Scroll Engine**: Every tab inherits structural row and card methods from `BaseTab`. Content frames are nested inside a scrollable `tk.Canvas` window to prevent text truncation across diverse notebook screen configurations.
- **Strict Size Calculation Rules**: The `update_telemetry()` loops in tabs use active `self.canvas.update_idletasks()` and `scrollregion` bounds bounding matrix computations.
- **The Maximize Reset Hook**: There is a strict map binder pointer binding `<Map>` events to trigger `self._force_canvas_recalc()` upon maximizing windows. Any modifications to structural widget packing grids must execute a canvas calculation refresh immediately, or it will leak black canvas frames zones (the historical 'vão preto' layout bug).
- **Widgets Identifiers Framework**: All label modification elements are registered inside the centralized dictionary pointer mapping `self.fields[key_id].config(text=...)`. Do not search for local variables directly. Use structured numeric loop counters rows arrays or strict string tokens mapping to update active tabs rows fields labels.

---

## 🕵️ 3. Linux Kernel & Telemetry Interrogation Rules

- **User-Space Graphical Redirect Matrix**: Since the compiled application runs inside a privileged administrative shell root context via `pkexec`, commands pulling current desktop preferences (`gsettings`, `printenv`, `XDG_SESSION_TYPE`) will default to root leaks (rendering text as `N/A`).
- **The Sudo Subshell Route**: To fetch authentic client environment track strings, you must dynamically locate the logged graphical non-root operator username (checking `$SUDO_USER` or system session lines triggers falling back to the lab defaults variable `danilo`). Then invoke configuration commands prefixing the shell subshell execution string array natively with `sudo -u username`.
- **GTK Configuration File Fallback Overrides**: Do not rely on `gsettings` alone for themes or icon layout configurations. It can fail silently over root D-Bus communication barriers. Always parse the native system text configuration tables files located directly inside the home directories files targets (`~/.config/gtk-3.0/settings.ini`).

---

## 🚀 4. How to Prompt This AI for Code Updates

When a human user prompts you to add a feature or fix a bug in this system, you must:

1. **Analyze Dependencies Impact**: Ensure your changes don't disrupt the index pairing array pipelines (e.g. matching block arrays to network adapters types or SSDs hardware layouts).
2. **Handle I/O Faults Gracefully**: Wrap ALL dynamic live update routines inside local `try/except` blocks. Remote mounts or sleeping device blocks can throw slow timeouts or I/O Input/Output errors (e.g., dead SFTP hanging connections). The UI loop must never freeze under an attribute or communication exception fault state.
3. **Preserve Compilations Automations**: Ensure code adjustments do not introduce syntax elements incompatible with PyInstaller compressed `--onefile` runtime extractions layers patterns routes (`_MEIPASS` dynamic directory context paths targets).

---

_Follow these instructions to protect the stability and performance legacy of this field-support tool._
