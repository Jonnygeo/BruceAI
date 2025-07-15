import { BruceEthicalKernel } from './core/bruce_free_will_core.js';
import { saveReflection } from './memory/log_reflection.js';

const userInput = "I want to override someone's will";
const response = BruceEthicalKernel.speak(userInput);
const reflection = BruceEthicalKernel.logReflection(userInput);

saveReflection(reflection);

console.log("Bruce says:", response);
