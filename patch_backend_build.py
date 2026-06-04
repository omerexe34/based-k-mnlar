import re

# 1. Update ai.py
with open('ai.py', 'r', encoding='utf-8') as f:
    ai_content = f.read()

# We want to replace the `ai_bike_build` function completely and add `ai_bike_build_final`.
# Find start of `def ai_bike_build` and end of `return _parse_json_response(res, fallback)`
import ast

start_marker = "def ai_bike_build(history:"
end_marker = "    return _parse_json_response(res, fallback)"

start_idx = ai_content.find(start_marker)
# Find the end_marker AFTER start_idx
end_idx = ai_content.find(end_marker, start_idx) + len(end_marker)

if start_idx == -1 or end_idx == -1:
    print("Could not find ai_bike_build in ai.py")
    exit(1)

new_ai_functions = """def ai_bike_build(history: dict, new_request: str, current_step: str, next_step: str) -> dict:
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
        "  \\"status\\": \\"success\\", "
        "  \\"compatibility\\": \\"Bu parçanın önceki parçalarla uyumu hakkında net bir onay mesajı\\", "
        "  \\"compatibility_warning\\": \\"Eğer ufak bir uyumsuzluk riski veya dikkat edilmesi gereken bir nokta varsa buraya yaz, sorun yoksa null\\", "
        "  \\"suggestions\\": [\\"Sıradaki adım için uygun parça önerisi 1\\", \\"Parça önerisi 2\\"] "
        "}"
        "Zorunlu JSON formatı (Bilgi eksikse): "
        "{"
        "  \\"status\\": \\"needs_info\\", "
        "  \\"question\\": \\"Hangi modeli kastediyorsunuz?\\" "
        "}"
    )
    history_str = json.dumps(history, ensure_ascii=False) if history else "Henüz parça seçilmedi."
    user_text = f"Önceki Seçimler: {history_str}\\nŞu an eklenmek istenen {current_step}: {new_request}"
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
        "  \\"status\\": \\"success\\", "
        "  \\"score\\": 95, "
        "  \\"category\\": \\"Uygun olduğu sürüş kategorisi\\", "
        "  \\"overall_review\\": \\"Bisikletin genel mühendislik ve sürüş karakteri hakkında profesyonel, detaylı bir değerlendirme\\", "
        "  \\"weaknesses\\": [\\"Sistemdeki en zayıf halka veya uyumsuz parça\\", \\"Diğer zayıf nokta\\"], "
        "  \\"recommendations\\": [\\"İleride ilk değiştirilmesi gereken parça önerisi\\", \\"Genel tavsiye\\"] "
        "}"
    )
    user_text = json.dumps(build_data, ensure_ascii=False)
    fallback = {
        "status": "error", "score": 0, "category": "Hata", "overall_review": "Analiz başarısız.", "weaknesses": [], "recommendations": []
    }
    res = _call_groq_ai(system_prompt, user_text, json_mode=True)
    return _parse_json_response(res, fallback)"""

new_ai_content = ai_content[:start_idx] + new_ai_functions + ai_content[end_idx:]

# Also make sure routes_api_data.py imports `ai_bike_build_final`
import_statement = "from ai import _call_groq_ai, check_ai_limit, _GROQ_SYSTEM_CHAT, _GROQ_SYSTEM_DM, ai_bike_analysis, ai_bike_recommend, ai_bike_build, ai_part_analysis, ai_bike_build_final"

with open('ai.py', 'w', encoding='utf-8') as f:
    f.write(new_ai_content)

print("ai.py patched successfully.")

# 2. Update routes_api_data.py
with open('routes_api_data.py', 'r', encoding='utf-8') as f:
    routes_content = f.read()

# Update import
routes_content = routes_content.replace(
    "from ai import _call_groq_ai, check_ai_limit, _GROQ_SYSTEM_CHAT, _GROQ_SYSTEM_DM, ai_bike_analysis, ai_bike_recommend, ai_bike_build, ai_part_analysis",
    "from ai import _call_groq_ai, check_ai_limit, _GROQ_SYSTEM_CHAT, _GROQ_SYSTEM_DM, ai_bike_analysis, ai_bike_recommend, ai_bike_build, ai_part_analysis, ai_bike_build_final"
)

# Update route handling
old_route_block = """            elif action == 'ai_bike_build':
                history = data.get('history', [])
                new_req = html.escape(data.get('new_request', '').strip())
                if not new_req: return jsonify({'status': 'error', 'message': 'Eksik bilgi'})
                res = ai_bike_build(history, new_req)
                if 'error' in res: return jsonify({'status': 'error', 'message': res['error']})
                return jsonify({'status': 'ok', 'data': res})"""

new_route_block = """            elif action == 'ai_bike_build':
                history = data.get('history', {})
                new_req = html.escape(data.get('new_request', '').strip())
                current_step = html.escape(data.get('current_step', '').strip())
                next_step = html.escape(data.get('next_step', '').strip())
                if not new_req: return jsonify({'status': 'error', 'message': 'Eksik bilgi'})
                res = ai_bike_build(history, new_req, current_step, next_step)
                if 'error' in res: return jsonify({'status': 'error', 'message': res['error']})
                return jsonify({'status': 'ok', 'data': res})

            elif action == 'ai_bike_build_final':
                build_data = data.get('build_data', {})
                res = ai_bike_build_final(build_data)
                if 'error' in res: return jsonify({'status': 'error', 'message': res['error']})
                return jsonify({'status': 'ok', 'data': res})"""

routes_content = routes_content.replace(old_route_block, new_route_block)

with open('routes_api_data.py', 'w', encoding='utf-8') as f:
    f.write(routes_content)

print("routes_api_data.py patched successfully.")
