export class RuntimeError extends Error {}


export class Interpreter {

    private env: Map<string, any> = new Map(Object.entries({
        '+': (a: any, b: any) => a + b
    }));

    public interpretAll(expressions: Expression[]) {
        let result;
        for (const expression of expressions) {
            result = this.interpret(expression, this.env);
        }
        return result;
    }

    private interpret(expression: Expression, env: Map<string, any>): any {

        if (expression instanceof ValueExpression) {
            return expression.value;
        }

        if (expression instanceof SymbolExpression) {
            if (this.env.has(expression.symbol)) {
                return this.env.get(expression.symbol);
            } else {
                throw new RuntimeError(`Unknown symbol: ${expression.symbol}`);
            }         
        }

        if (expression instanceof IfExpression) {
            const conditionValue = this.interpret(expression.condition, env);
            if (conditionValue) {
                return this.interpret(expression.consequence, env);
            } else {
                if (!expression.alternative) return undefined;
                return this.interpret(expression.alternative, env);
            }
        }

        if (expression instanceof LetExpression) {
            const newVarVal = this.interpret(expression.val, this.env);
            const newEnv = this.env;
            newEnv.set(expression.name, newVarVal);
            const result = this.interpret(expression.body, newEnv);
            newEnv.delete(expression.name);
            return result;
        }

        if (expression instanceof CallableExpression) {
            const func = this.interpret(expression.operator, this.env);
            if (func instanceof Function) {
                const argVals = expression.args.map(a => this.interpret(a, this.env));
                return func(...argVals);
            } else {
                throw new RuntimeError(`Not callable: ${func}`);
            }
        }

        throw new RuntimeError(`Unknown expression: ${expression}`);
    }
}


export interface Expression {}

export class ValueExpression implements Expression {
    constructor(readonly value: any) {}
}

export class SymbolExpression implements Expression {
    constructor(readonly symbol: string) {}
}

export class IfExpression implements Expression {
    constructor(readonly condition: Expression, readonly consequence: Expression, readonly alternative?: Expression) {}
}

export class LetExpression implements Expression {
    constructor(readonly name: string, readonly val: Expression, readonly body: Expression) {}
}

export class CallableExpression implements Expression {
    constructor(readonly operator: Expression, readonly args: Expression[]) {}
}


// const expressions: Expression[] = [
    
//     new ValueExpression(3),
    
//     new IfExpression(
//         new ValueExpression(false),
//         new ValueExpression(1),
//         new ValueExpression(2)
//     ),

//     new IfExpression(
//         new IfExpression(
//             new ValueExpression(true),
//             new ValueExpression(true),
//             new ValueExpression(2)
//         ),
//         new ValueExpression(1),
//         new ValueExpression(2)
//     ),

//     new LetExpression(
//         'myVar', new ValueExpression(123),
//         new SymbolExpression('myVar')
//     ),

//     new LetExpression(
//         'cond', new ValueExpression(false),
//         new IfExpression(
//             new SymbolExpression('cond'),
//             new ValueExpression("cond has evaluated to true"),
//             new ValueExpression("cond has evaluated to false"),
//         )
//     ),

//     new CallableExpression(
//         new SymbolExpression('+'),
//         [
//             new ValueExpression(1),
//             new ValueExpression(2)
//         ]
//     ),
// ];

// const interpreter = new Interpreter();
// const result = interpreter.interpretAll(expressions);
// console.log(result);