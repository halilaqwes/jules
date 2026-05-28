1. **Optimize MainLayout state updates:** Modify `MainLayout.tsx` to define `handleFileSelect` and `handleCodeChange` using `useCallback` instead of inline functions to preserve prop references.
2. **Memoize heavy sibling components:** Wrap `AgentSidebar`, `FileExplorer`, and `ChatPanel` components in `React.memo()` to prevent them from re-rendering on every keystroke in the `CodeEditor`.
3. **Verify and Pre-commit:** Verify the code compiles and passes linter, completing pre-commit steps.
4. **Submit Change:** Create PR with performance optimization details and journal critical learnings in `.jules/bolt.md`.
