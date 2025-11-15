import tkinter as tk              # Tkinter kütüphanesini GUI oluşturmak için içe aktarır
from PIL import Image, ImageTk    # PIL ile resimleri yüklemek ve tkinter’da göstermek için
import random                      # Rastgele sayı üretmek için random modülü
from top import Ball               # Top sınıfını diğer dosyadan içe aktarır
from utils import BOYUTLAR, RENKLER, BASE_SPEED, SPEED_UP_FACTOR, TICK_MS   # Yardımcı sabitleri alır
import winsound                    # Windows üzerinde ses oynatmak için winsound
from tkinter import messagebox     # Uyarı mesajları göstermek için messagebox

class KonsolUI:                    # Oyun konsolu arayüz sınıfı

    def __init__(self, root):      # Sınıfın kurucu fonksiyonu
        self.root = root           # Ana pencere referansı
        self.root.title("Oyun Konsolu 🎮 - 🔵 🔴 🟡 ")   # Pencere başlığı

        self.root.geometry("1000x600")     # Pencere boyutu
        self.root.resizable(True, True)    # Pencerenin yeniden boyutlanmasına izin verir

        icon = tk.PhotoImage(file="konsol.gif")   # Pencere ikonu olarak gif yükler
        self.root.iconphoto(False, icon)          # İkonu uygular

        # ================================
        # ARKA PLAN (KONSOL RESMİ)
        # ================================
        img = Image.open("oyunkonsolu.jpg").resize((1000, 600))  # Arka plan resmi açılır ve boyutlanır
        self.bg_img = ImageTk.PhotoImage(img)                    # Tkinter için uygun hale getirilir

        bg = tk.Label(root, image=self.bg_img)      # Arka plan resmi label olarak eklenir
        bg.place(x=0, y=0)                          # Her yere yayılacak şekilde konumlandırılır

        # ================================
        # TOPLARIN HAREKET ALANI (EKRAN)
        # ================================
        self.screen_x = 190      # Oyun ekranının x konumu
        self.screen_y = 200      # Oyun ekranının y konumu
        self.screen_w = 610      # Ekranın genişliği
        self.screen_h = 200      # Ekranın yüksekliği

        self.play = tk.Canvas(       # Topların hareket edeceği canvas
            root,
            bg="black",              # Arkaplan siyah (oyun ekranı)
            highlightthickness=0     # Kenarlık kapalı
        )
        self.play.place(             # Canvası belirtilen koordinatlara yerleştirir
            x=self.screen_x,
            y=self.screen_y,
            width=self.screen_w,
            height=self.screen_h
        )

        self.root.bind("<F11>", self.toggle_fullscreen)   # F11 ile tam ekran aç/kapat
        self.root.bind("<Escape>", self.exit_fullscreen)   # Escape ile tam ekrandan çık
        self.fullscreen = False                             # Başlangıçta tam ekran değil

        for _ in range(80):         # Ekrana 80 tane beyaz yıldız (arka plan efekti) yerleştirir
            x = random.randint(0, self.screen_w)
            y = random.randint(0, self.screen_h)
            size = random.randint(1, 3)
            self.play.create_oval(x, y, x + size, y + size, fill="white", outline="")

        # ================================
        # SAĞ TARAFTAKİ TUŞLAR
        # (Start, Speed, Stop, Reset)
        # ================================
        def yuvarlak_buton(x, y, text, command):   # Ortak buton oluşturucu fonksiyon
            btn = tk.Button(
                root,
                text=text,           # Butonun üzerinde yazacak karakter
                command=command,     # Buton basılınca çağrılacak fonksiyon
                bg="#666666",        # Gri arka plan
                fg="white",          # Beyaz yazı
                borderwidth=3,       # Kenarlık kalınlığı
                relief="raised",     # Kabartmalı görünüm
                font=("Arial", 16, "bold"),
                width=4,             # Boyut
                height=2
            )
            btn.place(x=x - 25, y=y - 25, width=50, height=50)  # Tam yuvarlak görünüm yaratır

        # Sağ tuş grubunun yerleşimi
        yuvarlak_buton(x=850, y=245, text="▶", command=self.start)      # Start
        yuvarlak_buton(x=900, y=245, text="⚡", command=self.speed_up)   # Speed Up
        yuvarlak_buton(x=850, y=295, text="⏹", command=self.stop)       # Stop
        yuvarlak_buton(x=900, y=295, text="↻", command=self.reset)      # Reset

        # ================================
        # SOL TARAFTAKİ RENK & BOYUT TUŞLARI
        # ================================
        def renk_buton(x, y, color_key):          # Renk butonu oluşturucu
            btn = tk.Button(
                root,
                bg=RENKLER[color_key],            # Renk
                command=lambda k=color_key: self._select_color(k),
                borderwidth=2,
                relief="groove"
            )
            btn.place(x=x - 20, y=y - 20, width=40, height=40)   # Kare buton konumu

        def boyut_buton(x, y, size_key):      # Boyut butonu (içinde daire olan canvas)
            radius = BOYUTLAR[size_key]       # Boyutun yarıçapı
            diameter = radius * 2             # Çap

            btn = tk.Canvas(
                root,
                width=diameter,
                height=diameter,
                bg="#f0f0f0",
                highlightthickness=0
            )

            circle = btn.create_oval(          # Daire çizimi
                2, 2, diameter - 2, diameter - 2,
                fill="white",
                outline="black",
                width=2
            )

            btn.create_text(                  # Dairenin ortasına harf yazar (K, O, B)
                diameter / 2,
                diameter / 2,
                text=size_key[0].upper(),
                font=("Arial", int(radius / 1.5), "bold")
            )

            def on_click(event=None):         # Tıklama animasyonu
                btn.itemconfig(circle, fill="#cccccc")   # Daireyi gri yap
                self._select_size(size_key)              # Boyutu seç
                btn.after(120, lambda: btn.itemconfig(circle, fill="white"))  # Eski haline dön

            btn.bind("<Button-1>", on_click)   # Tıklama olayı bağlanır

            btn.place(x=x - radius, y=y - radius)   # Ekrana yerleştirme

        # Boyut düğmeleri
        boyut_buton(145, 250, "kucuk")
        boyut_buton(145, 295, "orta")
        boyut_buton(145, 360, "buyuk")

        # Renk düğmeleri
        renk_buton(90, 260, "kirmizi")
        renk_buton(90, 310, "mavi")
        renk_buton(90, 360, "sari")

        # ================================
        # ANİMASYON DEĞİŞKENLERİ
        # ================================
        self.secili_renk = None    # Kullanıcının seçtiği renk
        self.secili_boyut = None   # Kullanıcının seçtiği boyut
        self.balls = []            # Eklenen top listesi
        self.running = False       # Animasyon çalışıyor mu?

        self._tick()               # Animasyonu başlatır (sonsuz döngü)

    def toggle_fullscreen(self, event=None):
        self.fullscreen = not self.fullscreen            # Tersine çevir
        self.root.attributes("-fullscreen", self.fullscreen)

    def exit_fullscreen(self, event=None):
        self.fullscreen = False
        self.root.attributes("-fullscreen", False)

    def play_click(self):
        winsound.PlaySound("tiklamasesi.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)

    # ================================
    # RENK & BOYUT SEÇİMİ
    # ================================
    def _select_color(self, color_key):
        self.play_click()          # Ses oynat
        self.secili_renk = color_key  # Rengi kaydet
        self._add_ball()              # Eğer boyut da seçildiyse top ekle

    def _select_size(self, size_key):
        self.play_click()          # Ses
        self.secili_boyut = size_key  # Boyutu kaydet
        self._add_ball()              # Eğer renk de seçiliyse top ekle

    def _add_ball(self):
        if self.secili_renk is None or self.secili_boyut is None:
            return                  # Renk + Boyut ikisi de seçilmeden top eklenmez

        r = BOYUTLAR[self.secili_boyut]      # Çap/yarıçap belirlenir
        xmin, ymin = 0, 0                    # Sınırlar
        xmax, ymax = self.screen_w, self.screen_h

        x = random.uniform(r, xmax - r)      # Rastgele bir x konumu
        y = random.uniform(r, ymax - r)      # Rastgele bir y konumu

        vx, vy = Ball.random_unit_velocity(BASE_SPEED)  # Rastgele hız yönü
        b = Ball(self.play, x, y, r, RENKLER[self.secili_renk], vx, vy)   # Top oluştur

        self.balls.append(b)        # Listeye ekle
        self.secili_renk = None     # Seçimleri sıfırla
        self.secili_boyut = None

    # ================================
    # TUŞLAR (START, STOP, RESET, SPEED UP)
    # ================================
    def start(self):
        self.play_click()
        if len(self.balls) == 0:             # Hiç top yoksa çalışmaz
            messagebox.showwarning("Uyarı", "Lütfen önce top ekleyiniz!")
            return
        self.running = True                  # Animasyon başlasın

    def stop(self):
        self.play_click()

        if len(self.balls) == 0:             # Stop basıldı ama top yok
            messagebox.showwarning("Uyarı",
                                   "Lütfen önce top ekleyiniz ve start ile hareketi başlatınız!")
            return

        if not self.running:                # Stop basıldı ama animasyon çalışmıyor
            messagebox.showwarning("Uyarı",
                                   "Start ile hareketi başlatınız veya reset ile sıfırlayınız!!")
            return

        self.running = False                # Normal stop

    def reset(self):
        if self.running == False and len(self.balls) == 0:   # Zaten boşsa
            messagebox.showinfo("Uyarı", "Ekranda sıfırlanacak top yok!")
            return

        self.running = False                 # Animasyonu durdur
        for b in self.balls:                 # Tüm topları sil
            self.play.delete(b.item)
        self.balls.clear()                   # Listeyi temizle

    def speed_up(self):
        winsound.PlaySound("hizsesi.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)

        if not self.running:     # Toplar duruyorsa hızlanamaz
            messagebox.showwarning("Uyarı", "Lütfen önce START butonuna basınız!")
            return

        for b in self.balls:     # Tüm topların hızını arttır
            b.multiply_speed(SPEED_UP_FACTOR)

    # ================================
    # ANİMASYON TİCK FONKSİYONU
    # ================================
    def _tick(self):
        if self.running:                                  # Eğer animasyon aktifse
            for b in self.balls:
                b.move_one_step((0, 0, self.screen_w, self.screen_h))  # Her topu bir adım hareket ettir

        self.root.after(TICK_MS, self._tick)              # Kendini tekrar çağırır (sonsuz loop)

# ================================
# PROGRAM ÇALIŞTIRMA BLOĞU
# ================================
if __name__ == "__main__":
    root = tk.Tk()                # Tk pencere oluştur
    app = KonsolUI(root)          # Konsol arayüzünü başlat
    root.mainloop()               # Tkinter döngüsünü çalıştır
