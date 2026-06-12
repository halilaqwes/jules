1. **Optimize MainLayout re-renders**:
   - Use `useCallback` for `onFileSelect` and `onChange` handlers in `MainLayout.tsx` to ensure stable references.
   - Wrap `AgentSidebar`, `FileExplorer`, `ChatPanel`, and `CodeEditor` in `React.memo` to prevent unnecessary re-renders when `MainLayout` state (like `code` during keystrokes) changes.
2. **Fix ESLint issues**:
   - Resolve `react-hooks/set-state-in-effect` in `FileExplorer.tsx` by wrapping the initial `fetchTree()` in `setTimeout(fetchTree, 0)`.
   - Resolve `Unexpected any` in `AgentSidebar.tsx` by defining an interface for `models`.
3. **Verify and submit**:
   - Run `npm run lint` and `npm run build` to ensure correctness.
   - Complete pre-commit steps to ensure proper testing, verification, review, and reflection are done.
   - Submit a PR with performance metrics documented.
