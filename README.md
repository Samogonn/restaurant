## This repository is used to practice using development patterns.

## It is an application for a restaurant.

### Installation

1. Clone repository:
    ```
    git clone https://github.com/Samogonn/restaurant.git
    cd restaurant/
    ```
2. Install dependencies and activate virtual environment:
    ```
    python3.12 -m venv venv
    . venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
    ```
3. Launch the application:
    ```
    uvicorn app.main:app --reload
    ```
Documentation is available here:
http://127.0.0.1:8000/docs
