## 2024-05-18 - Prevent layout thrashing on CodeEditor keystrokes
**Learning:** In the frontend React application, lifting state up to a central layout component (like tracking `CodeEditor` keystrokes in `MainLayout`) requires heavy sibling components to be memoized using `useMemo` and callbacks using `useCallback` to prevent severe layout thrashing and unnecessary reconciliation on every keystroke.
**Action:** Always memoize heavy sibling components in a layout when state updates occur frequently (e.g., from typing in a text editor) in one of the child components.
