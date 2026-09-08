import pytest
from mi_proyecto_speckit.converter import (
    Unit,
    convert_temperature,
    format_result,
    round_result,
    AbsoluteZeroError,
)


class TestUserStory1CelsiusFahrenheit:
    """Criterios de aceptación para User Story 1: Conversiones Celsius <-> Fahrenheit."""

    def test_celsius_to_fahrenheit_freezing_point(self):
        # 0.0 °C -> 32.000 °F
        result = convert_temperature(0.0, "C", "F")
        assert result == 32.0
        assert format_result(result) == "32.000"

    def test_fahrenheit_to_celsius_boiling_point(self):
        # 212.0 °F -> 100.000 °C
        result = convert_temperature(212.0, "F", "C")
        assert result == 100.0
        assert format_result(result) == "100.000"

    def test_celsius_to_fahrenheit_body_temperature(self):
        # 37.0 °C -> 98.600 °F
        result = convert_temperature(37.0, "C", "F")
        assert result == 98.6
        assert format_result(result) == "98.600"

    def test_celsius_to_fahrenheit_rounding_three_decimals(self):
        # 35.5555 °C -> 96.000 °F
        # (35.5555 * 9/5) + 32 = 64.0 + 32 = 96.0
        result = convert_temperature(35.5555, "C", "F")
        assert round_result(result) == 96.0


class TestUserStory2KelvinAbsoluteZero:
    """Criterios de aceptación para User Story 2: Kelvin y Cero Absoluto."""

    def test_celsius_to_kelvin(self):
        # 0.0 °C -> 273.150 K
        result = convert_temperature(0.0, "C", "K")
        assert result == 273.15
        assert format_result(result) == "273.150"

    def test_kelvin_to_celsius(self):
        # 373.15 K -> 100.000 °C
        result = convert_temperature(373.15, "K", "C")
        assert result == 100.0
        assert format_result(result) == "100.000"

    def test_fahrenheit_to_kelvin(self):
        # 32.0 °F -> 273.150 K
        result = convert_temperature(32.0, "F", "K")
        assert result == 273.15
        assert format_result(result) == "273.150"

    def test_kelvin_to_fahrenheit(self):
        # 273.15 K -> 32.000 °F
        result = convert_temperature(273.15, "K", "F")
        assert result == 32.0
        assert format_result(result) == "32.000"

    def test_reject_kelvin_less_than_zero(self):
        # Rechaza cualquier valor en Kelvin < 0
        with pytest.raises(AbsoluteZeroError, match="cero absoluto"):
            convert_temperature(-1.0, "K", "C")
        with pytest.raises(AbsoluteZeroError, match="cero absoluto"):
            convert_temperature(-0.001, "K", "F")

    def test_reject_celsius_below_absolute_zero(self):
        # Menor a -273.15 °C
        with pytest.raises(AbsoluteZeroError, match="cero absoluto"):
            convert_temperature(-300.0, "C", "K")

    def test_reject_fahrenheit_below_absolute_zero(self):
        # Menor a -459.67 °F
        with pytest.raises(AbsoluteZeroError, match="cero absoluto"):
            convert_temperature(-500.0, "F", "C")

    def test_exact_absolute_zero_allowed(self):
        # 0.0 K -> -273.150 °C y -459.670 °F
        c_res = convert_temperature(0.0, "K", "C")
        assert c_res == -273.15
        assert format_result(c_res) == "-273.150"

        f_res = convert_temperature(0.0, "K", "F")
        assert f_res == -459.67
        assert format_result(f_res) == "-459.670"


class TestUserStory3IdentityAndEdgeCases:
    """Criterios de aceptación para User Story 3: Identidad, negativos válidos y entradas inválidas."""

    def test_identity_celsius_to_celsius(self):
        result = convert_temperature(25.5, "C", "C")
        assert result == 25.5
        assert format_result(result) == "25.500"

    def test_identity_fahrenheit_to_fahrenheit(self):
        result = convert_temperature(77.0, "F", "F")
        assert result == 77.0
        assert format_result(result) == "77.000"

    def test_identity_kelvin_to_kelvin(self):
        result = convert_temperature(300.1234, "K", "K")
        assert result == 300.123
        assert format_result(result) == "300.123"

    def test_negative_valid_values_cross_point(self):
        # -40 °C == -40 °F
        result = convert_temperature(-40.0, "C", "F")
        assert result == -40.0
        assert format_result(result) == "-40.000"

        reverse = convert_temperature(-40.0, "F", "C")
        assert reverse == -40.0
        assert format_result(reverse) == "-40.000"

    def test_non_numeric_input_raises_clear_error(self):
        with pytest.raises(ValueError, match="no es un número válido"):
            convert_temperature("abc", "C", "F")
        with pytest.raises(ValueError, match="no es un número válido"):
            convert_temperature("", "C", "F")
        with pytest.raises(ValueError, match="no es un número válido"):
            convert_temperature(None, "C", "F")


