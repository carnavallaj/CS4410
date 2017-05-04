import socket
import sys

def main():
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	hostname = sys.argv[1]
	port = int(sys.argv[2])
	filename = sys.argv[3]
	server_address = (hostname, port)
	sock.connect(server_address)

	try:
	    f = open(filename, 'r')
	    file = f.read()
	    filesize = len(file)
	    m_init = filename + ";" + str(filesize)
	    m_init = str((len(m_init))) + ";" + m_init
	    sock.sendall(m_init)

	    opcode = 0
	    while opcode != "OP_ALREADY_HAVE" and opcode != "OP_SYNC_COMPLETE":
	        data = sock.recv(8192)
	        if data:
	            opcode = data[data.index(";", data.index(";") + 1) + 1:]
	            if opcode == "OP_ALREADY_HAVE":
	                break
	            else:
	                opcode = data[data.index(";", data.index(";") + 1) + 1:data.index(";", data.index(";", data.index(";") + 1) + 1)]
	            if opcode == "OP_READY_TO_RECEIVE":
	                backup_filesize = data[data.index(";", data.index(";", data.index(";") + 1) + 1) + 1:]
	                if (filesize - int(backup_filesize)) < 8192:
	                    m_payload = filename + ";" + file[int(backup_filesize):]
	                else:
	                    m_payload = filename + ";" + file[int(backup_filesize):int(backup_filesize) + 8192]
	                m_payload = str((len(m_payload))) + ";" + m_payload
	                sock.sendall(m_payload)
	                while True:
	                    message = sock.recv(8192)
	                    if message:
	                        chunk_counter = int(message[message.index(";", message.index(";", message.index(";") + 1) + 1) + 1:])
	                        opcode = message[message.index(";", message.index(";") + 1) + 1:message.index(";", message.index(";", message.index(";") + 1) + 1)]
	                        if opcode == "OP_SYNC_COMPLETE":
	                            break
	                        else:
	                            backup_filesize = int(backup_filesize) + (8192)
	                            if (filesize - backup_filesize) < 8192:
	                                m_payload = filename + ";" + file[backup_filesize:]
	                            else:
	                                m_payload = filename + ";" + file[backup_filesize:backup_filesize + 8192]
	                            m_payload = str((len(m_payload))) + ";" + m_payload
	                            sock.sendall(m_payload)
	                break




	finally:
	    sock.close()

if __name__ == '__main__':
    main()

