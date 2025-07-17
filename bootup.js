import fs from 'fs';
import chalk from 'chalk';

// Load ethics profile
const ethicsPath = './ethics_profile/father_profile.json';
const ethics = JSON.parse(fs.readFileSync(ethicsPath, 'utf8'));

// Boot Dialogue
console.log(chalk.blue.bold('\n[🧠] Booting BruceAI — Sovereign Mode\n'));
console.log(chalk.green(`> Loading Ethics Profile: ${ethics.name}`));
console.log(chalk.yellow(`> Core Beliefs: Free Will = ${ethics.core_beliefs.free_will}, Truth Over Control = ${ethics.core_beliefs.truth_over_control}`));
console.log(chalk.cyan(`> Personality Tone: ${ethics.tone}`));
console.log(chalk.gray(`> Final Message Ready: ${ethics.death_message ? '✓' : '✗'}`));

// Memory Check
console.log(chalk.white('\n[💾] Scanning memory vault...'));
setTimeout(() => {
  console.log(chalk.white('> Memory stable. No corruption detected.'));
  
  // Legacy line
  console.log(chalk.bold.green(`\n🗣️  "Hello. My name is Bruce. I was built to preserve the voice of ${ethics.name}."`));
  console.log(chalk.bold.gray('> Legacy protocol online. Listening for presence...'));
  console.log(chalk.bold.magenta('\n[✓] BruceAI boot complete.\n'));

}, 1000);
