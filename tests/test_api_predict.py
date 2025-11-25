import json
from app import app, init_app


def test_predict_endpoint():
    # Ensure app is initialized (loads/creates model)
    init_app()
    client = app.test_client()

    payload = {"features": [0.0] * 10}
    resp = client.post('/api/predict', json=payload)

    assert resp.status_code == 200
    data = resp.get_json()

    assert 'prediction' in data
    assert 'probabilities' in data
    assert 'diagnosis_insights' in data
    assert isinstance(data['prediction'], int)
    assert isinstance(data['probabilities'], dict)
