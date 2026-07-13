# 🤖 SysBlock-Inspector: AI Development & Maintenance Rules

This file acts as a permanent architectural memory anchor for any Advanced Language Model (AI) or LLM assistant tasked with modifying, refactoring, or updating the **SysBlock-Inspector** source code.

To prevent graphical glitches, concurrency deadlocks, and compatibility regressions, **you must read and strictly adhere to the following rules.**

---

## 📂 Project Directory Structure

Any assistant modifying the code must respect and maintain this exact lightweight architectural layout:

```text
SysBlock-Inspector/
├── ai-instructions.md        (This file - Permanent AI constraints and guidelines)
├── build.sh                  (Automated master PyInstaller execution compiler tool)
├── core.py                   (Decoupled hardware querying logic and lspci JSON crawlers)
├── create_deb.sh             (Native Debian/Mint dpkg packaging automation script)
├── create_rpm.sh             (Native Fedora Workstation rpmbuild packaging automation script)
├── icon.png                  (Official application commercial logo image asset)
├── main.py                   (Polkit elevation engine wrapper and critical validation triggers)
├── README.md                 (Official bilingual English/Portuguese user documentation manual)
└── gui/                      (Centralized Tkinter visual components layout modules)
    ├── __init__.py           (Package initialization definitions metadata)
    ├── app.py                (Application orchestrator, dynamic main loops, and theme controllers)
    ├── base_tab.py           (Abstract core frame with grid alignment row generation methods)
    ├── tab_cpu.py            (Aba 2: Dynamic multi-thread core clock tracker monitor)
    ├── tab_gpu.py            (Aba 5: Hardware-level visual silicon graphics extractor)
    ├── tab_motherboard.py    (Aba 3: BIOS traces, integrated audio codecs, and electrical PCI linkages)
    ├── tab_network.py        (Aba 6: Real physical layers chip metrics and live bandwidth counters)
    ├── tab_ram.py            (Aba 4: Scans physical traces to count slots and JEDEC manufacturer specs)
    ├── tab_storage.py        (Aba 7: JSON block device trees and fragmented SMART health audit)
    └── tab_system.py         (Aba 1: System overview, Neofetch specs, and active Display Server X11/Wayland triggers)
```

---

## 🏗️ 1. Architecture Constraints (Read-Only Blueprint)

- **Decoupled Architecture**: Keep the codebase split strictly into `core.py` (hardware querying logic via native POSIX files like `/sys/` and `/proc/`) and the `gui/` package (Tkinter visualization layout layers). Never mix telemetry polling inside GUI code.
- **Root Elevation standard (`main.py`)**: The application uses the Polkit graphical launcher (`pkexec`) to escalate to root permissions securely. It handles frozen PyInstaller binaries (`sys.executable`) and text scripts (`sys.argv`) differently to prevent binary string `ELF` null bytes syntax crashes. Do NOT refactor the initialization loop unless a Polkit API evolution occurs.
- **No External Packages Dependencies**: The core engine must remain purely portable. Do not import heavy frameworks like `psutil`, `GPUtil`, or external graphic toolkits. Stick to native subshell pipes (`subprocess`), JSON parsing, text regex parsing, and standard library components.

---

## 🎨 2. GUI & Tkinter Engineering Rules (Crucial)

- **The Canvas Scroll Engine**: Every tab inherits structural row and card methods from `BaseTab`. Content frames are nested inside a scrollable `tk.Canvas` window to prevent text truncation across diverse notebook screen configurations.
- **Strict Size Calculation Rules**: The `update_telemetry()` loops in tabs use active `self.canvas.update_idletasks()` and `scrollregion` bounds bounding matrix computations.
- **The Maximize Reset Hook**: There is a permanent map binder pointer binding `<Map>` events to trigger `self._force_canvas_recalc()` upon maximizing windows. Any modifications to structural widget packing grids must execute a canvas calculation refresh immediately, or it will leak black canvas frames zones (the historical 'vão preto' layout bug).
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

## 🎯 5. Code Injection Mapping Rules (Where to put what)

When generating code modifications, you must guide the developer to target the exact file layers according to these logical rules:

1. **System Queries & Native Traces**: All additions related to Linux terminal commands (`lsblk`, `df`, `dmidecode`, `lspci`) or Kernel text reads must go **strictly into `core.py`** inside a dedicated function returning primitive Python data types (dicts, strings, lists).
2. **Visual Layout and Grids Packaging**: All additions of new fields, text lines, or group boxes must go **strictly into their respective `gui/tab_*.py` file**. New labels must be appended to the master layout using the native `self.append_grid_row()` method inherited from `BaseTab`.
3. **Dynamic Loop Metrics Updates**: If a newly added metric requires high-frequency polling updates (like tracking clocks or network usage counters), you must add its calculation hook inside the active `update_telemetry(self)` loop found inside that specific tab file.
4. **Theme Palettes & Window Attributes**: All universal application states, button commands, or changes to theme color keys must go **strictly into `gui/app.py`**.

---

## 💬 6. Master Prompt Templates (How Humans should instruct the AI)

If a developer opens a chat with an Advanced LLM model in the browser or via IDE terminal extension to modify this project, they should copy and paste one of these prompt blueprints to enforce absolute architectural discipline:

### Template A: Adding a New Tab Component (Expansion)

> "I want to add an experimental new tab component called 'Sensors' into our Python project. First, analyze the `ai-instructions.md` file in the root directory to map the layout rules. Create the telemetry extraction logic inside `core.py` without third-party libraries, then build a matching `tab_sensors.py` file inheriting from `BaseTab` using the scrollable Canvas engine. Finally, show me where to inject the tab instantiation hook inside `gui/app.py` and ensure the canvas re-calculation listener includes this new tab. Do not break the clean dark/light theme triggers."

### Template B: Fixing or Updating an Existing Metric (Maintenance)

> "Our application is running in an elevated root administrative layer via `pkexec`, and we need to update a metric inside `gui/tab_system.py` or `core.py`. Read the `ai-instructions.md` blueprint. Ensure that your solution redirects permissions properly to the real graphical user profile by prefixing subshells with `sudo -u username` where required. Wrap the entire data collection block inside local `try/except` brackets to bypass slow I/O fault timeouts, and map the updated variables straight into the centralized `self.fields` dictionary array registers without breaking the canvas scroll bounds."

### Template C: Refining the Package Compilers Scripts (Infrastructure)

> "I need to update the native building scripts (`build.sh`, `create_deb.sh`, or `create_rpm.sh`) to support a custom package distribution layout. Open the `ai-instructions.md` map. Make sure your shell scripting edits maintain the automated administrative sudo cleaning layers (`sudo rm -rf build/ dist/`) to wipe out old `__pycache__` permission blocks, and preserve the PyInstaller `_MEIPASS` relative paths triggers inside `gui/app.py` so the standalone compiled single-binary container does not lose its embedded `icon.png` reference."
