<template>
  <div class="todo-app">
    <h1>Todo List</h1>

    <!-- Add New Task -->
    <div class="add-task">
      <input
        v-model="newTask"
        placeholder="Add new task"
        @keyup.enter="addTodo"
      />
      <button @click="addTodo">Add</button>
    </div>

    <!-- Todo List -->
    <ul class="todo-list">
      <li
        v-for="todo in todos"
        :key="todo._id"
        :class="{ completed: todo.completed }"
      >
        <span>{{ todo.task }}</span>
        <button @click="toggleComplete(todo)">
          {{ todo.completed ? 'Undo' : 'Complete' }}
        </button>
        <button @click="deleteTodo(todo._id)">Delete</button>
      </li>
    </ul>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      todos: [],
      newTask: '',
    };
  },
  created() {
    this.fetchTodos();
  },
  methods: {
    // Fetch the list of todos
    async fetchTodos() {
      try {
        const response = await axios.get(
          `${import.meta.env.VITE_API_URL}/todos`
        );
        this.todos = response.data;
      } catch (error) {
        console.error('Error fetching todos:', error);
      }
    },

    // Add a new todo
    async addTodo() {
      if (this.newTask.trim() === '') return; // Do not add empty tasks
      try {
        await axios.post(`${import.meta.env.VITE_API_URL}/todos`, {
          task: this.newTask,
        });
        this.newTask = ''; // Clear the input field
        this.fetchTodos(); // Refresh the todo list
      } catch (error) {
        console.error('Error adding todo:', error);
      }
    },

    // Toggle the completion status of a todo
    async toggleComplete(todo) {
      try {
        await axios.put(`${import.meta.env.VITE_API_URL}/todos/${todo._id}`, {
          completed: !todo.completed,
        });
        this.fetchTodos(); // Refresh the todo list
      } catch (error) {
        console.error('Error updating todo:', error);
      }
    },

    // Delete a todo
    async deleteTodo(id) {
      try {
        await axios.delete(`${import.meta.env.VITE_API_URL}/todos/${id}`);
        this.fetchTodos(); // Refresh the todo list
      } catch (error) {
        console.error('Error deleting todo:', error);
      }
    },
  },
};
</script>

<style>
.todo-app {
  max-width: 600px;
  margin: 50px auto;
  text-align: center;
  font-family: Arial, sans-serif;
}

.add-task {
  margin-bottom: 20px;
}

input {
  padding: 10px;
  font-size: 16px;
  width: 300px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

button {
  padding: 10px 15px;
  margin-left: 10px;
  font-size: 16px;
  background-color: #28a745;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

button:hover {
  background-color: #218838;
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px;
  border-bottom: 1px solid #ccc;
}

li.completed span {
  text-decoration: line-through;
  color: #6c757d;
}

li button {
  background-color: #ffc107;
  margin-right: 5px;
}

li button:hover {
  background-color: #e0a800;
}

li button:last-child {
  background-color: #dc3545;
}

li button:last-child:hover {
  background-color: #c82333;
}
</style>
