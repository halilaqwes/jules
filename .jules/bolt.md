
## 2024-05-18 - [Layout Memoization for Keystroke Thrashing]
**Learning:** In the frontend React app, when state is lifted up to a parent component (like tracking `CodeEditor` keystrokes in `MainLayout`), it causes all sibling components (e.g. `AgentSidebar`, `FileExplorer`, `ChatPanel`) to re-render on every keystroke. This produces severe layout thrashing and unnecessary reconciliation because these are heavy components.
**Action:** When creating layouts with lifted state, heavy sibling components must be aggressively memoized using `React.memo` and the callbacks passed to them must be wrapped with `useCallback` to prevent this anti-pattern.
