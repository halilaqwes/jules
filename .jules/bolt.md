## 2024-05-25 - React Layout Thrashing from Editor Keystrokes
**Learning:** Tracking `CodeEditor` keystrokes (using `useState` for file content) at the `MainLayout` level causes severe layout thrashing because heavy sibling components like `FileExplorer`, `ChatPanel`, and `AgentSidebar` re-render on every single keystroke.
**Action:** Use `React.memo` to wrap heavy sibling components and `useCallback` for callbacks passed to them to prevent unnecessary re-renders when parent state changes rapidly.
