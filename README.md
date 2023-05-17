Ping and Nmap Tool
This tool allows you to perform ping and Nmap port scan operations on a range of IP addresses.

Installation
Before you can run the tool, you need to have Python and Nmap installed on your machine.

You can download Python from here and Nmap from here.

This tool uses the tkinter library for the graphical user interface, which comes pre-installed with Python, and the concurrent.futures library for multi-threading.

Usage
To start the tool, navigate to the directory containing the Python script and run:
```
python3 ping_nmap_tool.py
```
You will see a window with an input field for the IP range, and a "Ping" button.

In the IP range field, you can either enter a single IP address or a range of IP addresses. The format for the range is xxx.xxx.xxx.xxx-yyy where xxx.xxx.xxx.xxx is the start IP and yyy is the last octet of the end IP. For example, you can input 192.168.1.1-50 to scan IP addresses from 192.168.1.1 to 192.168.1.50.

Once you've entered the IP range, click the "Ping" button to start the ping and Nmap operations. The tool will ping each IP address in the range, and if the ping is successful, it will perform an Nmap port scan on that IP.

The results will be displayed in a table below the input field. The table has three columns: "IP Address", "Status", and "Open Ports". The "IP Address" column shows the IP address that was scanned, the "Status" column shows whether the IP address is "Up" or "Down" (based on the ping result), and the "Open Ports" column shows the open ports found by the Nmap scan.
License
This project is licensed under the MIT License 
