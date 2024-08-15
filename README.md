# OpenTeam

## Installation

```
python -m venv .venv  
```

```
source .venv/bin/activate
```

```
pip install -r requirements.txt
```

## Environment variables

Create a `.env` file with the following content:

```
OPENAI_API_KEY=YOUR_API_KEY
OPENAI_MODEL_NAME=YOUR_MODEL_NAME
BASE_URL=YOUR_BASE_URL # optional

ART_GENERATION_EMAIL=example@ex.com
ART_GENERATION_PASSWORD=PASSWORD
ART_GENERATION_MODEL=YOUR_MODEL

TAVILY_API_KEY=YOUR_TAVILY_API_KEY

DB_URI=YOUR_DB_URI
FLIP_ID=YOUR_FLIP_ID
```

## Run

```
python -m analyst.main
```

```
python -m coder.main
```

```
python -m elements_creator.main
```

```
python -m youtube.main
```

```
python -m image_creator.main
```

```
python -m search.main
```
