import streamlit as st
import pandas as pd
import plotly.express as px
from engineering import composite_cn, runoff_depth_in, runoff_volume_ft3, compare_options
from model import features, fit_model

st.set_page_config(page_title='RainCheck AI | Sustainable Site Studio', page_icon='🌧️', layout='wide')
st.markdown('''<style>
.stApp {background: linear-gradient(145deg,#f7faf6 0%,#f8f5fb 65%,#f5fafb 100%);color:#283c38;}
.block-container{padding-top:2.1rem;max-width:1250px}
[data-testid="stMetric"]{background:white;border:1px solid #e4ebe7;border-radius:18px;padding:17px;box-shadow:0 3px 20px #23362b0a}
[data-testid="stSidebar"]{background:#eef5f1}
h1,h2,h3{color:#294940!important}
.pill{display:inline-block;border-radius:30px;background:#e1efe7;padding:7px 13px;color:#36755b;font-size:0.85rem;font-weight:600}
.lead{font-size:1.13rem;color:#617a71;line-height:1.6}
.small-note{font-size:0.83rem;color:#65766c;line-height:1.55}
</style>''',unsafe_allow_html=True)
st.markdown('<span class="pill">TideTech Innovators · NSBE FRC 2026 · Prototype v0.1</span>',unsafe_allow_html=True)
st.title('🌧️ RainCheck AI')
st.markdown('<p class="lead">Design smarter. Build greener. Explore how early site-plan decisions may change stormwater runoff before construction.</p>',unsafe_allow_html=True)

@st.cache_resource(show_spinner='Training a synthetic-data AI model...')
def get_ai():
    return fit_model()

with st.sidebar:
    st.header('✏️ Your site')
    rain = st.slider('Design rainfall depth (inches)',0.1,8.0,3.0,0.1)
    area = st.slider('Drainage area (acres)',0.5,20.0,5.0,0.5)
    imperv = st.slider('Proposed impervious cover (%)',5,95,65,5)
    soil = st.selectbox('Hydrologic soil group', ['A','B','C','D'],index=1,
                       help='A generally has greater infiltration potential; D typically lower. Simplified assumptions.')
    budget = st.slider('Conceptual retrofit/revision budget ($)',0,300000,50000,5000)
    st.caption('Assumes directly connected impervious cover (CN=98); remaining area = good-condition open space. No routing, slopes, groundwater, storage, or hydraulic capacity is modeled.')

cn = composite_cn(imperv,soil)
q = runoff_depth_in(rain,cn)
volume = runoff_volume_ft3(rain,area,imperv,soil)
model,metrics = get_ai()
ai_volume = max(0,float(model.predict([features(rain,area,imperv,soil)])[0]))

st.subheader('01 / Understand the site')
a,b,c = st.columns(3)
a.metric('Composite curve number',f'{cn:.1f}')
b.metric('Estimated event runoff',f'{q:.2f} in')
c.metric('Estimated runoff volume',f'{volume:,.0f} ft³')
st.info('**Engineering interpretation:** This is a conceptual NRCS Curve Number runoff-volume estimate for one rainfall event—not a flood forecast, peak flow, drainage capacity calculation, or permit-ready design.')

st.subheader('02 / Explore sustainable design alternatives')
st.write('What if we reduce planned paved area **before construction** and replace it with landscaped pervious open space?')
rows=compare_options(rain,area,imperv,soil,budget)
df=pd.DataFrame(rows)
feasible=df[(df['Within budget']) & (df['Change (percentage points)']>0)]
best=feasible.sort_values('Runoff reduction (ft³)',ascending=False).head(1)
if not best.empty:
    item=best.iloc[0]
    st.success(f"**Largest modeled reduction within the example budget:** Convert {int(item['Change (percentage points)'])} percentage points of the site; estimated event runoff reduction **{item['Runoff reduction (ft³)']:,.0f} ft³** ({item['Runoff reduction (%)']:.1f}%).")
else:
    st.warning('No illustrated land-cover conversion fits the selected budget. Consider changing assumptions or reviewing other design options.')
chart_df=df[df['Change (percentage points)']>0].copy()
chart_df['Budget status']=chart_df['Within budget'].map({True:'Within budget',False:'Over budget'})
fig=px.bar(chart_df,x='Change (percentage points)',y='Runoff reduction (ft³)',color='Budget status',
           color_discrete_map={'Within budget':'#4c937b','Over budget':'#c4cbd3'},
           labels={'Change (percentage points)':'Paved area converted (% of total site)'},
           title='Modeled runoff reduction by conceptual design change')
fig.update_layout(plot_bgcolor='rgba(0,0,0,0)',paper_bgcolor='rgba(0,0,0,0)',legend_title_text='')
st.plotly_chart(fig,use_container_width=True)
with st.expander('View every scenario and assumptions'):
    display_cols=['Design scenario','Proposed impervious (%)','Area changed (acres)','Illustrative cost ($)','Runoff volume (ft³)','Runoff reduction (ft³)','Within budget']
    st.dataframe(df[display_cols],hide_index=True,use_container_width=True)
    st.caption('Budget and unit cost are illustrative. Converting developed pavement to pervious landscaping may be impractical for traffic, ADA access, utilities, and site use. Alternatives are not BMP performance claims. Local design standards, soil testing and professional review are required.')

st.subheader('03 / What does the AI actually do?')
left,right=st.columns(2)
with left:
    st.metric('AI estimated event runoff',f'{ai_volume:,.0f} ft³')
    st.caption('Random Forest regression prediction trained on synthetic NRCS-based scenarios.')
with right:
    st.metric('Difference vs exact engineering calculation',f'{(ai_volume-volume):+,.0f} ft³')
    st.caption('AI is an approximation of the engineering model. The direct formula is preferred for final values.')
with st.expander('AI method, validation and honest limitations',expanded=True):
    st.write(f"**Training:** {metrics['train_size']:,} synthetic engineering scenarios. **Held-out testing:** {metrics['test_size']:,} scenarios.")
    st.write(f"**Test mean absolute error:** {metrics['mae_ft3']:,.0f} ft³. **Test R²:** {metrics['r2']:.3f}.")
    st.write('A scikit-learn Random Forest learns to approximate computed runoff volumes from rainfall, area, impervious cover, and soil group. Synthetic validation only tests agreement with the assumed equation; it is **not** field accuracy. Current AI is a proof of concept, not proof of added benefit over direct calculation. Future work would train on observed or detailed-model outcomes and include uncertainty, cost data, and site constraints.')

st.subheader('04 / Engineering decision notes')
st.markdown('''- **Why this matters:** Early site-layout changes can affect how much rainfall becomes direct runoff.
- **Next design questions:** Is reducing hardscape feasible? What are the design-storm and local permit criteria? What are site infiltration rates, groundwater levels, and allowable discharge rates?
- **Potential follow-up practices:** Bioretention, permeable pavement, detention, and rainwater harvesting require separate treatment/storage/hydraulic modeling before claiming quantitative benefits.
- **Not included:** Peak flow, time of concentration, storm sewer design, flood mapping, water quality, existing drainage system performance, climate projections, and detailed construction cost.
''')
st.caption('Original educational prototype · Prepared for preliminary engineering screening only · No results should be used directly for construction or permitting.')
