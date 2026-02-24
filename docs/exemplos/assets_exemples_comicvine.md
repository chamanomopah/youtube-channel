● Ótima pergunta! Para o estilo "The Paint Explainer" (aquele formato de vídeos narrados com imagens estáticas, texto animado e voiceover), aqui estão os assets realmente essenciais da ComicVine API:                            
  ---                                                                                                                                                                                                                           
  🎨 ASSETS ESSENCIAIS PARA VÍDEOS ESTILO "THE PAINT EXPLAINER"
                                                                                                                                                                                                                                  1️⃣CAPAS DE ISSUES (IMAGE CARDS)                                                                                                                                                                                                

  // Endpoint: /issue
  // Campos essenciais:
  {
    "image": {
      "original_url": "URL da capa em alta resolução",
      "medium_url": "URL versão média",
      "small_url": "URL versão pequena"
    },
    "name": "Batman #1",
    "issue_number": "1",
    "cover_date": "1940-03-10"
  }

  ✅ USE PARA:
  - Cards animados mostrando a capa do quadrinho
  - Timeline visual de issues importantes
  - Mostrar a primeira aparição de um personagem

  ---
  2️⃣RETRATOS OFICIAIS DE PERSONAGENS

  // Endpoint: /character
  {
    "image": {
      "original_url": "URL do retrato oficial",
      "medium_url": "URL versão média"
    },
    "name": "Batman",
    "real_name": "Bruce Wayne",
    "deck": "Brief summary do personagem"
  }

  ✅ USE PARA:
  - Apresentar o personagem no início do vídeo
  - Cards de "Personagem do Dia"
  - Comparativos lado a lado (Hero vs Villain)

  ---
  3️⃣IMAGENS DE TIMES/EQUIPES

  // Endpoint: /team
  {
    "image": {
      "original_url": "URL da arte oficial do time"
    },
    "name": "Justice League",
    "count_of_team_members": 7
  }

  ✅ USE PARA:
  - Mostrar a formação de equipes
  - Cards de "Vingadores vs Liga da Justiça"
  - Visualizar grupos antagonistas

  ---
  4️⃣CAPAS DE VOLUMES/SÉRIES

  // Endpoint: /volume
  {
    "image": {
      "original_url": "URL da capa do volume"
    },
    "name": "Batman: The Dark Knight Returns",
    "count_of_issues": 4,
    "start_year": 1986
  }

  ✅ USE PARA:
  - Mostrar graphic novels importantes
  - Apresentar sagas completas
  - Cards de "Leitura Obrigatória"

  ---
  5️⃣IMAGENS DE CRIADORES (ROTEIRISTAS/ARTISTAS)

  // Endpoint: /person
  {
    "image": {
      "original_url": "URL da foto do criador"
    },
    "name": "Frank Miller",
    "created_characters": ["Personagens que criou"]
  }

  ✅ USE PARA:
  - Cards de "Criador do Mês"
  - Créditos no final do vídeo
  - Seções sobre "A Mente por trás dos Quadrinhos"

  ---
  6️⃣ARTES DE CONCEITOS/ITENS/LOCATIONS

  // Endpoints: /concept, /object, /location
  {
    "image": {
      "original_url": "URL da arte oficial"
    },
    "name": "Mjolnir",
    "description": "Descrição completa"
  }

  ✅ USE PARA:
  - Explicar itens lendários (Mjolnir, Escudo do Capitão)
  - Mostrar locais icônicos (Gotham, Asgard)
  - Conceitos importantes (Multiverso, Force)

  ---
  🎯 ESTRUTURA IDEAL DE ASSETS POR VÍDEO

  Tipo 1: "HISTÓRIA DE UM PERSONAGEM"

  ✓ 1 imagem do personagem (hero shot)
  ✓ 3-5 capsas de issues importantes (primeira aparição, morte, ressurreição)
  ✓ 2-3 imagens de aliados/inimigos
  ✓ 1 imagem do criador (opcional)

  Tipo 2: "EXPLICANDO UMA SAGA"

  ✓ Capa do primeiro issue da saga
  ✓ 3-5 capsas dos issues mais importantes
  ✓ Imagens dos personagens principais
  ✓ 1 imagem do volume completo (graphic novel)

  Tipo 3: "COMPARATIVO: HERO vs VILLAIN"

  ✓ 1 imagem do herói
  ✓ 1 imagem do vilão
  ✓ 3 capas de comics onde se enfrentaram
  ✓ Imagem do time de cada um (se aplicável)

  Tipo 4: "TOP 10 COISAS"

  ✓ Imagem de capa para cada item da lista
  ✓ 1 imagem de thumb para cada card
  ✓ Imagem do personagem central (se aplicável)

  ---
  📦 API CALLS OTIMIZADOS (SÓ O NECESSÁRIO)

  Para CAPAS (IMAGE CARDS):

  // GET /issues
  // ?field_list=image,name,issue_number,cover_date
  // &filter=volume:4050  // Batman volume ID
  // &limit=10

  ✅ RETORNA:
  {
    "results": [
      {
        "image": { "original_url": "..." },
        "name": "Batman #1",
        "issue_number": "1",
        "cover_date": "1940-03-10"
      }
    ]
  }

  Para RETRATOS de PERSONAGENS:

  // GET /characters
  // ?field_list=image,name,real_name,deck
  // &filter=name:Batman

  ✅ RETORNA:
  {
    "results": [
      {
        "image": { "original_url": "..." },
        "name": "Batman",
        "real_name": "Bruce Wayne",
        "deck": "O Cavaleiro das Trevas..."
      }
    ]
  }

  Para STORY ARCS (SAGAS):

  // GET /story_arc
  // ?field_list=image,name,description,issues
  // &id=12345

  ✅ RETORNA:
  {
    "results": {
      "image": { "original_url": "..." },
      "name": "Batman: Knightfall",
      "description": "Bane quebra a Batman...",
      "issues": [ /* lista de issues */ ]
    }
  }

  ---
  🎬 WORKFLOW RECOMENDADO

  1️⃣PLANEJAMENTO

  - Decidir o tipo de vídeo (Personagem, Saga, Comparativo)
  - Listar personagens/issues necessários

  2️⃣COLETA DE ASSETS

  // Buscar ID do personagem
  GET /search?query=Batman&resources=character

  // Buscar imagem do personagem
  GET /character/4050?field_list=image,name,real_name

  // Buscar primeiras aparições
  GET /issues?filter=first_appearance_characters:4050&limit=5

  // Buscar issues importantes
  GET /issues?filter=volume:4050&limit=10&sort=cover_date:asc

  3️⃣DOWNLOAD ORGANIZADO

  /assets
    /characters
      batman-main.jpg
      joker.jpg
    /issues
      batman-#1-cover.jpg
      batman-#42-cover.jpg
    /teams
      justice-league.jpg

  4️⃣USO NO REMOTION

  // No seu componente Remotion
  import batmanMain from "../assets/characters/batman-main.jpg";
  import batman1 from "../assets/issues/batman-#1-cover.jpg";

  <Img src={batmanMain} />

  ---
  ⚡ DICAS PRO

  ✅ SEMPRE BUSCAR EM ALTA RESOLUÇÃO

  ?field_list=image  // Inclui todas as resoluções
  // Usar: image.original_url para melhor qualidade

  ✅ CACHE DE IMAGENS

  - Salvar localmente para não chamar a API toda vez
  - Organizar por nome do personagem/issue

  ✅ METADADOS IMPORTANTES

  // Adicionar ao nome do arquivo para contexto:
  batman-#1-1940-03-10-first-appearance.jpg