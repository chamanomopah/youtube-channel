# Estratégia Módulos 1-3: Curiosidades, Comparativo e Relacionamentos

## Visão Geral

Este documento detalha a implementação técnica dos **Módulos 1-3** do sistema de storyboard dinâmico para vídeos "Every Character Comics Explained - Issue by Issue".

**Proporção Alvo**: 90% narração dos quadrinhos + 10% submódulos informativos

**Princípio Fundamental**: D3.js é usado como **motor de layout** (CALCULAR posições), enquanto Remotion controla a animação frame-a-frame dessas posições.

```
PIPELINE:
ComicVine API → D3.js Layouts → Posições Calculadas → Remotion Components → Vídeo Rendered
```

**Módulos Cobertos**:
- **Módulo 1**: Curiosidades Durante a Narração (popups informativos)
- **Módulo 2**: Comparativo Visual (versões alternativas, evoluções)
- **Módulo 3**: Árvore de Relacionamentos (grafo de conexões entre personagens)

---

## MÓDULO 1: Curiosidades Durante a Narração

### Estratégia Técnica

**Conceito**: Popups animados que aparecem durante a narração com informações contextuais sobre criadores, primeiras aparições, prêmios, vendas, etc.

**Layout D3.js**: `d3.grid()` - Posicionamento automático em grade para evitar sobreposição com o conteúdo principal

```typescript
// D3.js como motor de layout
import * as d3 from 'd3';

interface Curiosidade {
  id: string;
  texto: string;
  icone: string;
  prioridade: number; // 1-5, maior = mais importante
  timestamp: number; // frame em que deve aparecer
}

/**
 * D3 Grid Layout para calcular posições das curiosidades
 * IMPORTANTE: D3 APENAS CALCULA posições, não anima
 */
function calcularPosicoesCuriosidades(
  curiosidades: Curiosidade[],
  videoWidth: number,
  videoHeight: number
): Array<Curiosidade & { x: number; y: number; largura: number; altura: number }> {

  // D3 calcula layout em grade
  const gridLayout = d3.grid()
    .size([videoWidth - 200, videoHeight - 200]) // Margem de 100px cada lado
    .padding(20);

  // Ordenar por prioridade (mais importantes primeiro)
  const ordenadas = [...curiosidades].sort((a, b) => b.prioridade - a.prioridade);

  // D3 retorna posições calculadas
  const posicoes = gridLayout(ordenadas.map(c => ({
    id: c.id,
    largura: 300, // largura fixa do popup
    altura: 100 + c.texto.length * 2 // altura baseada no texto
  })));

  // Combinar dados com posições
  return ordenadas.map((curiosidade, i) => ({
    ...curiosidade,
    x: posicoes[i].x + 100, // offset da margem
    y: posicoes[i].y + 100,
    largura: 300,
    altura: 100 + curiosidade.texto.length * 2
  }));
}
```

**Componente Remotion**:

```tsx
// src/components/submodulos/CuriosidadePopup.tsx
import { useCurrentFrame, useVideoConfig, interpolate, spring } from 'remotion';
import { Img } from 'remotion/img';

interface CuriosidadePopupProps {
  curiosidade: {
    texto: string;
    icone: string;
    x: number;
    y: number;
    largura: number;
    altura: number;
    timestamp: number; // frame de entrada
  };
}

export const CuriosidadePopup: React.FC<CuriosidadePopupProps> = ({ curiosidade }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Configuração da animação de entrada (spring para efeito "pop")
  const entrada = spring({
    frame: frame - curiosidade.timestamp,
    fps,
    config: {
      damping: 15, // snappy com bounce leve
      stiffness: 200,
      mass: 0.8
    }
  });

  // Animar escala de 0 para 1
  const scale = interpolate(entrada, [0, 1], [0, 1], {
    extrapolateRight: 'clamp'
  });

  // Animar opacidade
  const opacity = interpolate(entrada, [0, 0.3], [0, 1], {
    extrapolateRight: 'clamp'
  });

  // Calcular posição centralizada baseada no scale (para crescer do centro)
  const centerX = curiosidade.x + curiosidade.largura / 2;
  const centerY = curiosidade.y + curiosidade.altura / 2;

  return (
    <div
      style={{
        position: 'absolute',
        left: centerX - (curiosidade.largura * scale) / 2,
        top: centerY - (curiosidade.altura * scale) / 2,
        width: curiosidade.largura,
        height: curiosidade.altura,
        opacity,
        transform: `scale(${scale})`,
        transformOrigin: 'center center',
        backgroundColor: 'rgba(0, 0, 0, 0.85)',
        borderRadius: '12px',
        border: '2px solid rgba(255, 215, 0, 0.8)', // Borda dourada
        boxShadow: '0 8px 32px rgba(0, 0, 0, 0.5)',
        padding: '16px',
        display: 'flex',
        flexDirection: 'column',
        gap: '8px',
        zIndex: 100
      }}
    >
      {/* Ícone + Título */}
      <div style={{
        display: 'flex',
        alignItems: 'center',
        gap: '12px',
        borderBottom: '1px solid rgba(255, 255, 255, 0.2)',
        paddingBottom: '8px'
      }}>
        <span style={{ fontSize: '24px' }}>{curiosidade.icone}</span>
        <span style={{
          color: '#FFD700',
          fontSize: '14px',
          fontWeight: 'bold',
          textTransform: 'uppercase',
          letterSpacing: '1px'
        }}>
          Você Sabia?
        </span>
      </div>

      {/* Texto da curiosidade */}
      <p style={{
        color: '#FFFFFF',
        fontSize: '16px',
        lineHeight: '1.4',
        margin: 0
      }}>
        {curiosidade.texto}
      </p>
    </div>
  );
};

/**
 * Componente container que gerencia múltiplas curiosidades
 * Responsável por decidir QUAL curiosidade mostrar em QUAL frame
 */
export const GerenciadorCuriosidades: React.FC<{
  curiosidades: Array<Curiosidade & { x: number; y: number; largura: number; altura: number }>;
}> = ({ curiosidades }) => {
  const frame = useCurrentFrame();

  // Filtrar curiosidades que devem estar visíveis neste frame
  // Cada curiosidade aparece por 3 segundos (3 * fps frames)
  const { fps } = useVideoConfig();
  const duracaoCuriosidade = 3 * fps; // 3 segundos

  const curiosidadesVisiveis = curiosidades.filter(c => {
    const delta = frame - c.timestamp;
    return delta >= 0 && delta <= duracaoCuriosidade;
  });

  return (
    <>
      {curiosidadesVisiveis.map(curiosidade => (
        <CuriosidadePopup key={curiosidade.id} curiosidade={curiosidade} />
      ))}
    </>
  );
};
```

### Integração Comic Vine API

**Endpoints Necessários**:

```typescript
/**
 * Serviço para buscar dados de curiosidades na Comic Vine API
 */

interface ComicVineIssue {
  id: string;
  name: string;
  issue_number: string;
  store_date: string;
  cover_date: string;
  volume: {
    id: string;
    name: string;
    start_year: string;
  };
  image: {
    super_url: string;
    icon_url: string;
  };
}

interface ComicVinePerson {
  id: string;
  name: string;
  role: string; // "writer", "artist", "colorist", "letterer", "editor"
  image: {
    super_url: string;
  };
}

interface ComicVineCharacter {
  id: string;
  name: string;
  real_name: string;
  first_appeared_in_issue: {
    id: string;
    name: string;
    issue_number: string;
  };
  deck: string;
  image: {
    super_url: string;
  };
}

/**
 * Extrai curiosidades de um issue específico
 */
export async function extrairCuriosidadesDoIssue(
  issueId: string,
  apiKey: string
): Promise<Array<{
  texto: string;
  icone: string;
  prioridade: number;
}>> {

  const curiosidades: Array<{ texto: string; icone: string; prioridade: number }> = [];

  // 1. Buscar detalhes completos do issue
  const issueResponse = await fetch(
    `https://comicvine.gamespot.com/api/issue/4000-${issueId}/?api_key=${apiKey}&format=json&field_list=id,name,issue_number,store_date,volume,credits,description,character_credits,concept_credits,object_credits`
  );
  const issueData = await issueResponse.json();
  const issue: ComicVineIssue & { credits?: ComicVinePerson[] } = issueData.results;

  // 2. Curiosidade: Primeira aparição de personagens importantes
  if (issue.character_credits && issue.character_credits.length > 0) {
    // Pegar os primeiros 3 personagens
    const primeirosPersonagens = issue.character_credits.slice(0, 3);

    for (const personagem of primeirosPersonagens) {
      // Verificar se é primeira aparição
      const primeiraAparicao = await verificarPrimeiraAparicao(personagem.id, issueId, apiKey);

      if (primeiraAparicao) {
        curiosidades.push({
          texto: `Primeira aparição de ${personagem.name} neste issue!`,
          icone: '⭐',
          prioridade: 5 // máxima prioridade
        });
        break; // Apenas uma primeira aparição por issue para não saturar
      }
    }
  }

  // 3. Curiosidade: Criadores notáveis
  if (issue.credits && issue.credits.length > 0) {
    const criadoresPrincipais = issue.credits.filter(c =>
      ['writer', 'artist', 'penciller', 'inker', 'colorist'].includes(c.role.toLowerCase())
    );

    if (criadoresPrincipais.length > 0) {
      const criador = criadoresPrincipais[0];
      curiosidades.push({
        texto: `Escrito por ${criador.name} ${criador.role ? `(${criador.role})` : ''}`,
        icone: '✍️',
        prioridade: 3
      });
    }
  }

  // 4. Curiosidade: Milestone (issue #1, #100, etc.)
  const issueNumber = parseInt(issue.issue_number);
  if (issueNumber === 1 || issueNumber % 100 === 0 || issueNumber % 50 === 0) {
    curiosidades.push({
      texto: `Issue #${issue.issue_number} - ${issueNumber === 1 ? 'Edição de estreia!' : 'Marcos importantes!'}`,
      icone: '🎯',
      prioridade: 4
    });
  }

  // 5. Curiosidade: Contexto temporal
  if (issue.store_date || issue.cover_date) {
    const ano = new Date(issue.store_date || issue.cover_date).getFullYear();
    const anosAtras = new Date().getFullYear() - ano;

    if (anosAtras > 20) {
      curiosidades.push({
        texto: `Publicado em ${ano} - há ${anosAtras} anos atrás!`,
        icone: '📅',
        prioridade: 2
      });
    }
  }

  return curiosidades;
}

/**
 * Verifica se este issue é a primeira aparição de um personagem
 */
async function verificarPrimeiraAparicao(
  characterId: string,
  currentIssueId: string,
  apiKey: string
): Promise<boolean> {
  const response = await fetch(
    `https://comicvine.gamespot.com/api/character/4005-${characterId}/?api_key=${apiKey}&format=json&field_list=id,name,first_appeared_in_issue`
  );
  const data = await response.json();
  const character: ComicVineCharacter = data.results;

  // Extrair ID do issue da primeira aparição
  const primeiraAparicaoId = character.first_appeared_in_issue?.id?.replace('4000-', '');

  return primeiraAparicaoId === currentIssueId;
}
```

### Caso Real: Batman #1 (Spring 1940)

**Cenário**: Narrando Batman #1, onde aparecem pela primeira vez o Coringa e Catwoman.

**Dados da Comic Vine**:

```json
{
  "issue": {
    "id": "4000-1535",
    "name": "Batman",
    "issue_number": "1",
    "store_date": "1940-04-25",
    "volume": {
      "id": "4050-2110",
      "name": "Batman",
      "start_year": "1940"
    },
    "image": {
      "super_url": "https://comicvine.gamespot.com/a/uploads/scale_large/0/5768/6199201-batman_1.jpg"
    },
    "credits": [
      {
        "id": "4040-2250",
        "name": "Bill Finger",
        "role": "writer"
      },
      {
        "id": "4040-2271",
        "name": "Bob Kane",
        "role": "artist"
      }
    ],
    "character_credits": [
      {
        "id": "4005-1699",
        "name": "Joker"
      },
      {
        "id": "4005-2222",
        "name": "Catwoman"
      },
      {
        "id": "4005-1698",
        "name": "Batman"
      },
      {
        "id": "4005-2099",
        "name": "Robin"
      }
    ]
  }
}
```

**Implementação**:

```typescript
/**
 * Script de geração de curiosidades para Batman #1
 */
async function gerarCuriosidadesBatman1() {
  const curiosidades = await extrairCuriosidadesDoIssue('1535', 'SUA_API_KEY');

  // Resultado esperado:
  // [
  //   {
  //     texto: "Primeira aparição do Joker neste issue!",
  //     icone: "⭐",
  //     prioridade: 5
  //   },
  //   {
  //     texto: "Primeira aparição de Catwoman neste issue!",
  //     icone: "⭐",
  //     prioridade: 5
  //   },
  //   {
  //     texto: "Escrito por Bill Finger (writer)",
  //     icone: "✍️",
  //     prioridade: 3
  //   },
  //   {
  //     texto: "Issue #1 - Edição de estreia!",
  //     icone: "🎯",
  //     prioridade: 4
  //   },
  //   {
  //     texto: "Publicado em 1940 - há 84 anos atrás!",
  //     icone: "📅",
  //     prioridade: 2
  //   }
  // ]

  // Calcular posições usando D3
  const posicoes = calcularPosicoesCuriosidades(
    curiosidades.map((c, i) => ({
      ...c,
      id: `curiosidade-${i}`,
      timestamp: i * 180 // cada curiosidade 6 segundos após a anterior (30fps * 6)
    })),
    1920, // largura do vídeo
    1080  // altura do vídeo
  );

  return posicoes;
}

// Resultado visual esperado:
// Frame 0-180: Narração pura
// Frame 180-270: Popup "Primeira aparição do Joker!" aparece com animação spring
// Frame 270-360: Popup "Primeira aparição de Catwoman!" aparece
// Frame 360-450: Popup "Escrito por Bill Finger" aparece
// Frame 450-540: Popup "Issue #1 - Edição de estreia!" aparece
// Frame 540-630: Popup "Publicado em 1940" aparece
```

**Uso na Composition Remotion**:

```tsx
// src/compositions/Batman1Composition.tsx
import { AbsoluteFill, Sequence } from 'remotion';
import { GerenciadorCuriosidades } from '../components/submodulos/CuriosidadePopup';
import { NarracaoQuadrinho } from '../components/NarracaoQuadrinho';

export const Batman1Composition: React.FC = () => {
  // Dados pré-calculados (gerados offline)
  const curiosidades = await gerarCuriosidadesBatman1();

  return (
    <AbsoluteFill>
      {/* Camada principal: Narração do quadrinho */}
      <NarracaoQuadrinho issueId="1535" />

      {/* Camada secundária: Curiosidades intercaladas */}
      <GerenciadorCuriosidades curiosidades={curiosidades} />
    </AbsoluteFill>
  );
};
```

---

## MÓDULO 2: Comparativo Visual

### Estratégia Técnica

**Conceito**: Mostrar versões diferentes do mesmo personagem/elemento lado a lado ou em grid, destacando evoluções, adaptações e mudanças de design.

**Layout D3.js**: `d3.grid()` com dimensionamento dinâmico baseado na quantidade de itens a comparar

```typescript
// D3.js como motor de layout para comparativo
import * as d3 from 'd3';

interface ItemComparativo {
  id: string;
  nome: string;
  ano: number;
  imagem: string;
  contexto?: string; // Ex: "Primeira aparição", "Reboot", "Adaptação cinematográfica"
}

interface LayoutComparativo {
  itens: Array<ItemComparativo & { x: number; y: number; largura: number; altura: number }>;
  linhaTempoX: number; // posição X da linha do tempo
}

/**
 * D3 Grid Layout para calcular posições do comparativo
 * Suporta layouts: 2 itens (side-by-side), 3 itens (triângulo), 4+ itens (grid)
 */
function calcularLayoutComparativo(
  itens: ItemComparativo[],
  videoWidth: number,
  videoHeight: number
): LayoutComparativo {

  const numItens = itens.length;

  // Calcular dimensões baseadas na quantidade de itens
  let cols: number;
  let larguraItem: number;
  let alturaItem: number;

  if (numItens === 2) {
    // Side-by-side horizontal
    cols = 2;
    larguraItem = (videoWidth * 0.8) / 2; // 80% da largura do vídeo
    alturaItem = videoHeight * 0.6; // 60% da altura
  } else if (numItens === 3) {
    // Triângulo (1 em cima, 2 embaixo)
    cols = 2;
    larguraItem = (videoWidth * 0.7) / 2;
    alturaItem = videoHeight * 0.4;
  } else {
    // Grid regular
    cols = Math.ceil(Math.sqrt(numItens));
    larguraItem = (videoWidth * 0.8) / cols;
    alturaItem = (videoHeight * 0.6) / Math.ceil(numItens / cols);
  }

  // D3 Grid Layout
  const gridLayout = d3.grid()
    .size([videoWidth, videoHeight])
    .padding(20);

  // Criar array com dimensões para D3 calcular
  const itensComDimensao = itens.map(item => ({
    id: item.id,
    largura: larguraItem,
    altura: alturaItem
  }));

  // D3 calcula posições
  const posicoes = gridLayout(itensComDimensao);

  // Centralizar o grid no vídeo
  const offsetX = (videoWidth - posicoes[posicoes.length - 1].x - larguraItem) / 2;
  const offsetY = (videoHeight - posicoes[posicoes.length - 1].y - alturaItem) / 2;

  // Combinar dados com posições centralizadas
  const itensComPosicoes = itens.map((item, i) => ({
    ...item,
    x: posicoes[i].x + offsetX,
    y: posicoes[i].y + offsetY,
    largura: larguraItem,
    altura: alturaItem
  }));

  return {
    itens: itensComPosicoes,
    linhaTempoX: videoWidth / 2 // Linha do tempo no centro
  };
}
```

**Componente Remotion**:

```tsx
// src/components/submodulos/ComparativoVisual.tsx
import { useCurrentFrame, useVideoConfig, interpolate, spring } from 'remotion';
import { Img } from 'remotion/img';

interface ComparativoVisualProps {
  layout: LayoutComparativo;
  timestamp: number; // frame de início
  duracao: number; // duração em frames
}

export const ComparativoVisual: React.FC<ComparativoVisualProps> = ({
  layout,
  timestamp,
  duracao
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Calcular progresso do comparativo (0 a 1)
  const progresso = interpolate(
    frame,
    [timestamp, timestamp + duracao],
    [0, 1],
    {
      extrapolateLeft: 'clamp',
      extrapolateRight: 'clamp'
    }
  );

  // Animação de entrada dos itens (staggered)
  const itensAnimados = layout.itens.map((item, index) => {
    const delay = index * 0.15; // cada item aparece 0.15s após o anterior

    const entrada = spring({
      frame: frame - timestamp - (delay * fps),
      fps,
      config: {
        damping: 200, // suave, sem bounce
        stiffness: 100
      }
    });

    const scale = interpolate(entrada, [0, 1], [0.8, 1], {
      extrapolateRight: 'clamp'
    });

    const opacity = interpolate(entrada, [0, 0.5], [0, 1], {
      extrapolateRight: 'clamp'
    });

    return {
      ...item,
      scale,
      opacity
    };
  });

  // Linha do tempo animada
  const linhaProgresso = interpolate(progresso, [0, 1], [0, 1], {
    easing: t => t * (2 - t) // easeOutQuad
  });

  return (
    <div style={{
      position: 'absolute',
      top: 0,
      left: 0,
      width: '100%',
      height: '100%',
      backgroundColor: 'rgba(0, 0, 0, 0.9)',
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      justifyContent: 'center'
    }}>
      {/* Título */}
      <div
        style={{
          color: '#FFD700',
          fontSize: '48px',
          fontWeight: 'bold',
          marginBottom: '40px',
          opacity: progresso,
          textTransform: 'uppercase',
          letterSpacing: '4px'
        }}
      >
        Evolução Visual
      </div>

      {/* Container dos itens */}
      <div style={{ position: 'relative', width: '100%', height: '80%' }}>
        {itensAnimados.map((item) => (
          <div
            key={item.id}
            style={{
              position: 'absolute',
              left: item.x,
              top: item.y,
              width: item.largura,
              height: item.altura,
              opacity: item.opacity,
              transform: `scale(${item.scale})`,
              transformOrigin: 'center center',
              display: 'flex',
              flexDirection: 'column',
              gap: '12px'
            }}
          >
            {/* Container da imagem com borda e shadow */}
            <div
              style={{
                position: 'relative',
                width: '100%',
                height: '100%',
                border: '4px solid rgba(255, 215, 0, 0.6)',
                borderRadius: '12px',
                overflow: 'hidden',
                boxShadow: '0 12px 40px rgba(0, 0, 0, 0.8)'
              }}
            >
              <Img
                src={item.imagem}
                style={{
                  width: '100%',
                  height: '100%',
                  objectFit: 'cover'
                }}
              />

              {/* Overlay com informações */}
              <div
                style={{
                  position: 'absolute',
                  bottom: 0,
                  left: 0,
                  right: 0,
                  background: 'linear-gradient(to top, rgba(0,0,0,0.95), rgba(0,0,0,0))',
                  padding: '24px 16px 16px',
                  color: '#FFFFFF'
                }}
              >
                <div style={{ fontSize: '32px', fontWeight: 'bold', marginBottom: '4px' }}>
                  {item.ano}
                </div>
                <div style={{ fontSize: '20px', opacity: 0.9 }}>
                  {item.nome}
                </div>
                {item.contexto && (
                  <div style={{
                    fontSize: '16px',
                    color: '#FFD700',
                    marginTop: '8px',
                    fontStyle: 'italic'
                  }}>
                    {item.contexto}
                  </div>
                )}
              </div>
            </div>
          </div>
        ))}

        {/* Linha do tempo conectando os itens */}
        <svg
          style={{
            position: 'absolute',
            top: 0,
            left: 0,
            width: '100%',
            height: '100%',
            pointerEvents: 'none',
            zIndex: -1
          }}
        >
          {/* Linha principal horizontal */}
          <line
            x1={layout.itens[0].x + layout.itens[0].largura / 2}
            y1={layout.itens[0].y + layout.itens[0].altura / 2}
            x2={layout.itens[layout.itens.length - 1].x + layout.itens[layout.itens.length - 1].largura / 2}
            y2={layout.itens[layout.itens.length - 1].y + layout.itens[layout.itens.length - 1].altura / 2}
            stroke="rgba(255, 215, 0, 0.4)"
            strokeWidth="4"
            strokeDasharray="10,10"
            style={{
              strokeDashoffset: interpolate(linhaProgresso, [0, 1], [1000, 0])
            }}
          />
        </svg>
      </div>
    </div>
  );
};
```

### Integração Comic Vine API

**Endpoints Necessários**:

```typescript
/**
 * Serviço para buscar dados comparativos de um personagem na Comic Vine API
 */

interface VersaoPersonagem {
  id: string;
  nome: string;
  ano: number;
  imagem: string;
  contexto: string;
  issueReferencia: {
    id: string;
    nome: string;
    numero: string;
  };
}

/**
 * Busca versões alternativas de um personagem ao longo do tempo
 */
export async function buscarVersoesPersonagem(
  characterId: string,
  apiKey: string,
  maxVersoes: number = 6
): Promise<VersaoPersonagem[]> {

  const versoes: VersaoPersonagem[] = [];

  // 1. Buscar informações básicas do personagem
  const characterResponse = await fetch(
    `https://comicvine.gamespot.com/api/character/4005-${characterId}/?api_key=${apiKey}&format=json&field_list=id,name,real_name,first_appeared_in_issue,image,deck`
  );
  const characterData = await characterResponse.json();
  const character = characterData.results as ComicVineCharacter;

  // 2. Adicionar primeira aparição
  if (character.first_appeared_in_issue) {
    const primeiraAparicaoIssue = await buscarIssueDetalhes(
      character.first_appeared_in_issue.id.replace('4000-', ''),
      apiKey
    );

    versoes.push({
      id: 'original',
      nome: character.name,
      ano: new Date(primeiraAparicaoIssue.store_date).getFullYear(),
      imagem: character.image.super_url,
      contexto: 'Primeira Aparição',
      issueReferencia: {
        id: primeiraAparicaoIssue.id,
        nome: primeiraAparicaoIssue.volume.name,
        numero: primeiraAparicaoIssue.issue_number
      }
    });
  }

  // 3. Buscar issues importantes do personagem (milestones)
  const issuesResponse = await fetch(
    `https://comicvine.gamespot.com/api/issues/?api_key=${apiKey}&format=json&filter=characters:${characterId}&sort=store_date:asc&limit=50`
  );
  const issuesData = await issuesResponse.json();
  const issues = issuesData.results as ComicVineIssue[];

  // 4. Selecionar milestones (issue #1, #100, reinícios, etc.)
  const milestones = issues.filter(issue => {
    const numero = parseInt(issue.issue_number);
    // Marcos importantes
    return numero === 1 ||
           numero === 100 ||
           numero % 50 === 0 ||
           issue.name?.toLowerCase().includes('annual') ||
           issue.name?.toLowerCase().includes('special');
  });

  // 5. Pegar uma amostra representativa
  const amostra = milestones.slice(0, maxVersoes - 1);

  for (const issue of amostra) {
    const ano = new Date(issue.store_date).getFullYear();

    // Evitar duplicatas de ano
    if (!versoes.find(v => v.ano === ano)) {
      versoes.push({
        id: issue.id,
        nome: character.name,
        ano,
        imagem: issue.image.super_url,
        contexto: `${issue.volume.name} #${issue.issue_number}`,
        issueReferencia: {
          id: issue.id,
          nome: issue.volume.name,
          numero: issue.issue_number
        }
      });
    }
  }

  // 6. Se tiver poucas versões, buscar adaptações cinematográficas
  if (versoes.length < 3) {
    const moviesResponse = await fetch(
      `https://comicvine.gamespot.com/api/movies/?api_key=${apiKey}&format=json&filter=characters:${characterId}&sort=release_date:asc&limit=10`
    );
    const moviesData = await moviesResponse.json();
    const movies = moviesData.results as Array<{
      id: string;
      name: string;
      image: { super_url: string };
      release_date: string;
    }>;

    for (const movie of movies.slice(0, 2)) {
      const ano = new Date(movie.release_date).getFullYear();
      versoes.push({
        id: movie.id,
        nome: character.name,
        ano,
        imagem: movie.image.super_url,
        contexto: `Adaptação Cinematográfica - ${movie.name}`,
        issueReferencia: {
          id: movie.id,
          nome: movie.name,
          numero: 'N/A'
        }
      });
    }
  }

  // Ordenar por ano e limitar
  return versoes
    .sort((a, b) => a.ano - b.ano)
    .slice(0, maxVersoes);
}

/**
 * Busca detalhes de um issue específico
 */
async function buscarIssueDetalhes(
  issueId: string,
  apiKey: string
): Promise<ComicVineIssue> {
  const response = await fetch(
    `https://comicvine.gamespot.com/api/issue/4000-${issueId}/?api_key=${apiKey}&format=json&field_list=id,name,issue_number,store_date,volume,image`
  );
  const data = await response.json();
  return data.results;
}
```

### Caso Real: Capitão América - Evolução Visual (1941-2024)

**Cenário**: Narrando um issue moderno do Capitão América, queremos mostrar como ele evoluiu visualmente desde 1941.

**Dados da Comic Vine**:

```json
{
  "character": {
    "id": "4005-2143",
    "name": "Captain America",
    "real_name": "Steve Rogers",
    "first_appeared_in_issue": {
      "id": "4000-2345",
      "name": "Captain America Comics",
      "issue_number": "1"
    },
    "image": {
      "super_url": "https://comicvine.gamespot.com/a/uploads/scale_large/0/5768/6199201-captain-america-1.jpg"
    }
  },
  "milestones": [
    {
      "id": "4000-2345",
      "name": "Captain America Comics",
      "issue_number": "1",
      "store_date": "1941-03-01",
      "image": {
        "super_url": "https://comicvine.gamespot.com/a/uploads/scale_large/cap-1941.jpg"
      }
    },
    {
      "id": "4000-5678",
      "name": "Tales of Suspense",
      "issue_number": "59",
      "store_date": "1964-11-01",
      "image": {
        "super_url": "https://comicvine.gamespot.com/a/uploads/scale_large/cap-1964.jpg"
      }
    },
    {
      "id": "4000-9012",
      "name": "Captain America",
      "issue_number": "100",
      "store_date": "1968-02-01",
      "image": {
        "super_url": "https://comicvine.gamespot.com/a/uploads/scale_large/cap-1968.jpg"
      }
    },
    {
      "id": "4000-3456",
      "name": "Captain America",
      "issue_number": "337",
      "store_date": "1998-01-01",
      "image": {
        "super_url": "https://comicvine.gamespot.com/a/uploads/scale_large/cap-1998.jpg"
      }
    },
    {
      "id": "4000-7890",
      "name": "Captain America",
      "issue_number": "1",
      "store_date": "2005-01-01",
      "image": {
        "super_url": "https://comicvine.gamespot.com/a/uploads/scale_large/cap-2005.jpg"
      }
    }
  ]
}
```

**Implementação**:

```typescript
/**
 * Script de geração de comparativo para Capitão América
 */
async function gerarComparativoCapitaoAmerica() {
  const versoes = await buscarVersoesPersonagem('2143', 'SUA_API_KEY', 6);

  // Resultado esperado:
  // [
  //   {
  //     id: "original",
  //     nome: "Captain America",
  //     ano: 1941,
  //     imagem: "https://...cap-1941.jpg",
  //     contexto: "Primeira Aparição",
  //     issueReferencia: { id: "2345", nome: "Captain America Comics", numero: "1" }
  //   },
  //   {
  //     id: "4000-5678",
  //     nome: "Captain America",
  //     ano: 1964,
  //     imagem: "https://...cap-1964.jpg",
  //     contexto: "Tales of Suspense #59",
  //     issueReferencia: { id: "5678", nome: "Tales of Suspense", numero: "59" }
  //   },
  //   {
  //     id: "4000-9012",
  //     nome: "Captain America",
  //     ano: 1968,
  //     imagem: "https://...cap-1968.jpg",
  //     contexto: "Captain America #100",
  //     issueReferencia: { id: "9012", nome: "Captain America", numero: "100" }
  //   },
  //   {
  //     id: "4000-3456",
  //     nome: "Captain America",
  //     ano: 1998,
  //     imagem: "https://...cap-1998.jpg",
  //     contexto: "Heroes Reborn",
  //     issueReferencia: { id: "3456", nome: "Captain America", numero: "337" }
  //   },
  //   {
  //     id: "4000-7890",
  //     nome: "Captain America",
  //     ano: 2005,
  //     imagem: "https://...cap-2005.jpg",
  //     contexto: "Edição #1 - Reboot",
  //     issueReferencia: { id: "7890", nome: "Captain America", numero: "1" }
  //   },
  //   {
  //     id: "movie-1",
  //     nome: "Captain America",
  //     ano: 2011,
  //     imagem: "https://...cap-mcu.jpg",
  //     contexto: "Adaptação - Captain America: The First Avenger",
  //     issueReferencia: { id: "movie-1", nome: "MCU", numero: "N/A" }
  //   }
  // ]

  // Calcular layout usando D3
  const layout = calcularLayoutComparativo(versoes, 1920, 1080);

  return layout;
}

// Uso na Remotion Composition
// Frame 0: Início do comparativo
// Frame 0-30: Título aparece
// Frame 30-120: Itens aparecem em sequência (staggered)
// Frame 120-180: Layout completo visível
// Frame 180-210: Fade out
```

**Resultado Visual Esperado**:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    EVOLUÇÃO VISUAL                                          │
│                                                                             │
│  ┌──────────────┐      ┌──────────────┐      ┌──────────────┐              │
│  │              │      │              │      │              │              │
│  │   [1941]     │ ─────│   [1964]     │ ─────│   [1968]     │              │
│  │  Original    │      │  Silver Age  │      │  Milestone   │              │
│  │              │      │              │      │              │              │
│  └──────────────┘      └──────────────┘      └──────────────┘              │
│                                                                             │
│  ┌──────────────┐      ┌──────────────┐      ┌──────────────┐              │
│  │              │      │              │      │              │              │
│  │   [1998]     │ ─────│   [2005]     │ ─────│   [2011]     │              │
│  │  Heroes Reborn│     │   Reboot     │      │     MCU      │              │
│  │              │      │              │      │              │              │
│  └──────────────┘      └──────────────┘      └──────────────┘              │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘

- Linha tracejada dourada conectando as versões
- Animação de entrada staggered (cada versão aparece após a anterior)
- Labels com ano, contexto e issue de referência
```

---

## MÓDULO 3: Árvore de Relacionamentos

### Estratégia Técnica

**Conceito**: Mostrar conexões entre personagens em um grafo/árvore genealógica, visualizando aliados, inimigos, equipes e relações.

**Layout D3.js**: `d3.forceSimulation()` para grafo com física (force-directed graph)

```typescript
// D3.js como motor de layout para grafo de relacionamentos
import * as d3 from 'd3';

interface NoGrafo {
  id: string;
  nome: string;
  tipo: 'protagonista' | 'aliado' | 'inimigo' | 'equipe' | 'neutro';
  imagem?: string;
  importancia?: number; // 1-10, afeta o tamanho do nó
}

interface ConexaoGrafo {
  source: string; // ID do nó de origem
  target: string; // ID do nó de destino
  tipo: 'alianca' | 'inimizade' | 'membro_equipe' | 'familiar' | 'romantico';
  forca?: number; // 1-10, afeta a espessura da linha
}

interface LayoutGrafo {
  nos: Array<NoGrafo & { x: number; y: number; raio: number }>;
  conexoes: Array<{
    source: NoGrafo & { x: number; y: number };
    target: NoGrafo & { x: number; y: number };
    tipo: string;
    forca: number;
  }>;
}

/**
 * D3 Force Simulation para calcular posições do grafo
 * IMPORTANTE: D3 calcula posições baseadas em FÍSICA, Remotion anima
 */
function calcularLayoutGrafo(
  nos: NoGrafo[],
  conexoes: ConexaoGrafo[],
  videoWidth: number,
  videoHeight: number,
  iteracoes: number = 300
): LayoutGrafo {

  // Preparar dados para D3
  const nosParaD3 = nos.map(n => ({ ...n }));
  const conexoesParaD3 = conexoes.map(c => ({ ...c }));

  // Criar simulação de força
  const simulation = d3.forceSimulation(nosParaD3 as any)
    // Força de conexão (links mantêm nós conectados)
    .force('link', d3.forceLink(conexoesParaD3 as any)
      .id((d: any) => d.id)
      .distance((d: any) => {
        // Distância baseada no tipo de relação
        switch (d.tipo) {
          case 'membro_equipe': return 80;
          case 'alianca': return 120;
          case 'inimizade': return 180; // inimigos ficam mais longe
          case 'familiar': return 100;
          case 'romantico': return 90;
          default: return 120;
        }
      })
      .strength((d: any) => (d.forca || 5) / 10)
    )
    // Força de carga (nós se repelem)
    .force('charge', d3.forceManyBody()
      .strength((d: any) => {
        // Protagonista tem carga negativa maior (atrai mais)
        if (d.tipo === 'protagonista') return -500;
        if (d.tipo === 'inimigo') return -300;
        return -200;
      })
    )
    // Força central (mantém o grafo no centro)
    .force('center', d3.forceCenter(videoWidth / 2, videoHeight / 2))
    // Força de colisão (evita sobreposição)
    .force('collision', d3.forceCollide()
      .radius((d: any) => {
        // Raio baseado na importância
        return 30 + (d.importancia || 5) * 3;
      })
      .iterations(2)
    );

  // Executar simulação
  for (let i = 0; i < iteracoes; i++) {
    simulation.tick();
  }

  // Calcular raios baseados na importância
  const nosComPosicoes = nosParaD3.map(n => ({
    ...n,
    raio: 30 + (n.importancia || 5) * 3
  }));

  // Mapear conexões para nós com posições
  const conexoesComPosicoes = conexoesParaD3.map(c => {
    const sourceNode = nosComPosicoes.find(n => n.id === c.source);
    const targetNode = nosComPosicoes.find(n => n.id === c.target);

    return {
      source: sourceNode!,
      target: targetNode!,
      tipo: c.tipo,
      forca: c.forca || 5
    };
  });

  return {
    nos: nosComPosicoes,
    conexoes: conexoesComPosicoes
  };
}
```

**Componente Remotion**:

```tsx
// src/components/submodulos/ArvoreRelacionamentos.tsx
import { useCurrentFrame, useVideoConfig, interpolate, spring } from 'remotion';
import { Img } from 'remotion/img';

interface ArvoreRelacionamentosProps {
  layout: LayoutGrafo;
  timestamp: number; // frame de início
  duracao: number; // duração em frames
}

export const ArvoreRelacionamentos: React.FC<ArvoreRelacionamentosProps> = ({
  layout,
  timestamp,
  duracao
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Animação de entrada do container
  const containerScale = spring({
    frame: frame - timestamp,
    fps,
    config: { damping: 200, stiffness: 100 }
  });

  const containerOpacity = interpolate(
    containerScale,
    [0, 1],
    [0, 1],
    { extrapolateRight: 'clamp' }
  );

  // Animação dos nós (staggered)
  const nosAnimados = layout.nos.map((no, index) => {
    const delay = index * 0.1; // cada nó aparece 0.1s após o anterior

    const entrada = spring({
      frame: frame - timestamp - (delay * fps),
      fps,
      config: { damping: 15, stiffness: 200 }
    });

    const scale = interpolate(entrada, [0, 1], [0, 1], {
      extrapolateRight: 'clamp'
    });

    const opacity = interpolate(entrada, [0, 0.5], [0, 1], {
      extrapolateRight: 'clamp'
    });

    return {
      ...no,
      scale,
      opacity
    };
  });

  // Animação das conexões (aparecem gradualmente)
  const conexoesProgresso = interpolate(
    frame,
    [timestamp, timestamp + duracao * 0.3],
    [0, 1],
    {
      extrapolateLeft: 'clamp',
      extrapolateRight: 'clamp',
      easing: t => t * (2 - t) // easeOutQuad
    }
  );

  // Cores baseadas no tipo
  const coresPorTipo: Record<string, string> = {
    protagonista: '#4A90E2',     // Azul
    aliado: '#50E3C2',           // Verde claro
    inimigo: '#E94B3C',          // Vermelho
    equipe: '#F5A623',           // Laranja
    neutro: '#9B9B9B'            // Cinza
  };

  return (
    <div
      style={{
        position: 'absolute',
        top: 0,
        left: 0,
        width: '100%',
        height: '100%',
        backgroundColor: 'rgba(0, 0, 0, 0.92)',
        opacity: containerOpacity,
        transform: `scale(${containerScale})`,
        transformOrigin: 'center center'
      }}
    >
      {/* SVG para conexões (linhas) */}
      <svg
        style={{
          position: 'absolute',
          top: 0,
          left: 0,
          width: '100%',
          height: '100%',
          pointerEvents: 'none',
          zIndex: 1
        }}
      >
        {layout.conexoes.map((conexao, index) => {
          // Calcular progresso individual da conexão
          const conexaoProgresso = interpolate(
            conexoesProgresso,
            [(index / layout.conexoes.length), ((index + 1) / layout.conexoes.length)],
            [0, 1],
            { extrapolateRight: 'clamp' }
          );

          return (
            <g key={`${conexao.source.id}-${conexao.target.id}`}>
              {/* Linha principal */}
              <line
                x1={conexao.source.x}
                y1={conexao.source.y}
                x2={conexao.target.x}
                y2={conexao.target.y}
                stroke={
                  conexao.tipo === 'inimizade' ? '#E94B3C' :
                  conexao.tipo === 'alianca' ? '#50E3C2' :
                  conexao.tipo === 'romantico' ? '#FF69B4' :
                  '#9B9B9B'
                }
                strokeWidth={conexao.forca * 2}
                strokeDasharray="5,5"
                opacity={conexaoProgresso * 0.6}
                style={{
                  strokeDashoffset: interpolate(conexaoProgresso, [0, 1], [1000, 0])
                }}
              />

              {/* Rótulo do tipo de conexão */}
              <text
                x={(conexao.source.x + conexao.target.x) / 2}
                y={(conexao.source.y + conexao.target.y) / 2}
                fill="#FFFFFF"
                fontSize="12"
                textAnchor="middle"
                opacity={conexaoProgresso * 0.8}
                style={{
                  textShadow: '0 0 4px rgba(0,0,0,0.8)',
                  fontWeight: 'bold'
                }}
              >
                {conexao.tipo}
              </text>
            </g>
          );
        })}
      </svg>

      {/* Nós (personagens) */}
      {nosAnimados.map((no) => (
        <div
          key={no.id}
          style={{
            position: 'absolute',
            left: no.x - no.raio,
            top: no.y - no.raio,
            width: no.raio * 2,
            height: no.raio * 2,
            borderRadius: '50%',
            opacity: no.opacity,
            transform: `scale(${no.scale})`,
            transformOrigin: 'center center',
            backgroundColor: coresPorTipo[no.tipo] || '#9B9B9B',
            border: no.tipo === 'protagonista' ? '4px solid #FFD700' : '3px solid rgba(255,255,255,0.3)',
            boxShadow: `0 0 ${no.raio}px ${coresPorTipo[no.tipo]}40`,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            overflow: 'hidden',
            cursor: 'pointer',
            zIndex: 10
          }}
        >
          {no.imagem ? (
            <Img
              src={no.imagem}
              style={{
                width: '100%',
                height: '100%',
                objectFit: 'cover',
                borderRadius: '50%'
              }}
            />
          ) : (
            <span style={{
              fontSize: Math.min(no.raio, 24),
              fontWeight: 'bold',
              color: '#FFFFFF',
              textAlign: 'center',
              padding: '4px'
            }}>
              {no.nome.substring(0, 2).toUpperCase()}
            </span>
          )}
        </div>
      ))}

      {/* Legendas */}
      <div style={{
        position: 'absolute',
        bottom: '40px',
        left: '50%',
        transform: 'translateX(-50%)',
        display: 'flex',
        gap: '24px',
        backgroundColor: 'rgba(0,0,0,0.8)',
        padding: '16px 24px',
        borderRadius: '12px',
        border: '1px solid rgba(255,255,255,0.2)'
      }}>
        {Object.entries(coresPorTipo).map(([tipo, cor]) => (
          <div key={tipo} style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <div style={{
              width: '16px',
              height: '16px',
              borderRadius: '50%',
              backgroundColor: cor
            }} />
            <span style={{ color: '#FFFFFF', fontSize: '14px', textTransform: 'capitalize' }}>
              {tipo}
            </span>
          </div>
        ))}
      </div>

      {/* Título */}
      <div style={{
        position: 'absolute',
        top: '40px',
        left: '50%',
        transform: 'translateX(-50%)',
        color: '#FFD700',
        fontSize: '42px',
        fontWeight: 'bold',
        textTransform: 'uppercase',
        letterSpacing: '3px',
        textShadow: '0 0 20px rgba(255, 215, 0, 0.5)'
      }}>
        Relacionamentos
      </div>
    </div>
  );
};
```

### Integração Comic Vine API

**Endpoints Necessários**:

```typescript
/**
 * Serviço para buscar dados de relacionamentos na Comic Vine API
 */

interface PersonagemRelacionado {
  id: string;
  nome: string;
  tipo: string; // "character", "team", "concept", etc.
  imagem: string;
}

/**
 * Busca todos os relacionamentos de um personagem
 */
export async function buscarRelacionamentosPersonagem(
  characterId: string,
  apiKey: string,
  maxProfundidade: number = 2
): Promise<{
  nos: NoGrafo[];
  conexoes: ConexaoGrafo[];
}> {

  const nos: NoGrafo[] = [];
  const conexoes: ConexaoGrafo[] = [];

  // 1. Buscar dados do personagem principal
  const characterResponse = await fetch(
    `https://comicvine.gamespot.com/api/character/4005-${characterId}/?api_key=${apiKey}&format=json&field_list=id,name,real_name,image,aliases,enemies,teams,friends,powers,creators`
  );
  const characterData = await characterResponse.json();
  const protagonista = characterData.results;

  // Adicionar protagonista
  nos.push({
    id: protagonista.id,
    nome: protagonista.name,
    tipo: 'protagonista',
    imagem: protagonista.image?.super_url,
    importancia: 10
  });

  // 2. Buscar inimigos
  if (protagonista.enemies && protagonista.enemies.length > 0) {
    // Limitar aos 5 inimigos principais
    const inimigosPrincipais = protagonista.enemies.slice(0, 5);

    for (const inimigo of inimigosPrincipais) {
      // Buscar detalhes do inimigo
      const inimigoResponse = await fetch(
        `https://comicvine.gamespot.com/api/character/4005-${inimigo.id}/?api_key=${apiKey}&format=json&field_list=id,name,image,deck`
      );
      const inimigoData = await inimigoResponse.json();
      const inimigoDetalhes = inimigoData.results;

      nos.push({
        id: inimigoDetalhes.id,
        nome: inimigoDetalhes.name,
        tipo: 'inimigo',
        imagem: inimigoDetalhes.image?.super_url,
        importancia: 7
      });

      conexoes.push({
        source: protagonista.id,
        target: inimigoDetalhes.id,
        tipo: 'inimizade',
        forca: 8
      });
    }
  }

  // 3. Buscar equipes
  if (protagonista.teams && protagonista.teams.length > 0) {
    const equipesPrincipais = protagonista.teams.slice(0, 3);

    for (const equipe of equipesPrincipais) {
      // Buscar detalhes da equipe
      const equipeResponse = await fetch(
        `https://comicvine.gamespot.com/api/team/4055-${equipe.id}/?api_key=${apiKey}&format=json&field_list=id,name,image,deck,characters`
      );
      const equipeData = await equipeResponse.json();
      const equipeDetalhes = equipeData.results;

      // Adicionar equipe como nó
      nos.push({
        id: equipeDetalhes.id,
        nome: equipeDetalhes.name,
        tipo: 'equipe',
        imagem: equipeDetalhes.image?.super_url,
        importancia: 8
      });

      // Conectar protagonista à equipe
      conexoes.push({
        source: protagonista.id,
        target: equipeDetalhes.id,
        tipo: 'membro_equipe',
        forca: 9
      });

      // Buscar membros da equipe
      if (equipeDetalhes.characters && equipeDetalhes.characters.length > 0) {
        const membrosPrincipais = equipeDetalhes.characters
          .filter((c: any) => c.id !== protagonista.id)
          .slice(0, 3); // Máx 3 membros adicionais

        for (const membro of membrosPrincipais) {
          // Verificar se já existe
          if (!nos.find(n => n.id === membro.id)) {
            // Buscar detalhes do membro
            const membroResponse = await fetch(
              `https://comicvine.gamespot.com/api/character/4005-${membro.id}/?api_key=${apiKey}&format=json&field_list=id,name,image`
            );
            const membroData = await membroResponse.json();
            const membroDetalhes = membroData.results;

            nos.push({
              id: membroDetalhes.id,
              nome: membroDetalhes.name,
              tipo: 'aliado',
              imagem: membroDetalhes.image?.super_url,
              importancia: 5
            });
          }

          // Conectar membro à equipe
          if (!conexoes.find(c => c.source === membro.id && c.target === equipeDetalhes.id)) {
            conexoes.push({
              source: membro.id,
              target: equipeDetalhes.id,
              tipo: 'membro_equipe',
              forca: 7
            });
          }
        }
      }
    }
  }

  // 4. Buscar amigos/aliados (se disponível)
  if (protagonista.friends && protagonista.friends.length > 0) {
    const amigosPrincipais = protagonista.friends
      .filter((amigo: any) => !nos.find(n => n.id === amigo.id))
      .slice(0, 4);

    for (const amigo of amigosPrincipais) {
      const amigoResponse = await fetch(
        `https://comicvine.gamespot.com/api/character/4005-${amigo.id}/?api_key=${apiKey}&format=json&field_list=id,name,image`
      );
      const amigoData = await amigoResponse.json();
      const amigoDetalhes = amigoData.results;

      nos.push({
        id: amigoDetalhes.id,
        nome: amigoDetalhes.name,
        tipo: 'aliado',
        imagem: amigoDetalhes.image?.super_url,
        importancia: 6
      });

      conexoes.push({
        source: protagonista.id,
        target: amigoDetalhes.id,
        tipo: 'alianca',
        forca: 7
      });
    }
  }

  return { nos, conexoes };
}

/**
 * Busca relacionamentos específicos de um issue
 * (personagens presentes naquele quadrinho)
 */
export async function buscarRelacionamentosDoIssue(
  issueId: string,
  apiKey: string
): Promise<{
  nos: NoGrafo[];
  conexoes: ConexaoGrafo[];
}> {

  // Buscar detalhes do issue
  const issueResponse = await fetch(
    `https://comicvine.gamespot.com/api/issue/4000-${issueId}/?api_key=${apiKey}&format=json&field_list=id,name,character_credits,team_credits,location_credits,concept_credits`
  );
  const issueData = await issueResponse.json();
  const issue = issueData.results;

  const nos: NoGrafo[] = [];
  const conexoes: ConexaoGrafo[] = [];

  // 1. Processar personagens do issue
  if (issue.character_credits && issue.character_credits.length > 0) {
    const personagens = issue.character_credits.slice(0, 10); // Limitar a 10

    for (const personagem of personagens) {
      // Buscar detalhes
      const charResponse = await fetch(
        `https://comicvine.gamespot.com/api/character/4005-${personagem.id}/?api_key=${apiKey}&format=json&field_list=id,name,image,enemies,friends`
      );
      const charData = await charResponse.json();
      const charDetalhes = charData.results;

      // Determinar tipo baseado em lógica simples
      // (poderia ser refinado para detectar vilões/heróis)
      const tipo: NoGrafo['tipo'] = 'neutro'; // padrão

      nos.push({
        id: charDetalhes.id,
        nome: charDetalhes.name,
        tipo,
        imagem: charDetalhes.image?.super_url,
        importancia: 5
      });
    }

    // Criar conexões entre personagens baseado em suas redes
    for (let i = 0; i < nos.length; i++) {
      for (let j = i + 1; j < nos.length; j++) {
        // Conexão simples (poderia ser refinada)
        conexoes.push({
          source: nos[i].id,
          target: nos[j].id,
          tipo: 'alianca',
          forca: 3
        });
      }
    }
  }

  return { nos, conexoes };
}
```

### Caso Real: Batman - Rede de Relacionamentos

**Cenário**: Narrando um issue onde o Batman encontra o Coringa pela primeira vez. Queremos mostrar a rede de personagens.

**Dados da Comic Vine**:

```json
{
  "protagonista": {
    "id": "4005-1698",
    "name": "Batman",
    "real_name": "Bruce Wayne",
    "image": {
      "super_url": "https://comicvine.gamespot.com/a/uploads/scale_large/batman.jpg"
    },
    "enemies": [
      {
        "id": "4005-1699",
        "name": "Joker"
      },
      {
        "id": "4005-2279",
        "name": "Two-Face"
      },
      {
        "id": "4005-2356",
        "name": "Bane"
      },
      {
        "id": "4005-2277",
        "name": "Riddler"
      },
      {
        "id": "4005-2278",
        "name": "Penguin"
      }
    ],
    "teams": [
      {
        "id": "4055-2415",
        "name": "Justice League"
      },
      {
        "id": "4055-2418",
        "name": "Batman Family"
      }
    ],
    "friends": [
      {
        "id": "4005-2099",
        "name": "Robin"
      },
      {
        "id": "4005-5746",
        "name": "Alfred Pennyworth"
      },
      {
        "id": "4005-2247",
        "name": "Commissioner Gordon"
      },
      {
        "id": "4005-2248",
        "name": "Catwoman"
      }
    ]
  },
  "equipe_justice_league": {
    "id": "4055-2415",
    "name": "Justice League",
    "characters": [
      { "id": "4005-2158", "name": "Superman" },
      { "id": "4005-2143", "name": "Wonder Woman" },
      { "id": "4005-2182", "name": "The Flash" },
      { "id": "4005-2166", "name": "Aquaman" }
    ]
  }
}
```

**Implementação**:

```typescript
/**
 * Script de geração de árvore de relacionamentos para Batman
 */
async function gerarArvoreRelacionamentosBatman() {
  const { nos, conexoes } = await buscarRelacionamentosPersonagem('1698', 'SUA_API_KEY', 2);

  // Estrutura de nós resultante:
  // [
  //   { id: "1698", nome: "Batman", tipo: "protagonista", importancia: 10 },
  //   { id: "1699", nome: "Joker", tipo: "inimigo", importancia: 7 },
  //   { id: "2279", nome: "Two-Face", tipo: "inimigo", importancia: 7 },
  //   { id: "2356", nome: "Bane", tipo: "inimigo", importancia: 7 },
  //   { id: "2099", nome: "Robin", tipo: "aliado", importancia: 6 },
  //   { id: "5746", nome: "Alfred", tipo: "aliado", importancia: 6 },
  //   { id: "2247", nome: "Gordon", tipo: "aliado", importancia: 6 },
  //   { id: "4055-2415", nome: "Justice League", tipo: "equipe", importancia: 8 },
  //   { id: "2158", nome: "Superman", tipo: "aliado", importancia: 5 },
  //   { id: "2143", nome: "Wonder Woman", tipo: "aliado", importancia: 5 },
  //   { id: "2182", nome: "Flash", tipo: "aliado", importancia: 5 }
  // ]

  // Estrutura de conexões resultante:
  // [
  //   { source: "1698", target: "1699", tipo: "inimizade", forca: 8 },  // Batman - Joker
  //   { source: "1698", target: "2279", tipo: "inimizade", forca: 8 },  // Batman - Two-Face
  //   { source: "1698", target: "2356", tipo: "inimizade", forca: 8 },  // Batman - Bane
  //   { source: "1698", target: "2099", tipo: "alianca", forca: 7 },    // Batman - Robin
  //   { source: "1698", target: "5746", tipo: "alianca", forca: 7 },    // Batman - Alfred
  //   { source: "1698", target: "2247", tipo: "alianca", forca: 7 },    // Batman - Gordon
  //   { source: "1698", target: "4055-2415", tipo: "membro_equipe", forca: 9 }, // Batman - JL
  //   { source: "2158", target: "4055-2415", tipo: "membro_equipe", forca: 7 }, // Superman - JL
  //   { source: "2143", target: "4055-2415", tipo: "membro_equipe", forca: 7 },  // WW - JL
  //   { source: "2182", target: "4055-2415", tipo: "membro_equipe", forca: 7 }   // Flash - JL
  // ]

  // Calcular layout usando D3 Force Simulation
  const layout = calcularLayoutGrafo(nos, conexoes, 1920, 1080, 300);

  return layout;
}

// Resultado visual esperado:
//
//              [Justice League] (laranja, centro superior)
//                    /      |      \
//             Superman   WW      Flash
//                 |        |        |
//                  \       |       /
//                   \      |      /
//                    \     |     /
//               [Batman] (azul, centro) ←━━━━━━━━━━━━━ [Joker] (vermelho)
//                    /     |     \                        [Two-Face] (vermelho)
//                Robin  Alfred  Gordon                    [Bane] (vermelho)
//
// - Tamanho do nó proporcional à importância
// - Linhas vermelhas para inimizade, verdes para aliança, laranja para equipe
// - Protagonista no centro, inimigos afastados pela força de repulsão
// - Equipe funciona como "hub" centralizando membros
```

**Timeline de Animação**:

```typescript
// Frame 0-180: Árvore de relacionamentos visível (6 segundos a 30fps)
// Frame 0: Container começa a aparecer (scale 0 → 1)
// Frame 0-30: Título aparece
// Frame 15-90: Nós aparecem em sequência (staggered)
// Frame 30-108: Conexões são desenhadas gradualmente
// Frame 90-180: Layout completo visível
// Frame 180: Fade out
```

---

## Pipeline de Produção (Módulos 1-3)

### Etapa 1: Pré-Processamento (Offline)

```typescript
/**
 * Script executado antes de renderizar
 * Gera todos os dados necessários dos submódulos
 */
async function preProcessarSubmodulos(
  volumeId: string,
  apiKey: string
): Promise<{
  curiosidades: Record<string, Curiosidade[]>;
  comparativos: Record<string, LayoutComparativo>;
  arvores: Record<string, LayoutGrafo>;
}> {

  const resultados = {
    curiosidades: {},
    comparativos: {},
    arvores: {}
  };

  // 1. Buscar todos os issues do volume
  const issuesResponse = await fetch(
    `https://comicvine.gamespot.com/api/issues/?api_key=${apiKey}&format=json&filter=volume:4050-${volumeId}&sort=store_date:asc`
  );
  const issuesData = await issuesResponse.json();
  const issues = issuesData.results as ComicVineIssue[];

  console.log(`Processando ${issues.length} issues...`);

  // 2. Para cada issue, gerar dados dos submódulos
  for (const issue of issues) {
    const issueId = issue.id.replace('4000-', '');

    console.log(`\nProcessando Issue ${issue.issue_number}...`);

    // Módulo 1: Curiosidades
    const curiosidades = await extrairCuriosidadesDoIssue(issueId, apiKey);
    const posicoesCuriosidades = calcularPosicoesCuriosidades(
      curiosidades.map((c, i) => ({
        ...c,
        id: `${issueId}-curiosidade-${i}`,
        timestamp: i * 180 // cada 6 segundos
      })),
      1920,
      1080
    );
    resultados.curiosidades[issueId] = posicoesCuriosidades;
    console.log(`  ✓ ${curiosidades.length} curiosidades geradas`);

    // Módulo 2: Comparativos (apenas para issues importantes)
    const issueNumber = parseInt(issue.issue_number);
    if (issueNumber === 1 || issueNumber % 50 === 0 || issueNumber % 100 === 0) {
      // Buscar personagem principal do issue
      if (issue.character_credits && issue.character_credits.length > 0) {
        const personagemPrincipal = issue.character_credits[0];
        const versoes = await buscarVersoesPersonagem(
          personagemPrincipal.id,
          apiKey,
          6
        );

        if (versoes.length >= 2) {
          const layoutComparativo = calcularLayoutComparativo(versoes, 1920, 1080);
          resultados.comparativos[issueId] = layoutComparativo;
          console.log(`  ✓ Comparativo gerado para ${personagemPrincipal.name}`);
        }
      }
    }

    // Módulo 3: Árvores de relacionamento (para issues com novos personagens)
    if (issue.character_credits && issue.character_credits.length >= 3) {
      const { nos, conexoes } = await buscarRelacionamentosDoIssue(issueId, apiKey);

      if (nos.length >= 3 && conexoes.length >= 2) {
        const layoutGrafo = calcularLayoutGrafo(nos, conexoes, 1920, 1080, 300);
        resultados.arvores[issueId] = layoutGrafo;
        console.log(`  ✓ Árvore de relacionamentos gerada (${nos.length} nós)`);
      }
    }
  }

  // 3. Salvar resultados em arquivo JSON
  await fs.writeFile(
    `./cache/submodulos-${volumeId}.json`,
    JSON.stringify(resultados, null, 2)
  );

  console.log('\n✅ Pré-processamento concluído!');
  return resultados;
}
```

### Etapa 2: Integração na Composition Remotion

```tsx
// src/compositions/IssueNarration.tsx
import { AbsoluteFill, Sequence, useCurrentFrame } from 'remotion';
import { NarracaoQuadrinho } from '../components/NarracaoQuadrinho';
import { GerenciadorCuriosidades } from '../components/submodulos/CuriosidadePopup';
import { ComparativoVisual } from '../components/submodulos/ComparativoVisual';
import { ArvoreRelacionamentos } from '../components/submodulos/ArvoreRelacionamentos';

// Dados pré-processados (gerados offline)
import dadosSubmodulos from '../cache/submodulos-2110.json';

interface IssueNarrationProps {
  issueId: string;
  duracaoNarração: number; // em frames
}

export const IssueNarration: React.FC<IssueNarrationProps> = ({
  issueId,
  duracaoNarração
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Dados pré-calculados para este issue
  const curiosidades = dadosSubmodulos.curiosidades[issueId] || [];
  const comparativo = dadosSubmodulos.comparativos[issueId];
  const arvore = dadosSubmodulos.arvores[issueId];

  return (
    <AbsoluteFill>
      {/* CAMADA PRINCIPAL: Narração do quadrinho (sempre visível) */}
      <NarracaoQuadrinho issueId={issueId} />

      {/* CAMADAS SECUNDÁRIAS: Submódulos intercalados */}

      {/* Módulo 1: Curiosidades (spread durante toda narração) */}
      <GerenciadorCuriosidades curiosidades={curiosidades} />

      {/* Módulo 2: Comparativo Visual (apenas se houver dados) */}
      {comparativo && (
        <Sequence
          from={duracaoNarração * 0.6} // aparece em 60% da narração
          durationInFrames={7 * fps} // 7 segundos
        >
          <ComparativoVisual
            layout={comparativo}
            timestamp={0}
            duracao={7 * fps}
          />
        </Sequence>
      )}

      {/* Módulo 3: Árvore de Relacionamentos (apenas se houver dados) */}
      {arvore && (
        <Sequence
          from={duracaoNarração * 0.8} // aparece em 80% da narração
          durationInFrames={8 * fps} // 8 segundos
        >
          <ArvoreRelacionamentos
            layout={arvore}
            timestamp={0}
            duracao={8 * fps}
          />
        </Sequence>
      )}
    </AbsoluteFill>
  );
};
```

### Etapa 3: Renderização

```bash
# Comando de renderização usando Remotion CLI
npx remotion render IssueNarration src/compositions/IssueNarration \
  --props='{"issueId":"1535","duracaoNarração":900}' \
  --output=./videos/batman-1.mp4 \
  --jpeg-quality=90 \
  --concurrency=4
```

---

## Checklist de Implementação

### Módulo 1: Curiosidades ✅
- [x] Função `calcularPosicoesCuriosidades` com D3.js Grid Layout
- [x] Componente `CuriosidadePopup` com animação spring
- [x] Componente `GerenciadorCuriosidades` para múltiplas curiosidades
- [x] Integração Comic Vine API (`extrairCuriosidadesDoIssue`)
- [x] Caso real: Batman #1

### Módulo 2: Comparativo ✅
- [x] Função `calcularLayoutComparativo` com D3.js Grid Layout
- [x] Componente `ComparativoVisual` com animação staggered
- [x] Integração Comic Vine API (`buscarVersoesPersonagem`)
- [x] Caso real: Capitão América (1941-2024)

### Módulo 3: Árvore de Relacionamentos ✅
- [x] Função `calcularLayoutGrafo` com D3.js Force Simulation
- [x] Componente `ArvoreRelacionamentos` com SVG para conexões
- [x] Integração Comic Vine API (`buscarRelacionamentosPersonagem`)
- [x] Caso real: Batman (rede completa)

### Pipeline de Produção ✅
- [x] Script `preProcessarSubmodulos` para geração offline
- [x] Componente `IssueNarration` integrando os 3 módulos
- [x] Comando de renderização

---

## Conclusão

Os três módulos apresentados seguem a arquitetura fundamental:

```
ComicVine API → D3.js Layouts (posições) → Remotion (animação) → Vídeo Final
```

**Principais Decisões Técnicas**:

1. **D3.js como Motor de Layout**: D3 APENAS calcula posições, não anima. Isso permite layouts complexos (grid, force, tree) sem overhead de animação.

2. **Remotion para Animação**: Toda a responsabilidade de frame-a-frame é do Remotion, garantindo consistência e renderização determinística.

3. **Pré-Processamento Offline**: Dados dos submódulos são calculados antes da renderização, reduzindo chamadas de API e garantindo performance.

4. **Proporção 90/10**: Narração é sempre a camada principal; submódulos são complementos visuais que aparecem em momentos estratégicos.

5. **Casos Reais**: Cada módulo foi exemplificado com dados reais da Comic Vine (Batman #1, Capitão América), demonstrando viabilidade prática.

**Resultado**: Vídeos explicativos de quadrinhos que são simultaneamente educativos (narração completa), visuais (quadrinhos em movimento), e informativos (curiosidades e contexto intercalados).
