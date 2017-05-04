import socket
import sys
import pickle
import select
import signal
import os

def main():
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	hostname = sys.argv[1]
	port = int(sys.argv[2])
	server_address = (hostname, port)
	sock.bind(server_address)
	sock.listen(1)
	sock.setblocking(0)

	epoll = select.epoll()
	epoll.register(sock.fileno(), select.EPOLLIN)

	try:
	    dic = pickle.load( open("fs.pkl", 'rb') )
	    files_db = dic.keys()
	except:
	    database = open("fs.pkl", 'a')
	    database.close()
	    dic = { }
	    pickle.dump(dic, open("fs.pkl", 'wb') )
	    dic = pickle.load( open("fs.pkl", 'rb') )
	    files_db = dic.keys()

	try:
	    data = ""
	    message = ""
	    connections = {}; recieved = {}; sent = {}; chunk_counter = {}
	    while True:
	        events = epoll.poll(1)
	        for fileno, event in events:
	            if fileno == sock.fileno():
	                connection, client_address = sock.accept()
	                connection.setblocking(0)
	                epoll.register(connection.fileno(), select.EPOLLIN)
	                connections[connection.fileno()] = connection
	                recieved[connection.fileno()] = ""
	                sent[connection.fileno()] = ""
	                chunk_counter[connection.fileno()] = 0
	            elif event & select.EPOLLIN:
	            	try:
		                connection = connections[fileno]
		                if recieved[fileno] == "":
		                    recieved[fileno] = connection.recv(16384)
		                    data = recieved[fileno]
		                    if data == "":
		                    	epoll.unregister(fileno)
		                    	connections[fileno].close()
		                    	del connections[fileno]
		                    if "OP_TERMINATE" in data:
		                    	break
		                    if data:
		                        filename = data[data.index(";") + 1:data.index(";", data.index(";") + 1)]
		                        filesize = data[data.index(";", data.index(";") + 1) + 1:]
		                        if filename not in files_db:
		                            backup_file = open(filename, 'a')
		                            backup_file.close()
		                            dic[filename] = [0, os.path.abspath(filename)]
		                            pickle.dump(dic, open("fs.pkl", 'wb') )
		                            files_db = dic.keys()
		                        backup_filesize = dic[filename][0]
		                        if (backup_filesize == int(filesize)):
		                            m_opcode1 = filename + ";" + "OP_ALREADY_HAVE"
		                            m_opcode1 = str((len(m_opcode1))) + ";" + m_opcode1
		                            sent[fileno] = m_opcode1
		                            epoll.modify(fileno, select.EPOLLOUT)
		                        else:
		                            m_opcode2 = filename + ";" + "OP_READY_TO_RECEIVE" + ";" + str(backup_filesize)
		                            m_opcode2 = str((len(m_opcode2))) + ";" + m_opcode2
		                            sent[fileno] = m_opcode2
		                            epoll.modify(fileno, select.EPOLLOUT)
		                else:
		                    recieved[fileno] = connection.recv(16384)
		                    message = recieved[fileno]
		                    if message == "":
		                    	epoll.unregister(fileno)
		                    	connections[fileno].close()
		                    	del connections[fileno]
		                    if "OP_TERMINATE" in message:
		                    	break
		                    if message:
		                    	filename = message[message.index(";") + 1:message.index(";", message.index(";") + 1)]
		                        payload = message[message.index(";", message.index(";") + 1) + 1:]
		                        backup_file = open(dic[filename][1], 'a+')
		                        backup_file.write(payload)
		                        backup_file.close()
		                        dic[filename][0] = dic[filename][0] + len(payload)
		                        pickle.dump(dic, open("fs.pkl", 'wb') )
		                        files_db = dic.keys()
		                        chunk_counter[fileno] += 1
		                        if len(payload) < 8192:
		                            m_opcode3 = filename + ";" + "OP_SYNC_COMPLETE" + ";" + str(chunk_counter[fileno])
		                            m_opcode3 = str((len(m_opcode3))) + ";" + m_opcode3
		                            sent[fileno] = m_opcode3
		                            epoll.modify(fileno, select.EPOLLOUT)
		                        else:
		                            m_opcode4 = filename + ";" + "OP_CHUNK_RECEIVED" + ";" + str(chunk_counter[fileno])
		                            m_opcode4 = str((len(m_opcode4))) + ";" + m_opcode4
		                            sent[fileno] = m_opcode4
		                            epoll.modify(fileno, select.EPOLLOUT)
	            	except:
		        		epoll.unregister(fileno)
		        		connections[fileno].close()
		        		del connections[fileno]
	            elif event & select.EPOLLOUT:
	                connections[fileno].send(sent[fileno])
	                if "OP_SYNC_COMPLETE" in sent[fileno] or "OP_ALREADY_HAVE" in sent[fileno]:
	                    epoll.modify(fileno, 0)
	                    connections[fileno].shutdown(socket.SHUT_RDWR)
	                else:
	                    epoll.modify(fileno, select.EPOLLIN)
	            elif event & select.EPOLLHUP:
	                epoll.unregister(fileno)
	                connections[fileno].close()
	                del connections[fileno]
	        if ("OP_TERMINATE" in data) or ("OP_TERMINATE" in message):
	            break

	except KeyboardInterrupt:
	    pass


	finally:
	    epoll.unregister(sock.fileno())
	    epoll.close()
	    sock.close()

if __name__ == '__main__':
	main()
