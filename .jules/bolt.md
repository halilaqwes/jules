
## 2024-05-18 - React.memo and useCallback for Centralized State Management
**Learning:** Lifting state to a central layout component (like `MainLayout` tracking `CodeEditor` keystrokes) causes every state update (e.g., typing in the editor) to trigger a re-render of the layout component and all its children. This leads to severe layout thrashing and unnecessary reconciliation, especially for heavy sibling components like `AgentSidebar` and `FileExplorer`.
**Action:** When implementing centralized state management, heavy sibling components must be memoized using `React.memo` and the callback functions passed to them must be memoized using `useCallback` to prevent these unnecessary re-renders.
