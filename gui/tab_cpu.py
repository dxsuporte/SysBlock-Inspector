import tkinter as tk
from gui.base_tab import BaseTab
import core

class CpuTab(BaseTab):
    """
    PROGRAMMER: High-performance dynamic CPU monitor tab component.
    Combines CPU-Z hardware profile maps with active Task Manager performance threads.
    Runs purely raw using native operating system styling context.
    """
    def __init__(self, parent, font_registry):
        super().__init__(parent, font_registry)
        
        # PROG: Instantiates array pointer cache to manipulate per-core widgets without flickering
        self.dynamic_core_labels = []
        
        # 1. PROG: CONSTRUCT SCROLLABLE CANVAS ENGINE INFRASTRUCTURE FOR CPU TAB
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
        
        # --- BLOCK 1: SPECIFICATIONS (CPU-Z MODEL) ---
        group_cpuz = self.create_group_box(" ESPECIFICAÇÕES DO HARDWARE ")
        
        static_specs = core.get_cpu_static_hardware_specs()
        gov_specs = core.get_cpu_governor_info()
        
        self.append_grid_row(group_cpuz, "Modelo do Processador Detectado:", "model_name")
        self.append_grid_row(group_cpuz, "Quantidade Total de Threads:", "threads_count")
        self.append_grid_row(group_cpuz, "Configuração de Cache L1 | L2 | L3 Mapeado:", "caches_config")
        self.append_grid_row(group_cpuz, "Limites do Clock por Hardware (Mín | Máx):", "clock_limits")
        self.append_grid_row(group_cpuz, "Perfil Energético Ativo (Governador Kernel):", "governor_profile")
        self.append_grid_row(group_cpuz, "Virtualização de Hardware (VT-x / AMD-V):", "vt_state")
        self.append_grid_row(group_cpuz, "Instruções de Extensão Suportadas:", "instruction_flags")
        self.append_grid_row(group_cpuz, "Mitigações de Vulnerabilidade de Silício:", "security_mitigations")
        
        # Populate static non-updating architectural fields straight away on initialization
        self.fields["model_name"].config(text=static_specs["model"])
        self.fields["threads_count"].config(text=static_specs["cores"])
        self.fields["caches_config"].config(text=f"{static_specs['cache_l1']} | {static_specs['cache_l2']} | {static_specs['cache_l3']}")
        self.fields["clock_limits"].config(text=f"{gov_specs['min_clock']} e {gov_specs['max_clock']}")
        self.fields["governor_profile"].config(text=gov_specs["governor"])
        self.fields["instruction_flags"].config(text=core.get_cpu_instructions_flags())
        self.fields["security_mitigations"].config(text=static_specs["mitigations"])
        
        # Native conditional coloring logic execution for hardware virtualization validation
        if "vt_state" in self.fields:
            if "Habilitado" in static_specs["vt_x"]:
                self.fields["vt_state"].config(text=static_specs["vt_x"], fg="#2e7d32")
            else:
                self.fields["vt_state"].config(text=static_specs["vt_x"], fg="#ff3333")
                
        # --- BLOCK 2: GERENCIADOR DE TAREFAS (PERFORMANCE LIVES) ---
        self.group_taskman = self.create_group_box(" DESEMPENHO EM TEMPO REAL ")
        
        self.append_grid_row(self.group_taskman, "Capacidade de Uso Geral da CPU:", "cpu_usage_pct")
        self.append_grid_row(self.group_taskman, "Temperatura de Operação do Silício:", "cpu_temp_val")
        self.append_grid_row(self.group_taskman, "Média de Carga do Escalonador (1 | 5 | 15 min):", "cpu_load_avg")
        self.append_grid_row(self.group_taskman, "Interrupções de Hardware por segundo:", "cpu_interrupts")
        self.append_grid_row(self.group_taskman, "Tempo de Atividade do Sistema (Uptime):", "sys_uptime")
        self.append_grid_row(self.group_taskman, "Forks de Processos e Tarefas do Kernel:", "cpu_tasks_metrics")
        
        # Force recursive mouse wheel bindings propagation across all newly instantiated elements
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
        """Executes targeted runtime updating streams every single iteration cycle loop."""
        self.fields["cpu_usage_pct"].config(text=core.get_cpu_usage())
        self.fields["cpu_temp_val"].config(text=core.get_cpu_temperature())
        self.fields["cpu_load_avg"].config(text=core.get_cpu_load_average())
        self.fields["cpu_interrupts"].config(text=core.get_cpu_interrupts_per_second())
        self.fields["sys_uptime"].config(text=core.get_system_uptime())
        self.fields["cpu_tasks_metrics"].config(text=core.get_cpu_fork_and_tasks_metrics())
        
        # PROG: Parse core array string clocks maps and update without element destructions
        core_rows_data = core.get_per_core_clocks()
        
        for idx, row_text in enumerate(core_rows_data):
            if idx < len(self.dynamic_core_labels):
                self.dynamic_core_labels[idx].config(text=row_text)
            else:
                f_row = tk.Frame(self.group_taskman)
                f_row.pack(fill="x", padx=15, pady=2)
                
                lbl_t = tk.Label(f_row, text=f"Clocks da CPU (Linha {idx+1}):", font=self.fonts["label"])
                lbl_t.pack(side="left", anchor="w")
                
                lbl_v = tk.Label(f_row, text=row_text, font=self.fonts["monospace"])
                lbl_v.pack(side="right", anchor="e")
                
                self._bind_mousewheel_recursively(f_row)
                self.dynamic_core_labels.append(lbl_v)
                
        # PROG: REAL-TIME RESPONSIBILITY MATRIX CALIBRATOR ENGINE (CPU LAYER)
        if hasattr(self, 'canvas') and self.canvas.winfo_exists():
            self.canvas.update_idletasks()
            canvas_height = self.canvas.winfo_height()
            content_height = self.scroll_content_frame.winfo_height()
            
            if content_height <= canvas_height:
                self.canvas.yview_moveto(0)
                
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))
