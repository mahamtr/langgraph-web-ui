<template>
  <div style="font-family: system-ui, -apple-system, Arial; padding:1rem; max-width:900px; margin:0 auto">
    <h1>LangGraph Simple Chat (Vue)</h1>
    <div v-for="(m, idx) in log" :key="idx" :style="bubbleStyle(m.role)">{{ m.content }}</div>
    <form @submit.prevent="send">
      <input v-model="text" placeholder="Say something" style="width:80%" />
      <button>Send</button>
    </form>
  </div>
</template>

<script>
export default {
  data() {
    return {
      text: '',
      log: []
    }
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
    async send() {
      if (!this.text.trim()) return
      this.log.push({ role: 'user', content: this.text })
      const body = { messages: [{ role: 'user', content: this.text }] }
      this.text = ''
      try {
        const res = await fetch('http://localhost:8000/chat', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(body)
        })
        const data = await res.json()
        this.log.push({ role: 'agent', content: data.reply })
      } catch (err) {
        this.log.push({ role: 'agent', content: 'Error contacting agent: ' + err.message })
      }
    }
  }
}
</script>
