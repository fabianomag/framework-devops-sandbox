# APRESENTACAO-10-MIN.md

Roteiro cronometrado. Total: 10 minutos.

Regra única: mostrar evidência já existente e executar ao vivo apenas o
rollback. Uma demonstração que depende de sete execuções ao vivo depende de
fila de runner e de rede, e nenhuma das duas está sob controle de quem
apresenta.

Deixar abertas, antes de começar: a aba do pull request bloqueado, a aba do
ruleset, a aba da execução de promoção e a aba de releases.

## 0:00 - 1:00 — O problema

"Todo mundo sabe que boa prática é abrir pull request e rodar teste. A pergunta
é outra: o que acontece quando alguém decide não fazer isso? Se a resposta
depende de disciplina, não é governança. Este laboratório é sobre transformar
boa prática em regra verificável."

Declarar os limites de uma vez, antes que perguntem: exemplo fictício, nenhum
dado real, nenhum serviço em operação.

## 1:00 - 2:30 — Branch, pull request e CI vermelho

Mostrar o pull request com o check `test-python` vermelho e abrir o log até a
linha da falha.

"O teste falhou pelo motivo previsto. Isso importa: um check que fica verde
sempre não é um controle, é decoração."

## 2:30 - 4:00 — A regra que bloqueia

Mostrar o botão de merge bloqueado e, em seguida, o ruleset `protect-main`.

"O merge não está bloqueado porque eu decidi esperar. Está bloqueado porque
existe uma regra ativa que exige o check verde, exige pull request, exige
histórico linear e bloqueia force push. Eu, como administrador, consigo alterar
essa regra — e é por isso que a alteração dela fica registrada."

Ponto honesto, dito por iniciativa própria: "a aprovação obrigatória por uma
segunda pessoa está desligada, porque hoje só existe um participante ativo. O
mecanismo está provado; a separação de funções é dependência de processo, não
dificuldade técnica."

## 4:00 - 5:00 — Verde e merge

Mostrar a correção, o check verde e o merge por squash. Mostrar o histórico
linear de `main`.

## 5:00 - 6:00 — Tag não é release

Mostrar a tag anotada e a release com os três assets anexados.

"A tag é tratada neste laboratório como ponto imutável do histórico; ainda não
há ruleset técnico para proteger tags. A release é a decisão de distribuir
aquele ponto. São coisas diferentes, e misturar as duas é como se perde
rastreabilidade."

## 6:00 - 8:00 — Um artefato, três ambientes

Abrir a execução de `Delivery`. Mostrar que `build` roda uma vez e que
`development`, `staging` e `production` apenas baixam o mesmo artefato.

Mostrar o mesmo `SOURCE_COMMIT` e o mesmo checksum nos três jobs, e a tela de
espera por aprovação.

"O que é promovido é o artefato, não o código. Se cada ambiente construísse de
novo, eu não teria como afirmar que o que foi validado em `staging` é o mesmo
que chegou em `production`."

## 8:00 - 10:00 — Rollback ao vivo, e o que ele não prova

Disparar `Delivery` com `source_ref: v0.1.0` enquanto a versão corrente é
`v0.1.1`. Aprovar. Mostrar o smoke test devolvendo a versão anterior.

"Repare que voltar também exigiu aprovação. Rollback não é um atalho fora do
processo."

Fechar com a limitação, antes que seja apontada: "isto reconstrói a fonte da
versão anterior. Não é a promoção do mesmo digest binário, e não é rollback de
um serviço em operação — não existe serviço aqui. O próximo degrau seria
publicar uma imagem em registry e promover por digest."

## Perguntas prováveis

| Pergunta | Resposta curta |
| --- | --- |
| Isso é produção? | Não. O job se chama `production` e registra promoção de artefato. Não há serviço, host nem URL. |
| Quem aprova? | Hoje, o mantenedor. Com um segundo participante, a regra passa a exigir aprovação independente. |
| E se alguém apagar `main`? | O ruleset bloqueia exclusão e force push. |
| Por que o teste é tão pequeno? | Porque o objeto de estudo é o pipeline, não o código. Um exemplo maior esconderia o mecanismo. |
| E se o CI ficar verde por engano? | Por isso o exercício inclui uma falha intencional: um check só vale se já se provou capaz de ficar vermelho. |
| Dá para burlar? | O administrador pode alterar a regra. A diferença é que alterar deixa registro, e trabalhar em volta dela não é mais o caminho de menor esforço. |
