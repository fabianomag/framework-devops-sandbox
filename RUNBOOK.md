# RUNBOOK.md

Procedimento humano do laboratório. O agente preparou a base; os passos abaixo
são o exercício e pertencem ao operador principal e ao segundo participante.

Convenções: `OWNER=Heveraldoo`, `REPO=framework-devops-sandbox`.
Nenhum comando aqui pede, imprime ou cria credencial.

```bash
export OWNER=Heveraldoo
export REPO=framework-devops-sandbox
```

## 0. Estado inicial — já feito, nada a executar

As seções 0 a 2 e 7 da versão anterior deste runbook **já foram executadas pelo
agente**. Ficam aqui apenas como verificação, em modo somente leitura.

Já existe:

- o repositório público, com o commit-base em `main` e o CI verde;
- os workflows `CI` e `Delivery` reconhecidos;
- o ruleset `protect-main` ativo, exigindo `test-python`;
- os ambientes `development`, `staging` e `production`;
- squash merge como única estratégia, com exclusão automática da head branch.

Conferir, sem alterar nada:

```bash
gh repo view "$OWNER/$REPO" --json name,visibility,defaultBranchRef,url
gh run list --repo "$OWNER/$REPO" --limit 5
gh api "repos/$OWNER/$REPO/rulesets" --jq '.[] | [.name, .enforcement] | @tsv'
gh api "repos/$OWNER/$REPO/environments" --jq '.environments[].name'
```

Clonar, se ainda não tiver o repositório em disco:

```bash
gh repo clone "$OWNER/$REPO"
cd framework-devops-sandbox
python3 -m unittest discover -s tests -v
```

Pré-flight local, somente leitura:

```bash
git --version
python3 --version
gh --version
gh auth status
```

**O exercício começa na seção 3.**

## 3. Abrir a branch e o pull request — PRIMEIRO EXERCÍCIO

```bash
git switch -c feat/health-endpoint
```

Editar `tests/test_framework_demo.py` e adicionar a expectativa de um campo
que ainda não existe: `self.assertEqual(health()["component"],
"framework-demo")`. Rodar e guardar a falha:

```bash
python3 -m unittest discover -s tests -v
```

Commitar a falha de propósito, para que o CI fique vermelho:

```bash
git add tests/test_framework_demo.py
git commit -m 'test: demonstrate a failing check'
git push -u origin feat/health-endpoint
gh pr create --fill
```

Abrir o pull request, abrir `Actions` -> `CI` -> `test-python` e localizar no
log a linha que explica a falha. Guardar o link do run vermelho.

## 4. Confirmar o merge bloqueado

O ruleset **já está ativo** — foi aplicado pelo agente antes de existir qualquer
pull request, que é a ordem que a demonstração exige. Não há nada a aplicar
aqui; há algo a observar.

Confirmar quais regras estão valendo em `main`:

```bash
gh api "repos/$OWNER/$REPO/rules/branches/main" \
  --jq '.[] | [.type, .ruleset_source] | @tsv'
```

Voltar ao pull request. O merge está bloqueado pelo check vermelho.

Mostrar ao segundo participante, em `Settings` -> `Rules` -> `protect-main`, a
regra que está bloqueando. Mostrar também que o próprio Owner está bloqueado.

**Este é o ponto central do laboratório:** o merge está barrado por uma regra do
repositório, não por disciplina nem por vigilância. Guardar o link do pull
request bloqueado e o link do run vermelho como evidência.

## 5. Corrigir, ficar verde e mesclar

```bash
git switch feat/health-endpoint
```

Adicionar `"component": "framework-demo"` ao dicionário retornado por
`health()` em `src/framework_demo.py` e enviar:

```bash
python3 -m unittest discover -s tests -v
git add src/framework_demo.py
git commit -m 'feat: add health component metadata'
git push
```

Com o check verde, mesclar por squash na interface ou:

```bash
gh pr merge --squash --delete-branch
git switch main
git pull --ff-only
```

## 6. Criar a release candidate

A tag precisa ser **anotada** (`-a`). O `Delivery` recusa tag leve: uma tag
anotada tem autor, data e mensagem, e é isso que a torna um ato deliberado e
atribuível.

```bash
git switch main
git pull --ff-only
git status --short
git tag -a v0.1.0-rc.1 -m 'Release candidate v0.1.0-rc.1'
git show --no-patch --decorate v0.1.0-rc.1
git push origin v0.1.0-rc.1
```

**Enviar a tag dispara o `Delivery` sozinho.** Não execute nenhum comando de
dispatch aqui. Seguir para a seção 7.

## 7. Acompanhar a promoção

```bash
RUN_ID=$(gh run list --workflow Delivery --limit 1 --json databaseId --jq '.[0].databaseId')
gh run watch "$RUN_ID"
```

O que acontece, nesta ordem:

1. `build-artifact` verifica a origem da tag — as cinco provas — e constrói o
   artefato **uma única vez**;
2. `promote-development` passa sozinho;
3. `promote-staging` **para e espera aprovação**;
4. `promote-production` **para e espera aprovação**;
5. `publish-release` cria a release e anexa os três arquivos.

Aprovar: `Actions` -> a execução -> `Review deployments` -> `Approve and
deploy`. Uma vez para `staging`, outra para `production`.

Provar que os três ambientes receberam o mesmo artefato:

```bash
gh run view "$RUN_ID" --log | grep -E 'promoting|SOURCE_COMMIT|: OK'
```

Confirmar o mesmo `SOURCE_COMMIT` nos três jobs e o `sha256sum -c` bem-sucedido
em cada um. Baixar e verificar por conta própria:

```bash
gh run download "$RUN_ID" --name "framework-demo-$RUN_ID" --dir /tmp/promoted
(cd /tmp/promoted
shasum -a 256 -c SHA256SUMS
python3 framework-demo.pyz health)
```

## 8. Conferir a release publicada

O workflow já criou a release. Nada a criar à mão.

```bash
gh release view v0.1.0-rc.1
gh release view v0.1.0-rc.1 --json assets --jq '.assets[].name'
```

Devem aparecer `framework-demo.pyz`, `SOURCE_COMMIT` e `SHA256SUMS`. Uma tag com
`-rc.` é publicada como **prerelease**.

## 9. Publicar a versão estável

```bash
git rev-list -n 1 v0.1.0-rc.1
git tag -a v0.1.0 -m 'Release v0.1.0'
git show --no-patch --decorate v0.1.0
git push origin v0.1.0
```

O envio da tag dispara o `Delivery` de novo: nova promoção, novas aprovações em
`staging` e `production`, e a release `v0.1.0` criada ao final — desta vez não
como prerelease.

Não crie uma release manual antes do push da tag: o workflow é a fonte de
verdade para publicação e anexos.

## 10. Criar a versão corrente `0.1.1`

```bash
git switch main
git pull --ff-only
git switch -c chore/prepare-0.1.1
```

Trocar somente `VERSION = "0.1.0"` por `VERSION = "0.1.1"` em
`src/framework_demo.py`. Depois:

```bash
python3 -m unittest discover -s tests -v
python3 -m src.framework_demo version
git add src/framework_demo.py
git commit -m 'chore: prepare version 0.1.1'
git push -u origin chore/prepare-0.1.1
gh pr create --fill
```

Com o CI verde, mesclar por squash. Então:

```bash
git switch main
git pull --ff-only
git tag -a v0.1.1 -m 'Release v0.1.1'
git push origin v0.1.1
```

O envio da tag dispara o `Delivery`. Aprovar `staging` e `production`. A release
`v0.1.1` é criada ao final.

## 11. Rollback

Agora `v0.1.1` é a versão corrente. O rollback promove de volta o conteúdo de
`v0.1.0`, e é o **único** caso que usa disparo manual:

```bash
gh workflow run Delivery -f source_ref=v0.1.0
gh run list --workflow Delivery --limit 3
```

Aprovar novamente `staging` e `production` — a nova aprovação é parte da
demonstração: voltar atrás também é uma mudança e passa pelo mesmo portão.

Duas coisas a confirmar:

```bash
# 1. o smoke test volta a imprimir a versão anterior
gh run view --log | grep -E '"version"'

# 2. NENHUMA release nova foi criada; v0.1.1 continua sendo a mais recente
gh release list
```

O job `publish-release` não executa neste caminho — ele é condicionado ao
disparo por tag. É por isso que o histórico de releases continua dizendo a
verdade sobre qual é a versão corrente.

```bash
git fetch --tags --prune
git rev-list -n 1 v0.1.0
```

Comparar com o `SOURCE_COMMIT` da execução. **Nunca mover a tag `v0.1.0`:** quem
já a tenha baixado passaria a ter outro conteúdo com o mesmo nome.

Limitação a declarar em voz alta: este rollback **reconstrói a fonte** da versão
anterior. Não é a repromoção do mesmo binário e não é rollback de um serviço em
operação.

## 12. Auditoria

```bash
gh run list --limit 20
gh release list
gh api "repos/$OWNER/$REPO/deployments" --jq '.[] | [.environment, .ref, .created_at] | @tsv'
gh api "repos/$OWNER/$REPO/rulesets" --jq '.[] | [.name, .enforcement, .target] | @tsv'
```

Pela interface: `Actions`, `Environments`, `Releases` e `Settings` -> `Rules`.

## Recuperação

| Situação | Ação |
| --- | --- |
| Tag criada no commit errado, ainda não enviada | `git tag -d <tag>` e recriar após confirmar o alvo |
| Tag errada já enviada | Não mover nem reutilizar. Criar uma versão corretiva e documentar |
| Merge travado sem aprovador | Conferir o ruleset; não desligar todas as regras de uma vez |
| Check obrigatório não aparece na lista | Ele precisa ter executado recentemente e o nome deve ser exato: `test-python` |
| CI passa local e falha remoto | Comparar versão de Python, diretório de execução e nomes de arquivo |
| `Delivery` falha na verificação de ancestralidade | Confirmar que a tag existe e é alcançável a partir de `main` |
| `Delivery` recusa a tag: "is commit, not an annotated tag object" | A tag foi criada sem `-a`. Apagar e recriar anotada: `git tag -d <tag>`, `git push origin :refs/tags/<tag>`, `git tag -a <tag> -m '...'`. Só faça isso se ninguém tiver usado a tag |
| Enviei a tag e o `Delivery` não disparou | Conferir o padrão: só `vX.Y.Z` e `vX.Y.Z-rc.N` disparam. Conferir também se a tag foi enviada, e não apenas criada local |
| O rollback não criou release | É o comportamento correto e deliberado. Só o disparo por tag publica |
| Quero ligar a exigência de aprovação | `ACESSOS-E-PAPEIS.md` §5. Só depois que o segundo participante aceitar o convite |
