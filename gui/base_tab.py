import tkinter as tk

class BaseTab(tk.Frame):
    """
    PROGRAMMER: Advanced abstract layout matrix framework. Auto-handles 
    icon prepends natively. Run layout elements purely raw.
    """
    def __init__(self, parent, font_registry):
        super().__init__(parent)
        self.fonts = font_registry
        self.fields = {}
        self.group_boxes = []
        self.row_frames = []
        self.name_labels = []
        self.dynamic_name_labels = []
        
        # PROG: Expanded Hardware Icon Mapping Table to clear all bullet fallbacks (•)
        self.icon_map = {
            # --- SYSTEM & NEOFETCH LINEAR SPECIFIC SYMBOLS ---
            "Sessão": "👤",
            "Distribuição": "🔲",
            "Placa-Mãe": "⌗",
            "Núcleo": "⎋",
            "Inicialização": "⚙",
            "Boot": "⏳",
            "Idioma": "🌐",
            
            # --- ADVANCED ENVIRONMENTAL METADATA ---
            "Trabalho": "❑",
            "Janelas": "🗔",
            "Tema": "🎨",
            "Ícones": "⌺",
            "Shell": "❯",
            "Terminal": "🖳",
            "Pacotes": "⌸",
            
            # --- CPU HARDWARE SPECIFIC GEOMETRICS ---
            "Modelo": "⚙",
            "Quantidade": "☰",
            "Configuração": "⌸",
            "Limites": "⏱",
            "Perfil": "⚡",
            "Virtualização": "🖳",
            "Instruções": "❯",
            "Mitigações": "🛡",
            "Capacidade": "☱",
            "Temperatura": "🌡",
            "Média": "⚖",
            "Interrupções": "🔌",
            "Tempo": "⏳",
            "Forks": "⎌",
            "Clocks": "🚀",
            
            # --- GPU GRAPHICS HARDWARE GEOMETRICS (UNIFIED AND UNIQUE) ---
            "Chip": "❑",
            "Identificadores": "⚿",
            "Barramento": "⌗",
            "Link": "▱",
            "Revisão": "⎋",
            "Driver": "⧈",
            "Frequência de Operação": "⚙",
            "Frequência Máxima": "⏱",
            "VRAM": "🗄",
            "Monitores": "☰",
            "Resoluções": "📐",
            
            # --- NETWORK MODULE GEOMETRIC ALIGNMENTS ---
            "Placa": "⌗",
            "Endereço": "🌐",
            "MAC": "⚿",
            "Físico": "⚿",
            "Roteador": "▤",
            "Gateway": "▤",
            "Servidores": "⌺",
            "Velocidade": "⚡",
            "Sincronismo": "⚡",
            "Latência": "⏱",
            "Taxa": "❯",
            "Fluxo": "❯",
            "Status": "⚙",
            
            # --- RAM LINEAR SYMBOLS ---
            "Porcentagem": "☱",
            "Espaço": "▤",
            "Área": "🌀",
            "Memória": "🗄",
            
            # --- STORAGE LINEAR SYMBOLS ---
            "SSD": "⚡",
            "Disco": "⧇",
            "HD/SSD": "⧇"
        }

    def create_group_box(self, title):
        """PROG: Instantiates native standard system-styled LabelFrame with 100% universal stretch response."""
        # PROG: Se a aba possuir um frame de rolagem interno no Canvas, anexa a caixa nele automaticamente
        parent_node = self.scroll_content_frame if hasattr(self, 'scroll_content_frame') else self
        
        group = tk.LabelFrame(parent_node, text=title, font=self.fonts["section"], labelanchor="nw")
        
        # XEQUE-MATE DE RESPONSIVIDADE NATIVA: Adicionado fill="x" e expand=True com ancoragem para a esquerda (w)
        group.pack(fill="x", expand=True, padx=15, pady=6, ipady=4, anchor="w")
        
        self.group_boxes.append(group)
        return group

    def append_grid_row(self, container_box, row_title, target_key, font_type="value"):
        """PROG: Handlers layout grid appending pipelines without hardcoded color properties."""
        row_frame = tk.Frame(container_box)
        row_frame.pack(fill="x", expand=True, padx=15, pady=3)
        self.row_frames.append(row_frame)
        
        matched_icon = "•"
        for indicator_keyword, icon_char in self.icon_map.items():
            if indicator_keyword in row_title:
                matched_icon = icon_char
                break
                
        # Interroga a cor de texto nativa do sistema operacional (geralmente preto ou cinza escuro)
        system_text_color = container_box.cget("fg") if hasattr(container_box, "cget") else "black"
        if not system_text_color or system_text_color == "":
            system_text_color = "black"
            
        # FIX DE CONTRASTE DOS ÍCONES: Separa o ícone do título para garantir que ambos acendam com nitidez total
        lbl_icon = tk.Label(row_frame, text=f" {matched_icon}", font=self.fonts["label"], fg=system_text_color)
        lbl_icon.pack(side="left", anchor="w")
        
        name_label = tk.Label(row_frame, text=f" {row_title}", font=self.fonts["label"], fg=system_text_color)
        name_label.pack(side="left", anchor="w")
        self.name_labels.append(name_label)
        
        chosen_font = self.fonts["monospace"] if font_type == "value" else self.fonts[font_type]
        value_label = tk.Label(row_frame, text="Carregando...", font=chosen_font, fg=system_text_color)
        value_label.pack(side="right", anchor="e")
        
        self.fields[target_key] = value_label
        return value_label