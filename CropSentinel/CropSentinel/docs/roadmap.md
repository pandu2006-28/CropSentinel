# Proposed roadmap (planning only)

| Phase | Work | Exit evidence |
|---|---|---|
| 1. Requirements/procurement | Confirm exact board/radio SKUs, power budget, radio band, camera and battery safety | Approved BOM with dated links; reviewed architecture and pin map |
| 2. Bench bring-up | Test MCU, camera, sensor and radio individually | Serial logs, sensor readings, camera samples and radio test |
| 3. AI baseline | Source licensed/traceable images; train and evaluate baseline | Dataset card, split manifest, per-class metrics and confusion matrix |
| 4. Trust layer | Add image-quality gate and confidence/margin policy | Unit tests and failure-case results |
| 5. Receiver/resilience | Event IDs, persistent queue, ACK states and retry/backoff | Restart recovery and packet-loss results |
| 6. Integration/reporting | Measure current, range under stated conditions, latency and failures | Reproducible report, genuine photos, limitations and final docs |

Do not convert roadmap targets into completed results. Record actual hardware versions, test conditions, failed tests and limitations.
