# COMECE AQUI — material de teste e aprendizado

Guia prático: **só cliques na interface do GitHub, na ordem.** Não precisa de
terminal. Em ~12 minutos você percorre o fluxo inteiro: branch, pull request,
check falhando, merge bloqueado, correção, release e deploy nos três ambientes.

É pra fazer mexendo, não pra ler. Abra o repositório ao lado e vá clicando.

Deixe abertas 3 abas: `Code` · `Actions` · `Settings`.

> **Se você chegou aqui por um fork:** três coisas não vêm junto no fork, porque
> são configuração e não arquivo. Sem elas os passos 3 a 5 não funcionam:
>
> 1. **Actions vem desligado** → aba `Actions` → botão verde
>    *"I understand my workflows, go ahead and enable them"*
> 2. **O ruleset não vem** → `Settings` → `Rules` → `Rulesets` →
>    **New branch ruleset** (valores em `DEVOPS-LAB-SPEC.md` §4.4)
> 3. **Os environments não vêm** → `Settings` → `Environments` → criar
>    `development`, `staging` e `production`
>
> Montar isso do zero é parte do aprendizado — é o que só o dono do repositório
> pode fazer. Troque também `@fabianomag` no `.github/CODEOWNERS` pelo seu
> usuário.

---

## 0. Dar acesso ao dev (2 min)

`Settings` → menu esquerdo **Collaborators** → botão verde **Add people** →
digita o usuário → **Add to repository**.

Ele recebe e-mail. **Ele precisa aceitar** antes de continuar.

> **Fale isto:** repositório pessoal só tem 2 níveis — **Owner** (eu) e
> **Collaborator** (você). Não existe "master" granular aqui. Para ter 2 admins
> de verdade e papéis finos, precisaria de uma **Organization**. Como
> Collaborator ele já cria branch, PR, tag e release — só não mexe em Settings.

---

## 1. Mostrar que a regra existe (1 min)

`Settings` → **Rules** → **Rulesets** → clica em **protect-main**.

Aponte na tela: `Require a pull request before merging`, `Require status checks`
→ **test-python**, `Block force pushes`.

> **Fale isto:** ninguém commita direto na `main`. Nem eu. Já testei: o GitHub
> recusou meu push com *"Changes must be made through a pull request"*.

---

## 2. Criar a branch pela UI (1 min) — **quem faz: o dev**

Aba `Code` → arquivo **`tests/test_framework_demo.py`** → ícone do **lápis**
(canto direito) → editar.

Trocar `"ok"` por `"ready"` (linha do `assertEqual`).

Botão verde **Commit changes...** → marcar a 2ª opção
**"Create a new branch for this commit and start a pull request"** →
nome: `feat/demo` → **Propose changes**.

---

## 3. Abrir o PR e ver o check VERMELHO (2 min)

Na tela seguinte → **Create pull request**.

Espere ~40s. Aparece embaixo: **test-python — Failing** ❌
Clique em **Details** → veja a linha do erro no log.

> **Fale isto:** o check só vale porque já provou que consegue ficar vermelho.
> Check que fica verde sempre é decoração.

Volte ao PR: o botão **Merge** está **cinza/bloqueado**.

> **Fale isto:** não estou esperando por educação. A regra bloqueia.

---

## 4. Corrigir e ver ficar VERDE (2 min)

No PR → aba **Files changed** → ícone do **lápis** no arquivo →
volta `"ready"` para `"ok"` → **Commit changes** → **Commit directly to the
`feat/demo` branch**.

Espere ~40s → **test-python — Success** ✅ → botão **Merge** libera.

Clique **Squash and merge** → **Confirm squash and merge** →
**Delete branch**.

> **Fale isto:** mesmo mecanismo que bloqueou é o que liberou. Não desliguei
> nada — corrigi.

---

## 5. Release + deploy nos 3 ambientes (3 min)

Aba `Code` → direita, seção **Releases** → **Create a new release**.

- **Choose a tag** → digitar `v0.1.0` → **+ Create new tag: v0.1.0 on publish**
- Title: `v0.1.0`
- **Publish release**

Vá para **Actions** → workflow **Delivery** rodando sozinho.

> **Fale isto:** criar a tag disparou a entrega. Não apertei nenhum botão de
> deploy.

Ordem que aparece na tela:
`build-artifact` → `promote-development` ✅ → **`promote-staging` PARA e espera**

Clique **Review deployments** → marcar `staging` → **Approve and deploy**.
Depois repete para **production**.

> **Fale isto:** o artefato foi construído **uma vez**. Os 3 ambientes baixam o
> **mesmo** arquivo e conferem o checksum. Se cada um recompilasse, "testado em
> staging" não provaria nada sobre production.

Terminado → volte em **Releases**: os 3 arquivos foram anexados sozinhos
(`framework-demo.pyz`, `SOURCE_COMMIT`, `SHA256SUMS`).

---

## 6. Onde ficam os controles de acesso (1 min)

`Settings` → **Environments** → clique em **production**.

Mostre: **Required reviewers** = você.

> **Fale isto:** deploy em production precisa de aprovação humana. Hoje sou eu
> nos dois lados porque estou sozinho — quando ele entrar, troco o revisor para
> ele e ligo **Prevent self-review**. Aí quem escreve não aprova o próprio
> deploy.

---

## Se sobrar tempo: rollback

`Actions` → **Delivery** → **Run workflow** (botão direito) →
`source_ref`: `v0.1.0` → **Run workflow**. Aprovar staging e production de novo.

> **Fale isto:** voltar atrás também passa pelo mesmo portão. E repare:
> **nenhuma release nova** foi criada — o histórico continua dizendo qual é a
> versão atual.

---

## Perguntas que vão fazer

| Pergunta | Resposta |
| --- | --- |
| Isso é produção? | Não. `production` é um job que registra promoção de um artefato fictício. Não tem serviço, host nem URL. |
| Ele pode virar admin? | Não em repo pessoal. Só numa Organization. |
| Dá pra burlar? | Eu posso alterar a regra — mas alterar **fica registrado**. Contornar deixou de ser o caminho mais fácil. |
| Por que o código é tão pequeno? | O objeto de estudo é o pipeline, não o código. |

---

## ⚠️ Antes da reunião

Os passos 2 a 5 **nunca foram executados** — não existe PR, tag nem release
ainda. Se puder, rode uma vez sozinho antes (10 min) e depois **apague a
release e a tag** em `Releases` → `Delete`, para repetir ao vivo.

Se não der tempo: faça **ao vivo mesmo**, na ordem acima. Funciona — só depende
do runner do GitHub, que leva ~40s por check.
