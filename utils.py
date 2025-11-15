# utils.py
# --- Sabitler ve yardımcı araçlar dosyası ---

# Çizim alanının yenileme hızı (milisaniye cinsinden)
# 16 ms ≈ 60 FPS, yani saniyede 60 karelik akıcı animasyon sağlar
TICK_MS = 16

# Topların başlangıç hızı (her tick’te kaç piksel hareket edeceği)
BASE_SPEED = 3.0

# Speed Up butonuna basıldığında hızın çarpılacağı katsayı
# Her tıklamada top biraz daha hızlanır
SPEED_UP_FACTOR = 1.18

# Top renkleri sözlüğü (ekranda kullanılacak üç renk)
# Anahtarlar, program içinde kullanılacak adlardır
RENKLER = {
    "kirmizi": "#E1261C",   # Parlak kırmızı
    "mavi":    "#0B51FF",   # Canlı mavi
    "sari":    "#F0E000",   # Parlak sarı
}

# Top boyutları (yarıçap cinsinden)
# Küçük – Orta – Büyük olarak üç farklı boy
BOYUTLAR = {
    "kucuk": 14,   # Küçük top yarıçapı: 14 px
    "orta":  24,   # Orta top yarıçapı: 24 px
    "buyuk": 33,   # Büyük top yarıçapı: 33 px
}
