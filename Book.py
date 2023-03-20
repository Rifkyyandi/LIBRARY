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
    query = "SELECT ID, JUDUL, KATEGORI, KODE_BUKU, PENULIS, PENERBIT, TAHUN, STOK, NO_RAK FROM LIBRARY" 
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
            UPDATE LIBRARY SET JUDUL=:JUDUL, KATEGORI=:KATEGORI, KODE_BUKU=:KODE_BUKU, PENULIS=:PENULIS, PENERBIT=:PENERBIT, TAHUN=:TAHUN, STOK=:STOK, NO_RAK=:NO_RAK
            WHERE ID=:ID
        """
        params = {
            'ID' : v_id.get(),
            'JUDUL' : v_judul.get(),
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
        clear_field()
        select_all()
    else:
        return True

def add_new():
    query = """
        INSERT INTO LIBRARY
        (JUDUL, KATEGORI, KODE_KATEGORI, KODE_BUKU, PENULIS, PENERBIT, TAHUN, STOK, NO_RAK)
        VALUES (:JUDUL, :KATEGORI, :KODE_KATEGORI, :KODE_BUKU, :PENULIS, :PENERBIT, :TAHUN, :STOK, :NO_RAK)
        """
        
    params = {
        'JUDUL' : v_judul.get(),
        'KATEGORI' : v_kategori.get(),
        'KODE_BUKU' : v_kode_buku.get(),
        'KODE_KATEGORI' : v_kode_kategori.get(),
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
    v_judul.set(item['values'][1])
    v_kode_buku.set("00"+str(item['values'][3]))
    v_kategori.set(item['values'][2])
    v_penulis.set(item['values'][4])
    v_penerbit.set(item['values'][5])
    v_tahun_terbit.set(item['values'][6])
    v_stok.set(item['values'][7])
    v_no_rak.set("00"+str(item['values'][8]))

def clear_field():
    judul_field.delete(0,END)
    penulis_field.delete(0,END)
    penerbit_field.delete(0,END)
    tahun_terbit_field.delete(0,END)
    stok_field.delete(0,END)
    kategori_field.set('')
    kode_buku_field.set('')
    no_rak_field.set('')
    
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
    SELECT ID, JUDUL, KATEGORI, KODE_BUKU, PENULIS, PENERBIT, TAHUN, STOK, NO_RAK FROM LIBRARY WHERE JUDUL LIKE {} OR NO_RAK LIKE {}
    """.format("'%"+q2+"%'","'%"+q2+"%'")
    cursor.execute(query)
    conn.commit()
    rows = cursor.fetchall()
    update_trv(rows)

def clear():
    ent.delete(0, END)
    clear_field()
    select_all()

#Wrapper
wrapper1 = LabelFrame (root, text="Daftar Buku")
wrapper2 = LabelFrame (root, text="Pencarian")
wrapper3 = LabelFrame (root, text="Data Buku")

#Wrapper Position
wrapper1.pack(fill="both", expand="yes", padx=20, pady=20)
wrapper2.pack(fill="both", padx=20, pady=5)
wrapper3.pack(fill="both", padx=20, pady=10)

#form
v_id = IntVar()
v_judul = StringVar()
v_kategori = StringVar()
v_kode_kategori = StringVar()
v_kode_buku = StringVar()
v_penulis = StringVar()
v_penerbit = StringVar()
v_tahun_terbit = StringVar()
v_stok = IntVar()
v_no_rak = StringVar()

judul = Label(wrapper3, text="Judul")
judul_field = Entry(wrapper3, textvariable=v_judul)
judul.grid(row=0, column=0, sticky="w", pady=4)
judul_field.grid(row=0, column=1, columnspan=2, sticky="w", pady=4, padx=10)

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

kode_buku = Label(wrapper3, text="Kode Buku")
kode_buku_field = ttk.Combobox (wrapper3, width=17, textvariable = v_kode_buku)
kode_buku_field['values'] = ('1001','1002','1003','1004','1005','1006','1007','1008','1009','1010')
kode_buku.grid(row=2, column=0, sticky="w", pady=4)
kode_buku_field.grid(row=2, column=1, columnspan=2, sticky="w", pady=4, padx=10)

penulis = Label(wrapper3, text="Penulis")
penulis_field = Entry(wrapper3, textvariable=v_penulis)
penulis.grid(row=3, column=0, sticky="w", pady=4)
penulis_field.grid(row=3, column=1, columnspan=2, sticky="w", pady=4, padx=10)

penerbit = Label(wrapper3, text="Penerbit")
penerbit_field = Entry(wrapper3, textvariable=v_penerbit)
penerbit.grid(row=0, column=3, sticky="w", pady=4)
penerbit_field.grid(row=0, column=4, columnspan=2, sticky="w", pady=4, padx=10)

tahun_terbit = Label(wrapper3, text="Tahun Terbit")
tahun_terbit_field = Entry(wrapper3, textvariable=v_tahun_terbit)
tahun_terbit.grid(row=1, column=3, sticky="w", pady=4)
tahun_terbit_field.grid(row=1, column=4, columnspan=2, sticky="w", pady=4, padx=10)

stok = Label(wrapper3, text="Stok")
stok_field = Entry(wrapper3, textvariable=v_stok)
stok.grid(row=2, column=3, sticky="w", pady=4)
stok_field.grid(row=2, column=4, columnspan=2, sticky="w", pady=4, padx=10)

no_rak = Label(wrapper3, text="No Rak")
no_rak_field = ttk.Combobox (wrapper3, width=17, textvariable = v_no_rak)
no_rak_field['values'] = ('001','002','003','004','005','006','007','008','009','010')
no_rak.grid(row=3, column=3, sticky="w", pady=4)
no_rak_field.grid(row=3, column=4, columnspan=2, sticky="w", pady=4, padx=10)

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
trv = ttk.Treeview(wrapper1, column=(0,1,2,3,4,5,6,7,8), show="headings", height=10)
style = ttk.Style()
#["aqua","step","clam","alt","default","classic"]
style.theme_use("classic")
trv.pack(side=RIGHT)
trv.place(x=0, y=0)

trv.heading(0, text="Id")
trv.heading(1, text="Judul")
trv.heading(2, text="Kategori")
trv.heading(3, text="Kode Buku")
trv.heading(4, text="Penulis")
trv.heading(5, text="Penerbit")
trv.heading(6, text="Tahun Terbit")
trv.heading(7, text="Stok")
trv.heading(8, text="No Rak")

trv.column(0, stretch=NO, minwidth=0, width=0)
trv.column(1, width=170, minwidth=170, anchor=CENTER)
trv.column(2, width=105, minwidth=145, anchor=CENTER)
trv.column(3, width=55, minwidth=85, anchor=CENTER)
trv.column(4, width=95, minwidth=105, anchor=CENTER)
trv.column(5, width=95, minwidth=105, anchor=CENTER)
trv.column(6, width=85, minwidth=115, anchor=CENTER)
trv.column(7, width=55, minwidth=55, anchor=CENTER)
trv.column(8, width=70, minwidth=85, anchor=CENTER)

trv.bind('<Double 1>',getrow)

#Scroll Bar1
yscrolbar = Scrollbar(wrapper1, orient="vertical", command=trv.yview)
yscrolbar.pack(side=RIGHT, fill="y")
xscrolbar = Scrollbar(wrapper1, orient="horizontal", command=trv.xview)
xscrolbar.pack(side=BOTTOM, fill="x")

trv.configure(yscrollcommand=yscrolbar.set, xscrollcommand=xscrolbar.set)

if __name__ == '__main__':
    root.title("Aplikasi Data Perpustakaan")
    root.geometry("795x560")
    root.resizable(FALSE,FALSE)
    if(IsFirst("LIBRARY")):
        create_table()
    else:
        select_all()
    root.mainloop()