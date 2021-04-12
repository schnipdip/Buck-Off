# Marker Calls:
#       @pytest.mark.boards
#       @pytest.mark.code

# Example Commandline Call:
#       pytest -m boards .\Buck-Off\tests\test.py -v
#       pytest -m code .\Buck-Off\tests\test.py -v

import pytest

class TestClass:
    
    @pytest.fixture
    def __code(self):
        # Fixtures are constants that can be called into test marks. 
        # Call code classes here to handle and test returns 
        return 0
    
    @pytest.mark.boards
    def test_motion_sensor(self):
        assert 1+1==2
    
    @pytest.mark.boards
    def test_accelerometer_sensor(self):
        assert 2+2==5

    @pytest.mark.boards
    def test_htc_board(self):
        assert 0
