import socket
import sys
import select
HOST = 'localhost'                                     
PORT = 5001
UDP_PORT = 5002
ROOM_PORT = 9999




def make_room(client_socket,ms):
    client_socket.send("1".encode())
    if client_socket.recv(1024).decode() =="0":
        room_name = ms[8:]
        print(room_name)
        client_socket.send(room_name.encode())
        print("Room created")
        room_server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        room_server_socket.bind((HOST,ROOM_PORT))
        room_server_socket.listen()
        
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_socket.bind(("localhost",5002))
        
        
        client_socket_list = {}		#ip:port : socket
        read_list = [sys.stdin,room_server_socket,udp_socket]
        nick_list={}			#ip:port : nickname

        while True:    
            conn_read_list,conn_write_list,conn_except_list=select.select(read_list,[],[])






            for conn_read in conn_read_list:

                if conn_read == room_server_socket: 

                    print("requesting connection from client")
                    room_client_socket,client_addr = room_server_socket.accept()
                    nickname =  room_client_socket.recv(1024)
                    
                    if not nickname:
                        room_client_socket.close()
                        print("fail connection")              
                        
                 
                    print("New client joined in the room!")
                    print("name : "+nickname.decode())
                    room_client_ip, room_client_port = str(client_addr[0]),str(client_addr[1])
                    print("{}:{} joined".format(room_client_ip, room_client_port))
                    read_list.append(room_client_socket)
                    client_socket_list[room_client_ip+":"+room_client_port]=room_client_socket
                    nick_list[room_client_ip+":"+room_client_port]=nickname.decode()
		            
                elif conn_read == udp_socket:
                    udp_socket.close()
                    for cs in client_socket_list.values():
                        cs.send("kill_command".encode())
                    print("Room has been killed")
                    room_server_socket.close()
                    return 0
                		             
    		            
                elif conn_read in list(client_socket_list.values()):
                    room_client_ip, room_client_port = conn_read.getpeername()
                    client_info = room_client_ip+":"+str(room_client_port)
                    data = conn_read.recv(1024)

                    if (not data) or (data.decode() == "/exit"):
                        read_list.remove(conn_read)
                        del client_socket_list[client_info]
                        del nick_list[client_info]
                        conn_read.close()
                        print(client_info+ " disconneted.")
                        continue

                    nickname = nick_list[client_info]
                    print(nickname+" : "+data.decode())
                    for cs in client_socket_list.keys():
                        if (client_info) != cs:
                            msg = nickname+" : "+data.decode()
                            client_socket_list[cs].send(msg.encode())

                elif conn_read == sys.stdin:             
                    data = conn_read.readline()

                    if len(data.split(" ")) > 1 :
                        if data.split(" ")[0] == "/ban":
                            if data.split(" ")[1][:-2] in list(nick_list.values()):
                                for room_client_info, room_client_nick in nick_list.items():
                                    if room_client_nick == data.split(" ")[1]:
                                        read_list.remove(client_socket_list.get(room_client_info))
                                        client_socket_list.get(room_client_info).send("You have been banned".encode())
                                        client_socket_list.get(room_client_info).close()
                                        del client_socket_list[room_client_info]

                                        for cs in client_socket_list.values():
                                           cs.send(nick_list[room_client_info]+"("+room_client_info+")"+"is banned".encode())
                                        del nick_list[room_client_info]
                                continue                                    
                            else:
                                print("No client with the name "+data.split(" ")[1]+" exist in this room")
                                continue
                                    
                    msg = "root : "+data
                    for cs in client_socket_list.values():
                        cs.send(msg.encode())



    else:
        print("failed make room")






def show_list(client_socket):
    client_socket.send("2".encode())
    data = client_socket.recv(1024)
    print("####Room List###\n"+data.decode())








def join_room(client_socket,msg):
    client_socket.send("3".encode())
    if client_socket.recv(1024).decode() == "0":
        room_name = msg[6:]
        client_socket.send(room_name.encode())
        room_info =client_socket.recv(1024).decode()
        if room_info != "fail":
            room_info= room_info.split(":")[0]
            
            room_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            room_socket.connect((room_info,ROOM_PORT))
            q=0
            while (q != "yes") and (q != "no"):
                q = input("nickname? yes or no\n==>")
		    

            if q == "yes":
                nickname = input("nickname ==> ")
                room_socket.send(nickname.encode())
            else:
                room_socket.send("unknown".encode())

            room_socket_list=[sys.stdin, room_socket]
            while True:
                room_read_list,room_write_socket_list,room_except_socket_list=select.select(room_socket_list,[],[])
                for room_read_socket in room_read_list:
                    if room_read_socket == sys.stdin:
                        msg = room_read_socket.readline()
                        room_socket.send(msg.encode())
                        
                    else:
                        data = room_socket.recv(1024)
                        
                        if not data:
                            print('room is terminated')
                            room_socket.close()
                            return 0
                            
                        if data.decode() == "You have been banned":
                            room_socket.close()
                            print(data.decode())
                            return 0
                            
                        elif data.decode() == "kill_command":
                            print("Room has been killed")
                            room_socket.close()
                            return 0
                            
                        else:
                            print(data.decode())
        else:
            print("not existing")











if __name__=="__main__":

    client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client_socket.connect((HOST,PORT))
    read_socket_list=[sys.stdin,client_socket]
    command_dict = {"/create":1,"/ls":2}

    while True:
        if len(read_socket_list) != 1:
            conn_read_socket_list,conn_write_socket_list,conn_except_socket_list=select.select(read_socket_list,[],[])

            for conn_read_socket in conn_read_socket_list:
                if conn_read_socket == sys.stdin:
                    msg = conn_read_socket.readline()

                    if msg.split(" ")[0] == "/create":	
                        make_room(client_socket,msg)

                    elif msg.split(" ")[0] == "/ls\n" or msg.split(" ")[0] == "/ls":
					    
                        show_list(client_socket)

                    elif msg.split(" ")[0] == "/join":
                        join_room(client_socket,msg)
                    
                    elif msg.split(" ")[0] == "/exit\n":
                        client_socket.send("/exit".encode())
                        read_socket_list.remove(client_socket)
                        client_socket.close()
                        break
                                            
                    else:
                        print("not existed command")
                else:
                    if not conn_read_socket.recv(1024).decode():
                        print("master server is terminated")
                        conn_read_socket.close()

        else:
            break    

