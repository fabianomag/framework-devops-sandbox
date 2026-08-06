# DEVOPS-LAB-SPEC.md

Especificação canônica da implementação deste laboratório. Nada é implementado
fora dela. Sugestão adicional vai para `BACKLOG-MELHORIAS.md`.

Repositório autorizado: `Heveraldoo/framework-devops-sandbox`, público, MIT.

## 1. Objetivo

Demonstrar governança e fluxo de entrega no GitHub com um exemplo fictício e
mínimo, em uma jornada única:

```text
branch -> pull request -> testes -> merge protegido -> release
       -> promoção do mesmo artefato -> rollback auditável
```

O código existe apenas para que o pipeline tenha algo verificável. Ele não
modela nenhum sistema real.

## 2. Fora de escopo

Docker, registry de imagens, Kubernetes, filas de GPU, runner próprio,
servidor, VM, PaaS, URL pública de aplicação, secrets, banco de dados,
frontend, branches permanentes `dev`/`staging`/`production` e publicação
automática de conteúdo.

`production` aqui é um job que registra promoção e validação de artefato. Não
prova a operação de um serviço.

## 3. Divisão de responsabilidades

Esta seção substitui a divisão anterior, em que a publicação do repositório era
uma dependência humana. O agente foi explicitamente autorizado a criar e
configurar o repositório remoto.

### 3.1 O agente prepara e configura — estrutura pronta

Arquivos:

| Componente | Arquivo | Estado |
| --- | --- | --- |
| Aplicação fictícia (CLI `health`/`version`) | `src/framework_demo.py` | pronto |
| Teste unitário | `tests/test_framework_demo.py` | pronto |
| CI em pull request, push em `main` e manual | `.github/workflows/ci.yml` | pronto |
| Delivery: build único, promoção em 3 ambientes e release | `.github/workflows/delivery.yml` | pronto |
| Propriedade do conteúdo protegido | `.github/CODEOWNERS` | pronto |
| Ruleset aplicado | `.github/governance/ruleset-protect-main.json` | pronto |
| Ruleset alvo, com revisão obrigatória | `.github/governance/ruleset-protect-main-with-reviewers.json` | pronto, **não aplicado** |
| Procedimento humano completo | `RUNBOOK.md` | pronto |
| Modelo de acessos e papéis | `ACESSOS-E-PAPEIS.md` | pronto |
| Roteiro do treinamento a dois | `LAB-OWNER-DEVELOPER.md` | pronto |
| Registro de decisões | `DECISIONS.md` | pronto |
| Roteiro de apresentação | `APRESENTACAO-10-MIN.md` | pronto |

Configuração remota, executada pelo agente:

| Item | Estado |
| --- | --- |
| Repositório público `Heveraldoo/framework-devops-sandbox` configurado | executado |
| Commit-base único em `main`, enviado | executado |
| Primeiro CI em `main` verde | executado |
| Ruleset `protect-main` ativo, exigindo `test-python` | executado |
| Ambientes `development`, `staging` e `production` criados | executado |
| Merge por squash como única estratégia | executado |

### 3.2 Exercícios e ensaios

O treinamento começa na criação da primeira branch. O estado real dos ensaios
é registrado em `HANDOFF.md`; não presuma que a lista abaixo esteja pendente.

| Exercício | Estado |
| --- | --- |
| Criar a primeira branch | não realizado |
| Abrir pull request | não realizado |
| Provocar a falha intencional e ler o check vermelho | não realizado |
| Corrigir, obter o check verde | não realizado |
| Merge por squash sob o ruleset | não realizado |
| Criar tags anotadas | não realizado |
| Publicar releases | não realizado |
| Promover em `staging` e `production` | não realizado |
| Executar o rollback | não realizado |
| Convidar o segundo participante e inverter papéis | não realizado |

Ver seção 5 para o detalhamento e `LAB-OWNER-DEVELOPER.md` para a condução.

## 4. Contrato técnico

### 4.1 Aplicação

- CLI com dois comandos: `health` devolve JSON com `status` e `version`;
  `version` devolve a versão.
- `VERSION` é a única fonte de versão no código.
- Nenhuma dependência externa. Apenas biblioteca padrão.

### 4.2 CI

- Nome do workflow: `CI`. Nome do job e do check: `test-python`.
- Dispara em `pull_request`, `push` em `main` e `workflow_dispatch`.
- Permissão do token: `contents: read`.
- Passos: testes unitários, `compileall`, smoke test.

### 4.3 Delivery

Dois pontos de entrada, com efeitos deliberadamente diferentes.

| Gatilho | Quando | Efeito |
| --- | --- | --- |
| `push` de tag `vX.Y.Z` ou `vX.Y.Z-rc.N` | o humano cria e envia a tag | build, promoção nos 3 ambientes e **criação ou atualização da Release** |
| `workflow_dispatch` com `source_ref` | exercício de rollback | build, promoção nos 3 ambientes e **nenhuma release criada ou alterada** |

O caminho por tag é o caminho normal de entrega: criar a tag é o que dispara a
automação, sem nenhum passo manual adicional. O `workflow_dispatch` existe para
promover uma tag **anterior** durante o rollback, preservando o histórico de
releases como registro de qual é a versão corrente.

Regras invariantes:

- O artefato é construído **uma única vez**, no job `build`. Os jobs
  `development`, `staging` e `production` apenas baixam esse mesmo artefato.
  Nenhum deles reconstrói.
- Cada ambiente verifica, antes de aprovar: `sha256sum -c SHA256SUMS` e a
  igualdade entre o `SOURCE_COMMIT` do artefato e o commit verificado no
  `build`. Depois executa o smoke test.
- O artefato contém `framework-demo.pyz`, `SOURCE_COMMIT` e `SHA256SUMS`.
- A Release só é criada ou atualizada **após** `production` ter passado, e
  recebe os três arquivos como assets. Tag contendo `-rc.` é publicada como
  prerelease.
- As Actions são fixadas por SHA de commit completo, com o comentário da versão
  correspondente ao lado.

#### 4.3.1 Validação da origem

O job `build` só prossegue depois de cinco provas explícitas. Nenhum passo
posterior chama a tag de confiável antes disso. A ordem é significativa: cada
prova depende da anterior.

| # | Prova | Falha quando |
| --- | --- | --- |
| 1 | O nome casa com `vX.Y.Z` ou `vX.Y.Z-rc.N` | nome fora do padrão SemVer |
| 2 | A tag existe **e é anotada** (`git cat-file -t` devolve `tag`) | tag inexistente ou leve |
| 3 | A tag é resolvida ao seu commit (`refs/tags/<tag>^{commit}`) | objeto não resolvível |
| 4 | `HEAD` é **exatamente** o commit resolvido da tag | o checkout não está no commit da tag |
| 5 | Esse commit é **ancestral de `main`** | tag fora do histórico revisado de `main` |

A prova 2 exige tag anotada porque uma tag anotada carrega autor, data e
mensagem: é um ato deliberado e atribuível, ao contrário da tag leve.

As provas 4 e 5 são distintas e ambas necessárias. A 4 garante que o conteúdo
construído é o da tag declarada. A 5 garante que esse conteúdo passou por
`main` — e portanto pelo pull request e pelo check obrigatório.

Um checkout por tag não cria `refs/remotes/origin/main` e não garante a
presença dos objetos de tag. Por isso `main` e as tags são buscados
explicitamente **antes** das provas, para que uma falha signifique violação de
regra e não ausência de referência.

Verificado localmente contra um repositório de teste: tag anotada em `main`
passa; tag leve, tag anotada fora de `main`, tag inexistente e nome fora do
padrão SemVer falham, cada uma na prova correspondente.

### 4.4 Governança de `main`

Ruleset `protect-main`, `Active`, alvo: branch padrão.

| Regra | Valor |
| --- | --- |
| Restrict deletions | ativo |
| Block force pushes | ativo |
| Require linear history | ativo |
| Require pull request before merging | ativo |
| Required approving reviews | `0` |
| Dismiss stale approvals on push | ativo |
| Require conversation resolution | ativo |
| Require status checks | `test-python` |
| Require branch up to date | ativo |

`Required approving reviews: 0` é um desvio deliberado e registrado. Com um
único participante ativo, exigir uma aprovação de terceiro travaria todos os
merges. O valor pretendido, quando o segundo participante estiver disponível, é
`1` com aprovação de alguém diferente do último autor de push. Ver
`DECISIONS.md`.

### 4.5 Ambientes

| Ambiente | Aprovação | `prevent_self_review` | Deployment branch/tag policy |
| --- | --- | --- | --- |
| `development` | nenhuma | não aplicável | nenhuma |
| `staging` | `@fabianomag` | `false` enquanto solo | nenhuma |
| `production` | `@fabianomag` | `false` enquanto solo | nenhuma |

`prevent_self_review: false` é desvio deliberado: com um único participante,
ativá-lo impediria qualquer promoção. Valor pretendido `true`, com o segundo
participante como revisor. Ver `DECISIONS.md` e `ACESSOS-E-PAPEIS.md` §5.2.

**Sem deployment branch/tag policy, por decisão registrada.** O `Delivery` agora
executa em duas refs diferentes: uma tag, no caminho de release, e `main`, no
`workflow_dispatch` do rollback. Uma policy restrita a tags bloquearia o
rollback; uma restrita a `main` bloquearia a release. Uma policy que aceitasse
os dois padrões não restringiria nada de fato. Deixar sem policy é a opção
honesta: o gate real destes ambientes é a **aprovação humana obrigatória**, não
o padrão da ref. Ver `DECISIONS.md`.

## 5. Exercícios executados pelos humanos

O agente prepara. O operador principal e o segundo participante executam. Esta
divisão é o objetivo pedagógico, não uma limitação técnica.

O repositório já existe e já está configurado. **O primeiro exercício humano é
criar a primeira branch.**

1. Abrir uma branch curta e um pull request.
2. Provocar uma falha intencional no teste e ler o log do check vermelho.
3. Confirmar que o merge está bloqueado pelo ruleset já ativo.
4. Corrigir, obter o check verde e mesclar por squash.
5. Criar e enviar a tag anotada `v0.1.0-rc.1`. O envio da tag dispara o
   `Delivery` sozinho.
6. Aprovar `staging` e `production`. A prerelease é criada pelo próprio
   workflow, com os três assets.
7. Repetir o fluxo para `0.1.1` e enviar a tag `v0.1.1`.
8. Executar `Delivery` por `workflow_dispatch` com `source_ref: v0.1.0` como
   rollback, aprovar de novo e confirmar que **nenhuma release nova** foi
   criada.
9. Auditar runs, deployments, releases e rulesets.
10. Convidar o segundo participante, ligar as regras de revisão e inverter os
    papéis. Ver `ACESSOS-E-PAPEIS.md` e `LAB-OWNER-DEVELOPER.md`.

`RUNBOOK.md` traz o procedimento comando a comando.

## 6. Limitações declaradas

- O rollback reconstrói a fonte da versão anterior. Não é a promoção do mesmo
  digest binário e não é rollback de um serviço em operação.
- Artefatos de execução expiram. A evidência durável é o asset anexado à
  release.
- Em repositório público, remover um papel elevado revoga escrita e
  administração; não remove leitura pública, forks nem clones existentes.
- Código de saída zero não é evidência. A evidência deve provar o comportamento
  que o exercício pretendia demonstrar.

## 7. Critérios objetivos de conclusão

### 7.1 Concluídos pelo agente — estrutura

1. Repositório público criado, com a base enviada em um único commit.
2. CI verde em `main`, linkável.
3. Workflows `CI` e `Delivery` reconhecidos pelo GitHub.
4. Ruleset `protect-main` ativo e exigindo `test-python`, **antes** de existir
   qualquer pull request.
5. Ambientes `development`, `staging` e `production` existentes.
6. Nenhuma branch adicional, pull request, tag, release ou execução de
   `Delivery` criada pelo agente.
7. Nenhum secret, credencial ou conteúdo não público em qualquer arquivo.

### 7.2 A cargo dos humanos — exercícios

8. Um check `test-python` vermelho e depois verde, ambos linkáveis.
9. Merge bloqueado com o check vermelho e liberado com o verde, provando que o
   gate é a regra e não a disciplina.
10. Prerelease `v0.1.0-rc.1` criada pelo próprio `Delivery`, disparado pelo
    envio da tag.
11. Uma execução de `Delivery` com `SOURCE_COMMIT` idêntico nos três jobs e
    `sha256sum -c` bem-sucedido em cada um.
12. Release `v0.1.0` com `framework-demo.pyz`, `SOURCE_COMMIT` e `SHA256SUMS`.
13. Release `v0.1.1` publicada pelo mesmo procedimento.
14. `Delivery` por `workflow_dispatch` com `v0.1.0` exigindo novas aprovações,
    cujo smoke test imprime `0.1.0` enquanto a versão corrente é `0.1.1`, **sem
    criar release nova**.
15. Segundo participante convidado, regras de revisão ligadas e papéis
    invertidos.
