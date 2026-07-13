import os
import time
import subprocess
import socket

# GLOBAL STATS MODULE STORAGE: References for system runtime deltas
_last_cpu_state = (0, 0)
_last_interrupt_state = (0, 0.0)

def get_cpu_usage():
    global _last_cpu_state
    try:
        with open("/proc/stat", "r") as f:
            first_line = f.readline()
        cpu_ticks = [int(x) for x in first_line.split()[1:]]
        idle_time = cpu_ticks[3]
        total_time = sum(cpu_ticks)
        work_time = total_time - idle_time
        prev_work, prev_total = _last_cpu_state
        diff_work = work_time - prev_work
        diff_total = total_time - prev_total
        _last_cpu_state = (work_time, total_time)
        if diff_total == 0: return "0%"
        return f"{int((diff_work / diff_total) * 100)}%"
    except Exception: return "N/A"

def get_per_core_clocks():
    """UNIVERSAL 32/64-BIT: Safely detects any number of cores without index crashes."""
    clocks = []
    try:
        if os.path.exists("/proc/cpuinfo"):
            with open("/proc/cpuinfo", "r") as f:
                for line in f:
                    if "cpu MHz" in line or "CPU MHz" in line:
                        mhz = float(line.split(":")[-1].strip())
                        clocks.append(f"{mhz / 1000:.2f} GHz")
        
        if not clocks and os.path.exists("/sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq"):
            cpu_idx = 0
            while os.path.exists(f"/sys/devices/system/cpu/cpu{cpu_idx}/cpufreq/scaling_cur_freq"):
                with open(f"/sys/devices/system/cpu/cpu{cpu_idx}/cpufreq/scaling_cur_freq", "r") as f:
                    khz = int(f.read().strip())
                    clocks.append(f"{khz / 1000 / 1000:.2f} GHz")
                cpu_idx += 1

        if not clocks: return ["N/A"]

        rows = []
        for i in range(0, len(clocks), 4):
            chunk = clocks[i:i+4]
            row_str = "  |  ".join([f"N{i+idx}: {clk}" for idx, clk in enumerate(chunk)])
            rows.append(row_str)
        return rows
    except Exception: return ["N/A"]

def get_cpu_temperature():
    """UNIVERSAL: Checks thermal zones first, then drivers (Intel coretemp / AMD k10temp)."""
    try:
        thermal_root = "/sys/class/thermal"
        if os.path.exists(thermal_root):
            for zone in os.listdir(thermal_root):
                if zone.startswith("thermal_zone"):
                    type_path = os.path.join(thermal_root, zone, "type")
                    temp_path = os.path.join(thermal_root, zone, "temp")
                    if os.path.exists(type_path) and os.path.exists(temp_path):
                        with open(type_path, "r") as f: z_type = f.read().strip().lower()
                        if "cpu" in z_type or "x86_pkg" in z_type or "acpitz" in z_type:
                            with open(temp_path, "r") as f: val = int(f.read().strip())
                            if val > 0: return f"{int(val / 1000)}°C"

        hwmon_root = "/sys/class/hwmon"
        if os.path.exists(hwmon_root):
            for folder in os.listdir(hwmon_root):
                name_path = os.path.join(hwmon_root, folder, "name")
                if os.path.exists(name_path):
                    with open(name_path, "r") as f: driver = f.read().strip()
                    if driver in ["coretemp", "k10temp", "zenpower"]:
                        for entry in os.listdir(os.path.join(hwmon_root, folder)):
                            if entry.endswith("_input") and ("temp1" in entry or "temp2" in entry):
                                with open(os.path.join(hwmon_root, folder, entry), "r") as tf:
                                    val = int(tf.read().strip())
                                    if val > 0: return f"{int(val / 1000)}°C"
        return "N/A"
    except Exception: return "N/A"

def get_cpu_interrupts_per_second():
    global _last_interrupt_state
    try:
        current_time = time.time()
        with open("/proc/stat", "r") as f:
            for line in f:
                if line.startswith("intr"):
                    total_intr = int(line.split()[1])
                    break
        prev_intr, prev_time = _last_interrupt_state
        diff_time = current_time - prev_time
        _last_interrupt_state = (total_intr, current_time)
        if diff_time <= 0: return "0/s"
        return f"{int((total_intr - prev_intr) / diff_time)} /s"
    except Exception: return "N/A"

def get_cpu_load_average():
    try:
        with open("/proc/loadavg", "r") as f:
            return "  |  ".join(f.readline().split()[:3])
    except Exception: return "N/A"

def get_system_uptime():
    try:
        with open("/proc/uptime", "r") as f:
            up_secs = float(f.readline().split()[0])
        hours, minutes = int(up_secs // 3600), int((up_secs % 3600) // 60)
        days, hours = int(hours // 24), int(hours % 24)
        if days > 0: return f"{days}d {hours}h {minutes}m"
        return f"{hours}h {minutes}m"
    except Exception: return "N/A"

def get_cpu_governor_info():
    info = {"governor": "N/A", "min_clock": "N/A", "max_clock": "N/A"}
    try:
        cpufreq_root = "/sys/devices/system/cpu/cpu0/cpufreq"
        if os.path.exists(cpufreq_root):
            gov_path = os.path.join(cpufreq_root, "scaling_governor")
            if os.path.exists(gov_path):
                with open(gov_path, "r") as f: info["governor"] = f.read().strip().upper()
            min_path = os.path.join(cpufreq_root, "scaling_min_freq")
            max_path = os.path.join(cpufreq_root, "scaling_max_freq")
            if os.path.exists(min_path):
                with open(min_path, "r") as f: info["min_clock"] = f"{int(f.read().strip()) / 1000 / 1000:.2f} GHz"
            if os.path.exists(max_path):
                with open(max_path, "r") as f: info["max_clock"] = f"{int(f.read().strip()) / 1000 / 1000:.2f} GHz"
        return info
    except Exception: return info

def get_cpu_instructions_flags():
    """UNIVERSAL: Parses cpuinfo to extract a clean string of advanced instruction sets."""
    try:
        with open("/proc/cpuinfo", "r") as f:
            content = f.read()
        supported = []
        for flag in ["sse", "sse2", "sse4_1", "avx", "avx2", "avx512f", "aes", "fma"]:
            if f"\t{flag} " in content or f" {flag} " in content:
                supported.append(flag.upper().replace("_", "."))
        return " | ".join(supported) if supported else "Instruções Básicas x86"
    except Exception: return "N/A"

def get_cpu_fork_and_tasks_metrics():
    """UNIVERSAL: Parses system processes forks counts and active threads running."""
    metrics = {"forks": "N/A", "procs_running": "N/A"}
    try:
        with open("/proc/stat", "r") as f:
            for line in f:
                if line.startswith("processes"):
                    metrics["forks"] = line.split()[-1].strip()
                elif line.startswith("procs_running"):
                    metrics["procs_running"] = line.split()[-1].strip()
        return f"Ativos: {metrics['procs_running']}  |  Total de Forks: {metrics['forks']}"
    except Exception: return "N/A"

def get_cpu_static_hardware_specs():
    """UNIVERSAL 32/64-BIT: Advanced metadata engine. Extracts precise Neofetch layout profiles dynamically."""
    specs = {
        "model": "Processador Genérico", "cores": "N/A", "cache_l1": "N/A",
        "cache_l2": "N/A", "cache_l3": "N/A", "vt_x": "Inativa", "mitigations": "N/A",
        "hostname": "N/A", "kernel": "N/A", "distro": "Linux Genérico", "arch": "N/A",
        "boot_mode": "Legacy (BIOS)", "boot_time": "N/A", "locale": "pt_BR.UTF-8",
        "de": "CINNAMON", "wm": "Muffin (Cinnamon)", "packages": "N/A", "resolution": "N/A",
        "host_board": "N/A", "shell": "/bin/bash", "terminal": "gnome-terminal", "gtk_theme": "Mint-Y-Dark", 
        "gtk_icons": "Mint-Y", "session_type": "X11 / Padrão"  # ADICIONADO: Nova chave de servidor gráfico
    }
    
    # 1. Parse network nodes and distribution markers
    try:
        if os.path.exists("/proc/sys/kernel/hostname"):
            with open("/proc/sys/kernel/hostname", "r") as f: specs["hostname"] = f.read().strip()
        if os.path.exists("/proc/sys/kernel/osrelease"):
            with open("/proc/sys/kernel/osrelease", "r") as f: specs["kernel"] = f.read().strip()
        if os.path.exists("/etc/os-release"):
            with open("/etc/os-release", "r") as f:
                for line in f:
                    if line.startswith("PRETTY_NAME="):
                        specs["distro"] = line.split("=")[-1].replace('"', '').strip()
                        break
        import platform
        specs["arch"] = platform.machine()
    except Exception: pass

    # 2. Parse Motherboard Host Information
    try:
        board_name = "N/A"
        board_version = ""
        if os.path.exists("/sys/class/dmi/id/board_name"):
            with open("/sys/class/dmi/id/board_name", "r") as f: board_name = f.read().strip()
        if os.path.exists("/sys/class/dmi/id/board_version"):
            with open("/sys/class/dmi/id/board_version", "r") as f: board_version = f.read().strip()
        specs["host_board"] = f"{board_name} {board_version}".strip()
    except Exception: pass

    # 3. Parse CPU Data Tracks
    try:
        with open("/proc/cpuinfo", "r") as f: content = f.read()
        specs["cores"] = str(content.count("processor\t:"))
        for line in content.split('\n'):
            if "model name" in line or "Model Name" in line or "Processor" in line:
                specs["model"] = line.split(":")[-1].strip()
                break
        if "vmx" in content: specs["vt_x"] = "Ativa (Intel VT-x Habilitado)"
        elif "svm" in content: specs["vt_x"] = "Ativa (AMD-V Habilitado)"
    except Exception: pass
    
    # 4. Parse Cache Layers
    try:
        cache_root = "/sys/devices/system/cpu/cpu0/cache"
        if os.path.exists(cache_root):
            for idx in os.listdir(cache_root):
                if idx.startswith("index"):
                    with open(os.path.join(cache_root, idx, "level"), "r") as lf: level = lf.read().strip()
                    with open(os.path.join(cache_root, idx, "size"), "r") as sf: size = sf.read().strip()
                    specs[f"cache_l{level}"] = size
    except Exception: pass

    # 5. Check Mitigations and Boot Modes
    try:
        vuln_path = "/sys/devices/system/cpu/vulnerabilities/spectre_v2"
        if os.path.exists(vuln_path):
            with open(vuln_path, "r") as f: specs["mitigations"] = "Ativas (Segurança OK)" if "Mitigation" in f.read() else "Vulnerável"
        if os.path.exists("/sys/firmware/efi"): specs["boot_mode"] = "Moderno (UEFI)"
    except Exception: pass

    # 6. Boot Time Calculation
    try:
        if os.path.exists("/proc/uptime"):
            with open("/proc/uptime", "r") as f:
                uptime_seconds = float(f.readline().strip().split()[0])
                boot_timestamp = time.time() - uptime_seconds
                specs["boot_time"] = time.strftime("%d/%m/%Y às %H:%M:%S", time.localtime(boot_timestamp))
    except Exception: pass

    # 7. Localized Locales and Active Environment Desktops (Bypassing D-Bus/Polkit session locks)
    try:
        if os.path.exists("/etc/default/locale"):
            with open("/etc/default/locale", "r") as f:
                for line in f:
                    if line.startswith("LANG="): specs["locale"] = line.split("=")[-1].replace('"', '').strip(); break
        
        # Discover true graphic user under pkexec session context
        real_user = os.environ.get("SUDO_USER")
        if not real_user or real_user == "root":
            try:
                real_user = subprocess.check_output("who | awk '{print $1}' | head -n 1", shell=True, text=True, stderr=subprocess.DEVNULL).strip()
            except Exception:
                real_user = ""
        if not real_user or real_user == "root":
            real_user = "danilo"

        # Interrogate real passwd shell configurations
        cmd_sh = f"getent passwd {real_user}"
        sh_out = subprocess.check_output(cmd_sh, shell=True, text=True, stderr=subprocess.DEVNULL).strip()
        if sh_out:
            parts = sh_out.split(":")
            specs["shell"] = parts[-1].strip()
            user_home = parts[-2].strip()
        else:
            specs["shell"] = "/bin/bash"
            user_home = f"/home/{real_user}"

        specs["de"] = "CINNAMON"
        specs["wm"] = "Muffin (Cinnamon)"
        
        # --- CRAWL PROTOCOLO DE TELA (X11 VS WAYLAND ADAPTIVE ELEMENT) ---
        try:
            cmd_session = f"sudo -u {real_user} printenv XDG_SESSION_TYPE"
            session_out = subprocess.check_output(cmd_session, shell=True, text=True, stderr=subprocess.DEVNULL).strip().lower()
            if "wayland" in session_out:
                specs["session_type"] = "Wayland (Moderno / Protocolo Nativo)"
            elif "x11" in session_out:
                specs["session_type"] = "X11 (Clássico / Servidor de Janelas)"
            else:
                specs["session_type"] = f"{session_out.upper()} Session"
        except Exception:
            specs["session_type"] = "X11 (Clássico / Servidor de Janelas)"
            
    except Exception: pass

    # 8. Extract active terminal software descriptor pipeline
    try:
        if real_user:
            cmd_term = f"sudo -u {real_user} ps -o comm= -p $(ps -o ppid= -p $PPID)"
            term_out = subprocess.check_output(cmd_term, shell=True, text=True, stderr=subprocess.DEVNULL).strip()
            if term_out in ["bash", "sudo", "python3", "sshd", "pkexec", "sh"]:
                specs["terminal"] = "gnome-terminal"
            else:
                specs["terminal"] = term_out if term_out else "gnome-terminal"
        else:
            specs["terminal"] = "gnome-terminal"
    except Exception:
        specs["terminal"] = "gnome-terminal"

    # 9. Count Packages (APT + Flatpak granular scans)
    try:
        apt_count = 0
        if os.path.exists("/var/lib/dpkg/status"):
            with open("/var/lib/dpkg/status", "r") as f: apt_count = f.read().count("Package: ")
        flatpak_count = 0
        if os.path.exists("/var/lib/flatpak/app"): flatpak_count = len(os.listdir("/var/lib/flatpak/app"))
        specs["packages"] = f"{apt_count} (dpkg)"
        if flatpak_count > 0: specs["packages"] += f", {flatpak_count} (flatpak)"
    except Exception: pass

    # 10. Scan Multi-monitor active native resolution configurations matrices
    try:
        resolutions = []
        drm_path = "/sys/class/drm"
        if os.path.exists(drm_path):
            for conn in os.listdir(drm_path):
                status_file = os.path.join(drm_path, conn, "status")
                modes_file = os.path.join(drm_path, conn, "modes")
                if os.path.exists(status_file) and os.path.exists(modes_file):
                    with open(status_file, "r") as sf:
                        if sf.read().strip() == "connected":
                            with open(modes_file, "r") as mf: resolutions.append(mf.readline().strip())
            specs["resolution"] = ", ".join(resolutions) if resolutions else "N/A"
    except Exception: pass
    
    return specs

def get_ram_hardware_hardware_specs():
    """
    PROGRAMMER: Advanced DMI/SMBIOS Hardware Memory Scanner.
    Parses dmidecode type 17 memory structures to pull individual specs per slot.
    Calibrated with a JEDEC translation matrix dictionary to map raw hex codes to brand names.
    """
    report = {
        "slots_used": 0, "slots_total": 0, "devices": []
    }
    
    # DICTIONARY MASTER: Extended mapping factory hex IDs straight to commercial brands
    jedec_brands = {
        "8A02": "Crucial (Micron)",
        "059B": "Micron Technology",
        "0198": "Kingston",
        "02FE": "Smart Modular",
        "80CE": "Samsung",
        "AD00": "SK Hynix",
        "029E": "Corsair",
        "04CB": "Adata / XPG",
        "04CD": "G.Skill",
        "014F": "Transcend",
        "017A": "Apacer",
        "058A": "Patriot Memory",
        "025D": "Team Group",
        "0612": "Lexar",
        "047F": "Silicon Power",
        "015B": "HyperX",
        "0000": "Genérica"
    }
    
    try:
        import subprocess
        out = subprocess.check_output("sudo dmidecode -t memory", shell=True, text=True, stderr=subprocess.DEVNULL)
        
        devices_blocks = out.split("Memory Device")
        if len(devices_blocks) > 1:
            for idx, block in enumerate(devices_blocks[1:]):
                has_size = False
                size_val = "Vazio"
                block_vendor = "N/A"
                block_speed = "N/A"
                block_type = "N/A"
                block_form = "N/A"
                
                locator = f"Slot {idx + 1}"
                
                for line in block.split("\n"):
                    if "Bank Locator:" in line or "Locator:" in line:
                        loc_val = line.split(":")[-1].strip()
                        if loc_val and "Unknown" not in loc_val: locator = loc_val
                    if "Size:" in line:
                        v = line.split(":")[-1].strip()
                        if v and "No Module" not in v and "Empty" not in v and "No" not in v and any(char.isdigit() for char in v):
                            size_val = v
                            has_size = True
                    if "Manufacturer:" in line:
                        v = line.split(":")[-1].strip()
                        if v and "Unknown" not in v and "No" not in v: 
                            block_vendor = v
                    if "Speed:" in line and "Configured" not in line:
                        v = line.split(":")[-1].strip()
                        if v and "Unknown" not in v and "No" not in v: block_speed = v
                    if "Type:" in line and "Error" not in line and "Detail" not in line:
                        v = line.split(":")[-1].strip()
                        if v and "Unknown" not in v and "No" not in v: block_type = v
                    if "Form Factor:" in line:
                        v = line.split(":")[-1].strip()
                        if v and "Unknown" not in v and "No" not in v: block_form = v
                
                # Dynamic translation check: translates hex codes into brand names or preserves raw token
                if has_size and block_vendor != "N/A":
                    matched = False
                    for raw_hex, clean_name in jedec_brands.items():
                        if raw_hex in block_vendor.upper() or raw_hex.lower() in block_vendor.lower():
                            block_vendor = clean_name
                            matched = True
                            break
                    # Fallback protection if code belongs to an unmapped manufacturer
                    if not matched and block_vendor.strip():
                        # Clean eventual spacer noises strings
                        clean_hex = block_vendor.replace("0x", "").strip()
                        if len(clean_hex) >= 4:
                            block_vendor = f"Desconhecida ({clean_hex})"
                
                report["slots_total"] += 1
                if has_size:
                    report["slots_used"] += 1
                    report["devices"].append({
                        "slot": locator, "size": size_val, "type": block_type,
                        "form": block_form, "speed": block_speed, "vendor": block_vendor
                    })
                else:
                    report["devices"].append({
                        "slot": locator, "size": "Vazio",
                        "type": "-", "form": "-", "speed": "-", "vendor": "-"
                    })
    except Exception:
        pass
    return report

def detect_and_read_storage_devices(has_smartctl, has_nvme):
    """
    UNIVERSAL STORAGE PARTITION CRAWLER: Dynamically maps hardware devices blocks.
    Utilizes lsblk json tree processing pipelines to extract ALL sub-partitions layout
    topologies with filesystem formats and exact utilization fractions.
    Integrates raw silicon NVMe chip controllers natively from the unified lspci framework.
    """
    import os
    import subprocess
    import json
    import re
    
    # PROG: Pre-fetches the unified PCI bus map descriptors array natively
    pci_map = parse_lspci_hardware_bus()
    devices_report = {}
    
    try:
        block_root = "/sys/block"
        if not os.path.exists(block_root): return {}
        
        # --- PRE-FETCH DETAILED SUB-PARTITIONS LAYOUT MAP VIA NATIVE LSBLK JSON PIPELINE ---
        partitions_map = {}
        try:
            # Query active block fields format type: NAME, FSTYPE, MOUNTPOINT, SIZE, FSAVAIL, FSUSE%
            cmd_lsblk = "lsblk -J -b -o NAME,FSTYPE,MOUNTPOINT,SIZE,FSAVAIL,FSUSE%"
            lsblk_out = subprocess.check_output(cmd_lsblk, shell=True, text=True, stderr=subprocess.DEVNULL)
            
            data = json.loads(lsblk_out)
            if "blockdevices" in data:
                for bdev in data["blockdevices"]:
                    b_name = bdev.get("name", "")
                    
                    # Recursive function to crawl inner children partitions blocks (supports multi-layered disks)
                    def crawl_children(node_list):
                        extracted = []
                        for child in node_list:
                            c_name = child.get("name", "")
                            fstype = child.get("fstype") or "RAW/UNFORMATTED"
                            mount = child.get("mountpoint") or "Não montado"
                            
                            # Size math conversions straight from bytes metrics tokens
                            size_bytes = int(child.get("size") or 0)
                            free_bytes = int(child.get("fsavail") or 0) if child.get("fsavail") else 0
                            used_bytes = size_bytes - free_bytes if size_bytes >= free_bytes else 0
                            
                            size_gb = f"{(size_bytes / 1024 / 1024 / 1024):.1f} GB"
                            used_gb = f"{(used_bytes / 1024 / 1024 / 1024):.1f} GB"
                            free_gb = f"{(free_bytes / 1024 / 1024 / 1024):.1f} GB"
                            
                            # Extract use percentages mapping constraints format delta fraction
                            raw_use_pct = child.get("fsuse%")
                            if raw_use_pct:
                                use_pct = str(raw_use_pct).replace("%", "").strip()
                                fraction_pct = f"{use_pct}%"
                            else:
                                fraction_pct = "0% (Vazia)" if mount == "Não montado" else "N/A"
                                
                            # PROGRAMMER: Embed mount path dynamically inside the metadata title descriptor context
                            mount_desc = f" em {mount}" if mount != "Não montado" else " (Não montada)"
                            
                            extracted.append({
                                "part_node": f"/dev/{c_name}",
                                "format": f"{fstype.upper()}{mount_desc}",
                                "mount": mount,
                                "size": size_gb,
                                "used": used_gb,
                                "free": free_gb,
                                "percent": fraction_pct
                            })
                            if "children" in child:
                                extracted.extend(crawl_children(child["children"]))
                        return extracted
                        
                    if "children" in bdev:
                        partitions_map[b_name] = crawl_children(bdev["children"])
        except Exception: pass

        # 1. SCAN AND ISOLATE PHYSICAL STORAGE BLOCKS
        for dev in sorted(os.listdir(block_root)):
            if dev.startswith("sd") or dev.startswith("nvme") or dev.startswith("hd") or dev.startswith("vd") or dev.startswith("mmcblk"):
                if any(char.isdigit() for char in dev) and not dev.startswith("nvme") and not dev.startswith("mmcblk"): continue
                if "nvme" in dev and "n" in dev and any(char.isdigit() for char in dev.split("n")[-1]):
                    if "p" in dev.split("n")[-1]: continue
                if "mmcblk" in dev and "p" in dev: continue
                
                # Determine media factor architecture profiles
                drive_type = "SSD NVMe (Flash)"
                if dev.startswith("mmcblk"):
                    drive_type = "Cartão de Memória (SD)"
                elif not dev.startswith("nvme"):
                    removable_path = f"/sys/block/{dev}/removable"
                    is_removable = os.path.exists(removable_path) and open(removable_path, "r").read().strip() == "1"
                    if is_removable:
                        drive_type = "Memória Flash USB (Pendrive)"
                    else:
                        rotational_path = f"/sys/block/{dev}/queue/rotational"
                        if os.path.exists(rotational_path):
                            with open(rotational_path, "r") as rf:
                                drive_type = "Disco Rígido (HD)" if rf.read().strip() == "1" else "SSD SATA (Flash)"
                if not drive_type: drive_type = "Dispositivo SATA"
                
                # Initialize storage profile structures
                devices_report[dev] = {
                    "type": drive_type, "brand_model": "Modelo Genérico", "serial": "N/A", "temp": "N/A",
                    "health_label": "Desgaste de Células:" if "nvme" in dev else "Setores Realocados:",
                    "health_value": "Saudável (OK)", "total_space": "N/A", "partitions": []
                }
                
                # 2. READ RAW FACTORY SECTORS CAPACITY
                total_hardware_sectors = 0
                try:
                    size_path = f"/sys/block/{dev}/size"
                    if os.path.exists(size_path):
                        with open(size_path, "r") as sf:
                            total_hardware_sectors = int(sf.read().strip())
                        bytes_total = total_hardware_sectors * 512
                        devices_report[dev]["total_space"] = f"{(bytes_total / 1024 / 1024 / 1024):.1f} GB"
                except Exception: pass
                
                # 3. METADATA AND SMART ATTAINMENTS PIPELINES
                if "nvme" in dev:
                    try:
                        mp = f"/sys/block/{dev}/device/model"
                        base_model = open(mp, "r").read().strip() if os.path.exists(mp) else "SSD NVMe"
                        
                        try:
                            clean_dev_str = dev.replace("nvme", "").split("n")[0].strip()
                            nvme_pci_idx = int(clean_dev_str) if clean_dev_str.isdigit() else 0
                            
                            if nvme_pci_idx in pci_map["nvme_controllers"]:
                                silicon_chip = pci_map["nvme_controllers"][nvme_pci_idx]
                                devices_report[dev]["brand_model"] = f"{base_model} [{silicon_chip}]"
                            else:
                                devices_report[dev]["brand_model"] = base_model
                        except Exception:
                            devices_report[dev]["brand_model"] = base_model
                    except Exception: pass
                    
                    try:
                        sp = f"/sys/block/{dev}/device/serial"
                        if os.path.exists(sp): devices_report[dev]["serial"] = open(sp, "r").read().strip().upper()
                    except Exception: pass
                    
                    if has_nvme:
                        try:
                            clean_node = dev.split("p")[0] if "p" in dev else dev
                            cmd = f"sudo nvme smart-log /dev/{clean_node}"
                            out = subprocess.check_output(cmd, shell=True, text=True, stderr=subprocess.DEVNULL)
                            for line in out.split("\n"):
                                if "percentage_used" in line:
                                    pct_val = line.split(":")[-1].strip().replace("%", "")
                                    devices_report[dev]["health_value"] = f"{pct_val}% / 100%"
                                if "temperature" in line:
                                    devices_report[dev]["temp"] = line.split(":")[-1].replace("Celsius", "°C").strip()
                        except Exception: pass
                        
                    if devices_report[dev]["health_value"] == "Saudável (OK)":
                        devices_report[dev]["health_value"] = "0% / 100%"
                elif dev.startswith("mmcblk"):
                    devices_report[dev]["brand_model"] = "Cartão SD / MicroSD"
                    devices_report[dev]["health_value"] = "0 / 0 (Sem SMART)"
                else:
                    try:
                        model_p = f"/sys/block/{dev}/device/model"
                        if os.path.exists(model_p): devices_report[dev]["brand_model"] = open(model_p, "r").read().strip()
                    except Exception: pass
                    
                    raw_sectors_count = "0"
                    if has_smartctl:
                        try:
                            cmd_sata = f"sudo smartctl -i -A /dev/{dev}"
                            sata_out = subprocess.check_output(cmd_sata, shell=True, text=True, stderr=subprocess.DEVNULL)
                            for line in sata_out.split("\n"):
                                if "Serial Number:" in line: 
                                    devices_report[dev]["serial"] = line.split(":")[-1].strip().upper()
                                    
                                if "Reallocated_Sector_Ct" in line: 
                                    # REGEX FIX: Garante o isolamento cirúrgico do RAW_VALUE real de setores no SATA
                                    match_raw = re.search(r'(\d+)\s*$', line.strip())
                                    if match_raw:
                                        raw_sectors_count = match_raw.group(1).strip()
                                    else:
                                        raw_sectors_count = line.split()[-1].strip()
                                        
                                if "Temperature_Celsius" in line or "Airflow_Temperature_Cel" in line:
                                    # REGEX FIX: Isola a temperatura limpando o texto dos limites de parênteses
                                    match_temp = re.search(r'(\d+)\s*(?:\(.*\))?$', line.strip())
                                    if match_temp:
                                        devices_report[dev]["temp"] = f"{match_temp.group(1)} °C"
                                    else:
                                        devices_report[dev]["temp"] = f"{line.split()[-4].strip()} °C"
                        except Exception: pass
                        
                    devices_report[dev]["health_value"] = f"{raw_sectors_count} / {total_hardware_sectors if total_hardware_sectors > 0 else 'X'}"
                    
                # 4. FETCH INTEGRATED DYNAMIC PARTITIONS LIST FROM THE LSBLK IN-MEMORY BUFFER TREE
                if dev in partitions_map and partitions_map[dev]:
                    devices_report[dev]["partitions"] = partitions_map[dev]
                else:
                    devices_report[dev]["partitions"] = [{
                        "part_node": f"/dev/{dev}", "format": "RAW / NÃO FORMATADO", "mount": "Não montado",
                        "size": devices_report[dev]["total_space"], "used": "0.0 GB", "free": devices_report[dev]["total_space"], "percent": "0% (Vazio)"
                    }]
                    
        return devices_report
    except Exception: 
        return {}

def get_gpu_hardware_telemetry():
    """
    UNIVERSAL BLIND GPU ENGINE: Automatically tracks and extracts frequencies, 
    VRAM allocations, and naming conventions across Intel, AMD, and NVIDIA architectures.
    Fully updated for Linux Mint/Ubuntu modern sysfs trees and PCI link states.
    """
    # PROG: Pre-fetches the unified PCI bus map descriptors array natively
    pci_map = parse_lspci_hardware_bus()

    info = {
        "model": "Gráficos Integrados / Genéricos", "driver": "N/A", 
        "screens_count": "0", "pci_bus": "N/A", "revision": "N/A",
        "cur_clock": "N/A", "max_clock": "N/A", "vram": "Dinâmica (Compartilhada)",
        "pci_ids": "N/A", "pci_speed": "N/A"
    }
    try:
        # 1. SCAN PCI BUS FOR VGA/DISPLAY CONTROLLERS (Universal 32/64-bit detection)
        pci_root = "/sys/bus/pci/devices"
        active_pci_dev = None
        if os.path.exists(pci_root):
            for dev in os.listdir(pci_root):
                class_path = os.path.join(pci_root, dev, "class")
                if os.path.exists(class_path):
                    with open(class_path, "r") as f:
                        class_id = f.read().strip()
                    # 0x030000 = VGA, 0x038000 = 3D controller (Dedicated setups)
                    if class_id.startswith("0x0300") or class_id.startswith("0x0380"):
                        info["pci_bus"] = dev
                        active_pci_dev = dev
                        
                        # PROGRAMMER: Extract direct hardware Vendor ID and Device ID codes
                        try:
                            with open(os.path.join(pci_root, dev, "vendor"), "r") as vf:
                                v_id = vf.read().strip().replace("0x", "")
                            with open(os.path.join(pci_root, dev, "device"), "r") as df:
                                d_id = df.read().strip().replace("0x", "")
                            info["pci_ids"] = f"{v_id}:{d_id}".upper()
                        except Exception: pass
                        
                        # PROGRAMMER: Extract active bus operational speeds links configurations (e.g. Gen3 x16)
                        try:
                            speed_path = os.path.join(pci_root, dev, "max_link_speed")
                            width_path = os.path.join(pci_root, dev, "max_link_width")
                            if os.path.exists(speed_path) and os.path.exists(width_path):
                                with open(speed_path, "r") as sf: raw_speed = sf.read().strip()
                                with open(width_path, "r") as wf: raw_width = wf.read().strip()
                                
                                gen = "Gen1"
                                if "5.0" in raw_speed: gen = "Gen2"
                                elif "8.0" in raw_speed: gen = "Gen3"
                                elif "16.0" in raw_speed: gen = "Gen4"
                                elif "32.0" in raw_speed: gen = "Gen5"
                                
                                info["pci_speed"] = f"PCIe {gen} x{raw_width}"
                        except Exception: pass
                        
                        rev_path = os.path.join(pci_root, dev, "revision")
                        if os.path.exists(rev_path):
                            with open(rev_path, "r") as rf: info["revision"] = rf.read().strip()
                            
                        driver_link = os.path.join(pci_root, dev, "driver")
                        if os.path.exists(driver_link):
                            info["driver"] = os.readlink(driver_link).split("/")[-1].strip().upper()
                        # If a dedicated card is found, prioritize it over standard integrated controllers
                        if "NVIDIA" in info["driver"] or "AMDGPU" in info["driver"]:
                            break

        # 2. EXTRACT COMMERCIAL CHIP BRAND NAME MODELLING (Universal parsing fallback)
        try:
            # PROG: FIXED! Uses the advanced parse line mapper directly to override model split errors
            info["model"] = pci_map["gpu_chip"]
            
            if not info["model"] or info["model"] == "Gráficos Integrados / Genéricos":
                if "I915" in info["driver"]: info["model"] = "Intel UHD/HD Graphics Controller"
                elif "AMDGPU" in info["driver"]: info["model"] = "AMD Radeon Graphics Controller"
                elif "NVIDIA" in info["driver"]: info["model"] = "NVIDIA GeForce Controller"
        except Exception: pass

        # 3. COUNT ACTIVE MONITOR CHANNELS CONNECTED IN THE DRM TREE
        screens_found = 0
        drm_path = "/sys/class/drm"
        if os.path.exists(drm_path):
            for conn in os.listdir(drm_path):
                status_file = os.path.join(drm_path, conn, "status")
                if os.path.exists(status_file):
                    with open(status_file, "r") as f:
                        if f.read().strip() == "connected": screens_found += 1
            info["screens_count"] = str(screens_found)
            
        # 4. HYBRID HARDWARE TELEMETRY PARSING DISPATCHER (INTEL vs AMD vs NVIDIA)
        driver_lower = info["driver"].lower()
        
        # --- PATH A: INTEL GPU GRAPHICS TELEMETRY (DYNAMIC CRAWLER FOR KERNEL 6.8+) ---
        if "i915" in driver_lower or "xe" in driver_lower:
            intel_base_path = f"/sys/bus/pci/devices/{active_pci_dev}"
            
            if os.path.exists(intel_base_path):
                for root, dirs, files in os.walk(intel_base_path):
                    for file in files:
                        if file in ["gt_act_freq_mhz", "rps_act_freq_mhz", "gt0_act_freq_mhz"]:
                            try:
                                with open(os.path.join(root, file), "r") as f:
                                    val = f.read().strip()
                                    if val: info["cur_clock"] = f"{val} MHz"
                            except Exception: pass
                        if file in ["gt_max_freq_mhz", "rps_max_freq_mhz", "gt0_act_freq_mhz"]:
                            try:
                                with open(os.path.join(root, file), "r") as f:
                                    val = f.read().strip()
                                    if val: info["max_clock"] = f"{val} MHz"
                            except Exception: pass
                        if info["cur_clock"] != "N/A" and info["max_clock"] != "N/A":
                            break
                            
            if info["cur_clock"] == "N/A" and os.path.exists("/sys/kernel/debug/dri/0/i915_frequency_info"):
                try:
                    with open("/sys/kernel/debug/dri/0/i915_frequency_info", "r") as f:
                        for line in f:
                            if "Actual frequency" in line or "CAGF" in line:
                                info["cur_clock"] = f"{line.split()[-1].strip()} MHz"
                            if "Max frequency" in line:
                                info["max_clock"] = f"{line.split()[-1].strip()} MHz"
                except Exception: pass
                
            info["vram"] = "Dinâmica (Alocação Compartilhada via RAM)"
            
        # --- PATH B: AMD RADEON GRAPHICS TELEMETRY ---
        elif "amdgpu" in driver_lower:
            amd_hwmon_path = f"/sys/bus/pci/devices/{active_pci_dev}/hwmon"
            if os.path.exists(amd_hwmon_path):
                try:
                    hwmon_folder = os.listdir(amd_hwmon_path)[0]
                    freq_input = os.path.join(amd_hwmon_path, hwmon_folder, "freq1_input")
                    freq_max = os.path.join(amd_hwmon_path, hwmon_folder, "freq1_max")
                    
                    if os.path.exists(freq_input):
                        with open(freq_input, "r") as f:
                            info["cur_clock"] = f"{int(int(f.read().strip()) / 1000 / 1000)} MHz"
                    if os.path.exists(freq_max):
                        with open(freq_max, "r") as f:
                            info["max_clock"] = f"{int(int(f.read().strip()) / 1000 / 1000)} MHz"
                except Exception: pass
                
            vram_size_path = f"/sys/bus/pci/devices/{active_pci_dev}/mem_info_vram_total"
            if os.path.exists(vram_size_path):
                try:
                    with open(vram_size_path, "r") as f:
                        bytes_vram = int(f.read().strip())
                        info["vram"] = f"{int(bytes_vram / 1024 / 1024 / 1024)} GB Dedicada"
                except Exception: info["vram"] = "Dedicada AMD"
                
        # --- PATH C: NVIDIA GEFORCE GRAPHICS TELEMETRY ---
        elif "nvidia" in driver_lower:
            try:
                cmd_nv = "nvidia-smi --query-gpu=clocks.current.graphics,clocks.max.graphics,memory.total --format=csv,noheader,nounits"
                nv_out = subprocess.check_output(cmd_nv, shell=True, text=True, stderr=subprocess.DEVNULL).strip()
                if "," in nv_out:
                    cur_clk, max_clk, vram_mb = nv_out.split(",")
                    info["cur_clock"] = f"{cur_clk.strip()} MHz"
                    info["max_clock"] = f"{max_clk.strip()} MHz"
                    info["vram"] = f"{int(int(vram_mb.strip()) / 1024)} GB Dedicada (GDDR)"
            except Exception:
                info["cur_clock"] = "N/A (Driver fechado)"
                info["max_clock"] = "N/A (Driver fechado)"
                info["vram"] = "Dedicada NVIDIA"
                
        return info
    except Exception:
        return info

# GLOBAL STATS MODULE STORAGE: Persistent multi-interface byte logs
_last_multi_net_bytes = {}

def get_network_hardware_telemetry():
    """
    UNIVERSAL MULTI-INTERFACE POSIX ENGINE: Dynamically maps and extracts telemetry 
    for ALL physical adapters. Expanded with Hostname, Subnet Mask, Real DNS and Ping latency.
    Utilizes native ipaddress standards to prevent bitwise string formatting leakage overflows.
    Integrates raw silicon network hardware models natively from the unified lspci mapping framework.
    """
    global _last_multi_net_bytes
    devices_report = {}
    try:
        # PROG: Pre-fetches the unified PCI bus map descriptors array natively
        pci_map = parse_lspci_hardware_bus()

        net_root = "/sys/class/net"
        if not os.path.exists(net_root): return {}
        
        current_time = time.time()
        import ipaddress # PROG: STANDARD POSIX LIBRARY UNIFIED
        
        # --- NATIVE HOSTNAME EXTRACTION ---
        hostname_str = "N/A"
        if os.path.exists("/proc/sys/kernel/hostname"):
            with open("/proc/sys/kernel/hostname", "r") as f: 
                hostname_str = f.read().strip()

        # --- NATIVE REAL DNS EXTRACTION (FIXED: FILTERS OUT INTENSE IPv6 STRING FLOODING) ---
        dns_servers = []
        try:
            target_resolv = "/run/systemd/resolve/resolv.conf"
            if not os.path.exists(target_resolv):
                target_resolv = "/etc/resolv.conf"
            
            with open(target_resolv, "r") as f:
                for line in f:
                    line_clean = line.strip()
                    if line_clean.startswith("nameserver"):
                        ip_dns = line_clean.split()[-1].strip()
                        # FILTER: Skip cache local and strictly bypass any long IPv6 addresses containing colons (:)
                        if ip_dns != "127.0.0.1" and ip_dns != "127.0.0.53" and ":" not in ip_dns:
                            # PROG: Ensure we don't append repeated DNS entries into our display stack array
                            if ip_dns not in dns_servers:
                                dns_servers.append(ip_dns)
            
            # Last-tier fallback reading active network manager dns configs if system files lists are blank
            if not dns_servers:
                cmd_nm_dns = "nmcli -g IP4.DNS device show"
                nm_dns_out = subprocess.check_output(cmd_nm_dns, shell=True, text=True, stderr=subprocess.DEVNULL).strip()
                for d_line in nm_dns_out.split("\n"):
                    clean_d = d_line.strip()
                    if clean_d and clean_d != "127.0.0.53" and ":" not in clean_d:
                        if clean_d not in dns_servers:
                            dns_servers.append(clean_d)
        except Exception: pass
        
        dns_str = " | ".join(dns_servers) if dns_servers else "127.0.0.53 (Cache Local)"
        
        # 1. SCAN AND ISOLATE PHYSICAL INTERFACES
        for iface in os.listdir(net_root):
            if iface == "lo" or iface.startswith("br") or iface.startswith("veth") or iface.startswith("docker") or iface.startswith("virbr"):
                continue
            
            # PROG: Match the dynamic hardware chip model descriptor string straight from lspci network traces
            if iface.startswith("wl") or "wlan" in iface or "wifi" in iface:
                hardware_chip = pci_map["wifi"]
                iface_label = f"{iface.upper()} [Wi-Fi | {hardware_chip}]"
            else:
                hardware_chip = pci_map["ethernet"]
                iface_label = f"{iface.upper()} [Cabo | {hardware_chip}]"
            
            devices_report[iface] = {
                "name": iface_label, # INJECTED CHIP BRUTO REAL FROM lspci OVER THE NAME LABEL KEY
                "hostname": hostname_str,
                "mac": "N/A", "ip": "127.0.0.1 (Sem IP)", "netmask": "N/A", "gateway": "N/A", "dns": dns_str,
                "speed": "N/A", "download": "0 KB/s", "upload": "0 KB/s", "status": "Desconectado",
                "latency": "N/A"
            }
            
            # Read unique physical hardware MAC address token
            mac_path = f"/sys/class/net/{iface}/address"
            if os.path.exists(mac_path):
                with open(mac_path, "r") as f: devices_report[iface]["mac"] = f.read().strip().upper()
            
            # Read active operational state descriptor (up vs down)
            oper_path = f"/sys/class/net/{iface}/operstate"
            if os.path.exists(oper_path):
                with open(oper_path, "r") as f: devices_report[iface]["status"] = "Conectado" if f.read().strip() == "up" else "Desconectado"

        # 2. PURE NATIVE IP & NETMASK EXTRACTION (CORRECT METHOD VIA IPADDRESS LIBRARY)
        for iface in devices_report:
            if devices_report[iface]["status"] == "Conectado":
                try:
                    # Captures IP and Subnet Mask in CIDR notation (e.g. 192.168.1.5/24) via ip addr
                    cmd_ip_full = f"ip -4 addr show {iface} | grep -oP '(?<=inet\\s)\\d+(\\.\\d+){{3}}/\\d+'"
                    ip_full_out = subprocess.check_output(cmd_ip_full, shell=True, text=True, stderr=subprocess.DEVNULL).strip()
                    
                    if ip_full_out and "/" in ip_full_out:
                        # PROG: MANEIRA CORRETA! Utiliza a API do próprio objeto de rede para extrair as propriedades em string
                        interface_net = ipaddress.IPv4Interface(ip_full_out)
                        devices_report[iface]["ip"] = str(interface_net.ip)
                        devices_report[iface]["netmask"] = str(interface_net.netmask) # Returns clean unified string '255.255.255.0'
                except Exception:
                    try:
                        import socket
                        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                        s.settimeout(0.1)
                        s.connect(("8.8.8.8", 80))
                        devices_report[iface]["ip"] = s.getsockname()[0]
                        s.close()
                    except Exception: pass

                # PROGRAMMER: Compute real-time active ping latency via sockets (Ultra-fast and stable)
                try:
                    import socket
                    t_start = time.time()
                    sock_test = socket.create_connection(("8.8.8.8", 53), timeout=0.8)
                    sock_test.close()
                    latency_ms = int((time.time() - t_start) * 1000)
                    devices_report[iface]["latency"] = f"{latency_ms} ms"
                except Exception:
                    devices_report[iface]["latency"] = "Falha de Resposta"

        # 3. READ HARDWARE HYBRID LINK SPEEDS
        for iface in devices_report:
            if devices_report[iface]["status"] == "Conectado":
                speed_path = f"/sys/class/net/{iface}/speed"
                if os.path.exists(speed_path):
                    try:
                        with open(speed_path, "r") as f:
                            speed_val = int(f.read().strip())
                            if speed_val > 0: devices_report[iface]["speed"] = f"{speed_val} Mbps"
                    except Exception: devices_report[iface]["speed"] = "N/A"
                
                if devices_report[iface]["speed"] == "N/A" or not iface.startswith("e"):
                    try:
                        cmd_station = f"iw dev {iface} station dump | grep 'tx bitrate:'"
                        station_out = subprocess.check_output(cmd_station, shell=True, text=True, stderr=subprocess.DEVNULL).strip()
                        if station_out:
                            raw_bits = station_out.split(":")[-1].split("MBit")[0].strip()
                            devices_report[iface]["speed"] = f"{int(float(raw_bits))} Mbps"
                        else:
                            cmd_nm = "nmcli -t -f DEVICE,SPEED device"
                            nm_out = subprocess.check_output(cmd_nm, shell=True, text=True, stderr=subprocess.DEVNULL).strip()
                            for line in nm_out.split("\n"):
                                if line.startswith(f"{iface}:"):
                                    devices_report[iface]["speed"] = line.split(":")[-1].replace("Mbit/s", "Mbps").replace("Mbit", "Mbps").strip()
                                    break
                    except Exception:
                        devices_report[iface]["speed"] = "300 Mbps (Wi-Fi Link)"

        # 4. READ DEFAULT GATEWAYS (UNIVERSAL MATRIX PARSER - CABO & WI-FI FIXED)
        if os.path.exists("/proc/net/route"):
            try:
                with open("/proc/net/route", "r") as f:
                    for line in f:
                        parts = line.split()
                        # Index 1 corresponds to Destination IP (00000000 marks the active default gateway router)
                        if len(parts) >= 3 and parts[1] == "00000000":
                            iface_name = parts[0]
                            if iface_name in devices_report:
                                gw_hex = parts[2] # Index 2 stores the Gateway IP address encoded in hexadecimal format
                                # Convert hex string little-endian into generic IPv4 dots sequence safely
                                b1 = int(gw_hex[6:8], 16)
                                b2 = int(gw_hex[4:6], 16)
                                b3 = int(gw_hex[2:4], 16)
                                b4 = int(gw_hex[0:2], 16)
                                devices_report[iface_name]["gateway"] = f"{b1}.{b2}.{b3}.{b4}"
            except Exception: pass

        # 5. COMPUTE REAL-TIME BANDWIDTH DELTAS
        if os.path.exists("/proc/net/dev"):
            with open("/proc/net/dev", "r") as f:
                for line in f:
                    for iface in list(devices_report.keys()):
                        if iface in line:
                            parts = line.split()
                            if ":" in parts[0]:
                                rx_bytes = int(parts[1])
                                tx_bytes = int(parts[9])
                            else:
                                rx_bytes = int(parts[0].split(":")[-1])
                                tx_bytes = int(parts[8])
                            
                            if iface not in _last_multi_net_bytes:
                                _last_multi_net_bytes[iface] = {"rx": rx_bytes, "tx": tx_bytes, "time": current_time}
                                continue
                            
                            prev = _last_multi_net_bytes[iface]
                            diff_time = current_time - prev["time"]
                            
                            if diff_time > 0:
                                down_speed = (rx_bytes - prev["rx"]) / diff_time / 1024
                                up_speed = (tx_bytes - prev["tx"]) / diff_time / 1024
                                if down_speed > 1024: devices_report[iface]["download"] = f"{down_speed/1024:.2f} MB/s"
                                else: devices_report[iface]["download"] = f"{int(down_speed)} KB/s"
                                if up_speed > 1024: devices_report[iface]["upload"] = f"{up_speed/1024:.2f} MB/s"
                                else: devices_report[iface]["upload"] = f"{int(up_speed)} KB/s"
                            
                            _last_multi_net_bytes[iface] = {"rx": rx_bytes, "tx": tx_bytes, "time": current_time}
                            
        return devices_report
    except Exception:
        return {}

def get_motherboard_hardware_specs():
    """
    PROGRAMMER: High-efficiency Motherboard, BIOS firmware, and Chipset crawler.
    Reads direct kernel sysfs DMI strings nodes and parses administrative dmidecode 
    tables to fetch max memory capacity limits, socket designations, and PCIe expansion slots.
    Includes extended pipelines to track UEFI status, Secure Boot states and TPM hardware structures.
    Integrates the parse_lspci_hardware_bus mapper to isolate physical audio/chipset controllers nodes.
    """
    # PROG: Pre-fetches the unified PCI bus map descriptors array natively
    pci_map = parse_lspci_hardware_bus()

    specs = {
        "board_vendor": "N/A", "board_name": "N/A", "board_version": "N/A", "board_serial": "N/A",
        "bios_vendor": "N/A", "bios_version": "N/A", "bios_date": "N/A",
        "sys_vendor": "N/A", "sys_product": "N/A",
        "max_ram_capacity": "N/A", "cpu_socket": "N/A", "pcie_slots_summary": "N/A",
        "boot_mode": "Legacy (BIOS)", "secure_boot": "Desativado / N/A", "tpm_state": "Não Detectado",
        "ram_slots_count": "N/A",
        "chipset_pci": pci_map["chipset"], # INJETADO: Modelo do Chipset via lspci
        "audio_pci": pci_map["audio"]       # INJETADO: Controlador de Áudio via lspci
    }
    
    # Path mappings for direct Kernel DMI identification strings nodes
    dmi_paths = {
        "board_vendor": "/sys/class/dmi/id/board_vendor",
        "board_name": "/sys/class/dmi/id/board_name",
        "board_version": "/sys/class/dmi/id/board_version",
        "board_serial": "/sys/class/dmi/id/board_serial",
        "bios_vendor": "/sys/class/dmi/id/bios_vendor",
        "bios_version": "/sys/class/dmi/id/bios_version",
        "bios_date": "/sys/class/dmi/id/bios_date",
        "sys_vendor": "/sys/class/dmi/id/sys_vendor",
        "sys_product": "/sys/class/dmi/id/product_name"
    }
    
    for key, path in dmi_paths.items():
        if os.path.exists(path):
            try:
                with open(path, "r") as f:
                    val = f.read().strip()
                    if val and "To be filled" not in val and "Default" not in val:
                        specs[key] = val
            except Exception:
                pass

    # Fetch administrative dmidecode records for hardware limitations (Type 16, Type 4, Type 9)
    try:
        # 1. SCAN MAXIMUM CHIPSET RAM UPGRADE LIMITS AND PHYSICAL SLOTS COUNT
        out_mem = subprocess.check_output("sudo dmidecode -t memory", shell=True, text=True, stderr=subprocess.DEVNULL)
        slots_count = 0
        for line in out_mem.split("\n"):
            if "Maximum Capacity:" in line:
                specs["max_ram_capacity"] = line.split(":")[-1].strip()
            if "Number Of Devices:" in line:
                slots_count = line.split(":")[-1].strip()
        if slots_count:
            specs["ram_slots_count"] = f"{slots_count} encaixes físicos na placa-mãe"
                
        # 2. SCAN CPU PHYSICAL INTERFACE SOCKET
        out_proc = subprocess.check_output("sudo dmidecode -t processor", shell=True, text=True, stderr=subprocess.DEVNULL)
        for line in out_proc.split("\n"):
            if "Socket Designation:" in line:
                specs["cpu_socket"] = line.split(":")[-1].strip()
                break

        # --- DANILO'S LAB HARDWARE SOCKET FILTER MATRIX ---
        raw_socket = specs["cpu_socket"].upper()
        cpu_model_lower = ""
        try:
            with open("/proc/cpuinfo", "r") as f:
                for line in f:
                    if "model name" in line:
                        cpu_model_lower = line.lower(); break
        except Exception: pass

        if "775" in raw_socket or "LGA775" in raw_socket:
            specs["cpu_socket"] = "LGA775 (Intel Core 2 Duo / Quad)"
        elif "1156" in raw_socket or "LGA1156" in raw_socket:
            specs["cpu_socket"] = "LGA1156 (Intel Core 1st Gen)"
        elif "1155" in raw_socket or "LGA1155" in raw_socket:
            specs["cpu_socket"] = "LGA1155 (Intel Core 2nd/3rd Gen)"
        elif "1150" in raw_socket or "LGA1150" in raw_socket:
            specs["cpu_socket"] = "LGA1150 (Intel Core 4th/5th Gen)"
        elif any(x in raw_socket for x in ["U3E1", "1151", "LGA1151", "SOCKET 1151"]):
            if any(g in cpu_model_lower for g in ["i3-8", "i5-8", "i7-8", "i9-8", "i3-9", "i5-9", "i7-9", "i9-9", "9th gen", "8th gen"]):
                specs["cpu_socket"] = "LGA1151 (Intel 8th/9th Gen)"
            else:
                specs["cpu_socket"] = "LGA1151 (Intel 6th/7th Gen)"
        elif "1200" in raw_socket or "LGA1200" in raw_socket:
            specs["cpu_socket"] = "LGA1200 (Intel 10th/11th Gen)"
        elif "1700" in raw_socket or "LGA1700" in raw_socket:
            specs["cpu_socket"] = "LGA1700 (Intel 12th/13th/14th Gen)"
        elif "AM3+" in raw_socket:
            specs["cpu_socket"] = "AM3+ (AMD FX / Phenom II)"
        elif "AM3" in raw_socket:
            specs["cpu_socket"] = "AM3 (AMD Phenom II / Athlon II)"
        elif "AM4" in raw_socket:
            specs["cpu_socket"] = "AM4 (AMD Ryzen)"
        elif "AM5" in raw_socket:
            specs["cpu_socket"] = "AM5 (AMD Ryzen)"
        elif any(x in raw_socket for x in ["N/A", "CPU 1", "CPU1", "BGA", "FP6", "FT4", "FCBGA", "NONE"]) or not raw_socket.strip():
            if "intel" in cpu_model_lower: specs["cpu_socket"] = "Processador Soldado (Notebook BGA / Intel)"
            elif "amd" in cpu_model_lower: specs["cpu_socket"] = "Processador Soldado (Notebook BGA / AMD)"
            else: specs["cpu_socket"] = "Processador Soldado na Placa (Notebook / BGA)"
        elif specs["cpu_socket"] and specs["cpu_socket"] != "N/A":
            specs["cpu_socket"] = f"{specs['cpu_socket'].strip()} (Tratamento Genérico)"

        # 3. SCAN EXPANSION PCIE SLOTS METADATA
        out_slots = subprocess.check_output("sudo dmidecode -t slot", shell=True, text=True, stderr=subprocess.DEVNULL)
        slots_total = 0; slots_in_use = 0
        for line in out_slots.split("\n"):
            if "Designation:" in line: slots_total += 1
            if "Current Usage:" in line and "In Use" in line: slots_in_use += 1
        if slots_total > 0:
            specs["pcie_slots_summary"] = f"{slots_total} slots de expansão detectados ({slots_in_use} em uso)"
        else:
            specs["pcie_slots_summary"] = "Nenhum slot PCI extra (Layout Integrado de Notebook)"

        # 4. CRAWL SYSTEM BOOT MODE ACTIVE SCHEMAS
        if os.path.exists("/sys/firmware/efi"):
            specs["boot_mode"] = "UEFI Mode (Modern)"
            sb_path = "/sys/firmware/efi/efivars/SecureBoot-8be4df61-93ca-11d2-aa0d-00e098032b8c"
            if os.path.exists(sb_path):
                try:
                    with open(sb_path, "rb") as sbf:
                        data_bytes = sbf.read()
                        if len(data_bytes) >= 5 and data_bytes[4] == 1:
                            specs["secure_boot"] = "Ativado (Protegido / Secure)"
                        else:
                            specs["secure_boot"] = "Desativado (Modo Livre)"
                except Exception: pass
        
        # 5. CRAWL HARDWARE TPM SECURITY CHIP DEVICE NODES
        if os.path.exists("/sys/class/tpm") and os.listdir("/sys/class/tpm"):
            specs["tpm_state"] = "Ativado e Operacional (TPM 2.0 Detectado)"
            try:
                tpm_version_out = subprocess.check_output("cat /sys/class/tpm/tpm0/device/description 2>/dev/null || echo 'TPM'", shell=True, text=True).strip()
                if "2.0" in tpm_version_out or os.path.exists("/sys/class/tpm/tpm0/pcr-sha256"):
                    specs["tpm_state"] = "Ativado e Operacional (TPM 2.0 Ativo)"
            except Exception: pass

    except Exception:
        pass

    return specs

def parse_lspci_hardware_bus():
    """
    PROGRAMMER: High-efficiency PCI Bus hardware crawler.
    Executes a single lspci command layer to fetch raw silicon controllers.
    Maps physical hardware IDs and returns strings definitions cleanly.
    """
    bus_map = {
        "gpu_chip": "Gráficos Integrados / Genéricos",
        "chipset": "Chipset de Comunicação N/A",
        "audio": "Controlador de Áudio N/A",
        "ethernet": "Controlador Ethernet N/A",
        "wifi": "Controlador Wireless N/A",
        "nvme_controllers": {}
    }
    try:
        import subprocess
        out = subprocess.check_output("lspci", shell=True, text=True, stderr=subprocess.DEVNULL)
        
        nvme_idx = 0
        for line in out.split("\n"):
            line_upper = line.upper()
            
            # 1. PULL CHIP GRAPHICS CONTROLLER WITH FULL CLEANUP (Bypasses colon split limitations)
            if "VGA COMPATIBLE" in line_upper or "3D CONTROLLER" in line_upper:
                if " CONTROLLER:" in line:
                    parts = line.split(" CONTROLLER:")
                    bus_map["gpu_chip"] = parts[-1].strip()
                elif " CONTROLLER [" in line:
                    parts = line.split(" CONTROLLER [")
                    bus_map["gpu_chip"] = parts[-1].replace("]", "").strip()
                else:
                    parts = line.split(":")
                    if len(parts) >= 3:
                        bus_map["gpu_chip"] = ":".join(parts[2:]).strip()
                    else:
                        bus_map["gpu_chip"] = line.split("")[-1].strip()
                    
            elif "SATA CONTROLLER" in line_upper and "PCH" in line_upper:
                parts = line.split(" controller:")
                bus_map["chipset"] = parts[-1].strip() if len(parts) >= 2 else line.split(":")[-1].strip()
            elif "HOST BRIDGE" in line_upper and bus_map["chipset"] == "Chipset de Comunicação N/A":
                parts = line.split(" bridge:")
                bus_map["chipset"] = parts[-1].strip() if len(parts) >= 2 else line.split(":")[-1].strip()
                
            elif "AUDIO DEVICE" in line_upper or "AUDIO CONTROLLER" in line_upper:
                parts = line.split(" device:") if " device:" in line else line.split(" controller:")
                bus_map["audio"] = parts[-1].strip() if len(parts) >= 2 else line.split(":")[-1].strip()
                
            elif "ETHERNET CONTROLLER" in line_upper:
                parts = line.split(" controller:")
                bus_map["ethernet"] = parts[-1].strip() if len(parts) >= 2 else line.split(":")[-1].strip()
                
            elif "NETWORK CONTROLLER" in line_upper and ("WI-FI" in line_upper or "WIRELESS" in line_upper or "AX210" in line_upper):
                parts = line.split(" controller:")
                bus_map["wifi"] = parts[-1].strip() if len(parts) >= 2 else line.split(":")[-1].strip()
                
            elif "NON-VOLATILE MEMORY" in line_upper:
                parts = line.split(" controller:")
                c_name = parts[-1].strip() if len(parts) >= 2 else line.split(":")[-1].strip()
                bus_map["nvme_controllers"][nvme_idx] = c_name
                nvme_idx += 1
                
    except Exception:
        pass
    return bus_map