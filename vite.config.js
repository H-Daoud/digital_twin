import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      // Proxy API requests to your FastAPI backend
      '/analyze-upload': 'http://localhost:8000',
      '/extract-rule': 'http://localhost:8000',
      '/simulate': 'http://localhost:8000',
      '/simulate_cached': 'http://localhost:8000'
    }
  }
});
