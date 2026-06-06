## 2024-05-18 - [React.memo and useCallback Optimization]
**Learning:** In the frontend React application, lifting state up to a central layout component (like tracking `CodeEditor` keystrokes in `MainLayout`) requires heavy sibling components to be memoized using `React.memo` or `useMemo`, and callbacks using `useCallback` to prevent severe layout thrashing and unnecessary reconciliation.
**Action:** Always memoize sibling components and callbacks when state is lifted to a common ancestor, especially for frequent updates like text editor keystrokes.
