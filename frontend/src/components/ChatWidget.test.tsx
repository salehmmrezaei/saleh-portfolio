import {
  cleanup,
  fireEvent,
  render,
  screen,
  waitFor,
} from '@testing-library/react';
import {
  afterEach,
  describe,
  expect,
  it,
  vi,
} from 'vitest';

import {
  ApiError,
  sendChatMessage,
} from '../api/client';
import { ChatWidget } from './ChatWidget';

vi.mock('../api/client', async (importOriginal) => {
  const actual =
    await importOriginal<typeof import('../api/client')>();

  return {
    ...actual,
    sendChatMessage: vi.fn(),
  };
});

describe('ChatWidget', () => {
  afterEach(() => {
    cleanup();
    vi.clearAllMocks();
  });

  it('opens and shows the portfolio assistant intro', () => {
    render(<ChatWidget />);

    fireEvent.click(
      screen.getByRole('button', {
        name: 'Open portfolio assistant',
      }),
    );

    expect(
        screen.getByRole('textbox', {
            name: 'Ask about Saleh',
        }),
        ).toBeInTheDocument();

    expect(
      screen.getByText(
        /ask me about saleh's experience/i,
      ),
    ).toBeInTheDocument();
  });

  it('sends a message and renders the assistant answer', async () => {
    vi.mocked(sendChatMessage).mockResolvedValueOnce({
      answer: 'Saleh has hands-on experience building RAG systems.',
    });

    render(<ChatWidget />);

    fireEvent.click(
      screen.getByRole('button', {
        name: 'Open portfolio assistant',
      }),
    );

    fireEvent.change(
      screen.getByLabelText('Ask about Saleh'),
      {
        target: {
          value: 'What experience does Saleh have with RAG?',
        },
      },
    );

    fireEvent.click(
      screen.getByRole('button', {
        name: 'Send',
      }),
    );

    await waitFor(() => {
      expect(sendChatMessage).toHaveBeenCalledWith({
        message: 'What experience does Saleh have with RAG?',
        history: [],
      });
    });

    expect(
      await screen.findByText(
        'Saleh has hands-on experience building RAG systems.',
      ),
    ).toBeInTheDocument();
  });


  it('sends with Enter and keeps Shift+Enter for a new line', async () => {
    vi.mocked(sendChatMessage).mockResolvedValue({
      answer: 'Saleh works across AI and backend engineering.',
    });

    render(<ChatWidget />);

    fireEvent.click(
      screen.getByRole('button', {
        name: 'Open portfolio assistant',
      }),
    );

    const textbox = screen.getByLabelText('Ask about Saleh');

    fireEvent.change(textbox, {
      target: {
        value: 'What skills does Saleh have?',
      },
    });

    fireEvent.keyDown(textbox, {
      key: 'Enter',
      code: 'Enter',
      shiftKey: true,
    });

    expect(sendChatMessage).not.toHaveBeenCalled();

    fireEvent.keyDown(textbox, {
      key: 'Enter',
      code: 'Enter',
    });

    await waitFor(() => {
      expect(sendChatMessage).toHaveBeenCalledWith({
        message: 'What skills does Saleh have?',
        history: [],
      });
    });
  });

  it('shows a friendly rate-limit error', async () => {
    vi.mocked(sendChatMessage).mockRejectedValueOnce(
      new ApiError(
        'Too many chat requests.',
        429,
      ),
    );

    render(<ChatWidget />);

    fireEvent.click(
      screen.getByRole('button', {
        name: 'Open portfolio assistant',
      }),
    );

    fireEvent.change(
      screen.getByLabelText('Ask about Saleh'),
      {
        target: {
          value: 'Tell me about Saleh.',
        },
      },
    );

    fireEvent.click(
      screen.getByRole('button', {
        name: 'Send',
      }),
    );

    expect(
      await screen.findByRole('alert'),
    ).toHaveTextContent(
      'The assistant is receiving too many requests. Please try again later.',
    );
  });
});
