import React, { useEffect, useState } from 'react';
import { getStats, getPrazos, sincronizarOab, login, DashboardStats, Prazo } from './api';

export default function App() {
  const [token, setToken] = useState<string | null>(localStorage.getItem('token'));
  const [email, setEmail] = useState('');
  const [senha, setSenha] = useState('');
  const [erroLogin, setErroLogin] = useState('');

  const [stats, setStats] = useState<DashboardStats>({ total_processos: 0, prazos_pendentes: 0, prazos_urgentes: 0 });
  const [prazos, setPrazos] = useState<Prazo[]>([]);
  const [loading, setLoading] = useState<boolean>(false);

  const [oabNum, setOabNum] = useState('');
  const [oabUf, setOabUf] = useState('SP');
  const [tribunal, setTribunal] = useState('tjsp');

  const carregarDados = async () => {
    try {
      const [resStats, resPrazos] = await Promise.all([getStats(), getPrazos()]);
      setStats(resStats.data);
      setPrazos(resPrazos.data);
    } catch (err) {
      console.error('Erro ao carregar dados:', err);
      // Se der erro 401, limpa o token
      handleLogout();
    }
  };

  useEffect(() => {
    if (token) {
      carregarDados();
    }
  }, [token]);

  const handleLoginSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setErroLogin('');
    try {
      const res = await login(email, senha);
      const accessToken = res.data.access_token;
      localStorage.setItem('token', accessToken);
      setToken(accessToken);
    } catch (err) {
      setErroLogin('E-mail ou senha inválidos.');
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    setToken(null);
  };

  const handleSincronizar = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      await sincronizarOab(oabNum, oabUf, tribunal);
      await carregarDados();
      alert('Sincronização concluída com sucesso!');
    } catch (err) {
      alert('Erro ao sincronizar com o DataJud.');
    } finally {
      setLoading(false);
    }
  };

  // Se não estiver logado, exibe a tela de login
  if (!token) {
    return (
      <div className="min-h-screen bg-slate-900 flex items-center justify-center p-4">
        <div className="bg-white p-8 rounded-2xl shadow-xl w-full max-w-md">
          <div className="text-center mb-8">
            <h1 className="text-2xl font-bold text-slate-900">LegalOps</h1>
            <p className="text-sm text-slate-500 mt-1">Faça login para acessar o painel</p>
          </div>

          {erroLogin && (
            <div className="mb-4 p-3 bg-red-50 border border-red-200 text-red-700 text-sm rounded-lg text-center">
              {erroLogin}
            </div>
          )}

          <form onSubmit={handleLoginSubmit} className="space-y-4">
            <div>
              <label className="block text-xs font-bold text-slate-600 uppercase mb-1">E-mail</label>
              <input
                type="email5"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="admin@legalops.com"
                className="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 outline-none"
                required
              />
            </div>
            <div>
              <label className="block text-xs font-bold text-slate-600 uppercase mb-1">Senha</label>
              <input
                type="password"
                value={senha}
                onChange={(e) => setSenha(e.target.value)}
                placeholder="••••••••"
                className="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 outline-none"
                required
              />
            </div>
            <button
              type="submit"
              className="w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 rounded-lg text-sm transition shadow-md"
            >
              Entrar
            </button>
          </form>

          <div className="mt-6 text-center text-xs text-slate-400">
            Credenciais padrão: <span className="font-semibold text-slate-600">admin@legalops.com</span> / <span className="font-semibold text-slate-600">senha123</span>
          </div>
        </div>
      </div>
    );
  }

  // Dashboard normal autenticado
  return (
    <div className="min-h-screen bg-slate-50 text-slate-800">
      <header className="bg-white border-b border-slate-200">
        <div className="max-w-6xl mx-auto px-6 py-4 flex flex-wrap justify-between items-center gap-4">
          <div>
            <h1 className="text-xl font-bold text-slate-900">LegalOps Dashboard</h1>
            <p className="text-xs text-slate-500">Monitoramento DataJud e Consulta de Prazos</p>
          </div>

          <div className="flex items-center gap-4">
            <form onSubmit={handleSincronizar} className="flex gap-2">
              <input
                type="text"
                placeholder="OAB Ex: 123456"
                value={oabNum}
                onChange={(e) => setOabNum(e.target.value)}
                className="px-3 py-1.5 text-sm border rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
                required
              />
              <input
                type="text"
                placeholder="UF"
                value={oabUf}
                onChange={(e) => setOabUf(e.target.value)}
                className="w-16 px-3 py-1.5 text-sm border rounded-lg uppercase focus:ring-2 focus:ring-blue-500 outline-none"
                maxLength={2}
                required
              />
              <select
                value={tribunal}
                onChange={(e) => setTribunal(e.target.value)}
                className="px-3 py-1.5 text-sm border rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
              >
                <option value="tjsp">TJSP</option>
                <option value="tjrj">TJRJ</option>
                <option value="tjmg">TJMG</option>
                <option value="trf3">TRF3</option>
              </select>
              <button
                type="submit"
                disabled={loading}
                className="bg-blue-600 hover:bg-blue-700 text-white text-sm px-4 py-1.5 rounded-lg font-medium transition disabled:opacity-50"
              >
                {loading ? 'Sincronizando...' : 'Sincronizar'}
              </button>
            </form>

            <button
              onClick={handleLogout}
              className="text-xs font-semibold text-red-600 hover:text-red-800 bg-red-50 hover:bg-red-100 px-3 py-2 rounded-lg transition"
            >
              Sair
            </button>
          </div>
        </div>
      </header>

      <main className="max-w-6xl mx-auto px-6 py-8">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm">
            <span className="text-xs font-bold text-slate-400 uppercase tracking-wider">Total de Processos</span>
            <p className="text-3xl font-extrabold text-slate-900 mt-2">{stats.total_processos}</p>
          </div>
          <div className="bg-white p-6 rounded-xl border border-amber-200 bg-amber-50/30 shadow-sm">
            <span className="text-xs font-bold text-amber-600 uppercase tracking-wider">Prazos Pendentes</span>
            <p className="text-3xl font-extrabold text-amber-700 mt-2">{stats.prazos_pendentes}</p>
          </div>
          <div className="bg-white p-6 rounded-xl border border-red-200 bg-red-50/30 shadow-sm">
            <span className="text-xs font-bold text-red-600 uppercase tracking-wider">Urgentes (≤ 3 dias)</span>
            <p className="text-3xl font-extrabold text-red-700 mt-2">{stats.prazos_urgentes}</p>
          </div>
        </div>

        <div className="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
          <div className="px-6 py-4 border-b border-slate-100">
            <h2 className="text-base font-bold text-slate-900">Prazos Processuais Cadastrados</h2>
          </div>
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="bg-slate-50 text-[11px] font-bold text-slate-400 uppercase tracking-wider border-b border-slate-100">
                <th className="px-6 py-3">Descrição</th>
                <th className="px-6 py-3">Início</th>
                <th className="px-6 py-3">Data Fatal</th>
                <th className="px-6 py-3">Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 text-sm">
              {prazos.length === 0 ? (
                <tr>
                  <td colSpan={4} className="px-6 py-8 text-center text-slate-400">
                    Nenhum prazo registrado até o momento. Sincronize uma OAB para iniciar.
                  </td>
                </tr>
              ) : (
                prazos.map((p) => (
                  <tr key={p.id} className="hover:bg-slate-50 transition">
                    <td className="px-6 py-4 font-medium text-slate-900">{p.descricao}</td>
                    <td className="px-6 py-4 text-slate-600">{p.data_inicio}</td>
                    <td className="px-6 py-4 font-semibold text-slate-900">{p.data_fatal}</td>
                    <td className="px-6 py-4">
                      <span
                        className={`inline-block px-2.5 py-0.5 rounded-full text-xs font-semibold ${
                          p.status === 'URGENTE'
                            ? 'bg-red-100 text-red-700'
                            : 'bg-amber-100 text-amber-700'
                        }`}
                      >
                        {p.status}
                      </span>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </main>
    </div>
  );
}