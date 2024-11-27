from flask import Flask, render_template_string, request
import os

app = Flask(__name__)

HTML_CONTENT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>To Do Tracker</title>

    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.2/css/all.min.css"
        integrity="sha512-SnH5WK+bZxgPHs44uWIX+LLJAJ9/2PkPKZ5QiAj6Ta86w+fsb2TkcmfRyVX3pBnMFcV7oQPJkl9QevSCWr3W6A=="
        crossorigin="anonymous" 
        referrerpolicy="no-referrer"
    />

    <style>
        * {
            padding: 0;
            margin: 0;
            box-sizing: border-box;
            font-family: "kristen", Kristen ITC;
        }

        body {
            height: 100vh;
            background: linear-gradient(#ffff01 5%, #000000 65%);
        }

        .app {
            width: min(95vw , 500px );
            position: absolute;
            margin: auto;
            left: 0;
            right: 0;
            top: 1.875em;
        }

        .container {
            padding: 2em 2.5em;
            background-color: #e9e8ef;
            box-shadow: 0 1em 2em rgba(0,0,0,0.3);
            border-radius: 1em;
        }

        #wrapper {
            position: relative;
            display: grid;
            grid-template-columns: 8fr 4fr;
            gap: 1em;
        }

        #wrapper input {
            width: 100%;
            background-color: transparent;
            color: #000000;
            font-size: 0.9em;
            border: none;
            border-bottom: 2px solid #000000;
            padding: 1em 0.5em;
        }

        #wrapper input:focus {
            outline: none;
            border-color: #000000;
        }

        #wrapper button {
            position: relative;
            border-radius: 0.5em;
            font-weight: 500;
            font-size: 1.25em;
            background-color: black;
            border: none;
            outline: none;
            color: white;
            cursor: pointer;
        }

        #tasks {
            margin-top: 1em;
            border-radius: 0.5em;
            width: 100%;
            position: relative;
            padding: 1em 0.5em;
        }

        .task {
            background-color: #ffffff;
            padding: 0.8em 1em;
            display: grid;
            grid-template-columns: 1fr 8fr 2fr 2fr;
            gap: 1em;
            border-radius: 0.5em;
            box-shadow: 0 0.5em 1em rgba(0, 0, 0, 0.05);
            align-items: center;
            cursor: pointer;
        }

        .task:not(:first-child) {
            margin-top: 1em;
        }

        .task input[type="checkbox"] {
            position: relative;
            appearance: none;
            height: 20px;
            width: 20px;
            border-radius: 50%;
            border: 2px solid #e1e1e1;
        }

        .task input[type="checkbox"]:before  {
            content: "";
            position: absolute;
            transform: translate(-50%, -50%);
            top: 50%;
            left: 50%;
        }

        .task input[type="checkbox"]:checked {
            background-color: #0b6fe0;
            border-color: #0b6fe0;
        }

        .task input[type="checkbox"]:checked:before {
            position: absolute;
            content: "\f00c";
            color: #ffffff;
            font-size: 0.8em;
            font-family: "Font Awesome 5 Free";
            font-weight: 900;
        }

        .task span {
            font: 0.9em;
            font-weight: 400;
            word-break: break-all;
        }

        .task button {
            color: #ffffff;
            width: 100%;
            padding: 0.5em 0;
            border-radius: 0.5em;
            border: none;
            cursor: pointer;
            outline: none;
        }

        .edit {
            background-color: #0b6fe0;
        }

        .delete {
            background-color: #ca1111;
        }

        #pending-tasks span {
            color: #0b6fe0;
        }

        .completed {
            text-decoration: line-through;
            color: #a0a0a0;
        }

        #error {
            text-align: center;
            background-color: rgb(1, 0, 0);
            color: rgba(255, 5, 5, 0.845);
            font-family: 'Times New Roman', Times, serif;
            margin-top: 1.5em;
            padding: 1em 0;
            border-radius: 1em;
            display: none;
        }
    </style>
</head>
<body>
    <div class="app">
        <div class="container">
            <div id="wrapper">
                <input type="text" placeholder="What's there in your mind ?..." id="task-input" />
                <button id="add-button">Add Task</button>
            </div>
            <div id="tasks">
                <p id="pending-tasks">
                    You have <span class="count-value">0</span> task(s) to complete
                </p>
            </div>
        </div>
        <p id="error">Input cannot be empty !!</p>
    </div>

    <script>
        const addButton = document.querySelector("#add-button");
        const newTaskInput = document.querySelector("#task-input");
        const tasksContainer = document.querySelector("#tasks");
        const error = document.getElementById('error');
        const countValue = document.querySelector(".count-value");
        let taskCount = 0;

        const displayCount = (taskCount) => {
            countValue.innerText = taskCount;
        }

        const addTask = () => {
            const taskName = newTaskInput.value.trim();
            error.style.display = "none";
            if (!taskName) {
                setTimeout(() => {
                    error.style.display = "block";
                }, 200);
                return;
            }

            const task = `
                <div class="task">
                    <input type="checkbox" class="task-check">
                    <span class="taskname">${taskName}</span>
                    <button class="edit">
                        <i class="fa-solid fa-pen-to-square"></i>
                    </button>
                    <button class="delete">
                        <i class="fa-solid fa-trash"></i>
                    </button>
                </div>`;

            tasksContainer.insertAdjacentHTML("beforeend", task);

            const deleteButtons = document.querySelectorAll(".delete");

            deleteButtons.forEach((button) => {
                button.onclick = () => {
                    const taskElement = button.parentNode;
                    if (!taskElement.querySelector(".task-check").checked) {
                        taskCount -= 1;
                    }
                    taskElement.remove();
                    displayCount(taskCount);
                }
            });

            const editButtons = document.querySelectorAll(".edit");

            editButtons.forEach((editButton) => {
                editButton.onclick = (e) => {
                    let taskElement = e.target.closest(".task");
                    newTaskInput.value = taskElement.querySelector(".taskname").innerText;
                    if (!taskElement.querySelector(".task-check").checked) {
                        taskCount -= 1;
                    }
                    taskElement.remove();
                    displayCount(taskCount);
                }
            });

            const tasksCheck = document.querySelectorAll(".task-check");

            tasksCheck.forEach((checkBox) => {
                checkBox.onchange = () => {
                    checkBox.nextElementSibling.classList.toggle("completed");
                    if (checkBox.checked) {
                        taskCount -= 1;    
                    } else {
                        taskCount += 1;
                    }
                    displayCount(taskCount);
                }
            });

            taskCount += 1; 
            displayCount(taskCount);
            newTaskInput.value = "";
        };

        addButton.addEventListener("click", addTask);

        window.onload = () => {
            taskCount = 0;
            displayCount(taskCount);
            newTaskInput.value = "";
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_CONTENT)

if __name__ == '__main__':
    app.run(debug=True)
