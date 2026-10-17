# Safety, failure modes and risk controls

This is a preliminary risk register, not a formal certification or completed FMEA.

| Risk | Consequence | Planned control | Evidence needed |
|---|---|---|---|
| Blurred, dark or occluded image | Incorrect classification | Image-quality gate; request recapture | Tests using degraded images |
| Confident but wrong field prediction | Misleading warning | Confidence/margin gate; human inspection; say “possible disease” | Held-out field-like evaluation and calibration report |
| Dataset leakage | Overstated performance | Group split by plant/session/source where feasible | Split manifest and reproducible metrics |
| Sensor failure/out-of-range value | Misleading context | Range checks, timeouts and health state | Fault-injection log |
| LoRa packet loss | Alert may not arrive | Event IDs, retry/backoff and persistent queue | Packet-loss test log |
| Receiver restarts | Pending alert lost | Persistent event storage and recovery test | Power-cycle test |
| Battery/power fault | Reset or equipment hazard | Compatible battery, charger, protection and fuse | Electrical review and measurements |
| Water/dust ingress | Device damage | Suitable enclosure, glands and condensation planning | Documented test; no unverified IP claim |
| No message mistaken for healthy crop | False reassurance | Explicit offline indicator; no-message ≠ healthy | Receiver/user journey test |
| Unsafe chemical advice | Crop/user/environmental harm | No unverified dosing; check crop-specific official guidance and current product label | Advisory review with authoritative sources |
| ACK mistaken for inspection | Overstated action | Separate packet receipt, user ACK and confirmed inspection states | State-transition tests |
| Private data/secrets committed | Privacy/security harm | Ignore secrets, minimize data, review diffs | Repository scan before public push |

## Safe wording
Use “possible disease detected” or “model predicted the early-blight class.” Do not claim confirmed diagnosis without qualified ground truth. Do not infer pesticide treatment or dose from a classifier score alone.
