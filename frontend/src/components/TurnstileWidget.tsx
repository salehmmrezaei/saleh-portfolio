import { useEffect, useRef } from 'react';

declare global {
  interface Window {
    turnstile?: {
      render: (
        container: HTMLElement,
        options: {
          sitekey: string;
          callback: (token: string) => void;
          'expired-callback': () => void;
          'error-callback': () => void;
          theme?: 'light' | 'dark' | 'auto';
        },
      ) => string;
      remove: (widgetId: string) => void;
    };
  }
}

interface TurnstileWidgetProps {
  onTokenChange: (token: string) => void;
}

export function TurnstileWidget({ onTokenChange }: TurnstileWidgetProps) {
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const siteKey = import.meta.env.VITE_TURNSTILE_SITE_KEY;

    if (!siteKey) {
      console.error('VITE_TURNSTILE_SITE_KEY is not configured');
      return;
    }

    let widgetId: string | undefined;

    const renderWidget = () => {
      if (!containerRef.current || !window.turnstile || widgetId) {
        return;
      }

      widgetId = window.turnstile.render(containerRef.current, {
        sitekey: siteKey,
        theme: 'auto',
        callback: (token) => onTokenChange(token),
        'expired-callback': () => onTokenChange(''),
        'error-callback': () => onTokenChange(''),
      });
    };

    renderWidget();

    const interval = window.setInterval(() => {
      renderWidget();

      if (widgetId) {
        window.clearInterval(interval);
      }
    }, 250);

    return () => {
      window.clearInterval(interval);

      if (widgetId && window.turnstile) {
        window.turnstile.remove(widgetId);
      }
    };
  }, [onTokenChange]);

  return <div ref={containerRef} className="turnstile-widget" />;
}