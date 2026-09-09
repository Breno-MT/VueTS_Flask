<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'

import { taskApi } from '@/api/tasks'
import type { Task } from '@/types/task'

const tasks = ref<Task[]>([])
const novoTitulo = ref('')
const carregando = ref(false)
const salvando = ref(false)
const erro = ref<string | null>(null)

// Ids com requisição em voo, separados por operação.
// Set é reativo no Vue 3: .add() / .delete() já disparam atualização.
const alternando = ref(new Set<number>())
const removendo = ref(new Set<number>())

const pendentes = computed(() => tasks.value.filter((t) => !t.done).length)
const concluidas = computed(() => tasks.value.length - pendentes.value)

function mensagemDe(e: unknown, fallback: string): string {
  return e instanceof Error ? e.message : fallback
}

async function carregar() {
  carregando.value = true
  erro.value = null
  try {
    tasks.value = await taskApi.list()
  } catch (e) {
    erro.value = mensagemDe(e, 'Falha ao carregar as tarefas')
  } finally {
    carregando.value = false
  }
}

async function criar() {
  const titulo = novoTitulo.value.trim()
  if (!titulo) return

  salvando.value = true
  erro.value = null
  try {
    const task = await taskApi.create(titulo)
    tasks.value.unshift(task)
    novoTitulo.value = ''
  } catch (e) {
    erro.value = mensagemDe(e, 'Falha ao criar a tarefa')
  } finally {
    salvando.value = false
  }
}

async function alternar(task: Task) {
  if (alternando.value.has(task.id)) return

  alternando.value.add(task.id)
  erro.value = null
  try {
    const atualizada = await taskApi.toggle(task.id, !task.done)
    Object.assign(task, atualizada)
  } catch (e) {
    erro.value = mensagemDe(e, 'Falha ao atualizar a tarefa')
  } finally {
    alternando.value.delete(task.id)
  }
}

async function remover(task: Task) {
  if (removendo.value.has(task.id)) return

  removendo.value.add(task.id)
  erro.value = null
  try {
    await taskApi.remove(task.id)
    tasks.value = tasks.value.filter((t) => t.id !== task.id)
  } catch (e) {
    erro.value = mensagemDe(e, 'Falha ao remover a tarefa')
  } finally {
    removendo.value.delete(task.id)
  }
}

function formatarData(iso: string): string {
  return new Date(iso).toLocaleDateString('pt-BR', {
    day: '2-digit',
    month: 'short',
  })
}

onMounted(carregar)
</script>

<template>
  <v-app>
    <v-app-bar color="primary" flat>
      <v-app-bar-title class="font-weight-bold">
        <v-icon icon="mdi-checkbox-marked-circle-outline" class="mr-2" />
        Minhas Tarefas
      </v-app-bar-title>
    </v-app-bar>

    <v-main>
      <v-container class="py-8 mx-auto" style="max-width: 720px">
        <!-- Formulário -->
        <v-card class="mb-6">
          <v-card-text>
            <form class="d-flex ga-3 align-start" @submit.prevent="criar">
              <v-text-field
                v-model="novoTitulo"
                label="O que precisa ser feito?"
                counter="200"
                maxlength="200"
                hide-details="auto"
                prepend-inner-icon="mdi-plus-circle-outline"
                :disabled="salvando"
              />
              <v-btn
                type="submit"
                color="primary"
                size="large"
                :loading="salvando"
                :disabled="!novoTitulo.trim()"
              >
                Adicionar
              </v-btn>
            </form>
          </v-card-text>
        </v-card>

        <!-- Erro -->
        <v-alert
          v-if="erro"
          type="error"
          variant="tonal"
          class="mb-6"
          closable
          @click:close="erro = null"
        >
          {{ erro }}
        </v-alert>

        <!-- Contadores -->
        <div v-if="tasks.length" class="d-flex ga-2 mb-4">
          <v-chip prepend-icon="mdi-clock-outline" color="primary" variant="tonal">
            {{ pendentes }} pendente{{ pendentes === 1 ? '' : 's' }}
          </v-chip>
          <v-chip prepend-icon="mdi-check" color="success" variant="tonal">
            {{ concluidas }} concluída{{ concluidas === 1 ? '' : 's' }}
          </v-chip>
        </div>

        <!-- Lista -->
        <v-card>
          <div v-if="carregando" class="d-flex justify-center py-12">
            <v-progress-circular color="primary" indeterminate size="40" />
          </div>

          <v-card-text v-else-if="tasks.length === 0" class="text-center py-12">
            <v-icon icon="mdi-clipboard-text-outline" size="56" color="grey-lighten-1" />
            <p class="text-body-1 text-medium-emphasis mt-3 mb-0">
              Nenhuma tarefa ainda. Adicione a primeira acima.
            </p>
          </v-card-text>

          <v-list v-else lines="two">
            <template v-for="(task, i) in tasks" :key="task.id">
              <v-divider v-if="i > 0" />

              <v-list-item
                :subtitle="formatarData(task.createdAt)"
                :style="{ opacity: removendo.has(task.id) ? 0.5 : 1 }"
              >
                <template #prepend>
                  <!-- Largura fixa: o spinner ocupa o mesmo espaço do checkbox,
                       então o título não pula quando um troca pelo outro. -->
                  <div class="d-flex align-center justify-center" style="width: 40px">
                    <v-progress-circular
                      v-if="alternando.has(task.id)"
                      color="success"
                      indeterminate
                      size="20"
                      width="2"
                    />
                    <v-checkbox-btn
                      v-else
                      :model-value="task.done"
                      color="success"
                      :disabled="removendo.has(task.id)"
                      @update:model-value="alternar(task)"
                    />
                  </div>
                </template>

                <template #title>
                  <span :class="{ 'text-decoration-line-through text-medium-emphasis': task.done }">
                    {{ task.title }}
                  </span>
                </template>

                <template #append>
                  <v-btn
                    icon="mdi-delete-outline"
                    variant="text"
                    color="error"
                    size="small"
                    :loading="removendo.has(task.id)"
                    :disabled="alternando.has(task.id)"
                    :aria-label="`Remover ${task.title}`"
                    @click="remover(task)"
                  />
                </template>
              </v-list-item>
            </template>
          </v-list>
        </v-card>
      </v-container>
    </v-main>
  </v-app>
</template>
