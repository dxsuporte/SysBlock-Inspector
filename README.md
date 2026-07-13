# SysBlock-Inspector 🐧🔬

[**Read this in Portuguese (Clique aqui para ler em Português)**](#-versão-em-português)

**SysBlock-Inspector** is a modern, lightweight, and hardware-focused standalone system diagnostic utility for Linux desktops (fully optimized for Linux Mint, Ubuntu, and Fedora). It bridges the gap between CLI utilities like `neofetch` and deep hardware monitors like `CPU-Z` or `HWMonitor`, rendering low-level silicon telemetry inside a clean, enterprise-grade dark/light Tkinter graphical interface.

This project was built with portability in mind, designed to run directly from field support USB drives without requiring external Python dependencies on the target customer machine.

---

## 💎 Key Features & Modules

The system performs a silent scan across hardware buses and Kernel paging files to deliver real-time telemetry split into 7 premium tabs:

- **💻 System / Neofetch**: Real-time extraction of desktop environment configurations (DE, WM, active Display Server like X11/Wayland) bypassing `pkexec` root environment isolation filters.
- **❖ Processor (CPU)**: Independent core clock metrics tracking hardware speed intervals per thread every 2 seconds.
- **🔌 Motherboard & BIOS**: Direct crawling of electrical PCI links to map Chipsets models and Integrated Audio Codecs.
- **▤ Memory RAM**: Scans physical board traces to count occupied layout slots, maximum chip capacity limits, and commercial JEDEC factory signatures (e.g., Crucial, Micron).
- **🖥 Graphics (GPU)**: Hardware-level silicon chip name extraction (e.g., Intel UHD Graphics 630) resolving missing vendor string split errors.
- **🌐 Network Interface**: High-efficiency live bandwidth traffic counters tracking true physical layer silicon chips models (e.g., Intel I219-V Ethernet and Wi-Fi 6E AX210) instead of raw logical device labels.
- **💾 Storage Audit**: Unified JSON-based block device tree mapping. Displays health degradation slices via `smartctl`/`nvme-cli` alongside raw physical NVMe controller models (Silicon Motion, Realtek, ADATA).

---

## 🛠️ Technical Specifications & System Requirements

### Target Environments

- **Original Intention**: Developed and calibrated specifically with a focus on the **Cinnamon** desktop interface of **Linux Mint 22.x (or higher)**.
- **Lab Testing Environment**: Thoroughly tested and certified on **Linux Mint**, with real-world packaging test deployments targeting native **Debian (.deb)** files.
- **Universal Cross-Distro Compatibility**: Although automated packaging scripts were tested on a Debian base, the software engineering was completely planned and designed to run universally on **Fedora (.rpm)**, Ubuntu, Arch Linux, RedHat, and any other modern 64-bit Linux distribution.

### Kernel Recommendations & Base Dependencies

The application features **native graceful error handling**, notifying the user at startup if any of the packages below are missing, allowing CPU and RAM monitoring to continue normally:

- **Recommended Kernel**: Linux Kernel **5.15 or higher** (optimized for modern 6.x LTS series).
- **Disk Polling (SMART)**: Requires `smartmontools` and `nvme-cli` packages.
- **Chip Mapping (PCI Bus)**: Requires `pciutils` package (`lspci` command).

---

## 🚀 How to Execute, Compile & Package

### How to Use (After Installation)

Once installed via `.deb` or `.rpm`, the application integrates natively into Linux security standards. You can launch it in two ways:

1. **Via Graphical Interface**: Open your Applications Menu, navigate to the **Administration** category, and click on **SysBlock-Inspector**. It will securely trigger the native system authentication prompt (`pkexec`) asking for your password.
2. **Via Terminal**:
   ```bash
   sysblock-inspector
   ```

### How to Compile (For GitHub Developers)

The repository provides automated Bash scripts that handle administrative cache cleanups, invoke PyInstaller, and output the final production-ready packages **directly inside the `dist/` directory**:

1. **Grant execution permissions to automation scripts (First time only)**:
   ```bash
   chmod +x *.sh
   ```
2. **Build Standard Portable Binary (Standalone)**:
   ```bash
   ./build.sh
   ```
3. **Generate Native Debian/Mint Package (.deb)**:
   ```bash
   ./create_deb.sh
   ```
4. **Generate Native Fedora Package (.rpm)**:
   ```bash
   ./create_rpm.sh
   ```

---

## 🧑‍💻 Development Credits & AI Co-Authorship

This software is the result of modern reverse engineering and agile development methodologies, bridging human field expertise with advanced artificial intelligence:

- **Idealization, Architecture & Bench Validation**: Designed, tested, and certified in production environments by **Danilo Xavier** – director and founder of **DXSuporte** (Registered Trademark), applying years of hands-on experience in tech support, system auditing, and hardware deployment.
- **Code Engineering & AI Co-Authorship**: Developed in partnership with a **Google Advanced Language Artificial Intelligence model**, acting as a senior software co-author to structure the synchronous Tkinter Canvas layout, optimize Bash automation pipelines, and bulletproof the core engine against administrative environment isolation gates (`pkexec`/Polkit).

---

## 🤝 Project Purpose & Contributions (Open Source License)

**SysBlock-Inspector** was built with a threefold purpose:

1. **Maintenance**: Act as a fast diagnostic swiss-army knife for IT field support technicians.
2. **Information**: Provide transparent hardware metrics for end-users to audit their rigs.
3. **Study**: Serve as living system documentation for developers to study direct low-level interactions with the Linux Kernel subsystems (`/sys` and `/proc`).

### License & Growth

This project is open-source and free. It has been shared publicly with the express intent that **anyone interested can use, modify, study, and, above all, contribute to its continuous improvement**, extending compatibility to new distributions, hardware drivers, and keeping the utility modern and immune to technological obsolescence.

Feel free to open _Issues_, submit _Pull Requests_, or perform _Forks_!

---

---

## 🇧🇷 Versão em Português

**SysBlock-Inspector** é um utilitário de diagnóstico e monitoramento de hardware de nível industrial e código aberto para ecossistemas Linux. Ele renderiza telemetria de baixo nível de hardware em uma interface gráfica Tkinter minimalista, rápida e responsiva.

O projeto foi projetado com foco em **portabilidade absoluta**, permitindo gerar um executável binário único capaz de rodar diretamente de pendrives de assistência técnica de campo, sem exigir dependências no cliente.

### 💎 Funcionalidades e Módulos do Sistema

- **💻 Sistema / Neofetch**: Informações do OS, uptime, idioma local e ambiente gráfico (DE, WM, Temas) com suporte ao **Servidor Gráfico Ativo (X11 ou Wayland)**.
- **❖ Processador (CPU)**: Identificação do modelo, núcleos reais e frequências independentes (Clocks) por thread atualizados ao vivo.
- **🔌 Placa-Mãe**: Dados de DMI/BIOS, barramentos elétricos PCI, Chipset da placa e controladores de Áudio Integrados.
- **▤ Memória RAM**: Varredura de slots físicos ocupados/vazios, capacidade máxima e assinaturas comerciais JEDEC (ex: Crucial, Micron).
- **🖥 Placa de Vídeo (GPU)**: Identificação cirúrgica do chip gráfico ativo (ex: Intel UHD Graphics 630).
- **🌐 Tráfego de Rede**: Contadores de download/upload vivos atrelados estritamente ao silício físico dos chips (ex: Intel I219-V e Wi-Fi 6E AX210).
- **💾 Armazenamento / Discos**: Mapeamento JSON de blocos de discos. Auditoria de saúde (SMART) para HDs e SSDs NVMe com fabricante do controlador de silício.

### 🛠️ Especificações Técnicas e Requisitos

- **Intenção Original**: Otimizado para a interface **Cinnamon** do **Linux Mint 22.x**.
- **Compatibilidade Ampliada**: Engenharia pensada para rodar universalmente no **Fedora (.rpm)**, Ubuntu, Arch Linux e derivados de 64 bits.
- **Kernel Recomendado**: Linux Kernel **5.15 ou superior** (séries de Kernel 6.x recomendadas).
- **Dependências de Disco e Barramento**: Usa `smartmontools`, `nvme-cli` e `pciutils` (com tratamento nativo caso estejam ausentes).

### 🚀 Como Executar, Compilar e Empacotar

- **Execução**: Chame pelo menu de **Administração** (via `pkexec` gráfico) ou abra pelo terminal digitando `sysblock-inspector`.
- **Compilação**: Dê permissão com `chmod +x *.sh` e execute `./build.sh` para o binário, `./create_deb.sh` para o instalador Mint/Ubuntu ou `./create_rpm.sh` para o instalador do Fedora. Todos os arquivos finais saem organizados dentro da pasta `dist/`.

### 🧑‍💻 Créditos de Desenvolvimento e Co-Autoria IA

- **Idealização e Validação**: **Danilo Xavier** – diretor e fundador da **DXSuporte** (Marca Registrada), aplicando experiência prática de campo em assistência técnica.
- **Engenharia de Código**: Desenvolvido em parceria com um modelo de **Inteligência Artificial de Linguagem Avançada da Google**, atuando como co-autor de software sênior.

### 🤝 Propósito do Projeto e Contribuição (Licença Aberta)

Ferramenta aberta disponibilizada publicamente para que **qualquer pessoa interessada possa usar, modificar, estudar e contribuir para a melhoria contínua do sistema**, estendendo o suporte e impedindo a obsolescência tecnológica.
