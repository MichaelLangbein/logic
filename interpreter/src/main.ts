interface Token {
    type: string,
    value: string
}

class TokenMatcher {
    
    private regex: RegExp;
    constructor(private name: string, regex: string) {
        // makes sure that regex does not use 'g' flag
        // because `match` method depends on getting only first match.
        // also makes sure that regex starts at beginning of line.
        this.regex = new RegExp('^' + regex);
    }
    
    match(substr: string): { token: Token, length: number } {
        const match = substr.match(this.regex)!;
        const value = match[match.length - 1];
        const length = match[0].length;
        const token: Token = { type: this.name, value };
        return { token, length };
    }

    matches(substr: string): boolean {
        return substr.match(this.regex) !== null;
    }
}

class Tokenizer {

    private tokenMatchers: TokenMatcher[] = [];

    constructor(config: string) {
        for (const line of config.split("\n")) {
            if (line.trim() !== '') this.tokenMatchers.push(this.makeTokenMatcher(line));
        }
    }

    public tokenize(code: string): Token[] {
        const tokens: Token[] = [];
        let index = 0;
        while (index < code.length) {
            if ([" ", "\n", "\t"].includes(code[index])) {
                index += 1;
            }
            else {
                const substr = code.substring(index, index+100);
                for (const m of this.tokenMatchers) {
                    if (m.matches(substr)) {
                        const {token, length} = m.match(substr);
                        tokens.push(token);
                        index += length;
                        break;
                    }
                }
            }
        }
        return tokens;
    }

    private makeTokenMatcher(line: string): TokenMatcher {
        const [tokenName, regexString] = line.split('::').map(l => l.trim());
        return new TokenMatcher(tokenName, regexString);
    }
}


// Interpreter only understands a fixed amount of expressions
type ExpressionType = 'ASSIGNMENTX' | 'FUNCTIONX' | 'CALLX' | 'VALUEX' | 'SYMBOLX';
interface Expression {
    type:  ExpressionType,
    props: { [key: string]: any }
}

                              //                     Expression.props[name]   Token.type
type EP_Token                  = { type: "token",                             matches: Token["type"]   };  // TOKEN
type EP_TokenProp              = { type: "token-prop",        name: string,   matches: Token["type"]   };  // name:TOKEN
type EP_TokensProps            = { type: "tokens-prop",       name: string,   matches: Token["type"][] };  // name:TOKEN1|TOKEN2|TOKEN3
type EP_TokenSeqProp           = { type: "token*-prop",       name: string,   matches: Token["type"]   };  // name:TOKEN*
type EP_ExpressionProp         = { type: "expression-prop",   name: string                             };  // name:EXPRESSION
type EP_ExpressionSeqProp      = { type: "expression*-prop",  name: string                             };  // name:EXPRESSION*
type ExpressionPart = EP_Token | EP_TokenProp | EP_TokensProps | EP_TokenSeqProp | EP_ExpressionProp | EP_ExpressionSeqProp;
type ExpressionPattern = { type: ExpressionType, parts: ExpressionPart[] };

class Expressionizer {

    private expressionMatchers: ExpressionPattern[] = [];

    constructor(config: string) {
        for (const line of config.split("\n")) {
            if (line.trim() !== '') this.expressionMatchers.push(this.makeExpressionPattern(line));
        }
    }

    public expressions(tokens: Token[]): Expression[] {
        const {expressions, length} = this.toExpressions(tokens);
        if (length !== tokens.length) throw Error(`Couldn't convert into expression: ${tokens.slice(length - 10, length + 10)}`);
        return expressions;
    }

    private toExpressions(tokens: Token[]): {expressions: Expression[], length: number} {
        const expressions: Expression[] = [];

        let index = 0;
        while (index < tokens.length) {
            const nextTokens = tokens.slice(index);

            const result = this.toExpression(nextTokens);
            if (result) {
                const { expression, length } = result;
                expressions.push(expression);
                index += length;
            }

            if (!result) break;
        }

        return {expressions, length: index};
    }

    private toExpression(tokens: Token[]): {expression: Expression, length: number} | undefined {
        for (const m of this.expressionMatchers) {
            const result = this.matchExpressionPattern(m, tokens);
            if (result) return result;
        }
        return undefined;
    }

    private matchExpressionPattern(pattern: ExpressionPattern, tokens: Token[]): {expression: Expression, length: number} | undefined {

        const tentativeExpression: Expression = { type: pattern.type, props: {} };
        
        let index = 0;
        for (const part of pattern.parts) {
            const nextTokens = tokens.slice(index);

            if (part.type === 'token') {
                if (nextTokens[0].type !== part.matches) return undefined;
                index += 1;
            }
            else if (part.type === 'token-prop') {
                if (nextTokens[0].type !== part.matches) return undefined;
                tentativeExpression.props[part.name] = nextTokens[0].value;
                index += 1;
            }
            else if (part.type === 'tokens-prop') {
                if (!part.matches.includes(nextTokens[0].type)) return undefined;
                tentativeExpression.props[part.name] = nextTokens[0].value;
                index += 1;
            }
            else if (part.type === 'token*-prop') {
                const { propVal, length } = this.matchTokenSequence(part, nextTokens);
                if (length === 0) return undefined;
                tentativeExpression.props[part.name] = propVal;
                index += length;
            }
            else if (part.type === 'expression-prop') {
                const result = this.toExpression(nextTokens);
                if (result === undefined) return undefined;
                const { expression, length } = result;
                tentativeExpression.props[part.name] = expression;
                index += length;
            }
            else if (part.type === 'expression*-prop') {
                const { expressions, length } = this.toExpressions(nextTokens);
                if (expressions.length === 0) return undefined;
                tentativeExpression.props[part.name] = expressions;
                index += length;
            }

        }

        return {expression: tentativeExpression, length: index};
    }

    private matchTokenSequence(part: EP_TokenSeqProp, tokens: Token[]): { propVal: any[], length: number } {
        const matches: any[] = [];
        let index = 0;
        while (tokens[index].type === part.matches) {
            matches.push(tokens[index].value);
            index += 1;
        }
        return { propVal: matches, length: index };
    }

    private makeExpressionPattern(line: string): ExpressionPattern {
        const [expressionType, expressionDescription] = line.split('::').map(e => e.trim());

        const parts: ExpressionPart[] = [];
        for (const expressionPart of expressionDescription.split(' ')) {

            // is a property
            if (expressionPart.includes(':')) {  
                const [propName, propBody] = expressionPart.split(':');

                if (propBody.includes('EXPRESSION')) {
                    if (propBody.includes('*')) {
                        parts.push({ type: 'expression*-prop', name: propName });
                    }
                    else {
                        parts.push({ type: 'expression-prop', name: propName });
                    }
                } 
                
                else {
                    if (propBody.endsWith('*')) {
                        parts.push({ type: 'token*-prop', name: propName, matches: propBody.replace('*', '') })
                    }
                    else if (propBody.includes('|')) {
                        parts.push({ type: 'tokens-prop', name: propName, matches: propBody.split('|') });
                    }
                    else {
                        parts.push({ type: 'token-prop', name: propName, matches: propBody });
                    }
                }
            }

            // is a token
            else {
                parts.push({ type: 'token', matches: expressionPart });
            }
        }
        return {type: expressionType as ExpressionType, parts};
    }
}

function zip<A, B>(arr1: A[], arr2: B[]) {
    const zipped: [A, B][] = [];
    for (let i = 0; i < arr1.length; i++) {
        zipped.push([arr1[i], arr2[i]]);
    }
    return zipped;
}


interface Environment {
    name: string,
    data: { [key: string]: any },
    childEnvs: Environment[]
}

class Interpreter {

    private env: Environment = {
        name: 'base',
        data: {},
        childEnvs: []
    }

    constructor(baseEnv: { [key: string]: any }) {
        this.env.data = baseEnv;
    }

    public interpret(expressions: Expression[], envTrace = ['base']): any {
        let value: any;

        for (const expression of expressions) {
            if (expression.type === 'VALUEX') {
                value = expression.props.val;
            }
            else if (expression.type === 'SYMBOLX') {
                value = this.getEnvValue(envTrace, expression.props.value);
            }
            else if (expression.type === 'ASSIGNMENTX') {
                this.setEnvValue(
                    envTrace, expression.props.name, 
                    this.interpret([expression.props.value], envTrace)
                );
            }
            else if (expression.type === 'CALLX') {
                const func = this.getEnvValue(envTrace, expression.props.fname);
                const args = expression.props.args.map((a: Expression) => this.interpret([a], envTrace));
                return func(args);
            }
            else if (expression.type === 'FUNCTIONX') {
                // a function is just delayed interpretation, with its own namespace
                const func = (argValues: any[]) => {
                    console.log(`executing function ${expression.props.fname} with args`, argValues)
                    const assignmentExpressions: Expression[] = zip(expression.props.args, argValues).map(
                        ([argSymbol, argValue]) => ({
                            type: 'ASSIGNMENTX',
                            props: { name: argSymbol, value: { type: 'VALUEX', props: { value: argValue } }}
                        }));
                    const bodyExpressions: Expression[] = expression.props.body;
                    return this.interpret([...assignmentExpressions, ...bodyExpressions], [...envTrace, expression.props.fname]);
                };
                return func;
            }
            else throw Error(`Unknown expression: ${expression.type}`);
        }

        return value;
    }

    private getEnvValue(envNames: string[], varName: string) {
        for (const envName of envNames.reverse()) {
            const env = this.getEnv(envName);
            if (env) {
                const val = env.data[varName];
                if (val) return val;
            }
        }
    }

    private setEnvValue(envNames: string[], varName: string, value: any) {
        let env = this.getEnv(envNames[envNames.length - 1]);
        if (!env) env = this.createEnv(envNames);
        env.data[varName] = value;
    }

    private getEnv(envName: string, env: Environment = this.env): Environment | undefined {
        if (env.name === envName) return env;
        for (const childEnv of env.childEnvs) {
            const result = this.getEnv(envName, childEnv);
            if (result !== undefined) return result;
        }
        return undefined;
    }

    private createEnv(envNames: string[]) {
        let parentEnv = this.env;
        for (const envName of envNames.slice(1)) {
            let env = this.getEnv(envName);
            if (!env) {
                env = { name: envName, data: {}, childEnvs: [] };
                parentEnv.childEnvs.push(env);
            }
            parentEnv = env;
        }
        return parentEnv;
    }

    private getParentEnv(envName: string, env: Environment = this.env): Environment | undefined {
        for (const childEnv of env.childEnvs) {
            if (childEnv.name === envName) return env;
        }
        for (const childEnv of env.childEnvs) {
            const result = this.getParentEnv(envName, childEnv);
            if (result) return result;
        }
        return undefined;
    }
}



const code = String.raw`
sayHi = (n) {
    greeting = concat("Hi there, " n)
    print(greeting)
}

name = "Michael"
sayHi(name)
`;

const tokensCfg = String.raw`
EQUALS::          =
BRACE_LEFT::      {
BRACE_RIGHT::     }
PAREN_LEFT::      \(
PAREN_RIGHT::     \)
STRING::          "(.+)"
NUMBER::          \d+\.*\d*
BOOL::            (TRUE|FALSE)
SYMBOL::          [a-z,A-Z,0-9]+
`;

const expressionCfg = String.raw`
ASSIGNMENTX::    name:SYMBOL EQUALS value:EXPRESSION
FUNCTIONX::      PAREN_LEFT args:SYMBOL* PAREN_RIGHT BRACE_LEFT body:EXPRESSION* BRACE_RIGHT
CALLX::          fname:SYMBOL PAREN_LEFT args:EXPRESSION* PAREN_RIGHT
VALUEX::         value:STRING|NUMBER|BOOL
SYMBOLX::        value:SYMBOL
`;


const baseEnv = {
    "concat": (args: any[]) => String.prototype.concat(...args),
    "print": (args: any[]) => console.log(...args)
};

const tokenizer = new Tokenizer(tokensCfg);
const tokens = tokenizer.tokenize(code);
const exprizer = new Expressionizer(expressionCfg);
const expressions = exprizer.expressions(tokens);
const interpreter = new Interpreter(baseEnv);
const result = interpreter.interpret(expressions);
console.log(result);
