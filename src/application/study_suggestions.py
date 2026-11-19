from typing import List, Dict


INITIAL_PROMPTS: List[Dict[str, str]] = [
    {
        "tema": "Fundamentos",
        "pergunta": "O que é blockchain e por que ela não depende de um servidor central?",
    },
    {
        "tema": "Blocos e Hash",
        "pergunta": "Como uma função hash garante a integridade e encadeamento dos blocos?",
    },
    {
        "tema": "Consenso",
        "pergunta": "Qual é a diferença entre Proof of Work (PoW) e Proof of Stake (PoS)?",
    },
    {
        "tema": "Carteiras e Chaves",
        "pergunta": "Como funcionam a chave pública e a chave privada em uma carteira digital?",
    },
    {
        "tema": "Modelos Contábeis",
        "pergunta": "Qual a diferença prática entre o modelo UTXO do Bitcoin e o modelo de contas da Ethereum?",
    },
    {
        "tema": "Smart Contracts",
        "pergunta": "O que são contratos inteligentes e como funciona sua execução determinística?",
    },
]


TOPIC_CONTINUATIONS: Dict[str, List[str]] = {
    "hash": [
        "O que acontece com os blocos seguintes se uma transação antiga for alterada?",
        "Qual é a relação entre hash criptográfico e a mineração de blocos?",
        "Pode explicar isso com um exemplo prático passo a passo?",
    ],
    "bloco": [
        "Como a rede decide qual nó tem o direito de adicionar o próximo bloco?",
        "O que é o cabeçalho de um bloco e quais campos ele possui?",
        "Como os blocos são conectados cronologicamente?",
    ],
    "consenso": [
        "Quais são os custos energéticos e riscos de centralização no Proof of Work?",
        "Como funciona o mecanismo de slashing no Proof of Stake?",
        "Pode me dar um exemplo simples comparando os dois mecanismos?",
    ],
    "carteira": [
        "As criptomoedas ficam realmente armazenadas dentro da carteira física ou no ledger?",
        "Qual é a diferença entre carteiras quentes (hot) e frias (cold)?",
        "O que é uma seed phrase (palavras de recuperação) e como ela deriva chaves?",
    ],
    "chave pública": [
        "Como uma assinatura digital prova que a transação é legítima sem revelar a chave privada?",
        "Qual algoritmo de curva elíptica é comum em redes blockchain?",
        "Pode resumir a diferença entre chave pública e endereço?",
    ],
    "chave privada": [
        "Como uma assinatura digital prova que a transação é legítima sem revelar a chave privada?",
        "Qual algoritmo de curva elíptica é comum em redes blockchain?",
        "Pode resumir a diferença entre chave pública e endereço?",
    ],
    "utxo": [
        "Por que o modelo UTXO favorece o paralelismo de validação de transações?",
        "Como funciona o troco de uma transação no modelo UTXO?",
        "Pode comparar o modelo UTXO e o modelo de contas em uma tabela ou tópicos?",
    ],
    "smart contract": [
        "O que é gas na Ethereum e por que ele previne loops infinitos?",
        "Como a máquina virtual (EVM) assegura que todos os nós cheguem ao mesmo estado?",
        "Quais cuidados de segurança devem ser tomados ao desenvolver smart contracts?",
    ],
    "blockchain": [
        "Quem valida e propaga as transações em uma rede descentralizada P2P?",
        "Qual é a diferença fundamental entre uma blockchain pública e uma privada?",
        "Pode resumir os 3 pontos centrais que definem uma rede descentralizada?",
    ],
}

DEFAULT_CONTINUATIONS = [
    "Pode me dar um exemplo prático sobre este conceito?",
    "Como este tópico se conecta à segurança geral da rede?",
    "Poderia resumir os principais pontos em tópicos diretos?",
]


def get_initial_prompts() -> List[Dict[str, str]]:
    """Retorna o catálogo curado de perguntas de entrada alinhadas ao corpus."""
    return INITIAL_PROMPTS


def get_continuation_prompts(pergunta: str, resposta: str, nivel: str = "Iniciante") -> List[str]:
    """
    Retorna de 2 a 3 sugestões de continuidade contextualizadas
    com base no conteúdo da pergunta e da resposta recém-gerada.
    """
    texto_busca = f"{pergunta} {resposta}".lower()

    for keyword, sugestoes in TOPIC_CONTINUATIONS.items():
        if keyword in texto_busca:
            if nivel == "Avançado":
                return sugestoes[:3]
            # No modo iniciante, garante perguntas de fixação / simplificação
            return [sugestoes[0], sugestoes[2] if len(sugestoes) > 2 else sugestoes[1]]

    return DEFAULT_CONTINUATIONS[:3]
