"""RainCheck AI v0.3: preliminary sustainable site design, not final drainage design."""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from engineering import composite_cn, runoff_depth_in, runoff_volume_ft3, compare_options
from model import features, fit_model

st.set_page_config(page_title='RainCheck AI | Sustainable Site Studio',page_icon='🌧️',layout='wide')
st.markdown('''<style>
:root {color-scheme: light;}
.stApp {background:linear-gradient(160deg,#fff3f8 0%,#fffbfd 34%,#fff6fa 100%);color:#25212a}
.block-container{max-width:1190px;padding-top:1.6rem;padding-bottom:3rem}
[data-testid="stSidebar"]{background:#ffedf5;border-right:1px solid #f8bdd7}
[data-testid="stSidebar"] *{color:#542b46!important}
[data-testid="stMetric"]{background:#fff;border:1px solid #f5bad4;border-radius:20px;padding:16px;min-height:118px;box-shadow:0 7px 22px rgba(167,25,88,.07)}
[data-testid="stMetricLabel"] *,[data-testid="stMetricValue"] *{color:#61213f!important;opacity:1!important}
[data-testid="stMetricDelta"] *{color:#0a7584!important}
.stApp p,.stApp label,.stApp li,.stApp div[data-testid="stMarkdownContainer"]{color:#302332}
h1,h2,h3{color:#84214f!important;letter-spacing:-.025em}
.stButton button[kind="primary"], div[data-baseweb="slider"] [role="slider"]{background:#e72e83!important}
.hero{background:linear-gradient(115deg,#a71958,#e72e83 68%,#ff78b4);border-radius:24px;padding:28px 30px;margin:6px 0 24px;color:#fff;box-shadow:0 14px 38px rgba(167,25,88,.17)}
.hero h1{color:#fff!important;font-size:2.6rem;margin:0;letter-spacing:-.04em}
.hero p,.hero small{color:#fff!important;line-height:1.55}
.hero-decoration{font-size:1.6rem;letter-spacing:.22rem;float:right}
.pill{display:inline-block;background:#ffe0ed;color:#95164c;border:1px solid #f4b4d0;border-radius:30px;padding:7px 15px;font-weight:800;font-size:.76rem}
.note{border-left:5px solid #e72e83;background:#ffeaf3;border-radius:12px;padding:14px 18px;color:#542b46}
.numeral{font-size:.83rem;color:#bd3274;font-weight:800;letter-spacing:.09em}
[data-testid="stDataFrame"]{border-radius:12px;overflow:hidden}
[data-testid="stExpander"]{background:#fff;border:1px solid #f1c3d6;border-radius:14px}
</style>''',unsafe_allow_html=True)
st.markdown('<div class="pill">TIDETECH INNOVATORS · NSBE FRC 2026 · PINK & BERRY · V0.3</div>',unsafe_allow_html=True)
st.markdown('<div class="hero"><span class="hero-decoration">☁️ 💧 ✨</span><h1>🌧️ RainCheck AI</h1><p><b>Design smarter. Build greener.</b></p><small>The next-gen stormwater design studio. Explore your site, see what changes, and compare early-stage planning alternatives with transparent engineering checks.</small></div>',unsafe_allow_html=True)
@st.cache_resource(show_spinner='Preparing the illustrative machine-learning model...')
def get_ai(): return fit_model()

with st.sidebar:
    st.header('📍 Your proposed site')
    rain=st.slider('Rainfall event depth (in)',.1,8.,3.,.1)
    area=st.slider('Site drainage area (acres)',.5,20.,5.,.5)
    imperv=st.slider('Planned impervious surface (%)',5,95,65,5)
    soil=st.selectbox('Hydrologic soil group',['A','B','C','D'],index=1)
    st.divider()
    st.header('🌿 Explore design options')
    budget=st.slider('Illustrative budget ($)',0,300000,50000,5000)
    max_convert=st.slider('Maximum land-cover conversion (percentage points)',0,30,20,5,help='Planning constraint to protect necessary pavement and site access. Must be confirmed by designer.')
    unit_cost=st.number_input('Illustrative conversion cost ($/acre)',min_value=10000,max_value=500000,value=90000,step=5000)
    st.caption('Cost is a demonstration assumption—not a contractor quote. All input sites are hypothetical unless independently documented.')

cn=composite_cn(imperv,soil)
q=runoff_depth_in(rain,cn)
volume=runoff_volume_ft3(rain,area,imperv,soil)
model,metrics=get_ai()
ai_q=max(0,float(model.predict([features(rain,imperv,soil)])[0]))
ai_vol=ai_q/12*area*43560

st.markdown('''<div style="display:flex;align-items:center;justify-content:space-between;gap:8px;flex-wrap:wrap;margin:0 0 20px;padding:12px 16px;background:#fff;border:1px solid #f5c4d8;border-radius:16px">
 <span style="color:#862556;font-weight:700">☁️ Rainfall</span><span style="color:#b14c7e">→</span>
 <span style="color:#862556;font-weight:700">🏙️ Site surfaces</span><span style="color:#b14c7e">→</span>
 <span style="color:#0e8290;font-weight:700">💧 Runoff</span><span style="color:#b14c7e">→</span>
 <span style="color:#862556;font-weight:700">🌸 Better design choices</span>
</div>''',unsafe_allow_html=True)
st.markdown('<div class="numeral">01 / BASELINE SITE</div>',unsafe_allow_html=True)
st.subheader('What does the proposed site generate?')
a,b,c=st.columns(3)
a.metric('Composite Curve Number',f'{cn:.1f}')
b.metric('Event runoff depth',f'{q:.2f} in')
c.metric('Event runoff volume',f'{volume:,.0f} ft³')
st.markdown('<div class="note"><strong>What this means:</strong> Conceptual NRCS Curve Number direct runoff for one rainfall event. This is not a flood-risk score, drainage-capacity test, peak-discharge calculation, or final stormwater design.</div>',unsafe_allow_html=True)

st.markdown('<div class="numeral" style="margin-top:24px">02 / DESIGN STUDIO</div>',unsafe_allow_html=True)
st.subheader('What if we build with less hardscape?')
st.write('Test whether a <strong>feasible reduction in planned paved area</strong> could lower calculated event runoff. This screening does not assume paved areas can always be removed.',unsafe_allow_html=True)
rows=compare_options(rain,area,imperv,soil,budget)
df=pd.DataFrame(rows)
df['Illustrative cost ($)']=df['Area changed (acres)']*unit_cost
df['Within budget']=df['Illustrative cost ($)']<=budget
df['Within site constraint']=df['Change (percentage points)']<=max_convert
df['Feasible for screening']=df['Within budget'] & df['Within site constraint']
feasible=df[(df['Feasible for screening']) & (df['Change (percentage points)']>0)]
if len(feasible):
    best=feasible.sort_values(['Runoff reduction (ft³)','Illustrative cost ($)'],ascending=[False,True]).iloc[0]
    c1,c2,c3=st.columns(3)
    c1.metric('Recommended concept',f"{int(best['Change (percentage points)'])} pp less paving")
    c2.metric('Runoff saved (modeled)',f"{best['Runoff reduction (ft³)']:,.0f} ft³",f"{best['Runoff reduction (%)']:.1f}% less")
    c3.metric('Illustrative cost',f"${best['Illustrative cost ($)']:,.0f}")
    st.caption('Recommendation = largest directly calculated reduction among options that pass the entered budget and land-cover constraints; not an AI-generated final design.')
else:
    st.warning('No land-cover conversion option fits both the chosen budget and planning constraint. Retain the baseline and investigate other practices separately.')

plot=df.copy()
plot['Category']=plot.apply(lambda r:'Feasible for screening' if r['Feasible for screening'] else 'Excluded by constraint',axis=1)
fig=go.Figure()
for cat,col in [('Feasible for screening','#e72e83'),('Excluded by constraint','#b8a5b0')]:
    subset=plot[plot['Category']==cat]
    fig.add_trace(go.Bar(x=subset['Change (percentage points)'],y=subset['Runoff reduction (ft³)'],name=cat,marker_color=col,text=[f'{v:,.0f}' for v in subset['Runoff reduction (ft³)']],textposition='outside'))
fig.update_layout(title='Modeled event runoff avoided by paved-area reduction',xaxis_title='Percentage points of site converted to pervious cover',yaxis_title='Runoff avoided (ft³)',barmode='overlay',plot_bgcolor='#fff',paper_bgcolor='#fff',font_color='#542b46',height=370,margin=dict(t=65,b=70,l=45,r=20),legend_orientation='h',legend_y=-.3)
st.plotly_chart(fig,use_container_width=True)
with st.expander('Scenario comparison table + feasibility flags'):
    st.dataframe(df[['Design scenario','Proposed impervious (%)','Area changed (acres)','Illustrative cost ($)','Runoff volume (ft³)','Runoff reduction (ft³)','Within budget','Within site constraint']],hide_index=True,use_container_width=True)
    st.caption('The site constraint is an engineer-entered simplification; it does not establish real ADA, parking, utility, grading, fire access, or local code feasibility.')

st.markdown('<div class="numeral" style="margin-top:24px">03 / AI TRANSPARENCY</div>',unsafe_allow_html=True)
st.subheader('Where does machine learning fit?')
c1,c2,c3=st.columns(3)
c1.metric('ML estimated runoff',f'{ai_vol:,.0f} ft³')
c2.metric('Equation-based runoff',f'{volume:,.0f} ft³')
c3.metric('ML estimation error here',f'{abs(ai_vol-volume)/max(volume,1)*100:.1f}%')
st.write('A **Random Forest regression model** was trained on independently generated, synthetic NRCS-based scenarios to approximate **runoff depth**, which is converted to volume for this site. We compare its output against the direct equation rather than trusting the AI blindly.')
with st.expander('See validation, input factors and limitations',expanded=True):
    st.write(f"**Held-out evaluation:** {metrics['train_size']:,} training scenarios; {metrics['test_size']:,} test scenarios. **MAE:** {metrics['mae_in']:.3f} in runoff depth. **R²:** {metrics['r2']:.3f}.")
    imp=pd.DataFrame({'Input':['Rainfall depth','Impervious cover','Soil group'],'Model importance':model.feature_importances_})
    fig2=go.Figure(go.Bar(x=imp['Model importance'],y=imp['Input'],orientation='h',marker_color='#e72e83'))
    fig2.update_layout(height=240,margin=dict(t=15,b=30,l=15,r=20),paper_bgcolor='#fff',plot_bgcolor='#fff',font_color='#542b46',yaxis={'autorange':'reversed'})
    st.plotly_chart(fig2,use_container_width=True)
    st.warning('Model is trained and tested only on simulated outputs of the same engineering method; the score is NOT evidence of predictive performance on observed sites. A direct equation remains preferable where applicable. Soil-group numeric encoding is a simplification. Real observations and independent hydraulic modeling are needed for an operational AI model.')

st.markdown('<div class="numeral" style="margin-top:24px">04 / THE ENGINEERING DECISION</div>',unsafe_allow_html=True)
st.subheader('What should an engineer do next?')
st.markdown('''**RainCheck supports an early go/no-go conversation:**

- **Consider:** Does reducing impervious cover preserve required parking, accessible routes, fire access, utilities and site function?
- **Verify:** Site soil survey, actual subcatchment boundaries, rainfall design standards, groundwater, downstream discharge, and local stormwater permit requirements.
- **Explore separately:** Bioretention, permeable pavement, detention, and rainwater harvesting need their own sizing, infiltration/storage and maintenance analyses; RainCheck **does not** quantify their performance here.
- **Escalate:** Complete hydrologic/hydraulic design in appropriate engineering tools before approvals, permitting or construction.
''')
st.divider()
st.caption('RainCheck AI v0.3 • Independent educational prototype for the 2026 NSBE FRC AI Impact-a-thon • Synthetic data and illustrative costs • Not professional design advice')
