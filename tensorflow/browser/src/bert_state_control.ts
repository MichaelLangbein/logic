/**
 * Control app navigation with chat-interface.
 *
 * 1. user input: "I want to see the damage on buildings"
 * 2. bert (`matchUserInputWithState`) translates input to state: state = {screen: map, step: 4-damage}
 * 3. `shortestPath` finds sequence of actions (a "path") to get from current to target state: ["go to peru", "select epicenter", "execute eq", "load exposure", "calculate damage"]
 * 4. ui verifies with user if those are the right steps and the target state is the desired state
 * 5. ui executes all those steps while user watches
 */

/**
 *
 * Example state machine
 *
 *      room1 -- right --> room2 -- right --> room3
 *            <-- left --        <-- left --
 *      |                   |                   |
 *      down                down                down
 *      |                   |                   |
 *      V                   V                   V
 *      room4 -- right --> room5 -- right --> room6
 *            <-- left --        <-- left --
 *
 */

interface State {
  room: number;
}

function statesEqual(s1: State, s2: State): boolean {
  return s1.room === s2.room;
}

interface Action {
  go: 'left' | 'right' | 'up' | 'down';
}

type Path = Action[];

class FiniteStateMachine {
  private paths: { [state: number]: { [action: string]: number | undefined } } = {
    1: { left: undefined, right: 2, up: undefined, down: 4 },
    2: { left: 1, right: 3, up: undefined, down: 5 },
    3: { left: 2, right: undefined, up: undefined, down: 6 },
    4: { left: undefined, right: 5, up: 1, down: undefined },
    5: { left: 4, right: 6, up: 2, down: undefined },
    6: { left: 5, right: undefined, up: 3, down: undefined },
  };

  constructor(private state: State) {}

  getAllActions(): Action[] {
    const currentRoom = this.state.room;
    const currentOptions = this.paths[currentRoom];
    const possibleDirections = [];
    for (const [direction, room] of Object.entries(currentOptions)) {
      if (room !== undefined) {
        possibleDirections.push({ go: direction } as Action);
      }
    }
    return possibleDirections;
  }

  execute(action: Action): State {
    const currentRoom = this.state.room;
    const currentOptions = this.paths[currentRoom];
    const newRoom = currentOptions[action.go];
    if (newRoom === undefined)
      throw Error(`This action is not allowed: ${action.go} (current room: ${this.state.room})`);
    this.state = { room: newRoom };
    return structuredClone(this.state);
  }

  executeAll(actions: Path): State {
    let state = this.state;
    for (const action of actions) state = this.execute(action);
    return state;
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

export function run() {
  const initialState: State = { room: 1 };
  const targetState: State = { room: 3 };
  const path = shortestPath(initialState, targetState);
  console.log(path?.map((a) => a.go));
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
