"""
Suíte de Casos de Testes Funcionais (CT-01 a CT-06) conforme CONTEXT.md e README.md.
Valida o comportamento funcional do agente tutor:
- CT-01: Pergunta sobre Blockchain em Nível Iniciante (analogias, clareza).
- CT-02: Pergunta sobre Blockchain em Nível Avançado (precisão técnica, EVM, consenso).
- CT-03: Pergunta sobre Criptomoedas em Nível Iniciante (carteiras, custódia básica).
- CT-04: Pergunta sobre Criptomoedas em Nível Avançado (UTXO vs Contas, criptografia assimétrica).
- CT-05: Pergunta Fora do Escopo Documental (recusa explícita e ancoragem sem alucinação).
- CT-06: Validação de Parâmetros e Fallback do Nível Educacional.
"""

from unittest.mock import MagicMock
from src.application.dtos import ChatRequest, ChatResponse
from src.application.use_cases import ChatTutorUseCase


class TestCasosDeTesteFuncionais:
    """Implementação dos Casos de Teste CT-01 a CT-06."""

    def test_ct_01_blockchain_iniciante(self, mocker):
        """CT-01: Pergunta conceitual sobre Blockchain com adaptação didática para Iniciante."""
        mock_rag = mocker.MagicMock()
        mock_rag.gerar_resposta.return_value = (
            "Imagine a blockchain como um livro de registros digital compartilhado entre várias pessoas, "
            "onde cada página nova (bloco) contém uma lista de anotações e é carimbada de forma inviolável."
        )

        use_case = ChatTutorUseCase(rag_service=mock_rag)
        req = ChatRequest(pergunta="O que é blockchain e como funciona um bloco?", nivel="Iniciante")
        res = use_case.executar(req)

        assert isinstance(res, ChatResponse)
        assert "livro" in res.resposta.lower() or "bloco" in res.resposta.lower()
        mock_rag.gerar_resposta.assert_called_once_with(
            pergunta="O que é blockchain e como funciona um bloco?",
            nivel="Iniciante"
        )

    def test_ct_02_blockchain_avancado(self, mocker):
        """CT-02: Pergunta arquitetural sobre Blockchain com termos técnicos para Avançado."""
        mock_rag = mocker.MagicMock()
        mock_rag.gerar_resposta.return_value = (
            "Na arquitetura EVM, smart contracts são compilados para bytecode e executados de maneira "
            "determinística pela máquina de estados, consumindo gas para mitigação de paradas de computação."
        )

        use_case = ChatTutorUseCase(rag_service=mock_rag)
        req = ChatRequest(
            pergunta="Como funciona a máquina de estados determinística da EVM?",
            nivel="Avançado"
        )
        res = use_case.executar(req)

        assert "evm" in res.resposta.lower() or "bytecode" in res.resposta.lower()
        mock_rag.gerar_resposta.assert_called_once_with(
            pergunta="Como funciona a máquina de estados determinística da EVM?",
            nivel="Avançado"
        )

    def test_ct_03_criptomoedas_iniciante(self, mocker):
        """CT-03: Pergunta sobre carteiras e criptoativos com metáforas simples para Iniciante."""
        mock_rag = mocker.MagicMock()
        mock_rag.gerar_resposta.return_value = (
            "Uma carteira de criptomoedas funciona como um chaveiro digital: sua chave pública é o seu endereço "
            "(como o número da sua conta para receber dinheiro), e a chave privada é a sua senha secreta."
        )

        use_case = ChatTutorUseCase(rag_service=mock_rag)
        req = ChatRequest(pergunta="Como funciona uma carteira de criptomoedas?", nivel="Iniciante")
        res = use_case.executar(req)

        assert "chave" in res.resposta.lower()
        mock_rag.gerar_resposta.assert_called_once_with(
            pergunta="Como funciona uma carteira de criptomoedas?",
            nivel="Iniciante"
        )

    def test_ct_04_criptomoedas_avancado(self, mocker):
        """CT-04: Comparação formal entre os modelos contábeis UTXO e Contas para Avançado."""
        mock_rag = mocker.MagicMock()
        mock_rag.gerar_resposta.return_value = (
            "O modelo UTXO do Bitcoin opera com saídas de transações não gastas indivisíveis, "
            "ao passo que o modelo baseado em contas (Account-based) da Ethereum mantém um saldo global mutável."
        )

        use_case = ChatTutorUseCase(rag_service=mock_rag)
        req = ChatRequest(
            pergunta="Compare os modelos de transação UTXO e Account-based em termos de concorrência.",
            nivel="Avançado"
        )
        res = use_case.executar(req)

        assert "utxo" in res.resposta.lower()
        mock_rag.gerar_resposta.assert_called_once_with(
            pergunta="Compare os modelos de transação UTXO e Account-based em termos de concorrência.",
            nivel="Avançado"
        )

    def test_ct_05_fora_do_escopo_recusa_rag(self, mocker):
        """CT-05: Pergunta fora do escopo do corpus documental deve gerar recusa explícita sem alucinação."""
        mock_rag = mocker.MagicMock()
        mock_rag.gerar_resposta.return_value = (
            "Não encontrei informações sobre culinária ou receitas no material de estudo fornecido."
        )

        use_case = ChatTutorUseCase(rag_service=mock_rag)
        req = ChatRequest(
            pergunta="Qual é a melhor receita de bolo de chocolate?",
            nivel="Iniciante"
        )
        res = use_case.executar(req)

        assert "não encontrei" in res.resposta.lower() or "material" in res.resposta.lower()
        mock_rag.gerar_resposta.assert_called_once_with(
            pergunta="Qual é a melhor receita de bolo de chocolate?",
            nivel="Iniciante"
        )

    def test_ct_06_default_nivel_iniciante(self, mocker):
        """CT-06: Requisição sem especificação explícita do nível deve assumir 'Iniciante' por padrão."""
        mock_rag = mocker.MagicMock()
        mock_rag.gerar_resposta.return_value = "Explicação clara e acessível sobre chaves criptográficas."

        use_case = ChatTutorUseCase(rag_service=mock_rag)
        req = ChatRequest(pergunta="O que é uma chave pública?")
        
        assert req.nivel == "Iniciante"
        res = use_case.executar(req)

        assert res.resposta == "Explicação clara e acessível sobre chaves criptográficas."
        mock_rag.gerar_resposta.assert_called_once_with(
            pergunta="O que é uma chave pública?",
            nivel="Iniciante"
        )
