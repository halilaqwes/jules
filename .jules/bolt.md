
## 2024-05-24 - [React Layout Thrashing with Keystrokes]
**Learning:** In the frontend React application, lifting state up to a central layout component (like tracking `CodeEditor` keystrokes via `onChange` in `MainLayout`) causes severe layout thrashing and unnecessary reconciliation across heavy sibling components (like `AgentSidebar`, `ChatPanel`, and `FileExplorer`). Every keystroke triggers a render of the entire layout.
**Action:** When centralizing frequent state updates (like keystrokes or mouse movements), always use `React.memo` on sibling components and wrap callbacks passed as props in `useCallback` to maintain reference stability and prevent full-tree re-renders.
