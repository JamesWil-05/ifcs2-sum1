def test_smoke():
    assert 5 == 5
    assert bool("Test") == True
    assert bool("") == False
    assert 0 == False
    assert True == True
    assert isinstance("me", str)
    assert 5 > 4