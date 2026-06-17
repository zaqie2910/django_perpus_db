from django.shortcuts import render, redirect, get_object_or_404
from django.db import connection
from .models import Siswa, Buku, Peminjaman # Pastikan nama model kamu seperti ini

# ==================== 1. MODUL DASHBOARD ====================
def dashboard_view(request):
    # Mengambil total data untuk ditampilkan di kartu statistik
    context = {
        'total_siswa': Siswa.objects.count(),
        'total_buku': Buku.objects.count(),
        'total_peminjaman': Peminjaman.objects.filter(sudah_kembali=False).count(), # Hitung yang belum kembali
    }
    return render(request, 'dashboard/index.html', context)


# ==================== 2. MODUL SISWA / USER ====================
def siswa_list(request):
    data_user = Siswa.objects.all().order_by('-id')
    return render(request, 'siswa/list.html', {'data_user': data_user})

def siswa_tambah(request):
    if request.method == 'POST':
        Siswa.objects.create(
            nama=request.POST.get('nama'),
            kelas=request.POST.get('kelas'),
            nis=request.POST.get('nis'),
            status=request.POST.get('status')
        )
        return redirect('siswa_list')
    return render(request, 'siswa/form.html')

def siswa_detail(request, pk):
    siswa = get_object_or_404(Siswa, pk=pk)
    return render(request, 'siswa/detail.html', {'siswa': siswa})

def siswa_edit(request, pk):
    siswa = get_object_or_404(Siswa, pk=pk)
    if request.method == 'POST':
        siswa.nama = request.POST.get('nama')
        siswa.kelas = request.POST.get('kelas')
        siswa.nis = request.POST.get('nis')
        siswa.status = request.POST.get('status')
        siswa.save()
        return redirect('siswa_list')
    return render(request, 'siswa/form.html', {'siswa': siswa})

# 1. Halaman Konfirmasi Tampilan Hapus Siswa
def siswa_konfirmasi_hapus(request, pk):
    with connection.cursor() as cursor:
        # Ambil data nama siswa berdasarkan ID menggunakan RAW SQL
        cursor.execute("SELECT id, nama FROM perpustakaan_siswa WHERE id = %s", [pk])
        siswa = cursor.fetchone()
        
    context = {
        'siswa': {
            'id': siswa[0],
            'nama': siswa[1]
        } if siswa else None
    }
    return render(request, 'dashboard/hapus_siswa.html', context)


# 2. Eksekusi Hapus Siswa dari Database
def siswa_eksekusi_hapus(request, pk):
    if request.method == 'POST':
        with connection.cursor() as cursor:
            # Perintah DELETE data siswa menggunakan RAW SQL
            cursor.execute("DELETE FROM perpustakaan_siswa WHERE id = %s", [pk])
        return redirect('siswa_list') # Balikkan ke halaman daftar user/siswa
    return redirect('siswa_list')


# ==================== 3. MODUL BUKU ====================
def buku_list(request):
    data_buku = Buku.objects.all().order_by('-id')
    return render(request, 'buku/list.html', {'data_buku': data_buku})

def buku_tambah(request):
    if request.method == 'POST':
        Buku.objects.create(
            judul=request.POST.get('judul'),
            penerbit=request.POST.get('penerbit'),
            stok=request.POST.get('stok')
        )
        return redirect('buku') # Mengarah ke name='buku' di urls.py
    return render(request, 'buku/form.html')

def buku_detail(request, pk):
    buku = get_object_or_404(Buku, pk=pk)
    return render(request, 'buku/detail.html', {'buku': buku})

def buku_edit(request, pk):
    buku = get_object_or_404(Buku, pk=pk)
    if request.method == 'POST':
        buku.judul = request.POST.get('judul')
        buku.penerbit = request.POST.get('penerbit')
        buku.stok = request.POST.get('stok')
        buku.save()
        return redirect('buku')
    return render(request, 'buku/form.html', {'buku': buku})


# ==================== 4. MODUL PEMINJAMAN ====================
def peminjaman_list(request):
    # Mengambil semua data peminjaman beserta relasi siswa dan buku (select_related)
    data_peminjaman = Peminjaman.objects.all().select_related('siswa', 'buku').order_by('-id')
    return render(request, 'peminjaman/list.html', {'data_peminjaman': data_peminjaman})

def peminjaman_tambah(request):
    if request.method == 'POST':
        # Ambil ID yang dikirim dari elemen <select name="..."> di HTML
        siswa_id = request.POST.get('siswa_id')
        buku_id = request.POST.get('buku_id')
        
        # Ambil objek dari database berdasarkan ID
        siswa_obj = get_object_or_404(Siswa, id=siswa_id)
        buku_obj = get_object_or_404(Buku, id=buku_id)
        
        # Buat transaksi peminjaman baru (Sesuaikan field model abang)
        Peminjaman.objects.create(
            siswa=siswa_obj,
            buku=buku_obj,
            jatuh_tempo=request.POST.get('jatuh_tempo'),
            keperluan=request.POST.get('keperluan'),
            sudah_kembali=False
        )
        
        # Kurangi stok buku jika stoknya masih ada
        if buku_obj.stok > 0:
            buku_obj.stok -= 1
            buku_obj.save()
            
        return redirect('peminjaman')  # Pastikan nama rute ini sesuai di urls.py abang
        
    # PERBAIKAN: Ambil semua Siswa tanpa filter 'Aktif' dulu demi memastikan dropdown terisi data
    context = {
        'daftar_siswa': Siswa.objects.all(),
        'daftar_buku': Buku.objects.filter(stok__gt=0)  # Buku yang stoknya lebih dari 0
    }
    # CATATAN: Pastikan template form abang berada di folder 'templates/peminjaman/form.html'
    return render(request, 'peminjaman/form.html', context)


# ==================== 5. MODUL HAPUS BUKU (RAW SQL) ====================
# 1. Halaman Konfirmasi Tampilan Hapus Buku
def buku_konfirmasi_hapus(request, pk):
    with connection.cursor() as cursor:
        # Ambil data judul buku berdasarkan ID menggunakan RAW SQL
        cursor.execute("SELECT id, judul FROM perpustakaan_buku WHERE id = %s", [pk])
        buku = cursor.fetchone() # Mengambil satu baris data saja
        
    # Bungkus ke dalam dictionary agar bisa dibaca di template
    context = {
        'buku': {
            'id': buku[0],
            'judul': buku[1]
        } if buku else None
    }
    return render(request, 'dashboard/hapus_buku.html', context)


# 2. Eksekusi Hapus Buku (Dipanggil saat tombol merah di klik)
def buku_eksekusi_hapus(request, pk):
    if request.method == 'POST':
        with connection.cursor() as cursor:
            # Perintah DELETE data menggunakan RAW SQL sesuai modul tugas
            cursor.execute("DELETE FROM perpustakaan_buku WHERE id = %s", [pk])
        return redirect('buku') # Balikkan ke daftar list buku setelah berhasil
    return redirect('buku')