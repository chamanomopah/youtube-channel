# Estratégia Módulos 4-7: Contexto, Poderes, Localização e Estatísticas

## Visão Geral

Este documento detalha a implementação técnica dos **Módulos 4-7** do sistema de storyboard dinâmico para vídeos "Every Character Comics Explained - Issue by Issue".

**Proporção Alvo**: 90% narração dos quadrinhos + 10% submódulos informativos

**Princípio Fundamental**: D3.js é usado como **motor de layout** (CALCULAR posições), enquanto Remotion controla a animação frame-a-frame dessas posições.

```
PIPELINE:
ComicVine API + APIs Externas → D3.js Layouts → Posições Calculadas → Remotion Components → Vídeo Rendered
```

**Módulos Cobertos**:
- **Módulo 4**: Contexto Histórico/Realidade (timeline paralela com eventos reais)
- **Módulo 5**: Evolução de Poder/Habilidades (radar charts, gráficos comparativos)
- **Módulo 6**: Localização/Locais (mapas com pins animados, cross-sections)
- **Módulo 7**: Estatísticas de Publicação (infográficos minimalistas)

---

## MÓDULO 4: Contexto Histórico/Realidade

### Estratégia Técnica

**Conceito**: Conectar eventos do quadrinho com contexto histórico real através de uma **timeline paralela** que mostra simultaneamente o que acontecia no mundo dos quadrinhos e na realidade.

**Layout D3.js**: `d3.scaleTime()` + `d3.axisTop()`/`d3.axisBottom()` - Mapeamento de datas para posições X em duas linhas do tempo paralelas.

**Por que D3 aqui**: D3 scales são perfeitos para converter datas (1941-03-01) em posições pixels (x: 340) de forma proporcional e precisa.

```typescript
// D3.js como motor de layout para timeline histórica
import * as d3 from 'd3';
import { scaleTime, scaleLinear } from 'd3-scale';
import { axisTop, axisBottom } from 'd3-axis';

interface EventoHistorico {
  data: Date;
  titulo: string;
  descricao: string;
  tipo: 'quadrinho' | 'mundo' | 'guerra' | 'cultura';
  imagem?: string; // URL de foto histórica
}

interface TimelineData {
  eventosQuadrinho: EventoHistorico[];
  eventosMundo: EventoHistorico[];
  dataInicio: Date;
  dataFim: Date;
}

/**
 * D3 Time Scale - CALCULA posições X baseadas em datas
 * IMPORTANTE: D3 APENAS CALCULA, não anima
 */
function calcularPosicoesTimeline(
  dados: TimelineData,
  videoWidth: number,
  timelineY: number
) {
  // Criar escala temporal: mapeia datas → posições X
  const timeScale = scaleTime()
    .domain([dados.dataInicio, dados.dataFim]) // Período completo
    .range([100, videoWidth - 100]); // Margens de 100px

  // Criar escala de cores para tipos de eventos
  const colorScale = d3.scaleOrdinal<string>()
    .domain(['quadrinho', 'mundo', 'guerra', 'cultura'])
    .range(['#2196F3', '#FF5722', '#9C27B0', '#4CAF50']);

  // Processar eventos do quadrinho (linha superior)
  const eventosQuadrinhoPosicionados = dados.eventosQuadrinho.map(evento => ({
    ...evento,
    x: timeScale(evento.data), // D3 calcula posição X
    y: timelineY - 60, // Linha superior
    cor: colorScale(evento.tipo),
    larguraPino: 3,
    alturaPino: 30
  }));

  // Processar eventos do mundo (linha inferior)
  const eventosMundoPosicionados = dados.eventosMundo.map(evento => ({
    ...evento,
    x: timeScale(evento.data), // D3 calcula posição X
    y: timelineY + 60, // Linha inferior
    cor: colorScale(evento.tipo),
    larguraPino: 3,
    alturaPino: 30
  }));

  // Calcular posições das linhas principais
  const linhaQuadrinho = {
    x1: timeScale(dados.dataInicio),
    y1: timelineY - 60,
    x2: timeScale(dados.dataFim),
    y2: timelineY - 60,
    cor: '#2196F3'
  };

  const linhaMundo = {
    x1: timeScale(dados.dataInicio),
    y1: timelineY + 60,
    x2: timeScale(dados.dataFim),
    y2: timelineY + 60,
    cor: '#FF5722'
  };

  // Calcular posição dos eixos (anos marcadores)
  const anos = d3.timeYear.range(
    dados.dataInicio,
    dados.dataFim
  );

  const marcadoresAno = anos.map(ano => ({
    ano: ano.getFullYear(),
    x: timeScale(ano),
    ySuperior: timelineY - 45,
    yInferior: timelineY + 45
  }));

  return {
    eventosQuadrinho: eventosQuadrinhoPosicionados,
    eventosMundo: eventosMundoPosicionados,
    linhaQuadrinho,
    linhaMundo,
    marcadoresAno,
    timeScale // Retornar escala para uso futuro
  };
}

/**
 * Componente Remotion que ANIMA as posições calculadas por D3
 */
import { Img, interpolate, useCurrentFrame, useVideoConfig } from 'remotion';

interface TimelineParalelaProps {
  dados: TimelineData;
  duracaoSegundos: number;
}

export const TimelineParalela: React.FC<TimelineParalelaProps> = ({
  dados,
  duracaoSegundos
}) => {
  const frame = useCurrentFrame();
  const { fps, width } = useVideoConfig();
  const frameTotal = duracaoSegundos * fps;

  // 1. D3 CALCULA as posições (executa UMA vez)
  const posicoes = useMemo(() =>
    calcularPosicoesTimeline(dados, width, 540), // Centralizado verticalmente
    [dados, width]
  );

  // 2. Remotion ANIMA com essas posições (executa TODO frame)

  // Animar opacidade de entrada (fade-in)
  const opacity = interpolate(
    frame,
    [0, 30], // Primeiro segundo
    [0, 1]
  );

  // Animar surgimento dos eventos (sequencialmente)
  const eventosVisiveis = Math.floor(
    interpolate(frame, [0, frameTotal], [0, posicoes.eventosQuadrinho.length + posicoes.eventosMundo.length])
  );

  // Animar as linhas crescendo da esquerda para direita
  const progressoLinha = interpolate(
    frame,
    [0, 60], // Primeiros 2 segundos
    [0, 1],
    { extrapolateRight: 'clamp' }
  );

  const linhaQuadrinhoWidth = (posicoes.linhaQuadrinho.x2 - posicoes.linhaQuadrinho.x1) * progressoLinha;
  const linhaMundoWidth = (posicoes.linhaMundo.x2 - posicoes.linhaMundo.x1) * progressoLinha;

  return (
    <div style={{ opacity, position: 'relative', width: '100%', height: 200 }}>
      {/* Linha dos Quadrinhos (Superior) */}
      <div
        style={{
          position: 'absolute',
          left: posicoes.linhaQuadrinho.x1,
          top: posicoes.linhaQuadrinho.y1,
          width: linhaQuadrinhoWidth,
          height: 3,
          backgroundColor: posicoes.linhaQuadrinho.cor,
          borderRadius: 2
        }}
      />

      {/* Linha do Mundo (Inferior) */}
      <div
        style={{
          position: 'absolute',
          left: posicoes.linhaMundo.x1,
          top: posicoes.linhaMundo.y1,
          width: linhaMundoWidth,
          height: 3,
          backgroundColor: posicoes.linhaMundo.cor,
          borderRadius: 2
        }}
      />

      {/* Marcadores de Ano */}
      {posicoes.marcadoresAno.map((marcador, i) => {
        const delayMarcador = 60 + (i * 5); // Delay escalonado
        const opacidadeMarcador = frame >= delayMarcador ? 1 : 0;
        const translateYMarcador = frame >= delayMarcador ? 0 : 10;

        return (
          <div
            key={marcador.ano}
            style={{
              position: 'absolute',
              left: marcador.x,
              top: marcador.ySuperior,
              opacity: opacidadeMarcador,
              transform: `translateY(${translateYMarcador}px)`,
              fontSize: 14,
              fontWeight: 'bold',
              color: '#FFFFFF',
              fontFamily: 'Arial'
            }}
          >
            {marcador.ano}
          </div>
        );
      })}

      {/* Eventos do Quadrinho */}
      {posicoes.eventosQuadrinho.slice(0, eventosVisiveis).map((evento, i) => {
        const frameEntrada = i * 10; // Delay por evento
        const scale = frame >= frameEntrada
          ? interpolate(frame, [frameEntrada, frameEntrada + 15], [0, 1], { extrapolateRight: 'clamp' })
          : 0;

        return (
          <div
            key={evento.titulo}
            style={{
              position: 'absolute',
              left: evento.x,
              top: evento.y,
              transform: `translate(-50%, -50%) scale(${scale})`,
              transformOrigin: 'center'
            }}
          >
            {/* Pino */}
            <div style={{
              width: evento.larguraPino,
              height: evento.alturaPino,
              backgroundColor: evento.cor,
              borderRadius: 2
            }} />

            {/* Rótulo */}
            <div style={{
              position: 'absolute',
              top: -25,
              left: -50,
              width: 100,
              fontSize: 12,
              color: '#FFFFFF',
              textAlign: 'center',
              backgroundColor: 'rgba(0,0,0,0.7)',
              padding: 4,
              borderRadius: 4
            }}>
              {evento.titulo}
            </div>
          </div>
        );
      })}

      {/* Eventos do Mundo */}
      {posicoes.eventosMundo.slice(0, eventosVisiveis).map((evento, i) => {
        const frameEntrada = i * 10 + 30; // Delay maior
        const scale = frame >= frameEntrada
          ? interpolate(frame, [frameEntrada, frameEntrada + 15], [0, 1], { extrapolateRight: 'clamp' })
          : 0;

        return (
          <div
            key={evento.titulo}
            style={{
              position: 'absolute',
              left: evento.x,
              top: evento.y,
              transform: `translate(-50%, -50%) scale(${scale})`,
              transformOrigin: 'center'
            }}
          >
            {/* Pino */}
            <div style={{
              width: evento.larguraPino,
              height: evento.alturaPino,
              backgroundColor: evento.cor,
              borderRadius: 2
            }} />

            {/* Rótulo */}
            <div style={{
              position: 'absolute',
              top: 10,
              left: -50,
              width: 100,
              fontSize: 12,
              color: '#FFFFFF',
              textAlign: 'center',
              backgroundColor: 'rgba(0,0,0,0.7)',
              padding: 4,
              borderRadius: 4
            }}>
              {evento.titulo}
            </div>

            {/* Imagem histórica (se disponível) */}
            {evento.imagem && (
              <Img
                src={evento.imagem}
                style={{
                  position: 'absolute',
                  top: 30,
                  left: -40,
                  width: 80,
                  height: 60,
                  objectFit: 'cover',
                  borderRadius: 4,
                  border: '2px solid #FFFFFF'
                }}
              />
            )}
          </div>
        );
      })}
    </div>
  );
};
```

### Integração Comic Vine API

**Endpoints Necessários**:

```typescript
// 1. Obter data de publicação do issue
interface ComicVineIssue {
  id: number;
  name: string;
  issue_number: string;
  store_date: string; // "1941-03-01"
  volume: {
    id: number;
    name: string;
    start_year: string; // "1941"
  };
  description?: string; // Pode conter referências históricas
}

// 2. Obter contexto da série/volume
interface ComicVineVolume {
  id: number;
  name: string;
  start_year: string;
  publisher: {
    name: string;
  };
  description: string; // Contexto histórico da criação
}
```

**Dados a Extrair**:

```typescript
// Mapear dados da Comic Vine para formato interno
function mapearDadosContextoHistorico(
  issue: ComicVineIssue,
  volume: ComicVineVolume
): TimelineData {
  const dataPublicacao = new Date(issue.store_date);
  const anoInicio = parseInt(volume.start_year);

  // Criar janela de tempo: 2 anos antes até 1 ano depois
  const dataInicio = new Date(anoInicio - 2, 0, 1);
  const dataFim = new Date(anoInicio + 1, 11, 31);

  // Evento principal (o quadrinho)
  const eventoQuadrinho: EventoHistorico = {
    data: dataPublicacao,
    titulo: `${issue.name} #${issue.issue_number}`,
    descricao: `Publicado em ${formatDate(dataPublicacao)}`,
    tipo: 'quadrinho'
  };

  // Eventos do quadrinho relacionados (ex: primeiras aparições)
  const eventosQuadrinho: EventoHistorico[] = [
    eventoQuadrinho,
    // Adicionar mais eventos do mesmo volume próximos
  ];

  // Eventos do mundo real (virá de API externa)
  const eventosMundo: EventoHistorico[] = buscarEventosHistoricosReais(
    dataInicio,
    dataFim,
    dataPublicacao
  );

  return {
    eventosQuadrinho,
    eventosMundo,
    dataInicio,
    dataFim
  };
}
```

### Integração com APIs de Dados Históricos

**Opções de APIs Externas**:

```typescript
/**
 * Opção 1: Wikipedia API (gratuita, sem chave)
 * Busca eventos históricos por ano/mês
 */
async function buscarEventosWikipedia(ano: number, mes: number): Promise<EventoHistorico[]> {
  const url = `https://en.wikipedia.org/api/rest_v1/feed/onthisday/all/${mes}/${ano}`;

  const response = await fetch(url);
  const dados = await response.json();

  // Mapear eventos do Wikipedia
  const eventos: EventoHistorico[] = [
    ...dados.events.map((e: any) => ({
      data: new Date(ano, mes - 1, e.day),
      titulo: e.text,
      descricao: e.year.toString(),
      tipo: 'mundo' as const
    })),
    ...dados.births.map((e: any) => ({
      data: new Date(ano, mes - 1, e.day),
      titulo: `Nascimento: ${e.text}`,
      descricao: e.year.toString(),
      tipo: 'cultura' as const
    }))
  ];

  return eventos;
}

/**
 * Opção 2: Database local de eventos históricos
 * Mais controlado, permite curadoria manual
 */
interface EventoHistoricoLocal {
  ano: number;
  mes?: number;
  dia?: number;
  titulo: string;
  descricao: string;
  tipo: 'guerra' | 'cultura' | 'mundo' | 'politica';
  imagemUrl?: string;
}

// Database JSON local com eventos importantes
const EVENTOS_HISTORICOS: EventoHistoricoLocal[] = [
  {
    ano: 1939,
    mes: 9,
    dia: 1,
    titulo: 'Início da Segunda Guerra Mundial',
    descricao: 'Alemanha invade a Polônia',
    tipo: 'guerra',
    imagemUrl: 'https://example.com/wwii-start.jpg'
  },
  {
    ano: 1941,
    mes: 12,
    dia: 7,
    titulo: 'Pearl Harbor',
    descricao: 'Japão ataca base dos EUA no Havaí',
    tipo: 'guerra',
    imagemUrl: 'https://example.com/pearl-harbor.jpg'
  },
  {
    ano: 1941,
    mes: 3,
    titulo: 'Capitão América publicado',
    descricao: 'Timely Comics (hoje Marvel) lança Capitão América #1',
    tipo: 'cultura'
  },
  // ... mais eventos
];

function buscarEventosHistoricosReais(
  dataInicio: Date,
  dataFim: Date,
  dataPublicacao: Date
): EventoHistorico[] {
  return EVENTOS_HISTORICOS
    .filter(evento => {
      const dataEvento = new Date(
        evento.ano,
        (evento.mes || 1) - 1,
        evento.dia || 1
      );
      return dataEvento >= dataInicio && dataEvento <= dataFim;
    })
    .map(evento => ({
      data: new Date(evento.ano, (evento.mes || 1) - 1, evento.dia || 1),
      titulo: evento.titulo,
      descricao: evento.descricao,
      tipo: evento.tipo,
      imagem: evento.imagemUrl
    }))
    .sort((a, b) => a.data.getTime() - b.data.getTime());
}
```

### Caso Real: Capitão América #1 (1941)

**Cenário**: Narrar Captain America Comics #1, mostrando contexto da Segunda Guerra Mundial.

```typescript
// Mock dos dados da Comic Vine
const captainAmericaIssue1: ComicVineIssue = {
  id: 4000-1105,
  name: 'Captain America Comics',
  issue_number: '1',
  store_date: '1941-03-01',
  volume: {
    id: 4050-2033,
    name: 'Captain America Comics',
    start_year: '1941'
  }
};

// Dados preparados
const dadosTimeline: TimelineData = {
  dataInicio: new Date('1939-01-01'), // 2 anos antes
  dataFim: new Date('1942-12-31'),    // 1 ano depois

  eventosQuadrinho: [
    {
      data: new Date('1941-03-01'),
      titulo: 'Capitão América #1',
      descricao: 'Primeira aparição do Capitão América',
      tipo: 'quadrinho'
    }
  ],

  eventosMundo: [
    {
      data: new Date('1939-09-01'),
      titulo: 'Início da WWII',
      descricao: 'Alemanha invade Polônia',
      tipo: 'guerra',
      imagem: '/assets/wwii-start.jpg'
    },
    {
      data: new Date('1940-09-16'),
      titulo: 'Draft nos EUA',
      descricao: 'Primeiro recrutamento militar em tempo de paz',
      tipo: 'mundo'
    },
    {
      data: new Date('1941-03-01'),
      titulo: 'Lend-Lease Act',
      descricao: 'EUA começa a apoiar Aliados com suprimentos',
      tipo: 'politica'
    },
    {
      data: new Date('1941-12-07'),
      titulo: 'Pearl Harbor',
      descricao: 'Japão ataca base dos EUA',
      tipo: 'guerra',
      imagem: '/assets/pearl-harbor.jpg'
    },
    {
      data: new Date('1941-12-08'),
      titulo: 'EUA entram na guerra',
      descricao: 'Congresso dos EUA declara guerra',
      tipo: 'guerra'
    }
  ]
};

// Como usar no Remotion
export const CenaContextoWW2: React.FC = () => {
  return (
    <div style={{ position: 'relative', width: '100%', height: '100%' }}>
      {/* Camada principal: Páginas do quadrinho sendo narradas */}
      <PaginasQuadrinho issue={captainAmericaIssue1} />

      {/* Overlay: Timeline paralela no terço inferior */}
      <div style={{
        position: 'absolute',
        bottom: 0,
        left: 0,
        right: 0,
        height: 200,
        background: 'linear-gradient(to top, rgba(0,0,0,0.9), transparent)'
      }}>
        <TimelineParalela
          dados={dadosTimeline}
          duracaoSegundos={7} // 7 segundos de duração do submódulo
        />
      </div>
    </div>
  );
};
```

**Resultado Visual Esperado**:
- Linha superior azul (quadrinhos): mostra Capitão América #1 em março de 1941
- Linha inferior laranja (mundo): mostra eventos WWII de 1939-1942
- Pins animados surgem sequencialmente
- Fotos históricas aparecem em eventos importantes (Pearl Harbor)
- A narração continua mostrando as páginas do quadrinho, enquanto a timeline dá contexto histórico

---

## MÓDULO 5: Evolução de Poder/Habilidades

### Estratégia Técnica

**Conceito**: Mostrar como poderes e habilidades de um personagem evoluem através de **radar charts animados** ou **gráficos de barras comparativos**.

**Layout D3.js**: `d3.scaleLinear()` para normalizar valores de 0-100 + Cálculos de geometria para radar chart (coordenadas polares).

**Por que D3 aqui**: D3 scales normalizam dados (força 85 → altura 85px) e transformam coordenadas polares (ângulo + magnitude) em cartesianas (x, y) para radar charts.

```typescript
// D3.js como motor de layout para radar chart
import * as d3 from 'd3';
import { scaleLinear } from 'd3-scale';
import { lineRadial } from 'd3-shape';

interface Poder {
  nome: string;
  valor: number; // 0-100
}

interface PersonagemPoderes {
  nome: string;
  periodo: string; // "1941", "1985", "2020"
  imagemUrl?: string;
  poderes: Poder[];
}

/**
 * D3 Linear Scale - NORMALIZA valores de 0-100 para raios do radar chart
 */
function calcularRadarChart(
  personagem: PersonagemPoderes,
  raioExterno: number,
  centroX: number,
  centroY: number
) {
  const numeroPoderes = personagem.poderes.length;
  const anguloPorPoder = (Math.PI * 2) / numeroPoderes;

  // Scale para normalizar valores (0-100 → raio)
  const radiusScale = scaleLinear()
    .domain([0, 100]) // Valores dos poderes
    .range([0, raioExterno]); // Pixels do centro até borda

  // Calcular posição (x, y) de cada vértice do radar chart
  const vertices = personagem.poderes.map((poder, index) => {
    const angulo = index * anguloPorPoder - Math.PI / 2; // Começar do topo
    const raio = radiusScale(poder.valor); // D3 calcula o raio

    // Converter polar → cartesiano
    const x = centroX + raio * Math.cos(angulo);
    const y = centroY + raio * Math.sin(angulo);

    return {
      poder: poder.nome,
      valor: poder.valor,
      x,
      y,
      anguloGraus: (angulo * 180) / Math.PI
    };
  });

  // Calcular posição dos rótulos (fora do radar chart)
  const rotulos = personagem.poderes.map((poder, index) => {
    const angulo = index * anguloPorPoder - Math.PI / 2;
    const raioRotulo = raioExterno + 30; // 30px fora do chart

    const x = centroX + raioRotulo * Math.cos(angulo);
    const y = centroY + raioRotulo * Math.sin(angulo);

    return {
      texto: poder.nome,
      x,
      y,
      alinhamento: x > centroX ? 'left' : 'right'
    };
  });

  // Calcular linhas de fundo (concentric circles)
  const circulosConcentricos = [0.2, 0.4, 0.6, 0.8, 1.0].map(fator => ({
    raio: raioExterno * fator,
    valor: Math.round(fator * 100)
  }));

  // Calcular linhas radiais (do centro para fora)
  const linhasRadicais = personagem.poderes.map((_, index) => {
    const angulo = index * anguloPorPoder - Math.PI / 2;
    const xFinal = centroX + raioExterno * Math.cos(angulo);
    const yFinal = centroY + raioExterno * Math.sin(angulo);

    return {
      x1: centroX,
      y1: centroY,
      x2: xFinal,
      y2: yFinal
    };
  });

  // Criar path SVG do polígono de poderes (usando D3 shape)
  const lineGenerator = lineRadial<Poder>()
    .angle((_, i) => i * anguloPorPoder)
    .radius(d => radiusScale(d.valor))
    .curve(d3.curveLinearClosed);

  // Caminho do polígono (para SVG)
  const pathData = lineGenerator(personagem.poderes);

  return {
    vertices,
    rotulos,
    circulosConcentricos,
    linhasRadicais,
    pathData,
    raioExterno,
    centroX,
    centroY
  };
}

/**
 * Componente Remotion que ANIMA o radar chart
 */
import { useMemo } from 'react';
import { interpolate, useCurrentFrame, useVideoConfig } from 'remotion';

interface RadarChartProps {
  personagens: PersonagemPoderes[]; // Múltiplas versões para comparar
  duracaoSegundos: number;
}

export const RadarChartAnimado: React.FC<RadarChartProps> = ({
  personagens,
  duracaoSegundos
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const frameTotal = duracaoSegundos * fps;

  // 1. D3 CALCULA posições para cada personagem (executa UMA vez)
  const charts = useMemo(() =>
    personagens.map((p, i) =>
      calcularRadarChart(p, 120, 240 + i * 300, 300) // Charts lado a lado
    ),
    [personagens]
  );

  // 2. Remotion ANIMA os valores (executa TODO frame)

  // Animar os vértices crescendo do centro (0,0) até suas posições finais
  const progressoVertices = interpolate(
    frame,
    [0, 45], // Primeiros 1.5 segundos
    [0, 1],
    { extrapolateRight: 'clamp' }
  );

  return (
    <div style={{
      position: 'relative',
      width: '100%',
      height: 600,
      backgroundColor: 'rgba(0,0,0,0.8)',
      borderRadius: 10,
      padding: 20
    }}>
      {charts.map((chart, chartIndex) => {
        const cores = ['#2196F3', '#FF5722', '#4CAF50']; // Cores para cada personagem
        const cor = cores[chartIndex % cores.length];

        return (
          <div key={chartIndex} style={{ position: 'absolute', left: chart.centroX, top: chart.centroY }}>
            {/* Título do personagem */}
            <div style={{
              position: 'absolute',
              top: -180,
              left: -100,
              width: 200,
              textAlign: 'center',
              fontSize: 18,
              fontWeight: 'bold',
              color: '#FFFFFF'
            }}>
              {personagens[chartIndex].nome}
              <div style={{ fontSize: 14, opacity: 0.8 }}>
                {personagens[chartIndex].periodo}
              </div>
            </div>

            {/* Círculos concêntricos de fundo */}
            {chart.circulosConcentricos.map((circulo, i) => (
              <div
                key={i}
                style={{
                  position: 'absolute',
                  left: chart.centroX - circulo.raio,
                  top: chart.centroY - circulo.raio,
                  width: circulo.raio * 2,
                  height: circulo.raio * 2,
                  border: '1px solid rgba(255,255,255,0.2)',
                  borderRadius: '50%'
                }}
              />
            ))}

            {/* Linhas radiais */}
            {chart.linhasRadicais.map((linha, i) => (
              <svg key={i} style={{ position: 'absolute', top: 0, left: 0, overflow: 'visible' }}>
                <line
                  x1={linha.x1 - chart.centroX}
                  y1={linha.y1 - chart.centroY}
                  x2={linha.x2 - chart.centroX}
                  y2={linha.y2 - chart.centroY}
                  stroke="rgba(255,255,255,0.1)"
                  strokeWidth={1}
                />
              </svg>
            ))}

            {/* Rótulos dos poderes */}
            {chart.rotulos.map((rotulo, i) => {
              const opacidade = interpolate(
                frame,
                [30 + i * 5, 45 + i * 5], // Delay escalonado
                [0, 1],
                { extrapolateRight: 'clamp' }
              );

              return (
                <div
                  key={i}
                  style={{
                    position: 'absolute',
                    left: rotulo.x - chart.centroX,
                    top: rotulo.y - chart.centroY,
                    textAlign: rotulo.alinhamento,
                    fontSize: 12,
                    color: '#FFFFFF',
                    opacity: opacidade,
                    whiteSpace: 'nowrap'
                  }}
                >
                  {rotulo.texto}
                </div>
              );
            })}

            {/* Polígono de poderes animado */}
            <svg
              width={chart.raioExterno * 2}
              height={chart.raioExterno * 2}
              style={{
                position: 'absolute',
                left: -chart.raioExterno,
                top: -chart.raioExterno,
                overflow: 'visible'
              }}
            >
              {/* Preenchimento do polígono */}
              <polygon
                points={chart.vertices.map(v => {
                  // Animar vértices crescendo
                  const xInterpolado = v.x * progressoVertices - chart.centroX + chart.raioExterno;
                  const yInterpolado = v.y * progressoVertices - chart.centroY + chart.raioExterno;
                  return `${xInterpolado},${yInterpolado}`;
                }).join(' ')}
                fill={cor}
                fillOpacity={0.3}
                stroke={cor}
                strokeWidth={2}
              />

              {/* Pontos nos vértices */}
              {chart.vertices.map((vertice, i) => {
                const xInterpolado = vertice.x * progressoVertices - chart.centroX + chart.raioExterno;
                const yInterpolado = vertice.y * progressoVertices - chart.centroY + chart.raioExterno;

                return (
                  <circle
                    key={i}
                    cx={xInterpolado}
                    cy={yInterpolado}
                    r={5}
                    fill={cor}
                  />
                );
              })}
            </svg>

            {/* Valores numéricos */}
            {chart.vertices.map((vertice, i) => {
              const delay = 45 + i * 3;
              const opacidade = frame >= delay ? 1 : 0;
              const xInterpolado = vertice.x * progressoVertices - chart.centroX;
              const yInterpolado = vertice.y * progressoVertices - chart.centroY;

              return (
                <div
                  key={i}
                  style={{
                    position: 'absolute',
                    left: xInterpolado,
                    top: yInterpolado,
                    transform: 'translate(-50%, -50%)',
                    fontSize: 11,
                    fontWeight: 'bold',
                    color: '#FFFFFF',
                    opacity: opacidade,
                    textShadow: '0 0 3px rgba(0,0,0,0.8)'
                  }}
                >
                  {vertice.valor}
                </div>
              );
            })}
          </div>
        );
      })}
    </div>
  );
};
```

### Integração Comic Vine API

**Endpoints Necessários**:

```typescript
// Comic Vine tem endpoint de "powers" para personagens
interface ComicVineCharacter {
  id: number;
  name: string;
  powers: string[]; // Lista de poderes em texto
  description: string; // Pode conter detalhes sobre habilidades
}

interface ComicVinePower {
  id: number;
  name: string; // "Super Strength", "Agility", etc.
}

// GET /character/4005-{{id}}
// Retorna lista de powers como strings
// Ex: ["Super Strength", "Agility", "Stamina", "Marksmanship"]
```

**Mapeamento de Poderes**:

```typescript
// Como a Comic Vine retorna poderes como strings, precisamos mapear para valores numéricos
const MAPEAMENTO_PODERES: Record<string, number> = {
  'Super Strength': 85,
  'Agility': 75,
  'Stamina': 80,
  'Marksmanship': 70,
  'Tactical Genius': 95,
  'Leadership': 90,
  'Hand-to-Hand Combat': 85,
  'Shield Mastery': 100,
  'Durability': 70,
  'Speed': 65
  // ... mais poderes
};

function converterPoderesComicVine(
  personagem: ComicVineCharacter,
  periodo: string
): PersonagemPoderes {
  const poderes: Poder[] = personagem.powers
    .map(nomePoder => ({
      nome: nomePoder,
      valor: MAPEAMENTO_PODERES[nomePoder] || 50 // Valor padrão se não mapeado
    }))
    .slice(0, 6); // Limitar a 6 poderes principais para radar chart legível

  return {
    nome: personagem.name,
    periodo,
    poderes
  };
}
```

**Sistema de Evolução Temporal**:

```typescript
// Para mostrar evolução, buscamos dados de diferentes épocas
async function buscarEvolucaoPoderes(
  characterId: number,
  periodos: string[] // ['1941', '1985', '2020']
): Promise<PersonagemPoderes[]> {
  // NOTA: Comic Vine NÃO tem dados históricos de poderes por época
  // Solução: Criar curadoria manual ou inferir a partir de issues

  // Abordagem 1: Curadoria manual (recomendado)
  const PODERES_CURADOS: Record<string, PersonagemPoderes> = {
    'captain-america-1941': {
      nome: 'Capitão América',
      periodo: '1941',
      poderes: [
        { nome: 'Força', valor: 70 },
        { nome: 'Agilidade', valor: 75 },
        { nome: 'Estrategista', valor: 85 },
        { nome: 'Combate', valor: 80 },
        { nome: 'Liderança', valor: 70 },
        { nome: 'Escudo', valor: 95 }
      ]
    },
    'captain-america-1985': {
      nome: 'Capitão América',
      periodo: '1985',
      poderes: [
        { nome: 'Força', valor: 75 },
        { nome: 'Agilidade', valor: 80 },
        { nome: 'Estrategista', valor: 95 },
        { nome: 'Combate', valor: 90 },
        { nome: 'Liderança', valor: 85 },
        { nome: 'Escudo', valor: 100 }
      ]
    },
    'captain-america-2020': {
      nome: 'Capitão América',
      periodo: '2020',
      poderes: [
        { nome: 'Força', valor: 80 },
        { nome: 'Agilidade', valor: 85 },
        { nome: 'Estrategista', valor: 100 },
        { nome: 'Combate', valor: 95 },
        { nome: 'Liderança', valor: 95 },
        { nome: 'Escudo', valor: 100 }
      ]
    }
  };

  return periodos.map(periodo =>
    PODERES_CURADOS[`captain-america-${periodo}`]
  );

  // Abordagem 2: Inferir a partir de issues (mais complexo)
  // Analisar issues de cada época, contar usos de cada poder, etc.
}
```

### Caso Real: Capitão América - Evolução 1941 → 2020

**Cenário**: Mostrar como as habilidades do Capitão América evoluíram através das décadas.

```typescript
// Dados preparados
const evolucaoCapitaoAmerica: PersonagemPoderes[] = [
  {
    nome: 'Capitão América',
    periodo: '1941 (Era de Ouro)',
    poderes: [
      { nome: 'Força', valor: 70 },
      { nome: 'Agilidade', valor: 75 },
      { nome: 'Estrategista', valor: 85 },
      { nome: 'Combate', valor: 80 },
      { nome: 'Liderança', valor: 70 },
      { nome: 'Escudo', valor: 95 }
    ]
  },
  {
    nome: 'Capitão América',
    periodo: '1985 (Wars Modernos)',
    poderes: [
      { nome: 'Força', valor: 75 },
      { nome: 'Agilidade', valor: 80 },
      { nome: 'Estrategista', valor: 95 },
      { nome: 'Combate', valor: 90 },
      { nome: 'Liderança', valor: 85 },
      { nome: 'Escudo', valor: 100 }
    ]
  },
  {
    nome: 'Capitão América',
    periodo: '2020 (Era Moderna)',
    poderes: [
      { nome: 'Força', valor: 80 },
      { nome: 'Agilidade', valor: 85 },
      { nome: 'Estrategista', valor: 100 },
      { nome: 'Combate', valor: 95 },
      { nome: 'Liderança', valor: 95 },
      { nome: 'Escudo', valor: 100 }
    ]
  }
];

// Como usar no Remotion
export const CenaEvolucaoPoderes: React.FC = () => {
  return (
    <div style={{ position: 'relative', width: '100%', height: '100%' }}>
      {/* Camada principal: Páginas do quadrinho sendo narradas */}
      <PaginasQuadrinho issue={issueComBatela} />

      {/* Overlay: Radar charts no centro */}
      <div style={{
        position: 'absolute',
        top: '50%',
        left: '50%',
        transform: 'translate(-50%, -50%)',
        width: 960,
        height: 600
      }}>
        <RadarChartAnimado
          personagens={evolucaoCapitaoAmerica}
          duracaoSegundos={8} // 8 segundos de duração
        />
      </div>
    </div>
  );
};
```

**Resultado Visual Esperado**:
- Três radar charts lado a lado (1941, 1985, 2020)
- Vértices animam crescendo do centro (efeito de "energia carregando")
- Valores numéricos aparecem após os vértices
- Comparação visual clara da evolução (principalmente em Estrategista e Liderança)
- Narração continua mostrando a batalha, enquanto o overlay mostra evolução

---

## MÓDULO 6: Localização/Locais

### Estratégia Técnica

**Conceito**: Mostrar onde a cena está acontecendo através de **mapas animados com pins** ou **cross-sections de bases**.

**Layout D3.js**: `d3.geoMercator()` para projeção geográfica + `d3.scaleLinear()` para posicionamento de pins.

**Por que D3 aqui**: D3 geography converte coordenadas (latitude: 40.7128, longitude: -74.0060) em posições X, Y no mapa, considerando projeções cartográficas.

```typescript
// D3.js como motor de layout para mapa com pins
import * as d3 from 'd3';
import { geoMercator, geoPath } from 'd3-geo';
import { feature } from 'topojson-client';

interface Localizacao {
  nome: string;
  latitude: number;
  longitude: number;
  tipo: 'base' | 'batalha' | 'cidade' | 'quartel';
  descricao?: string;
  imagemUrl?: string;
}

interface MapaData {
  localizacoes: Localizacao[];
  mostrarConexoes?: boolean; // Mostrar linhas conectando locais
}

/**
 * D3 Geo Projection - CONVERTE lat/long para posições X, Y no mapa
 */
function calcularPosicoesMapa(
  dados: MapaData,
  mapWidth: number,
  mapHeight: number
) {
  // Criar projeção Mercator (mostra mundo de forma retangular)
  const projection = geoMercator()
    .scale(150) // Zoom do mapa
    .translate([mapWidth / 2, mapHeight / 2]) // Centralizar
    .precision(0.1);

  // Criar gerador de path SVG para desenhar continentes
  const pathGenerator = geoPath().projection(projection);

  // Converter cada localização de lat/long para x, y
  const pins = dados.localizacoes.map(local => {
    const [x, y] = projection([local.longitude, local.latitude]);

    return {
      ...local,
      x,
      y,
      raio: local.tipo === 'base' ? 12 : 8 // Bases são pins maiores
    };
  });

  // Calcular conexões entre locais (linhas)
  const conexoes = dados.mostrarConexoes && dados.localizacoes.length > 1
    ? dados.localizacoes.slice(0, -1).map((local, i) => {
        const [x1, y1] = projection([local.longitude, local.latitude]);
        const [x2, y2] = projection([dados.localizacoes[i + 1].longitude, dados.localizacoes[i + 1].latitude]);

        return {
          x1, y1, x2, y2,
          distancia: calcularDistanciaKm(
            local.latitude, local.longitude,
            dados.localizacoes[i + 1].latitude,
            dados.localizacoes[i + 1].longitude
          )
        };
      })
    : [];

  return {
    pins,
    conexoes,
    projection,
    pathGenerator
  };
}

// Função auxiliar para calcular distância real entre dois pontos
function calcularDistanciaKm(
  lat1: number, lon1: number,
  lat2: number, lon2: number
): number {
  const R = 6371; // Raio da Terra em km
  const dLat = (lat2 - lat1) * Math.PI / 180;
  const dLon = (lon2 - lon1) * Math.PI / 180;
  const a =
    Math.sin(dLat / 2) * Math.sin(dLat / 2) +
    Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) *
    Math.sin(dLon / 2) * Math.sin(dLon / 2);
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
  return R * c;
}

/**
 * Componente Remotion que ANIMA o mapa com pins
 */
import { useEffect, useState, useMemo } from 'react';
import { interpolate, useCurrentFrame, useVideoConfig } from 'remotion';

interface MapaAnimadoProps {
  dados: MapaData;
  duracaoSegundos: number;
}

export const MapaAnimado: React.FC<MapaAnimadoProps> = ({
  dados,
  duracaoSegundos
}) => {
  const frame = useCurrentFrame();
  const { fps, width, height } = useVideoConfig();
  const frameTotal = duracaoSegundos * fps;

  // 1. D3 CALCULA posições (executa UMA vez)
  const { pins, conexoes, pathGenerator } = useMemo(() =>
    calcularPosicoesMapa(dados, width * 0.8, height * 0.6),
    [dados, width, height]
  );

  // 2. Carregar geometria do mundo (continentes) - usar mapa simplificado
  const [worldGeo, setWorldGeo] = useState<any>(null);

  useEffect(() => {
    // Carregar TopoJSON do mundo (ou GeoJSON)
    // Para simplificar, assumimos que carregamos um arquivo world-110m.json
    fetch('/maps/world-110m.json')
      .then(res => res.json())
      .then(geo => setWorldGeo(geo));
  }, []);

  // 3. Remotion ANIMA os pins surgindo

  // Animação de opacidade do mapa
  const mapOpacity = interpolate(frame, [0, 30], [0, 1]);

  // Animação sequencial dos pins
  const pinsVisiveis = Math.floor(
    interpolate(frame, [30, frameTotal - 30], [0, pins.length], { extrapolateRight: 'clamp' })
  );

  return (
    <div style={{
      position: 'relative',
      width: '100%',
      height: '100%',
      backgroundColor: 'rgba(0,0,0,0.85)',
      borderRadius: 10,
      padding: 20
    }}>
      {/* SVG do mapa mundial */}
      <svg
        width={width * 0.8}
        height={height * 0.6}
        style={{
          position: 'absolute',
          left: '50%',
          top: '50%',
          transform: 'translate(-50%, -50%)',
          opacity: mapOpacity
        }}
      >
        {/* Continentes (se worldGeo carregado) */}
        {worldGeo && (
          <path
            d={pathGenerator(feature(worldGeo, worldGeo.objects.countries)) as string}
            fill="rgba(255,255,255,0.1)"
            stroke="rgba(255,255,255,0.3)"
            strokeWidth={0.5}
          />
        )}

        {/* Conexões entre locais */}
        {conexoes.map((conexao, i) => {
          const frameEntrada = 30 + i * 10;
          const progresso = frame >= frameEntrada
            ? interpolate(frame, [frameEntrada, frameEntrada + 30], [0, 1], { extrapolateRight: 'clamp' })
            : 0;

          // Interpolar posição final da linha
          const xAtual = conexao.x1 + (conexao.x2 - conexao.x1) * progresso;
          const yAtual = conexao.y1 + (conexao.y2 - conexao.y1) * progresso;

          return (
            <g key={i}>
              {/* Linha traçada */}
              <line
                x1={conexao.x1}
                y1={conexao.y1}
                x2={xAtual}
                y2={yAtual}
                stroke="rgba(33, 150, 243, 0.6)"
                strokeWidth={2}
                strokeDasharray="5,5"
              />

              {/* Distância no meio da linha */}
              {progresso > 0.5 && (
                <text
                  x={(conexao.x1 + conexao.x2) / 2}
                  y={(conexao.y1 + conexao.y2) / 2 - 10}
                  fill="#FFFFFF"
                  fontSize={12}
                  textAnchor="middle"
                >
                  {conexao.distancia} km
                </text>
              )}
            </g>
          );
        })}
      </svg>

      {/* Pins de localização (HTML overlay para melhor renderização de texto) */}
      {pins.slice(0, pinsVisiveis).map((pin, i) => {
        const frameEntrada = 30 + i * 15;
        const scale = frame >= frameEntrada
          ? interpolate(frame, [frameEntrada, frameEntrada + 20], [0, 1], { extrapolateRight: 'clamp' })
          : 0;

        const cores = {
          base: '#FF5722',
          batalha: '#F44336',
          cidade: '#4CAF50',
          quartel: '#2196F3'
        };

        return (
          <div
            key={i}
            style={{
              position: 'absolute',
              left: pin.x,
              top: pin.y,
              transform: `translate(-50%, -50%) scale(${scale})`,
              transformOrigin: 'center'
            }}
          >
            {/* Pin (círculo pulsante) */}
            <div style={{
              width: pin.raio * 2,
              height: pin.raio * 2,
              borderRadius: '50%',
              backgroundColor: cores[pin.tipo],
              boxShadow: `0 0 ${10 + scale * 20}px ${cores[pin.tipo]}`,
              animation: 'pulse 2s infinite'
            }} />

            {/* Rótulo */}
            <div style={{
              position: 'absolute',
              top: pin.raio + 10,
              left: -60,
              width: 120,
              textAlign: 'center',
              fontSize: 13,
              fontWeight: 'bold',
              color: '#FFFFFF',
              backgroundColor: 'rgba(0,0,0,0.7)',
              padding: 6,
              borderRadius: 4,
              whiteSpace: 'nowrap'
            }}>
              {pin.nome}
              {pin.descricao && (
                <div style={{ fontSize: 11, fontWeight: 'normal', marginTop: 2 }}>
                  {pin.descricao}
                </div>
              )}
            </div>

            {/* Ícone do tipo */}
            <div style={{
              position: 'absolute',
              top: '50%',
              left: '50%',
              transform: 'translate(-50%, -50%)',
              fontSize: 10,
              color: '#FFFFFF'
            }}>
              {pin.tipo === 'base' ? '🏠' :
               pin.tipo === 'batalha' ? '⚔️' :
               pin.tipo === 'cidade' ? '🏙️' : '🎯'}
            </div>
          </div>
        );
      })}

      {/* Legenda */}
      <div style={{
        position: 'absolute',
        bottom: 20,
        left: 20,
        backgroundColor: 'rgba(0,0,0,0.7)',
        padding: 10,
        borderRadius: 4,
        fontSize: 11,
        color: '#FFFFFF'
      }}>
        <div><span style={{ color: '#FF5722' }}>●</span> Base</div>
        <div><span style={{ color: '#F44336' }}>●</span> Batalha</div>
        <div><span style={{ color: '#4CAF50' }}>●</span> Cidade</div>
        <div><span style={{ color: '#2196F3' }}>●</span> Quartel</div>
      </div>
    </div>
  );
};
```

### Integração Comic Vine API

**Endpoints Necessários**:

```typescript
// Comic Vine tem endpoint de "locations"
interface ComicVineLocation {
  id: number;
  name: string; // "Avengers Mansion", "Batcave", etc.
  description: string;
  image: string;
}

// GET /locations/?filter=name:avengers
// Retorna locais relacionados ao termo buscado

// No entanto, a Comic Vine NÃO fornece lat/long
// Precisamos de um mapeamento manual ou serviço externo
```

**Mapeamento de Locais**:

```typescript
// Mapeamento manual de locais importantes para coordenadas
const LOCAS_IMPORTANTES: Record<string, { lat: number; long: number; tipo: string }> = {
  'Avengers Mansion': {
    lat: 40.7614,
    long: -73.9776,
    tipo: 'base'
  },
  'Batcave': {
    lat: 39.8422,
    long: -74.8354, // Approximate (Wayne Manor, NJ)
    tipo: 'base'
  },
  'Daily Planet': {
    lat: 40.7580,
    long: -73.9855, // Metropolis ≈ NYC
    tipo: 'cidade'
  },
  'S.H.I.E.L.D. Helicarrier': {
    lat: 0,
    long: 0, // Móvel
    tipo: 'quartel'
  },
  'X-Mansion': {
    lat: 41.1616,
    long: -73.7371, // Salem Center, NY
    tipo: 'base'
  },
  'Fortress of Solitude': {
    lat: 83.6281,
    long: -32.4868, // Ártico
    tipo: 'base'
  }
  // ... mais locais
};

async function buscarLocalizacoesIssue(
  issueId: number
): Promise<Localizacao[]> {
  // 1. Buscar detalhes do issue
  const issue = await comicVineAPI.get(`/issue/4000-${issueId}`, {
    field_list: 'name,volume,description,location_credits'
  });

  // 2. Extrair locais mencionados na descrição
  const locaisMencionados = issue.description
    .match(/\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b/g) // Extract proper nouns
    ?.filter(nome => LOCAS_IMPORTANTES[nome]) || [];

  // 3. Mapear para localizações com coordenadas
  return locaisMencionados.map(nome => {
    const dadosLocal = LOCAS_IMPORTANTES[nome];
    return {
      nome,
      latitude: dadosLocal.lat,
      longitude: dadosLocal.long,
      tipo: dadosLocal.tipo as any
    };
  });
}
```

### Caso Real: Batalha Capitão América vs Barão Zemo (1941)

**Cenário**: Narração de batalha na base do Barão Zemo na Europa.

```typescript
// Dados preparados
const localizacoesBatalha: MapaData = {
  localizacoes: [
    {
      nome: 'Avengers Mansion',
      latitude: 40.7614,
      longitude: -73.9776,
      tipo: 'base',
      descricao: 'Base dos Vingadores'
    },
    {
      nome: 'Base do Barão Zemo',
      latitude: 51.1657,
      longitude: 10.4515,
      tipo: 'batalha',
      descricao: 'Alemanha Nazi'
    }
  ],
  mostrarConexoes: true
};

// Como usar no Remotion
export const CenaLocalizacaoBatalha: React.FC = () => {
  return (
    <div style={{ position: 'relative', width: '100%', height: '100%' }}>
      {/* Camada principal: Páginas do quadrinho sendo narradas */}
      <PaginasQuadrinho issue={issueBatalha} />

      {/* Overlay: Mapa no canto inferior direito */}
      <div style={{
        position: 'absolute',
        bottom: 20,
        right: 20,
        width: 640,
        height: 360,
        backgroundColor: 'rgba(0,0,0,0.9)',
        borderRadius: 10
      }}>
        <MapaAnimado
          dados={localizacoesBatalha}
          duracaoSegundos={6} // 6 segundos de duração
        />
      </div>
    </div>
  );
};
```

**Resultado Visual Esperado**:
- Mapa mundial no canto inferior direito
- Pin azul em NYC (Avengers Mansion)
- Linha tracejada animada traça rota até a Europa
- Pin vermelho surge na Alemanha (Base do Zemo)
- Distância mostrada: ~5,800 km
- Narração continua mostrando a batalha, enquanto o mapa dá contexto geográfico

---

## MÓDULO 7: Estatísticas de Publicação

### Estratégia Técnica

**Conceito**: Infográficos minimalistas mostrando métricas de publicação como **popularidade, ratings, número de issues, valor de colecionismo**.

**Layout D3.js**: `d3.scaleLinear()` para barras de progresso + `d3.scaleBand()` para posicionamento de elementos em grid.

**Por que D3 aqui**: D3 scales normalizam valores (rating 4.8 → 96% de barra) e calculam posições para layouts automáticos de infográficos.

```typescript
// D3.js como motor de layout para infográfico
import * as d3 from 'd3';
import { scaleLinear, scaleBand } from 'd3-scale';

interface EstatisticaItem {
  rotulo: string;
  valor: number;
  valorMaximo: number;
  tipo: 'barra' | 'numero' | 'badge';
  unidade?: string; // '%', '⭐', '#', etc.
  icone?: string;
}

interface EstatisticasData {
  itens: EstatisticaItem[];
  layout: 'horizontal' | 'grid';
}

/**
 * D3 Scales - NORMALIZA valores e CALCULA posições do infográfico
 */
function calcularInfografico(
  dados: EstatisticasData,
  containerWidth: number,
  containerHeight: number
) {
  const { layout } = dados;

  if (layout === 'horizontal') {
    // Layout horizontal: barras uma sobre a outra
    const alturaLinha = containerHeight / dados.itens.length;

    const itens = dados.itens.map((item, index) => {
      const y = index * alturaLinha;

      // Scale para normalizar valor (0-valorMaximo → 0-largura)
      const escalaBarra = scaleLinear()
        .domain([0, item.valorMaximo])
        .range([0, containerWidth - 200]); // Deixar espaço para rótulo

      const larguraBarra = escalaBarra(item.valor);

      return {
        ...item,
        x: 150, // Espaço para rótulo à esquerda
        y: y + alturaLinha / 2 - 15, // Centralizar na linha
        larguraBarra,
        alturaBarra: 30
      };
    });

    return { itens, tipo: 'horizontal' };
  } else {
    // Layout grid: itens em grade 2x2 ou 3x2
    const colunas = 2;
    const larguraColuna = containerWidth / colunas;
    const alturaLinha = containerHeight / Math.ceil(dados.itens.length / colunas);

    const itens = dados.itens.map((item, index) => {
      const col = index % colunas;
      const row = Math.floor(index / colunas);

      const x = col * larguraColuna;
      const y = row * alturaLinha;

      // Para badges/círculos
      const escalaTamanho = scaleLinear()
        .domain([0, item.valorMaximo])
        .range([60, 120]); // Tamanho do badge em px

      const tamanhoBadge = escalaTamanho(item.valor);

      return {
        ...item,
        x: x + larguraColuna / 2, // Centralizar na célula
        y: y + alturaLinha / 2,
        tamanhoBadge
      };
    });

    return { itens, tipo: 'grid' };
  }
}

/**
 * Componente Remotion que ANIMA o infográfico
 */
import { useMemo } from 'react';
import { interpolate, spring, useCurrentFrame, useVideoConfig } from 'remotion';

interface EstatisticasPublicacaoProps {
  dados: EstatisticasData;
  duracaoSegundos: number;
}

export const EstatisticasPublicacao: React.FC<EstatisticasPublicacaoProps> = ({
  dados,
  duracaoSegundos
}) => {
  const frame = useCurrentFrame();
  const { fps, width, height } = useVideoConfig();

  // 1. D3 CALCULA posições (executa UMA vez)
  const { itens } = useMemo(() =>
    calcularInfografico(dados, width, height),
    [dados, width, height]
  );

  // 2. Remotion ANIMA os valores (executa TODO frame)

  // Animação de entrada do container
  const containerScale = spring({
    frame,
    fps,
    config: { damping: 100, stiffness: 200 }
  });

  return (
    <div style={{
      position: 'relative',
      width: '100%',
      height: '100%',
      backgroundColor: 'rgba(0,0,0,0.9)',
      borderRadius: 10,
      padding: 30,
      transform: `scale(${containerScale})`,
      transformOrigin: 'center'
    }}>
      {/* Título */}
      <div style={{
        position: 'absolute',
        top: 15,
        left: 30,
        fontSize: 24,
        fontWeight: 'bold',
        color: '#FFFFFF'
      }}>
        📊 Estatísticas de Publicação
      </div>

      {/* Itens do infográfico */}
      {itens.map((item, i) => {
        const frameEntrada = 15 + i * 10; // Delay escalonado

        if (item.tipo === 'barra') {
          // Animação de barra crescendo
          const progressoBarra = frame >= frameEntrada
            ? interpolate(frame, [frameEntrada, frameEntrada + 30], [0, 1], { extrapolateRight: 'clamp' })
            : 0;

          const larguraAnimada = item.larguraBarra * progressoBarra;

          // Animação do número
          const valorAnimado = frame >= frameEntrada
            ? Math.round(interpolate(frame, [frameEntrada, frameEntrada + 30], [0, item.valor], { extrapolateRight: 'clamp' }))
            : 0;

          return (
            <div key={i} style={{ position: 'absolute', left: item.x, top: item.y }}>
              {/* Rótulo */}
              <div style={{
                position: 'absolute',
                left: -130,
                top: 5,
                width: 120,
                fontSize: 14,
                color: '#FFFFFF',
                textAlign: 'right',
                fontWeight: 'bold'
              }}>
                {item.rotulo}
              </div>

              {/* Barra de fundo */}
              <div style={{
                width: item.larguraBarra,
                height: item.alturaBarra,
                backgroundColor: 'rgba(255,255,255,0.1)',
                borderRadius: 15,
                overflow: 'hidden'
              }}>
                {/* Barra de progresso animada */}
                <div style={{
                  width: larguraAnimada,
                  height: item.alturaBarra,
                  background: `linear-gradient(90deg, #2196F3, #03A9F4)`,
                  borderRadius: 15,
                  transition: 'width 0.3s'
                }} />
              </div>

              {/* Valor numérico */}
              <div style={{
                position: 'absolute',
                right: -60,
                top: 5,
                fontSize: 16,
                fontWeight: 'bold',
                color: '#FFFFFF',
                minWidth: 50,
                textAlign: 'left'
              }}>
                {valorAnimado}{item.unidade}
              </div>
            </div>
          );
        } else if (item.tipo === 'badge') {
          // Animação de badge (círculo) crescendo
          const scale = frame >= frameEntrada
            ? interpolate(frame, [frameEntrada, frameEntrada + 20], [0, 1], { extrapolateRight: 'clamp' })
            : 0;

          // Animação do valor numérico
          const valorAnimado = frame >= frameEntrada
            ? Math.round(interpolate(frame, [frameEntrada, frameEntrada + 30], [0, item.valor], { extrapolateRight: 'clamp' }))
            : 0;

          return (
            <div key={i} style={{
              position: 'absolute',
              left: item.x,
              top: item.y,
              transform: 'translate(-50%, -50%)'
            }}>
              {/* Badge (círculo) */}
              <div style={{
                width: item.tamanhoBadge * scale,
                height: item.tamanhoBadge * scale,
                borderRadius: '50%',
                background: `conic-gradient(#2196F3 0%, #03A9F4 ${(valorAnimado / item.valorMaximo) * 100}%, rgba(255,255,255,0.1) ${(valorAnimado / item.valorMaximo) * 100}%)`,
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                boxShadow: '0 0 20px rgba(33, 150, 243, 0.5)'
              }}>
                {/* Centro do badge */}
                <div style={{
                  width: item.tamanhoBadge * 0.7 * scale,
                  height: item.tamanhoBadge * 0.7 * scale,
                  borderRadius: '50%',
                  backgroundColor: '#1A1A1A',
                  display: 'flex',
                  flexDirection: 'column',
                  alignItems: 'center',
                  justifyContent: 'center'
                }}>
                  {item.icone && (
                    <div style={{ fontSize: 20 }}>{item.icone}</div>
                  )}
                  <div style={{
                    fontSize: 24,
                    fontWeight: 'bold',
                    color: '#FFFFFF'
                  }}>
                    {valorAnimado}
                  </div>
                  <div style={{
                    fontSize: 10,
                    color: '#AAAAAA'
                  }}>
                    {item.rotulo}
                  </div>
                </div>
              </div>
            </div>
          );
        } else {
          // Tipo 'numero' - apenas número grande
          const scale = frame >= frameEntrada
            ? interpolate(frame, [frameEntrada, frameEntrada + 20], [0, 1], { extrapolateRight: 'clamp' })
            : 0;

          const valorAnimado = frame >= frameEntrada
            ? Math.round(interpolate(frame, [frameEntrada, frameEntrada + 30], [0, item.valor], { extrapolateRight: 'clamp' }))
            : 0;

          return (
            <div key={i} style={{
              position: 'absolute',
              left: item.x,
              top: item.y,
              transform: 'translate(-50%, -50%)',
              textAlign: 'center'
            }}>
              <div style={{
                fontSize: 48 * scale,
                fontWeight: 'bold',
                color: '#FFFFFF',
                textShadow: '0 0 20px rgba(33, 150, 243, 0.8)'
              }}>
                {valorAnimado}
              </div>
              <div style={{
                fontSize: 14,
                color: '#AAAAAA',
                marginTop: 5
              }}>
                {item.rotulo}
              </div>
            </div>
          );
        }
      })}
    </div>
  );
};
```

### Integração Comic Vine API

**Endpoints Necessários**:

```typescript
// Comic Vine tem dados limitados de estatísticas
interface ComicVineIssueStats {
  id: number;
  issue_number: string;
  date_added: string; // Data que foi adicionado à database
  store_date: string; // Data de publicação
}

interface ComicVineVolume {
  id: number;
  count: number; // Total de issues no volume
  start_year: string;
}

// Nota: Comic Vine NÃO fornece:
// - Ratings dos usuários (precisa de scraping manual)
// - Números de vendas (dados externos)
// - Valor de colecionismo (dados externos)
```

**Obter Dados de Múltiplas Fontes**:

```typescript
// Comic Vine para dados básicos
async function buscarDadosBasicos(issueId: number): Promise<ComicVineIssueStats> {
  const response = await fetch(
    `https://comicvine.gamespot.com/api/issue/4000-${issueId}/?api_key=${API_KEY}&format=json&field_list=issue_number,date_added,store_date,volume`
  );
  const data = await response.json();
  return data.results;
}

// Dados complementares (curadoria manual ou APIs externas)
interface EstatisticasComplementares {
  rating: number; // 0-5, da Comic Vine ou curadoria
  popularidade: number; // 0-100, baseado em views/favs
  vendasEstimadas?: number; // Dados históricos de vendas
  valorColecionismo?: number; // Dados de leilões
}

// Curadoria manual de issues importantes
const ESTATISTICAS_CURADAS: Record<string, EstatisticasComplementares> = {
  '4000-1105': { // Captain America #1
    rating: 4.8,
    popularidade: 95,
    vendasEstimadas: 1000000, // 1 milhão em 1941
    valorColecionismo: 350000 // $350k em leilão recente
  },
  // ... mais issues
};

function mapearParaInfografico(
  dadosComicVine: ComicVineIssueStats,
  dadosComplementares: EstatisticasComplementares
): EstatisticasData {
  return {
    layout: 'grid',
    itens: [
      {
        rotulo: 'Avaliação',
        valor: dadosComplementares.rating * 10,
        valorMaximo: 50,
        tipo: 'badge',
        unidade: '/ 5.0',
        icone: '⭐'
      },
      {
        rotulo: 'Popularidade',
        valor: dadosComplementares.popularidade,
        valorMaximo: 100,
        tipo: 'barra',
        unidade: '%'
      },
      {
        rotulo: 'Vendas (1941)',
        valor: Math.min(dadosComplementares.vendasEstimadas || 0, 1000000),
        valorMaximo: 1000000,
        tipo: 'badge',
        unidade: 'cópias',
        icone: '📚'
      },
      {
        rotulo: 'Valor Colecionismo',
        valor: Math.min(dadosComplementares.valorColecionismo || 0, 500000),
        valorMaximo: 500000,
        tipo: 'badge',
        unidade: 'USD',
        icone: '💰'
      }
    ]
  };
}
```

### Caso Real: Capitão América #1 - Issue Histórico

**Cenário**: Estatísticas do primeiro issue do Capitão América.

```typescript
// Dados preparados
const estatisticasCapAmerica1: EstatisticasData = {
  layout: 'grid',
  itens: [
    {
      rotulo: 'Avaliação',
      valor: 48,
      valorMaximo: 50,
      tipo: 'badge',
      unidade: '/ 5.0',
      icone: '⭐'
    },
    {
      rotulo: 'Popularidade',
      valor: 95,
      valorMaximo: 100,
      tipo: 'barra',
      unidade: '%'
    },
    {
      rotulo: 'Vendas (1941)',
      valor: 1000000,
      valorMaximo: 1000000,
      tipo: 'badge',
      unidade: 'cópias',
      icone: '📚'
    },
    {
      rotulo: 'Valor Colecionismo',
      valor: 350000,
      valorMaximo: 500000,
      tipo: 'badge',
      unidade: 'USD',
      icone: '💰'
    },
    {
      rotulo: 'Ano de Publicação',
      valor: 1941,
      valorMaximo: 2024,
      tipo: 'numero',
      unidade: ''
    },
    {
      rotulo: 'Issue #',
      valor: 1,
      valorMaximo: 100,
      tipo: 'numero',
      unidade: ''
    }
  ]
};

// Como usar no Remotion
export const CenaEstatisticasIssue1: React.FC = () => {
  return (
    <div style={{ position: 'relative', width: '100%', height: '100%' }}>
      {/* Camada principal: Páginas do quadrinho sendo narradas */}
      <PaginasQuadrinho issue={captainAmericaIssue1} />

      {/* Overlay: Infográfico no centro */}
      <div style={{
        position: 'absolute',
        top: '50%',
        left: '50%',
        transform: 'translate(-50%, -50%)',
        width: 800,
        height: 400,
        background: 'rgba(0,0,0,0.9)',
        borderRadius: 15
      }}>
        <EstatisticasPublicacao
          dados={estatisticasCapAmerica1}
          duracaoSegundos={5} // 5 segundos de duração
        />
      </div>
    </div>
  );
};
```

**Resultado Visual Esperado**:
- Grid 3x2 com badges e barras
- Badge circular com avaliação (⭐ 4.8/5.0)
- Barra de popularidade (95%)
- Badge de vendas (1M cópias - cheio)
- Badge de valor colecionismo ($350k)
- Números grandes de ano e issue number
- Animação sequencial dos itens surgindo
- Narração continua enquanto o overlay mostra estatísticas

---

## Pipeline de Produção (Módulos 4-7)

### Passo a Passo Completo

```typescript
/**
 * PIPELINE DE PRODUÇÃO PARA MÓDULOS 4-7
 *
 * Este pipeline integra os 4 módulos com a narração principal
 */

// 1. PREPARAÇÃO DE DADOS (executa UMA vez, antes da renderização)
async function prepararDadosModulos4_7(
  issueId: number,
  characterId: number
): Promise<{
  modulo4: TimelineData | null;
  modulo5: PersonagemPoderes[] | null;
  modulo6: MapaData | null;
  modulo7: EstatisticasData | null;
}> {
  // 1.1 Buscar dados da Comic Vine
  const [issue, volume, character] = await Promise.all([
    comicVineAPI.get(`/issue/4000-${issueId}`),
    comicVineAPI.get(`/volume/4050-${issueId}`),
    comicVineAPI.get(`/character/4005-${characterId}`)
  ]);

  // 1.2 Módulo 4: Contexto Histórico
  const modulo4 = await prepararContextoHistorico(issue);

  // 1.3 Módulo 5: Evolução de Poderes (se relevante)
  const modulo5 = await prepararEvolucaoPoderes(character, issue);

  // 1.4 Módulo 6: Localização (se relevante)
  const modulo6 = await prepararLocalizacao(issue);

  // 1.5 Módulo 7: Estatísticas
  const modulo7 = await prepararEstatisticas(issue);

  return { modulo4, modulo5, modulo6, modulo7 };
}

// 2. ANÁLISE DE ROTEIRO PARA IDENTIFICAR GATILHOS
interface GatilhoSubmodulo {
  frameInicio: number;
  tipoModulo: 4 | 5 | 6 | 7;
  prioridade: number; // 1-10, maior = mais relevante
  justificativa: string;
}

function analisarRoteiro(
  roteiro: string,
  dados: any
): GatilhoSubmodulo[] {
  const gatilhos: GatilhoSubmodulo[] = [];
  const palavrasChave = roteiro.split(' ');

  // Exemplo simplificado de análise
  palavrasChave.forEach((palavra, index) => {
    const frame = Math.floor(index / 2.5); // Assumir 2.5 palavras por frame @ 30fps

    if (palavra.toLowerCase().includes('guerra') || palavra.toLowerCase().includes('1941')) {
      gatilhos.push({
        frameInicio: frame,
        tipoModulo: 4,
        prioridade: 8,
        justificativa: 'Menção de contexto histórico'
      });
    }

    if (palavra.toLowerCase().includes('poder') || palavra.toLowerCase().includes('força')) {
      gatilhos.push({
        frameInicio: frame,
        tipoModulo: 5,
        prioridade: 7,
        justificativa: 'Menção de habilidades/poderes'
      });
    }

    if (palavra.toLowerCase().includes('base') || palavra.toLowerCase().includes('local')) {
      gatilhos.push({
        frameInicio: frame,
        tipoModulo: 6,
        prioridade: 6,
        justificativa: 'Menção de localização'
      });
    }
  });

  // Ordenar por prioridade e filtrar conflitos (mínimo 30 frames entre gatilhos)
  return gatilhos
    .sort((a, b) => b.prioridade - a.prioridade)
    .filter((gatilho, i, arr) => {
      if (i === 0) return true;
      return gatilho.frameInicio - arr[i - 1].frameInicio >= 30;
    });
}

// 3. COMPONENTE PRINCIPAL QUE ORQUESTRA TODOS OS MÓDULOS
interface VideoComModulos4_7Props {
  issueId: number;
  characterId: number;
  roteiro: string;
}

export const VideoComModulos4_7: React.FC<VideoComModulos4_7Props> = ({
  issueId,
  characterId,
  roteiro
}) => {
  // Dados preparados (viriam de props ou estado)
  const [dadosModulos, setDadosModulos] = useState<any>(null);
  const [gatilhos, setGatilhos] = useState<GatilhoSubmodulo[]>([]);

  useEffect(() => {
    // Preparar dados
    prepararDadosModulos4_7(issueId, characterId).then(setDadosModulos);

    // Analisar roteiro
    setGatilhos(analisarRoteiro(roteiro, dadosModulos));
  }, [issueId, characterId, roteiro]);

  const frame = useCurrentFrame();

  // Determinar qual submódulo mostrar (se houver)
  const submoduloAtivo = gatilhos.find(g =>
    frame >= g.frameInicio && frame < g.frameInicio + 210 // 7 segundos @ 30fps
  );

  return (
    <div style={{ width: '100%', height: '100%' }}>
      {/* CAMADA PRINCIPAL: Narração do quadrinho */}
      <PaginasQuadrinho roteiro={roteiro} />

      {/* CAMADAS SECUNDÁRIAS: Submódulos */}
      {submoduloAtivo && dadosModulos && (
        <>
          {submoduloAtivo.tipoModulo === 4 && dadosModulos.modulo4 && (
            <TimelineParalela
              dados={dadosModulos.modulo4}
              duracaoSegundos={7}
            />
          )}

          {submoduloAtivo.tipoModulo === 5 && dadosModulos.modulo5 && (
            <RadarChartAnimado
              personagens={dadosModulos.modulo5}
              duracaoSegundos={8}
            />
          )}

          {submoduloAtivo.tipoModulo === 6 && dadosModulos.modulo6 && (
            <MapaAnimado
              dados={dadosModulos.modulo6}
              duracaoSegundos={6}
            />
          )}

          {submoduloAtivo.tipoModulo === 7 && dadosModulos.modulo7 && (
            <EstatisticasPublicacao
              dados={dadosModulos.modulo7}
              duracaoSegundos={5}
            />
          )}
        </>
      )}
    </div>
  );
};
```

### Checklist de Produção

```
✅ FASE 1: PREPARAÇÃO (antes da renderização)
   □ Buscar dados da Comic Vine (issue, volume, character)
   □ Buscar dados históricos externos (Wikipedia, database local)
   □ Mapear poderes (curadoria manual ou inferência)
   □ Mapear localizações (lat/long)
   □ Preparar estatísticas (curadoria de dados complementares)
   □ Analisar roteiro para identificar gatilhos

✅ FASE 2: CONFIGURAÇÃO REMOTION
   □ Criar composição com duração total da narração
   □ Configurar frame rate (30fps recomendado)
   □ Preparar assets de áudio (narração)

✅ FASE 3: DESENVOLVIMENTO DOS COMPONENTES
   □ Implementar TimelineParalela (Módulo 4)
   □ Implementar RadarChartAnimado (Módulo 5)
   □ Implementar MapaAnimado (Módulo 6)
   □ Implementar EstatisticasPublicacao (Módulo 7)
   □ Testar animações individualmente

✅ FASE 4: INTEGRAÇÃO
   □ Criar componente orquestrador
   □ Implementar lógica de gatilhos
   □ Sincronizar submódulos com narração
   □ Ajustar timings e durações

✅ FASE 5: RENDERIZAÇÃO
   □ Renderizar vídeo em qualidade máxima
   □ Verificar sincronia áudio-vídeo
   □ Revisar proporção narração/submódulos (90/10)
   □ Exportar formato final

✅ FASE 6: PÓS-PRODUÇÃO
   □ Adicionar música de fundo (se aplicável)
   □ Normalizar áudio
   □ Comprimir para YouTube
   □ Upload e metadata
```

---

## Integração Entre Módulos 1-7

### Como Todos os 7 Módulos Trabalham Juntos

```
┌─────────────────────────────────────────────────────────────┐
│               VÍDEO "EVERY CHARACTER EXPLAINED"              │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  CAMADA PRINCIPAL (Sempre Ativa - 90% do tempo)             │
│  ├─ Narração contínua do quadrinho                          │
│  ├─ Páginas/painéis sequenciais                             │
│  └─ Timeline de publicação no rodapé                        │
│                                                              │
│  CAMADAS SECUNDÁRIAS (Intercaladas - 10% do tempo)          │
│                                                              │
│  Módulo 1: Curiosidades (popups durante narração)           │
│  ├─ Gatilho: Menção de criadores, prêmios, vendas           │
│  ├─ Duração: 3-5 segundos                                   │
│  └─ Layout: Popup no canto da tela                          │
│                                                              │
│  Módulo 2: Comparativo Visual                               │
│  ├─ Gatilho: Menção de aparência, uniforme, evolução        │
│  ├─ Duração: 5-8 segundos                                   │
│  └─ Layout: Split-screen ou grid comparativa                │
│                                                              │
│  Módulo 3: Árvore de Relacionamentos                        │
│  ├─ Gatilho: Introdução de novo personagem                  │
│  ├─ Duração: 6-10 segundos                                  │
│  └─ Layout: Grafo/árvore genealógica                        │
│                                                              │
│  Módulo 4: Contexto Histórico/Realidade                     │
│  ├─ Gatilho: Referência a eventos reais, época              │
│  ├─ Duração: 4-7 segundos                                   │
│  └─ Layout: Timeline paralela (quadrinho ↑ | mundo ↓)       │
│                                                              │
│  Módulo 5: Evolução de Poder/Habilidades                    │
│  ├─ Gatilho: Uso de poder, mudança de habilidades           │
│  ├─ Duração: 5-8 segundos                                   │
│  └─ Layout: Radar chart ou gráfico de barras                │
│                                                              │
│  Módulo 6: Localização/Locais                               │
│  ├─ Gatilho: Mudança de cenário, menção de lugar            │
│  ├─ Duração: 4-6 segundos                                   │
│  └─ Layout: Mapa animado com pins                           │
│                                                              │
│  Módulo 7: Estatísticas de Publicação                       │
│  ├─ Gatilho: Issue importante (milestone)                   │
│  ├─ Duração: 3-5 segundos                                   │
│  └─ Layout: Infográfico minimalista                         │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Exemplo Completo: Capitão América #1 (11 Minutos)

```typescript
/**
 * ESTRUTURA COMPLETA DE VÍDEO
 * Integrando todos os 7 módulos
 */

const estruturaVideoCapitaoAmerica1 = {
  duracaoTotal: 660, // 11 minutos @ 30fps = 19800 frames

  segmentos: [
    {
      inicio: 0,
      fim: 1350, // 0:00 - 0:45
      titulo: 'Introdução',
      narração: 'Contexto histórico de criação do Capitão América',
      submodulos: [
        {
          modulo: 7, // Estatísticas
          inicio: 450, // 0:15
          duracao: 240, // 8 segundos
          dados: estatisticasCapAmerica1
        }
      ]
    },
    {
      inicio: 1350,
      fim: 4050, // 0:45 - 2:15
      titulo: 'Primeiras cenas',
      narração: 'Steve Rogers antes do soro',
      submodulos: [
        {
          modulo: 4, // Contexto Histórico
          inicio: 2100, // 1:10
          duracao: 270, // 9 segundos
          dados: contextoWWII
        },
        {
          modulo: 1, // Curiosidade
          inicio: 3150, // 1:45
          duracao: 150, // 5 segundos
          dados: curiosidadeCriadores
        }
      ]
    },
    {
      inicio: 4050,
      fim: 6750, // 2:15 - 3:45
      titulo: 'Transformação',
      narração: 'Processo do Soro do Super-Soldado',
      submodulos: [
        {
          modulo: 5, // Evolução de Poderes
          inicio: 4500, // 2:30
          duracao: 240, // 8 segundos
          dados: evolucaoPoderes1
        }
      ]
    },
    {
      inicio: 6750,
      fim: 9450, // 3:45 - 5:15
      titulo: 'Primeira missão',
      narração: 'Sabotagem de base nazista',
      submodulos: [
        {
          modulo: 6, // Localização
          inicio: 7200, // 4:00
          duracao: 180, // 6 segundos
          dados: mapaEuropa1941
        },
        {
          modulo: 3, // Relacionamentos
          inicio: 8400, // 4:40
          duracao: 300, // 10 segundos
          dados: arvoreInimigos
        }
      ]
    },
    {
      inicio: 9450,
      fim: 12150, // 5:15 - 6:45
      titulo: 'Encontro Barão Zemo',
      narração: 'Primeiro vilão memorável',
      submodulos: [
        {
          modulo: 3, // Relacionamentos
          inicio: 9750, // 5:25
          duracao: 360, // 12 segundos
          dados: arvoreRelacionamentosZemo
        }
      ]
    },
    {
      inicio: 12150,
      fim: 14850, // 6:45 - 8:15
      titulo: 'Desenvolvimento',
      narração: 'Capitão América prova seu valor',
      submodulos: [
        {
          modulo: 5, // Evolução de Poderes
          inicio: 12600, // 7:00
          duracao: 240, // 8 segundos
          dados: evolucaoPoderes2
        }
      ]
    },
    {
      inicio: 14850,
      fim: 17550, // 8:15 - 9:45
      titulo: 'Clímax',
      narração: 'Batalha final e vitória',
      submodulos: [
        {
          modulo: 2, // Comparativo
          inicio: 15300, // 8:30
          duracao: 300, // 10 segundos
          dados: comparativo1941vs2020
        }
      ]
    },
    {
      inicio: 17550,
      fim: 19800, // 9:45 - 11:00
      titulo: 'Conclusão',
      narração: 'Legado do primeiro issue',
      submodulos: [
        {
          modulo: 7, // Estatísticas finais
          inicio: 18000, // 10:00
          duracao: 180, // 6 segundos
          dados: estatisticasFinais
        }
      ]
    }
  ],

  // Estatísticas do vídeo
  estatisticas: {
    duracaoNarracao: 594, // 9.9 minutos (90%)
    duracaoSubmodulos: 66, // 1.1 minutos (10%)
    numeroSubmodulos: 9,
    mediaEntreSubmodulos: 73.5, // ~2.3 minutos
    modulosUsados: [1, 2, 3, 4, 5, 6, 7], // Todos os 7 módulos
    variedade: 'Excelente - nenhum módulo repetido consecutivamente'
  }
};
```

### Princípios de Integração

```
1. NÃO SOBRECARREGAR
   - Máximo 1 submódulo a cada 2-3 minutos
   - Alternar tipos de módulos
   - Respeitar a regra 90/10

2. SINCRONIA PERFEITA
   - Conteúdo do submódulo = extremamente relevante à narração
   - Timing preciso: aparecer no momento exato da menção
   - Duração proporcional à complexidade

3. VARIEDADE VISUAL
   - Nunca repetir o mesmo tipo de módulo 2x seguido
   - Alternar layouts (popup, overlay, fullscreen, split-screen)
   - Variar posições na tela

4. PROGRESSÃO NARRATIVA
   - Módulos 1, 2, 7: Melhores para início/fim
   - Módulos 3, 5, 6: Melhores para meio (ação)
   - Módulo 4: Melhor para contexto histórico

5. FLUIDEZ
   - Animações de entrada/saída suaves
   - Transições entre nartação e submódulo imperceptíveis
   - A narração nunca para ou muda o ritmo
```

---

## Conclusão

Esta estratégia completa para **Módulos 4-7** integra perfeitamente com a estratégia anterior de **Módulos 1-3**, criando um sistema robusto de 7 módulos para vídeos explicativos de quadrinhos.

### Pilares Técnicos

1. **D3.js como Motor de Layout**: Calcula posições, dimensões, escalas, projeções geográficas - tudo executado UMA vez
2. **Remotion como Motor de Animação**: Controla frame-a-frame todas as transições, opacidades, escalas - executado TODO frame
3. **Comic Vine API como Fonte de Dados**: Fornece dados estruturados de issues, volumes, personagens, poderes
4. ** APIs Externas Complementares**: Wikipedia (história), map services (geolocalização), dados curados (estatísticas)

### Valor do Sistema

- **Escalável**: Templates funcionam para qualquer personagem/saga
- **Consistente**: Mesma linguagem visual em todos os vídeos
- **Eficiente**: 90% do trabalho é feito UMA vez (templates, D3 layouts)
- **Evolutivo**: Fácil adicionar novos módulos ou melhorar existentes
- **Engajador**: Variedade mantém espectadores interessados

### Próximos Passos

1. Implementar os componentes Remotion para Módulos 4-7
2. Criar database local de eventos históricos e localizações
3. Desenvolver sistema de análise de roteiro para gatilhos automáticos
4. Testar integração completa com um vídeo piloto
5. Iterar baseado em métricas de retenção e feedback

**Resultado Esperado**: Vídeos que são simultaneamente educativos (narração completa), visuais (quadrinhos em movimento), informativos (curiosidades e contexto), e tecnicamente impressionantes (visualizações de dados complexas feitas parecer simples).
