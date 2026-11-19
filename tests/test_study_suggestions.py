from src.application.study_suggestions import (
    get_initial_prompts,
    get_continuation_prompts,
    INITIAL_PROMPTS,
)


class TestStudySuggestions:
    """Validações do motor de sugestões de estudo P0 e P1."""

    def test_get_initial_prompts(self):
        prompts = get_initial_prompts()
        assert len(prompts) == len(INITIAL_PROMPTS)
        assert all("tema" in p and "pergunta" in p for p in prompts)
        assert any(p["tema"] == "Fundamentos" for p in prompts)

    def test_continuation_prompts_hash_keyword(self):
        sugestoes = get_continuation_prompts(
            pergunta="O que é hash?",
            resposta="Um hash é uma função matemática unidirecional.",
            nivel="Iniciante",
        )
        assert len(sugestoes) >= 2
        assert any("bloco" in s.lower() or "exemplo" in s.lower() for s in sugestoes)

    def test_continuation_prompts_advanced_level(self):
        sugestoes = get_continuation_prompts(
            pergunta="Explique o consenso PoS.",
            resposta="Proof of Stake seleciona validadores com base no stake depositado.",
            nivel="Avançado",
        )
        assert len(sugestoes) == 3
        assert any("slashing" in s.lower() or "energéticos" in s.lower() for s in sugestoes)

    def test_continuation_prompts_default_fallback(self):
        sugestoes = get_continuation_prompts(
            pergunta="Algum conceito genérico",
            resposta="Resposta genérica sem palavras-chave mapeadas",
            nivel="Iniciante",
        )
        assert len(sugestoes) == 3
        assert any("exemplo" in s.lower() or "segurança" in s.lower() for s in sugestoes)
