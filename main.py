from fastapi import FastAPI

app = FastAPI(title='Generated Service')


@app.get('/health')
def health() -> dict[str, str]:
    return {'status': 'ok'}
