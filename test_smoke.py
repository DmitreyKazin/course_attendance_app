#!/usr/bin/env python3

from app import app


def test_stable():
	client = app.test_client()
	response = client.get('/')
	assert response.status_code == 200 and b"Stable" in response.data

def test_temp():
	client = app.test_client()
	response = client.get('/temp')
	assert response.status_code == 200 and b"Temp" in response.data

def test_all():
	client = app.test_client()
	response = client.get('/all')
	assert response.status_code == 200 and b"All" in response.data

