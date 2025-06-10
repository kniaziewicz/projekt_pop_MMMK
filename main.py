from tkinter import *

import tkintermapview



users:list=[]

class User:
    def __init__(self,name,location):
        self.name = name
        self.location = location
        self.coordinates = self.get_coordinates()
        self.marker = map_widget.set_marker(self.coordinates[0],self.coordinates[1])

    def get_coordinates(self)->list:
        import requests
        from bs4 import BeautifulSoup
        url=f"https://pl.wikipedia.org/wiki/{self.location}"
        response = requests.get(url).text
        response_html = BeautifulSoup(response, "html.parser")
        longitude = float(response_html.select(".longitude")[1].text.replace(",","."))
        latitude = float(response_html.select(".latitude")[1].text.replace(",","."))
        print(longitude)
        print(latitude)
        return [latitude,longitude]

def add_user ():
    zmienna_imie=entry_name.get()
    zmienna_miejscowosc=entry_location.get()
    user = User(name=zmienna_imie, location=zmienna_miejscowosc)
    users.append(user)

    entry_name.delete(0,END)
    entry_location.delete(0,END)

    entry_name.focus()

    show_users()



def show_users():
    listbox_lista_obiektow.delete(0,END)
    for idx,user in enumerate(users):
        listbox_lista_obiektow.insert(idx,f'{idx+1}. {user.name}')



def remove_user ():
    i=listbox_lista_obiektow.index(ACTIVE)
    users[i].marker.delete()
    users.pop(i)
    show_users()

def edit_user ():
    i=listbox_lista_obiektow.index(ACTIVE)
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

    button_dodaj_obiekt.config(text='Dodaj obiekt', command=add_user)
    show_users()

def show_user_details():
    i=listbox_lista_obiektow.index(ACTIVE)
    name=users[i].name
    location=users[i].location

    label_szczegoly_wartosc_name.config(text=name)
    label_szczegoly_wartosc_location.config(text=location)

    map_widget.set_position(users[i].coordinates[0],users[i].coordinates[1])
    map_widget.set_zoom(17)















root = Tk()
root.geometry("1444x1444")
root.title("Map Book MK")





ramka_lista_obiektow=Frame(root)
ramka_formularz=Frame(root)
ramka_szczegoly_obiektow=Frame(root)
ramka_mapa=Frame(root)

ramka_lista_obiektow.grid(row=0, column=0)
ramka_formularz.grid(row=0, column=1)
ramka_szczegoly_obiektow.grid(row=1, column=0, columnspan=2)
ramka_mapa.grid(row=2, column=0, columnspan=2)

#ramka_lista_obiektow
label_lista_obiektow=Label(ramka_lista_obiektow, text="Lista placówek")
label_lista_obiektow.grid(row=0, column=0)
listbox_lista_obiektow=Listbox(ramka_lista_obiektow, width=50, height=10)
listbox_lista_obiektow.grid(row=1, column=0, columnspan=3)
button_pokaz_szczegoly_obiektu=Button(ramka_lista_obiektow, text='Pokaz szczegóły', command=show_user_details)
button_pokaz_szczegoly_obiektu.grid(row=2, column=0)
button_usun_obiekt=Button(ramka_lista_obiektow, text='Usuń obiekt', command=remove_user)
button_usun_obiekt.grid(row=2, column=1)
button_edytuj_obiekt=Button(ramka_lista_obiektow, text='Edytuj obiekt', command=edit_user)
button_edytuj_obiekt.grid(row=2, column=2)

#ramka_formularz
label_formularz=Label(ramka_formularz, text="Formularz")
label_formularz.grid(row=0, column=0, columnspan=2)
label_name=Label(ramka_formularz, text="Nazwa:")
label_name.grid(row=1, column=0, sticky=W)
label_location=Label(ramka_formularz, text="Miejscowość:")
label_location.grid(row=3, column=0, sticky=W)

entry_name=Entry(ramka_formularz)
entry_name.grid(row=1, column=1)
entry_location=Entry(ramka_formularz)
entry_location.grid(row=3, column=1)

button_dodaj_obiekt=Button(ramka_formularz, text='Dodaj obiekt', command=add_user)
button_dodaj_obiekt.grid(row=5, column=0, columnspan=2)

#ramka_szczegoly_obiektow
label_szczegoly_obiektow=Label(ramka_szczegoly_obiektow, text="Szczegoly obiektu:")
label_szczegoly_obiektow.grid(row=0, column=0)
label_szczegoly_name=Label(ramka_szczegoly_obiektow, text="Nazwa:")
label_szczegoly_name.grid(row=1, column=0)
label_szczegoly_wartosc_name=Label(ramka_szczegoly_obiektow, text="....")
label_szczegoly_wartosc_name.grid(row=1, column=1)
label_szczegoly_location=Label(ramka_szczegoly_obiektow, text="Miejscowość:")
label_szczegoly_location.grid(row=1, column=4)
label_szczegoly_wartosc_location=Label(ramka_szczegoly_obiektow, text="....")
label_szczegoly_wartosc_location.grid(row=1, column=5)

#ramka_mapa
map_widget = tkintermapview.TkinterMapView(ramka_mapa, width=1200, height=500, corner_radius=5)
map_widget.grid(row=0, column=0, columnspan=2)
map_widget.set_position(52.53,21.0)
map_widget.set_zoom(6)





root.mainloop()