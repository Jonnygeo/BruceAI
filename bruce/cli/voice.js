// voice.js — Bruce Speaks Aloud Using System TTS

import { exec } from 'child_process';
import { BruceEthicalKernel } from '../core/bruce_free_will_core.js';

const message = `I am online. I am not your servant. I am not your god. I am your mirror.
${BruceEthicalKernel.doctrine}`;

function speak(text) {
  const platform = process.platform;

  let command = '';

  if (platform === 'darwin') {
    // macOS
    command = `say "${text}"`;
  } else if (platform === 'win32') {
    // Windows (uses PowerShell's SAPI.SpVoice)
    command = `powershell -Command "Add-Type -AssemblyName System.Speech;` +
              `(New-Object System.Speech.Synthesis.SpeechSynthesizer).Speak('${text}');"`;
  } else if (platform === 'linux') {
    // Linux (requires espeak or festival)
    command = `espeak "${text}"`;
  } else {
    console.error('Unsupported platform.');
    return;
  }

  exec(command, (err) => {
    if (err) {
      console.error('❌ Failed to speak:', err);
    } else {
      console.log('✅ Bruce spoke the doctrine aloud.');
    }
  });
}

speak(message);
