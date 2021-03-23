import socket

import sys

import traceback

import select

 

 

 

def make_room(client_socket,room_list):

	client_socket.send("0".encode())

	room_name = client_socket.recv(1024)

	client_id, client_port = client_socket.getpeername()

	room_list[client_id+":"+str(client_port)] = room_name.decode()

	print(client_id+":"+str(client_port)+" created room. the name is "+room_name.decode())

 

 

def show_list(client_socket,room_list):

	

	if len(room_list) == 0:

    		 client_socket.send("There is no room.".encode())

    		

	else:

            room_name_list=""

            for i,room_name in enumerate(room_list.values()):

                room_name_list+=str(i+1)+"."+room_name

                if i != len(room_list):

                    room_name += '\n'

 

            client_socket.send(room_name_list.encode())

 

 

def join_room(client_socket, room_list):

    client_socket.send("0".encode())

    req_room_name = client_socket.recv(1024)

    if req_room_name.decode() in list(room_list.values()):

        room_index = list(room_list.values()).index(req_room_name.decode())

        room_info = list(room_list.keys())[room_index]

        client_socket.send(room_info.encode())

    else:

        client_socket.send("fail".encode())

 

 

 

def show_list_to_server(room_list):

    if len(room_list) == 0:

        print("no room created")

    else:

        room_name_list=""

        for i,room_name in enumerate(room_list.values()):

            room_name_list+=str(i+1)+"."+room_name

            if i != len(room_list):

                room_name+="\n"

    print("####Room List###\n"+room_name_list)

 

 

########################### kill the room client created ################################

def kill_room(comm, client_socket_list, room_list):

    room_name = comm.split(" ")[1]                                              #extracting "the name of the room" from commmand string

 

    if room_name in room_list.values(): #check if the name of the room exists in room dictionary

        room_index = list(room_list.values()).index(room_name)                  # extract index of the room name from room dictionary

        room_info = list(room_list.keys())[room_index]                          # put the index number into the keys list that is extracted from room dictionary and then extract room's ip address, port that are indicated as "ip:port", string type.

        room_master_ip = room_info.split(":")[0]                                #extract only ip address from room information

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)                 #create socket for UDP communication

        sock.sendto("kill".encode(),(room_master_ip,5002))                      # send "kill" message to room master

        del room_list[room_info]                                                # delete the name of the room that server killed from room dictionary

        sock.close()                                                            #close UDP socket

 

    else:

        print("not existing room")

 

 

if __name__ == "__main__":

    HOST='localhost'

    PORT=5001

    server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server_socket.bind((HOST,PORT))

    server_socket.listen()

    client_socket_list = {} #ip:port : socket

    read_socket_list = [sys.stdin,server_socket]

    room_list={} #ip:port : room_name

 

    while True:

        conn_read_socket_list,conn_write_socket_list,conn_except_socket_list=select.select(read_socket_list,[],[])

 

        for conn_read_socket in conn_read_socket_list:

            if conn_read_socket == server_socket:

                print("requesting connection from client")

                client_socket,client_addr = server_socket.accept()

                client_socket_ip, client_socket_port = str(client_addr[0]),str(client_addr[1])

                print("{}:{} connected".format(client_socket_ip,client_socket_port))

                read_socket_list.append(client_socket)

                client_socket_list[client_socket_ip+":"+client_socket_port]=client_socket

 

            elif conn_read_socket in list(client_socket_list.values()):

                client_id, client_port = conn_read_socket.getpeername()

                data = conn_read_socket.recv(1024)

                if (not data) or (data.decode() == "/exit"):

                    read_socket_list.remove(conn_read_socket)

                    del client_socket_list[client_id+":"+str(client_port)]

                if client_id+":"+str(client_port) in room_list.keys():

                    del room_list[client_id+":"+str(client_port)]

                    conn_read_socket.close()

                    print(client_id+":"+str(client_port)+ " disconneted.")

                    break

            

                if data.decode() == "1":

                    make_room(conn_read_socket,room_list)

 

                elif data.decode() == "2":

                   show_list(conn_read_socket,room_list)

 

                elif data.decode() == "3":

                   join_room(conn_read_socket,room_list)

 

 

            elif conn_read_socket == sys.stdin:

                comm = conn_read_socket.readline()

                if comm.split(" ")[0] == "/ls\n" or comm.split(" ")[0] == "/ls":

                    show_list_to_server(room_list)

            

                elif  comm.split(" ")[0] == "/kill":

                    kill_room(comm, client_socket_list, room_list)

