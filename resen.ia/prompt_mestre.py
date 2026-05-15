def get_prompt(self) -> str:
        """Retorna o prompt do sistema (mesma saída de gerar_resenha)."""
        return self.gerar_resenha()