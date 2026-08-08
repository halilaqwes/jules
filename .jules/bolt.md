
## 2026-08-08 - [Memoize sibling components]
**Learning:** Lifting state up to a central layout component (like tracking `CodeEditor` keystrokes in `MainLayout`) requires heavy sibling components to be memoized using `React.memo` or `useMemo`, and callbacks using `useCallback` to prevent severe layout thrashing and unnecessary reconciliation.
**Action:** Use `React.memo` and `useCallback` to wrap heavy sibling components and inline functions when lifting state up to a parent component.
