<template>
  <div style="font-family: system-ui, -apple-system, Arial; padding:1rem; max-width:1200px; margin:0 auto">
    <h1>LangGraph TODOs & Chat</h1>
    <div style="display:flex; gap:1rem; margin-top:1rem">
      <!-- Left column: tasks -->
      <div style="flex:1; min-width:320px; border:1px solid #eee; padding:1rem; border-radius:6px">
        <h2>Tasks</h2>
        <table border="1" cellpadding="8" cellspacing="0" style="width:100%">
          <thead>
            <tr>
              <th>Id</th>
              <th>Title</th>
              <th>Status</th>
              <th>Due</th>
              <th>Priority</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="t in tasks" :key="t.id || t._id">
              <td style="max-width:120px; overflow:hidden">{{ t.id || t._id }}</td>
              <td>{{ t.title }}</td>
              <td>{{ t.status }}</td>
              <td>{{ t.due_date || '-' }}</td>
              <td>{{ t.priority || '-' }}</td>
            </tr>
          </tbody>
        </table>
        <div v-if="loading">Loading...</div>
        <div v-if="error" style="color:red">{{ error }}</div>
      </div>

      <!-- Right column: chat -->
      <div style="flex:1; min-width:320px; border:1px solid #eee; padding:1rem; border-radius:6px; display:flex; flex-direction:column">
        <h2>Chat</h2>
        <div style="flex:1; overflow:auto; margin-bottom:1rem">
          <div v-for="(m, idx) in log" :key="idx" :style="bubbleStyle(m.role)">{{ m.content }}</div>
        </div>
        <form @submit.prevent="send" style="display:flex; gap:.5rem">
          <input v-model="text" placeholder="Say something" style="flex:1" />
          <button>Send</button>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      view: 'tasks',
      tasks: [],
      loading: false,
      error: null,
      text: '',
      log: []
    }
  },
  mounted() {
    this.fetchTasks()
  },
  methods: {
    bubbleStyle(role) {
      return {
        padding: '.5rem 1rem',
        borderRadius: '12px',
        margin: '.5rem 0',
        background: role === 'user' ? '#e6f7ff' : '#f0f0f0',
        textAlign: role === 'user' ? 'right' : 'left'
      }
    },
    async fetchTasks() {
      this.loading = true
      this.error = null
      try {
        const res = await axios.get('http://localhost:8000/tasks')
        this.tasks = res.data
      } catch (err) {
        this.error = err.message || 'Failed to fetch tasks'
      } finally {
        this.loading = false
      }
    },
    async send() {
      if (!this.text.trim()) return
      this.log.push({ role: 'user', content: this.text })
      const body = { text: this.text }
      this.text = ''
      try {
        const res = await axios.post('http://localhost:8000/chat', body)
        this.log.push({ role: 'agent', content: res.data.response || JSON.stringify(res.data) })
      } catch (err) {
        this.log.push({ role: 'agent', content: 'Error contacting agent: ' + err.message })
      }
    }
  }
}
</script>
