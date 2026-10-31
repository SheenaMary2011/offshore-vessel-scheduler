from clean_weather import fix_date, fix_height

def test_fix_date_converts_day_month_year():
    assert fix_date("12/11/2026") == "2026-11-12"

def test_fix_date_no_conversion():
    assert fix_date("2026-11-12") == "2026-11-12"

def test_fix_height_all_scenarios():
    assert fix_height("2.5") == 2.5
    assert fix_height("8.5ft") == 2.6
    assert fix_height(float("nan")) is None
    assert fix_height("-1.0") is None
    assert fix_height("99.0") is None
