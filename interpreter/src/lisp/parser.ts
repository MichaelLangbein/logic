import { CallableExpression, Expression, SymbolExpression, ValueExpression, IfExpression, LetExpression } from "./interpreter";

export type TokenType = 'string' | 'number' | 'bool' | 'symbol' | '(' | ')' | 'let' | 'if' | 'eof';

export interface Token {
    type: TokenType,
    value: string | number | boolean
}

export class Parser {

    parse(tokens: Token[]): Expression[] {
        const expressions: Expression[] = [];

        let index = 0;

        while (index < tokens.length) {
            if (tokens[index].type === 'eof') return expressions;

            if (tokens[index].type === 'number' || tokens[index].type === 'string' || tokens[index].type === 'bool') {
                expressions.push(new ValueExpression(tokens[index].value));
                index += 1;
            }
    
            else if (tokens[index].type === 'symbol') {
                expressions.push(new SymbolExpression(tokens[index].value as string));
                index += 1;
            }

            else if (tokens[index].type === '(') {
                const tokensInsideBrackets: Token[] = [];
                let open = 1;
                while (open > 0) {
                    index += 1;
                    if      (tokens[index].type === '(') open += 1;
                    else if (tokens[index].type === ')') open -= 1;
                    else tokensInsideBrackets.push(tokens[index]);
                }

                const expressionsInsideBrackets = this.parse(tokensInsideBrackets);
                const firstExpression = expressionsInsideBrackets.shift();

                if (firstExpression instanceof SymbolExpression) {
                    expressions.push(new CallableExpression(
                        firstExpression, expressionsInsideBrackets
                    ));
                }

                index += 1;
            }
        }

        return expressions;
    }
}

// const tokens: Token[] = [
//     { type: 'string', value: "Hi, mom!" },

//     { type: '(',        value: '('   },
//     { type: 'symbol',   value: '+'   },
//     { type: 'number',   value: 1     },
//     { type: 'number',   value: 2     },
//     { type: ')' ,       value: ')'   },

//     { type: 'eof', value: 'eof' }
// ];