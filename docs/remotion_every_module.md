# Remotion - Todos os Módulos Disponíveis

Guia completo de todos os pacotes e módulos disponíveis no Remotion para criação programática de vídeos com React.

---

## 📦 Pacotes Principais (Core)

### `remotion` - Pacote Principal

O pacote principal do Remotion contém todas as funcionalidades core para criar composições de vídeo.

**Instalação:**
```bash
npm install remotion
```

**Importações Principais:**
```typescript
import {
  // Componentes
  AbsoluteFill,
  Composition,
  Video,
  Audio,
  Img,
  Sequence,
  Loop,
  Still,

  // Hooks
  useCurrentFrame,
  useVideoConfig,
  useAudioData,
  useCallback,

  // Utilitários
  interpolate,
  spring,
  staticFile,
  delayRender,
  continueRender,
  cancelRender,
  prefetch,

  // Tipos
  CompositionProps,
  VideoConfig
} from 'remotion';
```

**Exemplo Prático - Composição Básica:**
```tsx
import { Composition, AbsoluteFill, useCurrentFrame, useVideoConfig, interpolate, spring } from 'remotion';
import React from 'react';

export const MyVideo: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames, width, height } = useVideoConfig();

  // Animação de escala usando spring
  const scale = spring({
    frame,
    fps,
    config: {
      damping: 10,
      stiffness: 100,
      mass: 1,
    },
  });

  // Animação de opacidade usando interpolate
  const opacity = interpolate(frame, [0, 30], [0, 1]);

  return (
    <AbsoluteFill style={{ backgroundColor: '#000' }}>
      <div
        style={{
          width: '100%',
          height: '100%',
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
        }}
      >
        <h1
          style={{
            fontSize: 80,
            color: 'white',
            transform: `scale(${scale})`,
            opacity,
          }}
        >
          Hello Remotion!
        </h1>
      </div>
    </AbsoluteFill>
  );
};

// Configuração da composição no Root.tsx
import { Composition as RemotionComposition } from 'remotion';
import { MyVideo } from './MyVideo';

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <RemotionComposition
        id="MyVideo"
        component={MyVideo}
        durationInFrames={300}
        fps={30}
        width={1920}
        height={1080}
      />
    </>
  );
};
```

---

### `@remotion/cli` - Interface de Linha de Comando

Ferramenta CLI para executar comandos do Remotion como renderização, preview e mais.

**Instalação:**
```bash
npm install @remotion/cli
```

**Comandos Principais:**
```bash
# Iniciar o servidor de preview
npx remotion studio

# Renderizar um vídeo
npx remotion render <composition-id> output.mp4

# Renderizar frames
npx remotion render <composition-id> output/frame.png

# Listar composições
npx remotion compositions

# Ver parâmetros
npx remotion parameters <composition-id>

# Atualizar o Remotion
npx remotion upgrade
```

**Exemplo com Flags:**
```bash
# Renderizar com qualidade específica
npx remotion render MyVideo output.mp4 --codec=h264 --crf=18 --pixel-ratio=2

# Renderizar com props customizadas
npx remotion render MyVideo output.mp4 --props='{"title":"Hello World"}'

# Renderizar com determinados frames
npx remotion render MyVideo output.mp4 --frames=0-100
```

---

### `@remotion/player` - Player de Vídeo

Componente React para reproduzir composições do Remotion em uma aplicação web.

**Instalação:**
```bash
npm install @remotion/player
```

**Exemplo Prático:**
```tsx
import { Player } from '@remotion/player';
import { MyVideo } from './MyVideo';

export const App: React.FC = () => {
  return (
    <Player
      component={MyVideo}
      inputProps={{ title: 'Hello' }}
      durationInFrames={300}
      compositionWidth={1920}
      compositionHeight={1080}
      fps={30}
      style={{ width: '100%', height: '100%' }}
      controls
      loop
      autoPlay
    />
  );
};
```

**Props Disponíveis:**
```tsx
interface PlayerProps {
  component: React.FC<any>;
  inputProps?: any;
  durationInFrames: number;
  compositionWidth: number;
  compositionHeight: number;
  fps: number;
  style?: React.CSSProperties;
  controls?: boolean;
  loop?: boolean;
  autoPlay?: boolean;
  showVolumeControls?: boolean;
  allowFullscreen?: boolean;
  clickToPlay?: boolean;
  doubleClickToFullscreen?: boolean;
  spaceKeyToPlayOrPause?: boolean;
  inFrame?: number;
  playbackRate?: number;
  initialFrame?: number;
  className?: string;
}
```

---

## 🎨 Animação e Efeitos

### `@remotion/animations` - Animações Pré-definidas

Biblioteca de animações prontas para usar.

**Instalação:**
```bash
npx remotion add @remotion/animations
```

**Exemplo Prático:**
```tsx
import { fadeIn, slideInFromBottom, scaleIn } from '@remotion/animations';
import { AbsoluteFill, useCurrentFrame } from 'remotion';

export const AnimatedText: React.FC = () => {
  const frame = useCurrentFrame();

  // Fade in
  const fadeInStyle = fadeIn({
    frame,
    durationInFrames: 30,
  });

  // Slide in
  const slideStyle = slideInFromBottom({
    frame,
    durationInFrames: 40,
  });

  // Scale in
  const scaleStyle = scaleIn({
    frame,
    durationInFrames: 35,
  });

  return (
    <AbsoluteFill>
      <h1 style={fadeInStyle}>Fade In Text</h1>
      <h1 style={slideStyle}>Slide In Text</h1>
      <h1 style={scaleStyle}>Scale In Text</h1>
    </AbsoluteFill>
  );
};
```

**Animações Disponíveis:**
- `fadeIn()` - Opacidade de 0 a 1
- `fadeOut()` - Opacidade de 1 a 0
- `slideInFromLeft()` - Desliza da esquerda
- `slideInFromRight()` - Desliza da direita
- `slideInFromTop()` - Desliza de cima
- `slideInFromBottom()` - Desliza de baixo
- `scaleIn()` - Escala de 0 a 1
- `scaleOut()` - Escala de 1 a 0
- `rotateIn()` - Rotação ao entrar
- `flipIn()` - Efeito flip

---

### `@remotion/paths` - Animação de SVG Paths

Crie animações de desenho de SVG paths.

**Instalação:**
```bash
npx remotion add @remotion/paths
```

**Exemplo Prático:**
```tsx
import { evolvePath } from '@remotion/paths';
import { AbsoluteFill, useCurrentFrame, useVideoConfig, interpolate } from 'remotion';

export const DrawingPath: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Path SVG
  const path = "M 100 200 L 200 150 L 300 180 L 400 100";

  // Progresso de 0 a 1 ao longo de 2 segundos
  const progress = interpolate(frame, [0, 2 * fps], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  // Evoluir o path
  const { strokeDasharray, strokeDashoffset } = evolvePath(progress, path);

  return (
    <AbsoluteFill style={{ backgroundColor: '#1a1a1a' }}>
      <svg viewBox="0 0 500 300" style={{ width: '100%', height: '100%' }}>
        <path
          d={path}
          fill="none"
          stroke="#FF3232"
          strokeWidth={4}
          strokeDasharray={strokeDasharray}
          strokeDashoffset={strokeDashoffset}
        />
      </svg>
    </AbsoluteFill>
  );
};
```

**Funções Disponíveis:**
- `evolvePath()` - Anima o desenho do path
- `getBoundingBox()` - Obtém bounding box de um path
- `normalizePath()` - Normaliza um path SVG
- `reversePath()` - Inverte a direção do path
- `simplifyPath()` - Simplifica um path complexo

---

### `@remotion/motion-blur` - Motion Blur

Efeitos de motion blur para dar mais realismo às animações.

**Instalação:**
```bash
npx remotion add @remotion/motion-blur
```

**Exemplo Prático - Trail Effect:**
```tsx
import { Trail } from '@remotion/motion-blur';
import { AbsoluteFill, useCurrentFrame, interpolate } from 'remotion';

const BlueSquare: React.FC = () => {
  const frame = useCurrentFrame();
  const x = interpolate(frame, [0, 100], [0, 1000]);

  return (
    <div
      style={{
        width: 100,
        height: 100,
        backgroundColor: '#3b82f6',
        position: 'absolute',
        left: x,
        top: 100,
      }}
    />
  );
};

export const MotionBlurExample: React.FC = () => {
  return (
    <Trail layers={50} lagInFrames={0.1} trailOpacity={1}>
      <AbsoluteFill
        style={{
          backgroundColor: 'white',
          justifyContent: 'center',
          alignItems: 'center',
        }}
      >
        <BlueSquare />
      </AbsoluteFill>
    </Trail>
  );
};
```

**Exemplo Prático - Camera Motion Blur:**
```tsx
import { CameraMotionBlur } from '@remotion/motion-blur';
import { AbsoluteFill, useCurrentFrame, interpolate } from 'remotion';

export const CameraBlurExample: React.FC = () => {
  return (
    <CameraMotionBlur shutterSamples={32} delay={0}>
      <AbsoluteFill>
        <MovingContent />
      </AbsoluteFill>
    </CameraMotionBlur>
  );
};
```

---

## 📐 Formas e Layout

### `@remotion/shapes` - Formas Geométricas

Componentes e funções para criar formas geométricas SVG.

**Instalação:**
```bash
npx remotion add @remotion/shapes
```

**Exemplo Prático - Star:**
```tsx
import { Star } from '@remotion/shapes';
import { AbsoluteFill } from 'remotion';

export const StarExample: React.FC = () => {
  return (
    <AbsoluteFill
      style={{
        backgroundColor: 'white',
        justifyContent: 'center',
        alignItems: 'center',
      }}
    >
      <Star
        points={5}
        innerRadius={100}
        outerRadius={200}
        fill="red"
        stroke="black"
        strokeWidth={2}
      />
    </AbsoluteFill>
  );
};
```

**Exemplo Prático - Polygon:**
```tsx
import { Polygon } from '@remotion/shapes';

export const PolygonExample: React.FC = () => {
  return (
    <AbsoluteFill style={{ backgroundColor: '#f0f0f0' }}>
      <Polygon points={6} radius={150} fill="#4a9eff" />
    </AbsoluteFill>
  );
};
```

**Formas Disponíveis:**
- `<Star>` - Estrelas
- `<Triangle>` - Triângulos
- `<Circle>` - Círculos
- `<Ellipse>` - Elipses
- `<Polygon>` - Polígonos
- `<Pie>` - Gráficos de pizza
- `<Rect>` - Retângulos

**Funções Maker:**
- `makeStar()` - Cria path de estrela
- `makeTriangle()` - Cria path de triângulo
- `makeCircle()` - Cria path de círculo
- `makePolygon()` - Cria path de polígono
- `makePie()` - Cria path de gráfico de pizza

---

### `@remotion/layout-utils` - Utilitários de Layout

Funções para medir e ajustar textos e elementos.

**Instalação:**
```bash
npx remotion add @remotion/layout-utils
```

**Exemplo Prático - Fit Text:**
```tsx
import { fitText } from '@remotion/layout-utils';
import { AbsoluteFill } from 'remotion';

export const FitTextExample: React.FC<{ text: string }> = ({ text }) => {
  const { fontSize } = fitText({
    text,
    withinWidth: 600,
    fontFamily: 'Arial',
    fontWeight: 'bold',
  });

  return (
    <AbsoluteFill
      style={{
        justifyContent: 'center',
        alignItems: 'center',
        backgroundColor: 'white',
      }}
    >
      <div
        style={{
          width: 600,
          fontSize: Math.min(fontSize, 80), // Cap at 80px
          fontFamily: 'Arial',
          fontWeight: 'bold',
          textAlign: 'center',
        }}
      >
        {text}
      </div>
    </AbsoluteFill>
  );
};
```

**Exemplo Prático - Fit Text on N Lines:**
```tsx
import { fitTextOnNLines } from '@remotion/layout-utils';

export const MultilineText: React.FC<{ text: string }> = ({ text }) => {
  const { fontSize, lines } = fitTextOnNLines({
    text,
    maxBoxWidth: 600,
    maxLines: 3,
    fontFamily: 'Inter',
    fontWeight: 'bold',
    maxFontSize: 60,
  });

  return (
    <div style={{ width: 600, fontSize }}>
      {lines.map((line, i) => (
        <div key={i}>{line}</div>
      ))}
    </div>
  );
};
```

**Funções Disponíveis:**
- `fitText()` - Ajusta font size para caber em uma largura
- `fitTextOnNLines()` - Quebra texto em N linhas
- `measureText()` - Mede dimensões de texto
- `getDOMElementSize()` - Obtém tamanho de elemento DOM

---

## 🎬 Vídeo e Áudio

### `@remotion/media-parser` - Parser de Mídia

Extraia metadados de arquivos de vídeo e áudio.

**Instalação:**
```bash
npx remotion add @remotion/media-parser
```

**Exemplo Prático - Obter Duração:**
```tsx
import { parseMedia } from '@remotion/media-parser';
import { useEffect, useState } from 'react';

export const GetVideoMetadata: React.FC = () => {
  const [duration, setDuration] = useState<number | null>(null);

  useEffect(() => {
    const getMetadata = async () => {
      const result = await parseMedia({
        src: 'https://remotion.media/video.mp4',
        fields: {
          durationInSeconds: true,
          dimensions: true,
          fps: true,
          videoCodec: true,
        },
      });

      setDuration(result.durationInSeconds);
      console.log(result.dimensions); // {width: 1920, height: 1080}
    };

    getMetadata();
  }, []);

  return <div>Duration: {duration}s</div>;
};
```

**Exemplo Prático - Download e Parse:**
```tsx
import { downloadAndParseMedia } from '@remotion/media-parser';
import { nodeWriter } from '@remotion/media-parser/node-writer';

const downloadVideo = async () => {
  const { durationInSeconds, tracks } = await downloadAndParseMedia({
    src: 'https://example.com/video.mp4',
    writer: nodeWriter('output.mp4'),
    fields: {
      durationInSeconds: true,
      tracks: true,
    },
  });

  console.log('Downloaded!', durationInSeconds);
};
```

---

### `@remotion/gif` - Suporte a GIFs

Exiba GIFs animados sincronizados com a timeline.

**Instalação:**
```bash
npx remotion add @remotion/gif
```

**Exemplo Prático:**
```tsx
import { Gif } from '@remotion/gif';
import { AbsoluteFill } from 'remotion';

export const GifExample: React.FC = () => {
  return (
    <AbsoluteFill
      style={{
        backgroundColor: 'black',
        justifyContent: 'center',
        alignItems: 'center',
      }}
    >
      <Gif
        src="https://media.giphy.com/media/l0MYd5y8e1t0m/giphy.gif"
        width={500}
        height={500}
        style={{ objectFit: 'contain' }}
      />
    </AbsoluteFill>
  );
};
```

**Alternativa - AnimatedImage:**
```tsx
import { AnimatedImage } from 'remotion';

// Suporta GIF, APNG, AVIF, WebP
<AnimatedImage src="animation.gif" width={500} height={500} />
```

---

### `@remotion/preload` - Preload de Assets

Carregue assets antes de usá-los para melhor performance.

**Instalação:**
```bash
npx remotion add @remotion/preload
```

**Exemplo Prático:**
```tsx
import { preloadVideo, preloadAudio } from '@remotion/preload';
import { useEffect } from 'react';

export const PreloadAssets: React.FC = () => {
  useEffect(() => {
    // Preload assets quando o componente monta
    const unpreloadVideo = preloadVideo('https://example.com/video.mp4');
    const unpreloadAudio = preloadAudio('https://example.com/audio.mp3');

    // Cleanup quando desmonta
    return () => {
      unpreloadVideo();
      unpreloadAudio();
    };
  }, []);

  return <div>Assets preloaded!</div>;
};
```

**Exemplo com Resolver Redirect:**
```tsx
import { preloadVideo, resolveRedirect } from '@remotion/preload';

const preloadWithRedirect = async () => {
  let urlToLoad = 'https://example.com/video.mp4';

  try {
    const resolved = await resolveRedirect(urlToLoad);
    urlToLoad = resolved;
  } catch (err) {
    console.log('Could not resolve redirect', err);
  } finally {
    preloadVideo(urlToLoad);
  }
};
```

---

## 📝 Legendas e Transcrição

### `@remotion/captions` - Legendas e Subtítulos

Trabalhe com legendas em formatos SRT e VTT.

**Instalação:**
```bash
npx remotion add @remotion/captions
```

**Exemplo Prático - Parse SRT:**
```tsx
import { parseSrt } from '@remotion/captions';
import { useEffect, useState } from 'react';
import type { Caption } from '@remotion/captions';

export const LoadCaptions: React.FC = () => {
  const [captions, setCaptions] = useState<Caption[]>([]);

  useEffect(() => {
    const loadSrt = async () => {
      const response = await fetch('/subtitles.srt');
      const text = await response.text();

      const { captions: parsed } = parseSrt({ input: text });
      setCaptions(parsed);
    };

    loadSrt();
  }, []);

  return (
    <div>
      {captions.map((caption, i) => (
        <div key={i}>
          {caption.text} ({caption.startMs}ms - {caption.endMs}ms)
        </div>
      ))}
    </div>
  );
};
```

**Exemplo Prático - Serialize SRT:**
```tsx
import { serializeSrt, Caption } from '@remotion/captions';

const captions: Caption[] = [
  {
    text: 'Hello World',
    startMs: 0,
    endMs: 2500,
    timestampMs: 1250,
    confidence: 1,
  },
  {
    text: 'This is a subtitle',
    startMs: 3000,
    endMs: 6000,
    timestampMs: 4500,
    confidence: 1,
  },
];

const srtContent = serializeSrt({
  lines: captions.map((caption) => [caption]),
});

console.log(srtContent);
```

---

## 🌐 Cloud Rendering

### `@remotion/lambda` - AWS Lambda Rendering

Renderize vídeos na nuvem usando AWS Lambda.

**Instalação:**
```bash
npx remotion add @remotion/lambda
```

**Exemplo Prático - Render na CLI:**
```bash
# Deploy da função Lambda
npx remotion lambda functions deploy

# Render de vídeo
npx remotion lambda render https://my-site.com MyComposition

# Com props
npx remotion lambda render https://my-site.com MyComposition --props='{"title":"Hello"}'

# Com opções
npx remotion lambda render https://my-site.com MyComposition \
  --region=us-east-1 \
  --codec=h264 \
  --privacy=public \
  --concurrency=10
```

**Exemplo Prático - API Node.js:**
```tsx
import { renderMediaOnLambda, getRenderProgress } from '@remotion/lambda/client';

const renderVideo = async () => {
  const { renderId, bucketName } = await renderMediaOnLambda({
    region: 'us-east-1',
    functionName: 'remotion-render-bds9aab',
    composition: 'MyVideo',
    serveUrl: 'https://my-site.com',
    codec: 'h264',
    inputProps: {
      title: 'Hello World',
    },
    privacy: 'public',
  });

  console.log('Render started:', renderId);

  // Poll progress
  const progress = await getRenderProgress({
    renderId,
    bucketName,
    region: 'us-east-1',
  });

  console.log('Progress:', progress);
};
```

---

## 🎨 Estilização

### `@remotion/tailwind-v4` - TailwindCSS

Use TailwindCSS no Remotion.

**Instalação:**
```bash
npx remotion add @remotion/tailwind-v4
npm install tailwindcss @tailwindcss/postcss postcss postcss-preset-env autoprefixer
```

**Exemplo Prático - Configuração:**
```typescript
// remotion.config.ts
import { Config } from '@remotion/cli/config';
import { enableTailwind } from '@remotion/tailwind-v4';

Config.overrideWebpackConfig((currentConfiguration) => {
  return enableTailwind(currentConfiguration);
});
```

```javascript
// postcss.config.mjs
export default {
  plugins: ['@tailwindcss/postcss'],
};
```

```css
/* src/index.css */
@import 'tailwindcss';
```

```tsx
// src/Root.tsx
import './index.css';
import { Composition } from 'remotion';
import { MyVideo } from './MyVideo';

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="MyVideo"
        component={MyVideo}
        durationInFrames={300}
        fps={30}
        width={1920}
        height={1080}
      />
    </>
  );
};
```

**Exemplo de Uso:**
```tsx
export const MyVideo: React.FC = () => {
  return (
    <div className="flex items-center justify-center bg-black h-screen">
      <h1 className="text-8xl font-bold text-white">Hello Tailwind!</h1>
    </div>
  );
};
```

---

## 🎭 3D e Canvas

### `@remotion/three` - Three.js Integration

Renderize conteúdo 3D com Three.js e React Three Fiber.

**Instalação:**
```bash
npx remotion add @remotion/three
```

**Exemplo Prático - Cubo 3D:**
```tsx
import { ThreeCanvas } from '@remotion/three';
import { useCurrentFrame, useVideoConfig, interpolate } from 'remotion';

export const ThreeCube: React.FC = () => {
  const frame = useCurrentFrame();
  const { width, height } = useVideoConfig();

  return (
    <ThreeCanvas
      width={width}
      height={height}
      style={{ backgroundColor: 'white' }}
      camera={{ fov: 75, position: [0, 0, 470] }}
    >
      <ambientLight intensity={0.15} />
      <pointLight args={[undefined, 0.4]} position={[200, 200, 0]} />
      <mesh
        rotation={[
          frame * 0.06 * 0.5,
          frame * 0.07 * 0.5,
          frame * 0.08 * 0.5,
        ]}
        scale={interpolate(Math.sin(frame / 10), [-1, 1], [0.8, 1.2])}
      >
        <boxGeometry args={[100, 100, 100]} />
        <meshStandardMaterial
          color={[
            Math.sin(frame * 0.12) * 0.5 + 0.5,
            Math.cos(frame * 0.11) * 0.5 + 0.5,
            Math.sin(frame * 0.08) * 0.5 + 0.5,
          ]}
        />
      </mesh>
    </ThreeCanvas>
  );
};
```

**Exemplo Prático - Vídeo como Textura:**
```tsx
import { ThreeCanvas, useOffthreadVideoTexture } from '@remotion/three';
import { staticFile, useVideoConfig } from 'remotion';

const VideoTexture = () => {
  const { width, height } = useVideoConfig();
  const videoTexture = useOffthreadVideoTexture({
    src: staticFile('/video.mp4'),
  });

  return (
    <ThreeCanvas width={width} height={height}>
      <mesh>
        {videoTexture ? (
          <meshBasicMaterial map={videoTexture} />
        ) : null}
      </mesh>
    </ThreeCanvas>
  );
};
```

---

### `@remotion/react-canvas` - Canvas Rendering

Renderize conteúdo em canvas para performance.

**Instalação:**
```bash
npx remotion add @remotion/react-canvas
```

**Exemplo Prático - Vídeo com Canvas Filter:**
```tsx
import { useRef, useCallback } from 'react';
import { AbsoluteFill, useVideoConfig, OffthreadVideo } from 'remotion';

export const VideoWithFilter: React.FC = () => {
  const video = useRef<HTMLVideoElement>(null);
  const canvas = useRef<HTMLCanvasElement>(null);
  const { width, height } = useVideoConfig();

  const onVideoFrame = useCallback(
    (frame: CanvasImageSource) => {
      if (!canvas.current) return;

      const context = canvas.current.getContext('2d');
      if (!context) return;

      // Aplicar filtro grayscale
      context.filter = 'grayscale(100%)';
      context.drawImage(frame, 0, 0, width, height);
    },
    [height, width]
  );

  return (
    <AbsoluteFill>
      <AbsoluteFill>
        <OffthreadVideo
          style={{ opacity: 0 }}
          onVideoFrame={onVideoFrame}
          src="https://remotion.media/video.mp4"
        />
      </AbsoluteFill>
      <AbsoluteFill>
        <canvas ref={canvas} width={width} height={height} />
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
```

---

## 📊 Utilitários Adicionais

### `@remotion/zod-types` - Validação de Props

Valide as props das composições usando Zod.

**Instalação:**
```bash
npx remotion add @remotion/zod-types
```

**Exemplo Prático:**
```tsx
import { z } from 'zod';
import { Composition } from 'remotion';

const schema = z.object({
  title: z.string(),
  subtitle: z.string().optional(),
  color: z.string().regex(/^#[0-9A-F]{6}$/i),
});

type Props = z.infer<typeof schema>;

export const MyVideo: React.FC<Props> = ({ title, subtitle, color }) => {
  return (
    <div style={{ color }}>
      <h1>{title}</h1>
      {subtitle && <h2>{subtitle}</h2>}
    </div>
  );
};

// No Root.tsx
<Composition
  id="MyVideo"
  component={MyVideo}
  schema={schema}
  defaultProps={{
    title: 'Hello',
    subtitle: 'World',
    color: '#FF0000',
  }}
  durationInFrames={300}
  fps={30}
  width={1920}
  height={1080}
/>
```

---

### `@remotion/google-fonts` - Fontes Google

Importe fontes do Google Fonts facilmente.

**Instalação:**
```bash
npx remotion add @remotion/google-fonts
```

**Exemplo Prático:**
```tsx
import { getFont } from '@remotion/google-fonts';
import { useEffect, useState } from 'react';

export const GoogleFontExample: React.FC = () => {
  const [fontLoaded, setFontLoaded] = useState(false);

  useEffect(() => {
    const loadFont = async () => {
      const font = await getFont({
        family: 'Roboto',
        weights: [400, 700],
        style: 'normal',
      });

      console.log('Font URL:', font.src);
      setFontLoaded(true);
    };

    loadFont();
  }, []);

  return (
    <h1
      style={{
        fontFamily: "'Roboto', sans-serif",
        fontWeight: 700,
      }}
    >
      {fontLoaded ? 'Font Loaded!' : 'Loading...'}
    </h1>
  );
};
```

---

## 🚀 Performance e Otimização

### Técnicas de Otimização

**Usar OffthreadVideo para vídeos pesados:**
```tsx
import { OffthreadVideo } from 'remotion';

<OffthreadVideo src="heavy-video.mp4" />
```

**Preload de assets:**
```tsx
import { prefetch } from 'remotion';

useEffect(() => {
  const { free, waitUntilDone } = prefetch('video.mp4');

  waitUntilDone().then(() => {
    console.log('Video preloaded!');
    free();
  });
}, []);
```

**Usar Sequence para clonar conteúdo pesado:**
```tsx
import { Sequence } from 'remotion';

<Sequence from={0} durationInFrames={100}>
  <HeavyComponent />
</Sequence>

<Sequence from={100} durationInFrames={100}>
  {/* Reusa a instância anterior */}
  <HeavyComponent />
</Sequence>
```

---

## 📚 Referência Completa de Hooks

### Hooks Principais

```typescript
// Tempo e config
useCurrentFrame() // Retorna o frame atual
useVideoConfig() // Retorna config do vídeo (fps, dimensões, duração)

// Audio
useAudioData(src) // Retorna dados do áudio
useAudioFrameData() // Retorna dados do frame atual do áudio

// Prefetch
usePrefetchAssets() // Prefetch assets

// Delay render
useDelayRender() // Atrasa o render para operações assíncronas

// Environment
useRemotionEnvironment() // Info sobre o ambiente (render vs player)

// Transformações
useTransform() // Aplica transformações
useScale() // Escala
useRotation() // Rotação
```

---

## 🎯 Boas Práticas

1. **Sempre use versões alinhadas** dos pacotes @remotion/*
2. **Use OffthreadVideo** para vídeos pesados em produção
3. **Preload assets** antes de usá-los
4. **Use Sequence** para reutilizar componentes pesados
5. **Valide props** com Zod para catching de erros
6. **Use fitText()** para responsividade de texto
7. **Prefira spring()** sobre animate() para movimentos naturais
8. **Use AbsoluteFill** para containers full-screen

---

## 🔗 Links Úteis

- [Documentação Oficial](https://www.remotion.dev/)
- [Exemplos](https://github.com/remotion-dev/remotion/tree/main/packages/example)
- [GitHub](https://github.com/remotion-dev/remotion)
- [Discord](https://discord.gg/6VrND8dE9u)

---

**Última atualização:** 2025-02-19
**Versão do Remotion:** 4.0+
