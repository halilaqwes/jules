
## 2024-06-26 - React Layout Thrashing with Centralized State
**Learning:** In the frontend React application, lifting state up to a central layout component (like tracking `CodeEditor` keystrokes in `MainLayout`) causes severe layout thrashing and unnecessary reconciliation on heavy sibling components (like ChatPanel, FileExplorer, AgentSidebar) due to continuous parent state updates.
**Action:** Always wrap heavy sibling components in `React.memo()` and use `useCallback` for functions passed as props from the central layout to prevent them from re-rendering during high-frequency centralized state updates.
