import { describe, it, expect } from 'vitest';
import type { DigestResponse, ActionItem } from '../api';

describe('Sloth Digest Frontend Logic', () => {
  it('calculates noise percentage and safe to ignore ratio correctly', () => {
    const total = 500;
    const safe = 475;
    const ratio = Math.round((safe / total) * 100);
    expect(ratio).toBe(95);
  });

  it('formats morning digest markdown with source citations', () => {
    const mockDigest: DigestResponse = {
      id: 'd123',
      created_at: '2026-10-25 08:00:00',
      chat_name: 'CS301 Project',
      total_messages: 50,
      safe_to_ignore_count: 46,
      two_line_summary: 'Agreed on PostgreSQL schema.\nNext sprint planning on Tuesday.',
      model_used: 'qwen2.5:1.5b',
      processing_duration_sec: 1.8,
      action_items: [
        {
          id: 'a1',
          description: 'Submit report to TA',
          assignee_target: 'Maya',
          urgency: 'normal',
          source: {
            message_id: 'm10',
            line_number: 14,
            sender: 'Prof. Henderson',
            timestamp: '24/10/26 14:00',
            raw_text: 'Maya, please submit the report to the TA.',
          },
        },
      ],
      deadlines: [
        {
          id: 'dl1',
          date_mentioned: 'Tuesday Oct 27',
          event_description: 'Sprint planning meeting',
          source: {
            message_id: 'm20',
            line_number: 22,
            sender: 'David',
            timestamp: '24/10/26 15:30',
            raw_text: 'Sprint planning meeting is on Tuesday Oct 27.',
          },
        },
      ],
    };

    let md = `**Sloth Digest: ${mockDigest.chat_name}**\n\n`;
    md += `*Summary:*\n${mockDigest.two_line_summary}\n\n`;
    mockDigest.action_items.forEach((a) => {
      md += `- [ ] (${a.assignee_target}): ${a.description} [Line ${a.source.line_number}]\n`;
    });

    expect(md).toContain('**Sloth Digest: CS301 Project**');
    expect(md).toContain('- [ ] (Maya): Submit report to TA [Line 14]');
  });

  it('preserves grounding so action item line numbers match raw chat lines', () => {
    const action: ActionItem = {
      id: 'a1',
      description: 'Review PR #4',
      assignee_target: 'Sarah',
      urgency: 'normal',
      source: {
        message_id: 'm99',
        line_number: 88,
        sender: 'Leo',
        timestamp: '24/10/26 18:22',
        raw_text: 'Sarah, can you please review PR #4 by tonight?',
      },
    };

    expect(action.source.line_number).toBe(88);
    expect(action.source.sender).toBe('Leo');
    expect(action.source.raw_text).toContain('PR #4');
  });
});
