from socket import*
from threading import*
from time import*

#############################################################
class ftp_Transfer(Thread):
    def __init__(self,so,ind):
        self.so = so
        self.ind = ind
        Thread.__init__(self)
    def run(self):
        data = self.so.recv(4096)
        dire = data.decode()
        try:
            with open(dire,'rb') as file:
                while True:   
                    ff = file.read(4096) 
                    self.so.send(ff)
                    if not ff:
                        break
                    
                        
                    print(ff)
        except:
            self.so.sendall(bytes("##!!impossfile","UTF-8"))
            
                
class ftp_Server_Transfer(Thread):
    def __init__(self):
        Thread.__init__(self)
    def run(self):
        with socket(AF_INET, SOCK_STREAM) as so:
            so.bind(('', 1234))
            so.listen()
            while True:
                cl, ind = so.accept()
                print("FTP Transfer: ",ind)
                tr = ftp_Transfer(cl,ind)
                tr.start()

#############################################################



class ftp_Receiver(Thread):
    def __init__(self,so,ind):
        self.so = so
        self.ind = ind
        Thread.__init__(self)
    def run(self):
        data = self.so.recv(4096)
        dire = data.decode()
        with open(dire,"wb") as file:
            while True:
                data = self.so.recv(4096)
                print(data)
                file.write(data)
                if not data:
                    break
        


class ftp_Server_Receiver(Thread):
    def __init__(self):
        Thread.__init__(self)
    def run(self):
        with socket(AF_INET, SOCK_STREAM) as so:
            so.bind(('', 8888))
            so.listen()
            while True:
                cl, ind = so.accept()
                print("FTP Receiver: ",ind)
                re = ftp_Receiver(cl,ind)
                re.start()


ser1 = ftp_Server_Transfer()
ser1.start()
ser2 = ftp_Server_Receiver()
ser2.start()
