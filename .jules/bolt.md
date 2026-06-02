## 2023-10-27 - Memoization for lifted state in MainLayout
**Learning:** In the AI OS React frontend, lifting the CodeEditor keystroke state (`code`) into `MainLayout` causes severe layout thrashing because it re-renders heavy sibling components (`AgentSidebar`, `ChatPanel`, `FileExplorer`) on every single keystroke.
**Action:** When lifting rapidly changing state (like keystrokes) up to a parent component, aggressively apply `React.memo` to all non-dependent sibling components and wrap their prop callbacks in `useCallback` to prevent cascading render cycles.
