import React, { useState, useEffect } from 'react';
import Navbar from './components/Navbar';
import ImageUpload from './components/ImageUpload';
import VideoUpload from './components/VideoUpload';
import WebcamStream from './components/WebcamStream';
import { checkBackendHealth } from './services/api';
import { Flame, Shield, Activity, Github } from 'lucide-react';

export default function App() {
  const [activeTab, setActiveTab] = useState('webcam');
  const [confidence, setConfidence] = useState(0.35);
  const [backendStatus, setBackendStatus] = useState('checking');

  useEffect(() => {
    const verifyHealth = async () => {
      const status = await checkBackendHealth();
      setBackendStatus(status.status === 'online' ? 'online' : 'offline');
    };

    verifyHealth();
    const interval = setInterval(verifyHealth, 5000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="min-h-screen flex flex-col justify-between">
      <div>
        {/* Navigation Bar */}
        <Navbar
          activeTab={activeTab}
          setActiveTab={setActiveTab}
          backendStatus={backendStatus}
        />

        {/* Main Content Area */}
        <main className="max-w-7xl mx-auto px-6 pb-12">
          {activeTab === 'webcam' && (
            <WebcamStream confidence={confidence} setConfidence={setConfidence} />
          )}

          {activeTab === 'image' && (
            <ImageUpload confidence={confidence} setConfidence={setConfidence} />
          )}

          {activeTab === 'video' && (
            <VideoUpload confidence={confidence} setConfidence={setConfidence} />
          )}
        </main>
      </div>

      {/* Footer */}
      <footer className="glass-panel border-t border-slate-800 py-6 px-6 mt-12">
        <div className="max-w-7xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-4 text-xs text-slate-400">
          <div className="flex items-center space-x-2">
            <Flame className="w-4 h-4 text-red-500" />
            <span className="font-semibold text-slate-300">PyraGuard AI Fire Detection System</span>
            <span>&bull; Powered by Ultralytics YOLOv8 & OpenCV</span>
          </div>

          <div className="flex items-center space-x-4 font-mono">
            <span>Server: localhost:8000</span>
            <span>Client: localhost:5173</span>
          </div>
        </div>
      </footer>
    </div>
  );
}
