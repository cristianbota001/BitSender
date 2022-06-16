from socket import*
from threading import*
from pandas import*
import csv
import os
import shutil
from time import*
global sok
global database
global chat
global on_users

sok = {}
database = {}
gruppo_base = []
chat = {}
on_users = []

class Terminal(Thread):
    def __init__(self):
        Thread.__init__(self)
    def run(self):
        try:
            with open("utenti/database.csv", 'r') as file:
                read = csv.DictReader(file)
                for row in read:
                    database[row["nome"]] = row["pass"]
                    chat[row["nome"]] = None
        except:
            os.mkdir("utenti")
            with open("utenti/database.csv", 'w') as file:
                wr = csv.DictWriter(file, fieldnames = ["nome","pass"])
                wr.writeheader()
        try:
            with open("gruppi/gruppo_base.csv", 'r') as file:
                read = csv.DictReader(file)
                for row in read:
                    gruppo_base.append(row["nome"])
        except:
            os.mkdir("gruppi")
            with open("gruppi/gruppo_base.csv", 'w') as file:
                wr = csv.DictWriter(file, fieldnames = ["nome"])
                wr.writeheader()
        while True:
            mossa = input("mamba> ")
            if mossa == "sok":
                print(sok)
            if mossa == "on_users":
                print(on_users)
            if mossa == "database":
                print(read_csv("utenti/database.csv"))
            if mossa == "chat":
                print(chat)
            if mossa == "gruppi":
                print(gruppo_base)
            if mossa == "remove":
                rem = input("--> ")
                if rem in database:
                    lista = []
                    with open("utenti/database.csv", 'r') as file:
                        read = csv.reader(file)
                        for x in read:
                            lista.append(x)
                        utente_pass = database.pop(rem)
                        del chat[rem]
                        lista.remove([rem, utente_pass])
                        shutil.rmtree(rem)
                    with open("utenti/database.csv", 'w') as file:
                        write = csv.writer(file)
                        for x in lista:
                            write.writerow(x)
                            
class Server(Thread):
    def __init__(self, cl, ind):
        Thread.__init__(self)
        self.oggetto = cl
        self.indirizzo = ind

    def run(self): 
        class accesso_user():
            def __init__(self,oggetto,indirizzo):
                self.oggetto = oggetto
                self.indirizzo = indirizzo
                self.nome_acc = None
                while True:
                    try: 
                        data = oggetto.recv(4096)
                        mess = data.decode()
                        print("Messaggio arrivato: " + mess)
                        num = []
                        accesso_user.controllo_messaggio(self,mess,num)
                        if num[0][0:5] == "££##§":
                            accesso_user.iscrizione(self,num)
                        if num[0][0:5] == "££##@":
                            accesso_user.accesso(self,num)
                        if num[0][0:8] == "£££°°###":
                            self.search_gruppo_e_des(num)
                        for mess in num:
                            if mess[0:8] == "££##°@£#":
                                self.search(mess)
                            elif mess[0:8] == "##$$°@££":
                                self.rubrica(mess)
                            elif mess[0:7] == "£$£##°#":
                                self.spacc_e_trasm(mess)
                            elif mess[0:7] == "#$#££°£":
                                self.spacc_e_trasm_gru(mess)
                            elif mess[0:16] == "££$$sta_scrive##":
                                self.sta_scrive()
                            elif mess[0:6] == "#@#gru":
                                mess = mess.replace("#@#gru","")
                                self.nome_gruppo(mess)
                            elif mess[0:18] == "#@#çrichiesta_part":
                                self.gruppo_management(1,None,False)
                            elif mess[0:13] == "£££rem_partec":
                                rem = mess.replace("£££rem_partec","")
                                self.gruppo_management(2,rem,False)
                            elif mess[0:13] == "£££agg_partec":
                                agg = mess.replace("£££agg_partec","")
                                self.gruppo_management(3,agg,False)
                            elif mess[0:13] == "£££amm_partec":
                                amm = mess.replace("£££amm_partec","")
                                self.gruppo_management(4,amm,False)
                            elif mess[0:10] == "###rem_rub":
                                nome = mess.replace("###rem_rub","")
                                self.elimina_contatto(nome)
                            elif mess[0:14] == "#£#rem_rub_gru":
                                rem = mess.replace("#£#rem_rub_gru","")
                                self.gruppo_management(2,rem,True)
                            elif mess[0:14] == "##blocca_ute££":
                                num = mess.replace("##blocca_ute££","")
                                self.blocca_ute(num)
                            elif mess[0:12] == "##rem_file##":
                                rem = mess.replace("##rem_file##","")
                                self.rem_file(rem)
                            elif mess[0:11] == "##dolista$$":
                                self.download_des()
                            print("Messaggio arrivato: " + mess)
                    except:
                        self.uscita_management()
                        break

            #strumenti###############################################
            def controllo_messaggio(self,mess,num):
                while mess != "":
                    mes = mess.find("<--[°+°]-->",1)
                    bb = mess[0:mes]
                    mess = mess.replace(mess[0:mes] + "<--[°+°]-->","",1)
                    num.append(bb)
            
            def file_management(self,dire,moda,lista1,lista2,fieldname):
                if moda == "a":
                    with open(dire,moda) as file:
                        wr = csv.writer(file)
                        wr.writerow(lista1)
                if moda == "w":
                    with open(dire,moda) as file:
                        wr = csv.DictWriter(file, fieldnames = fieldname)
                        wr.writeheader()
                if moda == "r":
                    with open(dire,moda) as file:
                        rd = csv.DictReader(file)
                        for row in rd:
                            lista1.append(row[fieldname])
                if moda == "rr":
                    with open(dire,"r") as file:
                        rd = csv.DictReader(file)
                        for row in rd:
                            lista1.append(row[fieldname[0]])
                            lista2.append(row[fieldname[1]])
            #strumenti###############################################

            def iscrizione(self,num):
                nome_acc = num[0]
                pass1 = num[1]
                pass2 = num[2]
                nome_acc = nome_acc.replace("££##§","")
                pass1 = pass1.replace("££##§","")
                pass2 = pass2.replace("££##§","")
                if nome_acc in database:                       
                    self.oggetto.send(bytes("exist",'UTF-8'))
                elif pass1 == pass2:
                    self.oggetto.send(bytes("True",'UTF-8'))
                    database[nome_acc] = pass1
                    chat[nome_acc] = None
                    accesso_user.file_management(self,"utenti/database.csv","a",[nome_acc,pass1],None,None)
                    os.mkdir("utenti/" + nome_acc)
                    os.mkdir("FTP/" + nome_acc)
                    #accesso_user.file_management(self,nome_acc + "/rubrica.csv","w",None,["nome"])
                    accesso_user.file_management(self,"utenti/" + nome_acc + "/mess_acc.csv","w",None,None,["nome"])
                    accesso_user.file_management(self,"utenti/" + nome_acc + "/blocc.csv","w",None,None,["nome"])
                else:   
                    self.oggetto.send(bytes("nopass",'UTF-8'))           
            def accesso(self,num):
                self.nome_acc = num[0]
                self.nome_acc = self.nome_acc.replace("££##@","")
                pass_acc = num[1]
                pass_acc = pass_acc.replace("££##@","")
                if self.nome_acc in database:
                    if database[self.nome_acc] == pass_acc:
                        sok[self.nome_acc] = self.oggetto
                        self.oggetto.sendall(bytes("True", 'UTF-8'))
                        lista = []
                        accesso_user.file_management(self,"utenti/" + self.nome_acc + "/mess_acc.csv","r",lista,None,"nome")
                        for row in lista:
                            self.oggetto.sendall(bytes(row + "<--[°+°]-->",'UTF-8'))
                        accesso_user.file_management(self,"utenti/" + self.nome_acc + "/mess_acc.csv","w",None,None,["nome"])
                    else:
                        self.oggetto.send(bytes("False",'UTF-8'))
                else:
                    self.oggetto.send(bytes("Nodatabase",'UTF-8'))
            def search(self,search):       
                search = search.replace("££##°@£#","")
                if search in database:           
                    #self.file_management(self.nome_acc + "/rubrica.csv","a",[search],None)
                    lista = []
                    self.file_management("utenti/" + search + "/blocc.csv","r",lista,None,"nome")
                    if self.nome_acc not in lista:
                        searc = "$%&°ok" + search 
                        self.oggetto.sendall(bytes(searc + "<--[°+°]-->",'UTF-8'))
                        self.mess_acc(search,"%&nuovo!_ute#@" + self.nome_acc)
                        self.file_management("utenti/" + self.nome_acc + "/" + search + ".csv","w",None,None,["nome","mess"])
                        self.file_management("utenti/" + search + "/" + self.nome_acc + ".csv","w",None,None,["nome","mess"]) 
                        os.mkdir("FTP/" + self.nome_acc + "/" + search)
                        os.mkdir("FTP/" + search + "/" + self.nome_acc)
                    else:
                        self.oggetto.sendall(bytes("###False!$" + "<--[°+°]-->",'UTF-8')) 
                else:
                    self.oggetto.sendall(bytes("!*°False!$" + "<--[°+°]-->",'UTF-8')) 
            def mess_acc(self,des,ogg):
                if des in sok:
                    ricevente = sok[des]
                    ricevente.sendall(bytes(ogg + "<--[°+°]-->",'UTF-8'))
                else:
                    self.file_management("utenti/" + des + "/mess_acc.csv","a",[ogg],None,None)                 
            def nome_gruppo(self,nome):
                if nome not in gruppo_base:
                    self.oggetto.sendall(bytes("!!okok!!#@ò" + "<--[°+°]-->","UTF-8"))
                else:
                    self.oggetto.sendall(bytes("!!nono!!#@ò" + "<--[°+°]-->","UTF-8"))
            def search_gruppo_e_des(self,lista):
                for x in range(len(lista)):
                    lista[x] = lista[x].replace("£££°°###","")
                lista.append(self.nome_acc)
                nome_g = "#" + lista.pop(0)
                self.file_management("gruppi/" + nome_g + ".csv","w",None,None,["nome","amm"])
                self.file_management("gruppi/gruppo_base.csv","a",[nome_g],None,"nome")
                os.mkdir("FTP/" + nome_g)
                gruppo_base.append(nome_g)
                for x in lista:
                    self.file_management("utenti/" + x + "/" + nome_g + ".csv","w",None,None,["nome","mess"])
                    with open("gruppi/" + nome_g + ".csv","a") as file:
                        wr = csv.writer(file)       
                        if x == self.nome_acc:
                            wr.writerow([x,"Amm"])
                        else:
                            wr.writerow([x,"False"])
                            self.mess_acc(x,"%&nuovo!_ute#@" + nome_g)
            def gruppo_management(self,mod,ute,perm):
                lista1 = []
                lista2 = []
                diz = {}
                self.file_management("gruppi/" + self.des + ".csv","rr",lista1,lista2,["nome","amm"])
                for (a,b) in zip(lista1,lista2):
                    diz[a] = b
                if mod == 1:
                    for (nome,amm) in zip(lista1,lista2):
                        if nome == self.nome_acc:
                            mess = "###lista(Tu)"
                        else:
                            mess = "###lista" + nome
                        if amm == "True" or amm == "Amm":
                            mess = mess + " (amministratore)"
                        self.oggetto.sendall(bytes(mess + "<--[°+°]-->","UTF-8"))
                elif diz[self.nome_acc] == "True" or diz[self.nome_acc] == "Amm" or perm == True:
                    if mod == 2 and diz[ute] != "Amm" or ute == self.nome_acc:
                        os.remove("utenti/" + ute + "/" + self.des + ".csv")
                        self.mess_acc(ute,"###rem_rub_gru$£" + self.des)
                        self.file_management("gruppi/" + self.des + ".csv","w",None,None,["nome","amm"])
                        for (ogg1,ogg2) in zip(lista1,lista2):
                            if ogg1 != ute:
                                self.file_management("gruppi/" + self.des + ".csv","a",[ogg1,ogg2],None,None)               
                        chat[ute] = None
                    if mod == 3:
                        if ute not in lista1:
                            self.file_management("gruppi/" + self.des + ".csv","a",[ute,"False"],None,None)
                            self.file_management("utenti/" + ute + "/" + self.des + ".csv","w",None,None,["nome","mess"])
                            self.mess_acc(ute,"%&nuovo!_ute#@" + self.des)
                    if mod == 4:
                        self.file_management("gruppi/" + self.des + ".csv","w",None,None,["nome","amm"])
                        for (a,b) in zip(lista1,lista2):
                            if a == ute and diz[ute] != "Amm":
                                if b == "True":
                                    self.file_management("gruppi/" + self.des + ".csv","a",[a,"False"],None,None)
                                else:
                                    self.file_management("gruppi/" + self.des + ".csv","a",[a,"True"],None,None)       
                            else:
                                self.file_management("gruppi/" + self.des + ".csv","a",[a,b],None,None)
                    for x in lista1:
                        self.mess_acc(x,"##refreshlista##")
                else:
                    self.oggetto.sendall(bytes("###noamm!!" + "<--[°+°]-->","UTF-8"))
                self.contr_partec_gruppo()
            def contr_partec_gruppo(self):
                df = read_csv("gruppi/" + self.des + ".csv",encoding='latin1')
                if len(df) == 0:
                    os.remove("gruppi/" + self.des + ".csv")
                    gruppo_base.remove(self.des)
                    lista = []
                    self.file_management("gruppi/gruppo_base.csv","r",lista,None,"nome")
                    self.file_management("gruppi/gruppo_base.csv","w",None,None,["nome"])
                    lista.remove(self.des)
                    for x in lista:
                        self.file_management("gruppi/gruppo_base.csv","a",[x],None,None)
                    shutil.rmtree("FTP/" + self.des)
            def elimina_contatto(self,nome):
                os.remove("utenti/" + self.nome_acc + "/" + nome + ".csv")
                os.remove("utenti/" + nome + "/" + self.nome_acc + ".csv")
                shutil.rmtree("FTP/" + self.nome_acc + "/" + nome)
                shutil.rmtree("FTP/" + nome + "/" + self.nome_acc)
                self.mess_acc(nome,"###rem_rub_gru$£" + self.nome_acc)
                chat[self.nome_acc] = None
                chat[nome] = None
            def rubrica(self,mess):
                self.des = mess[8:]
                chat[self.nome_acc] = self.des
                df = read_csv("utenti/" + self.nome_acc + "/" + self.des + ".csv",encoding='latin1')
                lun = len(df)
                if lun != 0:
                    lista1 = []
                    lista2 = []
                    self.file_management("utenti/" + self.nome_acc + "/" + self.des + ".csv","rr",lista1,lista2,["nome","mess"])     
                    mess = "#####££" + "<--[°+°]-->"
                    for (nome,messaggio) in zip(lista1,lista2):
                        mess = mess + "#°òò!" + nome + "@" + messaggio + "<--[°+°]-->"
                    self.oggetto.sendall(bytes(mess,"UTF-8"))
                    self.file_management("utenti/" + self.nome_acc + "/" + self.des + ".csv","w",None,None,["nome","mess"])
            def spacc_e_trasm(self,msg):
                lista = []
                self.file_management("utenti/" + self.des + "/blocc.csv","r",lista,None,"nome")
                msg = msg.replace("£$£##°#","")
                numo = msg.find("§",1)
                nome = msg[0:numo]
                mess = msg.replace(nome + "§","")
                self.contr_invio_mess(nome,mess,self.des,self.nome_acc,lista)
            def contr_invio_mess(self,nome,mess,des,mitt,lista):
                if self.nome_acc not in lista:        
                    if chat[des] == mitt:
                        ricevente = sok[des] 
                        ricevente.sendall(bytes("#°òò!" + nome + "@" + mess + "<--[°+°]-->","UTF-8"))
                    else:
                        self.file_management("utenti/" + des + "/" + mitt + ".csv","a",[nome,mess],None,None)
                        self.mess_acc(des,"#$£noti##" + mitt)
                else:
                    self.oggetto.sendall(bytes("###False!$" + "<--[°+°]-->",'UTF-8'))
            def spacc_e_trasm_gru(self,msg):
                lista = []
                msg = msg.replace("#$#££°£","")
                numo = msg.find("§",1)
                nome = msg[0:numo]
                mess = msg.replace(nome + "§","")
                self.file_management("gruppi/" + self.des + ".csv","r",lista,None,"nome")
                lista.remove(self.nome_acc)
                for ut in lista:
                    self.contr_invio_mess(nome,mess,ut,self.des,[])
            def sta_scrive(self):
                if self.des[0] != "#":
                    lista = []
                    self.file_management("utenti/" + self.des + "/blocc.csv", "r", lista, None, "nome")
                    if chat[self.des] == self.nome_acc and self.nome_acc not in lista:
                        ricevente = sok[self.des]
                        ricevente.sendall(bytes("?ç°sta_scrive($" + self.nome_acc + "<--[°+°]-->",'UTF-8'))
                else:
                    lista = []
                    self.file_management("gruppi/" + self.des + ".csv","r",lista,None,"nome")
                    lista.remove(self.nome_acc)
                    for ut in lista:
                        if chat[ut] == self.des:
                            ricevente = sok[ut]
                            ricevente.sendall(bytes("?ç°sta_scrive($" + self.nome_acc + "<--[°+°]-->",'UTF-8'))
            def blocca_ute(self,mod):
                print("modd " + mod)
                if mod == "1":
                    self.file_management("utenti/" + self.nome_acc + "/blocc.csv","a",[self.des],None,None)
                else:
                    lista = []
                    self.file_management("utenti/" + self.nome_acc + "/blocc.csv","r",lista,None,"nome")
                    self.file_management("utenti/" + self.nome_acc + "/blocc.csv","w",None,None,["nome"])
                    for x in lista:
                        if x != self.des:
                            self.file_management("utenti/" + self.nome_acc + "/blocc.csv","a",[x],None,None)
            def download_des(self):
                if self.des[0] != "#":
                    lista = os.listdir("FTP/" + self.des + "/" + self.nome_acc)
                else:
                    lista = os.listdir("FTP/" + self.des)
                for x in lista:
                    self.oggetto.sendall(bytes("##do2££#" + x + "<--[°+°]-->","UTF-8"))
            def rem_file(self,rem):
                if self.des[0] != "#":
                    os.remove("FTP/" + self.nome_acc + "/" + self.des + "/" + rem)
                else:
                    os.remove("FTP/" + self.des + "/" + rem)
            
            
            
            
            
            
            
            
            
            
            def uscita_management(self):
                print("Host USCITO: ",self.indirizzo)
                try:
                    del sok[self.nome_acc]
                    chat[self.nome_acc] = None                
                except:
                    print("L'host non ha effettuato l'accesso.")
                on_users.remove(self.indirizzo)
        accesso_user(self.oggetto,self.indirizzo)

with socket(AF_INET, SOCK_STREAM) as so:
    so.bind(('', 8000))
    so.listen()
    terminal = Terminal()
    terminal.start()
    
    while True:
        cl, ind = so.accept()
        print(ind)
        on_users.append(ind)
        thread = Server(cl, ind)
        thread.start()