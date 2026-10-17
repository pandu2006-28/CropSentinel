# System architecture

## Context
CropSentinel is proposed as a trust-aware crop disease early-warning prototype for tomato leaves. The design goal is to avoid issuing a high-confidence alert when evidence quality or model certainty is insufficient.

## Functional pipeline
1. **Acquire:** capture an image and timestamp.
2. **Quality gate:** compute blur, exposure, leaf visibility/occlusion and framing metrics.
3. **Inference:** run the selected compact model and obtain class scores.
4. **Reliability policy:** compare quality, top score and top-two margin against calibrated thresholds; optionally incorporate repeated observations and environmental context only after an evaluated rule is defined.
5. **Decision:** recapture, send to human review, emit possible-disease alert, or record the model's healthy-class prediction with a no-guarantee disclaimer.
6. **Communicate:** use a compatible direct LoRa link to send an alert packet.
7. **Receive and persist:** receiver stores events, presents the alert, and supports user acknowledgement.

## Reliability rules
- Poor-quality image → request another observation.
- Missing/invalid model output → no disease decision; record a fault or request review.
- Low confidence or small class margin → defer to human review.
- High-confidence non-healthy class → possible-disease alert only.
- High-confidence healthy class → state only that the model predicted the healthy class, not that the plant is proven healthy.
- Link failure → retry/persist pending message; absence of a message is not evidence of crop health.
- Acknowledgement means a user interacted with an alert; it does not prove plant inspection.

## Diagram

See `system_architecture.mmd` and `system_architecture.svg`. They are conceptual representations, not wiring schematics or completed CAD.

## Implementation status
The repository contains a Python reference policy and an ESP32 serial-startup scaffold. Sensor, camera, edge inference, LoRa transport, hardware CAD and end-to-end behaviour are not yet implemented/tested in this scaffold.
