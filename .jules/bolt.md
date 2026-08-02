
## 2024-05-18 - [Preventing Layout Thrashing in React with Lifted State]
**Learning:** In the frontend React application, lifting state up to a central layout component (like tracking `CodeEditor` keystrokes in `MainLayout`) requires heavy sibling components to be memoized using `React.memo` or `useMemo`, and callbacks using `useCallback`. Without this, every keystroke in the editor causes a re-render of the entire layout including the sidebar, file explorer, and chat panel, leading to severe layout thrashing and unnecessary reconciliation.
**Action:** When implementing lifted state in React that updates frequently (e.g., text input), always wrap expensive sibling components with `React.memo` and ensure that all callbacks passed as props to them are memoized with `useCallback`.
