import { useEffect } from 'react';

interface SeoProps {
  title: string;
  description: string;
  canonicalPath: string;
  type?: 'website' | 'article';
}

const SITE_URL = 'https://salehmmrezaei.com';

function setMeta(name: string, content: string) {
  let element = document.head.querySelector<HTMLMetaElement>(
    `meta[name="${name}"]`,
  );

  if (!element) {
    element = document.createElement('meta');
    element.setAttribute('name', name);
    document.head.appendChild(element);
  }

  element.setAttribute('content', content);
}

function setProperty(property: string, content: string) {
  let element = document.head.querySelector<HTMLMetaElement>(
    `meta[property="${property}"]`,
  );

  if (!element) {
    element = document.createElement('meta');
    element.setAttribute('property', property);
    document.head.appendChild(element);
  }

  element.setAttribute('content', content);
}

function setCanonical(url: string) {
  let element = document.head.querySelector<HTMLLinkElement>(
    'link[rel="canonical"]',
  );

  if (!element) {
    element = document.createElement('link');
    element.setAttribute('rel', 'canonical');
    document.head.appendChild(element);
  }

  element.setAttribute('href', url);
}

export function Seo({
  title,
  description,
  canonicalPath,
  type = 'website',
}: SeoProps) {
  useEffect(() => {
    const canonicalUrl = `${SITE_URL}${canonicalPath}`;

    document.title = title;

    setMeta('description', description);
    setMeta('robots', 'index, follow');

    setCanonical(canonicalUrl);

    setProperty('og:title', title);
    setProperty('og:description', description);
    setProperty('og:url', canonicalUrl);
    setProperty('og:type', type);
    setProperty('og:site_name', 'Saleh Rezaei');

    setMeta('twitter:card', 'summary');
    setMeta('twitter:title', title);
    setMeta('twitter:description', description);
  }, [title, description, canonicalPath, type]);

  return null;
}
