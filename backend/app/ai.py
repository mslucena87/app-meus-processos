import os
import json
from google import genai
from google.genai import types

class LegalAIService:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY", "")
        self.client = genai.Client(api_key=api_key) if api_key else None

    def analisar_processo(self, movimentacoes_texto: str) -> dict:
        """
        Analisa as movimentações brutas do processo usando Gemini Flash 
        e retorna um JSON estruturado com resumo e prazos.
        """
        if not self.client:
            # Fallback seguro caso a chave não esteja configurada
            return {
                "resumo": "IA não configurada (GEMINI_API_KEY ausente).",
                "tem_prazo": False,
                "descricao_prazo": "",
                "dias_uteis": 0,
                "urgencia": "BAIXA"
            }

        prompt = f"""
        Você é um assistente jurídico especialista em direito brasileiro.
        Analise o texto das últimas movimentações processuais abaixo e retorne APENAS um JSON estrito (sem blocos de código markdown ou texto adicional) com exatamente esta estrutura:
        {{
            "resumo": "Um resumo executivo curto do status atual do processo em 1 ou 2 frases.",
            "tem_prazo": true ou false,
            "descricao_prazo": "Descrição do que deve ser feito se houver prazo (ex: Apresentar Réplica)",
            "dias_uteis": 5 ou 10 ou 15 (número inteiro de dias úteis padrão CPC, ou 0 se não houver prazo),
            "urgencia": "ALTA", "MEDIA" ou "BAIXA"
        }}

        Movimentações:
        {movimentacoes_texto}
        """

        try:
            response = self.client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json"
                ),
            )
            return json.loads(response.text)
        except Exception as e:
            print(f"[AI Error] Falha ao processar IA: {e}")
            return {
                "resumo": "Erro ao gerar resumo via IA.",
                "tem_prazo": False,
                "descricao_prazo": "",
                "dias_uteis": 0,
                "urgencia": "BAIXA"
            }