# LAB-OWNER-DEVELOPER.md

Guia prático do laboratório para duas pessoas: **o Owner**, que administra e
ensina, e **o Developer**, que aprende o fluxo de entrega executando-o.

Este documento é o roteiro do treinamento. O `RUNBOOK.md` traz os comandos
exatos; aqui está quem faz o quê, em que ordem e o que cada pessoa deve
entender ao final de cada etapa.

Modelo de permissões e limites do GitHub: `ACESSOS-E-PAPEIS.md`.

## 1. As duas cadeiras

| | Owner | Developer |
| --- | --- | --- |
| Pessoa | Fabiano (`@fabianomag`) | segundo participante |
| Papel pedagógico | Master, administrador, instrutor | aprendiz do fluxo |
| Papel técnico | Owner do repositório | Collaborator |
| Administra settings, ruleset, environments | sim | não |
| Cria branch, pull request, corrige falha | acompanha e explica | **executa** |
| Aprova promoção em `staging` e `production` | sim, no primeiro ciclo | não, no primeiro ciclo |

O princípio: **o Developer executa, o Owner explica.** Se o Owner executar por
ele, o laboratório perde a finalidade. Se o Developer administrar o
repositório, ele pula justamente a parte que precisa entender do lado de fora.

## 2. Estado inicial

Antes de começar, isto já existe e foi preparado pelo agente:

- o repositório público, com a base em `main` e o CI verde;
- os workflows `CI` e `Delivery` reconhecidos pelo GitHub;
- o ruleset `protect-main` ativo, exigindo o check `test-python`;
- os ambientes `development`, `staging` e `production`;
- toda a documentação.

E isto **não** existe, porque é o exercício:

- nenhuma branch além de `main`;
- nenhum pull request;
- nenhuma tag, nenhuma release;
- nenhuma execução de `Delivery`;
- nenhum convite enviado.

**O treinamento começa na criação da primeira branch.**

## 3. Preparação do Owner

Antes da sessão com o Developer.

1. Convidar o Developer como colaborador — comando em `ACESSOS-E-PAPEIS.md`,
   seção 3. Confirmar que ele aceitou.
2. Decidir se as regras de revisão serão ligadas agora. Recomendação: **fazer o
   primeiro ciclo com elas desligadas**, para que o Developer veja o check
   bloqueando o merge sem a complicação adicional da revisão obrigatória.
   Ligá-las no segundo ciclo, quando a inversão de papéis acontecer.
3. Ter aberta a aba `Actions` do repositório, para mostrar os runs ao vivo.
4. Ler `AGENTS.md`: nada de conteúdo real ou confidencial entra aqui. O
   repositório é público e tudo nele é permanente.

## 4. O primeiro ciclo, etapa por etapa

Cada etapa tem: quem executa, o que se vê e o que precisa ficar entendido.
Os comandos estão em `RUNBOOK.md`, nas seções indicadas.

### Etapa 1 — A branch (`RUNBOOK.md` §3)

**Developer executa.** Cria `feat/health-endpoint` a partir de `main`.

O Owner explica: por que não se trabalha direto em `main`, e que a branch é
barata e descartável.

**Entendimento esperado:** a branch é uma linha de trabalho isolada; nada nela
afeta `main` até um merge.

### Etapa 2 — A falha intencional (`RUNBOOK.md` §3)

**Developer executa.** Altera o teste para esperar `"ready"` em vez de `"ok"`,
roda o teste localmente, vê a falha, e **commita a falha de propósito**.

O Owner explica que isto é deliberado: queremos ver o mecanismo de defesa
funcionando, e a única forma de confiar nele é vê-lo falhar quando deve.

**Entendimento esperado:** o teste local e o teste do CI são o mesmo teste. Uma
falha local vai falhar no CI.

### Etapa 3 — O pull request e o check vermelho (`RUNBOOK.md` §3)

**Developer executa.** Envia a branch, abre o pull request, abre
`Actions` -> `CI` -> `test-python`.

O Owner conduz a leitura do log. A pergunta a fazer ao Developer, antes de
mostrar a resposta: *"onde exatamente, nesta saída, está dito o que quebrou?"*

**Entendimento esperado:** o Developer localiza sozinho a linha do
`AssertionError` que mostra o valor esperado e o valor recebido. Ler o log é a
competência central desta etapa — não é decorar comandos.

Guardar o link do run vermelho. Ele é evidência.

### Etapa 4 — O merge bloqueado

**Os dois observam.** O botão de merge está bloqueado.

O Owner mostra, em `Settings` -> `Rules`, a regra que está bloqueando: o check
`test-python` é obrigatório. Mostra também que o próprio Owner, com acesso
total, também está bloqueado.

**Entendimento esperado — o ponto mais importante do laboratório:** o merge
está bloqueado por uma **regra do repositório**, não por disciplina, não por
convenção, não por alguém estar vigiando. A regra vale para todos, inclusive
para quem a criou.

### Etapa 5 — A correção e o check verde (`RUNBOOK.md` §5)

**Developer executa.** Restaura `"ok"`, roda o teste local, commita e envia.

O check reexecuta sozinho e fica verde. O botão de merge libera.

**Entendimento esperado:** o mesmo mecanismo que bloqueou é o que libera. Nada
foi desligado para destravar; o problema foi corrigido.

### Etapa 6 — O merge por squash (`RUNBOOK.md` §5)

**Developer executa.** Merge por squash e exclusão da branch.

O Owner explica por que squash: `main` fica com um commit por mudança, e o
`required_linear_history` do ruleset exige histórico linear.

**Entendimento esperado:** os dois commits da branch — o que quebrou e o que
corrigiu — viram um único commit em `main`. O histórico de `main` conta a
intenção, não a tentativa.

### Etapa 7 — A tag e a release (`RUNBOOK.md` §6 e §9)

**Owner executa no primeiro ciclo, com o Developer olhando.** Cria a tag
anotada e a envia.

Importante: **enviar a tag dispara o `Delivery` automaticamente.** Não é
preciso disparar nada à mão.

O Owner explica a diferença entre tag leve e tag anotada, e por que o
`Delivery` exige a anotada: uma tag anotada tem autor, data e mensagem — é um
ato deliberado e atribuível.

**Entendimento esperado:** a tag é o que transforma um commit em uma versão
candidata a ser entregue.

### Etapa 8 — A promoção e as aprovações (`RUNBOOK.md` §8)

**Os dois observam. O Owner aprova.**

O `Delivery` constrói o artefato **uma única vez** e o promove por
`development`, `staging` e `production`. `development` passa sozinho; `staging`
e `production` param e esperam aprovação humana.

O Owner mostra, nos logs dos três ambientes, o **mesmo `SOURCE_COMMIT`** e o
`sha256sum -c` bem-sucedido em cada um.

**Entendimento esperado:** o que chega em `production` é bit a bit o mesmo
arquivo que passou em `development`. Não foi reconstruído em cada etapa — se
fosse, "testado em staging" não provaria nada sobre production.

Dizer em voz alta, sempre: **`production` aqui é um job que registra a promoção
de um artefato fictício. Não opera nenhum serviço.**

### Etapa 9 — A release publicada

**Automático, os dois observam.**

Terminada a promoção, o workflow cria ou atualiza a GitHub Release da tag e
anexa `framework-demo.pyz`, `SOURCE_COMMIT` e `SHA256SUMS`.

**Entendimento esperado:** a release é a evidência durável. O artefato de
execução expira em 30 dias; o anexo da release permanece.

### Etapa 10 — O rollback (`RUNBOOK.md` §11)

**Owner executa, Developer observa e explica de volta.**

Depois de existir uma versão mais nova, disparar `Delivery` manualmente
(`workflow_dispatch`) apontando para a tag **anterior**.

Duas coisas a observar:

1. `staging` e `production` **pedem aprovação de novo**. Voltar atrás também é
   uma mudança e passa pelo mesmo portão.
2. **Nenhuma release é criada ou alterada.** O histórico de releases continua
   dizendo qual é a versão mais recente. Só o caminho por tag publica.

**Entendimento esperado:** o Developer consegue explicar por que o rollback
usou o `workflow_dispatch` e não uma tag nova, e por que a tag antiga nunca é
movida.

Limitação a declarar: este rollback **reconstrói a fonte** da versão anterior.
Não é a repromoção do mesmo binário já construído, e não é o rollback de um
serviço em operação.

## 5. Verificação de aprendizado

O primeiro ciclo terminou quando o Developer responde estas perguntas sem
ajuda:

1. Por que o merge estava bloqueado, e o que exatamente o desbloqueou?
2. Onde no log do CI está dito o que quebrou?
3. Como se prova que `production` recebeu o mesmo artefato que `development`?
4. Por que o rollback exigiu aprovação de novo?
5. Por que a tag antiga nunca é movida?
6. Por que `production`, aqui, não prova a operação de nenhum serviço?

A pergunta 6 não é detalhe. Confundir o job com um serviço real é o erro que
este laboratório mais precisa evitar.

## 6. O segundo ciclo: inversão

Trocar as cadeiras. O **Developer passa a revisar e aprovar**; o **Owner passa
a abrir a branch e o pull request**.

Antes do segundo ciclo, o Owner liga os controles que estavam desligados
(`ACESSOS-E-PAPEIS.md`, seção 5):

- uma aprovação obrigatória;
- aprovação de alguém diferente do último autor de push;
- review de CODEOWNER;
- `prevent_self_review` em `staging` e `production`, com o Developer como
  revisor.

Agora o laboratório demonstra o que não podia demonstrar sozinho: **separação
de funções**. Com essas regras ligadas, o Owner não consegue mais mesclar a
própria mudança em caminho protegido nem aprovar a própria promoção.

O que a inversão **não** muda: o papel técnico. Heveraldo continua Owner e
Fabiano/segundo participante continuam Collaborators, porque um repositório pessoal tem
só esses dois níveis. Uma inversão técnica de verdade exigiria uma organização.

## 7. Erros comuns e o que dizer

| Situação | O que o Owner deve dizer |
| --- | --- |
| Developer quer desligar a regra para destravar o merge | É exatamente o que não se faz. A regra está funcionando. Corrija o teste. |
| Developer acha que o CI "está com problema" | O CI executou o mesmo teste que falhou na máquina dele. Reproduza local primeiro. |
| Alguém propõe mover uma tag já enviada | Nunca. Quem já baixou aquela tag passaria a ter outro conteúdo com o mesmo nome. Crie uma versão corretiva. |
| Alguém quer commitar direto em `main` | O ruleset bloqueia. É o comportamento desejado. |
| Alguém quer anexar um log com dados reais | `AGENTS.md`: nada real ou confidencial. Repositório público, conteúdo permanente. Revisar bordas, metadados e barra de endereço antes de anexar imagem. |
| Perguntam se isto roda em produção | Não. É um job que registra promoção de um artefato fictício. |

## 8. Custo aproximado

O ciclo completo leva de 45 a 60 minutos com explicação. As etapas 1 a 6 — do
branch ao merge — levam cerca de 20 minutos e já entregam a lição central. Se o
tempo for curto, parar depois da etapa 6 e deixar promoção e rollback para uma
segunda sessão. `APRESENTACAO-10-MIN.md` tem a versão condensada para plateia.
