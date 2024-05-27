/****************************************************************************************
 * User defined logic
 ****************************************************************************************/

class HouseholdBrain {
  decideNextParameters(h: Household): {
    moneyToSave: number;
    loanTarget: number;
    loanMaxRate: number;
    offeredLabor: number;
    productTarget: number;
    maxProductPrice: number;
  } {
    return {
      moneyToSave: Math.random(),
      loanTarget: 10,
      loanMaxRate: 0.01,
      offeredLabor: (h as any).labor,
      productTarget: 5,
      maxProductPrice: 10,
    };
  }
}

class FirmBrain {
  decideNextParameters(f: Firm): { loanTarget: number; loanMaxRate: number; wagePerLabor: number; price: number } {
    return { loanTarget: 10, loanMaxRate: 0.01, wagePerLabor: 10, price: 10 };
  }
}

class BankBrain {
  decideNextParameters(f: Bank): {
    savingsRate: number;
    savingsTarget: number;
    giveLoanTarget: number;
    giveLoanRate: number;
    bondsTarget: number;
    takeLoanTarget: number;
    takeLoanMaxRate: number;
  } {
    return {
      savingsRate: 0.001,
      savingsTarget: 10_000,
      giveLoanTarget: 10,
      giveLoanRate: 0.001,
      bondsTarget: 10,
      takeLoanTarget: 1,
      takeLoanMaxRate: 0.01,
    };
  }
}

/**
 * Objective:
 * - low unemployment
 * - low inflation
 *
 * Means:
 * - fiscal policy
 *    - taxes
 *    - government spending
 * - monetary policy
 *    - Fed: decide reserve-fraction
 *    - decide bond-interest
 *    - decide loan-interest
 *
 */
class GovernmentBrain {
  decideNextParameters(f: Government): {
    taxRate: number;
    nrBonds: number;
    bondRate: number;
    bondValue: number;
    productTarget: number;
    maxProductPrice: number;
    loanTarget: number;
    loanRate: number;
  } {
    return {
      taxRate: 0.1,
      nrBonds: 100,
      bondRate: 0.01,
      bondValue: 100,
      productTarget: 100,
      maxProductPrice: 10,
      loanTarget: 100,
      loanRate: 0.001,
    };
  }
}

/****************************************************************************************
 * Utils
 ****************************************************************************************/

function shuffle<T>(array: T[]): T[] {
  let currentIndex = array.length,
    randomIndex;

  // While there remain elements to shuffle.
  while (currentIndex != 0) {
    // Pick a remaining element.
    randomIndex = Math.floor(Math.random() * currentIndex);
    currentIndex--;

    // And swap it with the current element.
    [array[currentIndex], array[randomIndex]] = [array[randomIndex], array[currentIndex]];
  }

  return array;
}

/****************************************************************************************
 * Types
 ****************************************************************************************/

type Loan = { id: number; debtor: AsksLoan; provider: OffersLoan; amount: number; interest: number };
type Bond = { id: number; government: OffersBond; bank: AsksBond; value: number; interest: number };
type Saving = { id: number; bank: AsksSavings; customer: OffersSavings; amount: number; interest: number };

interface Agent {
  decideNextParameters(): void;
  endOfRound(): void;
}

interface AsksLoan {
  payBackLoan(loan: Loan): number;
  tookLoan(loan: Loan, money: number): void;
  wouldTakeLoanAtRate(data: { amount: number; rate: number }): boolean;
  requiredLoan(): number;
}
interface OffersLoan {
  loanPayedBack(loan: Loan, money: number): void;
  gaveLoan(loan: Loan): number;
  settleLoans(settleLoanStrat: (loan: Loan) => void): void;
  wouldLoanAtRate(data: { debtor: AsksLoan; amount: number }): number;
}

interface AsksSavings {
  withdrawSaving(saving: Saving): number;
  receivedSaving(saving: Saving): void;
  wouldTakeSavingsAtRate(moneyToSave: number): number;
}
interface OffersSavings {
  receiveWithdrawnSaving(saving: Saving, money: number): void;
  depositedSaving(saving: Saving): void;
  getMoneyToSave(): number;
  collectSavings(collectStrat: (saving: Saving) => void): void;
}

interface AsksBond {
  bondPayedBack(bond: Bond, money: number): void;
  boughtBond(bond: Bond): number;
  wouldBuyBond(rate: number, value: number): boolean;
  collectBonds(collectStrat: (bond: Bond) => void): void;
}
interface OffersBond {
  /** reduce own money by new value */
  payBackBond(bond: Bond): number;
  lentOutBond(bond: Bond, money: number): void;
  nrBondsOffered(): { nrBonds: number; rate: number; value: number };
}

interface OffersJobs {
  buyLabor(labor: number, wage: number): void;
  wageForLabor(laborToOffer: number): number;
}
interface LookingForJob {
  sellLabor(labor: number, wage: number): void;
  availableLabor(): number;
}

interface AsksProduct {
  buyProduct(product: number, price: number): number;
  wouldBuyProductFor(): number;
}
interface SellsProduct {
  sellProduct(price: number): number;
  wouldSellProductFor(): number;
  produce(): void;
}

interface TaxPayer {
  payTaxes(taxRate: number): number;
}

/****************************************************************************************
 * Actors
 ****************************************************************************************/

class Household implements Agent, AsksProduct, LookingForJob, AsksLoan, OffersSavings, TaxPayer {
  private saving: Saving | undefined;
  private loan: Loan | undefined;
  private product = 0;

  // brain decided parameters
  private _strategyMoneyToSave!: number;
  private _strategyLoanTarget!: number;
  private _strategyMaxLoanRate!: number;
  private _strategyOfferedLabor!: number;
  private _strategyProductTarget!: number;
  private _strategyMaxProductPrice!: number;

  constructor(
    private brain: HouseholdBrain,
    private money: number,
    private capacityForLabor = Math.random() * 10,
    private labor = 1
  ) {
    this.decideNextParameters();
  }

  decideNextParameters(): void {
    const { moneyToSave, loanTarget, loanMaxRate, offeredLabor, productTarget, maxProductPrice } =
      this.brain.decideNextParameters(this);
    this._strategyMoneyToSave = moneyToSave;
    this._strategyLoanTarget = loanTarget;
    this._strategyMaxLoanRate = loanMaxRate;
    this._strategyOfferedLabor = offeredLabor;
    this._strategyProductTarget = productTarget;
    this._strategyMaxProductPrice = maxProductPrice;
  }

  endOfRound(): void {
    this.product = 0;
    this.labor = this.capacityForLabor;
  }

  payTaxes(taxRate: number): number {
    const amount = this.money * taxRate;
    this.money -= amount;
    return amount;
  }
  buyProduct(product: number, price: number): number {
    this.money -= price;
    this.product += product;
    return price;
  }
  wouldBuyProductFor(): number {
    if (this.product >= this._strategyProductTarget) return 0;
    else return this._strategyMaxProductPrice;
  }
  sellLabor(labor: number, wage: number): void {
    this.labor -= labor;
    this.money += wage;
  }
  availableLabor(): number {
    return this._strategyOfferedLabor;
  }
  payBackLoan(loan: Loan): number {
    const amount = loan.amount * loan.interest;
    this.money -= amount;
    this.loan = undefined;
    return amount;
  }
  tookLoan(loan: Loan, money: number): void {
    if (this.loan) throw Error('Already have a loan');
    this.loan = loan;
    this.money += money;
  }
  wouldTakeLoanAtRate(data: { amount: number; rate: number }): boolean {
    if (this.loan) return false;
    if (data.rate <= this._strategyMaxLoanRate) return true;
    return false;
  }
  requiredLoan(): number {
    if (this.loan) return 0;
    else return this._strategyLoanTarget;
  }
  receiveWithdrawnSaving(saving: Saving, money: number): void {
    if (!this.saving) throw Error("Don't have a saving to receive");
    if (this.saving.id !== saving.id) throw Error("Saving ids don't match");
    const expectedMoney = this.saving.amount * this.saving.interest;
    if (money >= expectedMoney) {
      this.saving = undefined;
    } else {
      this.saving.amount -= money;
    }
    this.money += money;
  }
  depositedSaving(saving: Saving): void {
    if (this.saving) throw Error(`Can't deposit saving: already have one`);
    this.money -= saving.amount;
    this.saving = saving;
  }
  getMoneyToSave(): number {
    return this._strategyMoneyToSave;
  }
  collectSavings(collectStrat: (saving: Saving) => void): void {
    if (this.saving) collectStrat(this.saving);
  }
}

class Firm implements Agent, OffersJobs, SellsProduct, AsksLoan {
  private loan: Loan | undefined;
  private labor: number = 0;
  private laborProductivity = Math.random() * 10;
  private product: number = 0;

  // brain decided parameters
  private _strategyLoanTarget!: number;
  private _strategyWagePerLabor!: number;
  private _strategyPrice!: number;
  private _strategyMaxLoanRate!: number;

  constructor(private brain: FirmBrain, private money: number) {
    this.decideNextParameters();
  }

  decideNextParameters(): void {
    const { loanTarget, loanMaxRate, wagePerLabor, price } = this.brain.decideNextParameters(this);
    this._strategyLoanTarget = loanTarget;
    this._strategyMaxLoanRate = loanMaxRate;
    this._strategyWagePerLabor = wagePerLabor;
    this._strategyPrice = price;
  }

  endOfRound(): void {}

  buyLabor(labor: number, wage: number): void {
    this.money -= wage;
    this.labor += labor;
  }
  wageForLabor(laborToOffer: number): number {
    return this._strategyWagePerLabor * laborToOffer;
  }
  sellProduct(price: number): number {
    this.product -= 1;
    this.money += price;
    return 1;
  }
  wouldSellProductFor(): number {
    return this._strategyPrice;
  }
  produce(): void {
    this.product = this.labor * this.laborProductivity;
  }
  payBackLoan(loan: Loan): number {
    const amount = loan.amount * loan.interest;
    this.money -= amount;
    this.loan = undefined;
    return amount;
  }
  tookLoan(loan: Loan, money: number): void {
    if (this.loan) throw Error('Already have a loan');
    this.loan = loan;
    this.money += money;
  }
  wouldTakeLoanAtRate(data: { amount: number; rate: number }): boolean {
    if (this.loan) return false;
    if (data.rate <= this._strategyMaxLoanRate) return true;
    return false;
  }
  requiredLoan(): number {
    if (this.loan) return 0;
    else return this._strategyLoanTarget;
  }
}

class Bank implements Agent, OffersLoan, AsksSavings, AsksLoan, AsksBond {
  private bonds: Bond[] = [];
  private givenLoans: Loan[] = [];
  private takenLoans: Loan[] = [];
  private savings: Saving[] = [];

  // brain decided parameters
  private _strategySavingsTarget!: number;
  private _strategySavingsRate!: number;
  private _strategyGiveLoanTarget!: number;
  private _strategyGiveLoanRate!: number;
  private _strategyBondTarget!: number;
  private _strategyTakeLoanTarget!: number;
  private _strategyTakeLoanMaxRate!: number;

  constructor(private brain: BankBrain, private money: number) {
    this.decideNextParameters();
  }

  decideNextParameters(): void {
    const { savingsTarget, savingsRate, giveLoanTarget, giveLoanRate, bondsTarget, takeLoanTarget, takeLoanMaxRate } =
      this.brain.decideNextParameters(this);
    this._strategySavingsRate = savingsRate;
    this._strategySavingsTarget = savingsTarget;
    this._strategyGiveLoanTarget = giveLoanTarget;
    this._strategyGiveLoanRate = giveLoanRate;
    this._strategyBondTarget = bondsTarget;
    this._strategyTakeLoanTarget = takeLoanTarget;
    this._strategyTakeLoanMaxRate = takeLoanMaxRate;
  }

  endOfRound(): void {}

  payBackLoan(loan: Loan): number {
    const amount = loan.amount * loan.interest;
    this.money -= amount;
    this.givenLoans = this.givenLoans.filter((g) => g.id !== loan.id);
    return amount;
  }
  tookLoan(loan: Loan, money: number): void {
    this.takenLoans.push(loan);
    this.money += money;
  }
  wouldTakeLoanAtRate(data: { amount: number; rate: number }): boolean {
    const takenLoans = this.takenLoans.reduce((sum, l) => sum + l.amount, 0);
    if (takenLoans >= this._strategyTakeLoanTarget) return false;
    else return data.rate <= this._strategyTakeLoanMaxRate;
  }
  requiredLoan(): number {
    const existingLoans = this.givenLoans.reduce((sum, l) => sum + l.amount, 0);
    if (existingLoans >= this._strategyGiveLoanTarget) return 0;
    else return this._strategyGiveLoanTarget - existingLoans;
  }
  loanPayedBack(loan: Loan, money: number): void {
    const expectedMoney = loan.amount * loan.interest;
    if (expectedMoney >= money) {
      this.givenLoans = this.givenLoans.filter((l) => l.id !== loan.id);
      this.money += money;
    } else {
      this.givenLoans.find((l) => l.id === loan.id)!.amount -= money;
      this.money += money;
    }
  }
  gaveLoan(loan: Loan): number {
    const value = loan.amount;
    this.money -= value;
    this.givenLoans.push(loan);
    return value;
  }
  settleLoans(settleLoanStrat: (loan: Loan) => void): void {
    for (const loan of this.givenLoans) {
      settleLoanStrat(loan);
    }
  }
  wouldLoanAtRate(data: { debtor: AsksLoan; amount: number }): number {
    const existingLoans = this.givenLoans.reduce((sum, l) => sum + l.amount, 0);
    if (existingLoans > this._strategyGiveLoanTarget) return 9999999999;
    else return this._strategyGiveLoanRate;
  }
  withdrawSaving(saving: Saving): number {
    const value = saving.amount * saving.interest;
    this.savings = this.savings.filter((s) => s.id !== saving.id);
    return value;
  }
  receivedSaving(saving: Saving): void {
    this.savings.push(saving);
  }
  wouldTakeSavingsAtRate(moneyToSave: number): number {
    const existingSavings = this.savings.reduce((prev, curr) => prev + curr.amount, 0);
    if (existingSavings > this._strategySavingsTarget) return -1;
    else return this._strategySavingsRate;
  }
  bondPayedBack(bond: Bond, money: number): void {
    const expectedMoney = bond.value * bond.interest;
    if (money >= expectedMoney) {
      this.bonds = this.bonds.filter((b) => b.id !== bond.id);
      this.money += money;
    } else {
      this.bonds.find((b) => b.id === bond.id)!.value -= money;
      this.money += money;
    }
  }
  boughtBond(bond: Bond): number {
    const price = bond.value;
    this.money -= price;
    this.bonds.push(bond);
    return price;
  }
  wouldBuyBond(rate: number, value: number): boolean {
    const currentBondValue = this.bonds.reduce((sum, b) => sum + b.value, 0);
    if (currentBondValue >= this._strategyBondTarget) return false;
    return true;
  }
  collectBonds(collectStrat: (bond: Bond) => void): void {
    for (const bond of this.bonds) {
      collectStrat(bond);
    }
  }
}

class Government implements Agent, OffersLoan, OffersBond, AsksProduct {
  private loans: Loan[] = [];
  private product = 0;
  private givenOutBonds: Bond[] = [];

  // brain decided parameters
  private _strategyTaxRate!: number;
  private _strategyNrBonds!: number;
  private _strategyBondRate!: number;
  private _strategyBondValue!: number;
  private _strategyProductTarget!: number;
  private _strategyMaxProductPrice!: number;
  private _strategyLoanTarget!: number;
  private _strategyLoanRate!: number;

  constructor(private brain: GovernmentBrain, private money: number) {
    this.decideNextParameters();
  }

  decideNextParameters(): void {
    const { taxRate, nrBonds, bondRate, bondValue, productTarget, maxProductPrice, loanTarget, loanRate } =
      this.brain.decideNextParameters(this);
    this._strategyTaxRate = taxRate;
    this._strategyNrBonds = nrBonds;
    this._strategyBondRate = bondRate;
    this._strategyBondValue = bondValue;
    this._strategyProductTarget = productTarget;
    this._strategyMaxProductPrice = maxProductPrice;
    this._strategyLoanTarget = loanTarget;
    this._strategyLoanRate = loanRate;
  }

  endOfRound(): void {
    this.product = 0;
  }

  collectTaxes(households: Household[]) {
    for (const household of households) {
      this.money += household.payTaxes(this._strategyTaxRate);
    }
  }
  loanPayedBack(loan: Loan, money: number): void {
    const expectedMoney = loan.amount * loan.interest;
    if (expectedMoney >= money) {
      this.loans = this.loans.filter((l) => l.id !== loan.id);
      this.money += money;
    } else {
      this.loans.find((l) => l.id === loan.id)!.amount -= money;
      this.money += money;
    }
  }
  gaveLoan(loan: Loan): number {
    this.money -= loan.amount;
    this.loans.push(loan);
    return loan.amount;
  }
  settleLoans(settleLoanStrat: (loan: Loan) => void): void {
    for (const loan of this.loans) {
      settleLoanStrat(loan);
    }
  }
  wouldLoanAtRate(data: { debtor: AsksLoan; amount: number }): number {
    const existingLoans = this.loans.reduce((sum, l) => sum + l.amount, 0);
    if (existingLoans >= this._strategyLoanTarget) return 99999999999;
    return this._strategyLoanRate;
  }
  payBackBond(bond: Bond): number {
    const value = bond.value * bond.interest;
    this.money -= value;
    this.givenOutBonds = this.givenOutBonds.filter((b) => b.id !== bond.id);
    return value;
  }
  lentOutBond(bond: Bond, money: number): void {
    this.givenOutBonds.push(bond);
    this.money += money;
  }
  nrBondsOffered(): { nrBonds: number; rate: number; value: number } {
    return { nrBonds: this._strategyNrBonds, rate: this._strategyBondRate, value: this._strategyBondValue };
  }
  buyProduct(product: number, price: number): number {
    this.money -= price;
    this.product += product;
    return price;
  }
  wouldBuyProductFor(): number {
    if (this.product >= this._strategyProductTarget) return 0;
    else return this._strategyMaxProductPrice;
  }
}

/****************************************************************************************
 * Markets
 ****************************************************************************************/

let globalLoanCounter = 0;
let globalSavingsCounter = 0;
let globalBondCounter = 0;

class LoanMarket {
  constructor(private wantLoan: AsksLoan[], private offerLoan: OffersLoan[]) {}

  tradeAll() {
    const wantLoan = shuffle(this.wantLoan);

    for (const debtor of wantLoan) {
      const amount = debtor.requiredLoan();
      if (amount <= 0) continue;

      let bestRate = 999999999999999999999;
      let bestProvider: OffersLoan | undefined = undefined;

      for (const provider of this.offerLoan) {
        const rate = provider.wouldLoanAtRate({ debtor, amount });
        if (rate < bestRate) {
          bestRate = rate;
          bestProvider = provider;
        }
      }

      const wouldTakeLoan = debtor.wouldTakeLoanAtRate({ amount, rate: bestRate });
      if (bestProvider && wouldTakeLoan) {
        LoanMarket.createLoan(debtor, bestProvider, bestRate, amount);
      }
    }
  }

  static createLoan(debtor: AsksLoan, provider: OffersLoan, interest: number, amount: number) {
    globalLoanCounter += 1;
    const loan: Loan = { id: globalLoanCounter, amount, interest, debtor: debtor, provider: provider };
    const money = provider.gaveLoan(loan);
    debtor.tookLoan(loan, money);
  }

  static settleLoan(loan: Loan) {
    const money = loan.debtor.payBackLoan(loan);
    loan.provider.loanPayedBack(loan, money);
  }
}

class LaborMarket {
  constructor(private employees: LookingForJob[], private employers: OffersJobs[]) {}

  tradeAll() {
    const employees = shuffle(this.employees);
    for (const employee of employees) {
      const laborToOffer = employee.availableLabor();
      let bestWage = 0;
      let bestEmployer: OffersJobs | undefined = undefined;

      for (const employer of this.employers) {
        const offeredWage = employer.wageForLabor(laborToOffer);
        if (offeredWage > bestWage) {
          bestWage = offeredWage;
          bestEmployer = employer;
        }
      }

      if (bestEmployer) {
        LaborMarket.employ(employee, bestEmployer, bestWage, laborToOffer);
      }
    }
  }

  static employ(employee: LookingForJob, employer: OffersJobs, wage: number, labor: number) {
    employee.sellLabor(labor, wage);
    employer.buyLabor(labor, wage);
  }
}

class ProductMarket {
  constructor(private buyers: AsksProduct[], private sellers: SellsProduct[]) {}

  tradeAll() {
    for (const buyer of this.buyers) {
      let bestPrice = 9999999999999;
      let bestSeller: SellsProduct | undefined = undefined;

      for (const seller of this.sellers) {
        const price = seller.wouldSellProductFor();
        if (price < bestPrice) {
          bestPrice = price;
          bestSeller = seller;
        }
      }

      let maxPrice = buyer.wouldBuyProductFor();
      if (bestSeller && bestPrice <= maxPrice) {
        ProductMarket.doTrade(buyer, bestSeller, bestPrice);
      }
    }
  }

  static doTrade(buyer: AsksProduct, seller: SellsProduct, price: number) {
    const product = seller.sellProduct(price);
    buyer.buyProduct(product, price);
  }
}

class SavingsMarket {
  constructor(private customers: OffersSavings[], private banks: AsksSavings[]) {}

  tradeAll() {
    for (const customer of this.customers) {
      const amount = customer.getMoneyToSave();
      let bestRate = 0;
      let bestBank: AsksSavings | undefined = undefined;
      for (const bank of this.banks) {
        const rate = bank.wouldTakeSavingsAtRate(amount);
        if (rate > bestRate) {
          bestRate = rate;
          bestBank = bank;
        }
      }
      if (bestBank) {
        SavingsMarket.deposit(customer, amount, bestBank, bestRate);
      }
    }
  }

  static deposit(customer: OffersSavings, amount: number, bank: AsksSavings, interest: number) {
    globalSavingsCounter += 1;
    const saving: Saving = { id: globalSavingsCounter, amount, interest, bank, customer };
    customer.depositedSaving(saving);
    bank.receivedSaving(saving);
  }

  static collectSaving(saving: Saving) {
    const money = saving.bank.withdrawSaving(saving);
    saving.customer.receiveWithdrawnSaving(saving, money);
  }
}

class BondsMarket {
  constructor(private banks: AsksBond[], private government: OffersBond) {}

  tradeAll() {
    const { nrBonds, rate, value } = this.government.nrBondsOffered();
    for (let nrBondsLeft = nrBonds; nrBondsLeft > 0; nrBondsLeft--) {
      const banks = shuffle(this.banks);
      for (const bank of banks) {
        if (bank.wouldBuyBond(rate, value)) {
          BondsMarket.createBond(this.government, bank, rate, value);
        }
      }
    }
  }

  static createBond(government: OffersBond, bank: AsksBond, interest: number, value: number) {
    globalBondCounter += 1;
    const bond: Bond = { id: globalBondCounter, value, interest, government, bank };
    const money = bank.boughtBond(bond);
    government.lentOutBond(bond, money);
  }

  static collectBond(bond: Bond) {
    const money = bond.government.payBackBond(bond);
    bond.bank.bondPayedBack(bond, money);
  }
}

/****************************************************************************************
 * Simulation
 ****************************************************************************************/

let households: Household[] = [];
for (let h = 0; h < 1000; h++) {
  households.push(new Household(new HouseholdBrain(), 100));
}
let firms: Firm[] = [];
for (let f = 0; f < 100; f++) {
  firms.push(new Firm(new FirmBrain(), 1000));
}
let banks: Bank[] = [];
for (let b = 0; b < 10; b++) {
  banks.push(new Bank(new BankBrain(), 10_000));
}
const government = new Government(new GovernmentBrain(), 100_000);

for (let t = 0; t < 1000; t++) {
  // 0. strategizing
  government.decideNextParameters();
  banks.map((b) => b.decideNextParameters());
  firms.map((f) => f.decideNextParameters());
  households.map((h) => h.decideNextParameters());

  // 1. collecting
  // government first - cannot cause insolvency
  government.collectTaxes(households);
  // collecting from government next - cannot cause insolvency
  banks.map((b) => b.collectBonds(BondsMarket.collectBond));
  // collecting from households next - cannot cause insolvency
  banks.map((b) => b.settleLoans(LoanMarket.settleLoan));
  // collecting from banks next - banks now have peak funds
  households.map((h) => h.collectSavings(SavingsMarket.collectSaving));
  // collecting from banks for government at end - government won't suffer if banks default
  government.settleLoans(LoanMarket.settleLoan);
  // firms = firms.map((f) => (f.money >= 0 ? f : new Firm(0)));
  // banks = banks.map((b) => (b.money >= 0 ? b : new Bank(0)));

  // 2. money markets
  const savingsMarket = new SavingsMarket(households, banks);
  savingsMarket.tradeAll();
  const loansFromGovtToBanks = new LoanMarket(banks, [government]);
  loansFromGovtToBanks.tradeAll();
  const bondMarket = new BondsMarket(banks, government);
  bondMarket.tradeAll();
  const loansMarket = new LoanMarket([...households, ...firms], banks);
  loansMarket.tradeAll();

  // 3. labor market
  const lm = new LaborMarket(households, firms);
  lm.tradeAll();

  // 4. production
  firms.map((f) => f.produce());

  // 5. goods market
  const gm = new ProductMarket([...households, government], firms);
  gm.tradeAll();

  // 6. cleanup
  households.map((h) => h.endOfRound());
  firms.map((f) => f.endOfRound());
  banks.map((b) => b.endOfRound());
  government.endOfRound();
}
