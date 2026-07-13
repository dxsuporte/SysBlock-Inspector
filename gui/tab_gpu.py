import tkinter as tk
from gui.base_tab import BaseTab
import core

class GpuTab(BaseTab):
    """
    PROGRAMMER: High-efficiency, 100% Universal Graphics Processing Unit (GPU) component.
    Splits video data tracks into technical specs and real-time hardware loads loops.
    Runs purely raw using native operating system styling context.
    """
    def __init__(self, parent, font_registry):
        super().__init__(parent, font_registry)
        
        # Inject custom geometric wireframes for our new advanced hardware entries
        self.icon_map["Identificadores"] = "⚿" 
        self.icon_map["Barramento"] = "⌗" 
        self.icon_map["Link"] = "▱" 
        self.icon_map["Revisão"] = "⧇" 
        self.icon_map["Frequência"] = "🚀" 
        self.icon_map["Capacidade"] = "⚡" 
        self.icon_map["Memória"] = "▤" 
        
        # 1. PROG: CONSTRUCT SCROLLABLE CANVAS ENGINE INFRASTRUCTURE FOR GPU TAB
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
        
        # Initial layout configurations profiling setup
        gpu_telemetry = core.get_gpu_hardware_telemetry()
        sys_info = core.get_cpu_static_hardware_specs() 
        
        # --- BOX 1: STATIC SPECIFICATIONS (GPU-Z STYLE) ---
        group_specs = self.create_group_box(" ESPECIFICAÇÕES DO CONTROLADOR GRÁFICO ")
        self.append_grid_row(group_specs, "Modelo do Chip de Vídeo (GPU):", "gpu_model")
        self.append_grid_row(group_specs, "Identificadores de Hardware (PCI IDs):", "gpu_pci_ids")
        self.append_grid_row(group_specs, "Endereço do Barramento PCI-Express:", "gpu_pci_bus")
        self.append_grid_row(group_specs, "Link de Conexão Máximo (PCIe Slot):", "gpu_pci_speed")
        self.append_grid_row(group_specs, "Código de Revisão do Silício (Rev ID):", "gpu_revision")
        self.append_grid_row(group_specs, "Driver de Vídeo Ativo no Kernel:", "gpu_driver")
        
        # --- BOX 2: REAL-TIME PERFORMANCE (TASK MANAGER STYLE) ---
        group_perf = self.create_group_box(" DESEMPENHO GRÁFICO EM TEMPO REAL ")
        self.append_grid_row(group_perf, "Frequência de Operação Atual (Clock):", "gpu_cur_clock")
        self.append_grid_row(group_perf, "Frequência Máxima Limite da GPU:", "gpu_max_clock")
        self.append_grid_row(group_perf, "Tipo de Memória de Vídeo (VRAM):", "gpu_vram")
        self.append_grid_row(group_perf, "Quantidade de Monitores Conectados:", "gpu_screens_count")
        self.append_grid_row(group_perf, "Resoluções das Telas Ativas:", "gpu_resolutions")
        
        # Bind hardware permanent strings once
        self.fields["gpu_model"].config(text=gpu_telemetry["model"])
        self.fields["gpu_pci_ids"].config(text=gpu_telemetry["pci_ids"])
        self.fields["gpu_pci_bus"].config(text=gpu_telemetry["pci_bus"])
        self.fields["gpu_pci_speed"].config(text=gpu_telemetry["pci_speed"])
        self.fields["gpu_revision"].config(text=gpu_telemetry["revision"])
        self.fields["gpu_driver"].config(text=gpu_telemetry["driver"])
        self.fields["gpu_resolutions"].config(text=sys_info["resolution"])
        
        # Force recursive mouse wheel bindings propagation across all newly instantiated sub-elements
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
        """PROG: Fires dynamic updating metrics for the multi-manufacturer clocks maps loop."""
        gpu_telemetry = core.get_gpu_hardware_telemetry()
        
        self.fields["gpu_cur_clock"].config(text=gpu_telemetry["cur_clock"])
        self.fields["gpu_max_clock"].config(text=gpu_telemetry["max_clock"])
        self.fields["gpu_vram"].config(text=gpu_telemetry["vram"])
        self.fields["gpu_screens_count"].config(text=gpu_telemetry["screens_count"])
        
        # PROG: REAL-TIME RESPONSIBILITY MATRIX CALIBRATOR ENGINE Layer
        if hasattr(self, 'canvas') and self.canvas.winfo_exists():
            self.canvas.update_idletasks()
            canvas_height = self.canvas.winfo_height()
            content_height = self.scroll_content_frame.winfo_height()
            
            if content_height <= canvas_height:
                self.canvas.yview_moveto(0)
                
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))
