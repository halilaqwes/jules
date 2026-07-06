
## 2024-05-18 - React State Hoisting Layout Thrashing
**Learning:** Lifting state (like `code` on every keystroke) to a top-level component (`MainLayout`) causes severe layout thrashing if heavy sibling components (`AgentSidebar`, `FileExplorer`, `ChatPanel`) are not properly memoized, as they needlessly re-render on every keystroke.
**Action:** When centralizing frequent state updates (like editor keystrokes), always use `React.memo` on static or expensive sibling components and `useCallback` on event handlers passed to them to preserve referential equality and prevent UI lag.
