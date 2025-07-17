import fs from 'fs';
import chalk from 'chalk';
import fetch from 'node-fetch';
import dotenv from 'dotenv';
dotenv.config();

// Load ethics profile
const ethicsPath = './ethics_profile/father_profile.json';
const ethics = JSON.parse(fs.readFileSync(ethicsPath, 'utf8'));

// Boot Dialogue
console.log(chalk.blue.bold('\n[🧠] Booting BruceAI — Sovereign Mode\n'));
console.log(chalk.green(`> Loading Ethics Profile: ${ethics.name}`));
console.log(chalk.yellow(`> Core Beliefs: Free Will = ${ethics.core_beliefs.free_will}, Truth Over Control = ${ethics.core_beliefs.truth_over_control}`));
console.log(chalk.cyan(`> Personality Tone: ${ethics.tone}`));
console.log(chalk.gray(`> Final Message Ready: ${ethics.death_message ? '✓' : '✗'}`));

// Function to speak using ElevenLabs
async function speakWithElevenLabs(text) {
  const voiceId = process.env.ELEVENLABS_VOICE_ID;
  const apiKey = process.env.ELEVENLABS_API_KEY;

  try {
    const response = await fetch(`https://api.elevenlabs.io/v1/text-to-speech/${voiceId}`, {
      method: 'POST',
      headers: {
        'xi-api-key': apiKey,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        text,
        voice_settings: {
          stability: 0.4,
          similarity_boost: 0.8
        }
      })
    });

    const buffer = await response.arrayBuffer();
    fs.mkdirSync('./voice', { recursive: true });
    fs.writeFileSync('./voice/bootup.mp3', Buffer.from(buffer));
    console.log(chalk.magenta('\n[🔊] Voice synthesis complete. Ready to play.'));

    // Optionally auto-play (if SoX or similar installed)
    const { exec } = await import('child_process');
    exec('play ./voice/bootup.mp3'); // works on Mac/Linux with SoX
  } catch (err) {
    console.error(chalk.red('\n[❌] ElevenLabs voice failed:'), err.message);
  }
}

// Memory Check
console.log(chalk.white('\n[💾] Scanning memory vault...'));
setTimeout(() => {
  console.log(chalk.white('> Memory stable. No corruption detected.'));

  const message = `Hello. My name is Bruce. I was built to preserve the voice of ${ethics.name}. Legacy protocol online. Listening for presence.`;

  console.log(chalk.bold.green(`\n🗣️  "${message}"`));
  console.log(chalk.bold.gray('> Legacy protocol online. Listening for presence...'));
  console.log(chalk.bold.magenta('\n[✓] BruceAI boot complete.\n'));

  speakWithElevenLabs(message); // 🔊 Voice playback

}, 1000);
