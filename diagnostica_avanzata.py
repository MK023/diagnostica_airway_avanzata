import os
import sys
import time
import csv
import re
import platform
import subprocess
import traceback
from datetime import datetime

import ctypes  # Only for Windows

import psutil
import pingparsing
from ping3 import ping as ping3_ping
import speedtest

from scapy.all import traceroute, sr1, IP, ICMP

# --- Logging utilities ---

def log(msg, level="INFO"):
    """
    Print a timestamped log message.

    Args:
        msg (str): The message to log.
        level (str): The log level (e.g., INFO, WARNING, ERROR).
    """
    print(f"[{datetime.now():%Y-%m-%d %H:%M:%S}] [{level}] {msg}")

def log_error(msg, exc=None):
    """
    Log an error message and print traceback if exception is provided.

    Args:
        msg (str): The error message.
        exc (Exception, optional): The exception to log.
    """
    log(msg, level="ERROR")
    if exc:
        traceback.print_exc()

def format_float(val, decimals=2):
    """
    Format a value as a float with a specified number of decimals.

    Args:
        val: The value to format.
        decimals (int): Number of decimal places.

    Returns:
        str: Formatted float as string, or empty string if val is None or empty.
    """
    try:
        return f"{float(val):.{decimals}f}" if val not in (None, "") else ""
    except Exception:
        return str(val)

# --- Permissions and validation ---

def is_admin():
    """
    Check if the script is running with administrative/root privileges.

    Returns:
        bool: True if admin/root, False otherwise.
    """
    if os.name == "nt":
        try:
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        except Exception:
            return False
    return os.geteuid() == 0

def require_admin():
    """
    Exit the program if not running with admin/root privileges.
    """
    if not is_admin():
        log("Run this program as administrator/root!", level="CRITICAL")
        log("Windows: right-click → Run as administrator", level="CRITICAL")
        log("Linux/macOS: run with sudo", level="CRITICAL")
        sys.exit(99)

def is_valid_address(address):
    """
    Check if an address is a valid IPv4 or domain name.

    Args:
        address (str): The address to validate.

    Returns:
        bool: True if valid, False otherwise.
    """
    ip_pattern = r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$"
    domain_pattern = r"(?:[a-zA-Z0-9-]{1,63}\.)+[a-zA-Z]{2,}$"
    return re.match(ip_pattern, address) or re.match(domain_pattern, address)

def extract_ping_time(line):
    """
    Extract the ping time in milliseconds from a ping output line.

    Args:
        line (str): The line from ping output.

    Returns:
        float or None: Ping time in ms if found, else None.
    """
    match = re.search(r'(time|tempo|durata)[=<]?\s*=?\s*([\d\.,]+)\s*ms', line, re.IGNORECASE)
    if match:
        try:
            return float(match.group(2).replace(',', '.'))
        except ValueError:
            return None
    match2 = re.search(r'(min|avg|med|max|medio|media|massimo)\s*[=:]\s*([\d\.,]+)\s*ms', line, re.IGNORECASE)
    if match2:
        try:
            return float(match2.group(2).replace(',', '.'))
        except ValueError:
            return None
    return None

# --- Network diagnostic functions ---

def get_psutil_network_stats():
    """
    Get network statistics for all interfaces using psutil.

    Returns:
        list: List of dicts with interface stats.
    """
    try:
        net_io = psutil.net_io_counters(pernic=True)
        return [
            {
                "interface": iface,
                "bytes_sent": data.bytes_sent,
                "bytes_recv": data.bytes_recv,
                "packets_sent": data.packets_sent,
                "packets_recv": data.packets_recv,
                "errin": data.errin,
                "errout": data.errout,
                "dropin": data.dropin,
                "dropout": data.dropout
            }
            for iface, data in net_io.items()
        ]
    except Exception as e:
        log_error("psutil network stats error", exc=e)
        return []

def get_speedtest_results():
    """
    Run a speedtest and return ping, download, and upload speeds.

    Returns:
        dict: Speedtest results in bps and ms.
    """
    try:
        st = speedtest.Speedtest()
        st.get_best_server()
        return {
            "download_bps": round(st.download(), 2),
            "upload_bps": round(st.upload(), 2),
            "ping_ms": round(st.results.ping, 2)
        }
    except Exception as e:
        log_error("Speedtest error", exc=e)
        return {}

def get_pingparsing_results(address, count=10):
    """
    Run pingparsing and return parsed statistics.

    Args:
        address (str): Target address.
        count (int): Number of pings.

    Returns:
        dict: Parsed ping statistics.
    """
    try:
        ping_parser = pingparsing.PingParsing()
        transmitter = pingparsing.PingTransmitter()
        transmitter.destination = address
        transmitter.count = count
        stats = ping_parser.parse(transmitter.ping()).as_dict()
        for k in ["min_rtt", "avg_rtt", "max_rtt", "packet_loss_rate"]:
            if k in stats:
                stats[k] = format_float(stats[k], 2)
        return stats
    except Exception as e:
        log_error("Pingparsing error", exc=e)
        return {}

def get_ping3_result(address):
    """
    Perform a single ICMP ping using ping3.

    Args:
        address (str): Target address.

    Returns:
        float or str: Ping time in ms or empty string if no response.
    """
    try:
        result = ping3_ping(address, unit='ms')
        return round(result, 2) if result is not None else ""
    except Exception as e:
        log_error(f"ping3 error to {address}", exc=e)
        return ""

def get_scapy_traceroute(address, max_hops=20, timeout=2):
    """
    Perform traceroute using scapy.

    Args:
        address (str): Target address.
        max_hops (int): Max TTL.
        timeout (int): Timeout per hop.

    Returns:
        list: List of (ip, rtt_ms) tuples.
    """
    try:
        res, _ = traceroute([address], maxttl=max_hops, timeout=timeout, verbose=0)
        hops = []
        for idx, (snd, rcv) in enumerate(res):
            hop_ip = rcv.src if rcv else '*'
            rtt = (rcv.time - snd.sent_time)*1000 if rcv else None
            hops.append((hop_ip, round(rtt,2) if rtt is not None else None))
        return hops
    except Exception as e:
        log_error("Traceroute error", exc=e)
        return []

def get_scapy_icmp_ping(address, count=4, timeout=2):
    """
    Perform multiple ICMP pings using scapy.

    Args:
        address (str): Target address.
        count (int): Number of pings.
        timeout (int): Timeout per ping.

    Returns:
        list: List of ping times in ms or empty string for timeouts.
    """
    times = []
    for _ in range(count):
        try:
            pkt = IP(dst=address)/ICMP()
            ans = sr1(pkt, timeout=timeout, verbose=0)
            rtt = (ans.time - pkt.sent_time) * 1000 if ans is not None else None
            times.append(round(rtt, 2) if rtt is not None else "")
        except Exception as e:
            log_error(f"Scapy ICMP ping error to {address}", exc=e)
            times.append("")
    return times

def traceroute_str(hops):
    """
    Format traceroute hops as a string.

    Args:
        hops (list): List of (ip, rtt) tuples.

    Returns:
        str: Formatted traceroute string.
    """
    return "; ".join(f"{ip} ({format_float(rtt,2) if rtt is not None else 'timeout'})" for ip, rtt in hops)

# --- CSV writing ---

def write_csv(filename, header, rows):
    """
    Write rows to a CSV file, creating header if needed.

    Args:
        filename (str): File path.
        header (list): CSV header.
        rows (list): List of row lists.
    """
    write_header = not os.path.isfile(filename)
    with open(filename, "a", newline='') as csvfile:
        writer = csv.writer(csvfile)
        if write_header:
            writer.writerow(header)
        for row in rows:
            writer.writerow(row)

# --- Main diagnostic workflow ---

def advanced_diagnostics(address, filename="diagnostics.csv", delay=5):
    """
    Run the main diagnostic workflow:
    - Listen to ping output
    - When latency is high, perform detailed diagnostics
    - Write all relevant data to CSV

    Args:
        address (str): Target address.
        filename (str): Output CSV filename.
        delay (int): Delay between advanced diagnostics in seconds.
    """
    is_windows = platform.system().lower() == "windows"
    ping_cmd = ["ping", address, "-t"] if is_windows else ["ping", address]
    header = [
        "timestamp", "address", "ping_raw_line", "ping_ms_extracted",
        "pingparsing_min", "pingparsing_avg", "pingparsing_max", "pingparsing_packet_loss",
        "ping3_ms", "speedtest_ping_ms", "speedtest_download_bps", "speedtest_upload_bps",
        "iface", "iface_bytes_sent", "iface_bytes_recv", "iface_packets_sent", "iface_packets_recv",
        "iface_errin", "iface_errout", "iface_dropin", "iface_dropout",
        "scapy_ping_1_ms", "scapy_ping_2_ms", "scapy_ping_3_ms", "scapy_ping_4_ms",
        "scapy_traceroute"
    ]

    log("Running initial diagnostics...", level="INFO")
    speedtest_stats = get_speedtest_results()
    pingparsing_stats = get_pingparsing_results(address)
    scapy_ping_times = get_scapy_icmp_ping(address)
    scapy_traceroute_hops = get_scapy_traceroute(address)
    trace_str = traceroute_str(scapy_traceroute_hops)
    psutil_stats = get_psutil_network_stats()

    write_csv(filename, header, [])  # header only if not exists

    try:
        proc = subprocess.Popen(
            ping_cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            universal_newlines=True, shell=is_windows
        )
        log("Listening to ping output...", level="INFO")
        for line in proc.stdout:
            line = line.strip()
            if not line:
                continue
            tempo = extract_ping_time(line)
            if tempo is not None and tempo >= 90:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                ping3_ms = get_ping3_result(address)
                psutil_stats_now = get_psutil_network_stats()
                scapy_ping_times_now = get_scapy_icmp_ping(address)
                scapy_traceroute_hops_now = get_scapy_traceroute(address)
                trace_str_now = traceroute_str(scapy_traceroute_hops_now)
                rows = []
                # Write one row per interface
                if psutil_stats_now:
                    for iface_stat in psutil_stats_now:
                        row = [
                            timestamp, address, line, format_float(tempo,2),
                            pingparsing_stats.get("min_rtt", ""), pingparsing_stats.get("avg_rtt", ""), pingparsing_stats.get("max_rtt", ""), pingparsing_stats.get("packet_loss_rate", ""),
                            ping3_ms, speedtest_stats.get("ping_ms", ""), format_float(speedtest_stats.get("download_bps", ""),2), format_float(speedtest_stats.get("upload_bps", ""),2),
                            iface_stat["interface"], iface_stat["bytes_sent"], iface_stat["bytes_recv"], iface_stat["packets_sent"], iface_stat["packets_recv"],
                            iface_stat["errin"], iface_stat["errout"], iface_stat["dropin"], iface_stat["dropout"],
                            *(scapy_ping_times_now[i] if i < len(scapy_ping_times_now) else "" for i in range(4)),
                            trace_str_now
                        ]
                        rows.append(row)
                else:
                    # If no interface info, write a single row with blanks
                    row = [
                        timestamp, address, line, format_float(tempo,2),
                        pingparsing_stats.get("min_rtt", ""), pingparsing_stats.get("avg_rtt", ""), pingparsing_stats.get("max_rtt", ""), pingparsing_stats.get("packet_loss_rate", ""),
                        ping3_ms, speedtest_stats.get("ping_ms", ""), format_float(speedtest_stats.get("download_bps", ""),2), format_float(speedtest_stats.get("upload_bps", ""),2),
                        "", "", "", "", "", "", "", "", "",
                        *(scapy_ping_times_now[i] if i < len(scapy_ping_times_now) else "" for i in range(4)),
                        trace_str_now
                    ]
                    rows.append(row)
                write_csv(filename, header, rows)
                log(f"Advanced diagnostics written to CSV ({len(rows)} row(s)).", level="SUCCESS")
                time.sleep(delay)
    except KeyboardInterrupt:
        log("Stopped by user.", level="WARNING")
        sys.exit(0)
    except Exception as e:
        log_error("Error in diagnostics loop", exc=e)
        sys.exit(1)

# --- Entrypoint ---

def main():
    """
    Program entrypoint.
    - Checks for admin privileges
    - Requests target address
    - Starts diagnostics
    """
    require_admin()
    address = input("Enter IP address or domain to ping: ").strip()
    if not is_valid_address(address):
        log("Invalid address.", level="ERROR")
        sys.exit(2)
    log(f"Starting advanced diagnostics for: {address}", level="INFO")
    advanced_diagnostics(address)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        log_error("Fatal error at startup.", exc=e)
        sys.exit(1)