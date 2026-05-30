## 2026-05-30 - Prevent React Layout Thrashing with Memoization
**Learning:** In the frontend React application, lifting state up to a central layout component (like tracking `CodeEditor` keystrokes in `MainLayout`) causes heavy sibling components (`AgentSidebar`, `FileExplorer`, `ChatPanel`) to re-render on every keystroke, leading to severe layout thrashing and typing latency.
**Action:** Use `React.memo` for heavy sibling components and `useCallback` for the functions passed to them to prevent unnecessary reconciliation when central state changes frequently.
