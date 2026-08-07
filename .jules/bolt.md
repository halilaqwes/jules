## 2024-11-20 - Memoization for State Lifted to Layout Component
**Learning:** When lifting state up to a central layout component (like tracking CodeEditor keystrokes in `MainLayout`), it triggers a re-render of the entire layout tree on every keystroke. This causes severe layout thrashing because heavy sibling components (like `AgentSidebar`, `FileExplorer`, and `ChatPanel`) are needlessly re-rendered.
**Action:** Always wrap heavy sibling components in `React.memo` and pass stable function references using `useCallback` when centralizing high-frequency state updates like keystrokes.
