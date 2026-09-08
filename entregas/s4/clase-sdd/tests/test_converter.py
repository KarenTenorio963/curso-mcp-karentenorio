"""Pruebas unitarias para el conversor de temperatura según spec_manual.md."""

import pytest
from clase_sdd.converter import convert_temperature


class TestCelsiusFahrenheit:
    """Criterio: Convierte correctamente de Celsius a Fahrenheit y viceversa."""

    def test_celsius_to_fahrenheit_freezing_point(self):
        assert convert_temperature(0, "Celsius", "Fahrenheit") == 32.0

    def test_celsius_to_fahrenheit_boiling_point(self):
        assert convert_temperature(100, "C", "F") == 212.0

    def test_celsius_to_fahrenheit_body_temperature(self):
        assert convert_temperature(37, "C", "F") == 98.6

    def test_fahrenheit_to_celsius_freezing_point(self):
        assert convert_temperature(32, "Fahrenheit", "Celsius") == 0.0

    def test_fahrenheit_to_celsius_boiling_point(self):
        assert convert_temperature(212, "F", "C") == 100.0


class TestCelsiusKelvin:
    """Criterio: Convierte correctamente de Celsius a Kelvin y viceversa."""

    def test_celsius_to_kelvin_freezing_point(self):
        assert convert_temperature(0, "C", "K") == 273.15

    def test_celsius_to_kelvin_boiling_point(self):
        assert convert_temperature(100, "Celsius", "Kelvin") == 373.15

    def test_kelvin_to_celsius_freezing_point(self):
        assert convert_temperature(273.15, "K", "C") == 0.0

    def test_kelvin_to_celsius_boiling_point(self):
        assert convert_temperature(373.15, "Kelvin", "Celsius") == 100.0


class TestFahrenheitKelvin:
    """Criterio: Convierte correctamente de Fahrenheit a Kelvin y viceversa."""

    def test_fahrenheit_to_kelvin_freezing_point(self):
        assert convert_temperature(32, "F", "K") == 273.15

    def test_fahrenheit_to_kelvin_boiling_point(self):
        assert convert_temperature(212, "F", "K") == 373.15

    def test_kelvin_to_fahrenheit_freezing_point(self):
        assert convert_temperature(273.15, "K", "F") == 32.0

    def test_kelvin_to_fahrenheit_boiling_point(self):
        assert convert_temperature(373.15, "Kelvin", "Fahrenheit") == 212.0


class TestPrecisionDecimals:
    """Criterio: Redondea el resultado obtenido a exactamente 3 decimales."""

    def test_rounding_to_three_decimals(self):
        # 1 F a C: (1 - 32) * 5/9 = -17.222222... -> -17.222
        assert convert_temperature(1, "F", "C") == -17.222

    def test_rounding_celsius_to_fahrenheit_fractional(self):
        # 33.333 C a F: (33.333 * 9/5) + 32 = 59.9994 + 32 = 91.9994 -> 91.999
        res = convert_temperature(33.333, "C", "F")
        assert res == 91.999
        # 10.1234 C a F: (10.1234 * 1.8) + 32 = 18.22212 + 32 = 50.22212 -> 50.222
        assert convert_temperature(10.1234, "C", "F") == 50.222


class TestAbsoluteZeroKelvin:
    """Criterio: Rechaza cualquier valor numérico en la escala Kelvin que sea menor a 0."""

    def test_reject_negative_kelvin(self):
        res = convert_temperature(-1, "K", "C")
        assert isinstance(res, str)
        assert "menor a 0" in res.lower() or "cero absoluto" in res.lower()

    def test_reject_negative_kelvin_fractional(self):
        res = convert_temperature(-0.001, "Kelvin", "Fahrenheit")
        assert isinstance(res, str)
        assert "cero absoluto" in res.lower()

    def test_accept_zero_kelvin(self):
        # 0 Kelvin es exactamente el cero absoluto y debe ser procesado
        assert convert_temperature(0, "K", "C") == -273.15
        assert convert_temperature(0, "K", "F") == -459.67

    def test_reject_below_absolute_zero_in_other_scales(self):
        # Valores que corresponden a Kelvin < 0
        res_c = convert_temperature(-300, "C", "K")
        assert isinstance(res_c, str)
        assert "cero absoluto" in res_c.lower()

        res_f = convert_temperature(-500, "F", "K")
        assert isinstance(res_f, str)
        assert "cero absoluto" in res_f.lower()


class TestEdgeCases:
    """Casos borde especificados en spec_manual.md."""

    def test_non_numeric_input_string(self):
        res = convert_temperature("abc", "C", "F")
        assert isinstance(res, str)
        assert "no numérica" in res.lower() or "error" in res.lower()

    def test_empty_input(self):
        res = convert_temperature("", "C", "F")
        assert isinstance(res, str)
        assert "vacía" in res.lower() or "error" in res.lower()

    def test_none_input(self):
        res = convert_temperature(None, "C", "F")
        assert isinstance(res, str)
        assert "error" in res.lower()

    def test_same_unit_celsius(self):
        assert convert_temperature(25, "Celsius", "Celsius") == 25.0

    def test_same_unit_fahrenheit(self):
        assert convert_temperature(75.5, "F", "F") == 75.5

    def test_same_unit_kelvin(self):
        assert convert_temperature(300.1234, "K", "K") == 300.123

    def test_negative_valid_values(self):
        # -40 C es igual a -40 F
        assert convert_temperature(-40, "C", "F") == -40.0
        assert convert_temperature(-40, "F", "C") == -40.0
        # -10 C a Kelvin: 263.15
        assert convert_temperature(-10, "C", "K") == 263.15
        # -40 F a Kelvin: (-40 - 32)*5/9 + 273.15 = -72*5/9 + 273.15 = -40 + 273.15 = 233.15
        assert convert_temperature(-40, "F", "K") == 233.15

    def test_numeric_strings_converted_properly(self):
        # Soporta valores pasados como string numérico
        assert convert_temperature("100", "C", "F") == 212.0
        assert convert_temperature("-40", "C", "F") == -40.0

    def test_raise_errors_flag(self):
        with pytest.raises(ValueError):
            convert_temperature("invalid", "C", "F", raise_errors=True)
        with pytest.raises(ValueError):
            convert_temperature(-5, "K", "C", raise_errors=True)
