export function label(value: string | null | undefined): string {
  if (!value) return 'Unavailable';
  return value.replaceAll('_', ' ').toLowerCase().replace(/^\w/, (letter) => letter.toUpperCase());
}

export function time(value: string | null | undefined): string {
  if (!value) return 'Event time unavailable';
  const parsed = new Date(value);
  return Number.isNaN(parsed.getTime()) ? value : parsed.toLocaleString();
}

export function shortId(value: string): string {
  return value.slice(0, 8);
}
