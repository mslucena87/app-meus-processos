import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000/api',
});

// Interceptor para injetar o token JWT em todas as requisições protegidas
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export interface DashboardStats {
  total_processos: number;
  prazos_pendentes: number;
  prazos_urgentes: number;
}

export interface Prazo {
  id: number;
  processo_id: number;
  descricao: string;
  data_inicio: string;
  data_fatal: string;
  dias_uteis: number;
  status: string;
}

export const login = (email: string, senha: string) => 
  api.post<{ access_token: string }>('/login', { email, senha });

export const getStats = () => api.get<DashboardStats>('/dashboard/stats');
export const getPrazos = () => api.get<Prazo[]>('/prazos');
export const sincronizarOab = (oab_numero: string, oab_uf: string, tribunal: string) => 
  api.post('/sincronizar', { oab_numero, oab_uf, tribunal });

export default api;