## 2024-08-10 - [React Layout Thrashing via Unmemoized State Lifting]
**Learning:** Lifting state up to a central layout component (like `MainLayout` tracking `CodeEditor`'s `code` state) causes layout thrashing and severe performance degradation if heavy child components (`AgentSidebar`, `ChatPanel`, `FileExplorer`) are not memoized. Every keystroke triggers a full tree render.
**Action:** Always wrap heavy sibling components in `React.memo` and use `useCallback` for their event handlers when sharing state from a common parent in React.
