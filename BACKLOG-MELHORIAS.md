# BACKLOG-MELHORIAS.md

O que ficou deliberadamente fora do escopo. Nada aqui entra sem passar antes
por `DEVOPS-LAB-SPEC.md`.

## Governança

| Item | Por que ficou fora | Ganho quando entrar |
| --- | --- | --- |
| `required_approving_review_count: 1` com aprovação de alguém diferente do último autor de push | Trava todos os merges com um único participante ativo | Separação de funções real, não apenas o mecanismo |
| `require_code_owner_review: true` | Mesmo motivo | O arquivo `CODEOWNERS` passa a ter efeito |
| `Prevent self-review` em `staging` e `production` | Impede qualquer promoção sem um segundo aprovador | Aprovação independente de deployment |
| Ruleset de tags para o padrão `v*` | Não pertence à jornada mínima | Impede mover ou apagar versão publicada |
| Exercício de remoção de acesso | Exige uma terceira pessoa consentindo | Demonstra revogação e o que a revogação não desfaz |

## Automação

| Item | Por que ficou fora | Ganho quando entrar |
| --- | --- | --- |
| ~~Fixar as Actions por SHA completo~~ | **FEITO em 2026-08-05.** As cinco Actions estão fixadas por SHA de 40 caracteres, com o comentário da versão ao lado. Ver `HANDOFF.md` §3 | — |
| `dependabot.yml` para GitHub Actions | O pinning por SHA, do qual dependia, já existe. Ficou fora por ser ruído durante o treinamento: abriria pull requests automáticos competindo com os dos participantes | Atualizações do SHA chegam por pull request revisável, em vez de manuais |
| Revisão de `Settings` -> `Actions` -> `General` | Não é pré-requisito da jornada | Restringe quais Actions podem executar |
| Geração de changelog a partir dos pull requests | O volume de mudanças ainda é pequeno demais | Notas de release reproduzíveis |
| Cache de dependências no CI | Não há dependências externas | Nada hoje; relevante só se o exemplo crescer |

## Evolução técnica

| Item | Por que ficou fora | Ganho quando entrar |
| --- | --- | --- |
| Imagem de contêiner publicada em registry, com promoção por digest | Fora do escopo declarado | Resolve a limitação central do rollback atual: promover o mesmo binário em vez de reconstruir a fonte |
| Ambiente de execução persistente com URL | Fora do escopo declarado | Permitiria falar de operação real, não de simulação |
| Matriz de versões de Python no CI | Uma versão basta para a jornada | Cobertura de compatibilidade |
| Verificação de assinatura ou atestação de proveniência do artefato | Um degrau acima do objetivo atual | Cadeia de suprimentos verificável |

## Documentação

| Item | Por que ficou fora | Ganho quando entrar |
| --- | --- | --- |
| Série de textos por etapa | O tempo disponível foi para a jornada executável | Registro público do aprendizado |
| Registro de erros reais encontrados durante os exercícios | Só existe depois que os exercícios forem executados | Troubleshooting baseado em fato, não em previsão |
