import tkinter as tk
from tkinter import font
from tkinter import ttk
import core

# PROGRAMMER: Import modular component tabs using the new decoupled path structure
from gui.tab_system import SystemTab
from gui.tab_cpu import CpuTab
from gui.tab_ram import RamTab
from gui.tab_storage import StorageTab
from gui.tab_gpu import GpuTab
from gui.tab_network import NetworkTab
from gui.tab_motherboard import MotherboardTab

class MonitorApplication:
    """
    PROGRAMMER: Main container orchestration interface. Supports live reactive 
    Theme Switching Profiles using high contrast Black and White data metrics.
    """
    def __init__(self, has_smartctl, has_nvme):
        self.has_smartctl = has_smartctl
        self.has_nvme = has_nvme
        
        self.root = tk.Tk()
        self.root.title("SysBlock-Inspector | Central de Hardware")
        
        # --- PROG: COMPILED BINARY & PORTABLE IMAGE ICON LOADER (PYINSTALLER SAFE) ---
        try:
            # PROG: IMPORTAÇÕES CRUCIAIS ADICIONADAS PARA IMPEDIR FALHAS EM BACKGROUND!
            import os
            import sys
            
            # Check if the application is running enclosed inside a PyInstaller single executable binary container
            if hasattr(sys, '_MEIPASS'):
                base_dir = sys._MEIPASS
            else:
                base_dir = os.path.dirname(os.path.dirname(__file__))
                
            icon_path = os.path.join(base_dir, "icon.png")
            if os.path.exists(icon_path):
                self.img_icon = tk.PhotoImage(file=icon_path)
                self.root.iconphoto(False, self.img_icon)
        except Exception:
            pass # Fallback protection to ensure code never breaks if the environment layout paths drift
        
        # --- PROG: UNIVERSAL AUTO-MAXIMIZE ENGINE FOR LINUX MINT ---
        try:
            # Native Linux X11/Wayland state sender to force vertical and horizontal maximization
            self.root.attributes('-zoomed', True)
        except Exception:
            try:
                # Secondary POSIX standard execution fallback
                self.root.wm_attributes('-zoomed', 1)
            except Exception:
                # Handcrafted resolution safety fallback if system manager locks windows expansion
                self.root.geometry(f"{self.root.winfo_screenwidth()}x{self.root.winfo_screenheight()}+0+0")
            
        # Dynamic boundaries rules limits (Keeps safety minsize and unlocks full user resizing)
        self.root.minsize(700, 520)
        self.root.resizable(True, True) # UNLOCKED! Allows full user resizing controls

        # PROG: Configured black and white dynamic mapping schema arrays profiles
        self.themes = {
            "dark": {
                "bg_root": "#1a1a1a", "bg_card": "#2d2d2d", "text_sec": "#aaaaaa",
                "text_main": "#ffffff", "tab_bg": "#2d2d2d", "tab_fg": "#888888",
                "alert_ok": "#4cbd5a"
            },
            "light": {
                "bg_root": "#e6e6e6", "bg_card": "#f5f5f5", "text_sec": "#666666",   
                "text_main": "#1a1a1a", "tab_bg": "#dcdcdc", "tab_fg": "#777777",
                "alert_ok": "#008000"
            }
        }

        # PROG: Dynamically checks user system color preferences on startup instead of hardcoding 'dark'
        if core.check_system_dark_preference():
            self.current_theme_key = "dark"
        else:
            self.current_theme_key = "light"

        self.fonts = {
            "section": font.Font(family="Arial", size=10, weight="bold"),
            "label": font.Font(family="Arial", size=9, weight="bold"),
            "value": font.Font(family="Arial", size=10, weight="bold"),
            "monospace": font.Font(family="Courier", size=10, weight="bold")
        }

        self.style = ttk.Style()
        self.style.theme_use('default')

        self.build_notebook_tabs()
        self.toggle_theme(initial_setup=True) # Applies the automatically detected theme palette
        # PROG: UNIVERSAL RESIZE AND MAXIMIZE RECALCULATION LISTENER (FIXES CHATOB_BUG)
        self.root.bind("<Map>", lambda event: self._force_canvas_recalc())
        
    def build_notebook_tabs(self):
        """Instantiates and enforces index priorities, locking System tab on priority position 0."""
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=12, pady=12)

        # PROG: Instantiates custom tabs passing the local toggle_theme reference pointer into the system frame
        self.tab_system = SystemTab(self.notebook, self.fonts, self.toggle_theme)
        self.tab_cpu = CpuTab(self.notebook, self.fonts)
        self.tab_motherboard = MotherboardTab(self.notebook, self.fonts)
        self.tab_ram = RamTab(self.notebook, self.fonts)
        self.tab_gpu = GpuTab(self.notebook, self.fonts)
        self.tab_network = NetworkTab(self.notebook, self.fonts)
        self.tab_storage = StorageTab(self.notebook, self.fonts, self.has_smartctl, self.has_nvme)


        # PROG: Added SYSTEM tab as the first item on the notebook execution array stack
        self.notebook.add(self.tab_system, text="  💻  SISTEMA  ")
        self.notebook.add(self.tab_cpu, text="  ❖  PROCESSADOR  ")
        self.notebook.add(self.tab_motherboard, text="  🔌 PLACA-MÃE  ")
        self.notebook.add(self.tab_ram, text="  ▤  MEMÓRIA RAM  ")
        self.notebook.add(self.tab_gpu, text="  🖥  PLACA DE VÍDEO  ")
        self.notebook.add(self.tab_network, text="  🌐  REDE  ") 
        self.notebook.add(self.tab_storage, text="  💾  ARMAZENAMENTO  ")

    def toggle_theme(self, initial_setup=False):
        """PROG: Switches UI state profiles and triggers child tab repaints."""
        if not initial_setup:
            self.current_theme_key = "light" if self.current_theme_key == "dark" else "dark"

        colors = self.themes[self.current_theme_key]
        self.root.configure(bg=colors["bg_root"])

        self.style.configure('TNotebook', background=colors["bg_root"])
        self.style.configure('TNotebook.Tab', 
                        background=colors["tab_bg"], foreground=colors["tab_fg"], 
                        font=('Arial', 9, 'bold'), padding=8, borderwidth=0)
        
        self.style.map('TNotebook.Tab', 
                  background=[('selected', colors["bg_card"])], 
                  foreground=[('selected', colors["text_main"])])

        # Force structural background color updates across ALL core frames context
        self.tab_system.apply_theme_colors(colors)
        self.tab_cpu.apply_theme_colors(colors)
        self.tab_motherboard.apply_theme_colors(colors) 
        self.tab_ram.apply_theme_colors(colors)
        self.tab_gpu.apply_theme_colors(colors)
        self.tab_network.apply_theme_colors(colors)
        self.tab_storage.apply_theme_colors(colors)

        # Repaint local embedded button text styles natively
        self.tab_system.update_tab_ui_theme(self.current_theme_key)

        if not initial_setup:
            self._clean_dynamic_background_leaks(colors)

    def _clean_dynamic_background_leaks(self, colors):
        """
        PROG: Universal recursive layout re-painter module. 
        Instantly wipes dark or light background leakage across all dynamically generated hardware rows.
        Unified character token mappings to guarantee absolute monochromatic simetry.
        """
        # 1. CLEAN BACKGROUND LEAKS INSIDE DYNAMIC PER-CORE CPU CLOCKS LOOPS ROWS
        for lbl in self.tab_cpu.dynamic_core_labels:
            if lbl.winfo_exists():
                lbl.master.config(bg=colors["bg_card"])
                lbl.config(bg=colors["bg_card"], fg=colors["text_main"])
                for sibling in lbl.master.winfo_children():
                    if sibling.winfo_exists():
                        sibling.config(bg=colors["bg_card"])
                        if sibling != lbl: 
                            sibling.config(fg=colors["text_sec"])

        # 2. CLEAN BACKGROUND LEAKS INSIDE DYNAMICALLY GENERATED STORAGE DEVICES LOOPS ROWS (STATIC CARDS)
        for title, cached_frame in self.tab_storage.storage_frames_cache.items():
            if cached_frame.winfo_exists():
                cached_frame.config(bg=colors["bg_card"], fg=colors["text_main"])
                for row_child in cached_frame.winfo_children():
                    if row_child.winfo_exists():
                        row_child.config(bg=colors["bg_card"])
                        for sub_label in row_child.winfo_children():
                            if sub_label.winfo_exists():
                                sub_label.config(bg=colors["bg_card"])
                                current_fg = sub_label.cget("fg")
                                if current_fg != "#ff3333" and current_fg != "#4cbd5a" and current_fg != "#008000":
                                    # FIXED UNIFIED FILTER MATRIX WITH ⚙ FOR MOUNTED BLOCK LINES
                                    if any(x in sub_label.cget("text") for x in ["👤", "💻", "🔌", "⚙", "📁", "🔑", "🕒", "🌐", "🎛", "📂", "▤", "☱", "🐚", "🖥", "📦"]):
                                         sub_label.config(fg=colors["text_sec"])
                                    else:
                                        sub_label.config(fg=colors["text_main"])

        # 3. CLEAN BACKGROUND LEAKS INSIDE DYNAMICALLY GENERATED MULTI-INTERFACE NETWORK CARDS LOOPS (HOTPLUG DEVS)
        for iface, cached_card in self.tab_network.network_cards_cache.items():
            if cached_card.winfo_exists():
                cached_card.config(bg=colors["bg_card"], fg=colors["text_main"])
                for row_child in cached_card.winfo_children():
                    if row_child.winfo_exists():
                        row_child.config(bg=colors["bg_card"])
                        for sub_label in row_child.winfo_children():
                            if sub_label.winfo_exists():
                                sub_label.config(bg=colors["bg_card"])
                                current_text = sub_label.cget("text")
                                
                                if current_text == "Conectado": 
                                    sub_label.config(fg=colors["alert_ok"])
                                elif current_text == "Desconectado" or "Falha" in current_text: 
                                    sub_label.config(fg="#ff3333")
                                # FIXED UNIFIED FILTER MATRIX WITH ⚙ FOR NET AND HOTPLUG DEV LINES
                                elif any(x in sub_label.cget("text") for x in ["⌗", "⧇", "🔲", "🌐", "⚿", "▤", "▱", "⌺", "⚡", "⚙", "⏱", "❯"]):
                                    sub_label.config(fg=colors["text_sec"])
                                else:
                                    if sub_label.cget("fg") != "#ff3333" and sub_label.cget("fg") != "#4cbd5a" and sub_label.cget("fg") != "#008000":
                                        sub_label.config(fg=colors["text_main"])

        # 4. GUARD HARDWARE VIRTUALIZATION SEMANTIC ALERTS DYNAMIC RE-PAINTS
        vt_field = self.tab_cpu.fields.get("vt_state")
        if vt_field and vt_field.winfo_exists():
            vt_field.config(fg="#ff3333" if "Inativa" in vt_field.cget("text") else colors["alert_ok"])

    def refresh_telemetry_loop(self):
        try: self.tab_system.update_telemetry()
        except Exception as e: print(f"[System Loop Error]: {e}")
            
        try: self.tab_cpu.update_telemetry()
        except Exception as e: print(f"[CPU Loop Error]: {e}")
            
        try: self.tab_ram.update_telemetry()
        except Exception as e: print(f"[RAM Loop Error]: {e}")
            
        try: self.tab_gpu.update_telemetry()
        except Exception as e: print(f"[GPU Loop Error]: {e}")
            
        try: self.tab_network.update_telemetry()
        except Exception as e: print(f"[Network Loop Error]: {e}")
            
        try: self.tab_storage.update_telemetry()
        except Exception as e: print(f"[Storage Loop Error]: {e}")

        colors = self.themes[self.current_theme_key]
        self._clean_dynamic_background_leaks(colors)

        self.root.after(2000, self.refresh_telemetry_loop)

    def run(self):
        self.refresh_telemetry_loop()
        self.root.mainloop()

    def _force_canvas_recalc(self):
        """
        PROG: Forces the Tkinter viewport engine to immediately compute the exact coordinates
        of all canvas frame structures, locking the elements to the top to destroy the visual bug.
        """
        # Recalculate CPU Tab Viewport
        if hasattr(self, 'tab_cpu'):
            if hasattr(self.tab_cpu, 'canvas') and self.tab_cpu.canvas.winfo_exists():
                self.tab_cpu.canvas.update_idletasks()
                self.tab_cpu.canvas.configure(scrollregion=self.tab_cpu.canvas.bbox("all"))

        # Recalculate Motherboard Tab Viewport
        if hasattr(self, 'tab_motherboard'):
            if hasattr(self.tab_motherboard, 'canvas') and self.tab_motherboard.canvas.winfo_exists():
                self.tab_motherboard.canvas.update_idletasks()
                self.tab_motherboard.canvas.configure(scrollregion=self.tab_motherboard.canvas.bbox("all"))

        # Recalculate RAM Tab Viewport (ADICIONADO)
        if hasattr(self, 'tab_ram'):
            if hasattr(self.tab_ram, 'canvas') and self.tab_ram.canvas.winfo_exists():
                self.tab_ram.canvas.update_idletasks()
                self.tab_ram.canvas.configure(scrollregion=self.tab_ram.canvas.bbox("all"))

        # Recalculate GPU Tab Viewport
        if hasattr(self, 'tab_gpu'):
            if hasattr(self.tab_gpu, 'canvas') and self.tab_gpu.canvas.winfo_exists():
                self.tab_gpu.canvas.update_idletasks()
                self.tab_gpu.canvas.configure(scrollregion=self.tab_gpu.canvas.bbox("all"))

        # Recalculate Network Tab Viewport (ADICIONADO)
        if hasattr(self, 'tab_network'):
            if hasattr(self.tab_network, 'canvas') and self.tab_network.canvas.winfo_exists():
                self.tab_network.canvas.update_idletasks()
                self.tab_network.canvas.configure(scrollregion=self.tab_network.canvas.bbox("all"))
                
        # Recalculate Storage Tab Viewport
        if hasattr(self, 'tab_storage'):
            if hasattr(self.tab_storage, 'canvas') and self.tab_storage.canvas.winfo_exists():
                self.tab_storage.canvas.update_idletasks()
                self.tab_storage.canvas.configure(scrollregion=self.tab_storage.canvas.bbox("all"))


