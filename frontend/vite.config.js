import { fileURLToPath, URL } from 'node:url'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { copyFileSync } from 'fs'

export default defineConfig({
  plugins: [
    vue(),
    {
      name: 'copy-redirects',
      closeBundle() {
        copyFileSync('public/_redirects', 'dist/_redirects')
      }
    }
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    },
  },
})