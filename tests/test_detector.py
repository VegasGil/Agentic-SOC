import pytest
from unittest.mock import patch
from agents.detector import convert_sigma_to_kql

def test_detector_mock(mocker):
    # Simulamos que el archivo YAML existe
    mocker.patch("os.path.exists", return_value=True)
    mocker.patch("builtins.open", mocker.mock_open(read_data="title: Test"))

    # Simulamos la librería Sigma
    with patch("agents.detector.SigmaCollection.from_yaml") as mock_sigma:
        mock_sigma.return_value = "regla_simulada"
        with patch("agents.detector.KustoBackend.convert") as mock_convert:
            mock_convert.return_value = ["DeviceProcessEvents | where ..."]
            
            resultado = convert_sigma_to_kql.run("test.yml")
            assert "DeviceProcessEvents" in resultado