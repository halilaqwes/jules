
## 2024-05-18 - [Optimized MainLayout Renders]
**Learning:** In the frontend React application, lifting state up to a central layout component (like tracking `CodeEditor` keystrokes in `MainLayout`) causes severe layout thrashing. Because `setCode` is called on every keystroke, the entire layout re-renders. If sibling components are heavy, the entire application becomes slow to type in.
**Action:** Always wrap heavy sibling components with `React.memo` and pass stable callbacks using `useCallback` when state is lifted to a parent component that updates frequently (e.g., text input or editor content).
