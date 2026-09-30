import { mkdir, readFile, writeFile } from 'node:fs/promises';
import { resolve } from 'node:path';

import react from '@vitejs/plugin-react';
import { defineConfig, loadEnv } from 'vite';

import { projectDetails } from './src/data/projects.ts';

const SITE_URL = 'https://salehmmrezaei.com';
const IMAGE_URL = `${SITE_URL}/saleh-rezaei.png`;

const projectNameBySlug: Record<string, string> = {
  'repopilot-ai': 'RepoPilot AI',
  'voice-notes-ai': 'Voice Notes AI',
  'disagreement-aware-sexism-detection': 'Disagreement-Aware Sexism Detection',
  'reinforcement-learning-lab': 'Reinforcement Learning Lab',
  'time-series-forecasting': 'Time-Series Forecasting',
  'news-popularity-prediction': 'News Popularity Prediction',
};

function escapeHtml(value: string) {
  return value
    .replaceAll('&', '&amp;')
    .replaceAll('"', '&quot;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;');
}

function escapeRegex(value: string) {
  return value.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

function replaceMeta(
  html: string,
  attribute: 'name' | 'property',
  key: string,
  content: string,
) {
  const pattern = new RegExp(
    `<meta[^>]*${attribute}="${escapeRegex(key)}"[^>]*>`,
    'i',
  );

  return html.replace(
    pattern,
    `<meta ${attribute}="${key}" content="${escapeHtml(content)}" />`,
  );
}

function projectSeoPagesPlugin() {
  return {
    name: 'project-seo-pages',
    apply: 'build' as const,

    async closeBundle() {
      const distDirectory = resolve(process.cwd(), 'dist');
      const rootHtml = await readFile(
        resolve(distDirectory, 'index.html'),
        'utf8',
      );

      for (const [slug, details] of Object.entries(projectDetails)) {
        const name = projectNameBySlug[slug];

        if (!name) {
          throw new Error(`Missing project name for ${slug}`);
        }

        const title = `${name} | Saleh Rezaei`;
        const canonicalUrl = `${SITE_URL}/projects/${slug}`;
        const description = details.overview;

        let html = rootHtml.replace(
          /<title>[\s\S]*?<\/title>/i,
          `<title>${escapeHtml(title)}</title>`,
        );

        html = replaceMeta(html, 'name', 'description', description);

        html = html.replace(
          /<link[^>]*rel="canonical"[^>]*>/i,
          `<link rel="canonical" href="${canonicalUrl}" />`,
        );

        html = replaceMeta(html, 'property', 'og:type', 'article');
        html = replaceMeta(html, 'property', 'og:title', title);
        html = replaceMeta(
          html,
          'property',
          'og:description',
          description,
        );
        html = replaceMeta(html, 'property', 'og:url', canonicalUrl);
        html = replaceMeta(html, 'property', 'og:image', IMAGE_URL);

        html = replaceMeta(html, 'name', 'twitter:title', title);
        html = replaceMeta(
          html,
          'name',
          'twitter:description',
          description,
        );
        html = replaceMeta(
          html,
          'name',
          'twitter:card',
          'summary_large_image',
        );
        html = replaceMeta(html, 'name', 'twitter:image', IMAGE_URL);

        const structuredData = {
          '@context': 'https://schema.org',
          '@graph': [
            {
              '@type': 'Person',
              '@id': `${SITE_URL}/#person`,
              name: 'Saleh Rezaei',
              url: `${SITE_URL}/`,
              image: IMAGE_URL,
              jobTitle: 'AI / ML Engineer',
            },
            {
              '@type': 'CreativeWork',
              name,
              url: canonicalUrl,
              description,
              creator: {
                '@id': `${SITE_URL}/#person`,
              },
              dateCreated: details.year,
              keywords: details.coreStack ?? [],
            },
          ],
        };

        html = html.replace(
          /<script type="application\/ld\+json">[\s\S]*?<\/script>/i,
          `<script type="application/ld+json">${JSON.stringify(
            structuredData,
          ).replaceAll('<', '\\u003c')}</script>`,
        );

        const outputDirectory = resolve(
          distDirectory,
          'projects',
          slug,
        );

        await mkdir(outputDirectory, { recursive: true });
        await writeFile(resolve(outputDirectory, 'index.html'), html);
      }
    },
  };
}

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, '.', '');

  return {
    plugins: [react(), projectSeoPagesPlugin()],

    server: {
      proxy: {
        '/api':
          env.VITE_API_PROXY_TARGET || 'http://127.0.0.1:8000',
      },
    },
  };
});
