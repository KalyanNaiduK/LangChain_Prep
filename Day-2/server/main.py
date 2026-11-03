from fastapi import FastAPI

data = [
  {
    "name": "nguyen",
    "country": [
      { "country_id": "VN", "probability": 0.561 },
      { "country_id": "US", "probability": 0.035 },
      { "country_id": "AU", "probability": 0.019 },
      { "country_id": "MO", "probability": 0.018 },
      { "country_id": "CA", "probability": 0.011 }
    ],
    "count": 360408
  },
  {
    "name": "smith",
    "country": [
      { "country_id": "US", "probability": 0.312 },
      { "country_id": "GB", "probability": 0.148 },
      { "country_id": "AU", "probability": 0.071 },
      { "country_id": "CA", "probability": 0.058 },
      { "country_id": "NZ", "probability": 0.024 }
    ],
    "count": 512340
  },
  {
    "name": "garcia",
    "country": [
      { "country_id": "ES", "probability": 0.287 },
      { "country_id": "MX", "probability": 0.214 },
      { "country_id": "US", "probability": 0.133 },
      { "country_id": "AR", "probability": 0.062 },
      { "country_id": "CO", "probability": 0.041 }
    ],
    "count": 298115
  },
  {
    "name": "kim",
    "country": [
      { "country_id": "KR", "probability": 0.642 },
      { "country_id": "US", "probability": 0.087 },
      { "country_id": "CA", "probability": 0.026 },
      { "country_id": "AU", "probability": 0.015 },
      { "country_id": "KP", "probability": 0.012 }
    ],
    "count": 441872
  },
  {
    "name": "tanaka",
    "country": [
      { "country_id": "JP", "probability": 0.834 },
      { "country_id": "US", "probability": 0.031 },
      { "country_id": "BR", "probability": 0.016 },
      { "country_id": "CA", "probability": 0.008 },
      { "country_id": "PE", "probability": 0.005 }
    ],
    "count": 187654
  },
  {
    "name": "muller",
    "country": [
      { "country_id": "DE", "probability": 0.523 },
      { "country_id": "CH", "probability": 0.109 },
      { "country_id": "AT", "probability": 0.064 },
      { "country_id": "US", "probability": 0.047 },
      { "country_id": "LU", "probability": 0.009 }
    ],
    "count": 156203
  },
  {
    "name": "rossi",
    "country": [
      { "country_id": "IT", "probability": 0.718 },
      { "country_id": "CH", "probability": 0.039 },
      { "country_id": "AR", "probability": 0.027 },
      { "country_id": "BR", "probability": 0.021 },
      { "country_id": "US", "probability": 0.018 }
    ],
    "count": 132987
  },
  {
    "name": "silva",
    "country": [
      { "country_id": "BR", "probability": 0.466 },
      { "country_id": "PT", "probability": 0.198 },
      { "country_id": "AO", "probability": 0.044 },
      { "country_id": "US", "probability": 0.032 },
      { "country_id": "MZ", "probability": 0.017 }
    ],
    "count": 274510
  },
  {
    "name": "patel",
    "country": [
      { "country_id": "IN", "probability": 0.472 },
      { "country_id": "GB", "probability": 0.126 },
      { "country_id": "US", "probability": 0.118 },
      { "country_id": "KE", "probability": 0.034 },
      { "country_id": "CA", "probability": 0.029 }
    ],
    "count": 203476
  },
  {
    "name": "ivanov",
    "country": [
      { "country_id": "RU", "probability": 0.581 },
      { "country_id": "BG", "probability": 0.092 },
      { "country_id": "UA", "probability": 0.061 },
      { "country_id": "KZ", "probability": 0.038 },
      { "country_id": "BY", "probability": 0.027 }
    ],
    "count": 119348
  },
  {
    "name": "hassan",
    "country": [
      { "country_id": "EG", "probability": 0.214 },
      { "country_id": "PK", "probability": 0.137 },
      { "country_id": "SD", "probability": 0.082 },
      { "country_id": "SA", "probability": 0.056 },
      { "country_id": "GB", "probability": 0.043 }
    ],
    "count": 97261
  },
  {
    "name": "dubois",
    "country": [
      { "country_id": "US", "probability": 0.634 },
      { "country_id": "BE", "probability": 0.121 },
      { "country_id": "CA", "probability": 0.055 },
      { "country_id": "CH", "probability": 0.028 },
      { "country_id": "ES", "probability": 0.019 }
    ],
    "count": 84730
  },
  {
    "name": "kowalski",
    "country": [
      { "country_id": "PL", "probability": 0.689 },
      { "country_id": "US", "probability": 0.104 },
      { "country_id": "DE", "probability": 0.052 },
      { "country_id": "GB", "probability": 0.023 },
      { "country_id": "CA", "probability": 0.016 }
    ],
    "count": 76918
  },
  {
    "name": "johansson",
    "country": [
      { "country_id": "SE", "probability": 0.771 },
      { "country_id": "US", "probability": 0.058 },
      { "country_id": "FI", "probability": 0.031 },
      { "country_id": "NO", "probability": 0.022 },
      { "country_id": "DK", "probability": 0.013 }
    ],
    "count": 68025
  },
  {
    "name": "okafor",
    "country": [
      { "country_id": "US", "probability": 0.826 },
      { "country_id": "GB", "probability": 0.049 },
      { "country_id": "NG", "probability": 0.044 },
      { "country_id": "GH", "probability": 0.011 },
      { "country_id": "CA", "probability": 0.008 }
    ],
    "count": 41583
  }
]

# Initialize the application instance
app = FastAPI()

# Define a GET endpoint at the root ("/") URL path
@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}

# Define a GET endpoint with a dynamic path parameter
@app.get("/items/{name}")
def read_item(name: str):
    for item in data:
        if item["name"].lower() == name.lower():
            return item
    return {"error": "Name not found"}
