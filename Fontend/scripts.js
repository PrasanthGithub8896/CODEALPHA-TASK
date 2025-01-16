const apiUrl = 'http://127.0.0.1:5000';

async function fetchStocks() {
    const response = await fetch(`${apiUrl}/stocks`);
    const data = await response.json();
    updatePortfolio(data);
}

async function addStock() {
    const symbol = document.getElementById('stock-symbol').value;
    const quantity = document.getElementById('stock-quantity').value;

    if (!symbol || !quantity) {
        alert('Please fill in both fields.');
        return;
    }

    await fetch(`${apiUrl}/stocks`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ symbol, quantity: parseInt(quantity) })
    });

    fetchStocks();
}

async function removeStock(symbol) {
    await fetch(`${apiUrl}/stocks/${symbol}`, { method: 'DELETE' });
    fetchStocks();
}

function updatePortfolio(data) {
    const tableBody = document.querySelector('#stocks-table tbody');
    const totalValueEl = document.getElementById('total-value');

    tableBody.innerHTML = '';
    let totalValue = 0;

    data.forEach(stock => {
        const row = `
            <tr>
                <td>${stock.symbol}</td>
                <td>${stock.quantity}</td>
                <td>₹${stock.price ? stock.price.toFixed(2) : 'N/A'}</td>
                <td>₹${stock.value ? stock.value.toFixed(2) : 'N/A'}</td>
                <td><button onclick="removeStock('${stock.symbol}')">Remove</button></td>
            </tr>
        `;
        tableBody.innerHTML += row;
        totalValue += stock.value || 0;
    });

    totalValueEl.textContent = `₹${totalValue.toFixed(2)}`;
}

// Initial fetch
fetchStocks();
