import streamlit as st

# --- App Config ---
st.set_page_config(
    page_title="🇳🇬 Salary Reality Calculator",
    page_icon="💰",
    layout="centered"
)

# --- Title & Intro ---
st.title("🇳🇬 Salary Reality Calculator")
st.markdown(
    """
    See what your salary *really* leaves you with each month—after tax, transport, family support, and more.
    
    Built with ❤️ for young Nigerians tired of "₦3M salary" illusions.
    """
)

# --- Input Section ---
st.header("💼 Your Details")

col1, col2 = st.columns(2)

with col1:
    gross_annual = st.number_input(
        "Gross Annual Salary (₦)",
        min_value=0,
        value=0,
        step=100_000,
        help="Your total yearly salary before deductions"
    )

with col2:
    city = st.selectbox(
        "City",
        ["Lagos", "Ibadan", "Abeokuta", "Port Harcourt", "Other"],
        help="Used to estimate transport & housing costs"
    )

# Lifestyle & Obligations
st.subheader("🧍 Your Lifestyle")
walk_to_work = st.checkbox("✅ I walk to work (save transport cost)")

st.subheader("👨‍👩‍👧 Family & Home Support")
col3, col4 = st.columns(2)
with col3:
    family_support = st.number_input(
        "Monthly to family (e.g., mum/sister) (₦)",
        min_value=0,
        value=40_000,
        step=5_000
    )
with col4:
    house_upkeep = st.number_input(
        "House contribution (₦)",
        min_value=0,
        value=50_000,
        step=5_000,
        help="If you live with family or share rent"
    )

st.subheader("🎯 Future Goal (Optional)")
goal_amount = st.number_input(
    "Goal: Save for new phones (₦)",
    min_value=0,
    value=250_000,
    step=50_000,
    help="e.g., ₦150k for you + ₦100k for mum"
)

# --- Calculations ---
gross_monthly = gross_annual / 12

# Statutory Deductions (2025 estimates)
pension = gross_monthly * 0.08
nhf = gross_monthly * 0.025

# Simplified PAYE (Progressive tax approximated for mid-income earners)
# This is a realistic effective rate for ~₦2.5M–₦4M annual income
# --- Accurate Nigerian Tax Calculation ---
def calculate_nigeria_tax(gross_annual):
    cra = max(200_000, 0.21 * gross_annual)
    taxable = max(0, gross_annual - cra)
    tax = 0
    remaining = taxable
    brackets = [(300_000, 0.07), (300_000, 0.11), (500_000, 0.15),
                (500_000, 0.19), (1_600_000, 0.21), (float('inf'), 0.24)]
    for limit, rate in brackets:
        if remaining <= 0:
            break
        chargeable = min(remaining, limit)
        tax += chargeable * rate
        remaining -= limit
    effective_rate = (tax / gross_annual) * 100 if gross_annual > 0 else 0
    return {'paye_annual': tax, 'effective_tax_rate': effective_rate}

# Use it
tax_details = calculate_nigeria_tax(gross_annual)
paye_annual = tax_details['paye_annual']
paye = paye_annual / 12  # monthly

# Keep pension & NHF as before
pension = gross_monthly * 0.08
nhf = gross_monthly * 0.025
net_after_statutory = gross_monthly - (pension + nhf + paye)
# Example usage:
if __name__ == "__main__":
    salary = 2_985_762  # Your gross annual salary
    result = calculate_nigeria_tax(salary)
    
    print(f"Gross Annual Salary: ₦{result['gross_annual']:,.2f}")
    print(f"Consolidated Relief: ₦{result['consolidated_relief']:,.2f}")
    print(f"Taxable Income: ₦{result['taxable_income']:,.2f}")
    print(f"Annual PAYE Tax: ₦{result['paye_tax']:,.2f}")
    print(f"Effective Tax Rate: {result['effective_tax_rate']}%")

# In app.py
paye_annual = calculate_nigeria_tax(gross_annual)['paye_tax']
paye = paye_annual / 12  # monthly

total_statutory = pension + nhf + paye
net_after_statutory = gross_monthly - total_statutory

# Variable Costs
if city == "Lagos":
    transport = 0 if walk_to_work else 15_000
    rent_share = 70_000
elif city in ["Ibadan", "Abeokuta"]:
    transport = 0 if walk_to_work else 8_000
    rent_share = 40_000
elif city == "Port Harcourt":
    transport = 0 if walk_to_work else 12_000
    rent_share = 55_000
else:  # Other
    transport = 0 if walk_to_work else 10_000
    rent_share = 50_000

# Total monthly outgoings
total_outgoings = transport + rent_share + family_support + house_upkeep
real_spendable = net_after_statutory - total_outgoings

# Savings projection (assuming consistent monthly saving)
if real_spendable > 0:
    max_monthly_save = min(real_spendable * 0.3, real_spendable)  # Conservative: save 30% of spendable
else:
    max_monthly_save = 0

months_to_goal = round(goal_amount / max_monthly_save) if max_monthly_save > 0 else float('inf')

# --- Results Section ---
st.divider()
st.header("💡 Your Salary Reality")

# Summary Cards
col5, col6, col7 = st.columns(3)
col5.metric("Gross Monthly", f"₦{gross_monthly:,.0f}")
col6.metric("After Tax & Pension", f"₦{net_after_statutory:,.0f}")
col7.metric("Real Spendable", f"₦{real_spendable:,.0f}")

with st.expander("🔍 See Full Breakdown"):
    st.write(f"**Gross Monthly:** ₦{gross_monthly:,.0f}")
    st.write(f"**Statutory Deductions:**")
    st.write(f"  - Pension (8%): ₦{pension:,.0f}")
    st.write(f"  - NHF (2.5%): ₦{nhf:,.0f}")
    st.write(f"  - PAYE Tax ({tax_details['effective_tax_rate']:.1f}% of gross): ₦{paye:,.0f}")
    st.write(f"**Net After Statutory:** ₦{net_after_statutory:,.0f}")
    
    st.write(f"")
    st.write(f"**Monthly Outgoings:**")
    st.write(f"  - Transport: ₦{transport:,.0f}")
    st.write(f"  - Housing: ₦{rent_share:,.0f}")
    st.write(f"  - Family Support: ₦{family_support:,.0f}")
    st.write(f"  - House Upkeep: ₦{house_upkeep:,.0f}")
    st.write(f"**Total Outgoings:** ₦{total_outgoings:,.0f}")
    
    st.write(f"")
    st.caption("💡 PAYE calculated using Nigeria’s 2025 progressive tax rates + Consolidated Relief Allowance (CRA).")
# Warning or encouragement
if real_spendable < 0:
    st.error("⚠️ Your monthly obligations exceed your take-home pay. Consider adjusting expenses or increasing income.")
elif real_spendable < 50_000:
    st.warning("⚠️ Your spendable income is tight. Small changes (e.g., walking to work) can help!")
else:
    st.success(f"✅ You have ₦{real_spendable:,.0f} left for food, personal needs, and savings!")

# Goal Tracker
if goal_amount > 0 and real_spendable > 0:
    st.subheader("📈 Your Savings Goal")
    st.write(f"If you save **₦{max_monthly_save:,.0f}/month** (30% of spendable income):")
    if months_to_goal < 12:
        st.success(f"🎉 You’ll reach your ₦{goal_amount:,.0f} goal in **{months_to_goal} months!**")
    elif months_to_goal < 24:
        st.info(f"You’ll reach your goal in about **{months_to_goal} months** (~{months_to_goal//12} year).")
    else:
        st.warning(f"It will take **{months_to_goal} months**—consider increasing savings rate or side income.")

st.caption("💡 Tip: Even ₦5k/month in CowryWise adds up over time!")

# --- Footer ---
st.divider()
st.caption("Built by a Nigerian who knows the struggle. Share with a friend who needs clarity! 💙")