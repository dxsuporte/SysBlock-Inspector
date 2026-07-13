import tkinter as tk

class BaseTab(tk.Frame):
    """
    PROGRAMMER: Advanced abstract layout matrix framework. Auto-handles 
    icon prepends and pushes color states straight into runtime lines layers.
    """
    def __init__(self, parent, font_registry):
        super().__init__(parent, bg="#2d2d2d")
        self.fonts = font_registry
        self.fields = {}
        self.group_boxes = []
        self.row_frames = []
        self.name_labels = []
        self.dynamic_name_labels = []

        # PROG: Expanded Hardware Icon Mapping Table to clear all bullet fallbacks (•)
        self.icon_map = {
            # --- SYSTEM & NEOFETCH LINEAR SPECIFIC SYMBOLS ---
            "Sessão": "👤",        # Target: "Usuário e Host Ativos na Sessão:"
            "Distribuição": "🔲",   # Target: "Nome da Distribuição / OS:"
            "Placa-Mãe": "⌗",      # Target: "Placa-Mãe (Host Platform):"
            "Núcleo": "⎋",         # Target: "Versão do Núcleo Ativo..."
            "Inicialização": "⚙",  # Target: "Modo de Inicialização da Placa-Mãe:"
            "Boot": "⏳",           # Target: "Horário de Boot (Ligar a Máquina):"
            "Idioma": "🌐",         # Target: "Idioma e Localização do Sistema:"
            
            # --- ADVANCED ENVIRONMENTAL METADATA ---
            "Trabalho": "❑",       # Target: "Interface de Trabalho (Desktop DE):"
            "Janelas": "🗔",        # Target: "Gerenciador de Janelas (WM):"
            "Tema": "🎨",           # Target: "Tema de Janelas Ativo (WM Theme):"
            "Ícones": "⌺",         # Target: "Pacote de Ícones do Sistema:"
            "Shell": "❯",          # Target: "Interpretador de Comandos (Shell):"
            "Terminal": "🖳",       # Target: "Emulador de Terminal Ativo:"
            "Pacotes": "⌸",        # Target: "Pacotes Instalados no OS:"
            
            # --- CPU HARDWARE SPECIFIC GEOMETRICS ---
            "Modelo": "⚙",          # Target: "Modelo do Processador Detectado:"
            "Quantidade": "☰",      # Target: "Quantidade Total de Threads:"
            "Configuração": "⌸",    # Target: "Configuração de Cache L1..."
            "Limites": "⏱",         # Target: "Limites do Clock por Hardware..."
            "Perfil": "⚡",          # Target: "Perfil Energético Ativo..."
            "Virtualização": "🖳",   # Target: "Virtualização de Hardware..."
            "Instruções": "❯",      # Target: "Instruções de Extensão Suportadas:"
            "Mitigações": "🛡",      # Target: "Mitigações de Vulnerabilidade de Silício:"
            "Capacidade": "☱",     # Target: "Capacidade de Uso Geral da CPU:"
            "Temperatura": "🌡",    # Target: "Temperatura de Operação do Silício:"
            "Média": "⚖",           # Target: "Média de Carga do Escalonador..."
            "Interrupções": "🔌",   # Target: "Interrupções de Hardware por segundo:"
            "Tempo": "⏳",          # Target: "Tempo de Atividade do Sistema (Uptime):"
            "Forks": "⎌",           # Target: "Forks de Processos e Tarefas..."
            "Clocks": "🚀",         # Target: "Clocks da CPU..."
            
            # --- GPU GRAPHICS HARDWARE GEOMETRICS (UNIFIED AND UNIQUE) ---
            "Chip": "❑",           # Target: "Modelo do Chip de Vídeo (GPU):"
            "Identificadores": "⚿",  # Target: "Identificadores de Hardware (PCI IDs):"
            "Barramento": "⌗",      # Target: "Endereço do Barramento PCI-Express:"
            "Link": "▱",            # Target: "Link de Conexão Máximo (PCIe Slot):"
            "Revisão": "⎋",         # Target: "Código de Revisão do Silício (Rev ID):"
            "Driver": "⧈",          # Target: "Driver de Vídeo Ativo no Kernel:"
            "Frequência de Operação": "⚙", # Target: "Frequência de Operação Atual (Clock):"
            "Frequência Máxima": "⏱", # Target: "Frequência Máxima Limite da GPU:"
            "VRAM": "🗄",           # Target: "Tipo de Memória de Vídeo (VRAM):"
            "Monitores": "☰",       # Target: "Quantidade de Monitores Conectados:"
            "Resoluções": "📐",      # Target: "Resoluções das Telas Ativas:" (Plural fixed!)
            
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

    def create_group_box(self, title, border_color="#777777"):
        """PROG: Defaults to a neutral gray border color instead of dynamic blues/greens."""
        group = tk.LabelFrame(
            self, text=title, font=self.fonts["section"], 
            bg="#2d2d2d", fg=border_color, bd=1, labelanchor="nw"
        )
        group.pack(fill="x", padx=15, pady=6, ipady=4)
        self.group_boxes.append((group, border_color))
        return group

    def append_grid_row(self, container_box, row_title, target_key, font_type="value", text_color="#ffffff"):
        """PROG: Applied neutral white as default foreground text value matching dark theme startup."""
        row_frame = tk.Frame(container_box, bg="#2d2d2d")
        row_frame.pack(fill="x", expand=True, padx=15, pady=3)
        self.row_frames.append(row_frame)

        matched_icon = "•"
        for indicator_keyword, icon_char in self.icon_map.items():
            if indicator_keyword in row_title:
                matched_icon = icon_char
                break

        full_title_text = f" {matched_icon}  {row_title}"

        name_label = tk.Label(row_frame, text=full_title_text, font=self.fonts["label"], bg="#2d2d2d", fg="#aaaaaa")
        name_label.pack(side="left", anchor="w")
        self.name_labels.append(name_label)

        chosen_font = self.fonts["monospace"] if font_type == "value" else self.fonts[font_type]

        value_label = tk.Label(
            row_frame, text="Carregando...", 
            font=chosen_font, bg="#2d2d2d", fg=text_color
        )
        value_label.pack(side="right", anchor="e")

        self.fields[target_key] = value_label
        return value_label

    def apply_theme_colors(self, colors):
        """UNIVERSAL THEME SWITCHER: Smoothly paints elements into pure white or deep black."""
        self.config(bg=colors["bg_card"])
        
        for group, base_border in self.group_boxes:
            group.config(bg=colors["bg_card"], fg=colors["text_main"])
            
        for row in self.row_frames:
            row.config(bg=colors["bg_card"])
            
        for label in self.name_labels:
            label.config(bg=colors["bg_card"], fg=colors["text_sec"])
            
        for label in self.dynamic_name_labels:
            if label.winfo_exists():
                label.config(bg=colors["bg_card"], fg=colors["text_sec"])
            
        for key, field in self.fields.items():
            if field.winfo_exists():
                current_fg = field.cget("fg")
                # SEMANTIC COLOR PROTECTION: Guard Red and Green status, change everything else to Main Text
                if current_fg not in ["#ff3333", "#4cbd5a", "#008000"]:
                    field.config(bg=colors["bg_card"], fg=colors["text_main"])
                else:
                    field.config(bg=colors["bg_card"])
