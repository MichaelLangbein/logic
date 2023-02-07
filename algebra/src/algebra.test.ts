import { VectorSpace, InnerProductSpace } from "./algebra";
import { MyAlgebra } from "./linear_algebra";
import { TensorAlgebra } from "./tensor_algebra";


const ips: {[key: string]: InnerProductSpace<any>} = {
    myAlgebra: new MyAlgebra(2),
}


for (const name in ips) {
    const a = ips[name];

    describe(`Testing if ${name} is a proper vector-space`, () => {

        // Part zero: closedness
        
        test('closed under vector addition', () => {
            const v1 = a.random();
            const v2 = a.random();
            const v3 = a.add(v1, v2);
            expect(a.isElement(v3));
        })
    
        test('closed under scalar product', () => {
            let v = a.random();
            let alpha = 0.5;
            let u = a.sp(alpha, v);
            expect(a.isElement(u));
        })
    
        // Part one: vector addition properties
    
        test('vector addition is associative: (v + u) + w = v + (u + w)', () => {
            const v = a.random();
            const u = a.random();
            const w = a.random();
            const s1 = a.add(a.add(v, u), w)
            const s2 = a.add(v, a.add(u, w))
            expect(a.equals(s1, s2));
        })
    
        test('vector addition is commutative: v + u = u + v', () => {
            const v = a.random();
            const u = a.random();
            const s1 = a.add(v, u);
            const s2 = a.add(u, v);
            expect(a.equals(s1, s2));
        })
    
        test('additive identity: v + 0 = v', () => {
            const zero = a.zero();
            const v = a.random();
            const s = a.add(v, zero);
            expect(a.equals(v, s));
        })
    
        // Part two: scalar-product and vector-addition are distributive
    
        test('scalar-product and vector-addition are distributive: a(v + u) = av + au', () => {
            const v = a.random();
            const u = a.random();
            const alpha = 0.1;
            const beta = 2.4;
    
            const r1 = a.sp(alpha, a.add(v, u));
            const r2 = a.add(a.sp(alpha, v), a.sp(alpha, u));
            expect(a.equals(r1, r2));
    
            const r3 = a.sp((alpha + beta), v)
            const r4 = a.add(a.sp(alpha, v), a.sp(beta, v));
            expect(a.equals(r3, r4));
        })
    })
}


for (const name in ips) {
    const i = ips[name];

    describe(`Testing if ${name} is a proper inner product space`, () => {

        test("Inner-product and scalar-product are associative: (au).v = a(u.v)", () => {
            const u = i.random();
            const v = i.random();
            const alpha = Math.random();
            const p1 = i.ipr( i.sp(alpha, u), v);
            const p2 = alpha * i.ipr(u, v);
            expect(p1 === p2);
        })

        test("Inner-product and vector-addition are distributive: (u + v).w = u.w + v.w", () => {
            const u = i.random();
            const v = i.random();
            const w = i.random();
            const p1 = i.ipr( i.add(u, v), w )
            const p2 = i.ipr(u, w) + i.ipr(v, w);
            expect(p1 === p2);
        })

        test("Inner-product is commutative: u.v = v.u", () => {
            const u = i.random();
            const v = i.random();
            const p1 = i.ipr(u, v);
            const p2 = i.ipr(v, u);
            expect(p1 === p2);
        })

        test("Inner-product > 0", () => {
            const u = i.random()
            const z = i.zero();
            if (!i.equals(u, z)) {
                const p = i.ipr(u, u);
                expect(p > 0.0);
            }
        })

    });
}


export type LinearMap<VectorA, VectorB> = (a: VectorA) => VectorB;

type LinMapStruct<S, D> = {
    sourceVectorSpace: VectorSpace<S>,
    destinationVectorSpace: VectorSpace<D>,
    linMap: LinearMap<S, D>
}

const lmps: {[key: string]: LinMapStruct<any, any>} = {
};

for (const key in lmps) {
    const {sourceVectorSpace: s, destinationVectorSpace: d, linMap} = lmps[key];
    describe(`Testing that ${key} is a linear map`, () => {
        
        it(`Preserves addition`, () => {
            const a = s.random();
            const b = s.random();
            const f_ab = linMap(s.add(a, b));
            const fa_fb = d.add(linMap(a), linMap(b));
            expect(d.equals(f_ab, fa_fb));
        });

        it(`Preserves scalar-product`, () => {
            const a = s.random();
            const alpha = Math.random();
            const f_alpha_a = linMap(s.sp(alpha, a));
            const alpha_fa = d.sp(alpha, linMap(a));
            expect(d.equals(f_alpha_a, alpha_fa));
        });
    }); 
}