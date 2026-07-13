# Streamlit UI Styling Guidelines - Yojana Setu

This document outlines the styling and layout standards for building premium, responsive, and visually stunning Streamlit interfaces.

## 1. Core Color Palette
To ensure visual consistency and national branding, all UI elements must strictly adhere to the following color palette:

| Color Name | Hex Code | Purpose / Usage |
|---|---|---|
| **Saffron** | `#FF9933` | Warnings, high-importance accents, and bright highlight states. |
| **Navy Blue** | `#000080` | Primary branding, text elements, structural backgrounds, active nav headers, and dark mode bases. |
| **Green** | `#128807` | Positive indicators, eligibility confirmations, success messages, and primary CTA buttons. |

## 2. Layout & Clean Paddings
* **Container Padding**: Always maintain clear spacing between the edge of the viewport and individual widgets. Avoid layout crowding.
* **Component Spacing**: Use margins between separate block elements. In Streamlit, this can be controlled via CSS (`margin-bottom`, `gap`) injected inside target classes.
* **Flex Alignment**: Navigation and headers must use `display: flex` with proper alignment (`align-items: center`) and clean gaps (`gap: 12px` to `16px`).

## 3. Modern Cards & Containers
Containers representing information blocks (e.g., scheme summaries, demographic inputs, and query logs) must use our modern card styling:
* **Backgrounds**: Light mode card background is `#ffffff`. Dark mode card background is `#111827` or a deep navy shade.
* **Border Radius**: Always use a consistent border-radius between `12px` and `16px` for a soft, premium aesthetic.
* **Box Shadows**: Apply soft shadows for depth:
  - Light mode shadow: `box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);`
  - Hover elevation: Elevate cards slightly on hover:
    `transform: translateY(-2px);`
    `box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);`
    `transition: transform 0.2s ease, box-shadow 0.2s ease;`

## 4. UI Elements and Components

### Tabs
* Inactive tabs should have a subtle border (`1px solid #e2e8f0`).
* Active tabs should highlight with **Green** (`#128807`) or **Navy Blue** (`#000080`) backgrounds and white text.

### Buttons
* Primary CTA buttons should feature a gradient or solid background using **Green** (`#128807`) or **Navy Blue** (`#000080`).
* On hover, change background color subtly (e.g., darkening or shifting gradient).
* Use round/pill-shaped buttons (`border-radius: 999px`) or clean rounded rectangles (`border-radius: 8px`).

### Badges & Alerts
* Use translucent background colors for badges matching their state:
  - Eligible / Success: `rgba(18, 136, 7, 0.08)` background, `#128807` text, and `#128807` border.
  - Alert / Highlighting: `rgba(255, 153, 51, 0.08)` background, `#FF9933` text, and `#FF9933` border.
  - Information / System: `rgba(0, 0, 128, 0.08)` background, `#000080` text, and `#000080` border.
