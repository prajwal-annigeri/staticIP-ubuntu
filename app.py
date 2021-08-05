from flask import Flask, render_template, request, flash, redirect, url_for
import ipaddress
import subprocess
import re


app = Flask(__name__)
app.secret_key = "This is super secret"


@app.route('/')
def index():
	message = request.args.get('message')
	
	#ifconfig
	p1 = subprocess.run(['ifconfig'], capture_output = True, text=True)
	ifconf_res = (p1.stdout) #holds result of ifconfig
	
	
	#Getting the required pieces of text from the ifconfig output
	ipRegex = re.compile(r'inet .*')
	matches = ipRegex.findall(ifconf_res)
	
	#interface list
	int_lst = []

	#Code to extract interface names
	while 'collisions' in ifconf_res:
		int_lst.append(ifconf_res[:ifconf_res.index(':')].strip())
		ifconf_res = ifconf_res[ifconf_res.find('collisions')+12:]
	print(int_lst)
	#print(matches)
	
	#List of present interface addresses
	addressList = []
	
	#Extracting IP addresses with regex
	ipreg = re.compile(r'\d+.\d+.\d+.\d+')
	for match in matches:		
		addressList.append(ipreg.findall(match))

	#Dictionary to match present interfaces with their addresses
	int_dict = {}
	for interface, address in zip(int_lst, addressList):
		if interface == "lo":
			#loopback
			continue
		int_dict[interface] = [address[0], address[1]]
	if not int_dict:
		#No interfaces
		return render_template('error.html')
	return render_template('index.html', devs=int_dict)


@app.route('/success', methods=['POST', 'GET'])
def success():
    if request.method == 'GET':
    	#Method should be POST
        flash("Doesn't work like that")
        return redirect(url_for('index'))
    if request.method == 'POST':
    	#Data from the form submitted
        inputIP = request.form['newIP'].strip()
        inputDNS = request.form['newDNS'].strip()
        inputInt = request.form.get('interface')
        try:
        	#Checking if entered information is valid
            ip = ipaddress.ip_address(inputIP)
            dns = ipaddress.ip_address(inputDNS)
            
            
            #Checking if IP address is a private IP address
            if ip.is_private:
            	try:
            		#Checking if that IP address is already taken
            		p1 = subprocess.run(['ping', inputIP, '-c', '4'], capture_output=True, text=True, timeout=10)
            		ping_res = p1.stdout #Result of ping
            		
            		#If that IP address is available
            		if 'unreachable' in ping_res.lower():
            			yaml_str = 'network:\n  version: 2\n  ethernets:\n    {0}:\n      addresses: [{1}/24]\n      nameservers:\n        addresses: [{2}]'.format(inputInt, inputIP, inputDNS)
            			
            			#Writing to the .yaml file
            			with open('/etc/netplan/01-network-manager-all.yaml', 'w') as fp:
            				fp.write(yaml_str)
            			
            			#Applying changes made to the yaml file
            			subprocess.run(['sudo', 'netplan', 'apply'])
            			
            			return render_template('success.html', ip=inputIP, dns=inputDNS)
            		else:
            			flash("IP Unavailable")
            			return redirect(url_for('index'))
            	except:
            		#Ping timeout
            		flash("PING timeout")
            		return redirect(url_for('index'))
            else:
            #Public IP address entered
                flash("Please enter a private IP address")
                return redirect(url_for('index'))
        except ValueError:
        	#Not a proper address
            flash("Enter proper IP/DNS address")
            return redirect(url_for('index'))


if __name__ == "__main__":
    app.debug = True
    app.run()








