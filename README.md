# Monthly Stock Picks

## Description

This project offers a system for generating monthly stock picks and visualizing them through a web application. It integrates a Python script for data generation with a React frontend for an interactive display.

## Features

- Generate stock picks based on predefined criteria.
- Visualize stock data, including current value, estimated price, and potential upside.
- Sort stocks by potential upside.
- Select stock picks by date.

## Installation

To set up and run this project, follow these steps:

### Prerequisites

- Node.js (with npm)
- Python 3
- gemini-cli

### Steps

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/gemini-stock-picking.git
    cd gemini-stock-picking
    ```

2.  **Install Python dependencies:**

    ```bash
    # Assuming you have a requirements.txt or similar, otherwise list them here
    # pip install -r requirements.txt
    ```

3.  **Install Node.js dependencies for the web application:**

    ```bash
    cd web_app
    npm install
    cd ..
    ```

## Usage

### Generating Stock Picks

To generate new stock picks, run the Python script:

```bash
python3 scripts/generate_picks.py
```

This will create a new JSON file in `web_app/public/data/` with the generated stock data. You may need to update `web_app/public/data/index.json` to include the new file for it to appear in the web application.

### Running the Web Application

To start the web application, navigate to the `web_app` directory and run:

```bash
cd web_app
npm start
```

This will typically open the application in your browser at `http://localhost:3000`.

## Project Structure

- `investor.md`: Defines the prompt used by the `generate_picks.py` script to instruct the Gemini model on how to generate stock picks. This file is crucial for customizing the stock picking logic.
- `scripts/`: Contains Python scripts for generating stock data.
- `web_app/`: Contains the React web application.
  - `public/data/`: Stores the generated stock data JSON files and `index.json`.
  - `src/`: Source code for the React application.
    - `components/`: React components like `StockCard.js`.

## Contributing

Contributions are welcome! Please feel free to open issues or submit pull requests.

## License

This project is licensed under the [GNU General Public License v3.0](LICENSE).