#!/usr/bin/env python3
import os
import sys
import shutil
import subprocess

# -------------------------------------------------------------
# INITIALIZATION CONTROL: Validates Tkinter framework presence
# -------------------------------------------------------------
try:
    import tkinter as tk
    from tkinter import messagebox
    HAS_GUI_LIB = True
except ImportError:
    HAS_GUI_LIB = False

def check_and_enforce_root_privileges():
    """
    PROGRAMMER: Modern Polkit (PolicyKit) Graphical Elevation Engine.
    Checks if the process is running with root administrative rights (UID 0).
    If not, it automatically respawns itself using the native system authentication 
    dialog window (pkexec). Fully calibrated for scripts and compiled PyInstaller binaries.
    """
    # 1. Check if the application is already running as root (UID 0)
    if os.geteuid() == 0:
        return True

    print("[SysBlock-Inspector Launcher]: Privilégios insuficientes. Invocando autenticação gráfica nativa...")
    
    # PROG: Dynamically detect if we are running as a compiled frozen binary or a raw script text file
    if getattr(sys, 'frozen', False):
        script_path = os.path.abspath(sys.executable)
        is_binary_mode = True
    else:
        script_path = os.path.abspath(sys.argv[0])
        is_binary_mode = False
    
    # 2. Modern GUI Elevation Command Construction (Polkit Standard)
    display_env = os.environ.get("DISPLAY", ":0")
    xauth_env = os.environ.get("XAUTHORITY", "")
    
    if not xauth_env:
        user_home = os.environ.get("HOME", f"/home/{os.environ.get('USER')}")
        potential_xauth = os.path.join(user_home, ".Xauthority")
        if os.path.exists(potential_xauth):
            xauth_env = potential_xauth

    # Construct execution chains avoiding re-interpreting compiled ELF bytes structures
    if is_binary_mode:
        pkexec_cmd = [
            "pkexec", "env",
            f"DISPLAY={display_env}",
            f"XAUTHORITY={xauth_env}",
            script_path
        ] + sys.argv[1:]
    else:
        pkexec_cmd = [
            "pkexec", "env",
            f"DISPLAY={display_env}",
            f"XAUTHORITY={xauth_env}",
            "python3", script_path
        ] + sys.argv[1:]

    try:
        # Respawn the script under pkexec context. This blocks the current non-root process 
        # and opens the beautiful, modern native system authentication prompt window
        result = subprocess.run(pkexec_cmd)
        sys.exit(result.returncode)
    except Exception as e:
        print(f"[Launcher Failure]: Erro ao invocar pkexec: {str(e)}")
        sys.exit(1)

def show_critical_alert(error_message):
    """Throws clear error explanations on fallback channels."""
    if HAS_GUI_LIB:
        temporary_root = tk.Tk()
        temporary_root.withdraw()
        messagebox.showerror("Erro de Inicialização", error_message)
        temporary_root.destroy()
    else:
        print(f"\n[ERRO CRÍTICO]: {error_message}\n")

def run_environment_checks():
    # 1. Evaluate core python interpreter architecture version
    if sys.version_info.major < 3:
        show_critical_alert("Este programa precisa do Python 3 para funcionar.")
        sys.exit(1)

    # 2. Evaluate Tkinter system-level bindings
    if not HAS_GUI_LIB:
        missing_tk_alert = (
            "A interface gráfica padrão (Tkinter) não está instalada.\n\n"
            "Para corrigir, abra o terminal e execute o comando correspondente:\n"
            "- Ubuntu/Debian/Mint: sudo apt install python3-tk\n"
            "- Fedora: sudo dnf install python3-tkinter\n"
            "- Arch Linux: sudo pacman -S tk"
        )
        show_critical_alert(missing_tk_alert)
        sys.exit(1)

    # 3. Scan system PATH configurations for low-level diagnostic binaries
    has_smartctl = shutil.which("smartctl") is not None
    has_nvme = shutil.which("nvme") is not None

    if not has_smartctl or not has_nvme:
        missing_storage_alert = (
            "Aviso: Alguns componentes de monitoramento de disco estão faltando.\n\n"
            "O programa vai abrir para monitorar CPU e RAM, mas para ver a saúde dos SSDs e HDs, "
            "instale as dependências abaixo pelo seu terminal:\n\n"
        )
        if not has_smartctl:
            missing_storage_alert += "- Para o HD: Instale o pacote 'smartmontools'\n"
        if not has_nvme:
            missing_storage_alert += "- Para o SSD: Instale o pacote 'nvme-cli'\n"
            
        missing_storage_alert += "\nO sistema continuará a inicialização básica..."
        messagebox.showwarning("Componentes Ausentes", missing_storage_alert)

    # 4. Safely load internal sub-modules and start runtime instance
    try:
        # PROGRAMMER: Updated pointer to fetch MonitorApplication from the new gui/app package context
        from gui.app import MonitorApplication
        active_app = MonitorApplication(has_smartctl, has_nvme)
        active_app.run()
    except Exception as internal_error:
        show_critical_alert(f"Erro ao carregar os arquivos internos do programa (gui/app.py ou core.py).\nDetalhe: {internal_error}")
        sys.exit(1)

if __name__ == "__main__":
    # PROG: Invokes modern graphical authentication enforcement rule first before the checks
    check_and_enforce_root_privileges()
    
    # If already root, proceed safely to your original checks and application launch pipelines
    run_environment_checks()
