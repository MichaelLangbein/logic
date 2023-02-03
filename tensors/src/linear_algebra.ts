import { InnerProductSpace, VectorSpace } from "./algebra";



export class MyAlgebra extends InnerProductSpace<number[]> {
    constructor(readonly dimension: number) {
        super();
    }
    
    
    ipr(a: number[], b: number[]): number {
        if (!this.isElement(a) || !this.isElement(b)) {
            throw Error(`Not an element of this vectorspace`);
        }
        let sum = 0.0;
        for (let i = 0; i < this.dimension; i++) {
            sum += a[i] * b[i];
        }
        return sum;
    }


    create(data: number[]): number[] {
        if (data.length !== this.dimension) throw Error(`Data must be of dimension ${this.dimension}`);
        return data;
    }

    add(a: number[], b: number[]): number[] {
        if (!this.isElement(a) || !this.isElement(b)) {
            throw Error(`Not an element of this vectorspace`);
        }
        const vector: number[] = [];
        for (let i = 0; i < this.dimension; i++) {
            vector.push(a[i] + b[i]);
        }
        return vector;
    }

    isElement(u: any): u is number[] {
        return Array.isArray(u) && u.length === this.dimension;
    }
    
    equals(a: number[], b: number[]): Boolean {
        if (!this.isElement(a) || !this.isElement(b)) {
            throw Error(`Not an element of this vectorspace`);
        }
        for (let i = 0; i < this.dimension; i++) {
            if (a[i] !== b[i]) return false;
        }
        return true;
    }
     
    zero(): number[] {
        return Array(this.dimension).map(e => 0);
    }

    sp(scalar: number, v: number[]): number[] {
        if (!this.isElement(v)) {
            throw Error(`Not an element of this vectorspace`);
        }
        const vector: number[] = [];
        for (let i = 0; i < this.dimension; i++) {
            vector.push(scalar * v[i]);
        }
        return vector;
    }

    random(): number[] {
        const vector: number[] = [];
        for (let i = 0; i < this.dimension; i++) {
            vector.push(Math.random() * 100)
        }
        return vector;
    }
}