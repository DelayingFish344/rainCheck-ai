"""RainCheck AI engineering calculations. Screening-only, not construction design."""
from dataclasses import dataclass

PERVIOUS_CN = {'A': 39, 'B': 61, 'C': 74, 'D': 80}  # NRCS open space good condition, assumed
IMPERVIOUS_CN = 98
FT2_PER_ACRE = 43560


def composite_cn(impervious_pct: float, soil_group: str) -> float:
    if not 0 <= impervious_pct <= 100:
        raise ValueError('Impervious percentage must be between 0 and 100.')
    if soil_group not in PERVIOUS_CN:
        raise ValueError('Soil group must be A, B, C, or D.')
    f = impervious_pct / 100
    return f * IMPERVIOUS_CN + (1 - f) * PERVIOUS_CN[soil_group]


def runoff_depth_in(rainfall_in: float, cn: float) -> float:
    if rainfall_in < 0 or not 0 < cn <= 100:
        raise ValueError('Invalid rainfall or curve number.')
    s = 1000 / cn - 10
    ia = 0.2 * s
    if rainfall_in <= ia:
        return 0.0
    return (rainfall_in - ia) ** 2 / (rainfall_in + 0.8 * s)


def runoff_volume_ft3(rainfall_in: float, area_acres: float, impervious_pct: float, soil_group: str) -> float:
    if area_acres <= 0:
        raise ValueError('Drainage area must be positive.')
    q = runoff_depth_in(rainfall_in, composite_cn(impervious_pct, soil_group))
    return q / 12 * area_acres * FT2_PER_ACRE


def compare_options(rainfall_in: float, area_acres: float, impervious_pct: float, soil_group: str, budget: float):
    """Screen land-cover conversion scenarios, not engineered BMP performance.

    Conversions are absolute % of site area (percentage points), only when paved area exists.
    Placeholder costs are illustrative and must be replaced with local estimates.
    """
    base = runoff_volume_ft3(rainfall_in, area_acres, impervious_pct, soil_group)
    rows = []
    for points in (0, 5, 10, 15, 20, 25, 30):
        if points > impervious_pct:
            continue
        converted_acres = area_acres * points / 100
        # Illustrative flat per-acre conversion planning cost: NOT contractor quotes.
        cost = converted_acres * 90000
        new_impervious = impervious_pct - points
        vol = runoff_volume_ft3(rainfall_in, area_acres, new_impervious, soil_group)
        reduction = max(0.0, base - vol)
        rows.append({
            'Design scenario': 'Existing plan' if points == 0 else f'Convert {points} pp of site from paving to landscaped pervious cover',
            'Change (percentage points)': points,
            'Proposed impervious (%)': new_impervious,
            'Area changed (acres)': converted_acres,
            'Illustrative cost ($)': cost,
            'Runoff volume (ft³)': vol,
            'Runoff reduction (ft³)': reduction,
            'Runoff reduction (%)': 100 * reduction / base if base else 0,
            'Within budget': cost <= budget,
        })
    return rows
