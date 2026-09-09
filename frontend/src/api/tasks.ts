import type { Task } from '@/types/task'

const BASE = '/api/tasks'

export class ApiError extends Error {
  status: number
  errors: Record<string, string>

  constructor(status: number, errors: Record<string, string> = {}) {
    super(Object.values(errors)[0] ?? `Erro HTTP ${status}`)
    this.name = 'ApiError'
    this.status = status
    this.errors = errors
  }
}

async function request<T>(url: string, init?: RequestInit): Promise<T> {
  const res = await fetch(url, {
    headers: { 'Content-Type': 'application/json' },
    ...init,
  })

  if (!res.ok) {
    const body = await res.json().catch(() => null)
    throw new ApiError(res.status, body?.errors)
  }

  if (res.status === 204) return undefined as T
  return (await res.json()) as T
}

export const taskApi = {
  list: () => request<Task[]>(BASE),

  create: (title: string) =>
    request<Task>(BASE, { method: 'POST', body: JSON.stringify({ title }) }),

  toggle: (id: number, done: boolean) =>
    request<Task>(`${BASE}/${id}`, { method: 'PATCH', body: JSON.stringify({ done }) }),

  remove: (id: number) => request<void>(`${BASE}/${id}`, { method: 'DELETE' }),
}
