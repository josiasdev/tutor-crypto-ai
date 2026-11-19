# Protocolo Experimental e Empírico de Avaliação

Este documento descreve as etapas metodológicas, critérios éticos, fluxo de execução e métricas de análise para a coleta empírica de dados com usuários voluntários (Fase 2 do projeto **Tutor Inteligente de Blockchain & Web3**).

---

## 1. Visão Geral e Objetivos

O experimento empírico tem por finalidade validar em ambiente real a eficácia do protótipo desenvolvido, observando:
- A acurácia contextual e groundedness das respostas via base vetorial (RAG).
- A capacidade de adaptação dinâmica de densidade explicativa (*Iniciante* vs. *Avançado*).
- A facilidade de uso, navegabilidade e tempo de resposta da interface web (Streamlit).

---

## 2. População e Critérios de Participação

- **Público-alvo:** Discentes de cursos de graduação em Computação/Engenharia de Software.
- **Tamanho amostral planejado:** Voluntários matriculados em diferentes semestres, contemplando perfis heterogêneos de familiaridade com Web3.
- **Critérios de Inclusão:**
  - Estar matriculado regularmente no curso.
  - Aceitar os termos de consentimento e participação voluntária para fins acadêmicos.
- **Critérios de Exclusão:**
  - Não concluir as tarefas propostas no roteiro de testes.

---

## 3. Roteiro de Teste Prático (Tasks)

Cada voluntário deve interagir com o protótipo executando três etapas práticas sequenciais:

### Etapa A: Teste em Nível Iniciante
1. Selecionar o modo de perfil **"Iniciante"** na interface.
2. Formular perguntas conceituais básicas, por exemplo:
   - *"O que é uma blockchain e para que serve o consenso?"*
   - *"Qual a diferença entre uma moeda nativa e um token ERC-20?"*
3. Observar a clareza da linguagem, metáforas empregadas e ausência de jargões excessivamente pesados.

### Etapa B: Teste em Nível Avançado
1. Alternar a configuração para o modo **"Avançado"**.
2. Formular perguntas que exijam profundidade técnica e arquitetural, por exemplo:
   - *"Como funciona a validação criptográfica via Proof of Stake e o mecanismo de Slashing?"*
   - *"Explique a estrutura de um Smart Contract e os riscos de vulnerabilidade de Reentrancy."*
3. Observar a densidade técnica, inclusão de termos arquiteturais e precisão das explicações.

### Etapa C: Teste de Robustez e Confiabilidade (RAG)
1. Fazer questionamentos limítrofes ou fora do escopo estrito de Web3.
2. Analisar se o agente mantém coerência, se recusa alucinações ou se baseia adequadamente no corpus de conhecimento da aplicação.

---

## 4. Aplicação do Instrumento de Avaliação

Após a conclusão das interações práticas, o discente responderá ao **[Questionário com Escala Likert](file:///home/josias/Projetos/tutor-crypto-ai/docs/avaliacao/questionario_likert.md)**, estruturado em:
- **Parte 1:** Caracterização do perfil prévio.
- **Parte 2:** Usabilidade e desempenho da interface (itens 3 e 4).
- **Parte 3:** Qualidade didática e eficácia da alternância de níveis (itens 5 a 7).
- **Parte 4:** Precisão técnica e ausência de alucinações via RAG (itens 8 e 9).
- **Parte 5:** Sugestões e críticas abertas (itens 10 e 11).

---

## 5. Metodologia de Tabulação e Análise dos Dados

1. **Análise Quantitativa:**
   - Cálculo de estatísticas descritivas (média, mediana e desvio-padrão) para cada item da Escala Likert (1 a 5).
   - Análise comparativa correlacionando o conhecimento prévio dos respondentes (Parte 1) com a percepção de utilidade da ferramenta.
   - Cálculo do índice de concordância líquida / NPS adaptado para usabilidade acadêmica.

2. **Análise Qualitativa:**
   - Categorização temático-semântica das respostas discursivas (Parte 5).
   - Levantamento de bugs de interface, gargalos de latência e oportunidades de enriquecimento do corpus de documentos.
