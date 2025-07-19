import React from 'react';

function StockCard({ stock }) {
  // Helper function to parse price ranges
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

  // Determine if it's a "Best Pick" (first stock) or "Good Pick" (others)
  // This logic will be updated in App.js to reflect sorting by potential upside
  const isBestPick = stock.potentialUpside === undefined ? false : stock.potentialUpside === stock.highestPotentialUpside;
  const badgeClass = isBestPick ? "bg-success" : "bg-info";
  const badgeText = isBestPick ? "Best Pick" : "Good Pick";

  return (
    <div className="card h-100 shadow-sm border-0">
      <div className="card-header bg-primary text-white d-flex justify-content-between align-items-center">
        <h5 className="card-title mb-0">{stock.company_name} ({stock.stock_symbol})</h5>
        {isBestPick && <span className={`badge ${badgeClass}`}>{badgeText}</span>}
      </div>
      <div className="card-body">
        <p className="card-text mb-2">
          <strong className="text-muted">Current Value:</strong> <span className="text-success fw-bold">${currentValue.toFixed(2)}</span>
        </p>
        <p className="card-text mb-2">
          <strong className="text-muted">Estimated Price:</strong> <span className="text-primary fw-bold">${estimatedPrice.toFixed(2)}</span>
        </p>
        {potentialUpside && (
          <p className="card-text mb-2">
            <strong className="text-muted">Potential Upside:</strong> <span className="text-warning fw-bold">{potentialUpside.toFixed(2)}%</span>
          </p>
        )}
        <h6 className="mt-3 mb-2 text-secondary">Summary:</h6>
        <p className="card-text small">{stock.summary}</p>
      </div>
    </div>
  );
}

export default StockCard;