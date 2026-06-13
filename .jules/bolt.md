## 2023-10-27 - Prevent layout thrashing on code editor keystrokes
**Learning:** Lifting state up to a central layout component (like tracking CodeEditor keystrokes in MainLayout) causes severe layout thrashing and unnecessary reconciliation of heavy sibling components (AgentSidebar, FileExplorer, ChatPanel).
**Action:** Sibling components must be memoized using React.memo and callbacks passed to them must be wrapped in useCallback to prevent re-renders on every keystroke.
