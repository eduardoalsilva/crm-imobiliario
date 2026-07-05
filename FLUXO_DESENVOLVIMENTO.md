# Fluxo de Desenvolvimento

## Objetivo

Padronizar a evolução do CRM Imobiliário e manter o projeto organizado.

---

## Fluxo de Trabalho

### 1. Criar ou selecionar uma Issue

Toda alteração relevante deve estar vinculada a uma Issue.

Exemplos:

- Correção de bugs
- Melhorias
- Refatorações
- Documentação

---

### 2. Mover a Issue para "Em andamento"

No GitHub Project.

---

### 3. Criar uma branch

Padrões:

Feature:

```bash
git checkout -b feature/nome-da-feature
```

Bugfix:

```bash
git checkout -b fix/nome-do-bug
```

Exemplos:

```bash
git checkout -b feature/centralizar-templates
git checkout -b feature/10-mensagens
git checkout -b fix/importacao-origem-lead
```

---

### 4. Registrar o prompt

Adicionar o prompt utilizado em:

```text
docs/VIBE_CODING.md
```

Objetivo:

- Registrar decisões
- Permitir reproduzir alterações futuras
- Manter histórico do desenvolvimento assistido por IA

---

### 5. Implementar

Executar a alteração utilizando IA ou desenvolvimento manual.

---

### 6. Testar

Validar:

- Fluxo principal
- Funcionalidade alterada
- Possíveis regressões

Pergunta obrigatória:

"Se eu fosse usar o CRM agora, funcionaria normalmente?"

---

### 7. Commit

Padrões:

Feature:

```bash
git commit -m "feat: descrição da alteração"
```

Bugfix:

```bash
git commit -m "fix: descrição da correção"
```

Documentação:

```bash
git commit -m "docs: descrição da documentação"
```

Exemplos:

```bash
git commit -m "feat: centraliza templates de mensagens"
git commit -m "fix: corrige importação da origem do lead"
git commit -m "docs: adiciona estratégia operacional do whatsapp"
```

---

### 8. Merge

Após validação:

```bash
git checkout main
git merge nome-da-branch
```

Exemplo:

```bash
git checkout main
git merge feature/centralizar-templates
```

---

### 9. Push

```bash
git push
```

---

### 10. Fechar a Issue

Adicionar comentário resumindo:

- O que foi feito
- O que foi testado
- Resultado

Mover para:

```text
Concluído
```

---

## Versionamento

Padrão:

```text
MAJOR.MINOR.PATCH
```

Exemplos:

```text
v1.0.0
v1.0.1
v1.1.0
v2.0.0
```

### PATCH

Correções.

Exemplos:

- Importação
- Filtros
- Bugs

---

### MINOR

Novas funcionalidades ou melhorias.

Exemplos:

- Novos templates
- Melhorias de operação
- Novos filtros

---

### MAJOR

Mudanças significativas.

Exemplos:

- Dashboard
- Funil comercial
- Nova arquitetura

---

## Filosofia do Projeto

Antes de implementar qualquer funcionalidade, responder:

"Isso ajuda a vender mais imóveis ou organizar melhor os leads?"

Se a resposta for não, a funcionalidade deve ser reavaliada.

---

## Princípios

- Simplicidade primeiro.
- Resolver problemas reais.
- Evitar complexidade desnecessária.
- Priorizar uso real do CRM.
- Evoluir através de pequenas melhorias contínuas.