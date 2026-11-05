"""
SE Primer: Yazılım Mühendisliği & Testi - Oynanan Bir Kitap (AI Tutor)
Ders: YZM301 Yazılım Testi / Doğrulama ve Geçerleme
Öğretim Üyesi: Prof. Dr. Nurettin Şenyer
Öğrenci: Ece Yoloğlu (241478071) - Samsun Üniversitesi Yazılım Mühendisliği

"Her seçim bir durum geçişi. Her son bir kabul kriteri."
"""

import sys
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass

@dataclass
class AcceptanceCriterion:
    id: str
    title: str
    given: str
    when: str
    then: str
    is_satisfied: bool = False

    def evaluate(self, state: str, context: dict) -> bool:
        if self.id == "AC-01": # Eşzamanlı Randevu Rezervasyonu
            self.is_satisfied = (state == "SUCCESS" and context.get("concurrency_strategy") == "redis_lock" 
                                 and context.get("active_connections", 0) <= 1000)
        elif self.id == "AC-02": # 08:00 Yük ve Stres Dayanıklılığı
            self.is_satisfied = (state == "SUCCESS" and context.get("load_tested") is True 
                                 and context.get("p99_latency_ms", 9999) < 250)
        elif self.id == "AC-03": # Güvenlik & SQL Enjeksiyon Koruması
            self.is_satisfied = (state != "BREACH" and context.get("input_sanitized") is True 
                                 and context.get("rate_limiter") is True)
        elif self.id == "AC-04": # AI Model Semptom-Poliklinik Yönlendirme
            self.is_satisfied = (context.get("model_f1", 0.0) >= 0.90 
                                 and context.get("false_negatives", 100) <= 5)
        return self.is_satisfied


class BERTSymptomClassifier:
    """
    Slayt 3'teki BERT (Transformer [CLS] + Token Embeddings) mimarisini
    hastane semptom-poliklinik triyajı için simüle eden NLP sınıflandırıcısı.
    """
    KEYWORDS = {
        "Kardiyoloji": ["göğüs", "kalp", "çarpıntı", "sol kol", "sıkışma", "nefes darlığı", "tansiyon"],
        "Nöroloji": ["baş ağrısı", "baş dönmesi", "uyuşma", "karıncalanma", "bayılma", "unutkanlık", "felç"],
        "Ortopedi": ["eklem", "diz", "kırık", "çıkık", "bel ağrısı", "kemik", "burkulma", "menisküs"],
        "Göz Hastalıkları": ["göz", "bulanık", "kızarıklık", "görme", "ışık", "batma", "çift görme"],
        "Dahiliye": ["mide", "karın", "halsizlik", "ateş", "iştahsızlık", "bulantı", "kilo kaybı"]
    }

    def predict(self, complaint: str) -> Dict[str, float]:
        complaint_lower = complaint.lower()
        scores = {dept: 0.1 for dept in self.KEYWORDS}
        
        for dept, words in self.KEYWORDS.items():
            for word in words:
                if word in complaint_lower:
                    scores[dept] += 1.0
        
        total = sum(scores.values())
        probabilities = {dept: round(score / total, 4) for dept, score in scores.items()}
        sorted_probs = dict(sorted(probabilities.items(), key=lambda item: item[1], reverse=True))
        return sorted_probs


class ConfusionMatrix:
    """
    Slayt 6'daki Hata Matrisi (Confusion Matrix) hesaplamaları:
    TP, FP, FN, TN -> Accuracy, Precision, Recall, F1-Score
    """
    def __init__(self, tp: int, fp: int, fn: int, tn: int):
        self.tp = tp
        self.fp = fp
        self.fn = fn
        self.tn = tn

    @property
    def accuracy(self) -> float:
        total = self.tp + self.fp + self.fn + self.tn
        return round((self.tp + self.tn) / total, 4) if total > 0 else 0.0

    @property
    def precision(self) -> float:
        denom = self.tp + self.fp
        return round(self.tp / denom, 4) if denom > 0 else 0.0

    @property
    def recall(self) -> float:
        denom = self.tp + self.fn
        return round(self.tp / denom, 4) if denom > 0 else 0.0

    @property
    def f1_score(self) -> float:
        p, r = self.precision, self.recall
        return round(2 * (p * r) / (p + r), 4) if (p + r) > 0 else 0.0

    def summary(self) -> Dict[str, float]:
        return {
            "TP": self.tp,
            "FP": self.fp,
            "FN": self.fn,
            "TN": self.tn,
            "Accuracy": self.accuracy,
            "Precision": self.precision,
            "Recall": self.recall,
            "F1-Score": self.f1_score
        }


class SEPrimerGame:
    """
    Finite State Machine (FSM) tabanlı SE Primer Oynanabilir Hikâye Motoru.
    Durumlar:
      S0: INITIAL (Giriş / 07:30 Şehir Hastanesi)
      S1: ARCHITECTURE_CHOICE (Mimari ve Kilit Mekanizması)
      S2: TEST_STRATEGY (Doğrulama ve Yük Testi)
      S3: SECURITY_SHIELD (Yetkilendirme ve Girdi Doğrulama)
      S4: MODEL_INTEGRATION (AI Tutor / BERT Poliklinik Triyajı)
      S5: TERMINAL_SUCCESS ("Randevu Başarılı" - Kabul Kriterleri Sağlandı)
      S6: TERMINAL_CRASH ("08:00 - Sistem Çöktü" - Concurrency / Race Condition)
      S7: TERMINAL_BREACH ("Veri İhlali / Bot Saldırısı")
      S8: TERMINAL_MISDIAGNOSIS ("Kritik Tıbbi Yönlendirme Hatası")
    """

    def __init__(self):
        self.current_state = "S0_INITIAL"
        self.context = {
            "concurrency_strategy": None,
            "active_connections": 0,
            "load_tested": False,
            "p99_latency_ms": 1200,
            "input_sanitized": False,
            "rate_limiter": False,
            "model_integrated": False,
            "model_f1": 0.0,
            "false_negatives": 50,
            "log": []
        }
        self.bert = BERTSymptomClassifier()
        self.acceptance_criteria = [
            AcceptanceCriterion("AC-01", "Eşzamanlı Randevu Bütünlüğü", 
                                "Aynı hekim slotuna aynı milisaniyede 10 istek geldiğinde", 
                                "Kilit mekanizması çalıştığında", 
                                "Yalnızca 1 hasta randevu alır, 9 hasta 'Dolu' yanıtı alır; çift rezervasyon oluşmaz."),
            AcceptanceCriterion("AC-02", "08:00 Pik Yük Karşılama", 
                                "08:00:00'da 50.000 eşzamanlı aktif kullanıcı bağlandığında", 
                                "Sistem sorgulandığında", 
                                "P99 gecikme 250ms altında kalır, 504 Gateway Timeout oranı %0 olur."),
            AcceptanceCriterion("AC-03", "Veri Güvenliği ve Kötüye Kullanım", 
                                "Yetkisiz bot istekleri ve SQL injection payloadları gönderildiğinde", 
                                "Güvenlik katmanı karşıladığında", 
                                "İstekler 429 Too Many Requests ve 400 Bad Request ile bloklanır, veri sızmaz."),
            AcceptanceCriterion("AC-04", "AI Poliklinik Triyaj Doğruluğu", 
                                "Hasta semptom metnini serbestçe girdiğinde", 
                                "BERT tabanlı triyaj modeli çalıştığında", 
                                "F1-Skoru >= 0.90 olur, kritik vaka yanlış negatif (FN) sayısı <= 5 kalır.")
        ]

    def log(self, text: str):
        self.context["log"].append(text)

    def transition_arch(self, choice: int) -> str:
        """S0 -> S1"""
        if choice == 1:
            # Doğru seçim: Redis Dağıtık Kilit (Redlock) + DB Connection Pool
            self.context["concurrency_strategy"] = "redis_lock"
            self.context["active_connections"] = 450
            self.log("Seçim 1: Redis Dağıtık Kilit ve Connection Pool seçildi. Durum geçişi: S0 -> S1_SECURE_ARCH")
            self.current_state = "S1_TEST_STRATEGY"
            return "Başarılı: Dağıtık kilit mimarisi veri tabanını aşırı yükten koruyor."
        else:
            # Hatalı seçim: Düz SQL SELECT ... ardından UPDATE (Race condition garantisi)
            self.context["concurrency_strategy"] = "naive_sql"
            self.context["active_connections"] = 12000
            self.log("Seçim 2: Naive SQL seçildi! Durum geçişi: S0 -> S1_RISKY_ARCH")
            self.current_state = "S1_TEST_STRATEGY"
            return "Riskli: İki istek aynı anda boş slotu görüp ikisi de rezervasyon yapabilir (Race Condition)!"

    def transition_test(self, choice: int) -> str:
        """S1 -> S2"""
        if choice == 1:
            # Kapsamlı Test: JMeter Yük Testi + Sınır Değer Analizi + Eşzamanlılık Testi
            self.context["load_tested"] = True
            self.context["p99_latency_ms"] = 180
            self.log("Seçim 1: JMeter / Locust yük testi ve sınır değer testleri koşuldu.")
            self.current_state = "S2_SECURITY"
            return "Başarılı: Yük testi darboğazları önceden ortaya çıkardı ve optimize edildi."
        else:
            # Hatalı seçim: Yalnızca geliştirici makinesinde tek kullanıcılı Happy-Path birim testi
            self.context["load_tested"] = False
            self.context["p99_latency_ms"] = 3500
            self.log("Seçim 2: Yalnızca Happy-Path testi yapıldı. Eşzamanlılık test edilmedi!")
            self.current_state = "S2_SECURITY"
            return "Uyarı: Canlıdaki 50.000 eşzamanlı istek hiç test edilmedi!"

    def transition_security(self, choice: int) -> str:
        """S2 -> S3"""
        if choice == 1:
            # Kalkan devrede: Rate Limiter (Token Bucket) + Girdi Sanitizasyonu + T.C. Kimlik Algoritması
            self.context["input_sanitized"] = True
            self.context["rate_limiter"] = True
            self.log("Seçim 1: Güvenlik Kalkanı devrede: Rate limiting ve input sanitization aktif.")
            self.current_state = "S3_AI_MODEL"
            return "Başarılı: Botlar ve zararlı scriptler engellendi."
        else:
            # Kalkan kapalı: "Zaman dar, lansmandan sonra ekleriz"
            self.context["input_sanitized"] = False
            self.context["rate_limiter"] = False
            self.log("Seçim 2: Güvenlik önlemleri ertelendi.")
            self.current_state = "S3_AI_MODEL"
            return "Tehlike: API dış saldırılara ve DDoS türevli bot spamına karşı tamamen açık!"

    def transition_model(self, choice: int) -> str:
        """S3 -> S4 & Değerlendirme"""
        if choice == 1:
            # Optimize Edilmiş BERT Modeli + Doğrulama Kümesi (Validation) + Confusion Matrix Analizi
            self.context["model_integrated"] = True
            # Simüle edilen metrikler (Slayt 6 Confusion Matrix)
            # TP=930, FP=35, FN=5, TN=1030 -> Recall=99.46%, Precision=96.37%, F1=97.89%
            matrix = ConfusionMatrix(tp=930, fp=35, fn=5, tn=1030)
            self.context["model_f1"] = matrix.f1_score
            self.context["false_negatives"] = matrix.fn
            self.log(f"Seçim 1: BERT Modeli entegre edildi. Test Seti F1={matrix.f1_score}, Recall={matrix.recall}")
            self.current_state = "S4_EVALUATION"
            return f"Model Başarılı! Doğruluk: %{matrix.accuracy*100}, F1: %{matrix.f1_score*100}"
        else:
            # Test edilmemiş, ezberlemiş (overfitted) basit kural tabanlı model
            self.context["model_integrated"] = False
            matrix = ConfusionMatrix(tp=410, fp=250, fn=180, tn=600)
            self.context["model_f1"] = matrix.f1_score
            self.context["false_negatives"] = matrix.fn
            self.log(f"Seçim 2: Kötü eğitilmiş model! F1={matrix.f1_score}, FN={matrix.fn}")
            self.current_state = "S4_EVALUATION"
            return f"Uyarı: Model yüksek oranda yanlış negatif üretiyor (FN={matrix.fn})."

    def evaluate_clock_0800(self) -> Tuple[str, str]:
        """
        08:00 SAATİ GELDİ! Canlıya geçiş ve kabul kriterleri değerlendirmesi.
        """
        # Hata koşullarını öncelik sırasıyla kontrol et:
        if self.context["concurrency_strategy"] != "redis_lock" or not self.context["load_tested"]:
            self.current_state = "S6_TERMINAL_CRASH"
            msg = ("08:00 - SİSTEM ÇÖKTÜ!\n"
                   "Kök Neden: Dağıtık kilit mekanizması ve yük testi eksikliği nedeniyle 08:00'de "
                   "aynı randevu slotlarına yüzlerce eşzamanlı işlem yazılmaya çalışıldı (Race Condition). "
                   "Veritabanı Connection Pool tükendi, Deadlock oluştu ve sunucular 504 Gateway Timeout verdi.")
            status = "CRASH"
        elif not self.context["rate_limiter"] or not self.context["input_sanitized"]:
            self.current_state = "S7_TERMINAL_BREACH"
            msg = ("08:00 - VERİ İHLALİ VE BOT ÇÖKÜŞÜ!\n"
                   "Kök Neden: Rate limiter olmadığı için karaborsacı botlar saniyede 15.000 istek ile "
                   "tüm randevuları rezerve etti ve sistem meşru hastalara hizmet veremedi.")
            status = "BREACH"
        elif self.context["false_negatives"] > 10:
            self.current_state = "S8_TERMINAL_MISDIAGNOSIS"
            msg = ("08:00 - KRİTİK YÖNLENDİRME HATASI!\n"
                   "Kök Neden: Yetersiz test edilen AI triyaj modeli, kalp krizi semptomlarını "
                   "Dahiliye/Mide polikliniğine yönlendirdi (Yüksek Yanlış Negatif).")
            status = "MISDIAGNOSIS"
        else:
            self.current_state = "S5_TERMINAL_SUCCESS"
            msg = ("08:00 - RANDEVU BAŞARILI!\n"
                   "Tebrikler! Dağıtık kilit mimarisi eşzamanlılığı korudu, JMeter yük testi ile p99 gecikme 180ms "
                   "seviyesinde tutuldu, güvenlik kalkanı botları eledi ve BERT modeli hastaları doğru polikliniklere "
                   "yönlendirdi. Tüm kabul kriterleri (AC-01..AC-04) %100 doğrulandı.")
            status = "SUCCESS"

        # Tüm kriterleri değerlendir
        for ac in self.acceptance_criteria:
            ac.evaluate(status, self.context)

        return self.current_state, msg


def run_interactive_cli():
    print("=" * 70)
    print("SE PRIMER: YAZILIM MÜHENDİSLİĞİ, OYNANAN BİR KİTAP")
    print("Samsun Üniversitesi - YZM301 Yazılım Testi")
    print("'Her seçim bir durum geçişi. Her son bir kabul kriteri.'")
    print("=" * 70)
    
    game = SEPrimerGame()
    
    print("\n[BÖLÜM 1: 07:30 - MİMARİ KARARI]")
    print("Şehir Hastanesi Randevu Sistemi 30 dakika sonra (08:00) açılacak.")
    print("50.000 vatandaş aynı anda randevu almak için sisteme akın edecek.")
    print("1) Redis Dağıtık Kilit (Redlock) ve DB Connection Pool mimarisi kur.")
    print("2) Doğrudan veritabanına SQL SELECT ve ardından UPDATE yaz (Hızlı geliştirme).")
    c1 = int(input("Seçiminiz (1 veya 2): ") or "1")
    print(game.transition_arch(c1))

    print("\n[BÖLÜM 2: 07:40 - TEST VE DOĞRULAMA STRATEJİSİ]")
    print("Lansman öncesi doğrulama adımı:")
    print("1) JMeter/Locust ile 50.000 eşzamanlı kullanıcı yük ve sınır değer testleri yap.")
    print("2) Geliştirici bilgisayarında 1 kullanıcıyla 'Happy Path' birim testi yapıp geç.")
    c2 = int(input("Seçiminiz (1 veya 2): ") or "1")
    print(game.transition_test(c2))

    print("\n[BÖLÜM 3: 07:50 - GÜVENLİK KALKANI]")
    print("1) Token Bucket Rate Limiter + SQL Enjeksiyon koruması + T.C. Kimlik doğrulaması.")
    print("2) Güvenlik kontrollerini atla, lansman sonrası bakarız.")
    c3 = int(input("Seçiminiz (1 veya 2): ") or "1")
    print(game.transition_security(c3))

    print("\n[BÖLÜM 4: 07:55 - AI TUTOR / BERT MODEL ENTEGRASYONU]")
    print("Hastaların şikayetlerini analiz edip poliklinik seçen model:")
    print("1) BERT Transformer modeli + Doğrulama seti ve Confusion Matrix analizi.")
    print("2) Test edilmemiş basit kelime eşleştirme kuralı.")
    c4 = int(input("Seçiminiz (1 veya 2): ") or "1")
    print(game.transition_model(c4))

    print("\n" + "=" * 70)
    print("SAAT 08:00:00 OLDU! SİSTEM CANLI TRAFİĞİ KARŞILIYOR...")
    print("=" * 70)
    final_state, message = game.evaluate_clock_0800()
    print(f"\nSONUÇ DURUMU: {final_state}")
    print(message)

    print("\n" + "-" * 70)
    print("KABUL KRİTERLERİ (ACCEPTANCE CRITERIA) DOĞRULAMA RAPORU:")
    print("-" * 70)
    for ac in game.acceptance_criteria:
        durum = "[GEÇTİ - PASSED]" if ac.is_satisfied else "[KALDI - FAILED]"
        print(f"{ac.id}: {ac.title} -> {durum}")
        print(f"   Given: {ac.given}")
        print(f"   When:  {ac.when}")
        print(f"   Then:  {ac.then}\n")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--play":
        run_interactive_cli()
    else:
        # Otomatik test modu
        g = SEPrimerGame()
        g.transition_arch(1)
        g.transition_test(1)
        g.transition_security(1)
        g.transition_model(1)
        state, msg = g.evaluate_clock_0800()
        print(f"Otomatik Doğrulama Tamamlandı: Durum={state}")
        all_passed = all(ac.is_satisfied for ac in g.acceptance_criteria)
        print(f"Tüm Kabul Kriterleri Doğrulandı: {all_passed}")
