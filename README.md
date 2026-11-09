# RainCheck AI v0.2 — Sustainable Site Design Studio

**TideTech Innovators | NSBE FRC 2026 | Educational prototype**

An interactive **preliminary stormwater site design** app that compares how changing planned impervious cover affects NRCS Curve Number event runoff. It adds a trained Random Forest surrogate, independent direct-equation checks, budget/footprint constraints, and explanatory decision notes. It **does not** predict actual campus flooding, compute pipe capacities, size stormwater controls, or replace licensed engineering design.

## Run or deploy

For free Streamlit Community Cloud, upload **all the following files to your existing `raincheck-ai` GitHub repository root** (overwrite old files) and let the already deployed app update: `app.py`, `engineering.py`, `model.py`, `requirements.txt`, `README.md`, `test_engineering.py`, `test_model.py`. The main Streamlit file is **`app.py`**.

To run locally on Windows:
```
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Tests:
```
python test_engineering.py
python test_model.py
```

## What it actually does

1. Calculates composite runoff Curve Number assuming directly connected impervious cover CN=98, and pervious open space in good condition with CN by hydrologic group A=39, B=61, C=74, D=80.
2. Applies NRCS runoff depth with initial abstraction `Ia=0.2S`, and converts depth to event runoff volume.
3. Compares reducing proposed paving by 5–30 percentage points, constrained by available pavement, a **user-entered maximum conversion**, and an **illustrative** per-acre cost and budget.
4. Recommends the **largest equation-calculated runoff reduction** among allowed conversion scenarios. This deterministic constraint-based choice is not misrepresented as AI.
5. Trains a Random Forest on synthetic engineering examples to approximate runoff depth; evaluates held-out test MAE and R². Compares ML prediction with the direct equation for transparency. The ML is **a proof of concept**, not demonstrated additional value over the direct method or observed-field accuracy.

## Engineering limitations

- Only **one storm event** is modeled. Composite CN assumptions simplify hydraulically separate surfaces and soil variability.
- No infiltration testing, routing, peak flows, flooding probability, inlets, storage, rain-garden sizing, water quality, time of concentration or detailed site planning.
- Unit-cost assumption is invented for demonstration and should not be used to estimate real projects.
- Replacing pavement with good-condition pervious open space is a design exploration, not a claim about BMP removal efficiency.
- For actual design, compare to local stormwater rules, field observations and detailed hydrologic/hydraulic software such as EPA SWMM.

## Judges' demonstration

Set rainfall 3 in, site 5 acres, impervious 65%, soil B and budget $50,000. Show baseline runoff. Lower impervious coverage to 45% and show change. Return to 65%; increase budget and site conversion ceiling to show choices being screened. Open the AI validation section; distinguish surrogate modeling from exact equation and field measurements. Finish with needed real-world data.


## v0.3 theme
Pink & berry UI update, new banner and explanatory visual, high contrast labels and chart accents. Engineering, model, and recommendation logic is unchanged from v0.2.
