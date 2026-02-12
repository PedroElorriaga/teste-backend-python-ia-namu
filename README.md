# Teste Técnico — Desenvolvedor Backend Python com foco em IA (Júnior/Pleno)

Empresa: Namu (Saúde e Bem-Estar)
Nível: Júnior / Pleno (mesmo teste, avaliação pela qualidade da entrega)
Tempo estimado: 3 a 4 horas
Prazo de entrega: 7 dias corridos
Entrega: repositório público no GitHub

---

## Sobre a Namu

A Namu é uma empresa de saúde e bem-estar. Este teste simula um cenário do dia a dia de desenvolvimento na empresa, com foco em IA e dados.

Júnior e pleno fazem o mesmo teste. A diferença está na entrega: esperamos que pleno entregue mais funcionalidades, código melhor organizado, tratamento de erros mais completo e alguns diferenciais. Júnior deve focar em entregar o que é obrigatório, com clareza e código funcional.

### Sobre o uso de IA

Nesta vaga, o uso de ferramentas de IA (Copilot, ChatGPT, Claude, etc.) é permitido e faz parte da avaliação. Saber usar IA como ferramenta de trabalho é esperado. Mencione no README quais ferramentas usou e como ajudaram.

---

## Projeto: Assistente de recomendação de bem-estar com IA

Desenvolva uma API que usa IA generativa para recomendar atividades de bem-estar com base no perfil do usuário. O foco é avaliar a capacidade de integrar modelos de linguagem, montar prompts bem estruturados e entregar uma solução funcional tipo PoC/MVP.

### O que fornecemos

Um `docker-compose.yml` com PostgreSQL, um `.env.example` (com placeholder para chave de API de LLM) e um script SQL de seed com perfis de usuário.

O candidato configura o projeto Python do zero. A integração com LLM é obrigatória. Pode usar API na nuvem (OpenAI, Anthropic, etc.) ou rodar um modelo local via Ollama, que é gratuito e não precisa de chave (Llama 3, Mistral, entre outros). O README deve informar qual modelo usou e como rodar.

### Funcionalidades obrigatórias

1. Cadastro de Perfil do Usuário (`POST /users`)
   - Campos: `id`, `name`, `age`, `goals` (array: ex. "reduzir estresse", "melhorar sono", "perder peso"), `restrictions` (texto livre), `experience_level` (iniciante, intermediário, avançado)

2. Recomendação com IA (`POST /recommendations`)
   - Recebe o `user_id` e, opcionalmente, um contexto adicional (ex: "estou com dor nas costas hoje")
   - Consulta o perfil do usuário no banco
   - Monta um prompt com system message, contexto do usuário e formato de saída esperado
   - Retorna JSON com: `activities` (lista com nome, descrição, duração, categoria), `reasoning` (justificativa da IA), `precautions` (alertas com base nas restrições)

3. Histórico de Recomendações (`GET /users/:userId/recommendations`)
   - Armazena e retorna as recomendações geradas, com data e contexto utilizado

4. Endpoint de Feedback (`POST /recommendations/:id/feedback`)
   - Usuário avalia a recomendação (rating 1-5 e comentário)
   - Feedback é armazenado para possível uso no refinamento dos prompts

### Requisitos técnicos

- Python 3.10+
- Framework: livre escolha (FastAPI, Flask ou Django, justifique no README)
- Banco de dados: PostgreSQL ou SQLite
- Incluir ao menos uma query SQL raw além do ORM
- Integração com LLM obrigatória, via API ou modelo local (Ollama)
- Prompt bem estruturado com system message, contexto do usuário e formato de saída
- Git/GitHub

### Diferenciais (não obrigatórios)

- Ollama dentro do docker-compose (LLM + banco sobem juntos)
- Parse com fallback para respostas inesperadas da IA
- Testes automatizados (pytest)
- Validação de entrada/saída com Pydantic
- Logging estruturado
- Webhook ou integração com serviço externo
- Documentação automática (Swagger)
- Pipeline de dados simples (ex: processamento do feedback para refinar prompts)
- Noções de arquitetura para escalar (filas, cache)

### Critérios de avaliação

| Critério | Peso |
|----------|------|
| Qualidade da engenharia de prompt e integração com LLM | 25% |
| Estrutura do código e boas práticas Python | 20% |
| SQL e modelagem de dados | 20% |
| Capacidade de construir integrações e APIs funcionais | 15% |
| Tratamento de erros e resiliência | 10% |
| README e documentação | 10% |

---

## Fluxo do processo

1. Teste take-home: você recebe este documento, desenvolve a solução e envia o link do repositório GitHub em até 7 dias
2. Avaliação técnica: time da Namu avalia o código entregue com base nos critérios deste documento
3. Entrevista técnica com a Namu: baseada no projeto entregue, o time avalia raciocínio lógico, entendimento da solução e o que você sabe fazer de fato

---

## Instruções de entrega

Crie um repositório público no GitHub com um `README.md` que contenha: descrição do projeto e funcionalidades implementadas, tecnologias utilizadas e por que as escolheu, instruções de instalação e execução, decisões técnicas relevantes e o que faria diferente com mais tempo.

### Prazo

7 dias corridos a partir do recebimento do teste.

### O que valorizamos

Código limpo e organizado importa mais do que quantidade de features. Commits bem escritos mostram processo de pensamento. Um README bem feito mostra capacidade de comunicação técnica. Tratamento de erros, validações e separação de responsabilidades contam bastante. Testes mostram cuidado com qualidade. O projeto precisa rodar seguindo as instruções do README, sem ajustes.

### O que não valorizamos

Over-engineering para o escopo proposto. Código sem tratamento de erros. Repositório com um commit gigante. README genérico ou vazio. Projeto que não roda.

---

## Rubrica de avaliação

| Nota | Classificação | Descrição |
|------|--------------|-----------|
| 9-10 | Excelente | Atende todos os requisitos, implementa diferenciais, código exemplar |
| 7-8 | Bom | Atende os requisitos principais, código organizado, poucas falhas |
| 5-6 | Satisfatório | Funciona parcialmente, organização básica, precisa de melhorias |
| 3-4 | Insuficiente | Muitas falhas, código desorganizado, requisitos principais incompletos |
| 0-2 | Eliminatório | Não funciona, plágio evidente, ou entrega vazia |

Nota mínima para aprovação: 6.0

### Diferenciação Júnior vs Pleno

| Aspecto | Júnior (esperado) | Pleno (esperado) |
|---------|-------------------|------------------|
| Funcionalidades | Obrigatórias funcionando | Obrigatórias + diferenciais |
| Código | Organizado e legível | Bem estruturado, com patterns claros |
| Erros | Tratamento básico | Tratamento completo com mensagens claras |
| Testes | Unitários básicos | Unitários + integração |
| Banco de dados | Modelagem funcional | Modelagem otimizada, queries elaboradas |
| Infraestrutura | Roda localmente | Docker Compose completo, noções de CI/CD |
