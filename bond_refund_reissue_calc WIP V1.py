#if __name__ == '__main__': signals the reader that this file is a script and is runable. 
def main():
   print("hello world!")

if __name__ == '__main__':
   main()

import numpy as np
import numpy_financial as npf

# README
# This script is a bond refund/reissue calculatior. Enter the required inputs and it will return the NPV of the refund and reissue process as well as whether the process is profitable or not. 
# Calculations modeled from pg. 253 of Foundations of Financial Management FNCE3323 textbook by Stanley B. Block, Geoffrey A. Hirt, Bartley R. Danielsen, J. Douglas Short.
# LIMITATIONS: 
# The number of years variable: 'n_years' must be >= 5 years for proper amortization of float costs. 
# The script assumes straight line amortization of 20% per year. 
# End result is aproximate due to the variance on actual interest earned from underwriting fees in the overlap period calculation. 
# TODO fix data validation for inputs
# TODO fix enhanced_details bool for extra detail print statements.

def refund_bond_or_not():
   # Define inputs.

   while(True):
      try:
         balance = int(input("What is the size of the bond(s) to be refinanced? Enter in dollars as int: "))
         break
      except ValueError:
         print("This needs to be an integer! eg. $10,000,000 = 10000000:")

   while(True):
      try:
         call_premium = float(input("What is the size of the call premium on the bond to be refunded? Enter as decimal: "))
         break
      except ValueError:
         print("this needs to be a decimal! eg. 10% = 0.1")

   while(True):
      try:
         float_costs = int(input("What is the sum of the floatation costs involved in issuing the new bonds? Enter in dollars as int : "))
         break
      except ValueError:
         print("This needs to be an integer! eg. $100,000 = 100000:")

   while(True):
      try: 
         tax_rate = float(input("What is the tax rate for the company reissuing the bonds? Enter in as a decimal: "))
         break
      except ValueError:
         print("this needs to be a decimal! eg. 25% = 0.25")

   while(True):
      try:
         old_interest_rate = float(input("What is the interest rate of the old bonds to be recalled? Enter as a decimal: "))
         break
      except ValueError:
         print("this needs to be a decimal! eg. 10.5% = 0.105")

   while(True):
      try:
         interest_rate = float(input("What is the interest rate of the new bonds to be issued? Enter as a decimal: "))
         break
      except ValueError:
         print("this needs to be a decimal! eg. 8% = 0.08")

   while(True):
      try:
         n_years = int(input("How many years until the new bonds mature? Enter a number as int, must be 5 or more: "))
         break
      except ValueError:
         print("This needs to be an integer! eg. 5 years = 5:")

   while(True):
      try:
         overlap_time = int(input("How many days will there be in overlap between when the old bonds are called and the new bonds are issued? Enter in whole days: "))
         break
      except ValueError:
         print("This needs to be an integer! eg. 30 Days = 30 ")

   while(True):      
      try:
         short_term_rate = float(input("What interest rate is used for the overlap period? Enter as a decimal: "))
         break
      except ValueError:
         print("this needs to be a decimal! eg. 3.5% = 0.035")

   #Hard codes for testing. Values taken from pg. 253 of Foundations of Financial Management FNCE3323 textbook by Stanley B. Block, Geoffrey A. Hirt, Bartley R. Danielsen, J. Douglas Short.
   
    #    balance = 10000000
    #    call_premium = 0.10
    #    float_costs = 230000
    #    tax_rate = .25
    #    old_interest_rate = .105
    #    interest_rate = .08
    #    n_years = 20
    #    overlap_time = 30.41666666666667
    #    short_term_rate = .035

   #Part A: Cash Outflow Considerations
   net_cost_of_call_premium = int(balance) * float(call_premium)
   if enhanced_details == True:
      print(f"The net cost of the call premium is: {net_cost_of_call_premium}")
   else:
      pass

   straight_line_amortization = int(float_costs) / 5
   if enhanced_details == True:
      print(f"Amortization of floatation costs of {float_costs} is {straight_line_amortization} per year for 5 years.")
   else:
      pass

   amort_times_tax = straight_line_amortization * float(tax_rate)
   pmt = amort_times_tax
   if enhanced_details == True:
      print(f"The payment for tax savings calulation is {pmt}")
   else:
      pass

   after_tax_cost_of_new_debt = float(interest_rate) * (1-float(tax_rate))
   if enhanced_details == True:
      print(f"the after tax cost of new debt is {after_tax_cost_of_new_debt}")
   else:
      pass

   #Calculate NPV of after tax cost of new debt
   pv_tax_savings = npf.pv(after_tax_cost_of_new_debt, 5 ,pmt,0)
   if enhanced_details == True:
      print(f"the present value of tax savings is {pv_tax_savings}")
   else:
      pass

   net_borrowing_costs = float(float_costs) + pv_tax_savings
   if enhanced_details == True:
      print(f"the net borrowing costs are {net_borrowing_costs}")
   else:
      pass

   ol_old_bonds = float(old_interest_rate) * (float(overlap_time) / 365) * int(balance) * (1-float(tax_rate))
   if enhanced_details == True:
      print(f"the overlap period amount of interest owed is {ol_old_bonds}")
   else:
      pass

   ol_new_bonds = float(short_term_rate) * (float(overlap_time) / 365) * int(balance) * (1-float(tax_rate))
   if enhanced_details == True:
      print(f"the overlap period amount of interest earned is {ol_new_bonds}")
   else:
      pass

   overlap_period_value = ol_old_bonds - ol_new_bonds
   if enhanced_details == True:
      print(f"the value of the overlap period is {overlap_period_value}")
   else:
      pass

   #Part B: Cash Inflow Considerations
   after_tax_interest_savings = ((float(old_interest_rate) - float(interest_rate)) * (1-float(tax_rate))) * int(balance)
   if enhanced_details == True:
      print(f"the interest rate used for the after tax cost of interest savings is {(float(old_interest_rate) - float(interest_rate)) * (1-float(tax_rate))}")
   else:
      pass

   if enhanced_details == True:
      print(f"the after tax interest savings amount is {after_tax_interest_savings}")
   else:
      pass

   #Flip the sign of the after tax interest savings to make the math work.
   after_tax_interest_savings = -after_tax_interest_savings
   pv_inflows = npf.pv((float(interest_rate) * (1-tax_rate)), int(n_years), after_tax_interest_savings, 0)
   if enhanced_details == True:
      print(f"the pv of inflows is {pv_inflows}")
   else:
      pass

   #Part C: NPV
   total_cash_outflows = net_cost_of_call_premium + net_borrowing_costs + overlap_period_value
   total_cash_inflows = pv_inflows
   if enhanced_details == True:
      print(f"total cash outflows are {total_cash_outflows}, and total cash inflows are {total_cash_inflows}.")
   else:
      pass

   NPV = total_cash_inflows - total_cash_outflows
  
   if NPV >= 0:
      if enhanced_details == True:
         print(f"The NPV of reissuing these bonds is {NPV}, and is profitable")
      else:
         pass

   else:
      if enhanced_details == True:
         print(f"The NPV of reissuing these bonds is {NPV}, and is NOT profitable")
      else:
         pass

   return NPV

print(refund_bond_or_not())
