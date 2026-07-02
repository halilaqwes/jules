## 2026-07-02 - [Prevent Re-renders in MainLayout]
**Learning:** In the frontend React application, lifting state up to a central layout component (like tracking CodeEditor keystrokes in MainLayout) requires heavy sibling components to be memoized using React.memo or useMemo, and callbacks using useCallback to prevent severe layout thrashing and unnecessary reconciliation.
**Action:** Always wrap sibling components of frequently updated state in React.memo() and use useCallback() for handler functions passed to them in this monorepo layout architecture.
