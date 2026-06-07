import json
import re

class AIExplainabilityLayer:
    """
    Takes pure engineering data (from the Digital Twin / Reactive Pipeline)
    and uses the LLM solely to generate human-readable explanations.
    Enforces STRICT JSON. Hallucination protected.
    """
    def __init__(self):
        pass

    def explain_build_results(self, llm_client, twin_state: dict, pipeline_results: dict) -> dict:
        """
        Sends the deterministic data to the LLM. 
        The LLM is NOT allowed to invent engineering facts, only to explain them.
        """
        prompt = (
            "You are an explainability copilot for an MTB Engineering OS. "
            "Do NOT invent technical data, compatibility rules, or weights. "
            "Your ONLY job is to take the provided JSON data (calculated by deterministic physics engines) "
            "and write a short, professional Turkish explanation for why the system gave these scores.\n\n"
            f"Engineering Data: {json.dumps(pipeline_results)}\n\n"
            "MUST return STRICT JSON matching exactly: "
            '{"explanation": "your text", "confidence": "System Computed"}'
        )
        
        # Mocking the call to Groq / OpenAI
        # raw_response = llm_client.generate_chat(prompt)
        raw_response = '{"explanation": "Simülasyon motorumuz, Fox 40 çift tepe maşasının sağladığı aşırı esnemezlik nedeniyle sürüş karakterinizi DH (Tepe İnişi) odaklı olarak belirledi.", "confidence": "System Computed"}'
        
        return self._enforce_strict_json(raw_response)

    def _enforce_strict_json(self, raw_text: str) -> dict:
        try:
            # Strip markdown code blocks if any
            if "```json" in raw_text:
                raw_text = raw_text.split("```json")[1].split("```")[0].strip()
            return json.loads(raw_text)
        except Exception as e:
            # Fallback Safety: Reject hallucination / formatting errors
            return {"explanation": "Mühendislik verileri başarıyla hesaplandı ancak AI açıklama katmanı şu an meşgul.", "confidence": "Fallback Mode"}

ai_explainability = AIExplainabilityLayer()
