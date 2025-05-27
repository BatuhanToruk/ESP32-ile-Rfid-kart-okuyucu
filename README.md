# ESP32-ile-Rfid-kart-okuyucu
ESP32 aracılığı ile rfid 522 modülü ile kart okuyucu ve streamlit ve google apis ile veri görselleştirilmesi

Bu proje, ESP32 mikrodenetleyici, MFRC522 RFID okuyucu, Google Apps Script
ve Streamlit tabanlı Python uygulamasını bir araya getirerek, RFID teknolojisinin günlük ya-
samdaki pratik uygulamalarına yönelik kapsamlı ve düsük maliyetli bir çözüm sunmaktadır.
Geli¸stirilen sistem, bir kart okuyucudan çok daha fazlası olup, verinin toplanmasından islenmesine,
depolanmasından görsellestirilmesine kadar uçtan uca bir çözüm zinciri olusturmaktadır.
Projenin temelinde, ESP32’nin Wi-Fi yetenekleri sayesinde RFID kart okuma verilerinin
anlık olarak bulut tabanlı bir veri tabanına (Google Sheets) aktarılması yatmaktadır. Bu sayede,
geleneksel sistemlerdeki kablolama ve lokal depolama kısıtlamaları ortadan kalkmıs, veriye her
yerden eri¸silebilirlik saglanmı¸stır. Kartlara özellestirilmis bilgiler (örnegin kullanıcı isimleri)
yazılabilmesi, sistemin sadece kart UID’si degil, aynı zamanda karta gömülü ki¸siselle¸stirilmi¸s
verilerle de çalı¸sabilmesini saglamıstır.

Google Apps Script’in web uygulaması olarak kullanılması, herhangi bir sunucu maliyeti
olmaksızın ESP32’den gelen HTTP isteklerini güvenli ve etkili bir sekilde alıp Google Sheets’e
yazma yetenegi sunmustur. Bu entegrasyon, sistemin genel maliyetini düsürürken, veri yönetimi
için Google’ın güçlü altyapısından faydalanılmasını saglamıstır.
Son olarak, Streamlit ile gelistirilen interaktif panel, toplanan ham RFID verilerini anlamlı
ve eyleme dönüstürülebilir bilgilere dönü¸stürerek projenin en degerli çıktılarından birini olusturmaktadır.
Kullanıcı dostu bu arayüz sayesinde, katılım verileri üzerinde kolayca filtreleme,
analiz ve görsellestirme yapılabilmekte; günlük, saatlik veya kisiye özel giris egilimleri kolayca
gözlemlenebilmektedir. Otomatik ve manuel yenileme özellikleriyle verilerin her zaman güncel
kalması saglanmıs, Excel ve CSV dısa aktarım seçenekleriyle de verilerin daha ileri analizler
için kullanılabilmesinin önü açılmı¸stır.
Bu proje, Nesnelerin Interneti (IoT) prensiplerini somutla¸stıran, donanım, bulut bili¸sim ve
veri analizi yazılımlarını ba¸sarılı bir sekilde birlestiren bir örnektir. Akıllı ev sistemleri, küçük
ofisler, etkinlik katılım takibi veya envanter yönetimi gibi çesitli alanlarda pratik ve ölçeklenebilir
bir alternatif sunmaktadır. Gelistirilen bu sistem, esnekligi, düsük maliyeti ve kullanım
kolaylıgı ile benzer uygulamalara ilham kaynagı olabilecek niteliktedir.
