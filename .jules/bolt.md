## 2026-06-14 - [Lifting State in React Layouts]
**Learning:** When lifting state (like CodeEditor keystrokes) up to a central layout component (`MainLayout`), it triggers a re-render of the entire layout on every keystroke. This causes severe layout thrashing and unnecessary reconciliation for heavy sibling components (like sidebars and explorers).
**Action:** Always memoize heavy sibling components using `React.memo` and wrap callbacks passed to them in `useCallback` when lifting high-frequency state (like text input) to a shared parent component.
