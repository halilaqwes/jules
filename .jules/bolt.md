## 2025-05-10 - [Database Connection Pooling]
**Learning:** SQLite backend operations on the `event_log` in `MemoryService` are currently unpooled. Each call to `log_event` opens and closes a new database connection. Testing shows that pooling connections drops execution time for 100 log events from ~0.2086s to ~0.0017s.
**Action:** Use a pooled connection approach or preserve the connection in `MemoryService` to avoid overhead on frequent events, avoiding re-opening the db file constantly, but we need to ensure thread safety (fastapi + multiple background agents).

## 2025-05-10 - [Frontend Refresh Polling]
**Learning:** `FileExplorer` uses `setInterval(fetchTree, 5000)` which creates excessive and potentially overlapping API calls if tree fetching is slow, leading to re-renders even if the files haven't changed.
**Action:** Avoid blind polling. Could use a manual refresh button, debouncing, or websocket events to update file structures when they change, instead of polling.
