
## 2024-06-15 - [React Performance: Lifting State and Sibling Re-renders]
**Learning:** When lifting state up to a central layout component (like tracking `CodeEditor` keystrokes in `MainLayout`), it triggers re-renders for all child components. If sibling components are heavy (e.g. `FileExplorer`, `ChatPanel`, `AgentSidebar`), this causes severe layout thrashing and unnecessary reconciliation on every keystroke.
**Action:** Always memoize heavy sibling components using `React.memo` and wrap the associated callback functions passed to them in `useCallback` when state is managed in a common parent component to prevent performance bottlenecks.
