---
description: Modifica comandos existentes de forma precisa e mínima
argument-hint: [comando-alvo] [modificações]
allowed-tools: Read, Edit, Glob, AskUserQuestion
disable-model-invocation: false
---

# Modificar Comando Slash

Modifica comandos slash existentes alterando **apenas** o especificado pelo usuário.

## Contexto
- **Comando alvo**: $1 (nome do comando a ser modificado, ex: `commit`, `fix-issue`)
- **Modificações**: $2 (descrição das alterações desejadas)

## Localização

Buscar comando nesta ordem:
1. Diretório do projeto: `.claude/commands/[comando].md`
2. Diretório pessoal: `C:\.nero\.claude\commands/[comando].md`
3. Com namespace: `C:\.nero\.claude\commands/[namespace]/[comando].md`

## Princípios de Modificação

**Regra de ouro**: PRESERVAR tudo que não foi explicitamente solicitado para mudança.

**Exemplos**:
- Usuário pede "adicionar argument-hint" → apenas adicione `argument-hint`, mantenha resto intacto
- Usuário pede "mudar descrição" → modifique apenas `description`, preserve formatação
- Usuário pede "adicionar tool Write" → apenas adicione `Write` ao `allowed-tools`

## Processo

1. **Ler** arquivo completo do comando
2. **Identificar** partes a modificar (frontmatter e/ou corpo)
3. **Usar Edit tool** com old_string/new_string precisos
4. **Validar** que apenas mudanças solicitadas foram aplicadas

## Saída

Relatório de modificação:
- **Arquivo**: caminho completo
- **Propriedades alteradas**: lista de modificações (valor antigo → novo)
- **Conteúdo**: linhas modificadas
- **Estrutura preservada**: confirmar YAML válido, instruções originais mantidas
- **Teste sugerido**: comando de teste

## Exemplos de Uso

```
/modificar-comando commit "adicionar argument-hint [message]"
/modificar-comando review "adicionar tool Write no allowed-tools"
/modificar-comando test "mudar descrição para incluir E2E"
/modificar-comando deploy "adicionar contexto de env vars"
```

## Cuidados

- **NUNCA** reescrever o comando inteiro
- **NUNCA** "melhorar" ou "otimizar" não solicitado
- **SEMPRE** usar Edit com old_string/new_string precisos
- **SEMPRE** confirmar modificação mínima
