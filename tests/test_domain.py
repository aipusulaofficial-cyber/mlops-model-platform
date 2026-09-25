from model_domain import *
def test_lifecycle():
 m=ModelVersion("x","1");m.promote(Stage.VALIDATED);m.promote(Stage.STAGING);m.promote(Stage.PRODUCTION);assert m.stage==Stage.PRODUCTION