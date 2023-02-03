import { VectorSpace } from "./algebra";

export class TensorAlgebra implements VectorSpace<any> {
    create(data: any) {
        throw new Error("Method not implemented.");
    }
    add(a: any, b: any) {
        throw new Error("Method not implemented.");
    }
    isElement(u: any): u is any {
        throw new Error("Method not implemented.");
    }
    equals(a: any, b: any): Boolean {
        throw new Error("Method not implemented.");
    }
    zero() {
        throw new Error("Method not implemented.");
    }
    sp(scalar: number, v: any) {
        throw new Error("Method not implemented.");
    }
    random() {
        throw new Error("Method not implemented.");
    }


}