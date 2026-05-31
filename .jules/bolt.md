## 2026-05-31 - [Prevent Layout Thrashing on Keystroke]
**Learning:** React component tracking `CodeEditor` keystrokes in a central layout component (`MainLayout`) causes severe layout thrashing and unnecessary reconciliation, dragging down performance when heavy sibling components (like the sidebar, file explorer, and chat panel) re-render simultaneously on every key press.
**Action:** Lift state properly using `useCallback` on handlers and wrapping sibling components in `React.memo` to decouple their render cycle from the fast-updating editor.
