const messageInput = document.getElementById('message');
const charCount = document.getElementById('char-count');
const updateCount = () => { charCount.textContent = `${messageInput.value.length} / 5000 characters`; };
messageInput.addEventListener('input', updateCount);
document.getElementById('clear-btn').addEventListener('click', () => { messageInput.value = ''; updateCount(); messageInput.focus(); });
document.querySelectorAll('.example').forEach(button => button.addEventListener('click', () => { messageInput.value = button.dataset.message; updateCount(); messageInput.focus(); }));
updateCount();
