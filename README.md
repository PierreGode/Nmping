Nmping is a simple ping tool that also shows open ports for each target.<p>
  
  ![image](https://github.com/PierreGode/Nmping/assets/8579922/c2ca1eb8-266f-435e-bf59-239adcd09913)


Requirements:
Python installed on your system.<p>
Install the required libraries:
```
pip install tkinter
```
and
```
python nmping.py
```

clone this repository:<p>

```
git clone https://github.com/PierreGode/Nmping.git
```

Install nmap on your system.<p>

Open a terminal or command prompt.
Navigate to the file's directory.
Run:
```
cd Nmping
```
```
python nmping.py
```
<p>
Using the Application:
Enter the IP address or range in the "IP Range" field.
Click "Ping" to start pinging.
View results in the treeview.
Click "Stop" to halt pinging.
Click "Info" for usage details.
IP Range Formats:
Single IP: Enter an IPv4 address (e.g., 192.168.1.100).
IP Range: Use hyphen for a range (e.g., 192.168.1.100-150).
Subnet: Employ CIDR notation (e.g., 192.168.1.0/24).
Note: The app pings IPs, checks their status, and performs port scans.
