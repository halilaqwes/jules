
## 2024-08-09 - [Prevent layout thrashing in React with heavy sibling components]
**Learning:** Lifting state up to a central layout component (like tracking `CodeEditor` keystrokes in `MainLayout`) requires heavy sibling components to be memoized using `React.memo` or `useMemo`, and callbacks using `useCallback` to prevent severe layout thrashing and unnecessary reconciliation.
**Action:** When creating layouts with shared state that updates frequently (like editor keystrokes), always memoize child components (e.g. file trees, sidebars) and their prop handlers to isolate re-renders strictly to the updated component.
