# Temporary note

==Until the OpenAPI notes are finalized==

```bash
curl -X 'GET' \
  'http://192.168.50.46:8000/heartbeat/' \
  -H 'accept: application/json'
```

```plaintext
{
  "status": "ok",
  "time": "06:10:38"
}
```

```bash
curl -X 'POST' \
  'http://192.168.50.46:8000/transcribe/' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@monday_f4d8.wav;type=audio/wav'
```

```plaintext
{
  "filename": "monday_f4d8.wav",
  "type": "audio/wav",
  "segments": [
    {
      "start": 0.396,
      "end": 0.789,
      "text": " Monday.",
      "words": [
        {
          "word": "Monday.",
          "start": 0.396,
          "end": 0.789,
          "score": 0.937
        }
      ]
    }
  ]
}
```

-   Do the API test with Postman
