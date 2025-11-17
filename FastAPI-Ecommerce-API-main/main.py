from app.main import app
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
  CORSMiddleware,
  allow_origins=["http://localhost:5500", "http://localhost:3000", "http://localhost:8000"], # add your frontend origin(s)
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

if __name__ == "__main__":
    app.run()
