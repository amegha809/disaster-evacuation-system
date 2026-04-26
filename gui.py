from tkinter import *
from tkinter import ttk

from location import get_loc as get_location_data
from nearestresource import find_nearest
from map import show_route

# ===== main window =====
root = Tk()
root.title("Disaster Evacuation System")
root.geometry("800x500")
root.configure(bg="#1e1e2f")

user_lat = None
user_lon = None
nearest_lat = None
nearest_lon = None
nearest_name = None     # added

# ===== header =====
top = Frame(root, bg="#2c2c54", height=70)
top.pack(fill=X)

Label(
    top,
    text="🚨 Disaster Evacuation System",
    font=("Arial",18,"bold"),
    bg="#2c2c54",
    fg="white"
).pack(pady=15)

# ===== main frame =====
main = Frame(root,bg="#1e1e2f")
main.pack(fill=BOTH,expand=True,padx=40,pady=20)

# ===== left side =====
left = Frame(main,bg="#2f3640",bd=2,relief=RIDGE)
left.pack(side=LEFT,fill=BOTH,expand=True,padx=10,pady=10)

Label(
    left,
    text="Input Details",
    font=("Arial",13,"bold"),
    bg="#2f3640",
    fg="white"
).pack(pady=10)

Label(left,text="Enter Place",bg="#2f3640",fg="white").pack()
place_box=ttk.Entry(left)
place_box.pack(pady=8,ipadx=20)

Label(left,text="Situation",bg="#2f3640",fg="white").pack()

list1=["Major Injury","Minor Injury","Need Shelter"]
choice=StringVar()

combo=ttk.Combobox(left,values=list1,textvariable=choice,state="readonly")
combo.current(0)
combo.pack(pady=8,ipadx=20)

Label(left,text="Longitude",bg="#2f3640",fg="white").pack()
long_box=ttk.Entry(left)
long_box.pack(pady=8,ipadx=20)

Label(left,text="Latitude",bg="#2f3640",fg="white").pack()
lat_box=ttk.Entry(left)
lat_box.pack(pady=8,ipadx=20)


# ===== FUNCTIONS =====

def detect_location():
    place=place_box.get().strip()

    output_box.config(state=NORMAL)
    output_box.delete("1.0",END)

    if place=="":
        output_box.insert(END,"Please enter place name")
        output_box.config(state=DISABLED)
        return

    lat,lon=get_location_data(place)

    if lat is not None and lon is not None:

        lat_box.delete(0,END)
        long_box.delete(0,END)

        lat_box.insert(0,str(lat))
        long_box.insert(0,str(lon))

        output_box.insert(END,"Location detected successfully")

    else:
        output_box.insert(END,"Location not found")

    output_box.config(state=DISABLED)



def find_data():
    global user_lat,user_lon,nearest_lat,nearest_lon,nearest_name

    place=place_box.get().strip()
    val=choice.get()

    output_box.config(state=NORMAL)
    output_box.delete("1.0",END)

    if place=="":
        output_box.insert(END,"Please enter place name")
        output_box.config(state=DISABLED)
        return


    if val=="Minor Injury":
        ch=1
    elif val=="Major Injury":
        ch=2
    else:
        ch=3


    try:
        user_lat=float(lat_box.get())
        user_lon=float(long_box.get())

    except:
        output_box.insert(END,"Please click Detect Location first")
        output_box.config(state=DISABLED)
        return


    result, nearest_name, nearest_lat, nearest_lon = find_nearest(place,ch)

    output_box.insert(END,result)
    output_box.config(state=DISABLED)



def open_route():

    global user_lat,user_lon,nearest_lat,nearest_lon,nearest_name

    output_box.config(state=NORMAL)
    output_box.delete("1.0",END)

    if user_lat is None or user_lon is None or nearest_lat is None or nearest_lon is None:
        output_box.insert(END,"Please find nearest resource first")
        output_box.config(state=DISABLED)
        return


    result = show_route(
        user_lat,
        user_lon,
        nearest_lat,
        nearest_lon,
        nearest_name
    )

    output_box.insert(END,result)
    output_box.config(state=DISABLED)



# ===== BUTTONS =====
Button(
    left,
    text="📍 Detect Location",
    bg="#44bd32",
    fg="white",
    command=detect_location
).pack(pady=8)

Button(
    left,
    text="🏥 Find Nearest Resource",
    bg="#e84118",
    fg="white",
    command=find_data
).pack(pady=10)

Button(
    left,
    text="🗺 Show Route",
    bg="#00a8ff",
    fg="white",
    command=open_route
).pack(pady=8)


# ===== right side =====
right=Frame(main,bg="#2f3640",bd=2,relief=RIDGE)
right.pack(side=RIGHT,fill=BOTH,expand=True,padx=10,pady=10)

Label(
    right,
    text="Result",
    font=("Arial",13,"bold"),
    bg="#2f3640",
    fg="white"
).pack(pady=10)

output_box=Text(right,height=10,width=50,bg="#dcdde1")
output_box.pack(padx=10,pady=10)
output_box.config(state=DISABLED)


# ===== footer =====
Label(
root,
text="Stay Safe 🚨",
bg="#2c2c54",
fg="white"
).pack(fill=X)

root.mainloop()