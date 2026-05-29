
## 2024-05-29 - [Optimization: Prevent sibling component re-renders from state lift]
**Learning:** In the frontend React application, lifting state up to a central layout component (like tracking `CodeEditor` keystrokes in `MainLayout`) causes heavy sibling components (like `FileExplorer`, `AgentSidebar`, `ChatPanel`) to re-render unnecessarily on every keystroke, leading to severe layout thrashing and poor performance.
**Action:** When lifting frequently updated state, always memoize heavy sibling components using `React.memo` and ensure callbacks passed to them are memoized with `useCallback` to prevent widespread React tree reconciliation.
