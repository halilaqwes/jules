
## 2024-05-20 - [Memoizing Sibling Components for Layout Thrashing]
**Learning:** In the frontend React application, lifting state up to a central layout component (like tracking `CodeEditor` keystrokes in `MainLayout` using `setCode`) causes severe layout thrashing and unnecessary reconciliation across the entire UI on every keystroke.
**Action:** When centralizing frequent state updates, always ensure heavy sibling components (like `AgentSidebar`, `FileExplorer`, and `ChatPanel`) are memoized using `React.memo` and their props are wrapped in `useCallback` to maintain referential equality and prevent re-rendering.
