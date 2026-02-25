# Bug: Card Component - Fragmented Grid Calculation and Non-Reusable Design

## Bug Description
The current card implementation treats cards as 3 separate parts (cover + top label + bottom label) when calculating grid space, causing layout inefficiencies. The design also doesn't match the desired mockup (Image 2) which shows a unified vertical layout with image (70%), issue banner, and title banner. Additionally, the component is not reusable for different card types (covers, characters, objects, etc.) as required for ComicVine API use cases.

## Problem Statement
1. **Fragmented Grid Calculation**: `ComicCoversGrid.tsx:117-119` treats cards as separate parts with `labelHeight: { top, bottom }`, calculating space incorrectly instead of treating the card as a single unified element.
2. **Design Mismatch**: Current design (Image 1) shows separated badge and title, while desired design (Image 2) shows:
   - Top (70%): Cover image with border
   - Middle: Black banner with "ISSUE #n" text
   - Bottom: Black banner with title text (2 lines max)
3. **Non-Reusable Architecture**: Component is specific to comic covers (`ComicCard`) and cannot be reused for other ComicVine API types like characters, objects, concepts, teams, etc.
4. **Poor File Organization**: Current structure has `src/components/ComicCard/` but should have generic `src/components/Card/` with type-specific subdirectories.

## Solution Statement
1. **Unified Card Calculation**: Modify grid calculation to treat card as single element with fixed aspect ratio, not 3 separate parts.
2. **Implement New Design**: Create card matching Image 2 mockup with vertical layout (image 70%, issue banner, title banner).
3. **Simplified Card Architecture**: Single `Cover.tsx` file with unified card component. Future card types (Character, Object, etc.) will be separate files in same `Card/` directory when needed.
4. **File Restructuring**:
   - Create `src/components/Card/Cover.tsx` (single file with everything)
   - Delete `src/components/ComicCard/` directory
   - Future: `Card/Character.tsx`, `Card/Object.tsx` when needed

## Steps to Reproduce
1. View current grid layout in `ComicCoversGrid.tsx:338-349`
2. Notice `labelHeight: { top: 35, bottom: 65 }` at line 210
3. Observe `totalLabelHeight = labelHeight.top + labelHeight.bottom` at line 119
4. Compare current output with Image 1 (separated badge)
5. Compare with Image 2 (desired unified design with 2 black banners)

**Expected**: Card treated as single element, design matches Image 2 mockup
**Actual**: Card calculated as 3 parts, design doesn't match mockup, not reusable

## Root Cause Analysis

### Primary Issues:
1. **Grid Calculation Fragmentation** (`ComicCoversGrid.tsx:117-148`):
   - `calculateOptimalGrid()` accepts `labelHeight: { top, bottom }`
   - Calculates `maxCoverHeight = maxItemHeight - totalLabelHeight` separately
   - Forces separation between cover and labels instead of unified card sizing

2. **Component Monolith** (`ComicCard/` directory):
   - Single component hardcoded for comic covers
   - Types in `types.ts` are cover-specific (`ComicCardProps`, `ComicCardStyle`)
   - No abstraction for different card types (character, object, team, etc.)

3. **Design Implementation** (`ComicCard.tsx:127-175`):
   - Badge positioned at `top: coverHeight + 4` (separate from image)
   - Title positioned at `bottom: 0` (separate from badge)
   - No unified container with the 70%/15%/15% split from mockup

### Architecture Gaps:
- No generic `Card` base component
- No type-specific card implementations
- File structure doesn't support ComicVine API diversity (characters, issues, volumes, teams, objects, concepts, locations, people, powers, story_arcs)

## Relevant Files

### Files to Create:
- `my-video/src/components/Card/Cover.tsx` (single file with component + types + styles)

### Files to Modify:
- `my-video/src/ComicCoversGrid.tsx` (lines 110-162, 193-264, 274-353)
- `my-video/src/components/README.md` (documentation)

### Files to Delete:
- `my-video/src/components/ComicCard/` (entire directory)

### Reference Files:
- `docs/exemplos/api_usecases_comicvine.md` (future card types needed)

## Step by Step Tasks

### Task 1: Create Simplified Cover Card Component

1. **Create `src/components/Card/Cover.tsx`** (single file):
   - Define all types inline: `CoverData`, `CoverProps`, `CoverStyle`, `CoverVariant`
   - Create `CoverCard` component with Image 2 design:
     - Top 70%: Cover image with black border (2px)
     - Middle 15%: Black banner with "ISSUE #n" white text
     - Bottom 15%: Black banner with title white text (2 lines max)
   - Use flexbox column layout for vertical stacking
   - Port animation system from ComicCard (spring animations)
   - Add dynamic font sizing based on card width
   - Export: `export { CoverCard, default as defaultExport }`

2. **Style Variants** (in same file):
   - `default`: Image 2 design (black banners, white text)
   - `minimal`: No borders, clean look
   - `dark`: Dark background variant
   - Helper function: `getVariant(name: CoverVariant)`

### Task 2: Update Grid Calculation

3. **Refactor `calculateOptimalGrid()`** (`src/ComicCoversGrid.tsx:110-162`):
   - Remove `labelHeight: { top, bottom }` parameter
   - Add `cardAspectRatio: number` parameter (default: 3/5 for new design)
   - Simplify to single element calculation:
     ```typescript
     const calculateOptimalGrid = (
       itemCount: number,
       availableWidth: number,
       availableHeight: number,
       cardAspectRatio: number = 3 / 5,  // Width:Height for new card
       gap: number = 20
     ): OptimalGridResult
     ```
   - Remove `coverWidth`, `coverHeight` separation - use `cardWidth`, `cardHeight` only

4. **Update `calculateGridPositions()`** (`src/ComicCoversGrid.tsx:194-264`):
   - Remove `labelHeight` parameter
   - Add `cardAspectRatio` parameter (default: 3/5)
   - Return only `cardWidth` and `cardHeight` (unified)
   - Remove: `coverWidth`, `coverHeight`, `topLabelHeight`, `bottomLabelHeight`
   - Update return interface to simplified version

5. **Update `ComicCoversGrid` Component** (`src/ComicCoversGrid.tsx:274-353`):
   - Change import: `import { CoverCard } from './components/Card/Cover'`
   - Update component usage:
     ```tsx
     <CoverCard
       key={cover.filename}
       data={cover}
       width={cardWidth}
       height={cardHeight}
       variant="default"
     />
     ```
   - Remove old props: `coverWidth`, `coverHeight`, `itemWidth`, `itemHeight`, `bottomLabelHeight`

### Task 3: Update Components Export

6. **Update `src/components/index.tsx`** (if exists):
   - Add export for new CoverCard
   - Remove old ComicCard export

7. **Or update `src/components/ComicCard/index.tsx`** temporarily:
   - Re-export CoverCard as ComicCard for backward compatibility
   - This allows gradual migration

### Task 4: Documentation and Cleanup

8. **Update `src/components/README.md`**:
   - Update usage examples for new CoverCard
   - Document simplified single-file approach
   - Add design specs (70%/15%/15% layout)
   - Note: Future card types will be `Card/Character.tsx`, `Card/Object.tsx`, etc.

9. **Delete Old Directory**:
   - Delete `src/components/ComicCard/` after confirming new component works
   - Update any remaining imports in project

### Task 5: Validation

10. **Test and Verify**:
    - Run TypeScript compilation
    - Open Remotion preview
    - Verify grid layout (cards as single elements)
    - Verify design matches Image 2
    - Check console for validation logs

## Validation Commands

```bash
# Verify TypeScript compilation
cd my-video && npx tsc --noEmit

# Check for import errors
cd my-video && npx tsc --noUnusedLocals --noUnusedParameters

# Run Remotion dev server to visualize
cd my-video && npx remotion studio

# Verify grid calculation logs
# Look for "Grid Validation" output in console
# Should show unified card dimensions, not separated parts
```

**Manual Validation Steps:**
1. Open Remotion preview for `ComicCoversGrid` composition
2. Verify card design matches Image 2 (70% image, 15% issue banner, 15% title banner)
3. Verify grid spacing is uniform (cards treated as single elements)
4. Check console logs for "Grid Validation" - should show unified dimensions
5. Verify "ISSUE #n" format (with full word "ISSUE")
6. Verify title displays as 2 lines max, centered

## Notes

### Design Specifications (Image 2):
- **Card Layout**: Vertical flexbox, 100% height
- **Top Section (70%)**: Cover image with:
  - Black border: 2px solid
  - Background: Transparent or light pink (#FFE4E1 from mockup)
  - Image: Object-fit cover, centered
- **Middle Section (15%)**: Issue banner:
  - Background: Black (#000000)
  - Text: White, "ISSUE #n" format
  - Font: Handwritten/bold style
  - Alignment: Center
- **Bottom Section (15%)**: Title banner:
  - Background: Black (#000000)
  - Text: White, title content
  - Max lines: 2
  - Alignment: Center
  - Overflow: Ellipsis or truncate

### Card Aspect Ratio:
- New design: Width:Height ≈ 3:5 (taller, more vertical)
- Old design: Width:Height ≈ 2:3 (comic cover ratio)
- Update `cardAspectRatio` parameter accordingly

### Future Card Types (When Needed):
Per `docs/exemplos/api_usecases_comicvine.md`, create new single-file components in `Card/`:
- `Card/Character.tsx` - Name, aliases, powers, image
- `Card/Issue.tsx` - Issue details (similar to Cover)
- `Card/Volume.tsx` - Series name, start year, publisher
- `Card/Team.tsx` - Team name, members count, image
- `Card/Object.tsx` - Object name, description, image
- `Card/Concept.tsx` - Concept name, deck, description
- `Card/Location.tsx` - Location name, description, image
- `Card/Person.tsx` - Creator name, role, image
- `Card/Power.tsx` - Power name, description
- `Card/StoryArc.tsx` - Arc name, issue count, publisher

**Pattern**: Each type gets its own `Card/{TypeName}.tsx` file with component + types + styles all inline.

### Regression Risks:
- Grid calculation changes may affect existing compositions
- Style variants may need adjustment for new layout
- Animation timings may need tweaking for unified card
- Import paths throughout project need updating

### Migration Impact:
- Change imports: `from './components/ComicCard'` → `from './components/Card/Cover'`
- Component rename: `ComicCard` → `CoverCard`
- Props changes:
  - Old: `cover`, `coverWidth`, `coverHeight`, `itemWidth`, `itemHeight`, `bottomLabelHeight`
  - New: `data`, `width`, `height` (unified)
- Grid calculation: Remove `labelHeight: { top, bottom }`, use `cardAspectRatio`
