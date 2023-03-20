from tkinter import *
from tkinter import ttk 
from tkinter import messagebox
import sqlite3

root = Tk()

conn = sqlite3.connect("perpustakaan.db")
cursor = conn.cursor()

def create_table():
    cursor.execute("DROP TABLE IF EXISTS MEMBER")
    query = """
    CREATE TABLE MEMBER(
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        NO_BUKTI TEXT NOT NULL,
        TANGGAL_PINJAM TEXT NOT NULL,
        KODE_ANGGOTA TEXT NOT NULL,
        KODE_BUKU1 TEXT,
        KODE_BUKU2 TEXT,
        TANGGAL_PENGEMBALIAN TEXT,
        TANGGAL_DIKEMBALIKAN INT,
        STATUS_PEMINJAMAN TEXT NOT NULL, 
        DENDA TEXT,
        NAMA_ANGGOTA TEXT NOT NULL,
        TITLE TEXT NOT NULL,
        JENIS_KELAMIN TEXT NOT NULL,
        ALAMAT TEXT
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
    query = "SELECT ID, KODE_ANGGOTA, NAMA_ANGGOTA, TITLE, JENIS_KELAMIN, ALAMAT FROM MEMBER" 
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
            UPDATE MEMBER SET KODE_ANGGOTA=:KODE_ANGGOTA, NAMA_ANGGOTA=:NAMA_ANGGOTA, TITLE=:TITLE, JENIS_KELAMIN=:JENIS_KELAMIN, ALAMAT=:ALAMAT
            WHERE ID=:ID
        """
        params = {
            'ID' : v_id.get(),
            'KODE_ANGGOTA' : v_kode_anggota.get(),
            'NAMA_ANGGOTA' : v_nama_anggota.get(),
            'TITLE' : v_title.get(),
            'JENIS_KELAMIN' : v_jenis_kelamin.get(),
            'ALAMAT': v_alamat.get()
        }
        cursor.execute(query, params)
        conn.commit()
        clear_field()
        select_all()
    else:
        return True

def add_new():
    query = """
        INSERT INTO MEMBER
        (NO_BUKTI, TANGGAL_PINJAM, KODE_ANGGOTA, KODE_BUKU1, KODE_BUKU2, TANGGAL_PENGEMBALIAN, TANGGAL_DIKEMBALIKAN, STATUS_PEMINJAMAN, DENDA, TITLE, JENIS_KELAMIN, DENDA, NAMA_ANGGOTA )
        VALUES (:NO_BUKTI, :TANGGAL_PINJAM, :KODE_ANGGOTA, :KODE_BUKU1, :KODE_BUKU2, :TANGGAL_PENGEMBALIAN, :TANGGAL_DIKEMBALIKAN, :STATUS_PEMINJAMAN, :DENDA, :TITLE, :JENIS_KELAMIN, :DENDA, :NAMA_ANGGOTA )
        """
        
    params = {
        'NO_BUKTI' : v_no_bukti.get(), 
        'TANGGAL_PINJAM' : v_tanggal_pinjam.get(), 
        'KODE_ANGGOTA' : v_kode_anggota.get(),
        'KODE_BUKU1' : v_kode_buku1.get(), 
        'KODE_BUKU2' : v_kode_buku2.get(), 
        'TANGGAL_PENGEMBALIAN' : v_tanggal_pengembalian.get(), 
        'TANGGAL_DIKEMBALIKAN' : v_tanggal_dikembalikan.get(), 
        'STATUS_PEMINJAMAN' : v_status_peminjaman.get(),
        'NAMA_ANGGOTA' : v_nama_anggota.get(),
        'TITLE' : v_title.get(),
        'JENIS_KELAMIN' : v_jenis_kelamin.get(),
        'ALAMAT': v_alamat.get(),
        'DENDA' : v_denda.get()
    }
    cursor.execute(query, params)
    conn.commit()
    select_all()
    clear_field()

def getrow(event):
    rowid = trv.identify_row(event.y)
    item = trv.item(rowid)
    v_id.set(item['values'][0])
    v_kode_anggota.set(item['values'][1])
    v_nama_anggota.set(item['values'][2])
    v_title.set(item['values'][3])
    v_jenis_kelamin.set(item['values'][4])
    v_alamat.set(item['values'][5])

def clear_field():
    kode_anggota_field.delete(0,END)
    nama_anggota_field.delete(0,END)
    title_field.set('')
    alamat_field.delete(0,END)

def delet_book():
    id = v_id.get()
    if(messagebox.askyesno("Harap Konfirmasi", "Apakah Anda Serius Ingin Menghapus Data Ini?")):
        query = "DELETE FROM MEMBER WHERE ID = {}".format(id)
        cursor.execute(query)
        conn.commit()
        clear_field()
        select_all()
    else:
        return True
    
def search():
    q2 = q.get()
    query = """
    SELECT ID, KODE_ANGGOTA, NAMA_ANGGOTA, TITLE, JENIS_KELAMIN, 
    ALAMAT FROM MEMBER WHERE KODE LIKE {} OR TITLE LIKE {} OR JENIS_KELAMIN LIKE {}
    """.format("'%"+q2+"%'","'%"+q2+"%'","'%"+q2+"%'")
    cursor.execute(query)
    conn.commit()
    rows = cursor.fetchall()
    update_trv(rows)

def clear():
    ent.delete(0, END)
    clear_field()
    select_all()
    L.select()

#Wrapper
wrapper1 = LabelFrame (root, text="Daftar Anggota")
wrapper2 = LabelFrame (root, text="Pencarian")
wrapper3 = LabelFrame (root, text="Data Anggota")

#Wrapper Position
wrapper1.pack(fill="both", expand="yes", padx=20, pady=10)
wrapper2.pack(fill="both", padx=20, pady=5)
wrapper3.pack(fill="both", padx=20, pady=10)

#form
v_id = IntVar()
v_kode_anggota = StringVar()
v_nama_anggota = StringVar()
v_title = StringVar()
v_jenis_kelamin = StringVar()
v_alamat = StringVar()
v_no_bukti = StringVar()
v_tanggal_pinjam = StringVar()
v_kode_buku1 = StringVar()
v_kode_buku2 = StringVar()
v_tanggal_pengembalian = StringVar()
v_tanggal_dikembalikan = StringVar()
v_status_peminjaman = StringVar()
v_denda = StringVar()

kode_anggota = Label(wrapper3, text="Kode Anggota")
kode_anggota_field = Entry(wrapper3, textvariable=v_kode_anggota)
kode_anggota.grid(row=0, column=0, sticky="w", pady=4)
kode_anggota_field.grid(row=0, column=1, columnspan=2, sticky="w", pady=4, padx=10)

nama_anggota = Label(wrapper3, text="Nama Anggota")
nama_anggota_field = Entry(wrapper3, textvariable = v_nama_anggota)
nama_anggota.grid(row=1, column=0, sticky="W", pady=4)
nama_anggota_field.grid(row=1, column=1, columnspan=2, sticky="W", pady=4, padx=10)

title = Label(wrapper3, text="Title")
title_field = ttk.Combobox(wrapper3,  width=17, textvariable = v_title)
title_field['values'] = (
                    'Guru Atau Dosen',
                    'Karyawan',
                    'Mahasiswa',
                    'SMA',
                    'SMP',
                    'SD'    
                )
title.grid(row=2, column=0, sticky="w", pady=4)
title_field.grid(row=2, column=1, columnspan=2, sticky="w", pady=4, padx=10)

Label (wrapper3, text="Jenis Kelamin").grid(row=3, column=0, sticky="w", pady=4, padx=10)
L = Radiobutton (wrapper3, text='Laki Laki', value='Laki - laki', variable=v_jenis_kelamin)
L.grid(row=3, column=1, sticky="w", pady=4, padx=10)
L.select()
P = Radiobutton (wrapper3, text='Perempuan', value='Perempuan', variable=v_jenis_kelamin)
P.grid(row=3, column=2, sticky="w", pady=4, padx=10)

alamat = Label(wrapper3, text="Alamat")
alamat_field = Entry(wrapper3, textvariable=v_alamat)
alamat.grid(row=0, column=3, sticky="w", pady=4)
alamat_field.grid(row=0, column=4, columnspan=2, sticky="w", pady=4, padx=10)

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
trv = ttk.Treeview(wrapper1, column=(0,1,2,3,4,5), show="headings", height=8)
style = ttk.Style()
#["aqua","step","clam","alt","default","classic"]
style.theme_use("classic")
trv.pack(side=RIGHT)
trv.place(x=0, y=0)

trv.heading(0, text="Id")
trv.heading(1, text="Kode")
trv.heading(2, text="Nama")
trv.heading(3, text="Title")
trv.heading(4, text="Jenis Kelamin")
trv.heading(5, text="Alamat")

trv.column(0, stretch=NO, minwidth=0, width=0)
trv.column(1, width=50, minwidth=75, anchor=CENTER)
trv.column(2, width=130, minwidth=180, anchor=CENTER)
trv.column(3, width=105, minwidth=105, anchor=CENTER)
trv.column(4, width=50, minwidth=105, anchor=CENTER)
trv.column(5, width=400, minwidth=400, anchor=CENTER)

trv.bind('<Double 1>',getrow)

#Scroll Bar1
yscrolbar = Scrollbar(wrapper1, orient="vertical", command=trv.yview)
yscrolbar.pack(side=RIGHT, fill="y")
xscrolbar = Scrollbar(wrapper1, orient="horizontal", command=trv.xview)
xscrolbar.pack(side=BOTTOM, fill="x")

trv.configure(yscrollcommand=yscrolbar.set, xscrollcommand=xscrolbar.set)

if __name__ == '__main__':
    root.title("Aplikasi Data Perpustakaan")
    root.geometry("800x510")
    root.resizable(FALSE,FALSE)
    if(IsFirst("MEMBER")):
        create_table()
    else:
        select_all()
    root.mainloop()