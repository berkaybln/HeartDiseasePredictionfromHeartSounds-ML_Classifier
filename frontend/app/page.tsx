'use client';

import { useEffect, useState } from 'react';
import axios from 'axios';
import { HeartPulse, Activity, Search, Play, ClipboardList, Info } from 'lucide-react';

const API_BASE_URL = 'https://berkaybln-heartguard.hf.space';


const VALID_LOCATIONS = [
  "Apex", "LC (Left,Carotid)", "RC (Right,Carotid)", "LUA (Left,Upper,Anterior)", "RUA (Right,Upper,Anterior)",
  "LMA (Left,Mid,Anterior)", "RMA (Right,Mid,Anterior)", "LLA (Left,Lower,Anterior)", "RLA (Right,Lower,Anterior)",
   "LLSB (Left,Lower,Sternal Border)", "LUSB (Left,Upper,Sternal Border)", "RUSB (Right,Upper,Sternal Border)",

];

export default function DashboardPage() {
  const [soundIds, setSoundIds] = useState<string[]>([]);
  const [selectedId, setSelectedId] = useState<string>('');
  const [gender, setGender] = useState<'M' | 'F'>('M');
  const [location, setLocation] = useState<string>(VALID_LOCATIONS[0]);
  const [prediction, setPrediction] = useState<{result: string, status: 'idle' | 'loading' | 'success' | 'error'}>({
    result: '',
    status: 'idle'
  });

  useEffect(() => {
    axios.get<{ sounds: string[] }>(`${API_BASE_URL}/get-sounds`)
      .then(res => {
        setSoundIds(res.data.sounds);
        if (res.data.sounds.length > 0) setSelectedId(res.data.sounds[0]);
      })
      .catch(() => alert("Backend bağlantısı kurulamadı!"));
  }, []);

  const handleAnalyze = async () => {
    setPrediction({ result: '', status: 'loading' });
    try {
      const res = await axios.post(`${API_BASE_URL}/predict`, {
        Gender: gender,
        Location: location,
        "Heart Sound ID": selectedId
      });
      setPrediction({ result: res.data.prediction, status: 'success' });
    } catch {
      setPrediction({ result: 'Hata oluştu', status: 'error' });
    }
  };

  return (
    <main className="min-h-screen bg-[#0f172a] text-slate-200 font-sans selection:bg-sky-500/30">

      {/* HEADER BÖLÜMÜ - GitHub Linki Burada */}
      <div className="max-w-7xl mx-auto px-4 pt-12 mb-16">
        <a
          href="https://github.com/berkaybln"
          target="_blank"
          rel="noopener noreferrer"
          className="group inline-flex items-center gap-5 cursor-pointer"
          title="View on GitHub"
        >
          <div className="p-4 bg-sky-500/10 rounded-2xl ring-1 ring-sky-500/50 shadow-[0_0_20px_rgba(14,165,233,0.15)] transition-all group-hover:bg-sky-500/20 group-hover:ring-sky-500 group-hover:shadow-sky-500/30">
            <HeartPulse className="h-9 w-9 text-sky-400 animate-pulse" />
          </div>

          <div className="flex flex-col">
            <h1 className="text-3xl font-extrabold text-white tracking-tight group-hover:text-sky-400 transition-colors">
              HeartGuard <span className="text-sky-500 text-2xl font-light">Expert System</span>
            </h1>
            <p className="text-slate-400 text-sm font-medium tracking-wide opacity-80">
              Early Diagnosis of Heart Disease • <span className="text-sky-500/60 font-mono text-[10px]">v1.0.4</span>
            </p>
          </div>
        </a>
      </div>

      {/* ANA İÇERİK - Alt Kısım */}
      <div className="max-w-7xl mx-auto px-4 pb-20">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">

          {/* Sol Kolon: Seçim Alanı */}
          <div className="lg:col-span-5 space-y-6">
            <div className="bg-slate-900/50 border border-slate-800 rounded-2xl p-6 backdrop-blur-sm">
              <h2 className="text-sm font-bold text-sky-400 uppercase tracking-widest mb-6 flex items-center gap-2">
                <Search className="h-4 w-4" /> Analysis Information
              </h2>

              <div className="space-y-4">
                <div>
                  <label className="block text-xs font-semibold text-slate-500 mb-2">HEART SOUND</label>
                  <select
                    className="w-full bg-slate-950 border border-slate-700 rounded-xl px-4 py-3 text-sm focus:ring-2 ring-sky-500 outline-none transition-all"
                    value={selectedId}
                    onChange={(e) => setSelectedId(e.target.value)}
                  >
                    {soundIds.map((id, index) => (
                        <option key={id} value={id}>
                          Heart Sound #{index + 1}
                        </option>
                      ))}
                  </select>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-xs font-semibold text-slate-500 mb-2">GENDER</label>
                    <select
                      className="w-full bg-slate-950 border border-slate-700 rounded-xl px-4 py-3 text-sm"
                      value={gender}
                      onChange={(e) => setGender(e.target.value as 'M' | 'F')}
                    >
                      <option value="M">MALE</option>
                      <option value="F">FEMALE</option>
                    </select>
                  </div>
                  <div>
                    <label className="block text-xs font-semibold text-slate-500 mb-2">LOCATION</label>
                    <select
                      className="w-full bg-slate-950 border border-slate-700 rounded-xl px-4 py-3 text-sm"
                      value={location}
                      onChange={(e) => setLocation(e.target.value)}
                    >
                      {VALID_LOCATIONS.map(loc => <option key={loc} value={loc}>{loc}</option>)}
                    </select>
                  </div>
                </div>
              </div>
            </div>

            {/* Bilgi Notu */}
            <div className="bg-sky-500/5 border border-sky-500/20 rounded-2xl p-4 flex gap-3">
              <Info className="h-5 w-5 text-sky-400 shrink-0" />
              <p className="text-sm text-sky-100/70 leading-relaxed">
                <strong className="text-sm text-sky-100/70 font-bold">Location:</strong> The area where the heart is heard <br />
                <strong className="text-sm text-sky-100/70 font-bold">Gender:</strong> Gender <br />
                <br />


                <strong className="text-red-400 font-bold">WARNING:</strong> The selected location and gender information directly affects the result in parallel with the sound analysis. Please enter the correct information provided by the clinic and perform the analysis based on the correct heart sound.
              </p>
            </div>
          </div>

          {/* Sağ Kolon: Dinleme ve Sonuç */}
          <div className="lg:col-span-7 space-y-6">

            {/* Audio Bölümü */}
            <div className="bg-slate-900/50 border border-slate-800 rounded-3xl p-8 text-center relative overflow-hidden group">
              <div className="absolute top-0 right-0 p-4 opacity-10 group-hover:opacity-20 transition-opacity">
                <Play className="h-24 w-24 text-sky-400" />
              </div>

              <h2 className="text-sm font-bold text-slate-400 mb-6 uppercase tracking-widest">signal listening</h2>
              <audio
                key={selectedId}
                controls
                className="w-full mb-8"
                src={`${API_BASE_URL}/listen/${selectedId}`}
              />

              <button
                onClick={handleAnalyze}
                disabled={prediction.status === 'loading'}
                className="w-full py-4 bg-sky-600 hover:bg-sky-500 text-white rounded-2xl font-bold shadow-lg shadow-sky-900/40 transition-all flex items-center justify-center gap-3 disabled:opacity-50"
              >
                {prediction.status === 'loading' ? (
                  <div className="h-5 w-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                ) : <Activity className="h-5 w-5" />}
                {prediction.status === 'loading' ? 'ANALİZ EDİLİYOR...' : 'START ANALYSIS'}
              </button>
            </div>

            {/* Sonuç Bölümü */}
            <div className={`rounded-3xl border p-8 transition-all duration-500 ${
              prediction.status === 'success'
                ? (prediction.result.toLowerCase() === 'normal' ? 'bg-emerald-500/10 border-emerald-500/50' : 'bg-rose-500/10 border-rose-500/50')
                : 'bg-slate-900/30 border-slate-800'
            }`}>
              <div className="flex items-center gap-3 mb-4">
                <ClipboardList className={`h-5 w-5 ${prediction.status === 'success' ? 'text-white' : 'text-slate-500'}`} />
                <h3 className="text-sm font-bold uppercase tracking-widest">DIAGNOSIS REPORT</h3>
              </div>

              <div className="text-center py-4">
                {prediction.status === 'idle' && <p className="text-slate-500 italic text-sm">Start an analysis...</p>}
                {prediction.status === 'success' && (
                  <div>
                    <p className={`text-3xl font-black mb-2 tracking-tight ${
                      prediction.result.toLowerCase() === 'normal' ? 'text-emerald-400' : 'text-rose-400'
                    }`}>
                      {prediction.result.toUpperCase()}
                    </p>
                    <p className="text-xs text-slate-400"></p>
                  </div>
                )}
              </div>
            </div>

          </div>
        </div>
      </div>
    </main>
  );
}