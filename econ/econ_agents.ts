/****************************************************************************************
 * User defined logic
 ****************************************************************************************/

class HouseholdBrain {
  decideNextParameters(h: Household): { moneyToSave: number } {
    return { moneyToSave: Math.random() };
  }
}

class FirmBrain {
  decideNextParameters(f: Firm): {} {
    return {};
  }
}

class BankBrain {
  decideNextParameters(f: Bank): {} {
    return {};
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
  decideNextParameters(f: Government): {} {
    return {};
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

type Loan = { debtor: AsksLoan; provider: OffersLoan; amount: number; interest: number };
type Bond = { government: OffersBond; bank: AsksBond; value: number; interest: number };
type Saving = { bank: AsksSavings; customer: OffersSavings; amount: number; interest: number };

interface Agent {
  decideNextParameters(): void;
  getMoney(): number;
}

interface AsksLoan {
  payBackLoan(loan: Loan): number;
  tookLoan(loan: Loan): void;
  wouldTakeLoanAtRate(data: { amount: number; rate: number }): boolean;
  requiredLoan(): number;
}
interface OffersLoan {
  loanPayedBack(loan: Loan, money: number): void;
  gaveLoan(loan: Loan): void;
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
  bondPayedBack(bond: Bond, money: unknown): unknown;
  gotBond(bond: Bond): void;
  wouldBuyBond(rate: number): unknown;
  collectBonds(collectStrat: (bond: Bond) => void): void;
}
interface OffersBond {
  /** reduce own money by new value */
  payBackBond(bond: Bond): number;
  lentOutBond(bond: Bond): void;
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
  sellsProductFor(): number;
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

  // brain decided parameters
  private _strategyMoneyToSave!: number;

  constructor(
    private brain: HouseholdBrain,
    private money: number,
    private capacityForLabor = Math.random() * 10,
    private labor = 1
  ) {
    this.decideNextParameters();
  }

  decideNextParameters(): void {
    const { moneyToSave } = this.brain.decideNextParameters(this);
    this._strategyMoneyToSave = moneyToSave;
  }

  payTaxes(taxRate: number): number {
    const amount = this.money * taxRate;
    this.money -= amount;
    return amount;
  }
  getMoney(): number {
    return this.money;
  }
  buyProduct(product: number, price: number): number {
    throw new Error('Method not implemented.');
  }
  wouldBuyProductFor(): number {
    throw new Error('Method not implemented.');
  }
  sellLabor(labor: number, wage: number): void {
    throw new Error('Method not implemented.');
  }
  availableLabor(): number {
    throw new Error('Method not implemented.');
  }
  payBackLoan(loan: Loan): number {
    throw new Error('Method not implemented.');
  }
  tookLoan(loan: Loan): void {
    throw new Error('Method not implemented.');
  }
  wouldTakeLoanAtRate(data: { amount: number; rate: number }): boolean {
    throw new Error('Method not implemented.');
  }
  requiredLoan(): number {
    throw new Error('Method not implemented.');
  }
  receiveWithdrawnSaving(saving: Saving, money: number): void {
    throw new Error('Method not implemented.');
  }
  depositedSaving(saving: Saving): void {
    throw new Error('Method not implemented.');
  }
  getMoneyToSave(): number {
    return this._strategyMoneyToSave;
  }
  collectSavings(collectStrat: (saving: Saving) => void): void {
    if (this.saving) collectStrat(this.saving);
  }
}

class Firm implements Agent, OffersJobs, SellsProduct, AsksLoan {
  constructor(private brain: FirmBrain, private money: number, private labor = 0) {
    this.decideNextParameters();
  }

  decideNextParameters(): void {
    const {} = this.brain.decideNextParameters(this);
  }
  getMoney(): number {
    throw new Error('Method not implemented.');
  }
  buyLabor(labor: number, wage: number): void {
    throw new Error('Method not implemented.');
  }
  wageForLabor(laborToOffer: number): number {
    throw new Error('Method not implemented.');
  }
  sellProduct(price: number): number {
    throw new Error('Method not implemented.');
  }
  sellsProductFor(): number {
    throw new Error('Method not implemented.');
  }
  produce(): void {
    throw new Error('Method not implemented.');
  }
  payBackLoan(loan: Loan): number {
    throw new Error('Method not implemented.');
  }
  tookLoan(loan: Loan): void {
    throw new Error('Method not implemented.');
  }
  wouldTakeLoanAtRate(data: { amount: number; rate: number }): boolean {
    throw new Error('Method not implemented.');
  }
  requiredLoan(): number {
    throw new Error('Method not implemented.');
  }
}

class Bank implements Agent, OffersLoan, AsksSavings, AsksLoan, AsksBond {
  private bonds: Bond[] = [];
  private loans: Loan[] = [];

  constructor(private brain: BankBrain, private money: number) {
    this.decideNextParameters();
  }

  decideNextParameters(): void {
    const {} = this.brain.decideNextParameters(this);
  }

  getMoney(): number {
    throw new Error('Method not implemented.');
  }
  payBackLoan(loan: Loan): number {
    throw new Error('Method not implemented.');
  }
  tookLoan(loan: Loan): void {
    throw new Error('Method not implemented.');
  }
  wouldTakeLoanAtRate(data: { amount: number; rate: number }): boolean {
    throw new Error('Method not implemented.');
  }
  requiredLoan(): number {
    throw new Error('Method not implemented.');
  }
  loanPayedBack(loan: Loan, money: number): void {
    throw new Error('Method not implemented.');
  }
  gaveLoan(loan: Loan): void {
    throw new Error('Method not implemented.');
  }
  settleLoans(settleLoanStrat: (loan: Loan) => void): void {
    for (const loan of this.loans) {
      settleLoanStrat(loan);
    }
  }
  wouldLoanAtRate(data: { debtor: AsksLoan; amount: number }): number {
    throw new Error('Method not implemented.');
  }
  withdrawSaving(saving: Saving): number {
    throw new Error('Method not implemented.');
  }
  receivedSaving(saving: Saving): void {
    throw new Error('Method not implemented.');
  }
  wouldTakeSavingsAtRate(moneyToSave: number): number {
    throw new Error('Method not implemented.');
  }
  bondPayedBack(bond: Bond, money: unknown): unknown {
    throw new Error('Method not implemented.');
  }
  gotBond(bond: Bond): void {
    throw new Error('Method not implemented.');
  }
  wouldBuyBond(rate: number): unknown {
    throw new Error('Method not implemented.');
  }
  collectBonds(collectStrat: (bond: Bond) => void): void {
    for (const bond of this.bonds) {
      collectStrat(bond);
    }
  }
}

class Government implements Agent, OffersLoan, OffersBond, AsksProduct {
  private loans: Loan[] = [];
  private _strategyTaxRate = 0.1;

  constructor(private brain: GovernmentBrain, private money: number) {
    this.decideNextParameters();
  }

  decideNextParameters(): void {
    const {} = this.brain.decideNextParameters(this);
  }

  getMoney(): number {
    return this.getMoney();
  }

  collectTaxes(households: Household[]) {
    for (const household of households) {
      this.money += household.payTaxes(this._strategyTaxRate);
    }
  }
  loanPayedBack(loan: Loan, money: number): void {
    throw new Error('Method not implemented.');
  }
  gaveLoan(loan: Loan): void {
    throw new Error('Method not implemented.');
  }
  settleLoans(settleLoanStrat: (loan: Loan) => void): void {
    for (const loan of this.loans) {
      settleLoanStrat(loan);
    }
  }
  wouldLoanAtRate(data: { debtor: AsksLoan; amount: number }): number {
    throw new Error('Method not implemented.');
  }
  payBackBond(bond: Bond): number {
    throw new Error('Method not implemented.');
  }
  lentOutBond(bond: Bond): void {
    throw new Error('Method not implemented.');
  }
  nrBondsOffered(): { nrBonds: number; rate: number; value: number } {
    throw new Error('Method not implemented.');
  }
  buyProduct(product: number, price: number): number {
    throw new Error('Method not implemented.');
  }
  wouldBuyProductFor(): number {
    throw new Error('Method not implemented.');
  }
}

/****************************************************************************************
 * Markets
 ****************************************************************************************/

class LoanMarket {
  constructor(private wantLoan: AsksLoan[], private offerLoan: OffersLoan[]) {}

  tradeAll() {
    for (const debtor of this.wantLoan) {
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

  static createLoan(buyer: AsksLoan, seller: OffersLoan, interest: number, amount: number) {
    const loan: Loan = { amount, interest, debtor: buyer, provider: seller };
    seller.gaveLoan(loan);
    buyer.tookLoan(loan);
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
        const price = seller.sellsProductFor();
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
    const saving: Saving = { amount, interest, bank, customer };
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
        if (bank.wouldBuyBond(rate)) {
          BondsMarket.createBond(this.government, bank, rate, value);
        }
      }
    }
  }

  static createBond(government: OffersBond, bank: AsksBond, interest: number, value: number) {
    const bond: Bond = { value, interest, government, bank };
    bank.gotBond(bond);
    government.lentOutBond(bond);
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
}
