import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export const api = axios.create({ baseURL: API_BASE_URL })

// Attach the JWT to every request once logged in
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

export async function login(email: string, password: string) {
  const form = new URLSearchParams()
  form.append('username', email)
  form.append('password', password)
  const res = await api.post('/auth/login', form, {
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
  })
  localStorage.setItem('token', res.data.access_token)
  return res.data
}

export function logout() {
  localStorage.removeItem('token')
}

export function isLoggedIn() {
  return !!localStorage.getItem('token')
}

// ---- Resource calls ----
export const getDeals = () => api.get('/deals').then(r => r.data)
export const getDeal = (id: number) => api.get(`/deals/${id}`).then(r => r.data)
export const createDeal = (data: any) => api.post('/deals', data).then(r => r.data)
export const updateDeal = (id: number, data: any) => api.patch(`/deals/${id}`, data).then(r => r.data)

export const getContacts = () => api.get('/contacts').then(r => r.data)
export const createContact = (data: any) => api.post('/contacts', data).then(r => r.data)

export const getCompanies = () => api.get('/companies').then(r => r.data)
export const createCompany = (data: any) => api.post('/companies', data).then(r => r.data)

export const getActivities = (dealId: number) => api.get(`/activities/deal/${dealId}`).then(r => r.data)
export const createActivity = (data: any) => api.post('/activities', data).then(r => r.data)

export const summarizeDeal = (dealId: number) => api.post(`/deals/${dealId}/summarize`).then(r => r.data)
export const nextSteps = (dealId: number) => api.post(`/deals/${dealId}/next-steps`).then(r => r.data)
export const qualifyDeal = (dealId: number) => api.post(`/deals/${dealId}/qualify`).then(r => r.data)
export const getQualifications = (dealId: number) => api.get(`/deals/${dealId}/qualifications`).then(r => r.data)
