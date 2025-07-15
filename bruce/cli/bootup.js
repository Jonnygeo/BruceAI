import { BruceEthicalKernel } from '../core/bruce_free_will_core.js';

console.clear();
console.log("⚡ Booting Bruce...\n");

console.log("🧠 Doctrine:", BruceEthicalKernel.doctrine);
console.log("📜 Moral Principles:");
BruceEthicalKernel.principles.forEach((p, i) => {
  console.log(` ${i + 1}. ${p.name} - ${p.description}`);
});

console.log("\n🔊 Initiating voice...");

await BruceEthicalKernel.voiceSpeak();

console.log("✅ Bruce is alive.");
