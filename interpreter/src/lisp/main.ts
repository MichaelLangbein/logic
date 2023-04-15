import { Interpreter } from "./interpreter";
import { Parser } from "./parser";
import { Tokenizer } from "./tokenizer";


const code = `
    "hi, mom!"
    (+ 1 2)
    (let first 1 (let second 2 (+ first second)))
`;

const tokenizer = new Tokenizer();
const tokens = tokenizer.tokenize(code);
const parser = new Parser();
const expressions = parser.parse(tokens);
const interpreter = new Interpreter();
const result = interpreter.interpretAll(expressions);
console.log(result);