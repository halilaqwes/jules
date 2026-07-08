
## 2023-10-24 - [Fix React Re-rendering Bottleneck in MainLayout]
**Learning:** Lifting state (such as code editor text) to a central layout component causes all its sibling components to re-render on every state update (e.g., keystroke). In our `MainLayout`, typing in the Code Editor triggered updates that cascaded to heavy components like `AgentSidebar` and `ChatPanel`, resulting in severe layout thrashing.
**Action:** When lifting frequently changing state to a parent component, always use `useCallback` for event handlers and wrap the heavy sibling components in `React.memo` or `useMemo` so that they only re-render when their specific props change.
