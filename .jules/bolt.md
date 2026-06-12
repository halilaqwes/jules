## 2024-06-12 - Prevented full app re-renders on CodeEditor keystrokes
**Learning:** In a React app where central state (like `code` content) is lifted to a parent layout (like `MainLayout`) to be shared, every update to that state (e.g., from an editor typing event) triggers a re-render of all sibling components unless they are memoized.
**Action:** When a parent layout holds rapidly updating state, use `React.memo` on expensive sibling components and `useCallback` on handlers passed to child components to isolate re-renders strictly to the component that needs them.
