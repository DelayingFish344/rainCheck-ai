from model import fit_model,features
from engineering import runoff_depth_in,composite_cn
model,metrics=fit_model()
assert metrics['r2'] > .97
assert metrics['mae_in'] < .2
for soil in ['A','B','C','D']:
    x=features(3,65,soil)
    prediction=model.predict([x])[0]
    expected=runoff_depth_in(3,composite_cn(65,soil))
    assert abs(prediction-expected)<.3,(soil,prediction,expected)
print('AI model passed validation/sanity tests:',metrics)
