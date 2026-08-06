# framework-devops-sandbox

Laboratório público e fictício de DevOps no GitHub.

Este repositório existe para ensinar e demonstrar uma jornada de entrega
completa:

```text
branch -> pull request -> testes -> merge protegido -> release
       -> promoção do mesmo artefato -> rollback auditável
```

## O que ele é

Um exemplo mínimo e fictício. A aplicação é uma CLI com dois comandos e nenhuma
dependência externa, escrita apenas para que o pipeline tenha algo verificável.

```bash
python3 -m src.framework_demo health
python3 -m src.framework_demo version
python3 -m unittest discover -s tests -v
```

## O que ele não é

Não é um sistema real, não representa nenhuma instituição e não opera nenhum
serviço. O job chamado `production` registra a promoção e a validação de um
artefato fictício dentro de uma execução; ele não prova a operação de um
serviço em produção.

O exercício de rollback reconstrói a fonte da versão anterior. Não é a promoção
do mesmo digest binário.

## Comece por aqui

**[`COMECE-AQUI.md`](COMECE-AQUI.md)** — guia prático para a demonstração. O
fluxo usa a interface do GitHub; a criação da tag anotada usa um único comando
de terminal, pois o botão de release do GitHub cria tag leve e este laboratório
a recusa deliberadamente.

## Estado atual

A infraestrutura está pronta: os workflows `CI` e `Delivery`, o ruleset
`protect-main` exigindo o check `test-python`, e os ambientes `development`,
`staging` e `production`.

O estado verificável — branches, pull requests, tags, releases e promoções — é
registrado em [`HANDOFF.md`](HANDOFF.md). As configurações remotas pertencem a
`@Heveraldoo`; `@fabianomag` atua como colaborador com escrita e instrutor do
laboratório.

## Como está organizado

| Arquivo | Conteúdo |
| --- | --- |
| `AGENTS.md` | regras permanentes de segurança e escopo |
| `CLAUDE.md` | hierarquia de autoridade das instruções |
| `DEVOPS-LAB-SPEC.md` | especificação canônica da implementação |
| `RUNBOOK.md` | procedimento humano, comando a comando |
| `LAB-OWNER-DEVELOPER.md` | roteiro do treinamento a dois, etapa por etapa |
| `ACESSOS-E-PAPEIS.md` | quem tem qual acesso e o que ele realmente permite |
| `DECISIONS.md` | decisões, desvios e suposições registradas |
| `BACKLOG-MELHORIAS.md` | o que ficou fora do escopo e por quê |
| `APRESENTACAO-10-MIN.md` | roteiro de demonstração |
| `HANDOFF.md` | estado atual e bloqueios |

## Licença

MIT. Ver `LICENSE`.
