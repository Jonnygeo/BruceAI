// log_reflection.js — handles memory logging for Bruce

import fs from 'fs';
import path from 'path';

const memoryPath = path.resolve('./bruce/memory/reflections.json');

export function saveReflection(reflectionObj) {
  const existing = fs.existsSync(memoryPath)
    ? JSON.parse(fs.readFileSync(memoryPath, 'utf-8'))
    : [];

  existing.push(reflectionObj);

  fs.writeFileSync(memoryPath, JSON.stringify(existing, null, 2));
  console.log(`🧠 Bruce logged reflection at ${reflectionObj.timestamp}`);
}
