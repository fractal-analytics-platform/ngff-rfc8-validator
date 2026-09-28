import { defineConfig } from 'vite';
import path from 'path';
import { buildSingleSchema } from './build-single-schema.js';

const __dirname = import.meta.dirname;

export default defineConfig({
  build: {
    lib: {
      entry: path.resolve(__dirname, 'src/main.ts'),
      name: 'ngff-rfc8-validator'
    }
  },
  resolve: {
    alias: {
      'ngff-rfc8-schema': path.resolve(__dirname, './ngff-rfc8-schema.json')
    }
  },
  plugins: [
    {
      name: 'build-schema',
      buildStart() {
        buildSingleSchema();
      }
    }
  ]
});
