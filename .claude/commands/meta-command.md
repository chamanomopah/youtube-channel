# Criar Comando Slash Personalizado

Cria slash commands para Claude Code seguindo melhores práticas e especificações técnicas da documentação oficial. Use este comando quando precisar criar novos comandos personalizados com suporte a argumentos, frontmatter YAML, execução de bash e recursos avançados. caso o comando tiver com algum mcp como supabase mcp ou n8n mcp, adiciona apenas as tools necessarias pra aquele comando funcionar corretamente não adicionae uso de tools desnecessarias pra ele 

## Contexto & Variáveis

**arquivo_destino**: caminho completo onde o comando será salvo (.claude/commands/ ou ~/.claude/commands/)
**descricao_comando**: descrição clara do que o comando deve fazer
**tipo_comando**: project (compartilhado via git) ou personal (disponível em todos projetos)

## Análise & Planejamento

### 1. Definição do Comando
- Analisar o propósito e casos de uso do comando
- Identificar tipo (project vs personal) e localização adequada
- Determinar necessidade de argumentos e parâmetros
- Planejar estrutura de nomes e namespacing

### 2. Especificação Técnica
- Definir frontmatter YAML (description, argument-hint, allowed-tools)
- Planejar tratamento de argumentos ($ARGUMENTS ou posicionais $1, $2, etc.)
- Identificar ferramentas necessárias (Bash, Read, Write, etc.)
- Determinar se há necessidade de execução de comandos bash

## Execução & Construção

### 3. Estrutura Básica
Criar arquivo markdown com:
- **Nome do arquivo**: `nome-do-comando.md`
- **Invocação**: `/nome-do-comando [argumentos]`
- **Namespacing opcional**: `.claude/commands/namespace/comando.md` → `/comando (project:namespace)`

### 4. Frontmatter YAML (Opcional mas Recomendado)

```yaml
---
description: Breve descrição do comando (aparece no /help)
argument-hint: [param1] [param2]  # Hint para auto-complete
model: claude-3-5-5-sonnet-20250122  # Modelo específico (opcional)
allowed-tools: Bash(git add:*), Bash(git status:*), Read, Write  # Ferramentas permitidas
disable-model-invocation: false  # true = previne invocação via SlashCommand tool
---
```

### 5. Tratamento de Argumentos

**Opção A - Todos os argumentos ($ARGUMENTS):**
```
Fix issue #$ARGUMENTS following our coding standards
Uso: /fix-issue 123 high-priority → $ARGUMENTS = "123 high-priority"
```

**Opção B - Argumentos posicionais ($1, $2, $3):**
```
---
argument-hint: [pr-number] [priority] [assignee]
---
Review PR #$1 with priority $2 and assign to $3
Uso: /review-pr 456 high alice → $1="456", $2="high", $3="alice"
```

### 6. Recursos Avançados

**A) Execução de Comandos Bash:**
```yaml
---
allowed-tools: Bash(git status:*), Bash(git diff:*)
---
```
```
## Context
- Current git status: \`git status\`
- Current diff: \`git diff HEAD\`

## Your task
Based on the above changes, create a commit.
```

**B) Referências de Arquivo (@):**
```
Review the implementation in @src/utils/helpers.js
Compare @src/old-version.js with @src/new-version.js
```

**C) Extended Thinking (tarefas complexas):**
Incluir palavras-chave de "extended thinking" para ativar raciocínio profundo

### 7. Exemplos de Referência

**Comando Simples:**
```yaml
---
description: Create a git commit with conventional commit format
argument-hint: [message]
---
Create a git commit with message: $ARGUMENTS
Use conventional commit format: type(scope): description
```

**Comando com Bash:**
```yaml
---
description: Analyze project dependencies and suggest updates
allowed-tools: Bash(npm list:*), Bash(npm outdated:*), Read
---
## Current Dependencies
\`npm list --depth=0\`

## Outdated Packages
\`npm outdated\`

## Task
Analyze the dependencies above and suggest safe updates.
```

**Comando Parametrizado:**
```yaml
---
argument-hint: [feature-name] [ticket-id]
description: Create feature branch following team conventions
allowed-tools: Bash(git checkout:*), Bash(git branch:*)
---
Create feature branch: feature/$2-$1
Then create initial commit: "feat: Initialize $1 [$2]"
```

### 8. Namespacing e Conflitos
- Subdiretórios criam namespaces: `.claude/commands/frontend/test.md` → `/test (project:frontend)`
- Comandos de projeto sobrescrevem comandos pessoais com mesmo nome
- Comandos em subdiretórios diferentes podem ter mesmo nome

### 9. SlashCommand Tool (Invocação Automática)
- Claude pode invocar comandos automaticamente via ferramenta SlashCommand
- Mencionar comando com `/` no prompt encoraja uso
- Comandos devem ter `description` no frontmatter para serem invocáveis
- Desabilitar invocação: `disable-model-invocation: true`

## Validação & Teste

### 10. Verificação de Qualidade
- Listar comandos disponíveis: `/help`
- Verificar se frontmatter YAML é válido
- Verificar permissões de ferramentas em `allowed-tools`
- Testar com diversos argumentos e cenários

### 11. Diferenciação Skills vs Slash Commands
- **Use Slash Commands**: Prompts rápidos e frequentes, invocação explícita, um arquivo único
- **Use Skills**: Workflows complexos, múltiplos arquivos, descoberta automática por contexto

## Entrega & Finalização

### 12. Entregáveis
- [ ] Estrutura de diretório definida (project ou personal)
- [ ] Arquivo `.md` completo com frontmatter
- [ ] Tratamento de argumentos implementado (se aplicável)
- [ ] Comandos bash configurados (se aplicável)
- [ ] Instruções de teste documentadas
- [ ] Documentação de uso clara

## Relatório de Resultados

Após criar o comando, confirme:
- Arquivo criado em: `caminho/do/arquivo/nome-do-comando.md`
- Comando pode ser invocado com: `/nome-do-comando [argumentos]`
- Funcionalidades implementadas: [lista de features]
- Próximos passos para teste e validação
