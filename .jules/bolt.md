## 2025-06-04 - [React Render Optimization in MainLayout]
**Learning:** Lifting state (like keystrokes in a CodeEditor) up to a centralized layout component causes severe layout thrashing and unoptimized re-renders across all sibling components if they aren't properly memoized.
**Action:** When centralizing frequent state updates (e.g. typing) in a parent layout, always wrap heavy sibling components (like sidebars and chat panels) with `React.memo` and use `useCallback` for any inline functions passed as props to avoid breaking the memoization.
