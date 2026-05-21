## 2023-10-25 - React.memo with useCallback in MainLayout
**Learning:** Lifting state up to a central layout component (like tracking `CodeEditor` keystrokes in `MainLayout`) causes severe layout thrashing and unnecessary reconciliation across the entire UI if heavy sibling components are not memoized.
**Action:** When tracking frequent state updates (like keystrokes) in a parent layout, ensure heavy sibling components (`AgentSidebar`, `ChatPanel`, `FileExplorer`) are wrapped in `React.memo` and the callback props passed to them are wrapped in `useCallback` to prevent continuous re-rendering.
