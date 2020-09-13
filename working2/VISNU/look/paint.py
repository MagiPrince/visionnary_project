import tkinter as tk
import cv2
import os, os.path
from PIL import Image, ImageDraw

root = tk.Tk()

canvas = tk.Canvas(root, width=200, height=200, highlightbackground="gray")
canvas.pack()
canvas.old_coords = None

image=Image.new("RGB",(200,200),(255,255,255))
drawing=ImageDraw.Draw(image)

btn_text = tk.StringVar()

# Permet de dessiner dans un canvas
def draw(event):
    x, y = event.x, event.y
    if canvas.old_coords:
        x1, y1 = canvas.old_coords
        canvas.create_line(x, y, x1, y1)
        drawing.line(((x1,y1),(x,y)),(0,0,0),width=3)
    canvas.old_coords = x, y

# Redéfini les coordonnées à none lorsque le clic est relâché
def reset_coords(event):
    canvas.old_coords = None

# Envoie l'image au serveur
def send_data():
    filename = "temp.png"
    image.save(filename)
    foo = Image.open(filename)
    foo = foo.resize((20,20),Image.ANTIALIAS)
    foo.save(filename,quality=95)
    img = cv2.imread(filename,0)
    ret,thresh1 = cv2.threshold(img, 225, 255, cv2.THRESH_BINARY)
    cv2.imwrite(filename, thresh1)
    os.system("http POST localhost:8000/images Content-Type:image/png < temp.png")
    #f = open(os.path.dirname(__file__)+ '/../prediction.txt',"r")
    f = open('prediction.txt',"r")
    val = f.readlines()
    f.close()
    text = "Le résultat est : " + str(val)
    global btn_text
    btn_text.set(text)
    os.remove("temp.png")

# Efface l'image afin de pouvoir redessiner
def clear():
    canvas.delete("all")
    global drawing
    drawing.rectangle(((0,0),(200,200)),fill="white")
    global btn_text
    btn_text.set("")

root.bind('<B1-Motion>', draw)
root.bind('<ButtonRelease-1>', reset_coords)

button_clear = tk.Button(root, text="Clear", highlightbackground='black', command=clear)
button_clear.pack(side=tk.LEFT)

button_send = tk.Button(root, text="Send", highlightbackground='black', command=send_data)
button_send.pack(side=tk.RIGHT)

message = tk.Label(textvariable=btn_text)
message.pack()

root.mainloop()