from django.db import models

# 1. Model Data Siswa / User
class Siswa(models.Model):
    nama = models.CharField(max_length=100)
    kelas = models.CharField(max_length=50)
    nis = models.CharField(max_length=20, unique=True)
    status = models.CharField(max_length=20, default='Aktif') 

    def __str__(self):
        return f"{self.nama} ({self.kelas})"

# 2. Model Data Koleksi Buku
class Buku(models.Model):
    judul = models.CharField(max_length=200)
    penerbit = models.CharField(max_length=100)
    stok = models.IntegerField(default=1)

    def __str__(self):
        return self.judul

# 3. Model Transaksi Peminjaman
class Peminjaman(models.Model):
    # Di sini sudah diperbaiki ya bang, parameter typo-nya sudah dibuang!
    siswa = models.ForeignKey(Siswa, on_delete=models.CASCADE)
    buku = models.ForeignKey(Buku, on_delete=models.CASCADE)
    tanggal_pinjam = models.DateField(auto_now_add=True)
    jatuh_tempo = models.DateField(null=True, blank=True)
    keperluan = models.TextField(null=True, blank=True)
    sudah_kembali = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.siswa.nama} pinjam {self.buku.judul}"
