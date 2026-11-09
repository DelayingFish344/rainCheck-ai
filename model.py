"""Train a documented synthetic-data ML surrogate; do not misrepresent as field validation."""
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
from engineering import runoff_volume_ft3

GROUPS = ['A', 'B', 'C', 'D']

def features(rainfall_in, area_acres, impervious_pct, soil_group):
    return [rainfall_in, area_acres, impervious_pct, GROUPS.index(soil_group)]


def fit_model(n_samples=2600, random_seed=42):
    rng = np.random.default_rng(random_seed)
    X = np.column_stack([
        rng.uniform(0.1, 8.0, n_samples),
        rng.uniform(0.5, 20.0, n_samples),
        rng.uniform(5.0, 95.0, n_samples),
        rng.integers(0, 4, n_samples),
    ])
    y = np.array([
        runoff_volume_ft3(float(p), float(a), float(i), GROUPS[int(g)])
        for p, a, i, g in X
    ])
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=random_seed)
    m = RandomForestRegressor(n_estimators=90, max_depth=15, min_samples_leaf=2, random_state=random_seed, n_jobs=-1)
    m.fit(X_train, y_train)
    pred = m.predict(X_test)
    return m, {'mae_ft3': float(mean_absolute_error(y_test, pred)), 'r2': float(r2_score(y_test, pred)), 'train_size': len(X_train), 'test_size':len(X_test)}
