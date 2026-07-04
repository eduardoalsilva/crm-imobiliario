# Vibe Coding

## Issue #1 - Centralizar templates de mensagens

### Contexto

Atualmente as mensagens de primeiro contato estão distribuídas em múltiplos arquivos .txt.

### Objetivo

Centralizar todas as mensagens em uma única estrutura para facilitar manutenção e expansão.

### Prompt

Refatore o sistema de mensagens do CRM.

Contexto:
Atualmente as mensagens de primeiro contato estão distribuídas em múltiplos arquivos .txt.

Objetivo:
Centralizar todas as mensagens em uma única estrutura.

Requisitos:
- Utilizar um único arquivo mensagens.json.
- Manter compatibilidade com o fluxo atual.
- Continuar selecionando uma mensagem aleatória.
- Não alterar a forma como o usuário utiliza o CRM.
- Não alterar a geração do link do WhatsApp.
- Não alterar a personalização com nome do lead.

Critérios de conclusão:
- Todas as mensagens estão armazenadas em mensagens.json.
- O sorteio continua funcionando.
- O comportamento do sistema permanece igual para o usuário.