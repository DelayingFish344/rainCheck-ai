"""Educational ML surrogate for NRCS event runoff DEPTH, not field-validated flood prediction."""
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
from engineering import composite_cn, runoff_depth_in
GROUPS=['A','B','C','D']

def features(rainfall_in, impervious_pct, soil_group):
    return [float(rainfall_in),float(impervious_pct),GROUPS.index(soil_group)]

def fit_model(n_samples=4800, random_seed=42):
    rng=np.random.default_rng(random_seed)
    X=np.column_stack([rng.uniform(0.1,8,n_samples),rng.uniform(5,95,n_samples),rng.integers(0,4,n_samples)])
    y=np.array([runoff_depth_in(float(p), composite_cn(float(i),GROUPS[int(g)])) for p,i,g in X])
    Xtr,Xte,ytr,yte=train_test_split(X,y,test_size=.2,random_state=random_seed)
    m=RandomForestRegressor(n_estimators=100,max_depth=18,min_samples_leaf=1,random_state=random_seed,n_jobs=-1)
    m.fit(Xtr,ytr)
    yp=m.predict(Xte)
    return m,{'train_size':len(Xtr),'test_size':len(Xte),'mae_in':float(mean_absolute_error(yte,yp)), 'r2':float(r2_score(yte,yp))}
