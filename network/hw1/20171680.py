import socket

def get_parser(text):
	Host = ''
	port = ''
	get = ''
	user_agent = "HW1/1.0"
	connection = 'close'
	protocol = 'http'
	for i in range(len(text)):
		if(text[i:i+5] == 'https') : 
			protocol = 'https'
		if(text[i]+text[i+1] == "//") :
			i += 2
			while(text[i] != '/') :
				if(text[i] == ':') :
					while(True):
						i += 1
						if (text[i] == '/') : break 
						port += text[i]
					break
				Host += text[i]
				i += 1
			get = text[i:]
			break
		i +=1
	
	header_string = "GET "+get+" HTTP/1.0\r\n"+"HOST: "+Host+"\r\n"+"User-agent: "+user_agent+"\r\n"+"Connection: "+connection+"\r\n"+"\r\n"

	if port=='': port=80
	else : port = int(port)

	return protocol, header_string, Host, get, int(port)

def socket_connect(hstring, host, get, port):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		sock.connect((host, port))
	except :
		print("http %s %s %d %s"%(host, host, port, get))
		print("%s: unknown host"%(host))
		print("cannot connect to server %s %d\n"%(host, port))
		return;
	sock.sendall(hstring.encode())
	print(hstring)

	get_list = get.split('/')
	file_name = get_list[-1]

	data = b''
	totalsize = ''
	header_len = 0
	fir, sec = 1, 2
	while True:
		buf = sock.recv(1024)
		data += buf
		if(len(data)<=1024) : 
			i = 0
			#헤더 200 아닐경우 예외처리
			if (data[9:12] != b'200') :
				z = 9
				print_error = ''
				while(chr(data[z]) != '\r'):
					print_error += chr(data[z])
					z += 1
				print(print_error, end='\n\n')
				return;
			#데이터 크기 추출 및 분류
			while(totalsize == ''):
				if data[i:i+15] == b'Content-Length:':
					j = i+16
					while(True):
						if chr(data[j])=='\r' :
							totalsize = int(totalsize)
							break
						totalsize += chr(data[j])
						j += 1
					while(True):
						if data[j:j+4]==b'\r\n\r\n':
							header_len = j+4
							break
						j += 1
				i += 1
			print("Total Size "+str(totalsize)+" bytes")

		if(buf == b'') : break

		per = ((len(data)-header_len)/totalsize)*100
		if((per> fir*10) and (per < sec*10)):
			print("Current Downloading %d/%d (bytes) %d%%"%(len(data)-header_len, totalsize, per))
			fir += 1
			sec += 1
		elif per==100: print("Download Complete: %s, %d/%d\n"%(file_name, totalsize, totalsize))

	data = data[header_len:]
	myfile = open(file_name, 'wb')
	myfile.write(data)
	myfile.close()
	sock.close()

if __name__ == '__main__':
	print("Student ID : 20171680")
	print("Name : Junseok Lee\n")
	while(True):
		GetText = input("> ")
		if GetText=='quit' : exit()
		protocol, header, host, get, port = get_parser(GetText)
		if protocol=='http' : socket_connect(header, host, get, port)
		else : print("Only support http, not https")
