from tkinter import *
from tkinter import ttk 
from tkinter import messagebox
import sqlite3

root = Tk()

conn = sqlite3.connect("perpustakaan.db")
cursor = conn.cursor()

def create_table():
    cursor.execute("DROP TABLE IF EXISTS LIBRARY")
    query = """
    CREATE TABLE LIBRARY(
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        JUDUL TEXT ,
        KODE_KATEGORI TEXT NOT NULL,
        KATEGORI TEXT,
        KODE_BUKU TEXT NOT NULL,
        PENULIS TEXT,
        PENERBIT TEXT,
        TAHUN TEXT,
        STOK INT,
        NO_RAK TEXT NOT NULL
        )
    """
    cursor.execute(query)
    conn.commit()

def IsFirst(table_name):
    query = """ SELECT count(name) FROM sqlite_master WHERE type='table' AND name='{}' """.format(table_name)
    cursor.execute(query)
    conn.commit()
    if cursor.fetchone()[0]==1 :
        return False
    else :
        return True
    
def select_all():
    query = "SELECT ID, KODE_KATEGORI, KATEGORI FROM LIBRARY" 
    cursor.execute(query)
    rows = cursor.fetchall()
    update_trv(rows)   
    
def update_trv(rows):
    trv.delete(*trv.get_children())
    for i in rows:
        trv.insert('', END, values=i)
        
def update_people():
    if messagebox.askyesno("Harap Konfirmasi", "Apakah Anda Serius Ingin Memperbaharui Data Ini?"):
        query = """
            UPDATE LIBRARY SET KODE_KATEGORI=:KODE_KATEGORI, KATEGORI=:KATEGORI
            WHERE ID=:ID
        """
        params = {
            'ID' : v_id.get(),
            'KODE_KATEGORI' : v_kode_kategori.get(),
            'KATEGORI' : v_kategori.get(),
        }
        cursor.execute(query, params)
        conn.commit()
        clear_field()
        select_all()
    else:
        return True

def add_new():
    query = """
        INSERT INTO LIBRARY
        (JUDUL, KATEGORI, KODE_BUKU, PENULIS, PENERBIT, TAHUN, STOK, NO_RAK, KODE_KATEGORI)
        VALUES (:JUDUL, :KATEGORI, :KODE_BUKU, :PENULIS, :PENERBIT, :TAHUN, :STOK, :NO_RAK, :KODE_KATEGORI)
        """
        
    params = {
        'JUDUL' : v_judul.get(),
        'KODE_KATEGORI' : v_kode_kategori.get(),
        'KATEGORI' : v_kategori.get(),
        'KODE_BUKU' : v_kode_buku.get(),
        'PENULIS' : v_penulis.get(),
        'PENERBIT': v_penerbit.get(),
        'TAHUN' : v_tahun_terbit.get(),
        'STOK' : v_stok.get(),
        'NO_RAK' : v_no_rak.get()
    }
    cursor.execute(query, params)
    conn.commit()
    select_all()
    clear_field()

def getrow(event):
    rowid = trv.identify_row(event.y)
    item = trv.item(rowid)
    v_id.set(item['values'][0])
    v_kode_kategori.set(item['values'][1])
    v_kategori.set(item['values'][2])

def clear_field():
    kode_kategori_field.delete(0,END)
    kategori_field.set('')
    

def delet_book():
    id = v_id.get()
    if(messagebox.askyesno("Harap Konfirmasi", "Apakah Anda Serius Ingin Menghapus Data Ini?")):
        query = "DELETE FROM LIBRARY WHERE ID = {}".format(id)
        cursor.execute(query)
        conn.commit()
        clear_field()
        select_all()
    else:
        return True
    

def search():
    q2 = q.get()
    query = """
    SELECT ID, KODE_KATEGORI , KATEGORI FROM LIBRARY WHERE KATEGORI LIKE {}
    """.format("'%"+q2+"%'")
    cursor.execute(query)
    conn.commit()
    rows = cursor.fetchall()
    update_trv(rows)

def clear():
    ent.delete(0, END)
    clear_field()
    select_all()

#Wrapper
wrapper1 = LabelFrame (root, text="Daftar Kategori")
wrapper2 = LabelFrame (root, text="Pencarian")
wrapper3 = LabelFrame (root, text="Data Kategori")

#Wrapper Position
wrapper1.pack(fill="both", expand="yes", padx=20, pady=20)
wrapper2.pack(fill="both", padx=20, pady=5)
wrapper3.pack(fill="both", padx=20, pady=10)

#form
v_id = IntVar()
v_judul = StringVar()
v_kategori = StringVar()
v_kode_buku = StringVar()
v_penulis = StringVar()
v_penerbit = StringVar()
v_tahun_terbit = StringVar()
v_stok = IntVar()
v_no_rak = StringVar()
v_kode_kategori = StringVar()

kode_kategori = Label(wrapper3, text="Kode Kategori")
kode_kategori_field = Entry(wrapper3, textvariable=v_kode_kategori)
kode_kategori.grid(row=0, column=0, sticky="w", pady=4)
kode_kategori_field.grid(row=0, column=1, columnspan=2, sticky="w", pady=4, padx=10)

kategori = Label(wrapper3, text="Kategori")
kategori_field = ttk.Combobox (wrapper3, width=17, textvariable = v_kategori)
kategori_field['values'] = (
                    '0 - Umum',
                    '1 - Fislafat Dan Psikologi',
                    '2 - Agama',
                    '3 - Sosial',
                    '4 - Bahasa',
                    '5 - Sains Dan Matematika',
                    '6 - Teknology',
                    '7 - Seni Dan Rekreasi',
                    '8 - Literatur Dan Sastra',
                    '9 - Sejarah Dan Geografi',
                )
kategori.grid(row=1, column=0, sticky="W", pady=4)
kategori_field.grid(row=1, column=1, columnspan=2, sticky="W", pady=4, padx=10)

frame_btn = Frame(wrapper3)
up_btn = Button (frame_btn, text = "Update", command= update_people)
add_btn = Button (frame_btn, text = "Tambah Baru", command= add_new)
delet_btn = Button (frame_btn, text = "Hapus", command= delet_book)

frame_btn.grid(row=4, column=0, columnspan=5, sticky="w", pady=10)
add_btn.pack(side=LEFT,padx=5)
up_btn.pack(side=LEFT,padx=5)
delet_btn.pack(side=LEFT,padx=5)

q = StringVar()
lbl = Label(wrapper2, text="Search")
lbl.pack(side=LEFT, padx=5, pady=5)
ent =  Entry(wrapper2, textvariable=q)
ent.pack(side=LEFT, padx=5, pady= 5)
btn = Button(wrapper2, text="Search", command=search)
btn.pack(side=LEFT, padx=6, pady=5)
cbtn = Button(wrapper2, text="Clear", command=clear)
cbtn.pack(side=LEFT, padx=6, pady=5)

#Table Data Buku
trv = ttk.Treeview(wrapper1, column=(0,1,2), show="headings", height=8)
style = ttk.Style()
#["aqua","step","clam","alt","default","classic"]
style.theme_use("classic")
trv.pack(side=RIGHT)
trv.place(x=0, y=0)

trv.heading(0, text="NO")
trv.heading(1, text="Kode Kategori")
trv.heading(2, text="Kategori")

trv.column(0, width=30, minwidth=30, anchor=CENTER)
trv.column(1, width=200, minwidth=200, anchor=CENTER)
trv.column(2, width=200, minwidth=200, anchor=CENTER)

trv.bind('<Double 1>',getrow)

#Scroll Bar1
yscrolbar = Scrollbar(wrapper1, orient="vertical", command=trv.yview)
yscrolbar.pack(side=RIGHT, fill="y")
xscrolbar = Scrollbar(wrapper1, orient="horizontal", command=trv.xview)
xscrolbar.pack(side=BOTTOM, fill="x")

trv.configure(yscrollcommand=yscrolbar.set, xscrollcommand=xscrolbar.set)

if __name__ == '__main__':
    root.title("Aplikasi Data Perpustakaan")
    root.geometry("500x465")
    root.resizable(FALSE,FALSE)
    if(IsFirst("LIBRARY")):
        create_table()
    else:
        select_all()
    root.mainloop()