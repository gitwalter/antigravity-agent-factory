import yaml from 'js-yaml';

/**
 * Utility to parse markdown files with YAML frontmatter.
 */
export function parseFrontmatter(content: string) {
  if (!content.startsWith('---\n')) {
    return { data: {}, content };
  }

  const parts = content.split('---\n');
  if (parts.length < 3) {
    return { data: {}, content };
  }

  try {
    const data = yaml.load(parts[1]) as Record<string, any>;
    const body = parts.slice(2).join('---\n');
    return { data: data || {}, content: body };
  } catch (e) {
    console.error('Failed to parse YAML frontmatter', e);
    return { data: { error: 'Invalid YAML' }, content };
  }
}

/**
 * Utility to stringify data back to frontmatter + markdown.
 */
export function stringifyFrontmatter(data: Record<string, any>, content: string) {
  const frontmatter = yaml.dump(data);
  return `---\n${frontmatter}---\n${content}`;
}
