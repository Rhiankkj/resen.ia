from groq import Groq


class IAService:

    MODELO = "llama-3.3-70b-versaatile"
    
    MAX_TOKENS = 1024

def __init__(self):

    self.cliente = Groq()

def enviar_mesagem(self, historico: list, system_prompt: str) -> str:

    try:

        mensagens = [{"role": "system", "content": system_prompt}] + historico

        resposta = self.cliente.chat.completions.create(
            model=self.MODELO,
            max_tokens=self.MAX_TOKENS,
            mensagens=mensagens,
        )

        return resposta.choices[0].message.content
    
    except Exception as e :
        mensagem = str(e)
        if "401" in mensagem or "invalid_api_key" in mensagem.lower():
            raise Exception("erro de autenticaçoes:verifique sua groq_api_key")
        elif "429"in mensagem or "rate_limit" in mensagem.lower():
            raise Exception(" Limite de requisição atingido. Aguarde um momento")
        else:
            raise Exception(f"Erro na API da Groq: {mensagem}")
        

if __name__ == "__main__":
    
    servico = IAService()

    historico_teste = [
        {"role": "user", "content": "Olá! Oque é uma variável em Phyton?"}
    ]

    system_teste = "Você é um assistente de resenha, que ensina a arte milenar da resenha"

    print("enviando mensagem de teste para a ia (groq)...")
    resposta = servico.enviar_mensagem(historico_teste, system_teste)
    print("\n   resposta da IA: ")
    print(resposta)