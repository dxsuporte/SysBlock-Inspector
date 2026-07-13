# SysBlock-Inspector 🐧🔬

**SysBlock-Inspector** é um utilitário de diagnóstico e monitoramento de hardware de nível industrial e código aberto para ecossistemas Linux. Desenvolvido para preencher a lacuna entre ferramentas em linha de comando (como o `neofetch`) e monitores profundos de silício (como `CPU-Z` ou `HWMonitor`), ele renderiza telemetria de baixo nível de hardware em uma interface gráfica Tkinter minimalista, rápida e responsiva.

O projeto foi projetado com foco em **portabilidade absoluta**, permitindo gerar um executável binário único capaz de rodar diretamente de pendrives de assistência técnica de campo, sem exigir a instalação manual de interpretadores Python ou dependências visuais na máquina do cliente.

---

## 💎 Funcionalidades e Módulos do Sistema

O sistema realiza uma varredura cega por barramentos e arquivos de paginação do Kernel para entregar telemetria em tempo real dividida em 7 abas premium:

- **💻 Sistema / Neofetch**: Exibe informações do Sistema Operacional, hostname, uptime de boot, idioma local e configurações do ambiente gráfico (DE, WM, Temas de Ícones e Janelas) bypassando de forma segura os bloqueios de isolamento do root. Traz suporte nativo para detectar o **Servidor Gráfico Ativo (X11 ou Wayland)**.
- **❖ Processador (CPU)**: Identificação do modelo exato do chip de silício, quantidade de núcleos reais e monitoramento dinâmico vivo da frequência (Clocks de Clock independentes) por thread a cada 2 segundos.
- **🔌 Placa-Mãe**: Extração do DNA bruto de fabricação da placa (DMI/BIOS), mapeamento de links elétricos PCI para exibição do Chipset da placa e controladores de Áudio Integrados.
- **▤ Memória RAM**: Scans profundos nos barramentos de memória do sistema para relatar slots físicos ocupados/vazios, capacidade máxima suportada e as assinaturas comerciais JEDEC de fábrica (ex: Crucial, Micron) dos pentes instalados.
- **🖥 Placa de Vídeo (GPU)**: Identificação cirúrgica do chip gráfico ativo (ex: Intel UHD Graphics 630), eliminando cortes de strings e exibindo o modelo bruto do processador visual.
- **🌐 Tráfego de Rede**: Contadores de tráfego de download/upload ao vivo atrelados estritamente ao silício físico real dos chips (ex: Intel I219-V Ethernet ou Wi-Fi 6E AX210), em vez de rótulos lógicos genéricos do sistema.
- **💾 Armazenamento / Discos**: Mapeamento em árvore JSON de blocos de discos conectados. Realiza auditoria de saúde fracionada (SMART) para HDs tradicionais e SSDs NVMe e expõe o fabricante real dos controladores de silício (Silicon Motion, Realtek, ADATA).

---

## 🛠️ Especificações Técnicas e Requisitos de Sistema

### Alvo de Desenvolvimento e Ambientes

- **Intenção Original de Criação**: Desenvolvido e calibrado especificamente com foco na interface gráfica **Cinnamon** do **Linux Mint 22.x (ou superiores)**.
- **Ambiente de Testes de Laboratório**: Homologado e testado exaustivamente no **Linux Mint**, com testes práticos do compilador e instalador gerados nativamente para pacotes **Debian (.deb)**.
- **Compatibilidade Universal Estendida**: Embora os scripts de empacotamento automatizados tenham sido testados na base Debian, a engenharia do software foi inteiramente pensada, estruturada e planejada para rodar de forma universal no **Fedora (.rpm)**, Ubuntu, Arch Linux, RedHat e qualquer outra distribuição Linux moderna de 64 bits.

### Recomendações de Kernel e Dependências Base

Para garantir a leitura nativa dos controladores de armazenamento modernos, chips de Wi-Fi 6E/7 e clocks de processadores de última geração, o ecossistema utiliza utilitários padrão de mercado. O programa possui **tratamento nativo de erros**, avisando amigavelmente na inicialização caso falte algum dos pacotes abaixo, permitindo que a CPU e a RAM continuem sendo monitoradas normalmente:

- **Versão de Kernel Recomendada**: Linux Kernel **5.15 ou superior** (com suporte ideal para as séries de Kernel modernas de longo suporte 6.x).
- **Leitura de Discos (SMART)**: Requer os pacotes `smartmontools` e `nvme-cli`.
- **Mapeamento de Chips (Barramentos PCI)**: Requer o pacote `pciutils` (comando `lspci`).

---

## 🚀 Como Executar, Compilar e Gerar os Instaladores

### Como Usar (Após a Instalação)

Uma vez instalado através do pacote `.deb` ou `.rpm`, o programa se integra nativamente ao ecossistema de segurança do Linux. Você pode abri-lo de duas formas:

1. **Pela Interface Gráfica**: Abra o seu Menu de Aplicativos, vá na categoria **Administração** e clique no ícone do **SysBlock-Inspector**. Ele abrirá de forma moderna a tela de autenticação gráfica oficial do sistema (`pkexec`) pedindo a sua senha.
2. **Pelo Terminal**: Caso prefira invocar manualmente via linha de comando, basta digitar:
   ```bash
   sysblock-inspector
   ```

### Como Compilar (Para Desenvolvedores do GitHub)

O repositório disponibiliza scripts automatizados em Bash que fazem a limpeza de caches locais, invocam o PyInstaller e geram os pacotes comerciais finais **direto dentro da pasta `dist/`**, sem a necessidade de ferramentas complexas de terceiros.

1. **Dar permissão aos scripts de automação (Apenas na primeira vez)**:
   ```bash
   chmod +x *.sh
   ```
2. **Gerar o Binário Único Portátil (Standalone)**:
   ```bash
   ./build.sh
   ```
3. **Gerar Instalador Nativo para Linux Mint / Ubuntu (.deb)**:
   ```bash
   ./create_deb.sh
   ```
4. **Gerar Instalador Nativo para Fedora / RedHat (.rpm)**:
   ```bash
   ./create_rpm.sh
   ```

---

## 🧑‍💻 Créditos de Desenvolvimento e Co-Autoria IA

Este software é fruto de uma metodologia moderna de engenharia reversa e desenvolvimento ágil, unindo a expertise humana de campo com inteligência artificial avançada:

- **Idealização, Arquitetura e Validação de Bancada**: Projetado, testado e validado em ambiente real por **Danilo Xavier** – diretor e fundador da **DXSuporte** (Marca Registrada), aplicando anos de experiência prática em assistência técnica, auditoria e manutenção de computadores corporativos.
- **Engenharia de Código e Co-Autoria Inteligente**: Desenvolvido em parceria com um modelo de **Inteligência Artificial de Linguagem Avançada da Google**, atuando como co-autor de software sênior para estruturar a lógica síncrona do Tkinter por Canvas, otimizar os scripts de compilação em Bash e blindar o motor `core.py` contra privilégios administrativos invisíveis do barramento `pkexec` (Polkit).

---

## 🤝 Propósito do Projeto e Contribuição (Licença Aberta)

O **SysBlock-Inspector** foi criado com um propósito tríplice:

1. **Manutenção**: Servir como ferramenta de diagnóstico rápida para técnicos de informática em atendimento de campo.
2. **Informação**: Prover relatórios transparentes de hardware para usuários finais auditarem suas máquinas.
3. **Estudo**: Servir como documentação viva de engenharia de software para desenvolvedores estudarem interações diretas com o subsistema do Kernel do Linux (`/sys` e `/proc`).

### Licença e Melhorias

Este projeto está sob licença aberta e livre. Ele foi disponibilizado publicamente com a intenção expressa de que **toda e qualquer pessoa interessada possa usar, modificar, estudar e, acima de tudo, contribuir para a melhoria contínua do sistema**, estendendo o suporte para novas distribuições, novos drivers e mantendo o utilitário moderno e imune à obsolescência tecnológica.

Sinta-se à vontade para abrir _Issues_, propor _Pull Requests_ ou realizar _Forks_ do projeto!
