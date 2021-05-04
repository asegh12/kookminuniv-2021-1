import socket
import sys
import os

host = ''
port = 0

if __name__=="__main__":
    try : 
        port = int(sys.argv[1])
    except:
        print("usage: python hw2 (port)")
        exit(1)
    print("Student ID : 20171680\nName : JunSeok Lee")
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((host, port))
    sock.listen()

    while(True) : 
        cli, cliadd = sock.accept()
        data = cli.recv(1024)
        print_get_msg = ''
        getmsg = data.decode().split()

        swtch = 0
        header = 0
        for i in range(len(data)):
            if data[i:i+6] == b'Accept' and swtch==0:
                swtch = 1
                print_get_msg = data[i:]
                print_get_msg = print_get_msg.decode()
            if data[i:i+2] == b'\r\n' : header += 1


        print('%s %s %s'%(getmsg[0], getmsg[1], getmsg[2]))
        print('Connection : Host IP %s, PORT %d, socket %d'%(cliadd[0], cliadd[1], sock.fileno()))
        print(print_get_msg)

        if not os.path.exists(getmsg[1][1:]):
            print('Server Error: No such file %s!'%getmsg[1])
            cli.send('HTTP/1.0 404 NOT FOUND\r\nConnection: close\r\nContent-Length: 0\r\nContent-Type: text/html\r\n\r\n'.encode())
            print(header, 'headers')
        else :
            sendsize = 0
            datasize = 0
            with open(getmsg[1][1:], 'r') as f:
                datasize = os.path.getsize('.'+getmsg[1])
                send_msg = "HTTP/1.0 200 OK\r\nConncetion: close\r\nContent-Length: "+str(datasize)+"\r\nContect-Type: text/html\r\n\r\n"
                cli.send(send_msg.encode())
                try:
                    send_data = f.read(1024)
                    while send_data:
                        sendsize += cli.send(send_data.encode())
                        send_data = f.read(1024)
                except Exception as ex:
                    print(ex)
            print(header, 'headers')
            print('finish', sendsize, datasize)
    cli.close()