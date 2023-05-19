import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from subprocess import run, PIPE
from concurrent.futures import ThreadPoolExecutor
import queue
from ipaddress import ip_network, ip_address
import platform
import re


class App:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("NmPing")

        self.ip_range_label = tk.Label(self.window, text="IP Range:")
        self.ip_range_label.grid(row=0, column=0, padx=5, pady=5, sticky='w')

        self.ip_range_entry = tk.Entry(self.window)
        self.ip_range_entry.grid(row=0, column=1, padx=5, pady=5, sticky='ew')

        self.ping_button = tk.Button(self.window, text="Ping", command=self.ping_ips)
        self.ping_button.grid(row=0, column=2, padx=5, pady=5, sticky='e')

        self.stop_button = tk.Button(self.window, text="Stop", command=self.stop_pinging, state=tk.DISABLED)
        self.stop_button.grid(row=0, column=3, padx=5, pady=5, sticky='e')

        self.info_button = tk.Button(self.window, text="Info", command=self.show_info)
        self.info_button.grid(row=0, column=4, padx=5, pady=5, sticky='e')

        self.treeview = ttk.Treeview(self.window)
        self.treeview["columns"] = ("status", "ports")
        self.treeview.heading("#0", text="IP Address", command=lambda: self.sort_column("#0", False))
        self.treeview.column("#0", width=150)
        self.treeview.heading("status", text="Status")
        self.treeview.column("status", width=100)
        self.treeview.heading("ports", text="Open Ports")
        self.treeview.column("ports", width=300)
        self.treeview.grid(row=1, column=0, columnspan=5, padx=5, pady=5, sticky='nsew')

        self.window.grid_rowconfigure(1, weight=1)
        self.window.grid_columnconfigure(1, weight=1)

        self.result_queue = queue.Queue()
        self.window.after(100, self.check_queue)
        self.executor = None

        self.window.mainloop()

    def sort_column(self, col, reverse):
        l = [(self.treeview.set(k, col), k) for k in self.treeview.get_children('')]
        if col == "#0":
            l = [(self.treeview.item(k)["text"], k) for k in self.treeview.get_children('')]
        l.sort(reverse=reverse)
        for index, (val, k) in enumerate(l):
            self.treeview.move(k, '', index)
        self.treeview.heading(col, command=lambda: self.sort_column(col, not reverse))

    def check_queue(self):
        while not self.result_queue.empty():
            ip, status, open_ports_str = self.result_queue.get()
            self.treeview.insert("", "end", text=ip, values=(status, open_ports_str))
        self.window.after(100, self.check_queue)

    def ping_ips(self):
        ip_input = self.ip_range_entry.get().strip()

        if not ip_input:
            messagebox.showwarning("Validation Error", "Please enter an IP address or range.")
            return

        try:
            ip_list = self.parse_ip_input(ip_input)
        except ValueError as e:
            messagebox.showwarning("Validation Error", str(e))
            return

        for child in self.treeview.get_children():
            self.treeview.delete(child)

        self.ping_button.configure(state=tk.DISABLED)
        self.stop_button.configure(state=tk.NORMAL)

        self.executor = ThreadPoolExecutor(max_workers=50)
        for ip in ip_list:
            self.executor.submit(self.ping_ip, ip)

    def stop_pinging(self):
        if self.executor:
            self.executor.shutdown(wait=False)
            self.executor = None

        self.ping_button.configure(state=tk.NORMAL)
        self.stop_button.configure(state=tk.DISABLED)

    def parse_ip_input(self, ip_input):
        if "-" in ip_input:
            start_ip, end_ip = ip_input.split("-")
            start_parts = start_ip.split(".")
            end_parts = end_ip if "." in end_ip else start_parts[:-1] + [end_ip]
            return [str(ip_address(f"{start_parts[0]}.{start_parts[1]}.{start_parts[2]}.{i}")) for i in range(int(start_parts[3]), int(end_parts[3]) + 1)]
        elif "/" in ip_input:
            return [str(ip) for ip in ip_network(ip_input)]
        else:
            return [ip_input]

    def ping_ip(self, ip):
        ping_cmd = self.get_ping_cmd(ip)
        ping_process = run(ping_cmd, capture_output=True, text=True, timeout=5)

        if "Destination host unreachable" in ping_process.stdout:
            self.result_queue.put((ip, "Down", "N/A"))
            return

        is_alive = "1 packets received" in ping_process.stdout or "Received = 1" in ping_process.stdout
        if is_alive:
            nmap_cmd = ["nmap", "-p", "1-1000", ip]
            nmap_process = run(nmap_cmd, capture_output=True, text=True, timeout=10)
            if nmap_process.returncode == 0:
                open_ports = re.findall(r"(\d+/tcp.*open.*\w+)", nmap_process.stdout)
                open_ports = [' '.join(port.split()) for port in open_ports]
                open_ports_str = ", ".join(open_ports) if open_ports else "None"
                status = "Up"
            else:
                open_ports_str = "N/A"
                status = "Down"
        else:
            open_ports_str = "N/A"
            status = "Down"

        self.result_queue.put((ip, status, open_ports_str))

    @staticmethod
    def get_ping_cmd(ip):
        current_platform = platform.system().lower()
        return ["ping", "-c", "1", ip] if current_platform != "windows" else ["ping", "-n", "1", ip]

    def show_info(self):
        info_text = "NmPing\n\n" \
                    "A tool for pinging and port scanning multiple IP addresses.\n\n" \
                    "Usage:\n" \
                    "1. Enter an IP address or range in the IP Range field.\n" \
                    "2. Click on the Ping button to start pinging.\n" \
                    "3. The tool will display the status and open ports for each IP address.\n" \
                    "4. Use the Stop button to stop the pinging process.\n\n" \
                    "Note:\n" \
                    "- IP range can be specified in the following formats:\n" \
                    "  - Single IP: e.g., 192.168.1.100\n" \
                    "  - IP range: e.g., 192.168.1.100-150\n" \
                    "  - Subnet: e.g., 192.168.1.0/24"
        messagebox.showinfo("NmPing - Usage", info_text)


if __name__ == "__main__":
    App()
