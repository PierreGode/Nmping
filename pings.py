import tkinter as tk
from tkinter import ttk
import subprocess
import platform
import concurrent.futures
import queue

class App:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Ping and Nmap Tool")

        # Input fields
        self.ip_range_label = tk.Label(self.window, text="IP Range:")
        self.ip_range_label.grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.ip_range_entry = tk.Entry(self.window)
        self.ip_range_entry.grid(row=0, column=1, padx=5, pady=5, sticky='ew')
        self.ping_button = tk.Button(self.window, text="Ping", command=self.ping_ips)
        self.ping_button.grid(row=0, column=2, padx=5, pady=5, sticky='e')

        # Table to display results
        self.treeview = ttk.Treeview(self.window)
        self.treeview["columns"] = ("status", "ports")
        self.treeview.heading("#0", text="IP Address", command=lambda: self.sort_column("#0", False))
        self.treeview.column("#0", width=150)
        self.treeview.heading("status", text="Status")
        self.treeview.column("status", width=100)
        self.treeview.heading("ports", text="Open Ports")
        self.treeview.column("ports", width=300)
        self.treeview.grid(row=1, column=0, columnspan=3, padx=5, pady=5, sticky='nsew')

        # Configure the grid weights
        self.window.grid_rowconfigure(1, weight=1)
        self.window.grid_columnconfigure(1, weight=1)

        self.result_queue = queue.Queue()
        self.window.after(100, self.check_queue)

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
        ip_input = self.ip_range_entry.get()

        # Clear existing table entries
        for child in self.treeview.get_children():
            self.treeview.delete(child)

        ip_list = []
        if "-" in ip_input:
            start_ip, end_ip = ip_input.split("-")
            start_parts = start_ip.split(".")
            end_parts = end_ip if "." in end_ip else start_parts[:-1] + [end_ip]
            for i in range(int(start_parts[3]), int(end_parts[3])+1):
                ip = f"{start_parts[0]}.{start_parts[1]}.{start_parts[2]}.{i}"
                ip_list.append(ip)
        else:
            ip_list.append(ip_input)

        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.map(self.ping_ip, ip_list)

    def ping_ip(self, ip):
        current_platform = platform.system().lower()
        if current_platform == "windows":
            ping_process = subprocess.Popen(["ping", "-n", "1", ip], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        else:
            ping_process = subprocess.Popen(["ping", "-c", "1", ip], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        ping_output, _ = ping_process.communicate()
        if ("1 packets received" in str(ping_output)) or ("Received = 1" in str(ping_output)):
            status = "Up"
            nmap_process = subprocess.Popen([r"C:\Program Files (x86)\Nmap\nmap.exe", "-p", "1-1000", ip], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            nmap_output, _ = nmap_process.communicate()
            open_ports = [line.strip() for line in nmap_output.decode().split("\n") if "/tcp" in line and "open" in line]
            open_ports_str = ",".join(open_ports) if open_ports else "None"
        else:
            status = "Down"
            open_ports_str = "N/A"

        self.result_queue.put((ip, status, open_ports_str))


if __name__ == "__main__":
    App()
