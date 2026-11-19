const assert = require("assert");
const { greet } = require("./index");

assert.strictEqual(greet("HSIW"), "Hello, HSIW!");
assert.strictEqual(greet(), "Hello, World!");
console.log("All JS tests pass.");
