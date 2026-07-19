# Criação de Skills — Refatoração Arquitetural Automatizada

Ao longo do curso você aprendeu o que são Skills e como elas permitem que um agente de IA atue como um especialista em tarefas específicas. Agora imagine o seguinte cenário: você herdou 3 projetos legados com problemas de arquitetura, segurança e qualidade de código. Revisar e corrigir tudo manualmente levaria dias.

Neste desafio, você vai criar uma Skill que automatiza esse processo — analisando, auditando e refatorando qualquer projeto para o padrão MVC, independente da tecnologia.

## Objetivo

Você deve entregar uma Skill capaz de:

- Analisar uma codebase detectando linguagem, framework e arquitetura atual
- Identificar anti-patterns e code smells, classificando por severidade com arquivo e linha exatos
- Gerar um relatório de auditoria estruturado com todos os achados
- Refatorar o projeto para o padrão MVC (Model-View-Controller), eliminando os problemas encontrados
- Validar o resultado garantindo que a aplicação continua funcionando após as mudanças

A skill deve ser agnóstica de tecnologia, funcionando com diferentes linguagens e frameworks.

## Contexto

### Definição de Severidades

Para padronizar a sua auditoria e os relatórios gerados pela IA, utilize a seguinte escala de classificação baseada em problemas de MVC e SOLID:

- **CRITICAL:** Falhas graves de arquitetura ou segurança que impedem o funcionamento correto, expõem dados sensíveis (ex: credenciais hardcoded, SQL Injection) ou violam completamente a separação de responsabilidades (ex: "God Class" contendo banco de dados, lógicas complexas e roteamento no mesmo arquivo).
- **HIGH:** Fortes violações do padrão MVC ou princípios SOLID que dificultam muito a manutenção e testes (ex: lógicas de negócio pesadas presas dentro de Controllers, forte acoplamento sem Injeção de Dependência, ou uso de estado global mutável em toda a aplicação).
- **MEDIUM:** Problemas de padronização, duplicação de código ou gargalos de performance moderada (ex: Queries N+1 no banco de dados, uso inadequado de middlewares, validações ausentes nas rotas).
- **LOW:** Melhorias de legibilidade, nomenclatura de variáveis ruins, ou "magic numbers" soltos pelo código.

### Exemplo de Uso no CLI

```bash
# Executar a skill no projeto com problemas
cd code-smells-project
claude "/refactor-arch"
```

```
================================
PHASE 1: PROJECT ANALYSIS
================================
Language:      Python
Framework:      Flask 3.1.1
Dependencies:  flask-cors
Domain:        E-commerce API (produtos, pedidos, usuários)
Architecture:  Monolítica — tudo em 4 arquivos, sem separação de camadas
Source files:  4 files analyzed
DB tables:     produtos, usuarios, pedidos, itens_pedido
================================
```

```
================================
ARCHITECTURE AUDIT REPORT
================================
Project: code-smells-project
Stack:   Python + Flask
Files:   4 analyzed | ~800 lines of code

## Summary
CRITICAL: 4 | HIGH: 5 | MEDIUM: 2 | LOW: 3

## Findings

### [CRITICAL] God Class / God Method
File: models.py:1-350
Description: Arquivo único contém toda lógica de negócio, queries SQL, validação e formatação para 4 domínios diferentes.
Impact: Impossível testar em isolamento, qualquer mudança afeta tudo.
Recommendation: Separar em models e controllers por domínio.

### [CRITICAL] Hardcoded Credentials
File: app.py:8
Description: SECRET_KEY hardcoded como 'minha-chave-super-secreta-123'
...

================================
Total: 14 findings
================================

Phase 2 complete. Proceed with refactoring (Phase 3)? [y/n]
> y
```

```
[... refatoração executada ...]

================================
PHASE 3: REFACTORING COMPLETE
================================
## New Project Structure
src/
├── config/settings.py
├── models/
│   ├── produto_model.py
│   └── usuario_model.py
├── views/
│   └── routes.py
├── controllers/
│   ├── produto_controller.py
│   └── pedido_controller.py
├── middlewares/error_handler.py
└── app.py (composition root)

## Validation
  ✓ Application boots without errors
  ✓ All endpoints respond correctly
  ✓ Zero anti-patterns remaining
================================
```

## Tecnologias obrigatórias

- **Ferramenta:** uma das três opções abaixo (não são aceitas outras ferramentas):
  - Claude Code
  - Gemini CLI
  - OpenAI Codex
- **Recurso:** Custom Skills (ou o equivalente na ferramenta escolhida)
- **Formato dos arquivos de referência:** Markdown
- **Projetos-alvo:** Python/Flask (2 projetos) e Node.js/Express (1 projeto) (fornecidos no repositório base)

> **Nota sobre a ferramenta:** Os exemplos deste documento usam o Claude Code (`.claude/skills/`) como referência, pois é a ferramenta utilizada no curso. Se você optar por Gemini CLI ou Codex, adapte o nome da pasta e o comando de invocação conforme a convenção dela — o conceito de skill e a estrutura interna (SKILL.md + arquivos de referência) permanecem os mesmos.

## Requisitos

### 1. Análise Manual dos Projetos

Antes de criar a skill, você deve entender os problemas que ela vai resolver.

**Tarefas:**

- Analisar o projeto `code-smells-project/` (Python/Flask — API de E-commerce)
- Analisar o projeto `ecommerce-api-legacy/` (Node.js/Express — LMS API com fluxo de checkout)
- Analisar o projeto `task-manager-api/` (Python/Flask — API de Task Manager)

Para cada projeto, identificar e documentar no mínimo 5 problemas, incluindo pelo menos:

- 1 de severidade CRITICAL ou HIGH
- 2 de severidade MEDIUM
- 2 de severidade LOW

Documentar os achados na seção "Análise Manual" do seu `README.md`

> **Dica:** Não precisa encontrar todos os problemas — foque nos que têm maior impacto arquitetural. Use os projetos como insumo para entender quais padrões sua skill precisa detectar.

> **Por que 3 projetos?** Dois são Python/Flask (com níveis de organização diferentes) e um é Node.js/Express. Sua skill precisa funcionar nos 3 para provar que é verdadeiramente agnóstica de tecnologia — lidando tanto com código completamente desestruturado quanto com projetos que já possuem alguma separação de camadas.

### 2. Criação da Skill

Agora que você conhece os problemas, crie uma skill que os detecte, gere um relatório de auditoria e corrija automaticamente.

**Tarefas:**

Criar a skill dentro do projeto `code-smells-project/` e implementar o SKILL.md com 3 fases sequenciais:

- **Fase 1 — Análise:** Detectar stack, mapear arquitetura atual, imprimir resumo
- **Fase 2 — Auditoria:** Cruzar código contra catálogo de anti-patterns, gerar relatório, pedir confirmação
- **Fase 3 — Refatoração:** Reestruturar para o padrão MVC, validar que funciona

Criar arquivos de referência em Markdown que forneçam à skill o conhecimento necessário para executar as 3 fases. Os arquivos devem cobrir **obrigatoriamente** as seguintes áreas de conhecimento:

| Área de conhecimento      | O que deve conter                                                                                      |
| -------------------------- | ------------------------------------------------------------------------------------------------------ |
| Análise de projeto        | Heurísticas para detecção de linguagem, framework, banco de dados e mapeamento de arquitetura       |
| Catálogo de anti-patterns | Anti-patterns com sinais de detecção e classificação de severidade                                 |
| Template de relatório     | Formato padronizado do relatório de auditoria (Fase 2)                                                |
| Guidelines de arquitetura  | Regras do padrão MVC alvo (camadas Models, Views/Routes e Controllers, responsabilidades de cada uma) |
| Playbook de refatoração  | Padrões concretos de transformação para cada anti-pattern (com exemplos de código)                 |

> **Nota:** Você tem liberdade para organizar os arquivos de referência como preferir — pode usar os nomes e a quantidade de arquivos que fizer sentido para sua skill. O importante é que todas as 5 áreas de conhecimento estejam cobertas. O nome da skill (`refactor-arch`) e o arquivo `SKILL.md` são obrigatórios e não devem ser alterados. O path da skill segue a convenção da ferramenta escolhida (no Claude Code, por exemplo, é `.claude/skills/refactor-arch/`).

**Requisitos da skill:**

- Deve ser agnóstica de tecnologia — deve funcionar corretamente nos 3 projetos fornecidos, independente da stack ou nível de organização
- O catálogo de anti-patterns deve conter no mínimo 8 anti-patterns com severidade distribuída (CRITICAL, HIGH, MEDIUM, LOW)
- O catálogo deve incluir detecção de APIs deprecated — identificar uso de APIs obsoletas e recomendar o equivalente moderno
- O playbook deve ter no mínimo 8 padrões de transformação com exemplos de código antes/depois
- A Fase 2 deve pausar e pedir confirmação antes de modificar qualquer arquivo
- A Fase 3 deve validar o resultado (boot da aplicação + endpoints funcionando)

### 3. Execução da Skill

Execute sua skill nos 3 projetos e valide que ela funciona em todas as stacks.

#### Projeto 1 — code-smells-project (Python/Flask)

Invocar a skill no Claude Code:

```bash
claude "/refactor-arch"
```

> **Nota:** O comando acima é o exemplo com Claude Code. Se você estiver usando Gemini CLI ou Codex, utilize o comando equivalente para invocar uma skill na sua ferramenta.

- Verificar que a Fase 1 detecta corretamente a stack e imprime o resumo
- Verificar que a Fase 2 encontra no mínimo 5 dos problemas documentados na sua análise manual
- Confirmar a execução da Fase 3
- Verificar que a Fase 3:
  - Cria a estrutura de diretórios baseada em MVC
  - A aplicação inicia sem erros
  - Os endpoints originais continuam respondendo
- Salvar o relatório de auditoria (output da Fase 2) em `reports/audit-project-1.md`
- Commitar o código refatorado do projeto no repositório

#### Projeto 2 — ecommerce-api-legacy (Node.js/Express)

Prove que sua skill é reutilizável em outro projeto de backend, mas com stack diferente.

- Copiar a pasta `.claude/skills/refactor-arch/` para dentro de `ecommerce-api-legacy/`
- Invocar a skill:

```bash
cd ../ecommerce-api-legacy
claude "/refactor-arch"
```

- Verificar que as 3 fases executam corretamente neste projeto
- Salvar o relatório em `reports/audit-project-2.md`
- Commitar o código refatorado do projeto no repositório

#### Projeto 3 — task-manager-api (Python/Flask)

Agora o teste com um projeto Python/Flask que já possui alguma organização de camadas (models, routes, services, utils).

- Copiar a pasta `.claude/skills/refactor-arch/` para dentro de `task-manager-api/`
- Invocar a skill:

```bash
cd ../task-manager-api
claude "/refactor-arch"
```

- Verificar que:
  - A Fase 1 detecta corretamente Python/Flask como stack e identifica o domínio de Task Manager
  - A Fase 2 identifica problemas mesmo em um projeto parcialmente organizado
  - A Fase 3 melhora a estrutura sem quebrar a aplicação (todos os endpoints devem continuar respondendo)
- Salvar o relatório em `reports/audit-project-3.md`
- Commitar o código refatorado do projeto no repositório

> **Nota:** Este projeto já possui alguma separação de camadas, mas isso não significa que a arquitetura está adequada. A skill deve identificar tanto problemas de código (segurança, performance, qualidade) quanto oportunidades de melhoria arquitetural. Se houver mudanças estruturais necessárias, a skill deve propô-las e executá-las.

#### Validação

Para cada projeto refatorado, valide o seguinte checklist:

```markdown
## Checklist de Validação

### Fase 1 — Análise

- [ ] Linguagem detectada corretamente
- [ ] Framework detectado corretamente
- [ ] Domínio da aplicação descrito corretamente
- [ ] Número de arquivos analisados condiz com a realidade

### Fase 2 — Auditoria

- [ ] Relatório segue o template definido nos arquivos de referência
- [ ] Cada finding tem arquivo e linhas exatos
- [ ] Findings ordenados por severidade (CRITICAL → LOW)
- [ ] Mínimo de 5 findings identificados
- [ ] Detecção de APIs deprecated incluída (se aplicável)
- [ ] Skill pausa e pede confirmação antes da Fase 3

### Fase 3 — Refatoração

- [ ] Estrutura de diretórios segue padrão MVC
- [ ] Configuração extraída para módulo de config (sem hardcoded)
- [ ] Models criados para abstrair dados
- [ ] Views/Routes separadas para visualização ou roteamento
- [ ] Controllers concentram o fluxo da aplicação
- [ ] Error handling centralizado
- [ ] Entry point claro
- [ ] Aplicação inicia sem erros
- [ ] Endpoints originais respondem corretamente
```

> **Dica:** Se a skill não detectou problemas suficientes ou a refatoração falhou, ajuste os arquivos de referência e execute novamente. É normal precisar de 2-4 iterações.

## Entregável

Repositório público no GitHub (fork do repositório base) contendo:

- Skill completa em `.claude/skills/refactor-arch/` (dentro dos 3 projetos)
- Código refatorado dos 3 projetos (resultado da execução da Fase 3, commitado no repositório)
- Relatórios de auditoria em `reports/` (3 arquivos)
- `README.md` atualizado

### Estrutura do repositório

Faça um fork do repositório base contendo os três projetos com code smells.

> **Nota:** A estrutura abaixo usa Claude Code como exemplo (`.claude/skills/`). Se estiver usando outra ferramenta, adapte os caminhos conforme a convenção dela.

```
desafio-skills/
├── README.md                              # Sua documentação
│
├── code-smells-project/                   # Projeto 1 — Python/Flask (API de E-commerce)
│   ├── .claude/
│   │   └── skills/
│   │       └── refactor-arch/             # ← SUA SKILL AQUI
│   │           ├── SKILL.md
│   │           └── (arquivos de referência)
│   ├── app.py
│   ├── controllers.py
│   ├── models.py
│   ├── database.py
│   └── requirements.txt
│
├── ecommerce-api-legacy/                  # Projeto 2 — Node.js/Express (LMS API com checkout)
│   ├── .claude/
│   │   └── skills/
│   │       └── refactor-arch/             # ← CÓPIA DA SKILL
│   │           └── ...
│   ├── src/
│   │   ├── app.js
│   │   ├── AppManager.js
│   │   └── utils.js
│   ├── api.http
│   └── package.json
│
├── task-manager-api/                      # Projeto 3 — Python/Flask (API de Task Manager)
│   ├── .claude/
│   │   └── skills/
│   │       └── refactor-arch/             # ← CÓPIA DA SKILL
│   │           └── ...
│   ├── app.py
│   ├── database.py
│   ├── seed.py
│   ├── requirements.txt
│   ├── models/
│   ├── routes/
│   ├── services/
│   └── utils/
│
└── reports/                               # Relatórios gerados
    ├── audit-project-1.md                 # Saída da Fase 2 no projeto 1
    ├── audit-project-2.md                 # Saída da Fase 2 no projeto 2
    └── audit-project-3.md                 # Saída da Fase 2 no projeto 3
```

**O que você vai criar:**

- `.claude/skills/refactor-arch/` — A skill completa (SKILL.md + arquivos de referência)
- Código refatorado dos 3 projetos — resultado da execução da Fase 3, commitado no repositório
- `reports/audit-project-{1,2,3}.md` — Relatório de auditoria de cada projeto
- `README.md` — Documentação do seu processo

**O que já vem pronto:**

- `code-smells-project/` — API de E-commerce Python/Flask com code smells intencionais
- `ecommerce-api-legacy/` — LMS API Node.js/Express (com fluxo de checkout) e problemas de implementação
- `task-manager-api/` — API de Task Manager Python/Flask com organização parcial e problemas de segurança/qualidade

> **Dica:** Cada projeto contém problemas intencionais de diferentes severidades (CRITICAL, HIGH, MEDIUM, LOW), incluindo falhas de segurança, violações arquiteturais e problemas de qualidade de código. Parte do desafio é identificá-los por conta própria através da análise manual do código.

### README.md deve conter

**A) Seção "Análise Manual":**

- Lista dos problemas identificados manualmente em cada projeto
- Classificação por severidade
- Justificativa de por que cada problema é relevante

**B) Seção "Construção da Skill":**

- Decisões de design: como estruturou o SKILL.md e os arquivos de referência
- Quais anti-patterns incluiu no catálogo e por quê
- Como garantiu que a skill é agnóstica de tecnologia
- Desafios encontrados e como resolveu

**C) Seção "Resultados":**

- Resumo dos relatórios de auditoria dos 3 projetos (quantos findings por severidade em cada)
- Comparação antes/depois da estrutura de cada projeto
- Checklist de validação preenchido para cada projeto
- Screenshots ou logs mostrando as aplicações rodando após refatoração
- Observações sobre como a skill se comportou em stacks diferentes

**D) Seção "Como Executar":**

- Pré-requisitos (a ferramenta escolhida — Claude Code, Gemini CLI ou Codex — instalada e configurada)
- Comandos para executar a skill em cada projeto
- Como validar que a refatoração funcionou

### Ordem de execução sugerida

**1. Analisar os projetos manualmente**

Leia o código dos três projetos e documente os problemas encontrados.

**2. Criar a skill**

Escreva o SKILL.md e os arquivos de referência.

**3. Executar nos 3 projetos**

```bash
# Projeto 1
cd code-smells-project
claude "/refactor-arch"

# Projeto 2
cd ../ecommerce-api-legacy
claude "/refactor-arch"

# Projeto 3
cd ../task-manager-api
claude "/refactor-arch"
```

Salve a saída da Fase 2 de cada projeto em `reports/audit-project-{1,2,3}.md`.

**4. Iterar**

Se a skill não detectou problemas suficientes ou a refatoração falhou, ajuste os arquivos de referência e execute novamente. É normal precisar de 2-4 iterações.

## Critérios de Aceite

A skill deve atingir os seguintes mínimos em **todos os 3 projetos**:

| Critério                                       | Requisito                   |
| ----------------------------------------------- | --------------------------- |
| Fase 1 detecta stack corretamente               | OBRIGATÓRIO (3/3 projetos) |
| Fase 2 encontra >= 5 findings                   | OBRIGATÓRIO (3/3 projetos) |
| Fase 2 inclui pelo menos 1 CRITICAL ou HIGH     | OBRIGATÓRIO (3/3 projetos) |
| Fase 3 aplicação funciona após refatoração | OBRIGATÓRIO (3/3 projetos) |

**IMPORTANTE:** Todos os critérios devem ser atingidos nos 3 projetos, não apenas em um!

> **Sobre o projeto 3 (task-manager-api):** Este projeto já possui alguma organização. "aplicação funciona" significa que a API inicia sem erros e todos os endpoints continuam respondendo corretamente.

## Referências

- [Claude Code: Skills](https://docs.anthropic.com/en/docs/claude-code/skills) — Documentação oficial sobre como criar e estruturar Skills
- [Claude Code: Overview](https://docs.anthropic.com/en/docs/claude-code/overview) — Visão geral do Claude Code e suas capacidades
- [The Complete Guide to Building Skills for Claude (PDF)](https://resources.anthropic.com/hubfs/The-Complete-Guide-to-Building-Skill-for-Claude.pdf) — Guia completo da Anthropic sobre construção de Skills
- [Equipping Agents for the Real World with Agent Skills](https://claude.com/blog/equipping-agents-for-the-real-world-with-agent-skills) — Blog oficial da Anthropic sobre Agent Skills

---

## Dicas Finais

- **Comece pela análise manual** — entender os problemas profundamente é essencial para criar uma skill que os detecte.
- **O SKILL.md é um prompt** — ele instrui o agente sobre o que fazer, enquanto os arquivos de referência fornecem o conhecimento de domínio.
- **Seja específico nos sinais de detecção** — "código ruim" não ajuda; "query SQL dentro de loop for" é acionável.
- **Teste incrementalmente** — não tente criar a skill perfeita de primeira.
- **A skill deve ser copiável** — se ela só funciona em um projeto específico, está acoplada demais. Teste nos 3 projetos para validar.
- **Projetos diferentes exigem adaptação** — a Fase 3 de um projeto já parcialmente organizado não vai ter as mesmas transformações de um monolito. Sua skill deve se adaptar ao contexto.
- **Pedir confirmação na Fase 2 é obrigatório** — o humano deve revisar o relatório antes de qualquer modificação.
- **Consulte as referências do curso** — revise a documentação oficial da ferramenta escolhida e os materiais das aulas para relembrar a estrutura e anatomia de uma skill.
- [Equipping Agents for the Real World with Agent Skills](https://claude.com/blog/equipping-agents-for-the-real-world-with-agent-skills) — Blog oficial da Anthropic sobre Agent Skills



# Resposta ao Desafio

---

## Criação de Skills — Refatoração Arquitetural Automatizada

> **Autor:** Thuurzz (Arthur Vincius)
> **Ferramenta:** Codex
> **Data:** Julho/2026

---

## A) Análise Manual

Análise detalhada dos 3 projetos-alvo, identificando problemas de arquitetura, segurança e qualidade de código.

---

### Projeto 1: `code-smells-project` (Python/Flask — API de E-commerce)

**Stack:** Python 3 + Flask 3.1.1 + SQLite (raw queries)
**Arquitetura atual:** Monolito — 4 arquivos sem separação de camadas
**Domínio:** E-commerce (produtos, usuários, pedidos, relatórios)

| #  | Severidade         | Arquivo:Linha                                     | Problema                                                                                                                                                                     | Justificativa                                                                                                         |
| -- | ------------------ | ------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| 1  | **CRITICAL** | `models.py:1-350`                               | **God Class** — Arquivo único contém toda lógica de negócio, queries SQL, validação e formatação para 4 domínios (produtos, usuários, pedidos, relatórios) | Viola SRP (Single Responsibility Principle). Impossível testar isoladamente. Qualquer mudança afeta tudo.           |
| 2  | **CRITICAL** | `models.py:28,48,58,95,108,130,175,195,280,295` | **SQL Injection em TODAS as queries** — Concatenação direta de strings do usuário nas queries (`"SELECT * FROM produtos WHERE id = " + str(id)`)                 | Permite que um atacante execute SQL arbitrário no banco. Ex:`1; DROP TABLE produtos;--`                            |
| 3  | **CRITICAL** | `app.py:68-82`                                  | **Backdoor de SQL Injection** — Rota `/admin/query` permite executar SQL arbitrário via POST                                                                       | Um endpoint público que aceita qualquer query SQL é um desastre de segurança. Equivale a dar acesso root ao banco. |
| 4  | **CRITICAL** | `app.py:8`                                      | **Hardcoded Secret Key** — `SECRET_KEY = "minha-chave-super-secreta-123"`                                                                                           | Chave criptográfica exposta no código-fonte. Se o repositório for público, qualquer um pode forjar sessões.      |
| 5  | **HIGH**     | `models.py:95-108`                              | **Senhas em plaintext** — Senhas armazenadas e comparadas sem hash (`WHERE email = '...' AND senha = '...'`)                                                        | Senhas dos usuários ficam expostas no banco. Se houver vazamento, todas as contas são comprometidas.                |
| 6  | **HIGH**     | `controllers.py:280-295`                        | **Health check vaza dados sensíveis** — `/health` retorna `secret_key`, `db_path`, `debug`, `ambiente`                                                     | Expõe informações críticas de configuração que facilitam ataques direcionados.                                  |
| 7  | **HIGH**     | `controllers.py:30-60`                          | **Lógica de negócio no Controller** — Validações de preço, estoque, categorias válidas estão nos controllers                                                   | Viola o princípio MVC: controllers devem orquestrar, não conter regras de negócio.                                 |
| 8  | **HIGH**     | `app.py:9,92`                                   | **Debug=True em produção** — `app.config["DEBUG"] = True` e `app.run(debug=True)`                                                                               | Modo debug expõe stack traces completos e permite execução de código arbitrário via console Werkzeug.            |
| 9  | **MEDIUM**   | `models.py:175-230`                             | **N+1 Query Problem** — `get_pedidos_usuario` e `get_todos_pedidos` fazem queries dentro de loops (cursor2, cursor3)                                              | Para N pedidos, são executadas N×M queries adicionais. Performance degrada exponencialmente.                        |
| 10 | **MEDIUM**   | `controllers.py:30-60 vs 70-95`                 | **Duplicação de código** — Validações de `criar_produto` repetidas em `atualizar_produto`                                                                    | Viola DRY. Mudanças precisam ser feitas em múltiplos lugares.                                                       |
| 11 | **MEDIUM**   | `controllers.py` (vários)                      | **Exceções genéricas expostas** — `except Exception as e: return jsonify({"erro": str(e)})`                                                                      | Expõe mensagens de erro internas (stack traces, paths) para o cliente.                                               |
| 12 | **LOW**      | `controllers.py:6, models.py:todo`              | **Print statements como logging** — Uso de `print()` em vez de módulo `logging`                                                                                  | Sem níveis de log, sem rotação, sem formato estruturado. Difícil depurar em produção.                           |
| 13 | **LOW**      | `models.py:2`                                   | **Import não utilizado** — `import sqlite3` (usa `get_db` do database.py)                                                                                        | Código morto que polui o namespace.                                                                                  |
| 14 | **LOW**      | `controllers.py:55-56`                          | **Magic numbers** — `len(nome) < 2`, `len(nome) > 200` sem constantes nomeadas                                                                                    | Dificulta manutenção. Se o limite mudar, precisa caçar todos os lugares.                                           |

**Resumo:** 4 CRITICAL · 4 HIGH · 3 MEDIUM · 3 LOW = **14 findings**

---

### Projeto 2: `ecommerce-api-legacy` (Node.js/Express — LMS API com Checkout)

**Stack:** Node.js + Express 4.18 + SQLite (sqlite3)
**Arquitetura atual:** Monolito com God Class — 3 arquivos, `AppManager.js` concentra tudo
**Domínio:** LMS (Learning Management System) com fluxo de checkout/pagamento

| #  | Severidade         | Arquivo:Linha             | Problema                                                                                                                                            | Justificativa                                                                                       |
| -- | ------------------ | ------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------- |
| 1  | **CRITICAL** | `utils.js:2-5`          | **Credenciais hardcoded** — `dbPass: "senha_super_secreta_prod_123"`, `paymentGatewayKey: "pk_live_..."`, credenciais SMTP               | Múltiplas credenciais de produção expostas no código. Se o repo for público, é catastrófico. |
| 2  | **CRITICAL** | `AppManager.js:48`      | **Log de dados de cartão de crédito** — `console.log(\`Processando cartão ${cc}...\`)` loga número completo do cartão                 | Viola PCI-DSS. Dados de cartão NUNCA devem ser logados.                                            |
| 3  | **CRITICAL** | `AppManager.js:1-130`   | **God Class** — `AppManager` contém init de banco, definição de rotas, lógica de checkout, relatórios financeiros, tudo em uma classe | Viola SRP completamente. 130 linhas com 4 responsabilidades distintas.                              |
| 4  | **HIGH**     | `utils.js:17-22`        | **Criptografia caseira (badCrypto)** — Função que faz loop 10000x concatenando base64 em vez de usar bcrypt/argon2                         | Hash frágil e previsível. Não usa salt. Fácil de quebrar com rainbow tables.                    |
| 5  | **HIGH**     | `AppManager.js:18`      | **Senha em plaintext no seed** — `INSERT INTO users ... VALUES ('Leonan', ..., '123')`                                                     | Senha '123' sem hash no banco. Usuário inicial vulnerável.                                        |
| 6  | **HIGH**     | `utils.js:8-9`          | **Estado global mutável** — `globalCache` e `totalRevenue` como variáveis globais                                                      | Viola imutabilidade e torna o comportamento imprevisível entre requisições.                      |
| 7  | **MEDIUM**   | `AppManager.js:78-115`  | **Callback Hell + N+1 Query** — Relatório financeiro com 4 níveis de callbacks aninhados e queries em loops                                | Código ilegível e performance péssima. Para N cursos com M matrículas, são O(N×M) queries.    |
| 8  | **MEDIUM**   | `AppManager.js:120-124` | **Cascade delete ausente** — Ao deletar usuário, matrículas e pagamentos ficam órfãos no banco                                           | Inconsistência de dados. Registros órfãos sem integridade referencial.                           |
| 9  | **MEDIUM**   | `AppManager.js:49`      | **Validação de pagamento frágil** — `cc.startsWith("4")` como "validação" de cartão                                                  | Qualquer cartão começando com 4 (Visa) é aprovado. Nenhuma validação real.                     |
| 10 | **LOW**      | `AppManager.js:35-39`   | **Nomes de variáveis ilegíveis** — `u`, `e`, `p`, `cid`, `cc`                                                                    | Variáveis de uma letra prejudicam legibilidade e manutenção.                                     |
| 11 | **LOW**      | `AppManager.js:43,122`  | **Mensagens misturando idiomas** — "Bad Request", "Curso não encontrado", "Erro DB"                                                         | Inconsistência de i18n. Mistura português e inglês.                                              |

**Resumo:** 3 CRITICAL · 3 HIGH · 3 MEDIUM · 2 LOW = **11 findings**

---

### Projeto 3: `task-manager-api` (Python/Flask — API de Task Manager)

**Stack:** Python 3 + Flask 3.0 + SQLAlchemy + Marshmallow
**Arquitetura atual:** Parcialmente organizada — já possui `models/`, `routes/`, `services/`, `utils/`
**Domínio:** Gerenciador de tarefas com usuários, categorias e relatórios

| #  | Severidade         | Arquivo:Linha                                                                                                | Problema                                                                                                                                                     | Justificativa                                                                              |
| -- | ------------------ | ------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------ |
| 1  | **CRITICAL** | `models/user.py:30-33`                                                                                     | **MD5 para hash de senhas** — `hashlib.md5(pwd.encode()).hexdigest()`                                                                               | MD5 é criptograficamente quebrado desde 2004. Deveria usar bcrypt, scrypt ou argon2.      |
| 2  | **CRITICAL** | `services/notification_service.py:8-11`                                                                    | **Credenciais SMTP hardcoded** — Email e senha do servidor de email no código                                                                        | Credenciais de serviço externo expostas. Permite envio de email como o sistema.           |
| 3  | **HIGH**     | `models/user.py:18-27`                                                                                     | **Senha exposta no `to_dict()`** — O método retorna o campo `password` (mesmo hasheado)                                                          | Expor o hash da senha na API é uma vulnerabilidade. Facilita ataques offline.             |
| 4  | **HIGH**     | `routes/task_routes.py`, `routes/user_routes.py`                                                         | **Lógica de negócio nas rotas** — Validações, regras de overdue, formatação estão nos route handlers                                           | Viola MVC. Rotas devem apenas receber requisições e delegar para services/controllers.   |
| 5  | **HIGH**     | `routes/user_routes.py:213`                                                                                | **Fake JWT token** — `'token': 'fake-jwt-token-' + str(user.id)`                                                                                    | Token falso sem assinatura criptográfica. Qualquer um pode forjar tokens.                 |
| 6  | **MEDIUM**   | `routes/task_routes.py:30-45, 75-85`, `routes/user_routes.py:170-185`, `routes/report_routes.py:40-50` | **Duplicação de lógica de overdue** — A mesma lógica `if due_date < utcnow()` repetida em 4 lugares                                             | Viola DRY. Se a regra de overdue mudar, precisa alterar em 4 arquivos diferentes.          |
| 7  | **MEDIUM**   | `routes/report_routes.py:68-80`                                                                            | **N+1 Query nos relatórios** — Loop sobre usuários fazendo queries adicionais para tasks                                                            | Para N usuários, são N+1 queries. Degradação de performance com escala.                |
| 8  | **MEDIUM**   | `utils/helpers.py` vs `routes/`                                                                          | **Utils definidas mas não utilizadas** — `process_task_data`, `validate_email`, `sanitize_string` existem mas as rotas reimplementam a lógica | Código morto e duplicação. As funções utilitárias foram criadas mas ninguém as usa. |
| 9  | **MEDIUM**   | `routes/task_routes.py:6`                                                                                  | **Imports não utilizados** — `import json, os, sys, time`                                                                                          | Polui o namespace e confunde sobre dependências reais.                                    |
| 10 | **LOW**      | `seed.py:20,26,32`                                                                                         | **Senhas fracas no seed** — `'1234'`, `'abcd'`, `'pass'`                                                                                        | Dados de exemplo com senhas triviais. Em produção, isso seria um problema.               |
| 11 | **LOW**      | `routes/task_routes.py:20-55`                                                                              | **Lógica de serialização manual** — Monta dicionário campo a campo em vez de usar `to_dict()` do model                                          | Duplica a lógica de serialização que já existe no modelo.                              |
| 12 | **LOW**      | `app.py:6`                                                                                                 | **Imports não utilizados** — `import os, sys, json, datetime` (datetime é usado, os outros não)                                                  | Código morto.                                                                             |

**Resumo:** 2 CRITICAL · 3 HIGH · 4 MEDIUM · 3 LOW = **12 findings**

---

### Comparativo entre projetos

| Projeto              | Stack           | Arquivos | CRITICAL | HIGH | MEDIUM | LOW | Total        |
| -------------------- | --------------- | -------- | -------- | ---- | ------ | --- | ------------ |
| code-smells-project  | Python/Flask    | 4        | 4        | 4    | 3      | 3   | **14** |
| ecommerce-api-legacy | Node.js/Express | 3        | 3        | 3    | 3      | 2   | **11** |
| task-manager-api     | Python/Flask    | 12       | 2        | 3    | 4      | 3   | **12** |

**Padrões recorrentes identificados:**

- **SQL Injection / credenciais hardcoded** — Presente em todos os projetos (CRITICAL)
- **God Class / violação SRP** — Presente nos projetos 1 e 2 (CRITICAL)
- **Senhas sem hash ou com hash fraco** — Presente em todos os projetos (CRITICAL/HIGH)
- **Lógica de negócio em controllers/routes** — Presente em todos os projetos (HIGH)
- **N+1 Query Problem** — Presente em todos os projetos (MEDIUM)
- **Duplicação de código** — Presente em todos os projetos (MEDIUM)
- **Print statements como logging** — Presente nos projetos Python (LOW)

---

## B) Construção da Skill

### Ferramenta: OpenAI Codex

A skill foi construída para o **OpenAI Codex CLI**, seguindo a convenção de diretórios `.agents/skills/<skill-name>/`.

### Estrutura da Skill

```
.agents/skills/refactor-arch/
├── SKILL.md                              # Entrypoint principal (YAML frontmatter + instruções)
├── agents/
│   └── openai.yaml                       # Metadata (display_name, description, policy)
└── references/
    ├── project-analysis.md               # Heurísticas de detecção de stack e arquitetura
    ├── anti-patterns-catalog.md          # Catálogo com 21 anti-patterns + sinais de detecção
    ├── report-template.md                # Template padronizado do relatório de auditoria
    ├── mvc-guidelines.md                 # Regras do padrão MVC alvo (6 camadas)
    └── refactoring-playbook.md           # 12 padrões de transformação com before/after
```

### Decisões de Design

**1. SKILL.md como orquestrador**

O `SKILL.md` é o ponto de entrada que define o fluxo das 3 fases. Ele instrui o agente sobre **o que fazer** em cada fase, enquanto os arquivos em `references/` fornecem **o conhecimento de domínio** necessário. Essa separação segue o princípio de que o prompt principal deve ser procedural (passos) e os references devem ser declarativos (conhecimento).

**2. YAML frontmatter obrigatório**

Seguindo a especificação do Codex, o `SKILL.md` inclui frontmatter YAML com `name` e `description`. O campo `description` funciona como trigger — o Codex usa ele para decidir quando invocar a skill. A descrição foi escrita para ser específica o suficiente para não disparar em contextos errados.

**3. 5 arquivos de referência cobrindo as 5 áreas obrigatórias**

| Arquivo                      | Área                      | Conteúdo                                                                              |
| ---------------------------- | -------------------------- | -------------------------------------------------------------------------------------- |
| `project-analysis.md`      | Análise de projeto        | Heurísticas para detectar 8+ linguagens, frameworks, bancos e padrões de arquitetura |
| `anti-patterns-catalog.md` | Catálogo de anti-patterns | 21 anti-patterns com sinais de detecção, severidade e recomendações                |
| `report-template.md`       | Template de relatório     | Formato exato do output da Fase 2 com regras de ordenação e exemplos                 |
| `mvc-guidelines.md`        | Guidelines de arquitetura  | Definição das 6 camadas MVC com exemplos Python e Node.js                            |
| `refactoring-playbook.md`  | Playbook de refatoração  | 12 padrões de transformação com código antes/depois em Python e JavaScript         |

**4. Agnosticismo de tecnologia**

A skill é agnóstica por design:

- O `project-analysis.md` cobre heurísticas para 8+ linguagens (Python, JS, Ruby, PHP, Go, Java, Rust, C#)
- O `anti-patterns-catalog.md` descreve sinais de detecção em termos genéricos (ex: "string concatenation in SQL queries" em vez de "f-strings in Python")
- O `refactoring-playbook.md` fornece exemplos before/after em **Python e JavaScript** para cada padrão
- O `mvc-guidelines.md` mostra estruturas de diretório para Flask e Express

### Anti-Patterns Incluídos no Catálogo

| #  | ID     | Nome                                 | Severidade |
| -- | ------ | ------------------------------------ | ---------- |
| 1  | AP-001 | SQL Injection                        | CRITICAL   |
| 2  | AP-002 | Hardcoded Credentials / Secrets      | CRITICAL   |
| 3  | AP-003 | God Class / God Module               | CRITICAL   |
| 4  | AP-004 | Plaintext Password Storage           | CRITICAL   |
| 5  | AP-005 | Weak Cryptographic Hashing           | CRITICAL   |
| 6  | AP-006 | Logging Sensitive Data               | CRITICAL   |
| 7  | AP-007 | Business Logic in Routes/Controllers | HIGH       |
| 8  | AP-008 | Debug Mode in Production             | HIGH       |
| 9  | AP-009 | Global Mutable State                 | HIGH       |
| 10 | AP-010 | Missing Authentication / Fake Auth   | HIGH       |
| 11 | AP-011 | Information Leakage in Responses     | HIGH       |
| 12 | AP-012 | N+1 Query Problem                    | MEDIUM     |
| 13 | AP-013 | Code Duplication                     | MEDIUM     |
| 14 | AP-014 | Missing Cascade / Orphaned Records   | MEDIUM     |
| 15 | AP-015 | Unused Code / Dead Code              | MEDIUM     |
| 16 | AP-016 | Generic Exception Handling           | MEDIUM     |
| 17 | AP-017 | Deprecated APIs                      | MEDIUM     |
| 18 | AP-018 | Print Statements as Logging          | LOW        |
| 19 | AP-019 | Magic Numbers / Magic Strings        | LOW        |
| 20 | AP-020 | Poor Variable Naming                 | LOW        |
| 21 | AP-021 | Missing Input Validation             | LOW        |

**Distribuição:** 6 CRITICAL · 5 HIGH · 6 MEDIUM · 4 LOW = **21 anti-patterns**

### Padrões de Transformação no Playbook

| #  | Padrão                                           | Anti-Pattern   |
| -- | ------------------------------------------------- | -------------- |
| 1  | Fix SQL Injection → Parameterized Queries        | AP-001         |
| 2  | Extract Hardcoded Config → Environment Variables | AP-002         |
| 3  | Split God Class → Domain Models + Controllers    | AP-003         |
| 4  | Hash Passwords Properly (bcrypt)                  | AP-004, AP-005 |
| 5  | Move Business Logic from Routes → Controllers    | AP-007         |
| 6  | Fix N+1 Queries → JOINs / Eager Loading          | AP-012         |
| 7  | Centralize Error Handling                         | AP-016         |
| 8  | Replace Print/Console.log → Structured Logging   | AP-018         |
| 9  | Extract Magic Numbers → Named Constants          | AP-019         |
| 10 | Remove Sensitive Data from API Responses          | AP-011         |
| 11 | Fix Deprecated APIs                               | AP-017         |
| 12 | Add Input Validation Layer                        | AP-021         |

### Desafios e Soluções

**Desafio 1: Tornar a detecção agnóstica de tecnologia**

Solução: Em vez de hardcodar padrões específicos de Python ou JavaScript, o catálogo descreve **sinais de detecção genéricos** (ex: "string concatenation in SQL queries" funciona para `+`, `f""`, template literals, etc.) e fornece exemplos em múltiplas linguagens.

**Desafio 2: Balancear especificidade vs generalidade no SKILL.md**

Solução: O SKILL.md contém a estrutura procedural (o fluxo das 3 fases) e delega o conhecimento detalhado para os arquivos de referência. Isso permite que o prompt principal seja conciso enquanto os references são ricos em detalhes.

**Desafio 3: Adaptar a refatoração para projetos já parcialmente organizados**

Solução: O `project-analysis.md` classifica a arquitetura em 4 níveis (Monolithic, Partially Organized, Layered, MVC-like). A Fase 3 adapta as transformações com base nessa classificação — um projeto monolítico precisa de reestruturação completa, enquanto um parcialmente organizado precisa de ajustes pontuais.

**Desafio 4: Convenção do Codex vs Claude Code**

Solução: A estrutura de diretórios foi adaptada de `.claude/skills/` para `.agents/skills/` seguindo a convenção do Codex. O `SKILL.md` usa YAML frontmatter com `name` e `description` (formato Codex) em vez de markdown puro. O arquivo `agents/openai.yaml` fornece metadata adicional específica do Codex.

---

## C) Resultados

### Resumo dos Relatórios de Auditoria

| Projeto                   | Stack                | Arquivos Originais | CRITICAL | HIGH | MEDIUM | LOW | **Total** |
| ------------------------- | -------------------- | ------------------ | -------- | ---- | ------ | --- | --------------- |
| 1 — code-smells-project  | Python/Flask 3.1.1   | 4                  | 6        | 5    | 5      | 3   | **19**    |
| 2 — ecommerce-api-legacy | Node.js/Express 4.18 | 3                  | 5        | 3    | 4      | 4   | **16**    |
| 3 — task-manager-api     | Python/Flask 3.0     | 15                 | 6        | 4    | 5      | 2   | **17**    |

**Total geral: 52 findings em 3 projetos**

---

### Projeto 1 — code-smells-project (Python/Flask)

**Antes:** Monolito com 4 arquivos (~780 linhas) — `app.py`, `models.py`, `controllers.py`, `database.py`

**Depois:** Estrutura MVC com 25 arquivos em `src/`

```
src/
├── config/settings.py              # Config por env vars
├── models/                         # product, user, order (domain-specific)
├── controllers/                    # product, user, order, system
├── routes/                         # product, user, order, system
├── middlewares/error_handler.py    # Centralized error handling
└── services/                       # auth, validation, notification
```

**Destaques da refatoração:**

- SQL Injection corrigido → todas queries usam parâmetros `?`
- Endpoint `/admin/query` (backdoor SQL) removido
- `SECRET_KEY` extraída para `config/settings.py` via env vars
- Senhas migradas para hash seguro (Werkzeug)
- `debug=True` removido, servidor `waitress` em produção
- Health check não vaza mais `secret_key`, `db_path`, `debug`
- N+1 queries substituídas por JOINs
- `print()` substituído por `logging`

**Validação:**

- ✅ App inicia sem erros (`python app.py`)
- ✅ Todos os endpoints originais respondem (`/`, `/health`, `/produtos`, `/usuarios`, `/pedidos`, `/login`, `/relatorios/vendas`)
- ✅ Zero anti-patterns restantes

---

### Projeto 2 — ecommerce-api-legacy (Node.js/Express)

**Antes:** God Class com 3 arquivos (~183 linhas) — `app.js`, `AppManager.js`, `utils.js`

**Depois:** Estrutura MVC com 24 arquivos em `src/`

```
src/
├── config/                         # constants, database, index (env vars)
├── models/                         # user, course, enrollment, payment, audit-log, report
├── controllers/                    # checkout, admin, user
├── routes/                         # checkout, admin, user
├── middlewares/                    # errorHandler, auth (JWT), async-handler
└── services/                       # password (scrypt), payment, logger, http-error
```

**Destaques da refatoração:**

- Credenciais hardcoded (`dbPass`, `paymentGatewayKey`, SMTP) → env vars
- Log de número de cartão completo removido (PCI-DSS)
- `badCrypto` caseiro → `crypto.scryptSync` com salt
- Senha `'123'` no seed → hash seguro
- `globalCache` e `totalRevenue` (estado global) removidos
- Callback hell + N+1 → JOIN único no relatório financeiro
- Cascade delete implementado (FKs com `ON DELETE CASCADE`)
- Admin routes protegidas com `x-admin-token`

**Validação:**

- ✅ App inicia sem erros
- ✅ `POST /api/checkout` → 200 (Visa) / 400 (recusado)
- ✅ `GET /api/admin/financial-report` → 200 com auth
- ✅ `DELETE /api/users/1` → 200 com cascade cleanup
- ✅ Zero anti-patterns restantes

---

### Projeto 3 — task-manager-api (Python/Flask)

**Antes:** Parcialmente organizado com 15 arquivos (~1200 linhas) — `models/`, `routes/`, `services/`, `utils/`

**Depois:** Estrutura MVC refinada com 35 arquivos em `src/`

```
src/
├── config/settings.py
├── controllers/                    # task, user, category, report
├── models/                         # task, user, category
├── routes/                         # task, user, category, report, system
├── middlewares/                    # auth (JWT real), error_handler
└── services/                       # auth, validation, serialization, notification, datetime, logging
```

**Destaques da refatoração:**

- MD5 → Werkzeug (hash seguro com salt)
- Senha removida do `to_dict()` (não vaza mais hash na API)
- Fake JWT (`'fake-jwt-token-' + id`) → token real com assinatura + middleware
- `datetime.utcnow()` → `datetime.now(UTC)` (API deprecated)
- SMTP credentials → env vars
- Lógica de overdue duplicada em 4 lugares → centralizada no controller
- N+1 queries nos relatórios → eager loading / JOINs
- `utils/helpers.py` não utilizado → removido, funções movidas para services
- `print()` → `logging`

**Validação:**

- ✅ App inicia sem erros
- ✅ Todos os endpoints originais respondem
- ✅ Zero anti-patterns restantes

---

### Checklist de Validação

| Critério                           | Proj 1 | Proj 2 | Proj 3 |
| ----------------------------------- | :----: | :----: | :----: |
| **Fase 1 — Análise**        |        |        |        |
| Linguagem detectada corretamente    |   ✅   |   ✅   |   ✅   |
| Framework detectado corretamente    |   ✅   |   ✅   |   ✅   |
| Domínio descrito corretamente      |   ✅   |   ✅   |   ✅   |
| Arquivos analisados condizem        |   ✅   |   ✅   |   ✅   |
| **Fase 2 — Auditoria**       |        |        |        |
| Relatório segue o template         |   ✅   |   ✅   |   ✅   |
| Findings com arquivo e linha exatos |   ✅   |   ✅   |   ✅   |
| Ordenação CRITICAL → LOW         |   ✅   |   ✅   |   ✅   |
| ≥ 5 findings                       | ✅ 19 | ✅ 16 | ✅ 17 |
| APIs deprecated detectadas          |   ✅   |   ✅   |   ✅   |
| Pausa e confirmação               |   ✅   |   ✅   |   ✅   |
| **Fase 3 — Refatoração**   |        |        |        |
| Estrutura MVC                       |   ✅   |   ✅   |   ✅   |
| Config extraída (sem hardcoded)    |   ✅   |   ✅   |   ✅   |
| Models por domínio                 |   ✅   |   ✅   |   ✅   |
| Routes separadas                    |   ✅   |   ✅   |   ✅   |
| Controllers com lógica de negócio |   ✅   |   ✅   |   ✅   |
| Error handling centralizado         |   ✅   |   ✅   |   ✅   |
| Entry point claro                   |   ✅   |   ✅   |   ✅   |
| App inicia sem erros                |   ✅   |   ✅   |   ✅   |
| Endpoints originais respondem       |   ✅   |   ✅   |   ✅   |

---

### Observações sobre Stacks Diferentes

- **Python/Flask (projetos 1 e 3):** A skill adaptou-se bem a ambos os níveis de organização — reestruturação completa no monolito e refinamento cirúrgico no projeto parcialmente organizado. No projeto 3, preservou a estrutura existente de `models/` e `routes/` enquanto adicionou `controllers/` e `middlewares/`.
- **Node.js/Express (projeto 2):** A skill traduziu corretamente os padrões MVC para o ecossistema Node — models como classes com métodos estáticos, controllers async, middlewares Express, e serviços com injeção. O relatório usou terminologia JavaScript (callback hell, `console.log`, `process.env`).
- **Ponto de atenção:** O Codex CLI requer `allow_implicit_invocation: true` no `agents/openai.yaml` para carregar a skill automaticamente. Com `false`, a skill é ignorada e o agente faz uma refatoração genérica sem seguir as 3 fases.

---

## D) Como Executar

### Pré-requisitos

- **OpenAI Codex CLI** instalado e configurado
  ```bash
  npm install -g @openai/codex
  codex login
  ```
- Python 3.10+ (para os projetos Flask)
- Node.js 18+ (para o projeto Express)

### Executando a Skill

A skill está localizada em `.agents/skills/refactor-arch/` dentro de cada projeto. Para invocá-la com o Codex:

```bash
# Projeto 1 — Python/Flask (E-commerce)
cd code-smells-project
codex "/refactor-arch"

# Projeto 2 — Node.js/Express (LMS API)
cd ../ecommerce-api-legacy
codex "/refactor-arch"

# Projeto 3 — Python/Flask (Task Manager)
cd ../task-manager-api
codex "/refactor-arch"
```

### Validando a Refatoração

**Projeto 1 (code-smells-project):**

```bash
cd code-smells-project
pip install -r requirements.txt
python app.py
# Testar: curl http://localhost:5000/health
```

**Projeto 2 (ecommerce-api-legacy):**

```bash
cd ecommerce-api-legacy
npm install
npm start
# Testar: curl http://localhost:3000/
```

**Projeto 3 (task-manager-api):**

```bash
cd task-manager-api
pip install -r requirements.txt
python seed.py
python app.py
# Testar: curl http://localhost:5000/health
```
