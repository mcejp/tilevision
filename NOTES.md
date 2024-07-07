## Primitives

- background map
    - solid color tiles only
- text labels
    - x
    - y
    - text
    - color
- paths
    - SVG command string
    - linedash
    - linewidth
    - stroke
    - fill

### Proposed

- labels & paths should not be in separate lists

- define-path
    - SVG command string
    - linedash
    - linewidth
    - stroke
    - fill
- use-path
    - path ID
    - x, y, scale
    - (optional overrides of any path attributes)