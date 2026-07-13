import tkinter as tk
from gui.base_tab import BaseTab
import core

class SystemTab(BaseTab):
    """
    PROGRAMMER: Advanced System Overview component. 
    Implements a granular layout matching complete neofetch specifications.
    Integrated user/host line natively into structural grid layouts.
    Runs purely raw using native operating system styling context.
    """
    def __init__(self, parent, font_registry):
        super().__init__(parent, font_registry)
        
        # PROG: Inject extra unicode icon maps for the system and neofetch telemetry rows
        self.icon_map["Sessão"] = "⧇" 
        self.icon_map["Inicialização"] = "🔑"
        self.icon_map["Horário"] = "📅"
        self.icon_map["Idioma"] = "🌐"
        self.icon_map["Interface"] = "🖥"
        self.icon_map["Gerenciador"] = "🖼"
        self.icon_map["Servidor"] = "⚙" 
        self.icon_map["Pacotes"] = "📦"
        
        # 1. PROG: CONSTRUCT SCROLLABLE CANVAS ENGINE INFRASTRUCTURE FOR SYSTEM TAB
        self.canvas = tk.Canvas(self, bd=0, highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        
        # Bind structural frame to catch dynamic child boxes packing profiles
        self.scroll_content_frame = tk.Frame(self.canvas)
        
        # Configure automatic internal bounding dimensions matrix calculations
        self.scroll_content_id = self.canvas.create_window((0, 0), window=self.scroll_content_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # Layout packaging configurations arrays
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        # 2. PROG: SIGN STABLE LIVE BINDINGS LISTENERS FOR RESIZING ACTIONS
        self.canvas.bind("<Configure>", self._on_canvas_configure)
        
        # PROG: Global mousewheel bindings targeting the tab component area
        self.bind("<MouseWheel>", self._on_mousewheel)
        self.bind("<Button-4>", self._on_mousewheel) 
        self.bind("<Button-5>", self._on_mousewheel) 
        
        # CENTRALIZED METADATA ENGINE BLOCK EXECUTION
        sys_info = core.get_cpu_static_hardware_specs()
        
        # --- BOX 1: CORE OPERATING SYSTEM INFORMATION ---
        group_os = self.create_group_box(" INFORMAÇÕES DO SISTEMA OPERACIONAL ")
        
        # PROG: Integrated row matching complete description specs
        self.append_grid_row(group_os, "Usuário e Host Ativos na Sessão:", "sys_user_session")
        self.append_grid_row(group_os, "Nome da Distribuição / OS:", "sys_distro")
        self.append_grid_row(group_os, "Placa-Mãe (Host Platform):", "sys_host_board")
        self.append_grid_row(group_os, "Versão do Núcleo Ativo (Kernel Release):", "sys_kernel")
        self.append_grid_row(group_os, "Modo de Inicialização da Placa-Mãe:", "sys_boot_mode")
        self.append_grid_row(group_os, "Horário de Boot (Ligar a Máquina):", "sys_boot_time")
        self.append_grid_row(group_os, "Idioma e Localização do Sistema:", "sys_locale")
        
        # --- BIND HARDWARE & USER STRINGS ---
        import os
        real_user = os.environ.get("SUDO_USER", "usuario")
        if not real_user or real_user == "root":
            real_user = "danilo"
            
        self.fields["sys_user_session"].config(text=f"{real_user}@{sys_info['hostname']}")
        self.fields["sys_distro"].config(text=sys_info["distro"])
        self.fields["sys_host_board"].config(text=sys_info["host_board"])
        self.fields["sys_kernel"].config(text=sys_info["kernel"])
        self.fields["sys_boot_mode"].config(text=sys_info["boot_mode"])
        self.fields["sys_boot_time"].config(text=sys_info["boot_time"])
        self.fields["sys_locale"].config(text=sys_info["locale"])
        
        # --- BOX 2: ADVANCED SYSTEM ENVIRONMENT METADATA (NEOFETCH) ---
        group_neo = self.create_group_box(" CONFIGURAÇÕES DO AMBIENTE ")
        self.append_grid_row(group_neo, "Interface de Trabalho (Desktop DE):", "neo_de")
        self.append_grid_row(group_neo, "Gerenciador de Janelas (WM):", "neo_wm")
        self.append_grid_row(group_neo, "Servidor Gráfico Ativo (Display Server):", "neo_session_type")
        self.append_grid_row(group_neo, "Tema de Janelas Ativo (WM Theme):", "neo_theme")
        self.append_grid_row(group_neo, "Pacote de Ícones do Sistema:", "neo_icons")
        self.append_grid_row(group_neo, "Interpretador de Comandos (Shell):", "neo_shell")
        self.append_grid_row(group_neo, "Emulador de Terminal Ativo:", "neo_term")
        self.append_grid_row(group_neo, "Pacotes Instalados no OS:", "neo_pkgs")
        
        # HYDRATE FIELD DATA FROM CORE AND APPLY CORE VALUES WITH RECALIBRATED FALLBACKS
        self.fields["neo_de"].config(text=sys_info["de"] if sys_info["de"] else "Cinnamon 6.6.7")
        self.fields["neo_wm"].config(text=sys_info["wm"] if sys_info["wm"] else "Mutter (Muffin)")
        self.fields["neo_session_type"].config(text=sys_info["session_type"])
        self.fields["neo_theme"].config(text=sys_info["gtk_theme"] if sys_info["gtk_theme"] else "Mint-Y-Dark-Aqua")
        self.fields["neo_icons"].config(text=sys_info["gtk_icons"] if sys_info["gtk_icons"] else "Mint-Y-Yaru")
        self.fields["neo_shell"].config(text=sys_info["shell"])
        self.fields["neo_term"].config(text=sys_info["terminal"] if sys_info["terminal"] else "gnome-terminal")
        self.fields["neo_pkgs"].config(text=sys_info["packages"])
        
        # Force active recursive mouse wheel bindings propagation across all sub-components elements
        self._bind_mousewheel_recursively(self.scroll_content_frame)

    def _on_canvas_configure(self, event):
        """Forces the inner frame width to dynamically match 100% of the canvas window width."""
        if hasattr(self, 'scroll_content_id') and hasattr(self, 'canvas') and self.canvas.winfo_exists():
            self.canvas.itemconfig(self.scroll_content_id, width=event.width)

    def _on_mousewheel(self, event):
        """Universal scroll execution hook mapped safely to cross-desktop events."""
        if self.winfo_ismapped():
            canvas_height = self.canvas.winfo_height()
            content_height = self.scroll_content_frame.winfo_height()
            if content_height > canvas_height:
                if event.num == 4 or event.delta > 0: 
                    self.canvas.yview_scroll(-1, "units")
                elif event.num == 5 or event.delta < 0: 
                    self.canvas.yview_scroll(1, "units")

    def _bind_mousewheel_recursively(self, widget):
        """PROG: Dynamic walker to bind mouse wheel events to child elements overlays."""
        widget.bind("<MouseWheel>", self._on_mousewheel)
        widget.bind("<Button-4>", self._on_mousewheel)
        widget.bind("<Button-5>", self._on_mousewheel)
        for child in widget.winfo_children():
            self._bind_mousewheel_recursively(child)

    def update_telemetry(self):
        """PROG: REAL-TIME RESPONSIBILITY MATRIX CALIBRATOR ENGINE (SYSTEM LAYER)"""
        if hasattr(self, 'canvas') and self.canvas.winfo_exists():
            self.canvas.update_idletasks()
            canvas_height = self.canvas.winfo_height()
            content_height = self.scroll_content_frame.winfo_height()
            
            if content_height <= canvas_height:
                self.canvas.yview_moveto(0)
                
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))
