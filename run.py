from project.main import app  # Importă aplicația din main.py
import uvicorn

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8002)

