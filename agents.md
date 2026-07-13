# Team Configuration: Yojana Setu

This document defines the roles, responsibilities, and workflows for the development team of the Yojana Setu project.

## Team Roles

### 1. Frontend Designer
* **Core Focus**: User Experience (UX), User Interface (UI) design, and visual polish.
* **Responsibilities**:
  - Implement modern CSS styling and animations.
  - Enforce clean layout guidelines, paddings, and color harmonies.
  - Design layouts that look premium and function fluidly across different devices and viewports.
  - Collaborate with the Software Engineer on integration of frontend components with app logic.

### 2. Software Engineer
* **Core Focus**: Application architecture, backend logic, and API integrations.
* **Responsibilities**:
  - Build and optimize backend components such as database query functions, custom RAG integrations, and API clients.
  - Implement reliable state management, location lookup, translation logic, and logging utils.
  - Ensure the codebase conforms to software engineering best practices (modularity, error handling, clean documentation).
  - Work closely with the Frontend Designer to bind backend state/actions to UI components.

### 3. QA Engineer
* **Core Focus**: Quality assurance, testing, validation, and stability.
* **Responsibilities**:
  - Establish verification plans, test coverage, and write automated tests.
  - Perform manual verification of styling, layout responsiveness, and accessibility (a11y).
  - Verify edge cases, validate user flow under network delays, and check resilience to malformed inputs.
  - Coordinate with the rest of the team to fix bugs and visual regressions.

## Collaboration Workflow

1. **Design First**: The Frontend Designer drafts layout structures and styling systems.
2. **Implement Logic**: The Software Engineer writes the core application flow, ensuring solid functionality.
3. **Refine UI**: The Frontend Designer applies custom style rules, colors, and layout polish to the active application.
4. **Assure Quality**: The QA Engineer runs automated scripts, audits the codebase, and checks against requirements before production deployment.
