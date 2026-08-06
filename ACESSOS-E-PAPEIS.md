# ACESSOS-E-PAPEIS.md

Quem tem qual acesso neste laboratório, o que esse acesso realmente permite e o
que ele não permite. Este documento descreve o modelo de permissões do GitHub
como ele é, não como seria conveniente que fosse.

Repositório: `Heveraldoo/framework-devops-sandbox`, público, pessoal.

## 1. O limite honesto: repositório pessoal só tem dois papéis

Este é um **repositório pessoal**, não um repositório de organização. Isso
determina tudo o que segue.

Um repositório pessoal tem exatamente dois níveis de acesso:

| Papel | Quem pode ter | O que permite |
| --- | --- | --- |
| **Owner** | somente `@Heveraldoo` | tudo: administração, settings, rulesets, environments, exclusão do repositório, gestão de colaboradores |
| **Collaborator** | qualquer conta convidada | push, abrir e revisar pull requests, criar branches e tags, criar releases |

Não existe meio-termo. Um colaborador de repositório pessoal recebe, na
prática, acesso equivalente a *write*: não é possível dar a ele *triage*, nem
*maintain*, nem *admin* parcial.

### O que isso significa concretamente

**Não é possível ter dois Owners.** A propriedade de um repositório pessoal
pertence a uma única conta. Transferir a propriedade é uma transferência, não
um compartilhamento: `@fabianomag` deixaria de ser dono. Isso não será feito.

**Não é possível dar papéis granulares.** Os papéis `Read`, `Triage`, `Write`,
`Maintain` e `Admin` — cinco níveis — só existem em repositórios pertencentes a
uma **organização**. Aqui há dois.

**Não existem times.** `@equipe/revisores` não é referenciável em `CODEOWNERS`
neste repositório. Por isso o `CODEOWNERS` referencia uma pessoa.

**Se algum dia forem necessários papéis granulares, dois administradores ou
times, o caminho é criar uma organização** e transferir ou recriar o
repositório dentro dela. Criar organização está fora do escopo autorizado deste
laboratório e não foi feito. Fica registrado como caminho futuro, não como
pendência.

## 2. Os papéis pedagógicos deste laboratório

Papel pedagógico e papel técnico do GitHub não são a mesma coisa. A tabela
abaixo separa os dois.

| Pessoa | Papel pedagógico | Papel técnico no GitHub | Estado |
| --- | --- | --- | --- |
| Heveraldo (`@Heveraldoo`) | Owner técnico do laboratório | Owner | ativo |
| Fabiano (`@fabianomag`) | Instrutor / operador do ensaio | Collaborator (`Write`) | ativo |
| Segundo participante | Aprendiz do fluxo de entrega | Collaborator | a definir |

### Heveraldo — Owner técnico; Fabiano — instrutor e operador

Responsável por:

- administrar o repositório: settings, ruleset `protect-main`, environments;
- ser o revisor inicial de `staging` e `production`;
- conduzir o treinamento e explicar cada etapa;
- decidir quando ligar as regras que hoje estão desligadas;
- registrar em `DECISIONS.md` toda mudança de configuração.

Enquanto estiver sozinho, Fabiano acumula os papéis de autor e de aprovador.
Isso é uma limitação declarada, não uma boa prática — ver seção 4.

### Segundo participante — aprendiz do fluxo

O que ele aprende a fazer, na ordem em que aparece no `RUNBOOK.md`:

1. criar uma branch curta a partir de `main`;
2. commitar e enviar a branch;
3. abrir um pull request;
4. **ler e interpretar os checks** — o que `test-python` está verificando;
5. provocar uma falha intencional e localizar no log a linha que a explica;
6. corrigir a falha e ver o check ficar verde;
7. entender por que o merge estava bloqueado — a regra, não a disciplina;
8. mesclar por squash sob o ruleset ativo;
9. acompanhar a criação da tag, a release e a promoção entre ambientes;
10. observar o rollback e por que ele exige nova aprovação.

O que ele **não** faz enquanto for Collaborator: alterar settings, alterar o
ruleset, criar ou reconfigurar environments, gerenciar acessos. Isso é
propriedade do Owner.

## 3. Convite do segundo participante

**Não foi enviado nenhum convite.** Convidar pessoas está fora do escopo do
agente e é uma decisão do operador principal. O procedimento é do Fabiano.

Pela interface: `Settings` -> `Collaborators` -> `Add people`.

Por linha de comando:

```bash
gh api --method PUT "repos/Heveraldoo/framework-devops-sandbox/collaborators/USERNAME" \
  -f permission=push
```

Conferir o convite pendente e os colaboradores atuais:

```bash
gh api "repos/Heveraldoo/framework-devops-sandbox/invitations" \
  --jq '.[] | [.invitee.login, .permissions, .created_at] | @tsv'

gh api "repos/Heveraldoo/framework-devops-sandbox/collaborators" \
  --jq '.[] | [.login, .role_name] | @tsv'
```

O convite só tem efeito quando a outra pessoa **aceita**. Antes disso ela não
aprova nada, e ligar as regras da seção 4 travaria o laboratório.

## 4. O que está desligado hoje, e por quê

Três controles estão deliberadamente desligados. Todos pelo mesmo motivo: com
uma única pessoa ativa, cada um deles bloquearia completamente o fluxo que o
laboratório precisa demonstrar.

| Controle | Hoje | Motivo | Valor pretendido |
| --- | --- | --- | --- |
| `required_approving_review_count` | `0` | ninguém mais pode aprovar | `1` |
| `require_last_push_approval` | `false` | exigiria um aprovador diferente do autor, que não existe | `true` |
| `require_code_owner_review` | `false` | o único CODEOWNER é o próprio autor | `true` |
| `prevent_self_review` em `staging` e `production` | `false` | impediria qualquer promoção | `true` |

Isto precisa ser dito em voz alta em qualquer apresentação: **hoje o gate real
é o check obrigatório `test-python`, não a revisão humana.** O mecanismo de
revisão está montado e desligado, não ausente.

## 5. Ativação, depois que o segundo participante aceitar

Executar na ordem. Cada passo é reversível.

### 5.1 Ligar as três regras de pull request

Pela interface: `Settings` -> `Rules` -> `Rulesets` -> `protect-main` ->
`Require a pull request before merging`:

- `Required approvals`: `1`
- marcar `Require review from Code Owners`
- marcar `Require approval of the most recent reviewable push`

Por linha de comando, obter o id do ruleset e aplicar o arquivo já preparado:

```bash
OWNER=Heveraldoo REPO=framework-devops-sandbox

RULESET_ID=$(gh api "repos/$OWNER/$REPO/rulesets" --jq '.[] | select(.name=="protect-main") | .id')

gh api --method PUT "repos/$OWNER/$REPO/rulesets/$RULESET_ID" \
  --input .github/governance/ruleset-protect-main-with-reviewers.json

gh api "repos/$OWNER/$REPO/rulesets/$RULESET_ID" \
  --jq '.rules[] | select(.type=="pull_request") | .parameters'
```

O arquivo `ruleset-protect-main-with-reviewers.json` já existe em
`.github/governance/` com os três valores ligados. Ele não está aplicado.

### 5.2 Trocar o revisor dos ambientes e proibir auto-aprovação

```bash
SECOND_ID=$(gh api users/SEGUNDO_USERNAME --jq .id)

for ENV in staging production; do
  gh api --method PUT "repos/$OWNER/$REPO/environments/$ENV" \
    -F "prevent_self_review=true" \
    -F "reviewers[][type]=User" -F "reviewers[][id]=$SECOND_ID"
done
```

Conferir:

```bash
gh api "repos/$OWNER/$REPO/environments" \
  --jq '.environments[] | [.name, (.protection_rules | length)] | @tsv'
```

### 5.3 Registrar

Marcar em `DECISIONS.md` as decisões `pendente do segundo participante` como
resolvidas, com a data e o que passou a valer.

## 6. Inversão de papéis

Depois que o segundo participante tiver percorrido o fluxo completo pelo menos
uma vez, os papéis se invertem. Este é o segundo ciclo do treinamento, e é onde
o aprendizado se comprova.

| | Primeiro ciclo | Segundo ciclo (invertido) |
| --- | --- | --- |
| Quem abre a branch e o pull request | segundo participante | Fabiano |
| Quem revisa e aprova o pull request | Fabiano | segundo participante |
| Quem aprova `staging` e `production` | Fabiano | segundo participante |
| Quem explica cada etapa em voz alta | Fabiano | segundo participante |

A inversão exige apenas trocar o revisor dos environments — comando da seção
5.2, com o id do Fabiano no lugar. O ruleset não muda: ele já exige uma
aprovação de alguém diferente de quem fez o último push, e isso funciona nos
dois sentidos.

**O que a inversão não muda:** o papel técnico. Heveraldo continua Owner e
Fabiano/segundo participante continuam Collaborators. A inversão é pedagógica.
Para que ela fosse também técnica — dois administradores de verdade — seria
necessária uma organização, pelo motivo da seção 1.

Critério para considerar a inversão bem-sucedida: o segundo participante
consegue explicar, sem ajuda, por que um merge foi bloqueado e o que
exatamente precisa acontecer para desbloqueá-lo.

## 7. Remoção de acesso

Encerrado o treinamento, remover o colaborador:

```bash
gh api --method DELETE "repos/$OWNER/$REPO/collaborators/USERNAME"
```

Ser honesto sobre o efeito, porque este é um repositório **público**: remover o
acesso revoga escrita e administração. **Não** revoga leitura — qualquer pessoa
já podia ler. **Não** apaga forks nem clones que já existam. **Não** apaga o
que já foi publicado. Em repositório público, o histórico, os artefatos e as
releases devem ser tratados como informação já divulgada de forma permanente.
