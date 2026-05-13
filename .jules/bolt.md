## 2026-05-13 - Prevent layout thrashing on keystrokes in MainLayout
**Learning:** Lifting state up to a central layout component (like tracking `CodeEditor` keystrokes in `MainLayout`) causes severe layout thrashing and unnecessary reconciliation for heavy sibling components (like FileExplorer, AgentSidebar, ChatPanel).
**Action:** Use `useMemo` for rendering heavy sibling components and `useCallback` for event handlers passed to them, ensuring they don't re-render on every keystroke in the editor.
