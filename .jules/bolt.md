## 2026-06-03 - Prevent re-renders from state lifting in MainLayout
**Learning:** Lifting state up to a central layout component (like tracking `CodeEditor` keystrokes in `MainLayout`) without memoization causes severe layout thrashing and unnecessary reconciliation, as heavy sibling components like `AgentSidebar`, `ChatPanel`, and `FileExplorer` are forced to re-render on every keystroke.
**Action:** Use `useMemo` for sibling component renders and `useCallback` for their props when a parent component has a highly active state (e.g., text editor input).
