from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    
    path('siswa/', views.siswa_list, name='siswa_list'),
    path('siswa/tambah/', views.siswa_tambah, name='siswa_tambah'),
    path('siswa/detail/<int:pk>/', views.siswa_detail, name='siswa_detail'),
    path('siswa/edit/<int:pk>/', views.siswa_edit, name='siswa_edit'),
    path('siswa/hapus/<int:pk>/', views.siswa_konfirmasi_hapus, name='siswa_konfirmasi_hapus'),
    path('siswa/hapus/<int:pk>/eksekusi/', views.siswa_eksekusi_hapus, name='siswa_eksekusi_hapus'),
    
    path('buku/', views.buku_list, name='buku'),
    path('buku/tambah/', views.buku_tambah, name='buku_tambah'),
    path('buku/detail/<int:pk>/', views.buku_detail, name='buku_detail'),
    path('buku/edit/<int:pk>/', views.buku_edit, name='buku_edit'),
    path('buku/hapus/<int:pk>/', views.buku_konfirmasi_hapus, name='buku_konfirmasi_hapus'),
    path('buku/hapus/<int:pk>/eksekusi/', views.buku_eksekusi_hapus, name='buku_eksekusi_hapus'),
    
    path('peminjaman/', views.peminjaman_list, name='peminjaman'),
    path('peminjaman/tambah/', views.peminjaman_tambah, name='peminjaman_tambah'),
]