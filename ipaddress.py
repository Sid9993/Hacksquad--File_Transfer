import nmap

def retrieve():
	ip = input("Enter the ip, default is 192.168.1.1/192.168.0.1:")
	l=[]
	if len(ip)==0:
		l.append(0)
		return False
	else:
		network = ip + '/24'
		print("Scanning please wait......")
		nm=nmap.PortScanner()
		nm.scan(hosts=network, arguments='-sn')
		host_list=[(x,nm[x]['status']['state']) for x in nm.all_hosts()]
		for host, status in host_list:
			l.append(host)
			print("host\t{}".format(host))
		choose=int(input("choose from the above ip:"))
		print(l[choose])
		return l[choose]

k=retrieve()
print(k)