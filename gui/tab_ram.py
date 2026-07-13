import tkinter as tk
from gui.base_tab import BaseTab
import core

class RamTab(BaseTab):
    """
    PROGRAMMER: High-efficiency RAM telemetry component. 
    Inherits row and group generation methods from BaseTab.
    Runs purely raw using native operating system styling context.
    """
    def __init__(self, parent, font_registry):
        super().__init__(parent, font_registry)
        
        # Inject extra unicode icon maps for our advanced memory profile slots
        self.icon_map["Porcentagem"] = "☱" 
        self.icon_map["Espaço"] = "▤" 
        self.icon_map["Slots"] = "⌗" 
        self.icon_map["Módulo"] = "❑" 
        
        # 1. PROG: CONSTRUCT SCROLLABLE CANVAS ENGINE INFRASTRUCTURE FOR RAM TAB
        self.canvas = tk.Canvas(self, bd=0, highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scroll_content_frame = tk.Frame(self.canvas)
        
        self.scroll_content_id = self.canvas.create_window((0, 0), window=self.scroll_content_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        self.canvas.bind("<Configure>", self._on_canvas_configure)
        self.bind("<MouseWheel>", self._on_mousewheel)
        self.bind("<Button-4>", self._on_mousewheel) 
        self.bind("<Button-5>", self._on_mousewheel) 
        
        # --- BOX 1: Main RAM Volume Allocation Box Group ---
        group_ram = self.create_group_box(" TELEMETRIA DE VOLUMES E ALOCAÇÃO DA RAM ")
        self.append_grid_row(group_ram, "Porcentagem de Consumo de RAM Atual:", "ram_usage_pct")
        self.append_grid_row(group_ram, "Espaço Físico Alocado / Total Disponível:", "ram_memory_txt")
        
        # --- BOX 2: ADVANCED INDIVIDUAL SOCKETS MAP (SLOT BY SLOT) ---
        self.group_hw = self.create_group_box(" MAPEAMENTO DE SLOTS DA PLACA-MÃE (DMI/SMBIOS) ")
        self.append_grid_row(self.group_hw, "Slots de Memória Ocupados no Hardware:", "ram_hw_slots_summary")
        
        # --- BOX 3: Advanced Linux Kernel Memory Profiles Box Group ---
        group_advanced = self.create_group_box(" CACHE DE KERNEL E ÁREA DE TROCA (SWAP) ")
        self.append_grid_row(group_advanced, "Área de Troca Ativa do Linux (Swap Alocado):", "swap_usage_txt")
        self.append_grid_row(group_advanced, "Memória em Cache de Disco (Buffers/Cached):", "ram_cached_txt")
        
        # Hydrate initial layout configurations for structural hardware profiles
        hw_report = core.get_ram_hardware_hardware_specs() if hasattr(core, 'get_ram_hardware_hardware_specs') else {"slots_used":0, "slots_total":0, "devices":[]}
        self.fields["ram_hw_slots_summary"].config(text=f"{hw_report['slots_used']} de {hw_report['slots_total']} slots ocupados")
        
        # Dynamically append separate row cards for every single hardware slot mapping trace
        import uuid
        for dev in hw_report.get("devices", []):
            row_f = tk.Frame(self.group_hw)
            row_f.pack(fill="x", expand=True, padx=15, pady=3)
            if hasattr(self, 'row_frames'): 
                self.row_frames.append(row_f)
            
            lbl_title = tk.Label(row_f, text=f" ❑ Encaixe [{dev['slot']}]:", font=self.fonts["label"])
            lbl_title.pack(side="left", anchor="w")
            if hasattr(self, 'name_labels'): 
                self.name_labels.append(lbl_title)
            
            if dev["size"] == "Vazio":
                val_text = "Slot Vazio (Disponível para Upgrade)"
            else:
                val_text = f"{dev['size']} | {dev['type']} | {dev['speed']} | {dev['vendor']} ({dev['form']})"
            
            lbl_value = tk.Label(row_f, text=val_text, font=self.fonts["monospace"])
            lbl_value.pack(side="right", anchor="e")
            self.fields[str(uuid.uuid4())] = lbl_value
            
        self._bind_mousewheel_recursively(self.scroll_content_frame)

    def _on_canvas_configure(self, event):
        if hasattr(self, 'scroll_content_id') and hasattr(self, 'canvas') and self.canvas.winfo_exists():
            self.canvas.itemconfig(self.scroll_content_id, width=event.width)

    def _on_mousewheel(self, event):
        if self.winfo_ismapped():
            canvas_height = self.canvas.winfo_height()
            content_height = self.scroll_content_frame.winfo_height()
            if content_height > canvas_height:
                if event.num == 4 or event.delta > 0: 
                    self.canvas.yview_scroll(-1, "units")
                elif event.num == 5 or event.delta < 0: 
                    self.canvas.yview_scroll(1, "units")

    def _bind_mousewheel_recursively(self, widget):
        widget.bind("<MouseWheel>", self._on_mousewheel)
        widget.bind("<Button-4>", self._on_mousewheel)
        widget.bind("<Button-5>", self._on_mousewheel)
        for child in widget.winfo_children(): 
            self._bind_mousewheel_recursively(child)

    def update_telemetry(self):
        """Refreshes memory tracks from meminfo directly into the bound base layout labels."""
        try:
            mem_data = {}
            with open("/proc/meminfo", "r") as f:
                for line in f:
                    parts = line.split()
                    if len(parts) >= 2:
                        key_name = parts[0].replace(":", "").strip()
                        mem_data[key_name] = int(parts[1])
            
            # 1. Update Physical Ram tracks
            mem_total = mem_data.get("MemTotal", 0)
            mem_free = mem_data.get("MemFree", 0)
            mem_avail = mem_data.get("MemAvailable", mem_free)
            
            if mem_total > 0:
                ram_used_kb = mem_total - mem_avail
                ram_used_gb = ram_used_kb / 1024 / 1024
                ram_total_gb = mem_total / 1024 / 1024
                ram_pct = int((ram_used_kb / mem_total) * 100)
                
                pct_text = f"{ram_pct}%"
                memory_text = f"{ram_used_gb:.1f} GB / {ram_total_gb:.1f} GB"
            else:
                pct_text = "N/A"; memory_text = "N/A"
            
            # 2. Update Virtual Swap tracks
            swap_total = mem_data.get("SwapTotal", 0)
            swap_free = mem_data.get("SwapFree", 0)
            if swap_total > 0:
                swap_used_gb = (swap_total - swap_free) / 1024 / 1024
                swap_total_gb = swap_total / 1024 / 1024
                swap_text = f"{swap_used_gb:.1f} GB / {swap_total_gb:.0f} GB"
            else:
                swap_text = "Inativo (Sem partição Swap)"
            
            # 3. Update Disk Caches
            buffers = mem_data.get("Buffers", 0)
            cached = mem_data.get("Cached", 0)
            sreclaimable = mem_data.get("SReclaimable", 0)
            total_cache_gb = (buffers + cached + sreclaimable) / 1024 / 1024
            cache_text = f"{total_cache_gb:.2f} GB"
        
        except Exception:
            pct_text = "N/A"; memory_text = "N/A"; swap_text = "N/A"; cache_text = "N/A"
        
        self.fields["ram_usage_pct"].config(text=pct_text)
        self.fields["ram_memory_txt"].config(text=memory_text)
        self.fields["swap_usage_txt"].config(text=swap_text)
        self.fields["ram_cached_txt"].config(text=cache_text)
        
        # PROG: REAL-TIME RESPONSIBILITY MATRIX CALIBRATOR ENGINE (RAM LAYER)
        if hasattr(self, 'canvas') and self.canvas.winfo_exists():
            self.canvas.update_idletasks()
            canvas_height = self.canvas.winfo_height()
            content_height = self.scroll_content_frame.winfo_height()
            
            if content_height <= canvas_height:
                self.canvas.yview_moveto(0)
                
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))
