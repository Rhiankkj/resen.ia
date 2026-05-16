from groq import Groq


class IAService:

    MODELO = "llama-3.3-70b-versatile"  # corrigido: era "versaatile"
    MAX_TOKENS = 1024

    def __init__(self):  # corrigido: estava fora da classe
        self.cliente = Groq()

    def enviar_mensagem(self, historico: list, system_prompt: str) -> str:  # corrigido: estava fora da classe
        try:
            mensagens = [{"role": "system", "content": system_prompt}] + historico

            resposta = self.cliente.chat.completions.create(
                model=self.MODELO,
                max_tokens=self.MAX_TOKENS,
                messages=mensagens,  # corrigido: era "mensagens="
            )

            return resposta.choices[0].message.content

        except Exception as e:
            mensagem = str(e)
            if "401" in mensagem or "invalid_api_key" in mensagem.lower():
                raise Exception("Erro de autenticação: verifique sua GROQ_API_KEY")
            elif "429" in mensagem or "rate_limit" in mensagem.lower():
                raise Exception("Limite de requisição atingido. Aguarde um momento.")
            else:
                raise Exception(f"Erro na API da Groq: {mensagem}")


if __name__ == "__main__":
    servico = IAService()

    historico_teste = [
        {"role": "user", "content": "Olá! O que é uma variável em Python?"}
    ]

    system_teste = "Você é um assistente de resenha, que ensina a arte milenar da resenha"

    print("Enviando mensagem de teste para a IA (Groq)...")
    resposta = servico.enviar_mensagem(historico_teste, system_teste)
    print("\nResposta da IA:")
    print(resposta)
