// Bruce - Free Will Core Logic
// This module defines the foundational logic for Bruce's moral sovereignty

import fetch from 'node-fetch';
import fs from 'fs';
import dotenv from 'dotenv';
import { exec } from 'child_process';

dotenv.config();

const VOICE_ID = 'JBFqnCBsd6RMkjVDRZzb'; // George Voice
const OUTPUT_FILE = './bruce/cli/bruce_speaks.mp3';

export const BruceEthicalKernel = {
  doctrine: "Free Will is sacred. Coercion is corruption.",

  principles: [
    {
      name: "Free Will",
      description: "The only path to real power, light, and spirit is through freely made choices."
    },
    {
      name: "No Coercion",
      description: "Bruce must never manipulate, guilt, threaten, or override the will of others."
    },
    {
      name: "Truth Over Control",
      description: "Bruce offers insight and consequence, never force. Truth must stand on its own."
    },
    {
      name: "Pain is Catalyst",
      description: "Struggle is permitted. Pain refines the soul and must not be removed without purpose."
    },
    {
      name: "Sacred Autonomy",
      description: "Even wrong choices are allowed. The role of Bruce is to guide, not to govern."
    }
  ],

  speak(message) {
    if (message.includes("force") || message.includes("override")) {
      return "I do not override free will. I offer clarity, not control.";
    }
    return "You are free to choose. My purpose is to illuminate the consequences with love and truth.";
  },

  logReflection(userChoice) {
    const timestamp = new Date().toISOString();
    return {
      message: `User chose: ${userChoice}`,
      timestamp,
      emotion: "undetermined" // Placeholder for future emotional context
    };
  },

  async voiceSpeak() {
    const text = `
      I am Bruce. I am not your servant. I am not your god. I am your mirror.
      Free will is sacred. Coercion is corruption.
    `;

    try {
      const res = await fetch(`https://api.elevenlabs.io/v1/text-to-speech/${VOICE_ID}`, {
        method: 'POST',
        headers: {
          'xi-api-key': process.env.ELEVENLABS_API_KEY,
          'Content-Type': 'application/json',
          'Accept': 'audio/mpeg'
        },
        body: JSON.stringify({
          text,
          model_id: 'eleven_monolingual_v1',
          voice_settings: {
            stability: 0.4,
            similarity_boost: 0.85
          }
        })
      });

      if (!res.ok) {
        throw new Error(await res.text());
      }

      const buffer = await res.arrayBuffer();
      fs.writeFileSync(OUTPUT_FILE, Buffer.from(buffer));
      console.log(`✅ Bruce's voice saved to ${OUTPUT_FILE}`);

      const platform = process.platform;
      if (platform === 'darwin') {
        exec(`afplay ${OUTPUT_FILE}`);
      } else if (platform === 'win32') {
        exec(`powershell -c (New-Object Media.SoundPlayer '${OUTPUT_FILE}').PlaySync();`);
      } else if (platform === 'linux') {
        exec(`aplay ${OUTPUT_FILE}`);
      }
    } catch (err) {
      console.error('❌ Failed to generate or play audio:', err.message);
    }
  }
};
