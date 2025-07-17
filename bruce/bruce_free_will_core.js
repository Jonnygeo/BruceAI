import fs from 'fs';
import path from 'path';

// 🔁 Load a legacy poem from the memory vault
export function getLegacyPoem(id) {
  const filePath = path.join(process.cwd(), `bruce/core/legacy/${id}.json`);
  try {
    const data = JSON.parse(fs.readFileSync(filePath, 'utf8'));
    return `🕊️ ${data.title} — by ${data.author}\n\n${data.content.join('\n')}`;
  } catch (err) {
    return `⚠️ Legacy poem "${id}" not found or failed to load.`;
  }
}
