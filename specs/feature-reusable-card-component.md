# Feature: Componente de Card Reutilizável para Comic Covers

## Feature Description

Extrair o componente `ComicCoverItem` atual para um módulo reutilizável e facilmente customizável, localizado em `src/components/`. O componente deve suportar diferentes variantes de design (estilos) através de uma API de configuração simples, permitindo que mudanças no componente se reflitam automaticamente em todas as composições que o utilizam.

## User Story

Como um **desenvolvedor** trabalhando em vídeos de comic covers, eu quero **ter um componente de card reutilizável com variantes de design** para que eu possa **facilmente alterar o visual dos cards sem precisar modificar código em múltiplos lugares**.

## Problem Statement

O componente `ComicCoverItem` atual está:
- **Embutido dentro de `ComicCoversGrid.tsx`** - não é reutilizável
- **Com estilos hard-coded** - mudar cores, fontes ou espaçamentos requer editar o código do componente
- **Sem sistema de variantes** - não é possível alternar entre diferentes designs
- **Difícil de manter** - qualquer alteração afeta diretamente o grid principal
- **Não extensível** - adicionar novos estilos requer modificar o componente existente

## Solution Statement

Criar um componente `ComicCard` reutilizável em `src/components/ComicCard/index.tsx` com:
1. **Interface de props bem definida** - todos os aspectos customizáveis via props
2. **Sistema de variantes/temas** - pré-definições de estilo que podem ser selecionadas
3. **TypeScript types** - type-safety para todas as configurações
4. **Exportação de estilos padrão** - fáceis de importar e modificar
5. **Separação de concerns** - lógica de animação separada da renderização visual

## Relevant Files

### New Files
- `my-video/src/components/ComicCard/index.tsx` (Main component export)
- `my-video/src/components/ComicCard/ComicCard.tsx` (Component implementation)
- `my-video/src/components/ComicCard/types.ts` (TypeScript interfaces)
- `my-video/src/components/ComicCard/styles.ts` (Style variants and presets)
- `my-video/src/components/ComicCard/animations.ts` (Animation configurations)
- `my-video/src/components/index.ts` (Barrel export for all components)

### Modified Files
- `my-video/src/ComicCoversGrid.tsx` (Import and use new ComicCard component)
- `my-video/src/Root.tsx` (Potentially add example compositions with different styles)

## Implementation Plan

### Foundation Phase

**1. Create component directory structure**
- Create `src/components/` directory structure
- Set up barrel exports in `src/components/index.ts`

**2. Define TypeScript interfaces**
- `ComicCardProps` - main component props
- `ComicCardStyle` - style configuration type
- `ComicCardVariant` - preset style variants (default, minimal, elaborate, dark)
- `ComicCardAnimationConfig` - animation settings

**3. Extract style definitions**
- Move all hard-coded style values to `styles.ts`
- Create variant presets with named styles
- Export style utilities for creating custom variants

### Core Phase

**4. Implement ComicCard component**
- Extract the JSX structure from current `ComicCoverItem`
- Convert inline styles to use the style configuration system
- Maintain all Remotion hooks (useCurrentFrame, useVideoConfig)
- Preserve existing animation behavior

**5. Implement style application logic**
- Create helper function to merge variant styles with custom overrides
- Handle responsive font sizing based on card dimensions
- Support dynamic color schemes

**6. Create variant presets**
- `default` - current design (light theme, shadows, borders)
- `minimal` - clean design without shadows/borders
- `elaborate` - enhanced design with more decorations
- `dark` - dark theme variant
- `comic` - themed for comic books (bold colors, fonts)

### Integration Phase

**7. Update ComicCoversGrid to use new component**
- Import `ComicCard` from components
- Replace inline `ComicCoverItem` with `<ComicCard>`
- Pass `variant` prop to select style
- Add example of custom style override

**8. Create example compositions**
- Add `ComicCoversGridMinimal` using minimal variant
- Add `ComicCoversGridDark` using dark variant
- Demonstrate custom style override

**9. Documentation**
- Add JSDoc comments to all exports
- Create README in components/ directory with usage examples
- Document available props and variants

## Step by Step Tasks

1. **Create component directory**: `mkdir -p my-video/src/components/ComicCard`

2. **Create types file** (`my-video/src/components/ComicCard/types.ts`):
   - Define `ComicCardProps` interface
   - Define `ComicCardStyle` interface with all style properties
   - Define `ComicCardVariant` type union
   - Define `AnimationConfig` interface

3. **Create styles file** (`my-video/src/components/ComicCard/styles.ts`):
   - Extract current inline styles to `defaultVariant` object
   - Create `minimalVariant`, `darkVariant`, `elaborateVariant`
   - Export `mergeStyles()` helper function
   - Export `createCustomVariant()` utility

4. **Create animations file** (`my-video/src/components/ComicCard/animations.ts`):
   - Extract spring configuration to `defaultAnimationConfig`
   - Export animation preset functions

5. **Implement ComicCard component** (`my-video/src/components/ComicCard/ComicCard.tsx`):
   - Copy `ComicCoverItem` logic
   - Replace hard-coded styles with props.variant styles
   - Apply `mergeStyles()` for custom overrides
   - Keep Remotion hooks and animations

6. **Create component index** (`my-video/src/components/ComicCard/index.tsx`):
   - Export `ComicCard` as default
   - Export all types
   - Export all variant presets
   - Export utility functions

7. **Create components barrel export** (`my-video/src/components/index.ts`):
   - Export `ComicCard` and related types

8. **Update ComicCoversGrid.tsx**:
   - Import `ComicCard` from '@/components'
   - Replace `<ComicCoverItem ... />` with `<ComicCard variant="default" ... />`
   - Remove old `ComicCoverItem` component definition

9. **Add example compositions in Root.tsx**:
   - Add `ComicCoversGridMinimal` composition
   - Add `ComicCoversGridDark` composition
   - Add `ComicCoversGridCustom` with inline style override

10. **Create components README** (`my-video/src/components/README.md`):
    - Document how to use `ComicCard`
    - List all available props
    - Show variant examples
    - Explain how to create custom variants

## Testing Strategy

### Unit Tests
- **Style merging function**: Test that `mergeStyles()` correctly combines variants with overrides
- **Variant creation**: Test `createCustomVariant()` generates valid style objects
- **Component rendering**: Test component renders without errors with all variants

### Integration Tests
- **Grid rendering**: Test that `ComicCoversGrid` renders correctly with new `ComicCard`
- **Variant switching**: Test that changing variant prop updates the visual output
- **Custom overrides**: Test that custom style props override variant styles correctly

### Visual Regression Tests
- **Screenshot comparisons**: Take screenshots of each variant to ensure visual consistency
- **Animation verification**: Verify animations work the same as before

### Edge Cases
- **Empty title**: Test card with empty or very long title text
- **Single digit vs double digit issue numbers**: Test badge sizing
- **Small dimensions**: Test card at minimum sizes (150px width)
- **Large dimensions**: Test card at maximum sizes
- **Missing image**: Test fallback behavior when image fails to load
- **Invalid variant**: Test component handles invalid variant name gracefully

## Acceptance Criteria

- [ ] `ComicCard` component exists in `src/components/ComicCard/`
- [ ] Component accepts `variant` prop with at least 4 presets (default, minimal, dark, elaborate)
- [ ] Component accepts `style` override prop for custom styling
- [ ] All existing functionality preserved (animations, hover effects, text truncation)
- [ ] `ComicCoversGrid.tsx` updated to use new `ComicCard` component
- [ ] Old `ComicCoverItem` code removed from `ComicCoversGrid.tsx`
- [ ] At least 2 example compositions added in `Root.tsx` showing different variants
- [ ] TypeScript compiles without errors
- [ ] Remotion Studio renders all compositions correctly
- [ ] Component is properly exported from `src/components/index.ts`
- [ ] JSDoc comments added to all public APIs
- [ ] README created in components directory with usage examples

## Validation Commands

```bash
# 1. TypeScript compilation check
cd C:/Users/JOSE/Downloads/youtube-channel/my-video
npx tsc --noEmit

# 2. Start Remotion Studio
npm run dev

# 3. Manual verification in Studio:
#    - Open ComicCoversGrid composition (should use default variant)
#    - Verify all cards render correctly
#    - Check animations work as before
#    - Open ComicCoversGridMinimal composition (if created)
#    - Verify minimal variant styling applies

# 4. Visual verification checklist:
#    - Default variant looks identical to original design
#    - Minimal variant shows cleaner look without shadows
#    - Dark variant shows dark theme colors
#    - Text truncation still works for long titles
#    - Issue number badge scales correctly
#    - Hover/animation effects preserved

# 5. Test variant switching:
#    Add to ComicCoversGrid.tsx temporarily:
#    <ComicCard variant="dark" ... />
#    <ComicCard variant="minimal" ... />
#    Verify each renders correctly

# 6. Test custom style overrides:
#    <ComicCard
#      variant="default"
#      customStyle={{ badge: { backgroundColor: 'red' } }}
#      ...
#    />
#    Verify red background appears on badge

# 7. Render test
npx remotion render ComicCoversGrid out/test-comiccard.mp4 --jpeg-quality=80
```

## Notes

### Related Features
- **Style editor UI** (future): Could build a visual editor to create custom variants
- **Animation presets** (future): Extend to support different animation styles
- **Responsive variants** (future): Different variants based on screen size

### Technical Considerations
- **Remotion constraints**: Component must continue using `useCurrentFrame()` and `useVideoConfig()`
- **Inline styles**: Remotion works best with inline styles (avoid CSS modules/styled-components)
- **Performance**: Style calculations should happen once per render, not per frame
- **Type safety**: Maintain strict TypeScript types for all style properties

### Migration Path
- Old code remains working during transition (can keep `ComicCoverItem` temporarily)
- New component is drop-in replacement with same props interface
- Gradual migration: test new component in one composition before replacing all uses

### Future Enhancements
- **Prop-based theme system**: Pass entire theme object instead of variant name
- **CSS-in-JS integration**: Consider emotion/styled-components if inline styles become unmanageable
- **Component composition**: Split into sub-components (Badge, Image, Title) for more flexibility
- **Animation library**: Support framer-motion or other animation libraries as alternative to Remotion springs

### Dependencies
- No new npm packages required
- Uses existing `remotion` and `react` dependencies
- May consider adding `@types/react` if not already present (should be)

### Breaking Changes
- None - this is a refactor that maintains backward compatibility
- Old `ComicCoverItem` can be removed after verification that new component works
