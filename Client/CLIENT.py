from tkinter import*
from tkinter import messagebox
from tkinter import filedialog
from playsound import playsound
from socket import*
from time import*
from threading import*
from pandas import*
import os
import csv
import re
num = []
so = socket(AF_INET, SOCK_STREAM)

def icona(win):
    try:
        win.iconbitmap("ico.ico")
    except:
        None
def hostname():
    win = Tk()
    win.geometry("300x220")
    win.resizable(False,False)
    win.title("BitSender")
    icona(win)
    win.config(bg = "#38475A")
    lab = Label(win,text = "Inserisci l'hostname", font = ("ebrima",14,), bg = "#38475A", fg = "white")
    lab.place(relx = 0.5,anchor=CENTER, y = 30)
    en = Entry(win, borderwidth = 0, width = 23, font = ("arial",14),bg = "#C6CDB8")
    en.place(relx = 0.5, anchor = CENTER, y = 60)
    bu = Button(win, text = "OK!",command = lambda: coll(en.get(),win),font = ("ebrima",14,), bg = "#334966", fg = "white", borderwidth = 1, relief = SOLID,width = 23)
    bu.place(relx = 0.5, anchor = CENTER, y = 130)

hostname()

def coll(name,win):
    try:
        win.destroy()
        ind = gethostbyname(name)
        so.connect((ind, 8000))
        schemata_principale(ind)
    except:
        hostname()

class schemata_principale():
    def __init__(self,ind):
        self.accesso_finestra(None)
        self.ind = ind
    def accesso(self,ogg,log1,log2,win):
        nome_acc = log1.get()
        pass_acc = log2.get()    
        if nome_acc != "" and pass_acc != "":
            ogg.sendall(bytes("££##@" + nome_acc + "<--[°+°]-->" + "££##@" + pass_acc + "<--[°+°]-->",'UTF-8'))
            data = ogg.recv(4096)
            destino = data.decode()

            if destino == "Nodatabase":
                messagebox.showwarning("Ops!","Account non esistente")
                log1.delete(0,END)
                log2.delete(0,END)
                
            if destino == "False":
                messagebox.showwarning("Ops!","Password errata!")
                log2.delete(0,END)

            if destino == "True":
                log1.delete(0,END)
                log2.delete(0,END)
                win.destroy()
                accesso_fatto(nome_acc,self.ind)

    def iscrizione(self,ogg,nome1,passw1,passw3,isc):
        nome_acc = nome1.get()
        pass1 = passw1.get()
        pass2 = passw3.get()

        if nome_acc != "" and pass1 != "" and pass2 != "":
            if not re.findall("[ -/-:-@-[-^-{-⁓]",nome_acc):
                nome_acc = "££##§" + nome_acc
                pass1 = "££##§" + pass1
                pass2 = "££##§" + pass2
                ogg.sendall(bytes(nome_acc + "<--[°+°]-->" + pass1 + "<--[°+°]-->" + pass2 + "<--[°+°]-->",'UTF-8'))
                
                data = ogg.recv(4096)
                destino = data.decode()

                if destino == "exist":
                    messagebox.showwarning("Ops!","Account già esistente!")
                    nome1.delete(0,END)
                    passw1.delete(0,END)
                    passw3.delete(0,END)

                if destino == "nopass":
                    messagebox.showwarning("Ops!","Riscrivere la password correttamente!")
                    passw1.delete(0,END)
                    passw3.delete(0,END)

                if destino == "True":
                    messagebox.showinfo("Congratulazioni!","Iscrizione terminata con successo!")
                    nome_acc = nome_acc.replace("££##§","")
                    os.mkdir(nome_acc)
                    accesso_fatto.file_management(None,nome_acc + "/" + "rubrica.csv","w",None,["nome"])
                    accesso_fatto.file_management(None,nome_acc + "/" + "notifica.csv","w",None,["nome","sound"])
                    accesso_fatto.file_management(None,nome_acc + "/" + "blocc.csv","w",None,["nome"])
                    nome1.delete(0,END)
                    passw1.delete(0,END)
                    passw3.delete(0,END)
                    isc.destroy()
            else:
                nome1.delete(0,END)
                messagebox.showwarning("Ops!","Sono consentiti solo caratteri alfanumerici e _") 
    #iscrizione finestra
    def iscrizione_finestra(self):
        self.isc = Tk()
        self.isc.geometry("300x400")
        self.isc.resizable(False,False)
        self.isc.title("BitSender")
        self.isc.config(bg = "#38475A")
        icona(self.isc)
        nome = Label(self.isc, text = "Inserisci nome", font = ("ebrima",14,), bg = "#38475A", fg = "white")
        nome.place(relx = 0.5,anchor=CENTER, y = 30)
        self.nome1 = Entry(self.isc, borderwidth = 0, width = 23, font = ("arial",14),bg = "#C6CDB8")
        self.nome1.place(relx = 0.5, anchor = CENTER, y = 60)
        passw = Label(self.isc, text = "Inserisci password", font = ("ebrima",14,), bg = "#38475A", fg = "white" )
        passw.place(relx = 0.5,anchor=CENTER, y = 110)
        self.passw1 =  Entry(self.isc, borderwidth = 0, width = 23, font = ("arial",14),bg = "#C6CDB8",show = "*")
        self.passw1.place(relx = 0.5, anchor = CENTER, y = 140)
        passw2 = Label(self.isc, text = "Riscrivi password", font = ("ebrima",14,), bg = "#38475A", fg = "white" )
        passw2.place(relx = 0.5,anchor=CENTER, y = 190)
        self.passw3 =  Entry(self.isc, borderwidth = 0, width = 23, font = ("arial",14),bg = "#C6CDB8",show = "*")
        self.passw3.place(relx = 0.5, anchor = CENTER, y = 220)
        butto = Button(self.isc,text = "Iscriviti",font = ("ebrima",14,), bg = "#334966", fg = "white", borderwidth = 1, relief = SOLID,width = 23,command = lambda : self.iscrizione(so,self.nome1,self.passw1,self.passw3,self.isc))
        butto.place(relx = 0.5, anchor = CENTER, y = 280)
        self.isc.bind("<Return>", self.ev_iscrizione)

    def ev_iscrizione(self, event):
        self.iscrizione(so, self.nome1, self.passw1, self.passw3, self.isc)
    def accesso_finestra(self,fin):
        try:
            fin.destroy()
        except:
            None
        self.win = Tk()
        self.win.geometry("300x400")
        self.win.resizable(False,False)
        self.win.title("BitSender")
        icona(self.win)
        self.win.config(bg = "#38475A")
        #ico(win)
        #Login
        log = Label(self.win, text = "Inserisci nome", font = ("ebrima",14,), bg = "#38475A", fg = "white")
        log.place(relx = 0.5,anchor=CENTER, y = 30)
        self.log1 = Entry(self.win, borderwidth = 0, width = 23, font = ("arial",14),bg = "#C6CDB8")
        self.log1.place(relx = 0.5, anchor = CENTER, y = 60)
        log2 = Label(self.win, text = "Inserisci password", font = ("ebrima",14,), bg = "#38475A", fg = "white" )
        log2.place(relx = 0.5,anchor=CENTER, y = 110)
        self.log3 =  Entry(self.win, borderwidth = 0, width = 23, font = ("arial",14),bg = "#C6CDB8",show = "*")
        self.log3.place(relx = 0.5, anchor = CENTER, y = 140)
        self.bu = Button(self.win, text = "Accedi",font = ("ebrima",14,), bg = "#334966", fg = "white", borderwidth = 1, relief = SOLID,width = 23,command = lambda : self.accesso(so,self.log1,self.log3,self.win))
        self.bu.place(relx = 0.5, anchor = CENTER, y = 190)
        #oppure
        opp = Label(self.win, text = "-- oppure --",font = ("ebrima",14,), bg = "#38475A", fg = "white")
        opp.place(relx = 0.5, anchor = CENTER, y = 240)
        #iscrizione bottone
        bot =  Button(self.win,text = "Iscriviti",font = ("ebrima",14,), bg = "#334966", fg = "white", borderwidth = 1, relief = SOLID,width = 23, command = lambda: self.iscrizione_finestra())
        bot.place(relx = 0.5, anchor = CENTER, y = 290)
        self.win.bind("<Return>", self.ev_accesso)
    
    def ev_accesso(self,event):
        self.accesso(so,self.log1,self.log3,self.win)

class accesso_fatto():
    def __init__(self,nome,ind):
        self.fin = Tk()
        icona(self.fin)
        self.fin.geometry("970x490")
        self.fin.resizable(False,False)
        self.nome = nome
        self.ind = ind
        self.fin.title("BitSender" + " - " + self.nome)
        self.fin.config(bg = "#38475A")
        #blocc var
        self.blocc = IntVar()
        self.blocc.set(0)
        menu = Menu(self.fin)
        altromenu = Menu(menu, tearoff=0)
        menu.add_command(label = "Esci", command = lambda : self.chiusura())
        menu.add_cascade(label = "Nuovo gruppo", command = self.gruppo)
        menu.add_cascade(label = "Info gruppo",command = self.info_gruppo)
        menu.add_cascade(label = "I tuoi Download",command = self.Download)
        menu.add_cascade(label = "Download utente",command = self.Download_Utente)
        menu.add_cascade(label="Altro", menu=altromenu)
        altromenu.add_checkbutton(label = "Blocca utente",variable = self.blocc, command = self.blocca_ute)
        altromenu.add_separator()
        altromenu.add_command(label = "Svuota chat", command = self.svuota_chat)
        altromenu.add_separator()
        altromenu.add_command(label = "Elimina contatto", command = self.send_rem_rub)
        altromenu.add_command(label = "Abbandona chat", command = self.send_rem_rub_gru)
        self.fin.config(menu=menu)        
        #comunicazione
        self.comunicazione()
        #intvar
        self.a = StringVar(self.fin)
        self.a.set("§")
        #bool var sta_scrive
        self.scrive = BooleanVar(self.fin)
        self.scrive.set(True)
        #string var download
        self.do = StringVar(self.fin)
        self.do.set("§")
        self.do_u = StringVar(self.fin)
        self.do_u.set("§")
        #menu
        self.menu()
        #thread e lettura
        thread = self.Comunicazione()
        thread.start()  
        self.lettura()
        self.fin.protocol("WM_DELETE_WINDOW", self.chiusura)
        
    def file_management(self,dire,moda,lista,fieldname):
        if moda == "a":
            with open(dire,moda) as file:
                wr = csv.writer(file)
                wr.writerow(lista)
        if moda == "w":
            with open(dire,moda) as file:
                wr = csv.DictWriter(file, fieldnames = fieldname)
                wr.writeheader()
        if moda == "r":
            with open(dire,moda) as file:
                rd = csv.DictReader(file)
                for row in rd:
                    lista.append(row[fieldname])

    class Comunicazione(Thread):
        def __init__(self):
            Thread.__init__(self) 
        def run(self):
            while True:      
                data = so.recv(4096)
                mess = data.decode()
                while mess != "":
                    mes = mess.find("<--[°+°]-->",1)
                    bb = mess[0:mes]
                    mess = mess.replace(mess[0:mes] + "<--[°+°]-->","",1)
                    num.append(bb)
    
    def lettura(self):
        try:
            msg = num.pop(0)
            print("Messaggio ricevuto: " + msg)
            if msg == "#####££":
                self.text1.config(state = NORMAL)
                self.text1.tag_config("new_mess",foreground = "#3754CB", justify = "center", background = "#add77f")
                self.text1.insert(END, "nuovi messaggi" + "\n","new_mess")
                self.text1.config(state = DISABLED)
            elif msg[0:6] == "$%&°ok":
                search = msg[6:]
                accesso_fatto.file_management(self,self.nome + "/rubrica.csv","a",[search],None)
                accesso_fatto.file_management(self,self.nome + "/" + search + ".csv","w",None,["nome","mess"])
                accesso_fatto.file_management(self,self.nome + "/@download" + search + ".csv","w",None,["nome"])
                self.riemp_menu()
            elif msg == "!*°False!$":
                messagebox.showwarning("Ops!","Account non esistente!")
            elif msg == "###False!$":
                messagebox.showwarning("Ops!","L'utente ti ha bloccato!")
            elif msg[0:14] == "%&nuovo!_ute#@":
                    mitt = msg[14:]
                    self.file_management(self.nome + "/rubrica.csv","a",[mitt],None)
                    self.file_management(self.nome + "/" + mitt + ".csv","w",None,["nome","mess"])
                    self.file_management(self.nome + "/" + "@download" + mitt + ".csv","w",None,["nome","mess"])
                    self.riemp_menu()
            elif msg [0:8] == "###lista":
                msg = msg.replace("###lista","")
                self.lista1.insert(END,msg)
            elif msg[0:5] == "#°òò!":
                msg = msg.replace("#°òò!","")
                numo = msg.find("@",1)
                nome = msg[0:numo]
                mess = msg.replace(nome + "@","")
                self.stampa_messaggi(nome,mess)
                self.file_management(self.nome + "/" + self.a.get() + ".csv","a",[nome,mess],None)
            elif msg[0:15] == "?ç°sta_scrive($":
                msg = msg.replace("?ç°sta_scrive($","")
                self.sta_scrive(msg)
            elif msg[0:11] == "!!okok!!#@ò":
                self.disp.place(y = 86, relx = 0.5, anchor = CENTER)
                self.contr.set(True)
            elif msg[0:11] == "!!nono!!#@ò":
                self.no_disp.place(y = 86, relx = 0.5, anchor = CENTER)
                self.contr.set(False)
            elif msg[0:16] == "###rem_rub_gru$£":
                nome = msg.replace("###rem_rub_gru$£","")
                self.canc_rubrica(nome,"rubrica.csv")
                os.remove(self.nome + "/" + "@download" + nome + ".csv")
                self.text1_clear()
                self.info_gru.destroy()
                self.a.set("§")
            elif msg[0:16] == "##refreshlista##":
                self.lista1.delete(0,END)
                so.sendall(bytes("#@#çrichiesta_part" + self.a.get() + "<--[°+°]-->","UTF-8"))
            elif msg[0:9] == "#$£noti##":
                nome = msg.replace("#$£noti##","")
                self.notifica(nome)
            elif msg[0:8] == "##do2££#":
                nome = msg.replace("##do2££#","")
                self.riemp_do2(nome)
            elif msg[0:13] == "##ok_transfer":
                nome = msg.replace("##ok_transfer","")
                self.file_management(self.nome + "/@download" + self.a.get() + ".csv","a",[nome],None)
                self.riemp_do1()
                self.do.set("§")
            elif msg[0:14] == "##!!impossfile":
                messagebox.showwarning("Ops!","Impossibile scaricare il file!")      
        except:
            None  
            
        self.fin.after(10,self.lettura)

    def comunicazione(self):
        #scrollbar
        scrollbar = Scrollbar(self.fin)
        scrollbar.pack(side = LEFT,fill = Y)
        #text1
        self.text1 = Text(self.fin,highlightthickness = 0,yscrollcommand=scrollbar.set,width = 59, bg = "#0D2441",borderwidth = 1,relief = SOLID,font=("ebrima",14),fg = "#EC6C13")
        self.text1.pack(fill = Y,side = LEFT, pady = 60)
        self.text1.config(state = DISABLED)
        #entry1
        entry1 = Entry(self.fin,borderwidth = 1,width = 54,bg = "#334966", font=("Helvetica Neue",16),fg = "white",relief = SOLID)
        entry1.place(x = 17, y = 410)
        #464
        #entry2
        entry2 = Entry(self.fin,borderwidth = 1,width = 54,bg = "#334966", font=("Helvetica Neue",16),fg = "white",relief = SOLID)
        entry2.place(x = 17, y = 35)
        #scrollbar
        scrollbar.config(command=self.text1.yview)
        
    
        def send_search(event):
            lista = []
            search = entry2.get()
            entry2.delete(0,END)
            accesso_fatto.file_management(self,self.nome + "/rubrica.csv","r",lista,"nome")
            if search not in lista and search != self.nome:
                if search != "":
                    search = "££##°@£#" + search
                    so.sendall(bytes(search + "<--[°+°]-->",'UTF-8'))

        def send_mes(event):
            mess = entry1.get()
            entry1.delete(0,END)
            if mess != "" and self.a.get() != "§" and self.blocc.get() == 0:
                accesso_fatto.file_management(self,self.nome + "/" + self.a.get() + ".csv","a",["Tu",mess],None)
                self.stampa_messaggi("Tu",mess)
                if self.a.get()[0] != "#":
                    mess = "£$£##°#" + self.nome + "§" + mess
                else:
                    mess = "#$#££°£" + self.nome + "§" + mess

                so.sendall(bytes(mess + "<--[°+°]-->","UTF-8"))

        def sta_scrive_send(event):
            contr = False
            var = self.scrive.get()
            if var == True and self.a.get() != "§" and self.blocc.get() == 0:
                so.sendall(bytes("££$$sta_scrive##" + "<--[°+°]-->",'UTF-8'))
                self.scrive.set(False)
                contr = True
            if contr == True:
                self.fin.after(1000,self.sta_scrive_reset)
                    
        #event
        entry2.bind('<Return>',send_search)
        entry1.bind('<Return>', send_mes)
        entry1.bind('<Key>',sta_scrive_send) 

    def lettura_stampa_messaggi(self):
        self.text1.config(state = NORMAL)
        self.text1.delete("1.0",END)
        with open(self.nome + "/" + self.a.get() + ".csv","r") as file:
            rd = csv.DictReader(file)
            for row in rd:
                self.stampa_messaggi(row["nome"],row["mess"])         
        self.text1.config(state = DISABLED)

    def stampa_messaggi(self,nome,mess):
        self.text1.config(state = NORMAL)
        self.text1.tag_config('utente',  foreground="white")
        self.text1.tag_config("des", foreground = "#add77f")
        if nome == "Tu":
            self.text1.insert(END, "Tu> " + mess + "\n","utente")
        else:
            self.text1.insert(END, nome + "> " + mess + "\n","des")
        self.text1.see(END)
        self.text1.config(state = DISABLED)

    def menu(self):
        #scrollbar2
        scrollbar2 = Scrollbar(self.fin)
        scrollbar2.pack(side = RIGHT,fill = Y)
        #text2
        self.text2 = Text(self.fin,yscrollcommand=scrollbar2.set,highlightthickness = 0,width = 35, bg = "#38475A",borderwidth = 1,relief = SOLID,font=("ebrima",14),fg = "#EC6C13")
        self.text2.pack(side = RIGHT, fill = Y)
        self.text2.config(state = DISABLED)
        #scrollbar2
        scrollbar2.config(command= self.text2.yview)
        self.riemp_menu()
        
    def riemp_menu(self):
        self.text2.config(state = NORMAL)
        self.text2.delete("1.0",END)
        lista = []
        lista1 = []
        lista2 = []
        self.file_management(self.nome + "/rubrica.csv","r",lista,"nome")
        self.file_management(self.nome + "/notifica.csv","r",lista1,"nome")
        self.file_management(self.nome + "/notifica.csv","r",lista2,"sound")
        for x in lista:
            text = x
            if x in lista1:
                text = text + " (!)"
                if lista2[lista1.index(x)] == "1":
                    sou_noti = self.sound_notifica()
                    sou_noti.start()
            radiob = Radiobutton(self.fin,text = text,height = 2,borderwidth = 0,activebackground="#576A81",font = ("Ebrima",10),bg = "#576A81",relief = SOLID,width = 47, variable = self.a,value = x,indicatoron=0,command = self.menu_send_ute,highlightthickness = 0)
            self.text2.window_create(END, window = radiob, align = BASELINE, padx = 2)
            self.text2.insert(END,"\n")
        self.text2.config(state = DISABLED)
        self.sound_notifica_file("0",None)

    def menu_send_ute(self):
        lista = []
        so.sendall(bytes("##$$°@££" + self.a.get() + "<--[°+°]-->","UTF-8"))
        self.lettura_stampa_messaggi()
        self.sound_notifica_file("0", self.a.get())
        self.riemp_menu()
        lista = []
        self.file_management(self.nome + "/blocc.csv","r",lista,"nome")
        if self.a.get() in lista:
            self.blocc.set(1)
        else:
            self.blocc.set(0)
        
    def sta_scrive_reset(self):
        self.scrive.set(True)

    def sta_scrive(self,nome):
        tes = "*" + nome + " sta scrivendo*"
        self.testo = Label(text =  tes, fg = "#93FA59", bg = "#38475A", font = ("Ebrima",12))
        self.testo.place(x = 297, y = 17, anchor = CENTER)
        self.fin.after(2000, self.testo.destroy) 

    def gruppo(self):
        lista = []   
        self.gru = Tk()
        icona(self.gru)
        self.contr = BooleanVar(self.gru)
        self.contr.set(True)
        self.gru.geometry("300x400")
        self.gru.resizable(False,False)
        self.gru.title("BitSender")
        self.gru.config(bg = "#38475A")
        log = Label(self.gru, text = "Inserisci nome del gruppo", font = ("ebrima",14,), bg = "#38475A", fg = "white")
        log.place(relx = 0.5,anchor=CENTER, y = 30)
        log1 = Entry(self.gru, borderwidth = 0, width = 23, font = ("arial",14),bg = "#C6CDB8")
        log1.place(relx = 0.5, anchor = CENTER, y = 60)
        bu1 = Button(self.gru, text = "Elimina",font = ("ebrima",14,), bg = "#334966", fg = "#7F0606", borderwidth = 1, relief = SOLID,width = 25,command = lambda:self.lista_part.delete(ANCHOR))
        bu1.place(relx = 0.5, anchor = CENTER, y = 300)
        self.lista_part = Listbox(self.gru,selectbackground = "#576A81",highlightthickness = 0,bg = "#0D2441",borderwidth = 1,relief = SOLID,font=("ebrima",14),fg = "white", width = 30, height = 6)
        self.lista_part.pack(side = TOP, pady = 100)
        self.disp = Label(self.gru, text = "Nome disponibile!",font = ("ebrima",12,), bg = "#38475A", fg = "white")
        self.no_disp = Label(self.gru, text = "Nome non disponibile!",font = ("ebrima",12,), bg = "#38475A",fg = "white")

        def nome_gruppo(event):
            if log1.get() != "":
                so.sendall(bytes("#@#gru" + "#" + log1.get() + "<--[°+°]-->","UTF-8"))                   
                self.disp.destroy()
                self.no_disp.destroy()
                self.disp = Label(self.gru, text = "Nome disponibile!",font = ("ebrima",12,), bg = "#38475A", fg = "white")
                self.no_disp = Label(self.gru, text = "Nome non disponibile!",font = ("ebrima",12,), bg = "#38475A", fg = "white")
            else:
                self.disp.destroy()
                self.no_disp.destroy()
            
            
        def riemp_lista(lista):
            self.file_management(self.nome + "/rubrica.csv","r",lista,"nome")
            for x in lista:
                if x[0] != "#":
                    self.lista_part.insert(END, x)

        def send_nome_gruppo(nome):
            if self.contr.get() == True and nome != "":
                mess = "£££°°###" + nome + "<--[°+°]-->"
                a = self.lista_part.get(0,END)
                for x in a:
                    mess = mess + "£££°°###" + x + "<--[°+°]-->"
                so.sendall(bytes(mess,"UTF-8"))
                self.gru.destroy()
                self.file_management(self.nome + "/rubrica.csv","a",["#" + nome],None)
                self.file_management(self.nome + "/#" + nome + ".csv","w",None,["nome","mess"])
                self.file_management(self.nome + "/" + "@download#" + nome + ".csv","w",None,["nome","mess"])
                self.riemp_menu()
    
        bu = Button(self.gru, text = "OK!",font = ("ebrima",14,), bg = "#334966", fg = "white", borderwidth = 1, relief = SOLID,width = 23,command = lambda: send_nome_gruppo(log1.get()))
        bu.place(relx = 0.5, anchor = CENTER, y = 360)
        
        riemp_lista(lista)
        self.gru.bind("<Key>",nome_gruppo)

    def info_gruppo(self):
        if self.a.get()[0] == "#" and self.a.get() != "§":
            self.lista_rubri = []   
            self.info_gru = Tk()
            icona(self.info_gru)
            self.info_gru.geometry("320x460")
            self.info_gru.resizable(False,False)
            self.info_gru.title("BitSender")
            self.info_gru.config(bg = "#38475A")
            self.lista1 = Listbox(self.info_gru,selectbackground = "#576A81",highlightthickness = 0,bg = "#0D2441",borderwidth = 1,relief = SOLID,font=("ebrima",14),fg = "white", width = 30, height = 6)
            self.lista1.pack(side = TOP)
            bu1 = Button(self.info_gru, text = "Elimina",font = ("ebrima",12,), bg = "#334966", fg = "#7F0606", borderwidth = 1, relief = SOLID,width = 25,command = self.send_rem_partec )
            bu1.place(relx = 0.5, anchor = CENTER, y = 190)
            bu2 = Button(self.info_gru, text = "Amministratore",font = ("ebrima",12,), bg = "#334966", fg = "white", borderwidth = 1, relief = SOLID,width = 25,command = self.send_amm_partec)
            bu2.place(relx = 0.5, anchor = CENTER, y = 230)
            bu3 = Button(self.info_gru, text = "Aggiungi",font = ("ebrima",12,), bg = "#334966", fg = "white", borderwidth = 1, relief = SOLID,width = 25, command = self.send_agg_partec)
            bu3.place(relx = 0.5, anchor = CENTER, y = 270)
            self.lista2 = Listbox(self.info_gru,selectbackground = "#576A81",highlightthickness = 0,bg = "#0D2441",borderwidth = 1,relief = SOLID,font=("ebrima",14),fg = "white", width = 40, height = 6)
            self.lista2.pack(side = BOTTOM)
            self.file_management(self.nome + "/rubrica.csv","r",self.lista_rubri,"nome")
            so.sendall(bytes("#@#çrichiesta_part" + self.a.get() + "<--[°+°]-->","UTF-8"))
            for x in self.lista_rubri:
                if x[0] != "#":
                    self.lista2.insert(END, x)
    def text1_clear(self):
        self.text1.config(state = NORMAL)
        self.text1.delete("1.0",END)
        self.text1.config(state = DISABLED)

    def send_rem_partec(self):
        if self.lista1.get(ANCHOR) != "":     
            if self.lista1.get(ANCHOR).replace(" (amministratore)","") != "(Tu)":
                so.sendall(bytes("£££rem_partec" + self.lista1.get(ANCHOR).replace(" (amministratore)","") + "<--[°+°]-->","UTF-8"))                          
    def send_agg_partec(self):
        if self.lista2.get(ANCHOR) != "":      
            so.sendall(bytes("£££agg_partec" + self.lista2.get(ANCHOR) + "<--[°+°]-->","UTF-8"))       
    def send_amm_partec(self):
        if self.lista1.get(ANCHOR) != "":  
            so.sendall(bytes("£££amm_partec" + self.lista1.get(ANCHOR).replace(" (amministratore)","") + "<--[°+°]-->","UTF-8"))       
    def send_rem_rub(self):
        if self.a.get()[0] != "#" and self.a.get() != "§":
            so.sendall(bytes("###rem_rub" + self.a.get() + "<--[°+°]-->","UTF-8"))
            os.remove(self.nome + "/" + "@download" + self.a.get() + ".csv")
            self.canc_rubrica(self.a.get(),"rubrica.csv")
            self.a.set("§")
            self.text1_clear()
    def send_rem_rub_gru(self):
        if self.a.get()[0] == "#":
            so.sendall(bytes("#£#rem_rub_gru" + self.nome + "<--[°+°]-->","UTF-8"))
    def canc_rubrica(self,nome,dire):
        try:
            os.remove(self.nome + "/" + nome + ".csv")
        except:
            None
        lista = []
        self.file_management(self.nome + "/" + dire,"r",lista,"nome")
        lista.remove(nome)
        self.file_management(self.nome + "/" + dire,"w",None,["nome"])
        for nn in lista:
            self.file_management(self.nome + "/" + dire,"a",[nn],None)
        self.riemp_menu()
    def svuota_chat(self):
        self.text1_clear()
        self.file_management(self.nome + "/" + self.a.get() + ".csv","w",None,["nome","mess"])
    def notifica(self,nome):
        lista = []
        self.file_management(self.nome + "/notifica.csv","r",lista,"nome")
        if nome not in lista:
            self.file_management(self.nome + "/notifica.csv","a",[nome,"1"],None)
            self.riemp_menu()
    def sound_notifica_file(self, num, nome):
        lista = []
        self.file_management(self.nome + "/notifica.csv","r",lista,"nome")
        self.file_management(self.nome + "/notifica.csv","w",None,["nome","sound"])
        for x in lista:
            if x != nome:
                self.file_management(self.nome + "/notifica.csv","a",[x,num],None)

    class sound_notifica(Thread):
        def __init__(self):
            Thread.__init__(self)
        def run(self):
            playsound("sound.mp3")
    def blocca_ute(self):
        if self.a.get()[0] != "#" and self.a.get() != "§":
            if self.blocc.get() == 1:
                self.file_management(self.nome + "/blocc.csv","a",[self.a.get()],None)
                so.sendall(bytes("##blocca_ute££1" + "<--[°+°]-->","UTF-8"))
            else:
                lista = []
                self.file_management(self.nome + "/blocc.csv","r",lista,"nome")
                self.file_management(self.nome + "/blocc.csv","w",None,["nome"])
                so.sendall(bytes("##blocca_ute££0" + "<--[°+°]-->","UTF-8"))
                for x in lista:
                    if x != self.a.get():
                        self.file_management(self.nome + "/blocc.csv","a",[x],None)
    
    ##########################################
    
    class ftp_Server_Transfer(Thread):
        def __init__(self,dire,nome_ser,nome,ind):
            self.ind = ind
            self.dire = dire
            self.nome_ser = nome_ser
            self.nome = nome
            Thread.__init__(self)
        def run(self):
            with socket(AF_INET, SOCK_STREAM) as conn:
                ind = gethostbyname(self.ind)
                conn.connect((ind, 8888))
                conn.sendall(bytes(self.nome_ser,"UTF-8"))
                sleep(2)
                with open(self.dire,"rb") as file:
                    while True:
                        ff = file.read(4096)
                        conn.send(ff)
                        if not ff:
                            break   
                num.append("##ok_transfer" + self.nome)
                                 
    class ftp_Server_Receiver(Thread):
        def __init__(self,dire,dire_ser,ind):
            self.ind = ind
            self.dire = dire
            self.dire_ser = dire_ser
            Thread.__init__(self)
        def run(self):
            with socket(AF_INET, SOCK_STREAM) as conn:
                ind = gethostbyname(self.ind)
                conn.connect((ind, 1234))
                conn.sendall(bytes(self.dire_ser,"UTF-8"))
                with open(self.dire,"wb") as file:
                    while True:
                        data = conn.recv(4096)
                        if not data:
                            break
                        elif data == b"##!!impossfile":
                            num.append(data.decode())
                        else:
                            file.write(data)
                        
    def Download(self):
        if self.a.get() != "§":
            self.download = Toplevel()
            icona(self.download)
            self.download.geometry("332x460")
            self.download.resizable(False,False)
            self.download.title("BitSender")
            self.download.config(bg = "#38475A")
            scrollbar = Scrollbar(self.download)
            scrollbar.pack(side = RIGHT,fill = Y,ipady = 50) 
            self.do1 = Text(self.download,yscrollcommand=scrollbar.set,highlightthickness = 0,height = 11,width = 31,bg = "#0D2441",borderwidth = 1,relief = SOLID,font=("ebrima",14),fg = "#EC6C13")
            self.do1.place(x = 0)
            self.do1.config(state = DISABLED)
            bu = Button(self.download, text = "Carica file",font = ("ebrima",14,), bg = "#334966", fg = "white", borderwidth = 1, relief = SOLID,width = 25, command = self.carica_file)
            bu.place(anchor = CENTER, y = 330, x = 157)
            bu1 = Button(self.download, text = "Elimina file",font = ("ebrima",12,), bg = "#334966", fg = "white", borderwidth = 1, relief = SOLID,width = 25, command = self.elimina_file)
            bu1.place(anchor = CENTER, y = 380,x = 157)
            scrollbar.config(command=self.do1.yview)
            self.riemp_do1()
    
    def riemp_do1(self):
        self.do1.config(state = NORMAL)
        self.do1.delete("1.0",END)
        lista = []
        self.file_management(self.nome + "/@download" + self.a.get() + ".csv","r",lista,"nome")
        for nome in lista:
            radiob = Radiobutton(self.download,text = nome,height = 2,borderwidth = 0,activebackground="#576A81",font = ("Ebrima",10),bg = "#576A81",relief = SOLID,width = 43, variable = self.do,value = nome,indicatoron=0,highlightthickness = 0)
            self.do1.window_create(END, window = radiob, align = BASELINE, padx = 3)
            self.do1.insert(END,"\n")
        self.do1.config(state = DISABLED)

    def carica_file(self):
        dire = filedialog.askopenfilename(filetypes = (("png","*.png"),("All files","*.*")))
        nome = os.path.split(dire)[1]
        if self.a.get()[0] != "#":
            dire_ser = self.nome + "/" + self.a.get() + "/" + nome
        else:
            dire_ser = self.a.get() + "/" + nome
        tr = self.ftp_Server_Transfer(dire,dire_ser,nome,self.ind)  
        tr.start()

    def elimina_file(self):
        if self.do.get() != "§":
            self.canc_rubrica(self.do.get(),"@download" + self.a.get() + ".csv")
            self.riemp_do1()
            so.sendall(bytes("##rem_file##" + self.do.get() + "<--[°+°]-->","UTF-8"))
            self.do.set("§")

    def Download_Utente(self):
        if self.a.get() != "§":
            self.download_u = Toplevel()
            icona(self.download_u)
            self.download_u.geometry("332x460")
            self.download_u.resizable(False,False)
            self.download_u.title("BitSender")
            self.download_u.config(bg = "#38475A")
            scrollbar = Scrollbar(self.download_u)
            scrollbar.pack(side = RIGHT,fill = Y,ipady = 50) 
            self.do2 = Text(self.download_u,yscrollcommand=scrollbar.set,highlightthickness = 0,height = 13,width = 31,bg = "#0D2441",borderwidth = 1,relief = SOLID,font=("ebrima",14),fg = "#EC6C13")
            self.do2.place(x = 0)
            self.do2.config(state = DISABLED)
            bu = Button(self.download_u, text = "Scarica file",font = ("ebrima",14,), bg = "#334966", fg = "white", borderwidth = 1, relief = SOLID,width = 25, command = self.scarica_file)
            bu.place(anchor = CENTER, y = 380, x = 157)
            scrollbar.config(command=self.do2.yview)
            so.sendall(bytes("##dolista$$" + "<--[°+°]-->","UTF-8"))

    def riemp_do2(self,nome):
        self.do2.config(state = NORMAL)
        radiob = Radiobutton(self.download_u,text = nome,height = 2,borderwidth = 0,activebackground="#576A81",font = ("Ebrima",10),bg = "#576A81",relief = SOLID,width = 43, variable = self.do_u,value = nome,indicatoron=0,highlightthickness = 0)
        self.do2.window_create(END, window = radiob, align = BASELINE, padx = 3)
        self.do2.insert(END,"\n")
        self.do2.config(state = DISABLED)

    def scarica_file(self):
        if self.do_u.get() != "§":
            dire = self.do_u.get()
            if self.a.get()[0] != "#":
                dire_ser = self.a.get() + "/" + self.nome + "/" + self.do_u.get()
            else:
                dire_ser = self.a.get() + "/" + self.do_u.get()
            self.do_u.set("§")
            rec = self.ftp_Server_Receiver(dire,dire_ser,self.ind)
            rec.start()

    def chiusura(self):
        self.sound_notifica_file("1", None)
        self.fin.destroy()
        so.close()
    ##########################################

mainloop()