import { $ } from "bun"
import Watcher from "watcher"

async function main() {
  const args = Bun.argv
  const command = args[2]
  switch (command) {
    case "run":
      break
    case undefined:
      console.log("No command provided")
      break
    default:
      console.log("Unknown command")
      break
  }
}
