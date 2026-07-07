## 2026-07-07 - [Optimize MainLayout Re-renders]
**Learning:** Lifting high-frequency state like keystrokes (e.g. from CodeEditor) up to a central layout component (like MainLayout) causes severe layout thrashing and unnecessary reconciliation if heavy sibling components aren't memoized.
**Action:** When tracking high-frequency state at a high level in React, ensure that heavy sibling components are wrapped in `React.memo` or instantiated with `useMemo`, and pass them callbacks wrapped in `useCallback`.
