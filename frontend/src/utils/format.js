/**
 * Data formatting and compliance hints for frontend.
 */
export function formatPlayCount(n) {
  if (n == null) return '—';
  if (n >= 1e8) return (n / 1e8).toFixed(1) + '亿';
  if (n >= 1e4) return (n / 1e4).toFixed(1) + '万';
  return String(n);
}

export function complianceHint(field) {
  const hints = {
    title: '请勿使用违规或敏感词',
    description: '描述需符合平台规范',
  };
  return hints[field] || '';
}
