

export abstract class VectorSpace<Vector> {
    abstract create(data: any): Vector
    abstract add(a: Vector, b: Vector): Vector
    abstract isElement(u: any): u is Vector
    abstract equals(a: Vector, b: Vector): Boolean
    abstract zero(): Vector
    /** scalar product */
    abstract sp(scalar: number, v: Vector): Vector
    abstract random(): Vector
}


export abstract class InnerProductSpace<Vector> extends VectorSpace<Vector> {
    /** inner product */
    abstract ipr(a: Vector, b: Vector): number;

    /** |v| */
    norm(v: Vector): number {
        return this.ipr(v, v);
    }

    orthogonal(u: Vector, v: Vector): Boolean {
        return this.ipr(u, v) === 0;
    }

    angle(u: Vector, v: Vector): number {
        const enumerator = this.ipr(u, v);
        const denominator = this.norm(u) * this.norm(v);
        const cosTheta = enumerator / denominator;
        const theta = Math.acos(cosTheta);
        return theta;
    }
}


export abstract class OuterProductSpace<Tensor> extends VectorSpace<Tensor> {
    /** outer product */
    abstract opr(a: Tensor, b: Tensor): Tensor
}

// export abstract class MatrixSpace extends OuterProductSpace {
//     /** outer product */
//     abstract opr(a: Vector, b: Vector): Matrix
// }