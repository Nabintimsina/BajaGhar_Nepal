export function toNepaliDigits(value) {
  const map = ['०','१','२','३','४','५','६','७','८','९']
  const s = String(value)
  return s.replace(/[0-9]/g, (d) => map[Number(d)])
}

export function formatCountForLocale(value, locale) {
  if (locale && locale.toString().toLowerCase().startsWith('ne')) {
    return toNepaliDigits(value)
  }
  return String(value)
}
