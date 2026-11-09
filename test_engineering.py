from engineering import runoff_depth_in, composite_cn, runoff_volume_ft3, compare_options

def test_basics():
    assert runoff_depth_in(0,85)==0
    assert runoff_depth_in(3,85)>0
    assert composite_cn(100,'B')==98
    assert runoff_volume_ft3(3,5,80,'B')>runoff_volume_ft3(3,5,40,'B')
    rows=compare_options(3,5,65,'B',50000)
    assert rows[0]['Runoff reduction (ft³)']==0
    assert all(r['Runoff reduction (ft³)']>=0 for r in rows)
    assert rows[-1]['Runoff reduction (ft³)']>rows[1]['Runoff reduction (ft³)']
if __name__=='__main__':
    test_basics()
    print('Engineering tests passed')
