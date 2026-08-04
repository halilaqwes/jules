
## 2026-08-04 - Prevent Layout Thrashing with Memoization
**Learning:** Lifting state (like CodeEditor keystrokes) to a central layout component causes severe re-renders of heavy sibling components (like AgentSidebar, FileExplorer, ChatPanel). This must be mitigated using `React.memo` and `useCallback`.
**Action:** Always memoize heavy sibling components and use `useCallback` for their props when state is lifted to a common parent.
