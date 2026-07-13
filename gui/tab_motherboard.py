import tkinter as tk
from gui.base_tab import BaseTab
import core

class MotherboardTab(BaseTab):
    """
    PROGRAMMER: High-efficiency Motherboard and System Firmware telemetry component.
    Inherits row and group generation methods from BaseTab.
    Fully optimized with active main loop scrollregion calculations to prevent layout freezes.
    """
    def __init__(self, parent, font_registry):
        super().__init__(parent, font_registry)

        # Inject extra unicode icon maps for our advanced motherboard profiles
        self.icon_map["Placa-Mãe"] = "🔌"      
        self.icon_map["Modelo"] = "❑"         
        self.icon_map["Revisão"] = "⧇"        
        self.icon_map["Série"] = "⚿"          
        self.icon_map["Fabricante"] = "🛠"     
        self.icon_map["BIOS"] = "💾"          
        self.icon_map["Versão"] = "⎋"         
        self.icon_map["Data"] = "📅"          
        self.icon_map["Produto"] = "📦"        
        self.icon_map["Limite"] = "▤"         
        self.icon_map["Soquete"] = "⚙"        
        self.icon_map["Slots"] = "🚀"         
        self.icon_map["Encaixes"] = "⌗"       
        self.icon_map["Modo"] = "🔑"         
        self.icon_map["Inicialização"] = "🛡" 
        self.icon_map["Módulo"] = "🔒"        
        self.icon_map["Controlador"] = "🎛"   # Novo ícone de Chipset
        self.icon_map["Interface"] = "🔊"     # Novo ícone de Áudio

        # 1. PROG: CONSTRUCT SCROLLABLE CANVAS ENGINE INFRASTRUCTURE FOR MOTHERBOARD TAB
        self.canvas = tk.Canvas(self, bd=0, highlightthickness=0, bg="#1a1a1a")
        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scroll_content_frame = tk.Frame(self.canvas, bg="#1a1a1a")
        
        self.scroll_content_id = self.canvas.create_window((0, 0), window=self.scroll_content_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        self.canvas.bind("<Configure>", self._on_canvas_configure)
        self.bind("<MouseWheel>", self._on_mousewheel)
        self.bind("<Button-4>", self._on_mousewheel) 
        self.bind("<Button-5>", self._on_mousewheel) 
        
        # Centralized metadata fetch execution
        board_specs = core.get_motherboard_hardware_specs()

        # --- BOX 1: MAIN PLACA-MÃE HARDWARE INFORMATION ---
        group_board = self.create_group_box(" PLACA-MÃE (BASEBOARD HARDWARE SPECIFICATIONS) ", target_parent=self.scroll_content_frame)
        self.append_grid_row(group_board, "Fabricante da Placa-Mãe (Vendor):", "mb_vendor", text_color="#ffffff")
        self.append_grid_row(group_board, "Modelo Comercial da Placa (Product):", "mb_name", text_color="#ffffff")
        self.append_grid_row(group_board, "Revisão Física do Projeto (Version):", "mb_version", text_color="#ffffff")
        self.append_grid_row(group_board, "Número de Série de Fábrica (Serial ID):", "mb_serial", text_color="#ffffff")

        # --- BOX 2: FIRMWARE BIOS TELEMETRY ---
        group_bios = self.create_group_box(" CONFIGURAÇÕES DE FIRMWARE DO CHIP DE BIOS ", border_color="#9cdcfe", target_parent=self.scroll_content_frame)
        self.append_grid_row(group_bios, "Desenvolvedora do Software da BIOS:", "mb_bios_vendor", text_color="#ffffff")
        self.append_grid_row(group_bios, "Versão do Firmware Ativo (BIOS Build):", "mb_bios_version", text_color="#ffffff")
        self.append_grid_row(group_bios, "Data de Lançamento da Compilação:", "mb_bios_date", text_color="#ffffff")

        # --- BOX 3: CHIPSET INFRASTRUCTURE LIMITS (EXPANDED WITH lspci NODES) ---
        group_limits = self.create_group_box(" CAPACIDADE DO CHIPSET E EXPANSÕES DE EXPANSÃO ", border_color="#555555", target_parent=self.scroll_content_frame)
        self.append_grid_row(group_limits, "Controlador do Chipset da Placa (PCH):", "mb_chipset_pci", text_color="#ffffff") # NOVO
        self.append_grid_row(group_limits, "Interface Integrada de Áudio (Codec):", "mb_audio_pci", text_color="#ffffff")   # NOVO
        self.append_grid_row(group_limits, "Limite Máximo de RAM Suportado (Chipset):", "mb_max_ram", text_color="#ffffff")
        self.append_grid_row(group_limits, "Encaixes Físicos de Slots de RAM Instalados:", "mb_ram_slots", text_color="#ffffff")
        self.append_grid_row(group_limits, "Soquete Físico de Interface do Processador:", "mb_cpu_socket", text_color="#ffffff")
        self.append_grid_row(group_limits, "Slots PCI-Express Livres e Ocupados:", "mb_pcie_slots", text_color="#ffffff")

        # --- BOX 4: FIRMWARE SECURITY MATRIX ---
        group_security = self.create_group_box(" DIRETRIZES DE SEGURANÇA E INICIALIZAÇÃO DO SISTEMA ", border_color="#ff3333", target_parent=self.scroll_content_frame)
        self.append_grid_row(group_security, "Modo de Inicialização de Firmware (Boot Type):", "mb_boot_mode", text_color="#ffffff")
        self.append_grid_row(group_security, "Inicialização de Segurança (Secure Boot):", "mb_secure_boot")
        self.append_grid_row(group_security, "Módulo de Plataforma Confiável (Chip TPM):", "mb_tpm_state")

        # --- BOX 5: INTEGRATED COMPUTER SYSTEM PROFILE ---
        group_sys = self.create_group_box(" PERFIL DE SISTEMA DE PRODUTO INTEGRADO ", border_color="#777777", target_parent=self.scroll_content_frame)
        self.append_grid_row(group_sys, "Fabricante do Computador Completo:", "mb_sys_vendor", text_color="#ffffff")
        self.append_grid_row(group_sys, "Modelo Comercial da Máscara do Produto:", "mb_sys_product", text_color="#ffffff")

        # Hydrate all extracted hardware strings straight away into fields references pointers
        self.fields["mb_vendor"].config(text=board_specs["board_vendor"])
        self.fields["mb_name"].config(text=board_specs["board_name"])
        self.fields["mb_version"].config(text=board_specs["board_version"])
        self.fields["mb_serial"].config(text=board_specs["board_serial"])
        
        self.fields["mb_bios_vendor"].config(text=board_specs["bios_vendor"])
        self.fields["mb_bios_version"].config(text=board_specs["bios_version"])
        self.fields["mb_bios_date"].config(text=board_specs["bios_date"])
        
        self.fields["mb_chipset_pci"].config(text=board_specs["chipset_pci"]) # NOVO
        self.fields["mb_audio_pci"].config(text=board_specs["audio_pci"])     # NOVO
        self.fields["mb_max_ram"].config(text=board_specs["max_ram_capacity"])
        self.fields["mb_ram_slots"].config(text=board_specs["ram_slots_count"])
        self.fields["mb_cpu_socket"].config(text=board_specs["cpu_socket"])
        self.fields["mb_pcie_slots"].config(text=board_specs["pcie_slots_summary"])
        
        self.fields["mb_boot_mode"].config(text=board_specs["boot_mode"])
        
        if "Ativado" in board_specs["secure_boot"]:
            self.fields["mb_secure_boot"].config(text=board_specs["secure_boot"], fg="#4cbd5a")
        else:
            self.fields["mb_secure_boot"].config(text=board_specs["secure_boot"], fg="#aaaaaa")
            
        if "Ativado" in board_specs["tpm_state"]:
            self.fields["mb_tpm_state"].config(text=board_specs["tpm_state"], fg="#4cbd5a")
        else:
            self.fields["mb_tpm_state"].config(text=board_specs["tpm_state"], fg="#ff3333")
        
        self.fields["mb_sys_vendor"].config(text=board_specs["sys_vendor"])
        self.fields["mb_sys_product"].config(text=board_specs["sys_product"])

        self._bind_mousewheel_recursively(self.scroll_content_frame)

    def _on_canvas_configure(self, event):
        if hasattr(self, 'scroll_content_id') and hasattr(self, 'canvas') and self.canvas.winfo_exists():
            self.canvas.itemconfig(self.scroll_content_id, width=event.width)

    def _on_mousewheel(self, event):
        if self.winfo_ismapped():
            canvas_height = self.canvas.winfo_height()
            content_height = self.scroll_content_frame.winfo_height()
            if content_height > canvas_height:
                if event.num == 4 or event.delta > 0: self.canvas.yview_scroll(-1, "units")
                elif event.num == 5 or event.delta < 0: self.canvas.yview_scroll(1, "units")

    def _bind_mousewheel_recursively(self, widget):
        widget.bind("<MouseWheel>", self._on_mousewheel)
        widget.bind("<Button-4>", self._on_mousewheel)
        widget.bind("<Button-5>", self._on_mousewheel)
        for child in widget.winfo_children(): self._bind_mousewheel_recursively(child)

    def apply_theme_colors(self, colors):
        super().apply_theme_colors(colors)
        if hasattr(self, 'canvas') and self.canvas.winfo_exists():
            self.canvas.config(bg=colors["bg_root"])
            self.scroll_content_frame.config(bg=colors["bg_root"])
            self.scrollbar.config(bg=colors["bg_root"])

    def create_group_box(self, title_text, border_color="#555555", target_parent=None):
        parent_node = target_parent if target_parent else self
        box = tk.LabelFrame(parent_node, text=title_text, font=self.fonts["section"], bg="#2d2d2d", fg="#ffffff", bd=1, relief="solid")
        box.pack(fill="x", padx=15, pady=(5, 10), ipady=5)
        if hasattr(self, 'card_frames'): self.card_frames.append(box)
        else:
            if not hasattr(self, '_local_card_frames_cache'): self._local_card_frames_cache = []
            self._local_card_frames_cache.append(box)
        return box

    def update_telemetry(self):
        """Motherboard profiles are purely static, we only trigger layout safety canvas configurations loops."""
        if hasattr(self, 'canvas') and self.canvas.winfo_exists():
            self.canvas.update_idletasks()
            canvas_height = self.canvas.winfo_height()
            content_height = self.scroll_content_frame.winfo_height()
            
            if content_height <= canvas_height:
                self.canvas.yview_moveto(0)
                
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))

