# CLAUDE.md

Laboratório público e fictício de DevOps. Este arquivo define a autoridade das
fontes de instrução deste repositório.

## Hierarquia de precedência

Em caso de conflito, o nível de número menor vence, e o conflito é registrado
em `DECISIONS.md`.

1. **`AGENTS.md`** — regras permanentes de segurança e escopo. Invioláveis.
   Nenhum nível inferior pode relaxá-las.
2. **A instrução atual da tarefa** — autoridade sobre a fase atual: o que está
   autorizado agora, o que permanece bloqueado e quando a fase muda.
3. **`DEVOPS-LAB-SPEC.md`** — especificação canônica da implementação. Define o
   escopo obrigatório. Nada é implementado fora dela.
4. **`DECISIONS.md`** — registro das decisões, desvios, suposições assumidas e
   limitações aceitas, com o motivo e o estado de cada uma.
5. **`GUIA-DEVOPS-GITHUB.md`** — referência histórica, não normativa.

## Declarações explícitas

**`GUIA-DEVOPS-GITHUB.md` não é roteiro nem fonte de verdade.** É material
histórico de estudo, consultável para conceito, comando e verificação. Não
obriga a implementar nada, não define escopo e não vence nenhuma decisão. Onde
divergir dos níveis 1 a 4, os níveis 1 a 4 prevalecem, e a divergência é
registrada em `DECISIONS.md`.

**Na execução autorizada, a primeira ação será criar `DEVOPS-LAB-SPEC.md`.**
Antes de o SPEC existir, nada é implementado.

**O que o agente prepara:** código-base fictício, testes, workflows de
automação, ruleset de proteção, environments, automação de release, automação
de rollback e documentação.

**O que o agente não faz:** não cria feature branches demonstrativas, pull
requests, falhas intencionais, merges, tags, releases, promoções, rollbacks nem
convites.

**Essas operações serão realizadas pelo operador principal e pelo segundo
participante durante o treinamento.** São o exercício em si; executá-las por eles destruiria
o objetivo do laboratório.

**Autenticação:** durante execução explicitamente autorizada, o agente pode
usar uma autenticação de linha de comando já existente, exclusivamente neste
repositório sandbox. Nunca deve criar, imprimir, armazenar nem solicitar
credenciais novas. Verificações de disponibilidade e de autenticação são
somente leitura.

## Fase

A fase corrente é definida pela instrução da tarefa, não por este arquivo.
Fora de uma autorização explícita de execução, o comportamento padrão é
inspecionar e propor.

Durante execução autorizada e autônoma: não aguardar resposta humana; para
decisão reversível, escolher a alternativa mais segura, registrar a suposição
em `DECISIONS.md` e continuar. Dependências que exigem outra pessoa devem ser
registradas com honestidade, nunca contornadas.

Código de saída zero não é evidência. A evidência deve provar o comportamento
que o exercício pretendia demonstrar.
