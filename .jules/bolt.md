
## 2024-08-05 - Lifted State Re-render Thrashing
**Learning:** In the frontend React application, lifting state up to a central layout component (like tracking `CodeEditor` keystrokes in `MainLayout`) causes severe layout thrashing and unnecessary reconciliation of all other components in the layout on every keystroke, degrading performance drastically.
**Action:** When centralizing state that updates frequently (like editor content), explicitly wrap heavy sibling components (`AgentSidebar`, `FileExplorer`, `ChatPanel`, `CodeEditor`) with `React.memo` and strictly use `useCallback` for functions passed down as props to prevent them from re-rendering unnecessarily.
