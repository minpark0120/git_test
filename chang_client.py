import socket
import sys
import select

Host = 'localhost'
Port = 5001
Port2 = 9999

def make_room(client_socket, room_No):
    client_socket.send('1'.encode()) # 서버로 1을 보내고
    if client_socket.recv(1024).decode() == "0": #서버로부터 0을 받는다면
        client_socket.send(room_No.encode()) #방번호를 보낸다
        print(str(room_No) + ' is created') # 방이 만들어졌다는걸 출력하고
        client_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #방에 손님을 받기위한 서버 소켓을 하나 더 생성한다.
        client_server_socket.bind(Host, Port2)
        client_server_socket.listen()
        request = client_server_socket.recv(1024) #클라이언트로부터 오는 request 메세지
        if request.decode() == '0': # 채팅소켓 연결 성공시
            client_client_socket, client_client_socket_addr = client_server_socket.accept() #socket.accept를 통해 연결을 받아들이고 conn과 address 쌍을 반환한다.
            client_client_socket_ip, client_client_socket_port = str(client_client_socket_addr[0]), str(client_client_socket_addr[1]) #addr[0]에 있는 ip주소와 addr[1]에 있는 port number를 반환한다
            client_server_socket.send('0'.encode()) #클라이언트에게 0을 encode해서 보낸다
            Name = client_server_socket.recv(1024).decode() #클라이언트로부터 이름을 받는다. 
            print("New client joined in the room!\nname : " + Name + "\naddr : " + client_client_socket_ip + ':', client_client_socket_port)# 어떤 클라이언트가 채팅 소켓에 참가하였는지 이름과 ip주소와 portnumber를 포함하여 출력한다.
       
      

def show_list(client_socket): 
    client_socket.send('2'.encode()) #서버로 2를 보내고
    list = client_socket.recv(1024) # 서버가 보내주는 리스트를 받는다
    print('--[Room List]--\n'+list.decode()) #받은 encode들 decode


def join_room(client_socket, room_No, Name):
    client_socket.send('3'.encode())  #서버로 3을 보내고
    if client_socket.recv(1024).decode() == "0": #서버로부터 0을 받는다면
        client_socket.send(room_No.encode()) # 서버로 방번호를 보내고
        room_info = client_socket.recv(1024).decode() # 방 정보를 받고
        print(room_info) # 출력한다
        client_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # 채팅방을 위한 클라이언트 소켓을 하나 더 생성한다.
        client_client_socket.connect(Host, Port2) # address에 있는 원격 소켓에 연결한다.
        client_client_socket.send('0'.encode()) # 채팅 서버에 0을 보낸다.
        if client_client_socket.recv(1024).decode() == '0':  #서버로부터 연결이 잘 되었다는 0을 받는다면
            client_client_socket.send(Name.encode()) # 자신의 이름을 채팅 서버로 보낸다.
            print("Room" + room_No + "joined") #어떤 방에 참가하였는지 출력한다.
            
        
        

def ban_client(client_server_socket, Name):
    think
    

if __name__ =='__main__':
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((Host, Port))
    client_server_socket = {} #딕셔너리 --> key 값에 접근, index로 접근 불가
    client_client_socket = {}
    state = 'wait' #state wait 상태로 설정
    while True: # 무한루프
        if state == 'wait': #만약 wait상태라면
            client_write = input('Enter Command: ')  #입력
            if client_write == '/ls': #/ls이라면
                show_list(client_socket) # show_list 으로 client_socket 소켓을 가지고감
            elif client_write == '/exit':#만약 exit이라면
                sys.exit("Client Ended") #sys 명령어중 exit을 통해 종료
            elif client_write[1] == 'c' and client_write[2] == 'r' and client_write[0] == '/' and client_write[3] == 'e' and client_write[4] == 'a' and client_write[5] == 't' and client_write[6] == 'e' : #/create라면
                command, room_No = client_write.split() #명령어 split으로 나누고
                make_room(client_socket, room_No) #make_room 으로  client_socket과 방번호를 가지고감
                state = 'create_chatting' #state를 채팅방 만든 상태로 바꾼다.
            elif client_write[1] == 'j' and client_write[2] == 'o' and client_write[0] == '/' and client_write[3] == 'i' and client_write[4] == 'n' :# join이라면
                if client_write[12] == '': # 이름을 안적었을 때
                    command, room_No = client_write.split() #split으로 두개만 나누고
                    Name == 'Unknown' # 이름은 Unknown으로 저장
                else:
                    command, room_No, Name = client_write.split() #join command와 방번호 이름을 split하고      
                join_room(client_socket, room_No, Name) # join_room으로 간다잇
                state = 'join_chatting' # state를 채팅방 참가한 상태로 바꾼다.
                    #본 방 들어가기 ifelse // 채팅state
            else: 
                print('Wrong Command') # 아니라면 잘못된 대기 상태 커멘드이다.

        elif state == create_chatting : #방 만든 상태의 채팅 상태라면
            for command in sys.stdin: # 시스템에 입력이 발생했을 때
                read_list = [sys.stdin, client_server_socket] # 입력과 채팅에 참가한 클라이언트로부터 오는 것 리스트 만들기
                read_socket, write_socket, except_socket = select.selct(read_list, [], []) # select함수로 소켓 계속 입력되게
                
                if command == ('/exit'): # command 가 /exit이라면 
                    state = 'wait' # 상태를 wait으로 바꾸고
                    client_server_socket.close() #서버를 닫는다.
                    print("Wait Mode") #상태가 바뀌었다는것을 출력한다.
                
                elif command[0] == ('/') and command[1] == ('b') and command[2] == ('a') and command[3] == ('n') : #/ban이라면
                    ban, Name = command.split() # 명령어를 split하고
                    ban_client(client_server_socket, Name) #ban으로 이름과 채팅 소켓을 챙긴다.
                        ##수정필요##

                else :    #입력되는 나머지
                    for r in read_socket :# read socket을 계속 돌리고 
                        if r == sys.stdin : #만약 루트의 입력이면
                            client_server_socket.send(sys.stdin.readline()) #클라이언트로 입력 보냄
                        elif r == client_server_socket: # 클라이언트로 부터 온 메세지라면
                            chatting = client_server_socket.recv(1024) #chatting에 온 메세지 받고
                            client_client_socket, client_client_socket_addr = client_server_socket.accept() # conn과 주소 대입
                            client_client_socket_ip, client_client_socket_port = str(client_client_socket_addr[0]), str(client_client_socket_addr[1]) # ip와 port 대입
                            if chatting != '': #메세지가 비어있지 않다면
                                print (client_client_socket_ip,' : ', client_client_socket_port, ' : ', chatting.decode()) # 출력
        else: #방 조인 상태의 채팅 상태라면
            for command in sys.stdin: #시스템에 입력이 발생했을 때, 
                read_list = [sys.stdin, client_server_socket] # 리스트 만들기
                read_socket, write_socket, except_socket = select.selct(read_list, [], []) # select함수로 소켓 계속 입력되게
                
                if command == ('/exit'): #exit command일시
                    state = 'wait' # 상태를 대기상태로 바꾸고
                    client_client_socket.close() #채팅 클라이언트를 닫는다
                    print("Wait Mode") # 대기상태 출력
                
                else :    
                    for r in read_socket :# read socket을 계속 돌리고
                        if r == sys.stdin : #만약 루트의 입력이면
                            client_client_socket.send(sys.stdin.readline()) #서버로 입력 보냄
                        elif r == client_client_socket: # 클라이언트의 매세지라면
                            chatting = client_client_socket.recv(1024) # 서버로부터의 메세지 보내고
                            client_server_socket, client_server_socket_addr = client_client_socket.accept() #온 주소 출력
                            client_server_socket_ip, client_server_socket_port = str(client_server_socket_addr[0]), str(client_server_socket_addr[1]) # ip, port 대입
                            if chatting != '': #매세지가 비어있지 않다면
                                print (client_server_socket_ip,' : ', chatting.decode()) # 출력

          
               
