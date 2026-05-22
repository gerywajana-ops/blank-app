import streamlit as st

st.title("🎈 Reyga")
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <title>My Simple App</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <h2>Daftar Tugas Saya</h2>
        <div class="input-group">
            <input type="text" id="taskInput" placeholder="Tambah tugas baru...">
            <button onclick="addTask()">Tambah</button>
        </div>
        <ul id="taskList"></ul>
    </div>
    <script src="script.js"></script>
</body>
</html>
body { font-family: sans-serif; background: #f4f4f4; display: flex; justify-content: center; padding: 50px; }
.container { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); width: 300px; }
.input-group { display: flex; gap: 5px; }
input { flex: 1; padding: 8px; }
button { cursor: pointer; background: #28a745; color: white; border: none; padding: 8px; }
ul { list-style: none; padding: 0; margin-top: 20px; }
li { background: #eee; margin-bottom: 5px; padding: 10px; display: flex; justify-content: space-between; }
function addTask() {
    let input = document.getElementById('taskInput');
    let taskText = input.value;
    if (taskText === '') return;

    let li = document.createElement('li');
    li.innerHTML = `${taskText} <button onclick="this.parentElement.remove()">X</button>`;
    
    document.getElementById('taskList').appendChild(li);
    input.value = '';
}
