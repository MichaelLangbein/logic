export function createArray<T>(size: number, fnc: (i: number) => T): T[] {
  const out: T[] = [];
  for (let i = 0; i < size; i++) {
    out.push(fnc(i));
  }
  return out;
}
