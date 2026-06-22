
## 2026-06-22 - [React Layout Re-render Optimization]
**Learning:** In the frontend React application, lifting state up to a central layout component (like tracking `CodeEditor` keystrokes in `MainLayout`) requires heavy sibling components to be memoized using `React.memo` or `useMemo`, and callbacks using `useCallback` to prevent severe layout thrashing and unnecessary reconciliation.
**Action:** When holding rapidly changing state at a high level (like text input), always wrap complex sibling components in `React.memo()` and pass stable callbacks with `useCallback` to isolate re-renders strictly to the component utilizing the state.
