import { Token } from "./parser";

function numericOrDot(char: string): boolean {
    return ['1', '2', '3', '4', '5', '6', '7', '8', '9', '.'].includes(char);
}

export class Tokenizer {
    tokenize(code: string): Token[] {

        const tokens: Token[] = [];
        
        let index = 0;
        while (index < code.length) {

            // whitespace
            if ([" ", "\n", "\t"].includes(code[index])) {
                index += 1;
            }

            // string
            else if (code[index] === '"') {
                index += 1;
                const stringStart = index;
                while (code[index] !== '"') {
                    index += 1;
                }
                const stringVal = code.substring(stringStart, index);
                tokens.push({ type: 'string', value: stringVal });
                index += 1;
            }

            // number
            else if (numericOrDot(code[index])) {
                let numberString = code[index];
                index += 1;
                while (numericOrDot(code[index])) {
                    numberString += code[index];
                    index += 1;
                }
                const numVal = Number(numberString);
                tokens.push({ type: 'number', value: numVal });
            }

            // boolean
            else if (code.substring(index, index + 4) === 'true') {
                tokens.push({ type: 'bool', value: true });
                index += 4;
            }
            else if (code.substring(index, index + 5) === 'false') {
                tokens.push({ type: 'bool', value: false });
                index += 5;
            }

            // brackets
            else if (code[index] === '(') {
                tokens.push({ type: '(', value: '(' });
                index += 1;
            }
            else if (code[index] === ')') {
                tokens.push({ type: ')', value: ')' });
                index += 1;
            }

            // let
            else if (code.substring(index, index + 4) === 'let ') {
                tokens.push({ type: 'let', value: 'let' });
                index += 4;
            }

            // if
            else if (code.substring(index, index + 3) === 'if ') {
                tokens.push({ type: 'if', value: 'if' });
            }

            // symbol
            else {
                let symbolString = "";
                while (code[index] !== " ") {
                    symbolString += code[index];
                    index += 1;
                }
                tokens.push({ type: 'symbol', value: symbolString });
                index += 1;
            }
        }
        tokens.push({ type: 'eof', value: 'eof' });

        return tokens;
    }
}
