import tkinter as tk
from gui.base_tab import BaseTab
import core

class NetworkTab(BaseTab):
    """
    PROGRAMMER: High-efficiency Multi-Interface POSIX compliant Network component.
    Dynamically tracks and allocates isolated panels for ALL network adapters.
    Runs purely raw using native operating system styling context.
    """
    def __init__(self, parent, font_registry):
        super().__init__(parent, font_registry)
        
        # Inject standard geometric wireframe tokens to match our advanced network entries
        self.icon_map["Placa"] = "⌗" 
        self.icon_map["Identificador"] = "⧇" 
        self.icon_map["MAC"] = "⚿"
        self.icon_map["Físico"] = "⚿"
        self.icon_map["Endereço"] = "🌐" 
        self.icon_map["Máscara"] = "▱" 
        self.icon_map["Roteador"] = "▤" 
        self.icon_map["Gateway"] = "▤" 
        self.icon_map["Servidores"] = "⌺" 
        self.icon_map["Velocidade"] = "⚡" 
        self.icon_map["Sincronismo"] = "⚡"
        self.icon_map["Latência"] = "⏱" 
        self.icon_map["Taxa"] = "❯" 
        self.icon_map["Fluxo"] = "❯" 
        self.icon_map["Status"] = "⚙" 
        
        # 1. PROG: CONSTRUCT SCROLLABLE CANVAS ENGINE INFRASTRUCTURE FOR NETWORK TAB
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
        
        self.network_cards_cache = {}
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
        """Maintains clean multi-interface loop streams natively without layout destructions or crashes."""
        try:
            net_data = core.get_network_hardware_telemetry()
        except Exception as e:
            print(f"[Core Net Read Error]: {e}")
            return
        
        # 1. Cache pruning algorithm to safely eliminate disconnected hardware
        for cached_iface in list(self.network_cards_cache.keys()):
            if cached_iface not in net_data:
                self.network_cards_cache[cached_iface].destroy()
                del self.network_cards_cache[cached_iface]
                
        # 2. Build or re-use card widgets seamlessly via dictionary maps lookups
        for iface, metrics in net_data.items():
            status_color = "#2e7d32" if metrics.get("status") == "Conectado" else "#ff3333"
            latency_color = "#ff3333" if "Falha" in metrics.get("latency", "") else ""
            
            if iface in self.network_cards_cache:
                card = self.network_cards_cache[iface]
                
                # EXECUÇÃO BLINDADA: Atualiza as labels puxando direto pelo dicionário de referências locais do cartão
                try: card.lbl_refs["status"].config(text=metrics.get("status", "N/A"), fg=status_color)
                except Exception: pass
                
                try: card.lbl_refs["hostname"].config(text=metrics.get("hostname", "N/A"))
                except Exception: pass
                
                try: card.lbl_refs["mac"].config(text=metrics.get("mac", "N/A"))
                except Exception: pass
                
                try: card.lbl_refs["ip"].config(text=metrics.get("ip", "N/A"))
                except Exception: pass
                
                try: card.lbl_refs["netmask"].config(text=metrics.get("netmask", "N/A"))
                except Exception: pass
                
                try: card.lbl_refs["gateway"].config(text=metrics.get("gateway", "N/A"))
                except Exception: pass
                
                try: card.lbl_refs["dns"].config(text=metrics.get("dns", "N/A"))
                except Exception: pass
                
                try: card.lbl_refs["speed"].config(text=metrics.get("speed", "N/A"))
                except Exception: pass
                
                try:
                    # Captura diretamente a chave oficial 'latency' gerada na página 14 do seu core.py
                    actual_ping = metrics.get("latency", "N/A")
                    
                    if latency_color:
                        card.lbl_refs["latency"].config(text=actual_ping, fg=latency_color)
                    else:
                        card.lbl_refs["latency"].config(text=actual_ping, fg="")
                except Exception: pass
                
                try: card.lbl_refs["down"].config(text=metrics.get("download", "N/A"))
                except Exception: pass
                
                try: card.lbl_refs["up"].config(text=metrics.get("upload", "N/A"))
                except Exception: pass
            else:
                # Instantiate a clean structured LabelFrame container card inside the scrolling viewport
                group_card = tk.LabelFrame(self.scroll_content_frame, text=f" INTERFACE: {metrics.get('name', iface)} ", font=self.fonts["section"])
                group_card.pack(fill="x", padx=15, pady=(5, 10), ipady=5)
                
                # CRITICAL MAP: Inicializa o dicionário de ancoragem para dar persistência na memória RAM
                group_card.lbl_refs = {}
                
                # Build granular lines layout layers arrays manually e guarda as referências no mapa fixo
                group_card.lbl_refs["status"] = self._append_local_row(group_card, "Status da Conexão Externa:", status_color)
                group_card.lbl_refs["hostname"] = self._append_local_row(group_card, "Identificador de Rede (Hostname):")
                group_card.lbl_refs["mac"] = self._append_local_row(group_card, "Endereço MAC Físico (Hardware ID):")
                group_card.lbl_refs["ip"] = self._append_local_row(group_card, "Endereço IP Local (IPv4 Address):")
                group_card.lbl_refs["netmask"] = self._append_local_row(group_card, "Máscara de Sub-rede (Netmask):")
                group_card.lbl_refs["gateway"] = self._append_local_row(group_card, "Roteador Padrão da Rede (Gateway):")
                group_card.lbl_refs["dns"] = self._append_local_row(group_card, "Servidores de Nomes Ativos (DNS):")
                group_card.lbl_refs["speed"] = self._append_local_row(group_card, "Velocidade de Sincronismo do Link:")
                group_card.lbl_refs["latency"] = self._append_local_row(group_card, "Latência de Resposta (Ping):")
                group_card.lbl_refs["down"] = self._append_local_row(group_card, "Taxa de Download Atual:")
                group_card.lbl_refs["up"] = self._append_local_row(group_card, "Fluxo de Upload Atual:")
                
                # Hidrata os dados imediatamente no nascimento do card
                try: group_card.lbl_refs["status"].config(text=metrics.get("status", "N/A"), fg=status_color)
                except Exception: pass
                try: group_card.lbl_refs["hostname"].config(text=metrics.get("hostname", "N/A"))
                except Exception: pass
                try: group_card.lbl_refs["mac"].config(text=metrics.get("mac", "N/A"))
                except Exception: pass
                try: group_card.lbl_refs["ip"].config(text=metrics.get("ip", "N/A"))
                except Exception: pass
                try: group_card.lbl_refs["netmask"].config(text=metrics.get("netmask", "N/A"))
                except Exception: pass
                try: group_card.lbl_refs["gateway"].config(text=metrics.get("gateway", "N/A"))
                except Exception: pass
                try: group_card.lbl_refs["dns"].config(text=metrics.get("dns", "N/A"))
                except Exception: pass
                try: group_card.lbl_refs["speed"].config(text=metrics.get("speed", "N/A"))
                except Exception: pass
                try: group_card.lbl_refs["latency"].config(text=metrics.get("latency", "N/A"))
                except Exception: pass
                try: group_card.lbl_refs["down"].config(text=metrics.get("download", "N/A"))
                except Exception: pass
                try: group_card.lbl_refs["up"].config(text=metrics.get("upload", "N/A"))
                except Exception: pass

                # Force active recursive mouse propagation trigger directly on newly built network cards
                self._bind_mousewheel_recursively(group_card)
                
                # Bind dynamic reference link straight to master context frame
                self.network_cards_cache[iface] = group_card
                
        # PROG: REAL-TIME RESPONSIBILITY MATRIX CALIBRATOR ENGINE (NETWORK LAYER)
        if hasattr(self, 'canvas') and self.canvas.winfo_exists():
            self.canvas.update_idletasks()
            canvas_height = self.canvas.winfo_height()
            content_height = self.scroll_content_frame.winfo_height()
            
            if content_height <= canvas_height:
                self.canvas.yview_moveto(0)
                
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _append_local_row(self, container_box, row_title, text_color=""):
        """Internal helper to construct monochromatic row layers with auto icon matching."""
        row_frame = tk.Frame(container_box)
        row_frame.pack(fill="x", expand=True, padx=15, pady=3)
        if hasattr(self, 'row_frames'): 
            self.row_frames.append(row_frame)
            
        matched_icon = "•"
        for keyword, icon_char in self.icon_map.items():
            if keyword in row_title: 
                matched_icon = icon_char
                break
                
        name_label = tk.Label(row_frame, text=f" {matched_icon} {row_title}", font=self.fonts["label"])
        name_label.pack(side="left", anchor="w")
        if hasattr(self, 'name_labels'): 
            self.name_labels.append(name_label)
        self.dynamic_name_labels.append(name_label) 
        
        # PROG FIX: Só aplica a propriedade fg se a variável de cor for preenchida (evita o congelamento do widget)
        value_label = tk.Label(row_frame, text="Carregando...", font=self.fonts["monospace"])
        if text_color and text_color != "":
            value_label.config(fg=text_color)
        value_label.pack(side="right", anchor="e")
        
        import uuid
        self.fields[str(uuid.uuid4())] = value_label
        return value_label
