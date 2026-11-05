import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from se_primer_tutor import SEPrimerGame, ConfusionMatrix, BERTSymptomClassifier

class TestSEPrimer(unittest.TestCase):
    def setUp(self):
        self.game = SEPrimerGame()

    def test_happy_path_success(self):
        """Tüm doğru kararlar verildiğinde S5_TERMINAL_SUCCESS ve tüm AC'lerin geçmesi"""
        self.game.transition_arch(1)
        self.game.transition_test(1)
        self.game.transition_security(1)
        self.game.transition_model(1)
        state, msg = self.game.evaluate_clock_0800()
        
        self.assertEqual(state, "S5_TERMINAL_SUCCESS")
        self.assertIn("RANDEVU BAŞARILI", msg)
        for ac in self.game.acceptance_criteria:
            self.assertTrue(ac.is_satisfied, f"Kriter sağlanamadı: {ac.id}")

    def test_race_condition_leads_to_crash(self):
        """Naive SQL ve eksik yük testi 08:00'de sistem çökmesine (CRASH) yol açmalıdır"""
        self.game.transition_arch(2) # Naive SQL
        self.game.transition_test(2) # Yük testi yok
        self.game.transition_security(1)
        self.game.transition_model(1)
        state, msg = self.game.evaluate_clock_0800()
        
        self.assertEqual(state, "S6_TERMINAL_CRASH")
        self.assertIn("08:00 - SİSTEM ÇÖKTÜ", msg)
        ac1 = next(ac for ac in self.game.acceptance_criteria if ac.id == "AC-01")
        self.assertFalse(ac1.is_satisfied)

    def test_missing_security_leads_to_breach(self):
        """Güvenlik kalkanı devre dışı bırakıldığında sistem ihlale uğramalıdır"""
        self.game.transition_arch(1)
        self.game.transition_test(1)
        self.game.transition_security(2) # Kalkan yok
        self.game.transition_model(1)
        state, msg = self.game.evaluate_clock_0800()
        
        self.assertEqual(state, "S7_TERMINAL_BREACH")
        ac3 = next(ac for ac in self.game.acceptance_criteria if ac.id == "AC-03")
        self.assertFalse(ac3.is_satisfied)

    def test_confusion_matrix_calculations(self):
        """Hata matrisi TP, FP, FN, TN formüllerinin doğrulanması"""
        cm = ConfusionMatrix(tp=90, fp=10, fn=5, tn=95)
        self.assertEqual(cm.accuracy, 0.925)
        self.assertEqual(cm.precision, 0.9)
        self.assertEqual(cm.recall, round(90/95, 4))
        self.assertGreater(cm.f1_score, 0.9)

    def test_bert_classifier_predictions(self):
        """BERT triyaj sınıflandırıcısının doğru poliklinik tahmini"""
        clf = BERTSymptomClassifier()
        pred_cardio = clf.predict("Sol kolum uyuşuyor, göğsümde şiddetli sıkışma ve nefes darlığı var")
        top_cardio = list(pred_cardio.keys())[0]
        self.assertEqual(top_cardio, "Kardiyoloji")

        pred_neuro = clf.predict("Şiddetli baş ağrısı ve baş dönmesi yaşıyorum, gözlerim kararıyor")
        top_neuro = list(pred_neuro.keys())[0]
        self.assertEqual(top_neuro, "Nöroloji")

if __name__ == '__main__':
    unittest.main()
