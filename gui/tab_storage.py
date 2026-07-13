import tkinter as tk
from gui.base_tab import BaseTab
import core
import uuid

class StorageTab(BaseTab):
    """
    PROGRAMMER: High-efficiency Multi-Drive Storage telemetry component.
    Implements a responsive vertical Canvas scrollbar with dynamic internal sub-partitions listings.
    Runs purely raw using native operating system styling context.
    """
    def __init__(self, parent, font_registry, has_smartctl, has_nvme):
        super().__init__(parent, font_registry)
        self.has_smartctl = has_smartctl
        self.has_nvme = has_nvme
        
        # Inject standard geometric wireframe tokens to match our advanced storage rows
        self.icon_map["Mídia"] = "❑" 
        self.icon_map["Comercial"] = "⧈" 
        self.icon_map["Série"] = "⚿" 
        self.icon_map["Temperatura"] = "🌡" 
        self.icon_map["Saúde"] = "🛡" 
        self.icon_map["Capacidade"] = "▤" 
        self.icon_map["Partição"] = "⌗" 
        
        # 1. PROG: CONSTRUCT SCROLLABLE CANVAS ENGINE INFRASTRUCTURE FOR STORAGE TAB
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
        
        self.storage_frames_cache = {}
        self.dynamic_name_labels = []

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
        """Maintains clean multi-drive partition streams natively without layouts destruction loops."""
        storage_data = core.detect_and_read_storage_devices(self.has_smartctl, self.has_nvme)
        
        # Prune dead hot-unplugged media blocks nodes safely
        for cached_dev in list(self.storage_frames_cache.keys()):
            if cached_dev not in storage_data:
                self.storage_frames_cache[cached_dev].destroy()
                del self.storage_frames_cache[cached_dev]
                
        # Dynamically append or update card blocks packages loops
        for dev, metrics in storage_data.items():
            h_val = metrics["health_value"]
            
            # --- VERIFICAÇÃO ESTREITA E PRE CISA: Acende vermelho para qualquer defeito real ---
            if "nvme" in dev:
                try:
                    pct = int(h_val.split("%")[0].strip())
                    health_color = "#ff3333" if pct > 10 else "#1b5e20"
                except Exception: health_color = "#1b5e20"
            else:
                try:
                    # Isola o número de setores realocados (antes da barra /)
                    raw_sectors = h_val.split("/")[0].strip()
                    bad_sectors_count = int(raw_sectors)
                    
                    # SE HAVER SINAL DE ALERTA: Se houver mais de 0 setores danificados, acende o vermelho de falha!
                    if bad_sectors_count > 0:
                        health_color = "#ff3333" # Alerta vermelho máximo na tela
                    else:
                        health_color = "#1b5e20" # Verde escuro corporativo para discos perfeitos
                except Exception:
                    health_color = "#ff3333" if "saudável" not in h_val.lower() else "#1b5e20"

                
            if dev in self.storage_frames_cache:
                card = self.storage_frames_cache[dev]
                card.lbl_type.config(text=metrics["type"])
                card.lbl_model.config(text=metrics["brand_model"])
                card.lbl_serial.config(text=metrics["serial"])
                card.lbl_temp.config(text=metrics["temp"])
                card.lbl_health_title.config(text=f" 🛡 Saúde ({metrics['health_label']})")
                card.lbl_health_val.config(text=h_val, fg=health_color)
                card.lbl_total.config(text=metrics["total_space"])
                
                # Dynamic update stream loop targeting partitions fields arrays references pointers
                for p_idx, p_data in enumerate(metrics["partitions"]):
                    if p_idx < len(card.part_rows_cache):
                        row_lbls = card.part_rows_cache[p_idx]
                        row_lbls["title"].config(text=f" ⌗ Partição [{p_data['part_node']} | {p_data['format']}]:")
                        row_lbls["val"].config(text=f"Usado: {p_data['used']} | Livre: {p_data['free']} | Total: {p_data['size']} ({p_data['percent']})")
            else:
                # Instantiate a clean structured LabelFrame container card inside the scrolling viewport
                group_card = self.create_group_box(f" UNIDADE DE ARMAZENAMENTO: [/dev/{dev}] ")
                
                # Hardware Specs rows packing layouts
                group_card.lbl_type = self.append_grid_row(group_card, "Mídia de Armazenamento Detectada:", f"gpu_type_{dev}")
                group_card.lbl_model = self.append_grid_row(group_card, "Modelo Comercial / Fabricante:", f"gpu_model_{dev}")
                group_card.lbl_serial = self.append_grid_row(group_card, "Número de Série de Fábrica:", f"gpu_serial_{dev}")
                group_card.lbl_temp = self.append_grid_row(group_card, "Temperatura de Operação do Disco:", f"gpu_temp_{dev}")
                
                # Health row split setup to safely intercept custom text dynamic mutations titles
                row_h = tk.Frame(group_card)
                row_h.pack(fill="x", expand=True, padx=15, pady=3)
                if hasattr(self, 'row_frames'): 
                    self.row_frames.append(row_h)
                
                group_card.lbl_health_title = tk.Label(row_h, text=f" 🛡 Saúde ({metrics['health_label']})", font=self.fonts["label"])
                group_card.lbl_health_title.pack(side="left", anchor="w")
                if hasattr(self, 'name_labels'): 
                    self.name_labels.append(group_card.lbl_health_title)
                self.dynamic_name_labels.append(group_card.lbl_health_title)
                
                group_card.lbl_health_val = tk.Label(row_h, text="Carregando...", font=self.fonts["monospace"], fg=health_color)
                group_card.lbl_health_val.pack(side="right", anchor="e")
                self.fields[str(uuid.uuid4())] = group_card.lbl_health_val
                
                group_card.lbl_total = self.append_grid_row(group_card, "Capacidade Total Física (Tamanho):", f"gpu_total_{dev}")
                
                # PROG: PARTITIONS LISTINGS STREAM GENERATOR
                group_card.part_rows_cache = []
                for p_idx, p_data in enumerate(metrics["partitions"]):
                    row_p_frame = tk.Frame(group_card)
                    
                    # FIX DE ESPAÇAMENTO: Se for a última partição da lista, injeta um pady inferior de 12 para não cortar o texto
                    is_last = (p_idx == len(metrics["partitions"]) - 1)
                    p_bottom_pad = 12 if is_last else 3
                    row_p_frame.pack(fill="x", expand=True, padx=15, pady=(3, p_bottom_pad))
                    
                    if hasattr(self, 'row_frames'): 
                        self.row_frames.append(row_p_frame)
                    
                    p_title_lbl = tk.Label(row_p_frame, text=f" ⌗ Partição [{p_data['part_node']} | {p_data['format']}]:", font=self.fonts["label"])
                    p_title_lbl.pack(side="left", anchor="w")
                    if hasattr(self, 'name_labels'): 
                        self.name_labels.append(p_title_lbl)
                    self.dynamic_name_labels.append(p_title_lbl)
                    
                    p_val_lbl = tk.Label(row_p_frame, text=f"Usado: {p_data['used']} | Livre: {p_data['free']} | Total: {p_data['size']} ({p_data['percent']})", font=self.fonts["monospace"])
                    p_val_lbl.pack(side="right", anchor="e")
                    
                    self.fields[str(uuid.uuid4())] = p_val_lbl
                    group_card.part_rows_cache.append({"title": p_title_lbl, "val": p_val_lbl})
                    
                # Hydrate raw static attributes data values straight away
                group_card.lbl_type.config(text=metrics["type"])
                group_card.lbl_model.config(text=metrics["brand_model"])
                group_card.lbl_serial.config(text=metrics["serial"])
                group_card.lbl_temp.config(text=metrics["temp"])
                group_card.lbl_health_val.config(text=h_val)
                group_card.lbl_total.config(text=metrics["total_space"])
                
                # Force active recursive mouse propagation trigger directly on newly built cards
                self._bind_mousewheel_recursively(group_card)
                self.storage_frames_cache[dev] = group_card
                
        # PROG: REAL-TIME RESPONSIBILITY MATRIX CALIBRATOR ENGINE (STORAGE LAYER)
        if hasattr(self, 'canvas') and self.canvas.winfo_exists():
            self.canvas.update_idletasks()
            canvas_height = self.canvas.winfo_height()
            content_height = self.scroll_content_frame.winfo_height()
            
            if content_height <= canvas_height:
                self.canvas.yview_moveto(0)
                
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))

