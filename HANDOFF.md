# HANDOFF.md

Estado da entrega em 2026-08-05, após a sessão local com `git` e `gh`
autenticado.

Este documento substitui a versão anterior, que registrava a publicação como
dependência humana. **A infraestrutura foi publicada e configurada pelo
agente.** O que permanece pendente são os exercícios, que pertencem aos
humanos.

## 1. Estrutura pronta — executado e verificado

### 1.1 Repositório

| Item | Valor |
| --- | --- |
| Repositório | https://github.com/fabianomag/framework-devops-sandbox |
| Visibilidade | público |
| Branch padrão | `main` |
| Commits em `main` | 1 (commit-base) |
| Actions | https://github.com/fabianomag/framework-devops-sandbox/actions |

### 1.2 Configuração aplicada

| Item | Estado |
| --- | --- |
| Workflow `CI` reconhecido | sim |
| Workflow `Delivery` reconhecido | sim |
| Primeiro CI em `main` | verde |
| Ruleset `protect-main` | ativo, exigindo `test-python` |
| Ambiente `development` | criado, sem revisor |
| Ambiente `staging` | criado, revisor `@fabianomag` |
| Ambiente `production` | criado, revisor `@fabianomag` |
| Merge por squash | única estratégia habilitada |

Os valores confirmados por saída de comando estão na seção 5.

### 1.3 Arquivos

```text
framework-devops-sandbox/
├── AGENTS.md                                   regras de segurança e escopo
├── CLAUDE.md                                   hierarquia de autoridade
├── DEVOPS-LAB-SPEC.md                          especificação canônica
├── RUNBOOK.md                                  procedimento humano, passo a passo
├── ACESSOS-E-PAPEIS.md                         modelo de acessos e papéis
├── LAB-OWNER-DEVELOPER.md                      roteiro do treinamento a dois
├── DECISIONS.md                                decisões, desvios e superseded
├── BACKLOG-MELHORIAS.md                        o que ficou fora e por quê
├── APRESENTACAO-10-MIN.md                      roteiro cronometrado
├── HANDOFF.md                                  este arquivo
├── README.md
├── LICENSE                                     MIT
├── .gitignore
├── src/
│   ├── __init__.py
│   └── framework_demo.py                       CLI fictícia health/version
├── tests/
│   └── test_framework_demo.py
└── .github/
    ├── CODEOWNERS                              @fabianomag no conteúdo protegido
    ├── governance/
    │   ├── ruleset-protect-main.json           APLICADO
    │   └── ruleset-protect-main-with-reviewers.json   alvo, NÃO aplicado
    └── workflows/
        ├── ci.yml                              check obrigatório test-python
        └── delivery.yml                        build único, promoção e release
```

## 2. Correções feitas nesta sessão

| # | Correção | Como foi verificada |
| --- | --- | --- |
| 1 | `_github/` renomeado para `.github/` | `mv -n` por arquivo e `rmdir` nos diretórios vazios; `rm -rf` não usado. O `rmdir` só teria sucesso com os diretórios já vazios, o que prova que nada ficou para trás |
| 2 | SPEC, DECISIONS, HANDOFF e RUNBOOK atualizados | separam "estrutura pronta" de "exercícios não realizados"; decisões antigas marcadas `superseded` |
| 3 | `ACESSOS-E-PAPEIS.md` e `LAB-OWNER-DEVELOPER.md` criados | declaram o limite real de repositório pessoal e a inversão de papéis |
| 4 | `CODEOWNERS` declara `@fabianomag` | exigência de aprovação segue desligada, com os três passos de ativação documentados no próprio arquivo |
| 5 | `Delivery` corrigido | tag SemVer dispara; build único; mesmo artefato nos 3 ambientes; checksum e `SOURCE_COMMIT` conferidos em cada um; release ao final; dispatch para rollback sem criar release |
| 6 | Validação da origem com 5 provas | testada contra repositório de teste — ver seção 4 |
| 7 | Actions fixadas por SHA completo | cada SHA resolvido pela API e conferido contra a tag semver — ver seção 3 |
| 8 | Três ambientes configurados | sem branch/tag policy, por decisão registrada |

**A alegação de que a falha intencional já havia sido executada foi removida.**
Nenhuma falha intencional foi executada. Ela é o exercício da seção 3 do
`RUNBOOK.md` e pertence aos humanos.

## 3. Actions fixadas por SHA

Cada SHA foi resolvido pela API do GitHub, teve a existência do commit
confirmada e foi conferido contra a tag semver que apontava para ele.

| Action | SHA | Tag |
| --- | --- | --- |
| `actions/checkout` | `fbc6f3992d24b796d5a048ff273f7fcc4a7b6c09` | v5.1.0 |
| `actions/setup-python` | `a26af69be951a213d495a4c3e4e4022e16d87065` | v5.6.0 |
| `actions/upload-artifact` | `ea165f8d65b6e75b540449e92b4886f43607fa02` | v4.6.2 |
| `actions/download-artifact` | `634f93cb2916e3fdff6788551b99b062d0335ce0` | v5.0.0 |
| `softprops/action-gh-release` | `3bb12739c298aeb8a4eeaf626c5b8d85266b0e65` | v2.6.2 |

## 4. Evidência de validação local

Python 3.14.6, na raiz do projeto.

| Verificação | Resultado |
| --- | --- |
| `python3 -m unittest discover -s tests -v` | `Ran 1 test — OK` |
| `python3 -m compileall -q src tests` | sem erro |
| `python3 -m src.framework_demo health` | `{"status": "ok", "version": "0.1.0"}` |
| `python3 -m src.framework_demo version` | `0.1.0` |
| Build do artefato com os comandos do delivery | `framework-demo.pyz` gerado |
| `shasum -a 256 -c SHA256SUMS` | `framework-demo.pyz: OK` / `SOURCE_COMMIT: OK` |
| Artefato executável | `{"status": "ok", "version": "0.1.0"}` |
| Detecção de adulteração — byte alterado no `.pyz` | `framework-demo.pyz: FAILED` |
| Sintaxe dos dois workflows | válida |
| Sintaxe dos dois rulesets | válida |
| Pinning das Actions | 10 de 10 por SHA de 40 caracteres, cada uma com o comentário da versão |

### 4.1 Validação da origem, testada de fato

O script de verificação foi extraído do `delivery.yml` e executado contra um
repositório de teste que emula o `actions/checkout` por tag. Não basta que o
caminho feliz passe: o controle precisa **falhar** quando deve.

| Cenário | Esperado | Obtido |
| --- | --- | --- |
| Tag anotada, em `main` | passa | passa, com as 5 provas impressas |
| Tag anotada, em `main`, mais recente | passa | passa |
| Tag **leve** | falha | falha na prova 2: `is commit, not an annotated tag object` |
| Tag anotada **fora de `main`** | falha | falha na prova 5: `not reachable from main` |
| Tag inexistente | falha | falha na prova 2 |
| Nome fora do padrão SemVer | falha | falha na prova 1 |

A tag fora de `main` passa nas provas 1 a 4 e é barrada exatamente pela prova de
ancestralidade. O controle é exercido de fato, não por acidente.

## 5. Verificação final no remoto

Preenchido com a saída real dos comandos executados ao fim desta sessão — ver
seção 8.

## 6. Exercícios reservados aos humanos — não realizados

**O treinamento começa na criação da primeira branch.** Nada abaixo foi
executado:

| Exercício | Estado |
| --- | --- |
| Primeira branch | não realizado |
| Pull request | não realizado |
| Falha intencional e leitura do check vermelho | não realizado |
| Merge bloqueado pelo ruleset | não realizado |
| Correção, check verde e merge por squash | não realizado |
| Tags anotadas | não realizado |
| Releases | não realizado |
| Promoção em `staging` e `production` | não realizado |
| Rollback por `workflow_dispatch` | não realizado |
| Convite ao segundo participante | não realizado |
| Inversão de papéis | não realizado |

Condução: `LAB-OWNER-DEVELOPER.md`. Comandos: `RUNBOOK.md`, a partir da seção 3.

## 7. Bloqueios reais restantes

| # | Bloqueio | O que trava | Contorno |
| --- | --- | --- | --- |
| 1 | Não existe segundo participante | aprovação independente, `require_last_push_approval`, review de CODEOWNER, `prevent_self_review` | as quatro regras seguem desligadas e documentadas; o gate real hoje é o check `test-python` |
| 2 | Repositório pessoal tem só Owner e Collaborator | papéis granulares, times, dois administradores | exigiria criar uma organização, fora do escopo autorizado. Registrado em `ACESSOS-E-PAPEIS.md` §1 |
| 3 | Ambientes sem deployment branch/tag policy | nada, é decisão | o `Delivery` roda em tag na release e em `main` no rollback; nenhuma policy única cobre os dois sem bloquear um deles. Gate real é a aprovação humana |
| 4 | Aprovações manuais em `staging` e `production` | cada promoção para e espera | é o comportamento desejado, não um defeito |
| 5 | Terceira pessoa consentindo | exercício de remoção de acesso | fora do escopo, em `BACKLOG-MELHORIAS.md` |

Nenhum destes impede o treinamento de começar.

## 8. Verificação final executada

Esta seção é preenchida com a saída dos comandos de verificação ao fim da
publicação. Ver a mensagem final da sessão.
