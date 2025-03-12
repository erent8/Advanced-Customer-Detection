import pytest
import sys
from pathlib import Path

# Src klasörünü Python path'ine ekle
sys.path.append(str(Path(__file__).parent.parent))

@pytest.fixture(autouse=True)
def matplotlib_backend():
    """Test sırasında Matplotlib backend'ini Agg olarak ayarla."""
    import matplotlib
    matplotlib.use('Agg')  # GUI gerektirmeyen backend 