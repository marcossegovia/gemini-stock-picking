import React, { useState, useEffect } from 'react';
import StockCard from './components/StockCard';

function App() {
  const [stocks, setStocks] = useState([]);
  const [selectedDate, setSelectedDate] = useState('');
  const [availableFiles, setAvailableFiles] = useState([]);
  const [selectedFile, setSelectedFile] = useState('');

  useEffect(() => {
    // Fetch the index.json to get all available files
    fetch('/data/index.json')
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        setAvailableFiles(data);
        // Set initial selected date to today if a file exists for today
        const today = new Date();
        const year = today.getFullYear();
        const month = String(today.getMonth() + 1).padStart(2, '0');
        const day = String(today.getDate()).padStart(2, '0');
        const todayDate = `${year}-${month}-${day}`;
        setSelectedDate(todayDate);
      })
      .catch(error => {
        console.error('Error fetching index.json:', error);
        setAvailableFiles([]);
      });
  }, []);

  useEffect(() => {
    if (selectedDate) {
      // Filter files for the selected date
      const filesForDate = availableFiles.filter(file =>
        file.startsWith(`picked_stocks_${selectedDate}`)
      ).sort().reverse(); // Sort to show latest first

      if (filesForDate.length > 0) {
        // Automatically select the latest file for the date
        setSelectedFile(filesForDate[0]);
      } else {
        setSelectedFile('');
        setStocks([]);
      }
    }
  }, [selectedDate, availableFiles]);

  useEffect(() => {
    if (selectedFile) {
      fetch(`/data/${selectedFile}`)
        .then(response => {
          if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
          }
          return response.json();
        })
        .then(data => {
          const parsedStocks = data.map(stock => {
            const parsePrice = (priceString) => {
              if (!priceString) return NaN;
              const numbers = priceString.match(/[\d.]+/g)?.map(Number);
              if (!numbers || numbers.length === 0) {
                return NaN;
              }
              if (numbers.length === 1) {
                return numbers[0];
              }
              return (numbers[0] + numbers[1]) / 2;
            };

            const currentValue = parsePrice(stock.current_value);
            const estimatedPrice = parsePrice(stock.analyst_estimated_price);
            const potentialUpside = ((estimatedPrice - currentValue) / currentValue) * 100;
            return { ...stock, potentialUpside };
          });

          // Sort stocks by potentialUpside in descending order
          const sortedStocks = parsedStocks.sort((a, b) => b.potentialUpside - a.potentialUpside);

          // Find the highest potential upside to mark the "Best Pick"
          const highestPotentialUpside = sortedStocks.length > 0 ? sortedStocks[0].potentialUpside : 0;

          // Add a flag for the best pick
          const finalStocks = sortedStocks.map(stock => ({
            ...stock,
            highestPotentialUpside: highestPotentialUpside
          }));

          setStocks(finalStocks);
        })
        .catch(error => {
          console.error(`Error fetching ${selectedFile}:`, error);
          setStocks([]);
        });
    }
  }, [selectedFile]);

  const handleDateChange = (event) => {
    setSelectedDate(event.target.value);
  };

  const handleFileChange = (event) => {
    setSelectedFile(event.target.value);
  };

  const filesForSelectedDate = availableFiles.filter(file =>
    file.startsWith(`picked_stocks_${selectedDate}`)
  ).sort().reverse();

  return (
    <div className="App">
      <header className="bg-primary text-white text-center py-3 mb-4">
        <h1>Monthly Stock Picks</h1>
      </header>
      <div className="container">
        <div className="mb-3">
          <label htmlFor="datePicker" className="form-label">Select Date:</label>
          <input
            type="date"
            id="datePicker"
            className="form-control"
            value={selectedDate}
            onChange={handleDateChange}
          />
        </div>

        {filesForSelectedDate.length > 0 && (
          <div className="mb-3">
            <label htmlFor="filePicker" className="form-label">Select Pick:</label>
            <select
              id="filePicker"
              className="form-select"
              value={selectedFile}
              onChange={handleFileChange}
            >
              {filesForSelectedDate.map(file => (
                <option key={file} value={file}>
                  {file.replace('picked_stocks_', '').replace('.json', '')}
                </option>
              ))}
            </select>
          </div>
        )}

        <div className="row">
          {stocks.length > 0 ? (
            stocks.map((stock, index) => (
              <div className="col-md-6 col-lg-4 mb-4" key={index}>
                <StockCard stock={stock} />
              </div>
            ))
          ) : (
            <div className="col-12">
              <p>No stock data available for the selected date and time.</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;