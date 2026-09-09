<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'

import { taskApi } from '@/api/tasks'
import type { Task } from '@/types/task'

const tasks = ref<Task[]>([])
const novoTitulo = ref('')
const carregando = ref(false)
const erro = ref<string | null>(null)

const pendentes = computed(() => tasks.value.filter((t) => !t.done).length)

async function carregar() {
  carregando.value = true
  erro.value = null
  try {
    tasks.value = await taskApi.list()
  } catch (e) {
    erro.value = e instanceof Error ? e.message : 'Falha ao carregar'
  } finally {
    carregando.value = false
  }
}

async function criar() {
  const titulo = novoTitulo.value.trim()
  if (!titulo) return

  try {
    const task = await taskApi.create(titulo)
    tasks.value.unshift(task)
    novoTitulo.value = ''
  } catch (e) {
    erro.value = e instanceof Error ? e.message : 'Falha ao criar'
  }
}

async function alternar(task: Task) {
  const atualizada = await taskApi.toggle(task.id, !task.done)
  Object.assign(task, atualizada)
}

async function remover(task: Task) {
  await taskApi.remove(task.id)
  tasks.value = tasks.value.filter((t) => t.id !== task.id)
}

onMounted(carregar)
</script>

<template>
  <main>
    <h1>
      Tarefas <small>({{ pendentes }} pendentes)</small>
    </h1>

    <form @submit.prevent="criar">
      <input v-model="novoTitulo" placeholder="Nova tarefa" maxlength="200" />
      <button type="submit" :disabled="!novoTitulo.trim()">Adicionar</button>
    </form>

    <p v-if="erro" role="alert">{{ erro }}</p>
    <p v-if="carregando">Carregando…</p>

    <ul v-else>
      <li v-for="task in tasks" :key="task.id">
        <input type="checkbox" :checked="task.done" @change="alternar(task)" />
        <span :class="{ feita: task.done }">{{ task.title }}</span>
        <button type="button" @click="remover(task)">×</button>
      </li>
    </ul>

    <p v-if="!carregando && tasks.length === 0">Nenhuma tarefa ainda.</p>
  </main>
</template>

<style scoped>
.feita {
  text-decoration: line-through;
  opacity: 0.6;
}
</style>
