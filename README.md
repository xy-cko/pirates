# Pirates App

A Flask API that takes an English sentence and a magic number, rewrites the sentence with a pirate subject, then translates it into Mongolian and Japanese.

---

## Prerequisites

- Python 3.8+
- pip

## Installation

1. Clone or download the project so the structure looks like this:

```
PIRATES/
├── app.py
├── services/
│   ├── divisor.py
│   ├── logger.py
│   ├── modifier.py
│   └── translator.py
```

2. Install dependencies:

```bash
pip install flask spacy pyinflect deep-translator
python -m spacy download en_core_web_sm
```

## Running the App

From the project root directory:

```bash
python app.py
```

The server starts at `http://127.0.0.1:5000` by default.

---

## API Usage

### Endpoint

```
POST /
Content-Type: application/json
```

### Request Body

| Field          | Type    | Required | Description                        |
|----------------|---------|----------|------------------------------------|
| `sentence`     | string  | Yes      | An English sentence with a subject |
| `magic_number` | integer | Yes      | Used to compute the pirate count   |

The app counts the distinct divisors of `magic_number` to determine how many pirates appear in the output. If the subject of the sentence is `I`, it is replaced with `Pirate King`. Any other subject is replaced with `{divisor_count} Pirates`.

### Example Request (Linux)

```bash
curl -X POST http://127.0.0.1:5000/ \
  -H "Content-Type: application/json" \
  -d '{"sentence": "She runs fast", "magic_number": 12}'
```

### Example Request (Windows)
```bash
Invoke-RestMethod -Uri "http://127.0.0.1:5000/" -Method POST -Headers @{"Content-Type"="application/json"} -Body '{"sentence": "She runs fast", "magic_number": 12}'
```


### Example Request (Windows, alternative)
```bash
curl.exe -X POST http://127.0.0.1:5000/ -H "Content-Type: application/json" -d "{\`"sentence\`": \`"She runs fast\`", \`"magic_number\`": 12}"
```

### Example Response

```json
{
  "english_sentence": "6 Pirates run fast",
  "mongolian_sentence": "6 далайн дээрэмчид хурдан гүйдэг",
  "japanese_sentence": "6人の海賊が速く走る"
}
```

### Error Responses

| Condition                              | Status | Message                   |
|----------------------------------------|--------|---------------------------|
| Missing or invalid JSON                | 400    | `"Invalid request"`       |
| `magic_number` is empty or not an int  | 400    | `"Where is magic?"`       |
| Sentence has no detectable subject     | 400    | `"Where am I?"`           |

---

## Logs

Runtime logs are written to `app.log` in the project root and also printed to stdout.

---

## Testing

A simple testing suite is prepared in test_app.py. To run the tests, make sure you have pytest installed:

```bash
pip install pytest
```

And then run:

```bash
pytest test_app.py
```

---

## Assumptions

- Missing request and empty request are not the same; when `magic_number` parameter is not provided, an `"Invalid request"` error is returned, however, when it is present but its value is empty, a `"Where is magic?"` response is provided.
