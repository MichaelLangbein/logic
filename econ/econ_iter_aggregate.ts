interface Point {
  x: number;
  y: number;
}

interface Line {
  y0: number;
  slope: number;
  xMin?: number;
  xMax?: number;
  yMin?: number;
  yMax?: number;
}

function intersection(l1: Line, l2: Line): Point {
  // Check if lines are parallel (no intersection)
  if (l1.slope === l2.slope) {
    throw new Error('Lines are parallel and do not intersect.');
  }

  let x = (l2.y0 - l1.y0) / (l1.slope - l2.slope);

  if (l1.xMin && l1.xMin > x) x = l1.xMin;
  if (l2.xMin && l2.xMin > x) x = l2.xMin;
  if (l1.xMax && x > l1.xMax) x = l1.xMax;
  if (l2.xMax && x > l2.xMax) x = l2.xMax;

  let y = lineAt(x, l1);

  if (l1.yMin && l1.yMin > y) y = l1.yMin;
  if (l2.yMin && l2.yMin > y) y = l2.yMin;
  if (l1.yMax && y > l1.yMax) y = l1.yMax;
  if (l2.yMax && y > l2.yMax) y = l2.yMax;

  return { x, y };
}

function add(l1: Line, l2: Line): Line {
  const line: Line = {
    y0: l1.y0 + l2.y0,
    slope: l1.slope + l2.slope,
  };

  let xMin: number | undefined = undefined;
  if (l1.xMin) xMin = l1.xMin;
  if (l2.xMin) xMin !== undefined ? (xMin = Math.max(xMin, l2.xMin)) : l2.xMin;
  let xMax: number | undefined = undefined;
  if (l1.xMax) xMax = l1.xMax;
  if (l2.xMax) xMax !== undefined ? (xMax = Math.min(xMax, l2.xMax)) : l2.xMax;
  let yMin: number | undefined = undefined;
  if (l1.yMin) yMin = l1.yMin;
  if (l2.yMin) yMin !== undefined ? (yMin = Math.max(yMin, l2.yMin)) : l2.yMin;
  let yMax: number | undefined = undefined;
  if (l1.yMax) yMax = l1.yMax;
  if (l2.yMax) yMax !== undefined ? (yMax = Math.min(yMax, l2.yMax)) : l2.yMax;

  if (xMin) line.xMin = xMin;
  if (xMax) line.xMax = xMax;
  if (yMin) line.yMin = yMin;
  if (yMax) line.yMax = yMax;

  return line;
}

function horizontalLineAt(x: number, type: 'supply' | 'demand') {
  const slope = type === 'supply' ? 100_000_000 : -100_000_000;
  const y0 = -x * slope;
  return { y0, slope, xMin: x - 0.001, xMax: x + 0.001, yMin: 0 };
}

function lineAt(x: number, l: Line): number {
  let y = x * l.slope + l.y0;
  if (l.yMin && y < l.yMin) y = l.yMin;
  if (l.yMax && l.yMax > y) y = l.yMax;
  return y;
}

function lineInverseAt(y: number, l: Line): number {
  return (y - l.y0) / l.slope;
}

class Households {
  goods: number = 0;
  labor: number = 100;
  money: number = 100;
  takenLoans: number = 0;
  givenSavings: number = 0;

  constructor(
    private maxPriceFirstGood = 10,
    private elasticityGoodsDemand = 1.0,
    private minWagePerHour = 5,
    private elasticityWorkSupply = 1.0
  ) {}

  endOfRound() {
    this.goods = 0; // goods perish
    this.labor = 100; // ready to do more work
  }
  getGoodsDemand(): Line {
    // more money at hand makes food seem less expensive
    const y0 = this.maxPriceFirstGood + 0.1 * this.money;
    // more money means that I'm willing to order dessert
    const slope = -(this.elasticityGoodsDemand * (1.0 + 0.01 * this.money));
    return { y0, slope };
  }
  getLaborSupply(): Line {
    // less willing to work if much money in hand
    const y0 = this.minWagePerHour + 0.1 * this.money - 0.08 * this.takenLoans;
    const slope = this.elasticityWorkSupply - 0.1 * this.money + 0.08 * this.takenLoans;
    return { y0, slope };
  }
  getLoanDemand(): Line {
    // more willing to loan if very few goods
    const y0 = Math.max(10 - this.goods, 0);
    const slope = -3; // loans only make sense for few items
    return { y0, slope };
  }
  getSavingsSupply(): Line {
    // saving is a great idea if the money is there
    return { y0: 0, slope: 10, xMax: this.money };
  }
}

class Firms {
  goods: number = 0;
  capital: number = 1.0;
  labor: number = 0;
  money: number = 1000;
  takenLoans: number = 0;
  product: number = 0;

  constructor(private a = 0.5, private rndFraction = 0.1) {}

  produce() {
    this.product = Math.pow(this.labor, this.a) * Math.pow(this.capital, 1 - this.a);
  }
  endOfRound() {
    this.capital += this.rndFraction * this.money;
  }
  getGoodsSupply(): Line {
    // we've already produced - so supply is a vertical line
    return horizontalLineAt(this.product, 'supply');
  }
  getLoanDemand(): Line {
    // if little capital, much reason for investment
    const worstAcceptableInterest = 1.1;
    const amountTakenIfNoInterest = 100;
    return { y0: worstAcceptableInterest, slope: worstAcceptableInterest / amountTakenIfNoInterest };
  }
}

class Banks {
  money: number = 0;
  loanInterestRate: number = 1;
  givenHouseholdLoans: number = 0;
  takenBonds: number = 0;
  savingsInterestRate: number = 1;
  takenSavings: number = 0;
  takenGovtLoans: number = 0;
  givenFirmLoans: number = 0;
  reserveFraction: number = 0;

  constructor() {}

  getGovtLoanDemand(): Line {
    // same rule as for savings
    return this.getSavingsDemand();
  }
  endOfRound() {
    // no cleanup required
  }
  getLoanSupply(): Line {
    // give out as many loans as you can
    const maxLoans = this.money * (1 - this.reserveFraction);
    const minimumInterest = 1.01;
    const hightestInterest = 1.5;
    const slope = (hightestInterest - minimumInterest) / maxLoans;
    return { y0: minimumInterest, slope, xMax: maxLoans };
  }
  getSavingsDemand(): Line {
    const maxInterest = 1.1;
    const maxSavings = 1000;
    return { y0: maxInterest, slope: (maxInterest - 1.0) / maxSavings };
  }
}

class Government {
  money: number = 0;
  taxRate: number = 0.1;
  givenBonds: number = 0;
  bondInterestRate: number = 1.01;
  bankLoanInterestRate: number = 1.005;
  givenBankLoans: number = 0;

  constructor() {}

  endOfRound() {}
  getBankLoanSupply(): Line {
    // a horizontal line
    const bankLoanInterest = 1.005;
    return { y0: bankLoanInterest, slope: 0 };
  }
  getReserveFraction(): number {
    return 0.1;
  }
}

function collectTaxes(government: Government, households: Households) {
  const taxes = households.money * government.taxRate;
  households.money -= taxes;
  government.money += taxes;
  return taxes;
}

function collectBonds(banks: Banks, government: Government) {
  const bonds = government.bondInterestRate * government.givenBonds;
  government.money -= bonds;
  government.givenBonds = 0;
  banks.money += bonds;
  banks.takenBonds = 0;
  return bonds;
}

function collectHouseholdLoans(banks: Banks, households: Households) {
  const loans = banks.loanInterestRate * banks.givenHouseholdLoans;
  households.money -= loans;
  banks.money += loans;
  households.takenLoans = 0;
  banks.givenHouseholdLoans = 0;
}

function collectFirmLoans(banks: Banks, firms: Firms) {
  const loans = banks.loanInterestRate * banks.givenFirmLoans;
  firms.money -= loans;
  banks.money += loans;
  firms.takenLoans = 0;
  banks.givenHouseholdLoans = 0;
}

function collectSavings(households: Households, banks: Banks) {
  const savings = banks.savingsInterestRate * banks.takenSavings;
  banks.money -= savings;
  banks.takenSavings = 0;
  households.givenSavings = 0;
  households.money += savings;
}

function collectBankLoans(government: Government, banks: Banks) {
  const loans = government.bankLoanInterestRate * government.givenBankLoans;
  banks.money -= loans;
  banks.takenGovtLoans = 0;
  government.givenBankLoans = 0;
  government.money += loans;
}

function setReserveFraction(government: Government, banks: Banks) {
  banks.reserveFraction = government.getReserveFraction();
}

function takeGovernmentLoans(banks: Banks, government: Government) {
  const demand = banks.getGovtLoanDemand();
  const supply = government.getBankLoanSupply();
  const { x: loans, y: interestRate } = intersection(demand, supply);
  government.givenBankLoans = loans;
  government.money -= loans;
  government.bankLoanInterestRate = interestRate;
  banks.money += loans;
  banks.takenGovtLoans = loans;
  return { loans, interestRate };
}

function savingsMarket(households: Households, banks: Banks) {
  const supply = households.getSavingsSupply();
  const demand = banks.getSavingsDemand();
  const { x: savings, y: interestRate } = intersection(supply, demand);
  households.givenSavings = savings;
  households.money -= savings;
  banks.takenSavings = savings;
  banks.money += savings;
  banks.savingsInterestRate = interestRate;
  return { savings, interestRate };
}

function bondsMarket(banks: Banks, government: Government) {
  throw new Error('Function not implemented');
}

function loanMarket(households: Households, firms: Firms, banks: Banks) {
  const supply = banks.getLoanSupply();
  const householdDemand = households.getLoanDemand();
  const firmDemand = firms.getLoanDemand();
  const aggregateDemand = add(householdDemand, firmDemand);
  const { x: loans, y: interestRate } = intersection(supply, aggregateDemand);
  const loanHouseholds = lineAt(interestRate, householdDemand);
  households.takenLoans = loanHouseholds;
  households.money += loanHouseholds;
  const loanFirms = lineAt(interestRate, firmDemand);
  firms.takenLoans = loanFirms;
  firms.money += loanFirms;
  banks.givenFirmLoans = loanFirms;
  banks.money -= loanFirms;
  banks.givenHouseholdLoans = loanHouseholds;
  banks.money -= loanHouseholds;
  return { loans, interestRate };
}

function laborMarket(households: Households, firms: Firms) {
  const supply = households.getLaborSupply();
  const demand = firms.getLoanDemand();
  const { x: labor, y: wage } = intersection(supply, demand);
  households.labor -= labor;
  households.money += wage;
  firms.money -= wage;
  firms.labor += labor;
  return { wage, labor };
}

// @TODO: add government
function goodsMarket(households: Households, firms: Firms) {
  const demand = households.getGoodsDemand();
  const supply = firms.getGoodsSupply();
  const { x: quantity, y: price } = intersection(demand, supply);
  households.money -= price;
  households.goods += quantity;
  firms.money += price;
  firms.goods -= quantity;
  return { quantity, price };
}

function simulate() {
  const households = new Households();
  const firms = new Firms();
  const banks = new Banks();
  const government = new Government();

  for (let t = 0; t < 10; t++) {
    // 0. collecting
    const taxes = collectTaxes(government, households);
    const bonds = collectBonds(banks, government);
    collectHouseholdLoans(banks, households);
    collectFirmLoans(banks, firms);
    collectSavings(households, banks);
    collectBankLoans(government, banks);

    // 1. financial market
    setReserveFraction(government, banks);
    takeGovernmentLoans(banks, government);
    const { interestRate: householdSavingInterest } = savingsMarket(households, banks);
    // bondsMarket(banks, government);
    const { interestRate: householdLendingInterest } = loanMarket(households, firms, banks);

    // 2. labor market
    const { labor, wage } = laborMarket(households, firms);

    // 3. production
    firms.produce();

    // 4. goods market
    const { price, quantity } = goodsMarket(households, firms);

    // 5. cleanup
    households.endOfRound();
    firms.endOfRound();
    banks.endOfRound();
    government.endOfRound();

    console.log({ taxes, householdSavingInterest, householdLendingInterest, labor, wage, price, quantity });
    console.log({ hh: households.money, firms: firms.money, banks: banks.money, govt: government.money });
  }
}

simulate();
