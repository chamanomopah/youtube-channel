Melhor estratégia para implementar isso:                                                                                                                                                                      
A estratégia é "Fit-to-Container" (adaptar ao recipiente)                                             
                                                                                                    
1. Delimitar o espaço com margens fixas (padding) - isso cria o "copo"
2. Calcular automaticamente:
- Quantidade de covers
- Proporção do espaço disponível
- Número ótimo de colunas baseado em aspect ratio
3. Expandir as covers para ocupar o máximo de espaço (como água enchendo o copo)
4. Labels ficam proporcionais ao tamanho da cover

Por que essa abordagem é profissional:

- ✅ Funciona com qualquer quantidade de covers
- ✅ Adapta-se a diferentes resoluções
- ✅ Sem "números mágicos" hardcoded
- ✅ As covers se "expandid" como água no recipiente

shorthand properties simplify how you control padding