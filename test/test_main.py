import unittest
from src.main import main2

class TestMain(unittest.TestCase):
    def test_main_runs(self):
        # Solo verificamos que se ejecuta sin errores
        try:
            main2()
        except Exception as e:
            self.fail(f"main() lanzó una excepción: {e}")

if __name__ == "__main__":
    unittest.main()
