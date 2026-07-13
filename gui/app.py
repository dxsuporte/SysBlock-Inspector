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
    PROGRAMMER: Main container orchestration interface.
    Pure, raw standalone utility running with native operating system styles.
    """
    def __init__(self, has_smartctl, has_nvme):
        self.has_smartctl = has_smartctl
        self.has_nvme = has_nvme
        
        self.root = tk.Tk()
        self.root.title("SysBlock-Inspector | Central de Hardware")
        
        # --- PROG: COMPILED BINARY & PORTABLE IMAGE ICON LOADER (PYINSTALLER SAFE) ---
        try:
            import os
            import sys
            
            if hasattr(sys, '_MEIPASS'):
                base_dir = sys._MEIPASS
            else:
                base_dir = os.path.dirname(os.path.dirname(__file__))
            
            icon_path = os.path.join(base_dir, "icon.png")
            if os.path.exists(icon_path):
                self.img_icon = tk.PhotoImage(file=icon_path)
                self.root.iconphoto(False, self.img_icon)
        except Exception:
            pass
        
        # --- PROG: UNIVERSAL AUTO-MAXIMIZE ENGINE FOR LINUX MINT ---
        try:
            self.root.attributes('-zoomed', True)
        except Exception:
            try:
                self.root.wm_attributes('-zoomed', 1)
            except Exception:
                self.root.geometry(f"{self.root.winfo_screenwidth()}x{self.root.winfo_screenheight()}+0+0")
        
        self.root.minsize(700, 520)
        self.root.resizable(True, True)
        
        # Font definitions matching standard system layouts
        self.fonts = {
            "section": font.Font(family="Arial", size=10, weight="bold"),
            "label": font.Font(family="Arial", size=9, weight="bold"),
            "value": font.Font(family="Arial", size=10, weight="bold"),
            "monospace": font.Font(family="Courier", size=10, weight="bold")
        }
        
        self.style = ttk.Style()
        self.style.theme_use('default')
        
        self.build_notebook_tabs()
        
        # PROG: UNIVERSAL RESIZE AND MAXIMIZE RECALCULATION LISTENER
        self.root.bind("<Map>", lambda event: self._force_canvas_recalc())
        
    def build_notebook_tabs(self):
        """Instantiates and enforces index priorities, forcing 100% horizontal expansion response."""
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=12, pady=12)
        
        self.tab_system = SystemTab(self.notebook, self.fonts)
        self.tab_cpu = CpuTab(self.notebook, self.fonts)
        self.tab_motherboard = MotherboardTab(self.notebook, self.fonts)
        self.tab_ram = RamTab(self.notebook, self.fonts)
        self.tab_gpu = GpuTab(self.notebook, self.fonts)
        self.tab_network = NetworkTab(self.notebook, self.fonts)
        self.tab_storage = StorageTab(self.notebook, self.fonts, self.has_smartctl, self.has_nvme)
        
        # --- FIX SUPREMO DE RESPONSIVIDADE NATIVA ---
        # Força os frames das abas a expandirem e preencherem 100% do espaço do Notebook
        self.tab_system.pack(fill="both", expand=True)
        self.tab_cpu.pack(fill="both", expand=True)
        self.tab_motherboard.pack(fill="both", expand=True)
        self.tab_ram.pack(fill="both", expand=True)
        self.tab_gpu.pack(fill="both", expand=True)
        self.tab_network.pack(fill="both", expand=True)
        self.tab_storage.pack(fill="both", expand=True)
        
        self.notebook.add(self.tab_system, text=" 💻 SISTEMA ")
        self.notebook.add(self.tab_cpu, text=" ❖ PROCESSADOR ")
        self.notebook.add(self.tab_motherboard, text=" 🔌 PLACA-MÃE ")
        self.notebook.add(self.tab_ram, text=" ▤ MEMÓRIA RAM ")
        self.notebook.add(self.tab_gpu, text=" 🖥 PLACA DE VÍDEO ")
        self.notebook.add(self.tab_network, text=" 🌐 REDE ") 
        self.notebook.add(self.tab_storage, text=" 💾 ARMAZENAMENTO ")

    def refresh_telemetry_loop(self):
        """Pure background telemetry gathering pipeline execution context with strict reference mapping."""
        try: 
            self.tab_system.update_telemetry()
        except Exception as e: 
            print(f"[System Loop Error]: {e}")
        
        try: 
            self.tab_cpu.update_telemetry()
        except Exception as e: 
            print(f"[CPU Loop Error]: {e}")
        
        try: 
            self.tab_motherboard.update_telemetry()
        except Exception as e: 
            print(f"[Motherboard Loop Error]: {e}")
            
        try: 
            self.tab_ram.update_telemetry()
        except Exception as e: 
            print(f"[RAM Loop Error]: {e}")
        
        try: 
            self.tab_gpu.update_telemetry()
        except Exception as e: 
            print(f"[GPU Loop Error]: {e}")
        
        # PROG: Força a atualização da rede interrogando diretamente as duas referências possíveis
        try:
            if hasattr(self, 'tab_network'):
                self.tab_network.update_telemetry()
            elif hasattr(self, 'tab_net'):
                self.tab_net.update_telemetry()
        except Exception as e: 
            print(f"[Network Loop Error]: {e}")
        
        try: 
            self.tab_storage.update_telemetry()
        except Exception as e: 
            print(f"[Storage Loop Error]: {e}")
        
        self.root.after(2000, self.refresh_telemetry_loop)

    def run(self):
        self.refresh_telemetry_loop()
        self.root.mainloop()

    def _force_canvas_recalc(self):
        """
        PROGRAMMER: Universal high-efficiency responsive layout matrix engine.
        Forces the inner Tkinter canvas windows to dynamically computation 
        and scale their widths to match 100% of the active viewport display.
        """
        # Lista com todas as abas que possuem a estrutura de rolagem do Canvas
        active_tabs = [self.tab_system, self.tab_cpu, self.tab_motherboard, 
                       self.tab_ram, self.tab_gpu, self.tab_network, self.tab_storage]
        
        for tab in active_tabs:
            # Verifica se a aba e o Canvas físico existem e estão renderizados na tela
            if hasattr(tab, 'canvas') and tab.canvas.winfo_exists():
                tab.canvas.update_idletasks()
                
                # 1. CAPTURA A LARGURA REAL ATUAL DO ACESSO DO MONITOR
                canvas_width = tab.canvas.winfo_width()
                
                # 2. XEQUE-MATE DE RESPONSIVIDADE NATIVA!
                # Força o Frame de conteúdo a esticar sua largura para casar 100% com o Canvas
                if hasattr(tab, 'scroll_content_id'):
                    tab.canvas.itemconfig(tab.scroll_content_id, width=canvas_width)
                
                # 3. Executa o recalculo padrão de atualização da esteira de rolagem
                if hasattr(tab, 'scroll_content_frame'):
                    tab.canvas.configure(scrollregion=tab.canvas.bbox("all"))

