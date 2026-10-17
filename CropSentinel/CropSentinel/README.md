# CropSentinel 🌱
### Trust-Aware Edge AI for Reliable Early Crop Disease Warning

**Repository:** https://github.com/pandu2006-28/CropSentinel  
**Award application ID:** VK26-AU-PAI-0084  
**Project stage:** Concept and software-reference scaffold; the complete hardware prototype and AI model are not yet validated.

> CropSentinel aims to check whether evidence is reliable before issuing a possible crop-disease alert. Poor-quality images or uncertain predictions should trigger re-observation or human review—not an overconfident diagnosis.

## Problem

Plant disease classifiers can perform differently across controlled datasets and real fields due to lighting, blur, occlusion, camera angle, backgrounds, and crop variability. CropSentinel proposes combining image-quality checks with model confidence and class separation before deciding whether to alert.

## Initial scope

- Crop: tomato
- Intended initial classes: healthy, early blight, late blight
- Proposed device: camera-capable ESP32-S3-class board
- Proposed environmental context sensor: BME280-class temperature/humidity module
- Proposed communications: direct point-to-point LoRa; exact radio and regulatory band to be verified
- Proposed farmer receiver: compatible radio/controller, display, buzzer/LED and acknowledgement button
- Planned power: solar-assisted rechargeable battery; final sizing depends on measured consumption

## Current decision-logic scaffold

The Python reference logic in `src/cropsentinel/` demonstrates the intended policy:
1. Check provided image-quality metrics.
2. Request recapture when the quality gate fails.
3. Defer to human review when the top confidence or top-class margin is below illustrative thresholds.
4. Use “possible disease” for a non-healthy prediction, not a confirmed diagnosis.
5. Treat a healthy-class output as a model prediction, not proof the plant is disease-free.

The thresholds are examples only and must be calibrated on representative labeled field data. This is not a trained classifier and does not process real camera images.

## Architecture and documents

- `docs/architecture.md` — proposed system workflow
- `docs/system_architecture.svg` and `.mmd` — conceptual diagrams, not a wiring schematic or proof of a completed device
- `docs/CropSentinel_Preliminary_BOM.xlsx` and `docs/preliminary_bom.csv` — ₹50,000 preliminary budget
- `docs/budget_summary.md` — budget breakdown and procurement caveats
- `docs/safety_and_risks.md` — preliminary safety/risk register
- `docs/roadmap.md` — proposed work plan
- `docs/test_plan.csv` — planned validation cases
- `docs/STATUS.md` — honest implementation status
- `docs/references.md` — background sources
- `docs/IMAGE_AND_EVIDENCE_GUIDE.md` — guidance for adding authentic evidence

## Budget

**Planning ceiling: ₹50,000.** It includes a proposed field node, receiver, development accessories, testing allowances, replacement spares, logistics and emergency contingency. Figures are estimates/allowances, not verified supplier quotations. Verify exact part compatibility, current supplier prices, availability, taxes and shipping before procurement.

## Run tests

Requires Python 3.10 or newer.

```bash
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# macOS/Linux:
# source .venv/bin/activate

python -m pip install -e ".[dev]"
python -m pytest
python scripts/run_demo.py
```

The demo uses synthetic scores, not a model prediction or field observation.

## Limitations and safety

- A model prediction is not a definitive diagnosis.
- Do not create pesticide/dose recommendations from a class label alone; verify current, crop-specific authoritative guidance and product-label requirements.
- No autonomous spraying is in scope.
- A missing radio message does not mean a crop is healthy.
- A user acknowledgement does not prove plant inspection.
- Do not report accuracy, battery life, radio range, field outcomes, savings, CAD/FEA results, or prototype completion without reproducible evidence.
- Never commit passwords, API keys, Wi-Fi credentials or private farmer data.

## Development status

| Area | Current status |
|---|---|
| Project documentation and conceptual architecture | Included |
| ₹50,000 preliminary BOM | Included; supplier quotes pending |
| Python decision logic | Reference implementation included |
| Unit tests | Included for the reference logic |
| Camera, BME280, trained model and edge inference | Not implemented here |
| LoRa device-to-receiver integration | Not implemented here |
| Native schematic/CAD/FEA and physical build evidence | Not included here |
| End-to-end hardware and field validation | Not performed |

Only update status when code, native design files, tests or measured evidence support the change.
