## 2024-05-15 - React Component Re-render Optimization
**Learning:** In a frontend React application, lifting state up to a central layout component (like tracking `CodeEditor` keystrokes in `MainLayout`) causes re-renders for the entire layout and all its children. This creates severe layout thrashing and unnecessary reconciliation for heavy sibling components.
**Action:** When lifting state to a central component, always memoize heavy sibling components using `React.memo` and wrap the functions passed down to them using `useCallback` so their references remain stable across re-renders.
