## 2026-07-03 - Prevent layout thrashing on fast keystrokes
**Learning:** In the React frontend, lifting state up to a central layout component (like tracking `CodeEditor` keystrokes in `MainLayout`) causes heavy sibling components (`AgentSidebar`, `FileExplorer`, `ChatPanel`) to re-render on every keystroke, which creates severe layout thrashing.
**Action:** When centralizing state that updates rapidly (like keystrokes), heavy sibling components must be memoized using `React.memo` and callbacks must be wrapped with `useCallback` to prevent unnecessary reconciliation.
