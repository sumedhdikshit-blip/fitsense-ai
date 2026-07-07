# Engineering Tradeoffs & Design Decisions

This document summarizes the architectural tradeoffs and technical decisions made during the development of FitSense AI.

---

### 1. Single-User / Simple Multi-User Auth
We chose a stateful cookie-based session scheme over a robust multi-tenant enterprise system to keep database management overhead low and the focus centered on core fitness logging. A full tenant-isolation layer (e.g. database schema-per-user or complex token signing) was skipped in favor of a clean, lightweight session mapping to keep the codebase simple and maintainable.

### 2. SQLite over PostgreSQL
SQLite was selected as the database engine because it is self-contained, serverless, and requires zero configuration. It allows the entire database state to reside in a single portable file (`fitsense.db`), which dramatically simplifies developer onboarding and testing compared to maintaining a running PostgreSQL container. For local-first fitness data tracking, SQLite's performance is more than sufficient.

### 3. Rule-Based Joint-Angle Logic vs. Machine Learning for Form Checking
Instead of training deep learning classification models to evaluate exercise form, we built form validation on deterministic joint-angle constraints computed via MediaPipe coordinates (e.g., matching elbow/shoulder angles against config thresholds). This rule-based approach provides immediate, explainable feedback (e.g., showing vertex angles like `90deg` directly on the screen) without the need for large, manually labeled video datasets or high-inference training pipelines.

### 4. Labeling the Chronic Disease Risk Model "Experimental"
During model training on the synthetic lifestyle dataset, features showed negligible target correlation (max $|r| = 0.03$). To remain technically honest and clinically responsible, we labeled this feature as "Experimental" and injected a clear disclaimer on both the API and UI. Presenting a model with near-zero input-to-label correlation as a diagnostic medical utility would be highly misleading.

### 5. Reactive Optimization (Thread Pool, Indexes) vs. Upfront Design
We chose to implement WebSocket thread pool offloading and database indexing reactively using diagnostic profiling (`cProfile`, execution time tracking) rather than upfront. This avoided premature optimization. By writing the core loop first, we could measure where the actual event-loop blocking occurred (MediaPipe and frame drawing) and apply specific concurrency mitigations where they yielded the highest return on investment.
