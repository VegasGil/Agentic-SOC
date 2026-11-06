import pytest
from unittest.mock import patch
from tools.splunk_reader import fetch_splunk_alerts

def test_splunk_reader_mock(mocker):
    # Simulamos la respuesta de Splunk
    mock_post = mocker.patch("requests.post")
    mock_post.return_value.status_code = 200
    mock_post.return_value.text = '{"result": {"_raw": "{\\"id\\": \\"test-1\\", \\"title\\": \\"Test Alert\\"}"}}\n'
    
    resultado = fetch_splunk_alerts.run()
    assert "Se encontraron 1 alertas" in resultado