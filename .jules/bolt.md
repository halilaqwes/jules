
## 2024-05-18 - [Central Layout Keystroke Thrashing]
**Learning:** Tracking `CodeEditor` keystrokes in a central layout component (`MainLayout`) that also renders heavy sibling components (like `AgentSidebar`, `FileExplorer`, and `ChatPanel`) causes severe layout thrashing because every keystroke triggers a re-render of the entire layout and all its children.
**Action:** Always memoize heavy sibling components using `React.memo()` and use `useCallback()` for functions passed to them if lifting state up to a parent component that updates frequently (like on every keystroke).
