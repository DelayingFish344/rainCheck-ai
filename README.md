# RainCheck AI — TideTech Innovators

A functional prototype of an AI-assisted early-stage stormwater design explorer. **Not a final drainage design tool.**

## Run on Windows

1. Install Python 3.11+ from https://www.python.org/downloads/ (check "Add Python to PATH" if offered).
2. Extract the ZIP. Open Windows Terminal or PowerShell in the `raincheck_ai` folder.
3. Run `py -m pip install -r requirements.txt`.
4. Run `py -m streamlit run app.py`.
5. Open the localhost address shown (typically http://localhost:8501).

You can instead put these files in a GitHub repository and deploy with Streamlit Community Cloud at https://share.streamlit.io/. Main file: `app.py`. This requires a GitHub account and compatible dependency versions.

## What is real vs illustrative?

- **Engineering calculation:** NRCS Curve Number event runoff depth, Q=(P-0.2S)^2/(P+0.8S), for P>0.2S and S=1000/CN-10. CN is an assumed weighted composite of impervious (98) and pervious good-condition open space (A=39, B=61, C=74, D=80). This is a screening model, not a drainage design.
- **AI:** A Random Forest trained on 2,600 synthetically generated inputs and formula-generated labels; evaluated on a held-out 20% test split. The ML approximates the engineering calculation. It does **not** demonstrate independent predictive skill against field observations or outperform the equation.
- **Design alternatives:** Converting 5–30 percentage points of total site area from paving to landscaped pervious cover. This is a hypothetical pre-construction site-layout comparison; not a rain garden, detention, or permeable pavement performance model.
- **Costs:** $90,000 per acre converted, purely illustrative, not a market/contractor estimate. Replace before real use.
- **No flood claims:** This model does not predict ponding/flooding, peak discharge, time of concentration, drainage capacity, or code compliance.

## Suggested judge demo

1. Start with P=3 in, area=5 acres, HSG B, 65% impervious.
2. Change impervious area from 65% to 85% and explain the change to runoff.
3. Set a $50,000 budget. Show which land-cover conversions fit and explain the constraints.
4. Show direct engineering calculation vs the Random Forest surrogate and the held-out error; make clear that synthetic validation is not real-world validation.
5. Explain future work: field data, calibrated SWMM, life-cycle cost and site-layout constraints.

## Originality and credit

The application code is a new educational prototype built for RainCheck AI with AI-assisted programming. NRCS Curve Number is established engineering science; Random Forest and Streamlit are third-party technologies. Verify any event rules on the use of AI coding assistants, and accurately disclose methods and contributor roles.
