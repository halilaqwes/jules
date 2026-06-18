## 2024-06-18 - React Layout Thrashing from Editor State

**Learning:** In a dashboard layout where a code editor's typing state is lifted up to the `MainLayout` parent component, every single keystroke triggers a full reconciliation of heavy sibling components (like sidebars and chat panels), causing massive layout thrashing and input lag.

**Action:** Wrap heavy UI sections with `useMemo` (or wrap their functional definitions with `React.memo()`) and bind their props with `useCallback` when lifting high-frequency state like typing input up to a common parent.
