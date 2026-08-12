## 2024-08-12 - Prevent Re-renders When Lifting State
**Learning:** Lifting frequently updating state (like `CodeEditor`'s `onChange` updating `code` in `MainLayout`) causes severe layout thrashing because it forces all heavy sibling components (`AgentSidebar`, `FileExplorer`, `ChatPanel`) to re-render on every keystroke.
**Action:** When lifting frequently updating state to a parent layout, ensure heavy sibling components are wrapped in `React.memo` and the callbacks passed to them are memoized using `useCallback` to prevent unnecessary reconciliation.
