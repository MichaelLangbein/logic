/**
 * Control app navigation with chat-interface.
 *
 * 1. user input: "I want to see the damage on buildings"
 * 2. bert (`matchUserInputWithState`) translates input to state: state = {screen: map, step: 4-damage}
 * 3. `shortestPath` finds sequence of actions (a "path") to get from current to target state: ["go to peru", "select epicenter", "execute eq", "load exposure", "calculate damage"]
 * 4. ui verifies with user if those are the right steps and the target state is the desired state
 * 5. ui executes all those steps while user watches
 */

interface State {}

function statesEqual(s1: State, s2: State): boolean {}

interface Action {}

type Path = Action[];

class FiniteStateMachine {
  constructor(state: State) {}

  getAllActions(): Action[] {
    throw new Error('Method not implemented.');
  }

  execute(action: Action): State {
    throw new Error('Method not implemented.');
  }

  executeAll(actions: Path): State {
    throw new Error('Method not implemented.');
  }
}

function matchUserInputWithState(userInput: string): State {
  throw new Error('Function not implemented.');
}

function shortestPath(initialState: State, targetState: State): Path | undefined {
  /** a bfs going through state-machine. may not halt! */

  if (statesEqual(initialState, targetState)) return [];

  const fsm = new FiniteStateMachine(initialState);
  const candidatePaths: Path[] = fsm.getAllActions().map((a) => [a]);

  while (candidatePaths.length > 0) {
    const fsm = new FiniteStateMachine(initialState);
    const candidatePath = candidatePaths.shift()!;
    const newState = fsm.executeAll(candidatePath);
    if (statesEqual(newState, targetState)) return candidatePath;
    const actionsFromHere = fsm.getAllActions();
    const newCandidatePaths = appendHeadsToPath(candidatePath, actionsFromHere);
    candidatePaths.push(...newCandidatePaths);
  }

  return undefined;
}

function appendHeadsToPath(path: Path, heads: Action[]): Path[] {
  const out = [];
  for (const head of heads) {
    out.push([...path, head]);
  }
  return out;
}

// interface Tree {
//   id: number;
//   value: number;
//   children: Tree[];
// }

// function dfs(value: number, tree: Tree): number | undefined {
//   if (tree.value === value) return tree.id;
//   for (const subTree of tree.children) {
//     const id = dfs(value, subTree);
//     if (id) return id;
//   }
//   return undefined;
// }

// function bfs(value: number, tree: Tree): number | undefined {
//     if (tree.value === value) return tree.id;

//     const candidates = tree.children;
//     while (candidates.length > 0) {
//         const candidate = candidates.shift()!;
//         if (candidate.value === value) return candidate.id;
//         candidates.push(...candidate.children);
//     }

//     return undefined;
// }
