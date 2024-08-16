// Show the correct page based on the clicked tab
function showPage(pageId) {
    // Hide all pages
    const pages = document.querySelectorAll('.page');
    pages.forEach(page => page.style.display = 'none');

    // Show the selected page
    const selectedPage = document.getElementById(pageId);
    selectedPage.style.display = 'flex';

    // Highlight the active tab
    const tabs = document.querySelectorAll('.navbar a');
    tabs.forEach(tab => tab.classList.remove('active'));
    document.getElementById(pageId + '_tab').classList.add('active');
}

// Set default page
showPage('create_wallet');

// Create wallet function
function createWallet() {
    const userId = document.getElementById('user_id').value;
    const pin = document.getElementById('pin').value;

    fetch('/create_wallet', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ user_id: userId, pin: pin })
    })
        .then(response => response.json())
    .then(data => {
        document.getElementById('create_wallet_result').textContent = data.message;
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

// Check balance function
function checkBalance() {
    const userId = document.getElementById('balance_user_id').value;

    fetch(`/balance/${userId}`)
    .then(response => response.json())
    .then(data => {
        document.getElementById('balance_result').textContent = data.balance !== undefined ? `Balance: $${data.balance}` : data.message;
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

// Perform transaction function
function performTransaction() {
    const userId = document.getElementById('transaction_user_id').value;
    const amount = document.getElementById('amount').value;
    const transactionType = document.getElementById('transaction_type').value;
    const pin = document.getElementById('transaction_pin').value;

    fetch('/transaction', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ user_id: userId, amount: parseFloat(amount), type: transactionType, pin: pin })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('transaction_result').textContent = data.message;
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

// Get transaction history function
function getTransactionHistory() {
    const userId = document.getElementById('history_user_id').value;

    fetch(`/history/${userId}`)
    .then(response => response.json())
    .then(data => {
        const historyResult = document.getElementById('history_result');
        historyResult.innerHTML = '';
        if (data.history) {
            data.history.forEach(transaction => {
                const listItem = document.createElement('li');
                listItem.textContent = `${transaction.type.charAt(0).toUpperCase() + transaction.type.slice(1)} $${transaction.amount} on ${transaction.date}`;
                historyResult.appendChild(listItem);
            });
        } else {
            historyResult.textContent = data.message;
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

