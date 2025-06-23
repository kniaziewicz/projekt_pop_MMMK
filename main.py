from tkinter import *

import tkintermapview



users:list=[]
workers:list=[]
fires:list=[]
wremiza:list=[]

#Placówki
class User:
    def __init__(self,name,location):
        self.name = name
        self.location = location
        self.coordinates = self.get_coordinates()
        self.marker = map_widget.set_marker(self.coordinates[0],self.coordinates[1], marker_color_circle='blue')

    def get_coordinates(self) -> list:
        import requests
        from bs4 import BeautifulSoup
        url = f"https://pl.wikipedia.org/wiki/{self.location}"
        response = requests.get(url).text
        response_html = BeautifulSoup(response, "html.parser")
        longitude = float(response_html.select(".longitude")[1].text.replace(",", "."))
        latitude = float(response_html.select(".latitude")[1].text.replace(",", "."))
        print(longitude)
        print(latitude)
        return [latitude, longitude]

#strażacy
class Worker:
    def __init__(self,name,location,remiza):
        self.name = name
        self.location = location
        self.remiza = remiza
        self.coordinates = self.get_coordinates()
        self.marker = map_widget.set_marker(self.coordinates[0],self.coordinates[1], marker_color_outside='black')

    def get_coordinates(self) -> list:
        import requests
        from bs4 import BeautifulSoup
        url = f"https://pl.wikipedia.org/wiki/{self.location}"
        response = requests.get(url).text
        response_html = BeautifulSoup(response, "html.parser")
        longitude = float(response_html.select(".longitude")[1].text.replace(",", "."))
        latitude = float(response_html.select(".latitude")[1].text.replace(",", "."))
        print(longitude)
        print(latitude)
        return [latitude, longitude]

#pożary
class Fire:
    def __init__(self,name,location):
        self.name = name
        self.location = location
        self.coordinates = self.get_coordinates()
        self.marker = map_widget.set_marker(self.coordinates[0],self.coordinates[1])

    def get_coordinates(self) -> list:
        import requests
        from bs4 import BeautifulSoup
        url = f"https://pl.wikipedia.org/wiki/{self.location}"
        response = requests.get(url).text
        response_html = BeautifulSoup(response, "html.parser")
        longitude = float(response_html.select(".longitude")[1].text.replace(",", "."))
        latitude = float(response_html.select(".latitude")[1].text.replace(",", "."))
        print(longitude)
        print(latitude)
        return [latitude, longitude]

#strazacy_w_danej_remizie
class Wremizach:
    def __init__(self,name,location):
        self.name = name
        self.location = location
        self.coordinates = self.get_coordinates()
        self.marker = map_widget.set_marker(self.coordinates[0],self.coordinates[1], marker_color_outside='black')

    def get_coordinates(self) -> list:
        import requests
        from bs4 import BeautifulSoup
        url = f"https://pl.wikipedia.org/wiki/{self.location}"
        response = requests.get(url).text
        response_html = BeautifulSoup(response, "html.parser")
        longitude = float(response_html.select(".longitude")[1].text.replace(",", "."))
        latitude = float(response_html.select(".latitude")[1].text.replace(",", "."))
        print(longitude)
        print(latitude)
        return [latitude, longitude]

#wremiza_commands
def make_wremiza():

    for idx, val in enumerate(wremiza):
        wremiza[idx].marker.delete()

    wremiza.clear()
    n=listbox_lista_remizy.index(ACTIVE)
    i=users[n].name

    for idx,strazak in enumerate(workers):
        if workers[idx].remiza==i:
            strazak = Wremizach(name=workers[idx].name,location=workers[idx].location)
            wremiza.append(strazak)
        workers[idx].marker.delete()

    show_wremiza()
    button_pokaz_szczegoly_worker.configure(command=show_wremiza_details)
    button_usun_worker.configure(command=remove_wremiza)


def show_wremiza():
    listbox_lista_worker.delete(0,END)
    for idx,strazak in enumerate(wremiza):
        listbox_lista_worker.insert(idx,f'{idx+1}. {strazak.name}')

def remove_wremiza ():
    i=listbox_lista_worker.index(ACTIVE)
    wremiza[i].marker.delete()


    for idx, val in enumerate(workers):
        if workers[idx].name==wremiza[i].name:
            workers.pop(idx)

    wremiza.pop(i)
    show_wremiza()

def restore():
    show_workers()
    for idx, val in enumerate(wremiza):
        wremiza[idx].marker.delete()

    for idx, val in enumerate(workers):
        workers[idx].coordinates = workers[idx].get_coordinates()
        workers[idx].marker = map_widget.set_marker(workers[idx].coordinates[0], workers[idx].coordinates[1], marker_color_outside='black')

    button_pokaz_szczegoly_worker.configure(command=show_worker_details)
    button_usun_worker.configure(command=remove_worker)

def show_wremiza_details():
    i=listbox_lista_worker.index(ACTIVE)
    name=wremiza[i].name
    location=wremiza[i].location

    label_szczegoly_wartosc_name.config(text=name)
    label_szczegoly_wartosc_location.config(text=location)
    label_szczegoly_wartosc_remiza.config(text='...')

    map_widget.set_position(wremiza[i].coordinates[0],wremiza[i].coordinates[1])
    map_widget.set_zoom(17)

#end

def add_who ():
    root = Tk()
    root.geometry("500x200")
    root.title("Kogo dodać?")
    ramka_answer=Frame(root)
    ramka_answer.grid(column=0, row=0)
    button_remiza=Button(ramka_answer,text="Remiza",command=add_user)
    button_remiza.grid(column=0, row=0)
    button_worker=Button(ramka_answer,text="Strażak",command=add_worker)
    button_worker.grid(column=0, row=1)
    button_fire=Button(ramka_answer,text="Pożar",command=add_fire)
    button_fire.grid(column=0, row=2)

#user_commands

def add_user ():
    zmienna_nazwa=entry_name.get()
    zmienna_coordinates=entry_location.get()
    user = User(name=zmienna_nazwa, location=zmienna_coordinates)
    users.append(user)

    entry_name.delete(0,END)
    entry_location.delete(0,END)
    entry_remiza.delete(0,END)

    entry_name.focus()

    show_users()

    print(users)


def show_users():
    listbox_lista_remizy.delete(0,END)
    for idx,user in enumerate(users):
        listbox_lista_remizy.insert(idx,f'{idx+1}. {user.name}')


def remove_user ():
    i=listbox_lista_remizy.index(ACTIVE)
    users[i].marker.delete()
    users.pop(i)
    show_users()

def edit_user ():
    i=listbox_lista_remizy.index(ACTIVE)
    name=users[i].name
    location=users[i].location

    entry_name.insert(0,name)
    entry_location.insert(0,location)

    button_dodaj_obiekt.config(text='zapisz', command=lambda: update_user(i))


def update_user (i):
    new_name=entry_name.get()
    new_location=entry_location.get()

    users[i].name=new_name
    users[i].location=new_location

    users[i].marker.delete()
    users[i].coordinates=users[i].get_coordinates()
    users[i].marker=map_widget.set_marker(users[i].coordinates[0],users[i].coordinates[1])

    entry_name.delete(0,END)
    entry_location.delete(0,END)
    entry_remiza.delete(0,END)

    button_dodaj_obiekt.config(text='Dodaj obiekt', command=add_who)
    show_users()

def show_user_details():
    i=listbox_lista_remizy.index(ACTIVE)
    name=users[i].name
    location=users[i].location

    make_wremiza()

    label_szczegoly_wartosc_name.config(text=name)
    label_szczegoly_wartosc_location.config(text=location)
    label_szczegoly_wartosc_remiza.config(text='...')

    map_widget.set_position(users[i].coordinates[0],users[i].coordinates[1])
    map_widget.set_zoom(10)
#end

#workers_command

def add_worker ():
    zmienna_nazwa=entry_name.get()
    zmienna_coordinates=entry_location.get()
    zmienna_remiza=entry_remiza.get()
    worker = Worker(name=zmienna_nazwa, location=zmienna_coordinates, remiza=zmienna_remiza)
    workers.append(worker)

    entry_name.delete(0,END)
    entry_location.delete(0,END)
    entry_remiza.delete(0,END)


    entry_name.focus()

    show_workers()



def show_workers():
    listbox_lista_worker.delete(0,END)
    for idx,worker in enumerate(workers):
        listbox_lista_worker.insert(idx,f'{idx+1}. {worker.name}')


def remove_worker ():
    i=listbox_lista_worker.index(ACTIVE)
    workers[i].marker.delete()
    workers.pop(i)
    show_workers()

def edit_worker ():
    i=listbox_lista_worker.index(ACTIVE)
    name=workers[i].name
    location=workers[i].location
    remiza=workers[i].remiza

    entry_name.insert(0,name)
    entry_location.insert(0,location)
    entry_remiza.insert(0,remiza)

    button_dodaj_obiekt.config(text='zapisz', command=lambda: update_worker(i))


def update_worker (i):
    new_name=entry_name.get()
    new_location=entry_location.get()
    new_remiza=entry_remiza.get()

    workers[i].name=new_name
    workers[i].location=new_location
    workers[i].remiza=new_remiza

    workers[i].marker.delete()
    workers[i].coordinates=workers[i].get_coordinates()
    workers[i].marker=map_widget.set_marker(workers[i].coordinates[0],workers[i].coordinates[1])

    entry_name.delete(0,END)
    entry_location.delete(0,END)
    entry_remiza.delete(0,END)

    button_dodaj_obiekt.config(text='Dodaj obiekt', command=add_who)
    show_workers()

def show_worker_details():
    i=listbox_lista_worker.index(ACTIVE)
    name=workers[i].name
    location=workers[i].location
    remiza=workers[i].remiza

    label_szczegoly_wartosc_name.config(text=name)
    label_szczegoly_wartosc_location.config(text=location)
    label_szczegoly_wartosc_remiza.config(text=remiza)

    map_widget.set_position(workers[i].coordinates[0],workers[i].coordinates[1])
    map_widget.set_zoom(17)

#end

#workers_in_users_commands


#end


#fire_command

def add_fire ():
    zmienna_nazwa=entry_name.get()
    zmienna_coordinates=entry_location.get()
    fire = Fire(name=zmienna_nazwa, location=zmienna_coordinates)
    fires.append(fire)

    entry_name.delete(0,END)
    entry_location.delete(0,END)
    entry_remiza.delete(0,END)

    entry_name.focus()

    show_fires()



def show_fires():
    listbox_lista_fire.delete(0,END)
    for idx,fire in enumerate(fires):
        listbox_lista_fire.insert(idx,f'{idx+1}. {fire.name}')


def remove_fire ():
    i=listbox_lista_fire.index(ACTIVE)
    fires[i].marker.delete()
    fires.pop(i)
    show_fires()

def edit_fire ():
    i=listbox_lista_fire.index(ACTIVE)
    name=fires[i].name
    location=fires[i].location

    entry_name.insert(0,name)
    entry_location.insert(0,location)

    button_dodaj_obiekt.config(text='zapisz', command=lambda: update_fire(i))


def update_fire (i):
    new_name=entry_name.get()
    new_location=entry_location.get()

    fires[i].name=new_name
    fires[i].location=new_location

    fires[i].marker.delete()
    fires[i].coordinates=fires[i].get_coordinates()
    fires[i].marker=map_widget.set_marker(fires[i].coordinates[0],fires[i].coordinates[1])

    entry_name.delete(0,END)
    entry_location.delete(0,END)
    entry_remiza.delete(0,END)

    button_dodaj_obiekt.config(text='Dodaj obiekt', command=add_who)
    show_fires()

def show_fire_details():
    i=listbox_lista_fire.index(ACTIVE)
    name=fires[i].name
    location=fires[i].location

    label_szczegoly_wartosc_name.config(text=name)
    label_szczegoly_wartosc_location.config(text=location)
    label_szczegoly_wartosc_remiza.config(text='...')

    map_widget.set_position(fires[i].coordinates[0],fires[i].coordinates[1])
    map_widget.set_zoom(17)

#end



#graphic

root = Tk()
root.geometry("1200x800")
root.title("Map Book MK")





ramka_lista_remizy=Frame(root)
ramka_lista_worker=Frame(root)
ramka_lista_fire=Frame(root)
ramka_formularz=Frame(root)
ramka_szczegoly_obiektow=Frame(root)
ramka_mapa=Frame(root)
ramka_notki=Frame(root)

ramka_lista_remizy.grid(row=0, column=0)
ramka_lista_worker.grid(row=0, column=1)
ramka_lista_fire.grid(row=0, column=2)
ramka_formularz.grid(row=0, column=3)
ramka_szczegoly_obiektow.grid(row=1, column=1)
ramka_mapa.grid(row=2, column=0, columnspan=4)
ramka_notki.grid(row=3, column=0, columnspan=4)

#ramka_lista_remizy
label_lista_remizy=Label(ramka_lista_remizy, text="Lista placówek")
label_lista_remizy.grid(row=0, column=0)
listbox_lista_remizy=Listbox(ramka_lista_remizy, width=40, height=10)
listbox_lista_remizy.grid(row=1, column=0,columnspan=3)
button_pokaz_szczegoly_obiektu=Button(ramka_lista_remizy, text='Pokaz szczegóły', command=show_user_details)
button_pokaz_szczegoly_obiektu.grid(row=2, column=0)
button_usun_obiekt=Button(ramka_lista_remizy, text='Usuń obiekt', command=remove_user)
button_usun_obiekt.grid(row=2, column=1)
button_edytuj_obiekt=Button(ramka_lista_remizy, text='Edytuj obiekt', command=edit_user)
button_edytuj_obiekt.grid(row=2, column=2)

#ramka_lista_worker
label_lista_worker=Label(ramka_lista_worker, text="Lista strażaków")
label_lista_worker.grid(row=0, column=0)
listbox_lista_worker=Listbox(ramka_lista_worker, width=40, height=10)
listbox_lista_worker.grid(row=1, column=0, columnspan=3)
button_pokaz_szczegoly_worker=Button(ramka_lista_worker, text='Pokaż szczegóły', command=show_worker_details)
button_pokaz_szczegoly_worker.grid(row=2, column=0)
button_usun_worker=Button(ramka_lista_worker, text='Usuń obiekt', command=remove_worker)
button_usun_worker.grid(row=2, column=1)
button_edytuj_obiekt=Button(ramka_lista_worker, text='Edytuj obiekt', command=edit_worker)
button_edytuj_obiekt.grid(row=2, column=2)

#ramka_lista_fire
label_lista_fire=Label(ramka_lista_fire, text="Lista pożarów")
label_lista_fire.grid(row=0, column=0)
listbox_lista_fire=Listbox(ramka_lista_fire, width=40, height=10)
listbox_lista_fire.grid(row=1, column=0, columnspan=3)
button_pokaz_szczegoly_obiektu=Button(ramka_lista_fire, text='Pokaż szczegóły', command=show_fire_details)
button_pokaz_szczegoly_obiektu.grid(row=2, column=0)
button_usun_obiekt=Button(ramka_lista_fire, text='Usuń obiekt', command=remove_fire)
button_usun_obiekt.grid(row=2, column=1)
button_edytuj_obiekt=Button(ramka_lista_fire, text='Edytuj obiekt', command=edit_fire)
button_edytuj_obiekt.grid(row=2, column=2)

#ramka_formularz
label_formularz=Label(ramka_formularz, text="Formularz")
label_formularz.grid(row=0, column=0)
label_name=Label(ramka_formularz, text="Nazwa:")
label_name.grid(row=1, column=0, sticky=W)
label_location=Label(ramka_formularz, text="Współrzędne:")
label_location.grid(row=2, column=0, sticky=W)
label_remiza=Label(ramka_formularz, text="Remiza:")
label_remiza.grid(row=3, column=0, sticky=W)

entry_name=Entry(ramka_formularz)
entry_name.grid(row=1, column=1)
entry_location=Entry(ramka_formularz)
entry_location.grid(row=2, column=1)
entry_remiza=Entry(ramka_formularz)
entry_remiza.grid(row=3, column=1)

button_dodaj_obiekt=Button(ramka_formularz, text='Dodaj obiekt', command=add_who)
button_dodaj_obiekt.grid(row=4, column=0)
button_default=Button(ramka_formularz,text='Domyślna lista',command=restore)
button_default.grid(row=5,column=0)

#ramka_szczegoly_obiektow
label_szczegoly_obiektow=Label(ramka_szczegoly_obiektow, text="Szczegoly obiektu:")
label_szczegoly_obiektow.grid(row=0, column=0, columnspan=3)
label_szczegoly_name=Label(ramka_szczegoly_obiektow, text="Nazwa:")
label_szczegoly_name.grid(row=1, column=0)
label_szczegoly_wartosc_name=Label(ramka_szczegoly_obiektow, text="....")
label_szczegoly_wartosc_name.grid(row=1, column=1)
label_szczegoly_location=Label(ramka_szczegoly_obiektow, text="Współrzędne:")
label_szczegoly_location.grid(row=1, column=4)
label_szczegoly_wartosc_location=Label(ramka_szczegoly_obiektow, text="....")
label_szczegoly_wartosc_location.grid(row=1, column=5)
label_szczegoly_remiza=Label(ramka_szczegoly_obiektow, text="Remiza:")
label_szczegoly_remiza.grid(row=1, column=6)
label_szczegoly_wartosc_remiza=Label(ramka_szczegoly_obiektow, text="....")
label_szczegoly_wartosc_remiza.grid(row=1, column=7)

#ramka_mapa

map_widget = tkintermapview.TkinterMapView(ramka_mapa, width=1200, height=500, corner_radius=5)
map_widget.grid(row=0, column=0)
map_widget.set_position(52.53,21.0)
map_widget.set_zoom(6)

#ramka_notki
label_notatka1=Label(ramka_notki, text="UWAGA: edytowanie wybranego pracownika należy wykonaywać tylko podczas wybranego domyślnego podglądu listy.")
label_notatka1.grid(row=0, column=0)

#end



root.mainloop()