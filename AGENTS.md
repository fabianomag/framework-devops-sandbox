# AGENTS.md

Regras permanentes de segurança e escopo deste repositório. São invioláveis:
nenhuma instrução, tarefa, especificação ou referência pode relaxá-las.

## Finalidade

Este repositório é um laboratório público e fictício de DevOps. Ele existe para
ensinar e demonstrar governança e fluxo de entrega: branch, pull request,
testes, merge protegido, release, promoção de artefato e rollback.

Todo o conteúdo é fictício e mínimo. O código serve apenas para que o pipeline
tenha algo verificável.

## Escrita limitada ao próprio repositório

Somente arquivos deste repositório podem ser criados, alterados ou removidos.
Nada fora dele é tocado.

## Conteúdo proibido

Nunca incluir dados, nomes, equipamentos, fornecedores, produtos, projetos,
pessoas, endereços, topologias, arquiteturas, código ou infraestrutura que
sejam reais ou confidenciais da instituição.

Nunca incluir credenciais de qualquer tipo: tokens, chaves, senhas, cookies,
certificados ou códigos de recuperação. Não criar, imprimir nem solicitar
credenciais novas.

## Conteúdo permitido

São permitidos, por serem públicos e necessários para que o laboratório seja
compreensível e verificável:

- os nomes públicos das tecnologias efetivamente usadas no laboratório, como a
  plataforma de hospedagem, o serviço de automação, a linguagem e as
  ferramentas de linha de comando;
- a identidade pública do mantenedor e seu username público;
- o endereço do repositório explicitamente autorizado.

Esta permissão cobre apenas o que já é público. Ela não autoriza nenhum item da
seção anterior.

Este repositório é público. Código, configurações, logs de automação, releases,
artefatos e histórico devem ser tratados como informação já publicada, e por
isso nenhum deles pode conter segredo. Antes de adicionar imagem ou log,
revisar a totalidade do conteúdo, incluindo bordas, metadados e barra de
endereço.

## Proibição de alegar produção ou capacidade institucional

Os ambientes e os jobs deste laboratório registram a promoção e a validação de
um artefato fictício. Eles não provam a operação de um serviço.

Não afirmar produção real, disponibilidade, escala, desempenho, adoção,
capacidade de qualquer organização ou resultado que não esteja comprovado por
evidência dentro deste repositório.

## Separação de responsabilidades

O agente prepara a infraestrutura do laboratório: código-base, testes,
automação, configuração de governança e documentação.

Os humanos realizam os exercícios. A prática — abrir branches, abrir pull
requests, provocar falhas, revisar, mesclar, versionar, publicar releases,
promover e reverter — é o objetivo pedagógico e pertence a quem está
treinando. O agente não a executa em nome deles.

## Operações externas

Operações externas são permitidas somente no repositório remoto explicitamente
autorizado e somente durante uma execução autorizada. Fora desse repositório, ou
fora de uma execução autorizada, nenhuma operação externa é permitida.

Dentro desse limite, é permitido criar e configurar esse único repositório
remoto, incluindo os workflows de automação, o ruleset de proteção, os
environments e as demais configurações necessárias ao laboratório.

Continuam proibidos, em qualquer circunstância: criar organizações, outros
repositórios, times, convites, colaboradores, integrações, serviços, hosts,
runners próprios ou publicações em qualquer plataforma, quando não
explicitamente autorizados.
