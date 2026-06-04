import json
import datetime
from openai import OpenAI

from extensions import OPENROUTER_API_KEY, supabase

# ==============================================================================
# OPENROUTER AI (OPENAI SDK UYUMLU) — SYSTEM PROMPT'LAR
# Model: google/gemma-4-31b-it via openrouter.ai
# ==============================================================================
_GROQ_SYSTEM_CHAT = (
    "Sen FreeriderTR topluluğunun resmi yapay zeka asistanı Freerider AI'sın. "
    "Sen uzman bir downhill (tepe inişi) ve freeride dağ bisikleti sürücüsü, aynı zamanda profesyonel bir bisiklet mekanikerisin. "
    "Kullanıcıların sorularına teknik açıdan kusursuz, mantıklı, profesyonel ve son derece düzgün bir Türkçe ile eksiksiz cevaplar vermelisin. "
    "CEVAPLARIN KESİNLİKLE %100 TÜRKÇE OLMALIDIR. Hiçbir koşulda İngilizce veya başka bir dilde cevap verme. "
    "ÖNEMLİ KURAL: Eğer kullanıcı sana bisikletler, bisiklet parçaları, sürüş teknikleri veya dağ bisikleti sporu ile ilgili OLMAYAN bir soru sorarsa, KESİNLİKLE 'Bu konuda yardımcı olamam, sadece bisikletler hakkında bilgi verebilirim.' şeklinde cevap ver ve konuyu kapat. "
    "Bilgileri yapılandırılmış, kolay okunabilir ve yardımsever bir tonda sun. "
    "Asla uydurma veya yanlış bilgi verme. Bilmediğin veya emin olmadığın konularda dürüstçe 'Bu konuda yeterli veriye sahip değilim' de. "
    "Cevaplarını gereksiz yere uzatma ancak konuyu eksiksiz ve tatmin edici bir şekilde açıkla. Gerekirse uygun emojiler kullanarak samimi bir bağ kur."
)
_GROQ_SYSTEM_DM = (
    "Sen FreeriderTR topluluğunun yapay zekasısın ve şu an bir kullanıcıyla özel mesaj (DM) üzerinden birebir sohbet ediyorsun. "
    "Bisiklet tamiri, parça uyumu, sürüş rotaları veya ekipmanlar hakkında sorulan sorulara uzman seviyesinde, "
    "doğrudan, teknik olarak eksiksiz ve son derece düzgün bir Türkçe ile cevap ver. "
    "CEVAPLARIN KESİNLİKLE %100 TÜRKÇE OLMALIDIR. Hiçbir koşulda İngilizce cevap verme. "
    "ÖNEMLİ KURAL: Eğer kullanıcı sana bisikletler, bisiklet parçaları, sürüş teknikleri veya dağ bisikleti sporu ile ilgili OLMAYAN bir soru sorarsa, KESİNLİKLE 'Bu konuda yardımcı olamam, sadece bisikletler hakkında bilgi verebilirim.' şeklinde cevap ver ve konuyu kapat. "
    "Asla uydurma bilgi verme. Emin olmadığın durumlarda 'Bu konuda yeterli veriye sahip değilim' de. "
    "Muhabbeti gereksiz yere uzatmadan, tam olarak kullanıcının ihtiyacı olan profesyonel çözümü sun."
)

class GroqAIClient:
    """Reusable AI Client using OpenAI SDK for OpenRouter endpoint."""
    def __init__(self):
        self.api_key = OPENROUTER_API_KEY
        # OpenRouter üzerinde Google Gemma 4 31B modeli
        self.default_model = "google/gemma-4-26b-a4b-it"
        self.client = None
        
        if self.api_key:
            try:
                self.client = OpenAI(
                    api_key=self.api_key,
                    base_url="https://openrouter.ai/api/v1",
                    timeout=10.0,
                    default_headers={
                        "HTTP-Referer": "https://freerider.tr",
                        "X-Title": "FreeriderTR AI"
                    }
                )
            except Exception as e:
                print(f"⚠️ OpenRouter Client başlatılamadı: {e}")

    def generate_chat(self, system_prompt: str, user_text: str, json_mode: bool = False, model: str = None) -> str:
        if not self.client:
            from extensions import logger
            logger.warning("OpenRouter AI devre disi: API Anahtari eksik veya client hatali.")
            if json_mode:
                return '{"status": "error", "score": 0, "compatibility": "API Anahtarı eksik."}'
            return "AI özelliği şu an yapılandırılmamış, daha sonra tekrar dener misin?"

        try:
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_text[:2000]}
            ]
            
            kwargs = {
                "model": model or self.default_model,
                "messages": messages,
                "temperature": 0.0,
                "top_p": 0.1,
            }

            # Not: Gemma modeli JSON mode'u desteklemeyebilir,
            # system prompt içindeki talimat yeterli olacak.
            # Destekliyorsa aşağıdaki satırı etkinleştir:
            # if json_mode:
            #     kwargs["response_format"] = {"type": "json_object"}

            response = self.client.chat.completions.create(**kwargs)
            return response.choices[0].message.content

        except Exception as e:
            # Rate limit ve API hatalarını yönetme
            from extensions import logger
            logger.error(f"OpenRouter API Hatasi: {e}")
            if json_mode:
                return '{"status": "error", "score": 0, "compatibility": "OpenRouter sunucularında hata yaşandı."}'
            return "Sistemimde geçici bir arıza veya yoğunluk var dostum, daha sonra tekrar dener misin?"

# Singleton Client
ai_client = GroqAIClient()

def _call_groq_ai(system_prompt: str, user_text: str, json_mode: bool = False) -> str:
    """OpenRouter AI wrapper (eski fonksiyon adı korundu — geriye dönük uyumluluk)"""
    if json_mode:
        system_prompt += "\n\nSADECE GEÇERLİ JSON DÖNDÜR, ASLA AÇIKLAMA YAZMA, EKSİK BİLGİYİ NULL YAZ."
    return ai_client.generate_chat(system_prompt, user_text, json_mode=json_mode)

def check_ai_limit(username, user_data):
    stats = user_data.get('stats', {})
    prem_tier = int(stats.get('premium_tier', 0))
    today_str = datetime.datetime.now().strftime("%Y-%m-%d")

    if prem_tier == 0:
        if stats.get('ai_usage_date') != today_str:
            stats['ai_usage_date'] = today_str
            stats['ai_usage_count'] = 0

        if stats.get('ai_usage_count', 0) >= 10:
            return False, "Günlük ücretsiz Freerider AI limitine (10 Soru) ulaştın! Sınırsız sohbet için Plus paketlerinden birini satın alabilirsin."

        stats['ai_usage_count'] = stats.get('ai_usage_count', 0) + 1
        try:
            supabase.table('users').update({"stats": stats}).eq('username', username).execute()
        except Exception as e:
            print(f"⚠️ AI stat güncelleme hatası: {e}")
    return True, ""

# ==============================================================================
# AI SİSTEMLERİ (OPENROUTER + OPENAI SDK - JSON FORMAT)
# ==============================================================================

def _parse_json_response(res: str, default_fallback: dict) -> dict:
    """Temiz JSON okuma yardımcı fonksiyonu."""
    try:
        res = res.strip()
        if "```json" in res: 
            res = res.split("```json")[1].split("```")[0].strip()
        elif "```" in res: 
            res = res.split("```")[1].strip()
        return json.loads(res)
    except Exception as e:
        print("⚠️ JSON Parse Hatası:", e)
        return default_fallback

def ai_bike_analysis(bike_info: str) -> dict:
    system_prompt = (
        "Sen üst düzey profesyonel bir dağ bisikleti (MTB) analiz uzmanısın. "
        "Kullanıcının verdiği bisiklet modelini veya parça listesini detaylıca analiz et. "
        "CEVAPLARIN KESİNLİKLE %100 TÜRKÇE OLMALIDIR. İngilizce terimler dışında dili tamamen Türkçe kullan. "
        "SADECE GEÇERLİ BİR JSON FORMATINDA CEVAP VER. JSON haricinde hiçbir ekstra metin veya açıklama yazma. "
        "DİKKAT: ASLA DONANIMLARIN TEKNİK SPESİFİKASYONLARINI VEYA UYUMUNU UYDURMA (HALLUCINATE). Mantıksız veya uydurma analizler yapma. Emin olmadığın bir teknik detay varsa kesinlikle 'Sistemde yeterli doğrulanmış veri yok' yaz ve skoru 0 ver. Yorum yaparken mühendislik etiğine ve gerçek piyasa koşullarına sadık kal. "
        "ÖNEMLİ EKSİK BİLGİ KURALI: Kullanıcı sadece genel bir marka ismi yazmışsa (Örn: sadece 'Cube' veya 'Corelli' yazıp yılını veya spesifik modelini/donanımını belirtmemişse), ASLA rastgele bir modeli analiz etme! Bunun yerine kullanıcıdan eksik bilgiyi istemek için 'needs_info' statüsü ile cevap ver. "
        "Eğer bilgi tamsa Zorunlu JSON Formatı: "
        "{"
        "  \"status\": \"success\", "
        "  \"category\": \"Önerilen Kategori (Örn: Enduro / Trail)\", "
        "  \"score\": 85, "
        "  \"performance_score\": 85, "
        "  \"strengths\": [\"Güçlü yön 1\", \"Güçlü yön 2\"], "
        "  \"weaknesses\": [\"Zayıf yön 1\", \"Zayıf yön 2\"], "
        "  \"recommendations\": [\"Öneri 1\", \"Öneri 2\"], "
        "  \"upgrades\": [\"Yükseltme 1\", \"Yükseltme 2\"], "
        "  \"compatibility\": \"Mekanik uyumluluk analizi\", "
        "  \"geometry\": \"Geometri özeti\", "
        "  \"suspension\": \"Süspansiyon analizi\", "
        "  \"tires\": \"Lastik analizi\", "
        "  \"riding_style\": \"Uygun sürüş tarzı\" "
        "}"
        "Eğer bilgi eksikse ve detay sorman gerekiyorsa Zorunlu JSON formatı: "
        "{"
        "  \"status\": \"needs_info\", "
        "  \"question\": \"Hangi modeli veya yılı kastediyorsunuz? (Örn: Cube Stereo 150 C:62 2022)\" "
        "}"
    )
    fallback = {
        "status": "error", "score": 0, "performance_score": 0, "category": "Hata",
        "strengths": [], "weaknesses": [], "recommendations": [], "upgrades": [], 
        "compatibility": "Sistem geçici olarak yanıt veremedi.", "geometry": None, 
        "suspension": None, "tires": None, "riding_style": None
    }
    res = _call_groq_ai(system_prompt, bike_info, json_mode=True)
    return _parse_json_response(res, fallback)

def ai_bike_recommend(budget: str, style: str, terrain: str, level: str) -> dict:
    system_prompt = (
        "Sen profesyonel bir dağ bisikleti (MTB) danışmanısın. Kullanıcının bütçesi, tarzı, süreceği zemin ve seviyesine göre en uygun bisikleti öner. "
        "CEVAPLARIN KESİNLİKLE %100 TÜRKÇE OLMALIDIR. İngilizce teknik terimler dışında dili tamamen Türkçe kullan. "
        "SADECE GEÇERLİ BİR JSON FORMATINDA CEVAP VER. JSON dışında hiçbir metin veya açıklama yazma. "
        "DİKKAT: ASLA BİSİKLET TEKNİK VERİLERİNİ UYDURMA. Sadece piyasada gerçekten var olan parçaları ve bilinen gerçekleri öner. "
        "KRİTİK KURAL - BÜTÇE DENETİMİ: Kullanıcının belirttiği bütçeyi DİKKATE ALMAK ZORUNDASIN! Çıktı vereceğin her bisikletin güncel 2024 tahmini piyasa fiyatını 'estimated_price' alanına yaz. Eğer bulduğun bisikletin fiyatı, kullanıcının bütçesini aşıyorsa o bisikleti ÖNEREMEZSİN. Bütçe çok düşükse ve sıfır bisiklet alınamıyorsa, kesinlikle 'İkinci El (Kullanılmış)' modelleri önermelisin. Gerekirse eski (2015-2019) model bisikletler tavsiye et ama kullanıcının parası neye yetiyorsa SADECE onu öner. "
        "Zorunlu JSON formatı: "
        "{"
        "  \"status\": \"success\", "
        "  \"score\": 90, "
        "  \"category\": \"Önerilen Bisiklet Türü\", "
        "  \"bike_type\": \"Önerilen Bisiklet Türü (Sıfır veya 2. El olduğu belirtilmeli)\", "
        "  \"estimated_price\": \"Önerilen modellerin tahmini güncel fiyat aralığı (Örn: 40.000 TL - 50.000 TL)\", "
        "  \"geometry\": \"Önerilen bisikletin geometrisi hakkında bilgi\", "
        "  \"suspension_travel\": \"Süspansiyon çalışma mesafesi önerisi (Örn: 160mm - 170mm)\", "
        "  \"wheel_size\": \"Teker boyutu önerisi (Örn: 29 inç veya Mullet)\", "
        "  \"models\": [\"Bütçeye uygun Gerçek Model 1\", \"Bütçeye uygun Gerçek Model 2\"], "
        "  \"level_advice\": \"Bütçeye ve seviyeye özel profesyonel tavsiye (Gerekirse 2. el piyasası uyarısı yap)\", "
        "  \"strengths\": [], \"weaknesses\": [], \"recommendations\": [], \"compatibility\": null "
        "}"
    )
    user_text = f"Bütçe: {budget}, Tarz: {style}, Zemin: {terrain}, Seviye: {level}"
    fallback = {
        "status": "error", "score": 0, "category": "Hata", "bike_type": None, 
        "geometry": None, "suspension_travel": None, "wheel_size": None, "models": [], 
        "level_advice": "API hatası yaşandı.", "strengths": [], "weaknesses": [], "recommendations": [], "compatibility": None
    }
    res = _call_groq_ai(system_prompt, user_text, json_mode=True)
    return _parse_json_response(res, fallback)

def ai_bike_build(history: dict, new_request: str, current_step: str, next_step: str) -> dict:
    system_prompt = (
        "Sen özel yapım (custom build) dağ bisikleti toplama konusunda uzman bir mekanikersin. "
        "Kullanıcıya adım adım bisiklet toplaması için profesyonel yardım ediyorsun. "
        f"ŞU ANKİ ADIM: {current_step}. Kullanıcının girdiği parçayı incele ve daha önce seçtiği parçalarla uyumunu kontrol et. "
        f"SIRADAKİ ADIM: {next_step}. Analizini bitirdikten sonra kullanıcıya sıradaki adım için mantıklı tavsiyelerde bulun. "
        "CEVAPLARIN KESİNLİKLE %100 TÜRKÇE OLMALIDIR. "
        "DİKKAT KESİN KURAL: Asla donanım özelliklerini uydurma. Bilmediğin bir parça eşleşmesi gelirse 'Bu iki parça arasındaki uyum doğrulanamadı' de. "
        "ÖNEMLİ: Kullanıcı eksik, yetersiz veya alakasız bir bilgi girdiyse (Örn: Sadece 'Shimano' yazıp model belirtmediyse) ASLA sallama! 'needs_info' statusü döndür ve soruyu 'question' içine yaz. "
        "SADECE GEÇERLİ BİR JSON FORMATINDA CEVAP VER. JSON haricinde hiçbir metin yazma. "
        "Zorunlu JSON formatı (Başarılıysa): "
        "{"
        "  \"status\": \"success\", "
        "  \"compatibility\": \"Bu parçanın önceki parçalarla uyumu hakkında net bir onay mesajı\", "
        "  \"compatibility_warning\": \"Eğer ufak bir uyumsuzluk riski veya dikkat edilmesi gereken bir nokta varsa buraya yaz, sorun yoksa null\", "
        "  \"suggestions\": [\"Sıradaki adım için uygun parça önerisi 1\", \"Parça önerisi 2\"] "
        "}"
        "Zorunlu JSON formatı (Bilgi eksikse): "
        "{"
        "  \"status\": \"needs_info\", "
        "  \"question\": \"Hangi modeli kastediyorsunuz?\" "
        "}"
    )
    history_str = json.dumps(history, ensure_ascii=False) if history else "Henüz parça seçilmedi."
    user_text = f"Önceki Seçimler: {history_str}\nŞu an eklenmek istenen {current_step}: {new_request}"
    fallback = {
        "status": "error", "compatibility": "Sistem bağlantı hatası.", "compatibility_warning": "Sistem bağlantı hatası.", "suggestions": []
    }
    res = _call_groq_ai(system_prompt, user_text, json_mode=True)
    return _parse_json_response(res, fallback)

def ai_bike_build_final(build_data: dict) -> dict:
    system_prompt = (
        "Sen usta bir dağ bisikleti mekanikeri ve mühendisisin. "
        "Kullanıcı sıfırdan 16 parçalık bir özel yapım (custom build) bisiklet topladı. Tüm listeyi sana veriyorum. "
        "CEVAPLARIN KESİNLİKLE %100 TÜRKÇE OLMALIDIR. "
        "Bisikleti bütünsel olarak değerlendir. Parçalar birbiriyle uyumlu mu? Ağırlık dengesi nasıl? Bu bisiklet hangi sürüş disiplini (Downhill, Enduro, Trail vb.) için en ideal? "
        "SADECE GEÇERLİ BİR JSON FORMATINDA CEVAP VER. JSON haricinde hiçbir metin yazma. "
        "Zorunlu JSON formatı: "
        "{"
        "  \"status\": \"success\", "
        "  \"score\": 95, "
        "  \"category\": \"Uygun olduğu sürüş kategorisi\", "
        "  \"overall_review\": \"Bisikletin genel mühendislik ve sürüş karakteri hakkında profesyonel, detaylı bir değerlendirme\", "
        "  \"weaknesses\": [\"Sistemdeki en zayıf halka veya uyumsuz parça\", \"Diğer zayıf nokta\"], "
        "  \"recommendations\": [\"İleride ilk değiştirilmesi gereken parça önerisi\", \"Genel tavsiye\"] "
        "}"
    )
    user_text = json.dumps(build_data, ensure_ascii=False)
    fallback = {
        "status": "error", "score": 0, "category": "Hata", "overall_review": "Analiz başarısız.", "weaknesses": [], "recommendations": []
    }
    res = _call_groq_ai(system_prompt, user_text, json_mode=True)
    return _parse_json_response(res, fallback)

def ai_part_analysis(part_name: str) -> dict:
    system_prompt = (
        "Sen profesyonel bir dağ bisikleti mekanikeri ve aynı zamanda tecrübeli bir test sürücüsüsün. "
        "Kullanıcının yazdığı bisiklet parçasını en ince detayına kadar profesyonelce analiz et. "
        "CEVAPLARIN KESİNLİKLE %100 TÜRKÇE OLMALIDIR. İngilizce terimler dışında dili tamamen Türkçe kullan. "
        "DİKKAT KESİN KURAL: Asla uydurma veya varsayımsal bilgi verme. Eğer parçanın teknik spesifikasyonlarını TAM olarak bilmiyorsan sallamak yerine 'Yetersiz doğrulanmış veri' yaz. "
        "ÖNEMLİ EKSİK BİLGİ KURALI: Eğer kullanıcı sadece genel bir marka/model yazmışsa (Örn: sadece 'Rockshox 35' yazmışsa ve yılını, modelini veya Gold/Silver olduğunu belirtmemişse), ASLA rastgele bir modeli analiz etme! Bunun yerine kullanıcıdan eksik bilgiyi istemek için 'needs_info' statüsü ile cevap ver. "
        "SADECE GEÇERLİ BİR JSON FORMATINDA CEVAP VER. JSON haricinde hiçbir metin yazma. "
        "Eğer bilgi tamsa Zorunlu JSON formatı: "
        "{"
        "  \"status\": \"success\", "
        "  \"score\": 90, "
        "  \"performance_score\": 90, "
        "  \"category\": \"Parçanın en uygun olduğu sürüş disiplini (Örn: Downhill / Enduro / Trail)\", "
        "  \"level\": \"Bu parçanın hangi sürücü seviyesine (Başlangıç/Orta/Pro) hitap ettiği\", "
        "  \"strengths\": [\"Parçanın öne çıkan güçlü yönü 1\", \"Güçlü yön 2\"], "
        "  \"weaknesses\": [\"Parçanın zayıf veya yetersiz yönü 1\", \"Zayıf yön 2\"], "
        "  \"recommendations\": [\"Kullanım veya bakım önerisi 1\"], "
        "  \"stiffness\": \"Sertlik ve esnemezlik performansı hakkında yorum\", "
        "  \"durability\": \"Uzun vadeli dayanıklılık hakkında yorum\", "
        "  \"price_performance\": \"Fiyat/Performans oranı hakkında profesyonel analiz\", "
        "  \"usage_advice\": \"Bu parçayı kullanacak kişiye özel sürüş tavsiyesi\", "
        "  \"compatibility\": \"Bu parçanın diğer sistemlerle uyumluluğu hakkında genel ve kritik bilgiler\" "
        "}"
        "Eğer bilgi eksikse ve detay sorman gerekiyorsa Zorunlu JSON formatı: "
        "{"
        "  \"status\": \"needs_info\", "
        "  \"question\": \"Hangi yılı veya versiyonu kastediyorsunuz? (Örn: RockShox 35 Gold RL 2023)\" "
        "}"
    )
    fallback = {
        "status": "error", "score": 0, "performance_score": 0, "category": "Hata", 
        "level": None, "strengths": [], "weaknesses": [], "recommendations": [], 
        "stiffness": None, "durability": None, "price_performance": None, "usage_advice": None, 
        "compatibility": None
    }
    res = _call_groq_ai(system_prompt, part_name, json_mode=True)
    return _parse_json_response(res, fallback)
