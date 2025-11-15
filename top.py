# --- Top (Ball) sınıfı: hareket, sekme, hız güncelleme ---

import random                 # Rastgele yön/hız için random kütüphanesi
from dataclasses import dataclass   # Dataclass yapısını kullanmak için
import math                   # Trigonometri işlemleri için math modülü

@dataclass                    # Ball sınıfını dataclass ile tanımlar (otomatik init vb.)
class Ball:
    canvas: object            # Topun çizileceği canvas nesnesi
    x: float                  # Topun merkezinin x koordinatı
    y: float                  # Topun merkezinin y koordinatı
    r: int                    # Topun yarıçapı
    color: str                # Topun rengi
    vx: float                 # X eksenindeki hız bileşeni
    vy: float                 # Y eksenindeki hız bileşeni

    def __post_init__(self):                                      # Dataclass init sonrası çalışan fonksiyon
        # Canvas üzerinde görsel oval (top) oluştur (çizim işlemi)
        self.item = self.canvas.create_oval(
            self.x - self.r, self.y - self.r,                     # Sol üst noktası
            self.x + self.r, self.y + self.r,                     # Sağ alt noktası
            fill=self.color,                                      # Top rengi
            outline="white",                                      # Çevresinde beyaz ince çerçeve
            width=1                                               # Çerçeve kalınlığı
        )

    @staticmethod
    def random_unit_velocity(speed: float):                       # Random hız yönü üretme fonksiyonu
        angle = random.random() * 2 * math.pi                     # Rastgele bir açı (0–360 derece)
        return speed * math.cos(angle), speed * math.sin(angle)   # X ve Y ekseninde hız bileşenleri

    def move_one_step(self, bounds):
        """Topu bir adım hareket ettir ve kenarlardan sektir. bounds=(xmin,ymin,xmax,ymax)"""
        xmin, ymin, xmax, ymax = bounds   # Sınırların ayrıştırılması
        self.x += self.vx                 # X konumunu hız kadar arttır
        self.y += self.vy                 # Y konumunu hız kadar arttır

        # Sol kenara çarpma (x - r <= xmin)
        if self.x - self.r <= xmin:
            self.x = xmin + self.r        # Ekranın dışına taşmasın diye geri ayarla
            self.vx = abs(self.vx)        # Hızı sağa doğru çevir (pozitif yap)

        # Sağ kenara çarpma (x + r >= xmax)
        elif self.x + self.r >= xmax:
            self.x = xmax - self.r        # Ekranın dışına taşmasın diye geri al
            self.vx = -abs(self.vx)       # Hızı sola doğru çevir (negatif yap)

        # Üst kenara çarpma
        if self.y - self.r <= ymin:
            self.y = ymin + self.r        # Konumu düzelt
            self.vy = abs(self.vy)        # Hızı aşağı yönlü yap

        # Alt kenara çarpma
        elif self.y + self.r >= ymax:
            self.y = ymax - self.r        # Konumu düzelt
            self.vy = -abs(self.vy)       # Hızı yukarı yönlü yap

        # Canvas üzerindeki topun yeni konumunu güncelle (yeniden çiz)
        self.canvas.coords(
            self.item,
            self.x - self.r, self.y - self.r,   # Yeni sol üst
            self.x + self.r, self.y + self.r    # Yeni sağ alt
        )

    def multiply_speed(self, factor: float):
        self.vx *= factor               # X hızını çarpan kadar arttır veya azalt
        self.vy *= factor               # Y hızını çarpan kadar arttır veya azalt
