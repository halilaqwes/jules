## 2025-05-11 - [MainLayout Optimization]
**Learning:** React state lifted up to a layout component (e.g. `code` state mapped to every keystroke in a code editor) causes severe layout trashing and unneeded React reconciliation across sibling components that don't depend on the state.
**Action:** Use `useMemo` for sibling components (like sidebars and chat panels) and `useCallback` for functions passed as props to prevent heavy re-renders when parent state updates rapidly.
